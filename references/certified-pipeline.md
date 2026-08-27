# Certified Pipeline V5.0

## Mục tiêu

Pipeline biến nguồn hỗn hợp thành deck PowerPoint hiện đại, editable, có thể truy nguyên và có bằng chứng kiểm định. `PASS` chỉ được cấp khi toàn bộ gate bắt buộc có receipt hợp lệ; thiếu công cụ, thiếu receipt hoặc còn lỗi nghiêm trọng thì không được suy đoán thành đạt.

## State machine

```text
INTAKE
  -> CAPABILITY_READY
  -> SOURCE_LOCKED
  -> EXTRACTED
  -> CANONICALIZED
  -> RECONCILED
  -> COVERAGE_LOCKED
  -> NARRATIVE_SELECTED
  -> BLUEPRINT_CERTIFIED
  -> ART_DIRECTION_SELECTED
  -> PROTOTYPE_CERTIFIED
  -> STATIC_AUTHORED
  -> STATIC_CERTIFIED
  -> MOTION_AUTHORED
  -> MOTION_CERTIFIED
  -> ADVERSARIAL_QA_PASS
  -> RELEASE_CERTIFIED
```

Mỗi trạng thái phải có receipt trong workspace. Không nhảy trạng thái. Gate thất bại quay về stage sở hữu lỗi, sau đó chạy lại mọi stage downstream. `run-pipeline.ps1` chỉ thực hiện intake bootstrap đến `G2_ROUTING_DECISION`; nó không chạy adapter, authoring, static certification hay release certification.

## Gate contract

### G0 — Job contract

Tạo `job-contract.json` versioned và validate bằng `job-contract.schema.json` plus semantic validator trước G1. Ghi audience, purpose, desired action, language, `duration_minutes` kể cả `null`, modifiers kể cả mảng rỗng, slide-count policy, preservation mode, content-change budget, visual direction, motion level, confidentiality và output contract. Primary operation, modifiers, preservation mode và certification mode trong contract là nguồn quyết định routing; CLI operation xung đột phải `BLOCKED`. `LOCKED` không cho derive, reorder, omission hoặc đổi sequence. `CERTIFIED` yêu cầu source notes và full evidence package. Nếu người dùng không nêu, agent phải ghi default explicit: `CERTIFIED`, `MODERN_REFINED`, click-controlled và giữ nguyên ý nghĩa nguồn.

### G1 — Capability and security

Kiểm tra PowerPoint COM, Node runtime, Python, FFmpeg/FFprobe, OCR, font, disk, macro/external-link risk và ASR. Với `@oai/artifact-tool`, phải import thật entrypoint `dist/artifact_tool.mjs` bằng runtime Node; thư mục package tồn tại không đủ. Capability thiếu hoặc import fail làm certification ceiling xuống `UNVERIFIED`; không tự thay bằng tool không được phê duyệt.

### G2 — Source inventory and authority

Phân loại bằng file signature và package contents, tạo SHA-256, source role, authority, lineage, exclusion và risk flags. Inventory và routing decision phải validate bằng `source-manifest.schema.json` và `routing-decision.schema.json`; `source_count` phải bằng số record. Job contract, source set, inventory và routing artifact được hash trước/sau downstream use. Nguồn không được sửa. Macro, corrupt archive, extension mismatch hoặc provenance không rõ phải được đánh dấu.

Router validate enum contract trước khi dùng: operation, từng modifier, preservation mode và certification mode phải nằm trong tập enum tương ứng của routing-decision schema. Giá trị ngoài enum ghi fallback BLOCKED có schema-valid structure. Khi contract được truyền, router lấy modifiers chỉ từ contract, không bổ sung modifier phát sinh từ source families. Mỗi modifier phải có source family tương ứng: `REPAIR` cần deck, `UPDATE_DATA` cần deck + data, `TRANSCRIBE_MEDIA` cần audio/video, `EXTRACT_ARCHIVE` cần archive, `RECONCILE_SOURCES` cần ≥ 2 sources. Pipeline kiểm tra exact modifier binding giữa route và contract; lệch là `BLOCKED`.

