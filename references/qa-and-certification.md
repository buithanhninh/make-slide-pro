# QA And Certification

## Verification pyramid

1. **Structural** — schemas, file signatures, hashes, object IDs, counts.
2. **Semantic** — atom coverage, claims, metrics, transformations, conflicts.
3. **Native** — PowerPoint COM bounds, tables, charts, fonts, transitions, fresh-open.
4. **Rendered** — every slide PNG/PDF at full size, clipping/contrast/readability.
5. **Human judgment** — hierarchy, narrative, visual relevance, motion feel và decision clarity.

Lower layers không được bypass bằng aesthetic approval.

## Severity

- `P0`: release-stopping safety/control/evidence failure: auto-advance, fabricated evidence, source mutation, unresolved material conflict.
- `P1`: material correctness/usability failure: overflow, missing critical atom, wrong metric, broken chart/table, missing provenance, missing visual anchor, bad font/contrast.
- `P2`: significant polish hoặc maintainability issue; resolve trước premium release nếu khả thi.
- `P3`: minor refinement hoặc non-blocking note.

Open P0/P1 luôn block certified release. Waiver phải có approver, scope, reason, expiry và impact; waiver không tự biến P0/P1 thành PASS.

## Adversarial checks

- Change source sau inventory; hash gate phải block.
- Đổi extension nhưng giữ wrong signature; inventory phải flag.
- Inject conflicting metric cùng key/period/unit; reconciliation phải block.
- Remove một P0/P1 atom khỏi blueprint; coverage phải block.
- Mark AI-generated image là evidence; image audit phải block.
- Đặt text ngoài box, table cell hoặc canvas; native layout phải block.
- Dùng unsupported font hoặc emoji icon; typography/icon audit phải block.
- Set `AdvanceOnTime=true`; motion audit phải block.
- Remove render hoặc fresh-open receipt; release phải `UNVERIFIED`.
- Xóa native layout report, đổi native coverage report, đổi deck hash hoặc thiếu metadata của `visual_assets_verified`; release phải `BLOCKED`.
- Đổi blueprint/visual-assets sau coverage audit, giả `schema_version`, tạo slide number trùng/đứt quãng, làm `slide_count` lệch, hoặc để P0/P1 trong report có status `PASS`; release phải `BLOCKED`.
- Thêm receipt key ngoài exact profile set; release phải `BLOCKED`.
- Đổi certificate summary metadata nhưng giữ raw receipt, hoặc ngược lại; motion gate phải `BLOCKED`.
- Đổi raw receipt, nested native report, blueprint, asset manifest hoặc source trong khi PowerPoint đang áp motion; hậu kiểm phải xóa output và trả `BLOCKED`.
- Đặt receipt timestamp ở tương lai hoặc trước output/deck; gate phải reject.
- Đặt `asr` child directory thành junction/reparse point; ASR installer phải dừng trước khi đọc, ghi, move hoặc xóa.
- Mock hoặc giả lập `nvidia-smi` nhưng để CTranslate2 trả rỗng; probe phải giữ `selected_device=cpu`, `cuda_verified=false`.
- Cho probe output trỏ tới directory, reparse point hoặc race-prone target; probe phải trả `UNVERIFIED` và không ném exception không có receipt JSON.
- Đặt mutable-state target thành file symlink/junction; writer phải dừng trước atomic replace và không tác động target thật.
- Đổi job contract sau G0, inventory trong lúc routing, hoặc routing artifact trong lúc schema validation; intake phải `BLOCKED`.
- Làm `source_count` lệch số source records, thêm unknown property vào contract/inventory/route/storyboard, hoặc dùng schema ngoài thư mục approved; gate phải `BLOCKED`.
- Đặt `replace_existing=false`, bỏ `duration`/`delay`/`narrative_purpose`, hoặc thêm storyboard metadata runtime không có trong schema; motion phải dừng trước copy/COM.
- Dùng empty data ledger khi canonical content có metric hoặc không cung cấp canonical context; data gate phải `BLOCKED`.

## Scoring

Dùng weighted domain scores, không dùng visual enthusiasm. Domains chuẩn: source integrity, content fidelity, data accuracy, narrative logic, visual design, layout/typography, charts/tables, images/icons, motion và native compatibility. Mọi domain phải có score 0–100. Overall tối thiểu 97; từng domain tối thiểu 90.

Suggested weights: content fidelity 18, data accuracy 16, layout/typography 14, visual design 12, narrative logic 10, charts/tables 8, images/icons 7, motion 6, native compatibility 6, source integrity 3. Nếu đổi weights, ghi formula.

## Release statuses

`PASS` nghĩa required evidence đủ, capabilities verified, thresholds đạt, output tồn tại/hash khớp, native visual binding hợp lệ và không còn P0/P1. `UNVERIFIED` nghĩa output có thể tồn tại nhưng thiếu mandatory capability/evidence. `BLOCKED` nghĩa defect, conflict, unsafe operation, malformed input hoặc threshold failure chặn release.

`STATIC_READY_FOR_MOTION` không phải final release; `FINAL_RELEASE_STATIC` là static final, `FINAL_RELEASE_MOTION` là motion final. Legacy `FINAL_RELEASE` bị reject trong V6.2. Không nói "perfect" nếu không có evidence. Receipt hash không phải cryptographic authenticity. Báo exact limitation, exception và next action.

TOCTOU không thể bị loại bỏ tuyệt đối chỉ bằng path/hash checks nếu một tiến trình cùng quyền ghi có thể thay file sau lần kiểm cuối. Môi trường assurance cao cần workspace ACL riêng, process isolation và receipt/certificate có chữ ký số hoặc external attestation.
