import path from "node:path";
import { JsonInputError, assertNewOutput, loadJsonStrict, writeJsonNew } from "./safe-io.mjs";

function getArg(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index >= 0 && index + 1 < process.argv.length ? process.argv[index + 1] : fallback;
}

const assetsPath = getArg("--assets");
const registryPath = getArg("--registry");
const outputPath = getArg("--output");
if (!assetsPath || !registryPath || !outputPath) {
  console.error("Usage: node audit-icon-consistency.mjs --assets <visual-assets.json> --registry <registry.json> --output <report.json>");
  process.exit(3);
}

let outputFile;
try {
  outputFile = await assertNewOutput(outputPath, { protectedPaths: [assetsPath, registryPath] });
} catch (error) {
  console.error(String(error));
  process.exit(2);
}

try {
  const manifest = await loadJsonStrict(assetsPath);
  const registry = await loadJsonStrict(registryPath);
  const assets = Array.isArray(manifest) ? manifest : manifest.assets ?? [];
  if (!Array.isArray(assets)) throw new Error("assets must be an array");
  const icons = assets.filter((asset) => String(asset.kind ?? "").toUpperCase() === "ICON");
  const findings = [];
  const allowedNames = new Set([
    ...Object.keys(registry.icons ?? {}),
    ...Object.values(registry.semantic_registry ?? {}),
  ]);
  const family = String(registry.default_family ?? "lucide").toLowerCase();
  const defaultStroke = Number(registry.default_stroke_width ?? 1.75);
  if (!Number.isFinite(defaultStroke) || defaultStroke <= 0) throw new Error("INVALID_DEFAULT_STROKE_WIDTH");
  for (const icon of icons) {
    if (!icon || typeof icon !== "object" || Array.isArray(icon)) {
      findings.push({ severity: "P1", code: "ICON_RECORD_INVALID", detail: "icon is not an object" });
      continue;
    }
    const iconFamily = String(icon.family ?? "").toLowerCase();
    const iconName = String(icon.icon_name ?? "");
    const slide = icon.slide_number ?? null;
    const assetId = String(icon.asset_id ?? iconName ?? "unknown");
    if (iconFamily !== family) {
      findings.push({ severity: "P1", code: "ICON_FAMILY_INCONSISTENT", slide, object: assetId, detail: `family=${iconFamily} expected=${family}` });
    }
    if (!iconName || !allowedNames.has(iconName)) {
      findings.push({ severity: "P1", code: "ICON_NOT_IN_SEMANTIC_REGISTRY", slide, object: assetId, detail: iconName || "missing icon_name" });
    }
    if (String(icon.rendering ?? "vector").toLowerCase() === "unicode" || /\p{Extended_Pictographic}/u.test(iconName)) {
      findings.push({ severity: "P1", code: "UNICODE_OR_EMOJI_ICON_FORBIDDEN", slide, object: assetId, detail: iconName });
    }
    const stroke = Number(icon.stroke_width ?? defaultStroke);
    if (!Number.isFinite(stroke) || stroke <= 0 || Math.abs(stroke - defaultStroke) > 0.01) {
      findings.push({ severity: "P1", code: "ICON_STROKE_INCONSISTENT", slide, object: assetId, detail: `stroke=${stroke} expected=${defaultStroke}` });
    }
  }
  const blocked = findings.some((finding) => finding.severity === "P0" || finding.severity === "P1");
  const report = {
    schema_version: "1.0",
    generated_at: new Date().toISOString(),
    status: blocked ? "BLOCKED" : "PASS",
    assets_path: path.resolve(assetsPath),
    registry_path: path.resolve(registryPath),
    icon_count: icons.length,
    findings,
  };
  await writeJsonNew(report, outputFile);
  console.log(JSON.stringify(report, null, 2));
  process.exit(blocked ? 2 : 0);
} catch (error) {
  const blocked = error instanceof JsonInputError;
  const report = { schema_version: "1.0", generated_at: new Date().toISOString(), status: blocked ? "BLOCKED" : "UNVERIFIED", error: String(error), findings: [] };
  try {
    await writeJsonNew(report, outputFile);
  } catch {}
  console.error(JSON.stringify(report, null, 2));
  process.exit(blocked ? 2 : 3);
}