Gate receipt được ghi bằng `Add-ValidatedGateReceipt`: artifact phải đúng JSON object với `status` khớp trước khi receipt được confirm; artifact malformed ghi receipt `BLOCKED` với reason `ARTIFACT_VALIDATION_FAILED`. Python runtime cho pipeline phải là Application executable (`Get-Command -CommandType Application`); script/alias/function/reparse bị từ chối.

### G3 — Format adapters

Mỗi loại file dùng adapter riêng. Adapter ghi coverage (`processed`/`total`), artifact paths, hash và risks. Archive phải qua safe listing/containment check trước member routing; không execute member. Render/native inspection là evidence bổ sung, không thay extraction có cấu trúc.

### G4 — Canonical evidence

Chuyển nội dung thành atoms, claims, metrics, facts, assumptions, risks, decisions, actions, caveats, methodology và dependencies. Mỗi atom có locator, verbatim, normalized meaning, priority, confidence và destination.

### G5 — Reconciliation

Đối chiếu số liệu giữa document, deck, spreadsheet, PDF và transcript. So cùng metric key, period, unit, denominator và actual/forecast state. Conflict chưa resolution là `BLOCKED`; không chọn số “có vẻ hợp lý”.

### G6 — Fidelity and coverage

Mỗi atom phải vào `VISIBLE_SLIDE`, `SPEAKER_NOTES`, `APPENDIX` hoặc `INTENTIONALLY_OMITTED`. Atom P0/P1 hoặc `must_preserve=true` không được bỏ. Mọi compression, reorder, derivation và omission ghi difference log. `OMIT_WITH_APPROVAL` được phép có `meaning_preserved=false` chỉ khi approval đầy đủ; meaning loss khác không được `APPROVED`.

### G7 — Narrative architecture

Tạo ít nhất ba narrative candidates. Chấm theo audience relevance, evidence strength, decision clarity, flow, cognitive load và source fidelity. Chọn một candidate, ghi deck thesis, section thesis và question-answer chain.

### G8 — Slide blueprint

Mỗi slide có assertion title, primary claim, source atoms, primary evidence, implication, role, visual job, visual anchor, transition, motion beats, notes và appendix refs. Content slide phải có một visual anchor có ý nghĩa; decorative-only không đủ.

### G9 — Art direction

Tạo tối thiểu ba hướng visual bám audience, brand và evidence. Chọn một hệ `MODERN_REFINED` có token màu, typography, spacing, radius, shadow, icon registry, chart grammar, table grammar, imagery và visual rhythm. Mỗi content slide phải có visual anchor có ý nghĩa; không dùng decorative-only để lấp khoảng trống.

### G10 — Representative prototype

Dựng và review tối thiểu opening, dense data, complex concept, image/illustration và decision slide. Kiểm tra hierarchy, font fallback, chart/table behavior, visual anchor, content density và motion feasibility trước khi nhân rộng.

### G11 — Static production

Dùng `@oai/artifact-tool` ES modules. Giữ chart/table editable. Tạo output mới trong workspace riêng, không ghi đè source. Blueprint phải validate trước authoring.

### G12 — Static certification

Kiểm tra source traceability, data, images, contrast, icons, typography, native geometry, text containment, overlap, canvas bounds, placeholders, charts/tables, render set, fresh-open và native visual coverage. `visual_assets_verified` phải mang metadata trỏ tới coverage report, report SHA-256 và deck SHA-256; coverage report phải bind tiếp blueprint path/hash, asset-manifest path/hash và native layout path/hash. Schema version, slide count, unique/continuous slide sequence, shape/object counts và zero P0/P1 phải khớp. Static fail thì chưa được viết motion.

### G13 — Native motion

Chỉ chạy sau `STATIC_CERTIFIED`. Motion storyboard phải đúng schema, `replace_existing=true`, click-controlled, không auto-advance. Mỗi beat có exact shape names, effect, trigger, explicit duration, explicit delay và non-empty narrative purpose. Runtime không nhận field ngoài schema và không dùng timing mặc định. Native PowerPoint COM áp dụng transition/timeline và ghi receipt.

### G14 — Motion QA

