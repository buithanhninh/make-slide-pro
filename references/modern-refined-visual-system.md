# Modern Refined Visual System

## Intent

Modern refined nghĩa là hierarchy rõ, whitespace rộng, geometry chính xác, contrast cao, màu tiết chế và một visual anchor đáng nhớ. Không đồng nghĩa neon, gradient ồn, dashboard card grid hoặc decoration dày đặc.

Load tokens từ `assets/style-presets/modern-refined.tokens.json`. Brand rules luôn ưu tiên hơn preset. Không tạo visual language thứ hai giữa deck.

## Composition

- Dùng canvas 16:9 và 8-point grid.
- Giữ safe inset, title rail và footer rail nhất quán.
- Chọn một reading path chính: trái sang phải, trên xuống dưới hoặc focal-to-proof.
- Dùng 1–2 columns cho evidence; card chỉ dùng khi grouping có semantic purpose.
- Giữ alignment edges, gutters và baseline rhythm ổn định.
- Dùng negative space làm structure, không làm filler.

## Color

Dùng base, surface, ink, muted, brand, accent và semantic colors từ tokens. Brand color dành cho action/emphasis, không tô mọi object. Red/green không được là phân biệt duy nhất. Danger/warning/success chỉ dùng theo meaning. Chạy contrast audit trước release.

## Typography

Dùng tối đa hai families, đều có Vietnamese glyph coverage. Primary family cho prose; numeric family cho large values khi tăng scanability. Defaults: title 32 pt, body 18 pt, minimum body 16 pt, minimum title 28 pt. Ngoại lệ phải log.

`@oai/artifact-tool` nhận font size theo CSS-pixel unit; đổi point mục tiêu sang authoring value bằng `pt × 4/3`, rồi xác minh font size thực qua PowerPoint COM. Không truyền trực tiếp token `_pt` vào `fontSize`.

Dùng sentence case, assertion title ngắn, line length kiểm soát và weight nhất quán. Tránh all-caps paragraph, faux bold, condensed font, mixed punctuation và orphaned single words. Không giải overflow bằng hidden clipping hoặc type khó đọc.

## Images and illustrations

Thứ tự ưu tiên:

1. user-provided/official product và brand assets;
2. traceable licensed/source imagery;
3. programmatic diagrams và editable charts;
4. AI-generated conceptual image chỉ khi rõ ràng là conceptual.

Ghi asset kind, role, source type, provenance, hash, dimensions, crop, alt text và slide usage. Effective PPI tối thiểu 150; hero target 180+. Giữ aspect ratio. Không fabricate logos, products, people, UI, documents, screenshots, charts hoặc evidence. Conceptual imagery giống evidence phải được disclose.

Image phải trả lời visual question: ai/ở đâu, cái gì thay đổi, hệ thống hoạt động thế nào, cảm nhận gì hoặc scale có nghĩa gì. Tránh stock-photo filler và generic silhouettes lặp lại. Dùng crop grammar và tonal treatment nhất quán.

## Illustrations and diagrams

Ưu tiên editable vector-like primitives, labels rõ và semantic palette nhỏ. Connector phải chạm node, tránh crossing và giữ reading order. Một visual metaphor trên mỗi slide. Không dùng 3D perspective nếu che comparison.

## Lucide icons

Dùng `assets/style-presets/lucide-semantic-registry.json`. Một family, một stroke language, semantic mapping đã duyệt, vector paths, size theo token scale. Không emoji, Unicode symbol thay icon, mixed filled sets hoặc icon web ngẫu nhiên. Icon hỗ trợ label; không thay primary claim.

## Charts

Chọn chart theo câu hỏi: line cho trend, bar cho comparison, dot plot cho ranking, waterfall cho bridge, scatter cho relationship, map cho geography, process diagram cho sequence. Chart phải editable. Hiển thị units, period, denominator, source và uncertainty. Axis bắt đầu zero khi magnitude comparison đòi hỏi; nếu không, đánh dấu break và giải thích. Không decorative 3D, dual axes vô cớ, unlabeled percentages hoặc color-only categories.

## Tables

Dùng table cho exact lookup, không cho dense prose. Định nghĩa header hierarchy, row heights, padding, numeric alignment, wrapping policy và source footer. Giữ text trong cell. Split hoặc chuyển detail sang appendix thay vì thu nhỏ font. Kiểm tra merged cells, borders, repeated headers và totals.

## Coverage minimum

Mọi non-title content slide có ít nhất một meaningful visual anchor. Với strategy deck 20 slide, phân bổ có chủ đích: metrics, editable charts, photos/products, system diagrams, roadmap, map, operating model, decision matrix và selected conceptual illustration. Variety phục vụ narrative, không chạy theo novelty.
