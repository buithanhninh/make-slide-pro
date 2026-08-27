import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

export const TOKENS = {
  canvas: { width: 1280, height: 720 },
  colors: {
    base: "#F4F7FB",
    surface: "#FFFFFF",
    ink: "#102033",
    muted: "#53677D",
    line: "#D9E3EE",
    brand: "#D71920",
    accent: "#22C7E8",
    navy: "#07172E",
  },
  fonts: { primary: "Segoe UI", numeric: "Bahnschrift" },
  typographyPt: { title: 32, body: 18, small: 12, utility: 10 },
};

export function toArtifactFontSize(pointSize) {
  return Number(pointSize) * (4 / 3);
}

function addShape(slide, geometry, name, x, y, width, height, fill = "none", lineFill = "none", lineWidth = 0) {
  return slide.shapes.add({
    geometry,
    name,
    position: { left: x, top: y, width, height },
    fill,
    line: { style: "solid", fill: lineFill, width: lineWidth },
  });
}

export function addText(slide, text, options = {}) {
  const shape = addShape(
    slide,
    "textbox",
    options.name,
    options.x ?? 0,
    options.y ?? 0,
    options.width ?? 400,
    options.height ?? 48,
    options.fill ?? "none",
    options.lineFill ?? "none",
    options.lineWidth ?? 0,
  );
  shape.text = String(text);
  shape.text.style = {
    fontSize: toArtifactFontSize(options.fontSizePt ?? TOKENS.typographyPt.body),
    typeface: options.typeface ?? TOKENS.fonts.primary,
    color: options.color ?? TOKENS.colors.ink,
    bold: options.bold ?? false,
  };
  shape.text.alignment = options.alignment ?? "left";
  shape.text.verticalAlignment = options.verticalAlignment ?? "middle";
  shape.text.autoFit = "shrinkText";
  shape.text.wrap = "square";
  shape.text.insets = options.insets ?? { top: 0, right: 0, bottom: 0, left: 0 };
  return shape;
}

export function addModernChrome(slide, { section = "SECTION", slideNumber = 1, title = "Evidence-backed growth system" } = {}) {
  slide.background.fill = TOKENS.colors.base;
  addShape(slide, "rect", "chrome-top-rule", 0, 0, 1280, 5, `linear(0deg, ${TOKENS.colors.brand} 0%, ${TOKENS.colors.accent} 100%)`);
  addText(slide, "MAKE SLIDE PRO • MODERN REFINED", { x: 56, y: 20, width: 420, height: 22, fontSizePt: 11, bold: true, color: TOKENS.colors.brand });
  addText(slide, section, { x: 1010, y: 20, width: 150, height: 22, fontSizePt: 11, bold: true, color: TOKENS.colors.navy, alignment: "right" });
  addText(slide, String(slideNumber).padStart(2, "0"), { x: 1175, y: 20, width: 48, height: 22, fontSizePt: 12, bold: true, color: TOKENS.colors.muted, typeface: TOKENS.fonts.numeric, alignment: "right" });
  addText(slide, title, { name: "A01_TITLE", x: 56, y: 56, width: 1168, height: 74, fontSizePt: TOKENS.typographyPt.title, bold: true, color: TOKENS.colors.ink });
  addShape(slide, "line", "chrome-footer-rule", 56, 684, 1168, 0, "none", TOKENS.colors.line, 1);
  addText(slide, "SOURCE TRACEABILITY • STATIC FIRST • CLICK CONTROLLED", { x: 56, y: 690, width: 640, height: 18, fontSizePt: TOKENS.typographyPt.utility, bold: true, color: TOKENS.colors.muted });
}

export function buildStarterDeck({ slideCount = 1 } = {}) {
  const presentation = Presentation.create({ slideSize: TOKENS.canvas });
  for (let index = 0; index < slideCount; index += 1) {
    const slide = presentation.slides.add();
    addModernChrome(slide, { slideNumber: index + 1, title: "Evidence-backed growth system" });
    addText(slide, "One claim, one meaningful visual anchor, one traceable source path.", { x: 56, y: 184, width: 560, height: 96, fontSizePt: TOKENS.typographyPt.body, color: TOKENS.colors.muted });
  }
  return presentation;
}

export async function exportDeck(presentation, outputPath) {
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(outputPath);
  return outputPath;
}

export async function exportSlideLayouts(presentation, outputDirectory) {
  await fs.mkdir(outputDirectory, { recursive: true });
  for (let index = 0; index < presentation.slides.items.length; index += 1) {
    const slide = presentation.slides.getItem(index);
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(`${outputDirectory}/${stem}.layout.json`, await layout.text());
  }
}