Kiểm tra effect type, trigger, duration, delay, count, accidental auto-advance, missing shapes và end-frame equivalence. Render static và final end-frame; mismatch ngoài ngưỡng là `BLOCKED`.

### G15 — Independent, adversarial QA and release certification

`certify-release.ps1` tổng hợp exact receipt set của profile. Điều kiện `PASS`: quality score tối thiểu `97`, mọi domain tối thiểu `90`, zero P0/P1, source hash unchanged, output tồn tại và hash khớp, toàn bộ evidence boolean đạt, native visual binding hợp lệ, static/motion equivalent và fresh PowerPoint open thành công. Certifier tự tính weighted score `WEIGHTED_DOMAIN_V1`; không tin score do caller gửi nếu lệch quá `0.05`. Trước ghi certificate, release input, sources, output, receipts và nested native binding chain được rehash/revalidate lần cuối.

`STATIC_READY_FOR_MOTION` chỉ chứng nhận static gates và loại `motion` khỏi domain/evidence. `FINAL_RELEASE_STATIC` chứng nhận static final release. `FINAL_RELEASE_MOTION` bắt buộc motion gates và end-frame equivalence. Legacy `FINAL_RELEASE` bị reject trong V6.2. Không dùng static certificate làm final release certificate.

Trước certificate phải có blind review/fresh process, slideshow test, PDF export, long-string, locale, projector, grayscale, color-blind và media checks. Thiếu receipt, malformed payload, capability chưa xác minh hoặc unresolved exception không được nâng thành `PASS`.

## Evidence bundle

Tối thiểu gồm `job-contract.json`, `job-contract-validation.json`, `run-manifest.json`, `capability-report.json`, `source-inventory.json`, `source-inventory.validation.json`, `routing-decision.json`, `routing-decision.validation.json`, canonical atoms, claim/data ledgers, evidence/narrative graphs, coverage matrix, blueprints, asset manifest, static QA reports, render manifest, motion storyboard/report, content comparison, final certificate và source/output hashes.

Source, canonical ledgers, certified blueprints, visual-asset manifest, deck, QA report và receipt là immutable trong downstream gates. Run manifest/cache có thể mutable theo contract; mutable JSON writer phải chặn reparse target/ancestor và dùng create-new temp + atomic replace. Receipt hash chỉ phát hiện thay đổi sau khi receipt được tạo; không phải chữ ký số và không chứng minh nguồn gốc người tạo.

Hash source dùng `SOURCE_FILE_SHA256_OR_SET_V1`: một source dùng file SHA-256; nhiều source dùng SHA-256 của các record đã sort theo dạng `source_id + U+001F + normalized_path + U+001F + actual_sha256`, nối bằng LF. Receipt `generated_at` phải có timezone, không vượt quá hiện tại năm phút và không cũ hơn output/deck năm phút.

## Fail-closed rules

- Thiếu capability bắt buộc: `UNVERIFIED`.
- Conflict số liệu, source hash đổi, P0/P1 còn mở, blueprint thiếu coverage hoặc visual evidence giả: `BLOCKED`.
- Không dùng montage thay review từng slide.
- File mở được không có nghĩa layout đúng.
- Nhiều effect không có nghĩa motion tốt.
- Native visual report thiếu, sai hash, sai deck binding hoặc thiếu slide binding: `BLOCKED`.
- Blueprint/asset hash đổi, slide count/sequence sai, layout object count sai, report schema sai hoặc report `PASS` còn P0/P1: `BLOCKED`.
- Receipt container có key thừa hoặc binding đổi trong lúc certification/motion: `BLOCKED`.
- Job contract đổi sau G0, inventory đổi trong routing, routing artifact đổi trong schema validation, `source_count` lệch, hoặc schema có unknown property: `BLOCKED`.
- Empty data ledger chỉ được `PASS` khi canonical content đã được kiểm tra và không chứa metric; thiếu canonical context là `BLOCKED`.
- `ensure-faster-whisper.ps1` dùng mutex theo cache; cài đặt theo giao dịch staging → probe → publish, lỗi probe sau publish phải rollback và ghi `rollback_restored`/`rollback_errors`.
