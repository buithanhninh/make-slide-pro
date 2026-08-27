import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { JsonInputError, assertNewOutput, assertRegularInputFile, loadJsonStrict, writeJsonNew } from "./safe-io.mjs";

function getArg(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 && index + 1 < process.argv.length ? process.argv[index + 1] : null;
}

async function sha256File(filePath) {
  return crypto.createHash("sha256").update(await fs.readFile(filePath)).digest("hex");
}

const blueprintsPath = getArg("--blueprints");
const assetsPath = getArg("--assets");
const layoutReportPath = getArg("--layout-report");
const requireNativeBindings = process.argv.includes("--require-native-bindings");
const outputPath = getArg("--output");
if (!blueprintsPath || !assetsPath || !outputPath) {
  console.error("Usage: node audit-visual-coverage.mjs --blueprints <slide-blueprints.json> --assets <visual-assets.json> [--layout-report <native-layout.json> --require-native-bindings] --output <report.json>");
  process.exit(3);
}

let outputFile;
try {
  outputFile = await assertNewOutput(outputPath, { protectedPaths: [blueprintsPath, assetsPath, ...(layoutReportPath ? [layoutReportPath] : [])] });
} catch (error) {
  console.error(String(error));
  process.exit(2);
}

try {
  const resolvedBlueprintsPath = await assertRegularInputFile(blueprintsPath, "BLUEPRINTS");
  const resolvedAssetsPath = await assertRegularInputFile(assetsPath, "VISUAL_ASSETS");
  const blueprintsSha256Before = await sha256File(resolvedBlueprintsPath);
  const assetsSha256Before = await sha256File(resolvedAssetsPath);
  const blueprintsPayload = await loadJsonStrict(resolvedBlueprintsPath);
  const assetsPayload = await loadJsonStrict(resolvedAssetsPath);
  const slides = Array.isArray(blueprintsPayload) ? blueprintsPayload : blueprintsPayload?.slides;
  if (!Array.isArray(slides)) throw new Error("blueprint slides must be an array");
  const assets = Array.isArray(assetsPayload) ? assetsPayload : assetsPayload?.assets;
  if (!Array.isArray(assets)) throw new Error("visual assets must be an array");
  const findings = [];
  if (!blueprintsPayload || typeof blueprintsPayload !== "object" || Array.isArray(blueprintsPayload) || blueprintsPayload.schema_version !== "1.0") {
    findings.push({ severity: "P1", code: "BLUEPRINT_SCHEMA_VERSION_INVALID", detail: String(blueprintsPayload?.schema_version ?? "missing") });
  }
  if (!assetsPayload || typeof assetsPayload !== "object" || Array.isArray(assetsPayload) || assetsPayload.schema_version !== "1.0") {
    findings.push({ severity: "P1", code: "VISUAL_ASSETS_SCHEMA_VERSION_INVALID", detail: String(assetsPayload?.schema_version ?? "missing") });
  }
  let nativeBindingsUnverified = false;
  let nativeBindingsVerified = false;
  let nativeObjectsBySlide = new Map();
  let nativeDeckPath = null;
  let nativeDeckSha256 = null;
  let nativeDeckSha256Before = null;
  let nativeLayoutReportSha256 = null;
  let resolvedLayoutReportPath = null;
  if (requireNativeBindings && !layoutReportPath) {
    nativeBindingsUnverified = true;
    findings.push({ severity: "INFO", code: "NATIVE_LAYOUT_REPORT_MISSING", detail: "Native object binding requires audit-native-layout.ps1 output." });
  }
  if (layoutReportPath) {
    resolvedLayoutReportPath = await assertRegularInputFile(layoutReportPath, "NATIVE_LAYOUT_REPORT");
    nativeLayoutReportSha256 = await sha256File(resolvedLayoutReportPath);
    const layoutPayload = await loadJsonStrict(resolvedLayoutReportPath);
    if (!layoutPayload || typeof layoutPayload !== "object" || Array.isArray(layoutPayload)) throw new Error("native layout report must be an object");
    const layoutStatus = String(layoutPayload.status ?? "").toUpperCase();
    const declaredDeckPath = typeof layoutPayload.deck_path === "string" ? layoutPayload.deck_path.trim() : "";
    const declaredDeckHash = String(layoutPayload.deck_sha256 ?? "").toLowerCase();
    const hashBefore = String(layoutPayload.deck_sha256_before ?? "").toLowerCase();
    const hashAfter = String(layoutPayload.deck_sha256_after ?? "").toLowerCase();
    if (layoutStatus === "BLOCKED") {
      findings.push({ severity: "P1", code: "NATIVE_LAYOUT_REPORT_BLOCKED", detail: String(layoutPayload.error ?? "layout report status BLOCKED") });
    } else if (layoutStatus !== "PASS") {
      nativeBindingsUnverified = true;
      findings.push({ severity: "INFO", code: "NATIVE_LAYOUT_REPORT_NOT_PASS", detail: `status=${layoutStatus || "MISSING"}` });
    }
    if (!declaredDeckPath) {
      findings.push({ severity: "P1", code: "NATIVE_LAYOUT_DECK_PATH_INVALID", detail: "deck_path must be a non-empty string" });
    } else {
      try {
        nativeDeckPath = await assertRegularInputFile(path.resolve(declaredDeckPath), "NATIVE_DECK");
        nativeDeckSha256Before = await sha256File(nativeDeckPath);
        nativeDeckSha256 = nativeDeckSha256Before;
      } catch (error) {
        findings.push({ severity: "P1", code: "NATIVE_LAYOUT_DECK_PATH_INVALID", detail: String(error) });
      }
    }
    if (
      !/^[a-f0-9]{64}$/.test(declaredDeckHash)
      || !/^[a-f0-9]{64}$/.test(hashBefore)
      || !/^[a-f0-9]{64}$/.test(hashAfter)
      || declaredDeckHash !== hashBefore
      || hashBefore !== hashAfter
    ) {
      findings.push({ severity: "P1", code: "NATIVE_LAYOUT_DECK_HASH_INVALID", detail: `declared=${declaredDeckHash || "missing"} before=${hashBefore || "missing"} after=${hashAfter || "missing"}` });
    }
    if (nativeDeckSha256Before && /^[a-f0-9]{64}$/.test(hashAfter) && nativeDeckSha256Before !== hashAfter) {
      findings.push({ severity: "P1", code: "NATIVE_DECK_HASH_MISMATCH", detail: `reported=${hashAfter} actual=${nativeDeckSha256Before}` });
    }
    if (layoutPayload.schema_version !== "1.0") {
      findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SCHEMA_VERSION_INVALID", detail: String(layoutPayload.schema_version ?? "missing") });
    }
    if (!Array.isArray(layoutPayload.findings)) {
      findings.push({ severity: "P1", code: "NATIVE_LAYOUT_FINDINGS_INVALID", detail: "findings must be an array" });
    } else {
      const allowedSeverities = new Set(["P0", "P1", "P2", "P3", "INFO"]);
      let hasCriticalFinding = false;
      for (const [index, finding] of layoutPayload.findings.entries()) {
        const severity = String(finding?.severity ?? "").toUpperCase();
        const code = typeof finding?.code === "string" ? finding.code : "";
        const detail = typeof finding?.detail === "string" ? finding.detail : "";
        if (
          !finding
          || typeof finding !== "object"
          || Array.isArray(finding)
          || !allowedSeverities.has(severity)
          || !/^[A-Z][A-Z0-9_]{2,}$/.test(code)
          || !detail.trim()
        ) {
          findings.push({ severity: "P1", code: "NATIVE_LAYOUT_FINDING_RECORD_INVALID", detail: `findings[${index}]` });
          continue;
        }
        if (["P0", "P1"].includes(severity)) hasCriticalFinding = true;
      }
      if (hasCriticalFinding) findings.push({ severity: "P1", code: "NATIVE_LAYOUT_CRITICAL_FINDINGS", detail: "layout report contains P0/P1 findings" });
    }
    if (!Array.isArray(layoutPayload.slides)) {
      findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SLIDES_INVALID", detail: "slides must be an array" });
    } else {
      const declaredSlideCount = Number(layoutPayload.slide_count);
      const layoutSlideNumbers = [];
      const uniqueLayoutSlideNumbers = new Set();
      if (!Number.isInteger(declaredSlideCount) || declaredSlideCount < 1 || declaredSlideCount !== layoutPayload.slides.length) {
        findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SLIDE_COUNT_INVALID", detail: `declared=${layoutPayload.slide_count} actual=${layoutPayload.slides.length}` });
      }
      if (Number.isInteger(declaredSlideCount) && declaredSlideCount !== slides.length) {
        findings.push({ severity: "P1", code: "NATIVE_LAYOUT_BLUEPRINT_SLIDE_COUNT_MISMATCH", detail: `layout=${declaredSlideCount} blueprints=${slides.length}` });
      }
      for (const [index, slide] of layoutPayload.slides.entries()) {
        if (!slide || typeof slide !== "object" || Array.isArray(slide)) {
          findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SLIDE_RECORD_INVALID", detail: `slides[${index}]` });
          continue;
        }
        const slideNumber = Number(slide.slide);
        layoutSlideNumbers.push(slideNumber);
        if (!Number.isInteger(slideNumber) || slideNumber < 1 || (Number.isInteger(declaredSlideCount) && slideNumber > declaredSlideCount) || uniqueLayoutSlideNumbers.has(slideNumber)) {
          continue;
        }
        uniqueLayoutSlideNumbers.add(slideNumber);
        if (!Array.isArray(slide.objects)) {
          findings.push({ severity: "P1", code: "NATIVE_LAYOUT_OBJECTS_INVALID", slide: slideNumber, detail: `slides[${index}].objects` });
          continue;
        }
        const shapeCount = Number(slide.shape_count);
        if (!Number.isInteger(shapeCount) || shapeCount < 0) {
          findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SHAPE_COUNT_INVALID", slide: slideNumber, detail: String(slide.shape_count ?? "missing") });
        } else if (shapeCount !== slide.objects.length) {
          findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SHAPE_COUNT_MISMATCH", slide: slideNumber, detail: `declared=${shapeCount} actual=${slide.objects.length}` });
        }
        const names = new Set();
        for (const [objectIndex, object] of slide.objects.entries()) {
          if (!object || typeof object !== "object" || Array.isArray(object) || typeof object.name !== "string" || !object.name.trim()) {
            findings.push({ severity: "P1", code: "NATIVE_LAYOUT_OBJECT_NAME_INVALID", slide: slideNumber, detail: `objects[${objectIndex}]` });
            continue;
          }
          const normalizedName = object.name.trim().toLowerCase();
          if (names.has(normalizedName)) {
            findings.push({ severity: "P1", code: "NATIVE_LAYOUT_OBJECT_NAME_DUPLICATE", slide: slideNumber, object: object.name.trim(), detail: object.name.trim() });
            continue;
          }
          names.add(normalizedName);
        }
        nativeObjectsBySlide.set(slideNumber, names);
      }
      const expectedLayoutSlideNumbers = Number.isInteger(declaredSlideCount) && declaredSlideCount > 0
        ? Array.from({ length: declaredSlideCount }, (_, index) => index + 1)
        : [];
      if (uniqueLayoutSlideNumbers.size !== layoutPayload.slides.length || expectedLayoutSlideNumbers.some((slideNumber) => !uniqueLayoutSlideNumbers.has(slideNumber))) {
        findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SLIDE_SEQUENCE_INVALID", detail: layoutSlideNumbers.join(",") });
      }
      if (layoutStatus === "PASS") nativeBindingsVerified = true;
    }
  }
  if (slides.length === 0) findings.push({ severity: "P1", code: "EMPTY_BLUEPRINT", detail: "No slide blueprints supplied." });
  const validAssets = assets.filter((asset, index) => {
    if (asset && typeof asset === "object" && !Array.isArray(asset)) return true;
    findings.push({ severity: "P1", code: "VISUAL_ASSET_RECORD_INVALID", detail: `assets[${index}] is not an object` });
    return false;
  });
  const assetById = new Map();
  for (const [index, asset] of validAssets.entries()) {
    const assetId = String(asset.asset_id ?? "").trim();
    if (!assetId) {
      findings.push({ severity: "P1", code: "VISUAL_ASSET_ID_MISSING", detail: `assets[${index}]` });
      continue;
    }
    if (assetById.has(assetId)) findings.push({ severity: "P1", code: "DUPLICATE_VISUAL_ASSET_ID", object: assetId, detail: assetId });
    assetById.set(assetId, asset);
    const assetSlideNumber = Number(asset.slide_number);
    if (!Number.isInteger(assetSlideNumber) || assetSlideNumber < 1 || assetSlideNumber > slides.length) {
      findings.push({ severity: "P1", code: "VISUAL_ASSET_SLIDE_NUMBER_INVALID", object: assetId, detail: String(asset.slide_number ?? "missing") });
    }
  }
  const exemptRoles = new Set(["TITLE", "CLOSING"]);
  const idsFrom = (value) => Array.isArray(value) ? value.map(String) : [];
  const slideIds = new Set();
  const slideNumbers = new Set();
  let slideSequenceInvalid = false;
  for (const [index, slide] of slides.entries()) {
    if (!slide || typeof slide !== "object" || Array.isArray(slide)) {
      findings.push({ severity: "P1", code: "INVALID_SLIDE_RECORD", detail: `slides[${index}] is not an object` });
      continue;
    }
    const slideId = String(slide.slide_id ?? "").trim();
    if (slideId && slideIds.has(slideId)) findings.push({ severity: "P1", code: "DUPLICATE_SLIDE_ID", slide: slide.slide_number ?? null, detail: slideId });
    if (slideId) slideIds.add(slideId);
    const role = String(slide.role ?? "").toUpperCase();
    const slideNumber = Number(slide.slide_number);
    if (!Number.isInteger(slideNumber) || slideNumber < 1 || slideNumber > slides.length || slideNumbers.has(slideNumber)) {
      slideSequenceInvalid = true;
    } else {
      slideNumbers.add(slideNumber);
    }
    if (exemptRoles.has(role)) continue;
    const anchor = slide.visual_anchor;
    if (!anchor || typeof anchor !== "object" || !anchor.kind || !Array.isArray(anchor.asset_or_object_ids) || anchor.asset_or_object_ids.length === 0) {
      findings.push({ severity: "P1", code: "MEANINGFUL_VISUAL_ANCHOR_MISSING", slide: slideNumber, detail: slideId });
      continue;
    }
    const declaredObjectIds = new Set([
      ...idsFrom(slide.chart_ids),
      ...idsFrom(slide.table_ids),
      ...idsFrom(slide.diagram_ids),
      ...idsFrom(slide.metric_object_ids),
    ].map(String));
    const unresolved = anchor.asset_or_object_ids.map(String).filter((id) => !assetById.has(id) && !declaredObjectIds.has(id));
    if (unresolved.length > 0) {
      findings.push({ severity: "P1", code: "VISUAL_ANCHOR_REFERENCE_MISSING", slide: slideNumber, detail: unresolved.join(",") });
    }
    const referencedAssets = anchor.asset_or_object_ids.map(String).map((id) => assetById.get(id)).filter(Boolean);
    if (referencedAssets.length > 0 && referencedAssets.every((asset) => ["DECORATIVE", "NAVIGATION"].includes(String(asset.role ?? "").toUpperCase()))) {
      findings.push({ severity: "P1", code: "VISUAL_ANCHOR_IS_DECORATIVE_ONLY", slide: slideNumber, detail: anchor.asset_or_object_ids.join(",") });
    }
    for (const asset of referencedAssets) {
      if (String(asset.kind ?? "").toUpperCase() === "DATA_VISUAL" && asset.editable !== true) {
        findings.push({ severity: "P1", code: "FLATTENED_DATA_VISUAL", slide: slideNumber, object: asset.asset_id, detail: "editable must be true" });
      }
    }
    if (requireNativeBindings && layoutReportPath) {
      const nativeNames = nativeObjectsBySlide.get(Number(slideNumber));
      if (!nativeNames) {
        findings.push({ severity: "P1", code: "NATIVE_LAYOUT_SLIDE_MISSING", slide: slideNumber, detail: slideId });
      } else {
        for (const referenceId of anchor.asset_or_object_ids.map(String)) {
          const asset = assetById.get(referenceId);
          if (asset && Number(asset.slide_number) !== Number(slideNumber)) {
            findings.push({ severity: "P1", code: "VISUAL_ASSET_SLIDE_BINDING_MISMATCH", slide: slideNumber, object: referenceId, detail: `asset_slide=${asset.slide_number}` });
            continue;
          }
          const nativeObjectName = String(asset?.native_object_name ?? referenceId).trim();
          if (!nativeObjectName || !nativeNames.has(nativeObjectName.toLowerCase())) {
            findings.push({ severity: "P1", code: "VISUAL_ANCHOR_NATIVE_OBJECT_MISSING", slide: slideNumber, object: referenceId, detail: `native_object_name=${nativeObjectName || "missing"}` });
          }
        }
      }
    }
  }
  if (Array.from({ length: slides.length }, (_, index) => index + 1).some((slideNumber) => !slideNumbers.has(slideNumber))) {
    slideSequenceInvalid = true;
  }
  if (slideSequenceInvalid) findings.push({ severity: "P1", code: "BLUEPRINT_SLIDE_SEQUENCE_INVALID", detail: [...slideNumbers].sort((a, b) => a - b).join(",") });
  const blueprintsSha256After = await sha256File(resolvedBlueprintsPath);
  const assetsSha256After = await sha256File(resolvedAssetsPath);
  if (blueprintsSha256After !== blueprintsSha256Before) findings.push({ severity: "P1", code: "BLUEPRINTS_CHANGED_DURING_VISUAL_AUDIT", detail: resolvedBlueprintsPath });
  if (assetsSha256After !== assetsSha256Before) findings.push({ severity: "P1", code: "VISUAL_ASSETS_CHANGED_DURING_AUDIT", detail: resolvedAssetsPath });
  if (resolvedLayoutReportPath) {
    const nativeLayoutReportSha256After = await sha256File(resolvedLayoutReportPath);
    if (nativeLayoutReportSha256After !== nativeLayoutReportSha256) findings.push({ severity: "P1", code: "NATIVE_LAYOUT_REPORT_CHANGED_DURING_VISUAL_AUDIT", detail: resolvedLayoutReportPath });
  }
  if (nativeDeckPath && nativeDeckSha256Before) {
    try {
      const resolvedNativeDeckPathAfter = await assertRegularInputFile(nativeDeckPath, "NATIVE_DECK");
      const nativeDeckSha256After = await sha256File(resolvedNativeDeckPathAfter);
      if (nativeDeckSha256After !== nativeDeckSha256Before) findings.push({ severity: "P1", code: "NATIVE_DECK_CHANGED_DURING_VISUAL_AUDIT", detail: nativeDeckPath });
      nativeDeckSha256 = nativeDeckSha256After;
    } catch (error) {
      findings.push({ severity: "P1", code: "NATIVE_DECK_CHANGED_DURING_VISUAL_AUDIT", detail: String(error) });
    }
  }
  const blocked = findings.some((finding) => finding.severity === "P0" || finding.severity === "P1");
  const status = blocked ? "BLOCKED" : nativeBindingsUnverified ? "UNVERIFIED" : "PASS";
  const report = {
    schema_version: "1.0",
    generated_at: new Date().toISOString(),
    status,
    blueprints_path: resolvedBlueprintsPath,
    blueprints_sha256: blueprintsSha256After,
    assets_path: resolvedAssetsPath,
    assets_sha256: assetsSha256After,
    native_bindings_required: requireNativeBindings,
    native_layout_report_path: resolvedLayoutReportPath,
    native_layout_report_sha256: nativeLayoutReportSha256,
    native_deck_path: nativeDeckPath,
    native_deck_sha256: nativeDeckSha256,
    native_bindings_verified: requireNativeBindings ? nativeBindingsVerified && !nativeBindingsUnverified && !blocked : null,
    slide_count: slides.length,
    findings,
  };
  await writeJsonNew(report, outputFile);
  console.log(JSON.stringify(report, null, 2));
  process.exit(blocked ? 2 : nativeBindingsUnverified ? 3 : 0);
} catch (error) {
  const blocked = error instanceof JsonInputError;
  const report = { schema_version: "1.0", generated_at: new Date().toISOString(), status: blocked ? "BLOCKED" : "UNVERIFIED", error: String(error), findings: [] };
  try {
    await writeJsonNew(report, outputFile);
  } catch {}
  console.error(JSON.stringify(report, null, 2));
  process.exit(blocked ? 2 : 3);
}
