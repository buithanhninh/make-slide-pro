# Script Contracts

## General

Chạy từ skill `scripts`. Paths là absolute hoặc được resolve. JSON output là UTF-8, structure deterministic và chỉ ghi vào output path được chỉ định. Exit codes:

- `0`: `PASS`;
- `2`: `BLOCKED`;
- `3`: `UNVERIFIED` hoặc capability unavailable.

Không dùng source path làm output path. Script mutation không âm thầm overwrite output đã có.

## Intake

```powershell
python validate-job-contract.py --input <job-contract.json> --output <workspace>/job-contract-validation.json
pwsh -File preflight.ps1 -OutputPath <workspace>/capability-report.json -TargetPath <workspace>
pwsh -File inventory-inputs.ps1 -InputPath <source> -OutputPath <workspace>/source-inventory.json
pwsh -File route-job.ps1 -InventoryPath <workspace>/source-inventory.json -JobContractPath <job-contract.json> -RequestedOperation auto -OutputPath <workspace>/routing-decision.json
pwsh -File run-pipeline.ps1 -InputPath <source> -JobContractPath <job-contract.json> -Workspace <workspace>
pwsh -File inspect-archive.ps1 -ArchivePath <archive> -OutputPath <workspace>/archive-adapter.json
pwsh -File inspect-archive.ps1 -ArchivePath <archive> -ExtractionDirectory <workspace>/archive-members -Extract -OutputPath <workspace>/archive-adapter.json
```

`validate-job-contract.py` chạy strict schema plus semantic checks. `duration_minutes` và `modifiers` phải tồn tại explicit. `inventory-inputs.ps1` tạo signature và hash. `route-job.ps1` phân loại nguồn, chọn visual route/adapters, nhưng operation, modifiers, preservation mode và certification mode đến từ job contract khi contract được truyền; nó không authorize content omission.
`inspect-archive.ps1` chỉ liệt kê/extract an toàn khi path containment và resource limits đạt; archive risk hoặc unsupported extractor không được coi là PASS.

`route-job.ps1` validate contract trước khi đọc inventory: operation, modifier, preservation mode và certification mode phải nằm trong enum tương ứng của routing-decision schema; giá trị ngoài enum ghi fallback BLOCKED có schema-valid structure. Khi contract có mặt, router chỉ lấy modifiers từ contract; không tự thêm modifier phát sinh từ source families. Router sau đó kiểm tra từng modifier yêu cầu có source family phù hợp: `REPAIR` cần deck, `UPDATE_DATA` cần deck + data, `TRANSCRIBE_MEDIA` cần audio/video, `EXTRACT_ARCHIVE` cần archive, `RECONCILE_SOURCES` cần ≥ 2 sources. Modifier thiếu nguồn tương ứng là `BLOCKED`.

`run-pipeline.ps1` chỉ bootstrap G0–G2. Nó schema-validate inventory/routing, bind route với job-contract path/hash, kiểm tra `source_count`, và rehash job contract, source set, inventory và routing artifact quanh downstream use. Các file `*.stdout.txt` không được chứa raw source prose, secrets, credentials hoặc transcript nhạy cảm.

Pipeline dùng `Add-ValidatedGateReceipt` thay vì ghi receipt rồi mới assert: artifact được đọc và validate trước receipt; nếu artifact malformed, receipt ghi `BLOCKED` với reason `ARTIFACT_VALIDATION_FAILED:...` và không bao giờ ghi `PASS` cho gate tương ứng. `Get-PythonCommand` chỉ chấp nhận Application-type executable (`Get-Command -CommandType Application`); script, function, alias hoặc reparse point bị từ chối với lỗi `RUNTIME_PYTHON_NOT_APPLICATION`.

Pipeline kiểm tra binding giữa route modifiers và contract modifiers từng phần tử; route tự thêm hoặc bỏ modifier so với contract là `BLOCKED` (`ROUTE_JOB_CONTRACT_MODIFIERS_MISMATCH`).

## Content/data

```powershell
python validate-json.py --input <artifact.json> --schema <schema-name> --output <report.json>
python validate-data.py --input <data-ledger.json> --output <data-report.json>
python reconcile-content.py --content-atoms <canonical-content.json> --data-ledger <data-ledger.json> --output <reconciliation.json>
python validate-slide-blueprints.py --blueprints <slide-blueprints.json> --content-atoms <canonical-content.json> --output <blueprint-report.json>
pwsh -File compare-content.ps1 -BaselinePath <before.json> -CandidatePath <after.json> -OutputPath <diff.json>
```

Empty `data-ledger.metrics` chỉ hợp lệ khi truyền canonical content đã xác minh không chứa metric. Empty ledger không có canonical context là `BLOCKED`; không dùng mảng rỗng để né data QA.

## Visual/native

```powershell
python audit-images.py --assets <visual-assets.json> --output <image-report.json>
python audit-contrast.py --manifest <contrast-manifest.json> --output <contrast-report.json>
node audit-icon-consistency.mjs --assets <visual-assets.json> --registry <lucide-semantic-registry.json> --output <icon-report.json>
node audit-visual-coverage.mjs --blueprints <slide-blueprints.json> --assets <visual-assets.json> --layout-report <native-layout-report.json> --require-native-bindings --output <coverage-report.json>
pwsh -File audit-native-layout.ps1 -DeckPath <static.pptx> -OutputPath <layout-report.json>
pwsh -File audit-typography.ps1 -DeckPath <static.pptx> -OutputPath <type-report.json> -AllowedFonts 'Segoe UI,Bahnschrift'
pwsh -File render-native.ps1 -DeckPath <deck.pptx> -OutputDirectory <renders> -ReportPath <render-report.json>
```

## Motion/release

```powershell
pwsh -File apply-motion.ps1 -InputPath <static.pptx> -OutputPath <motion.pptx> -StoryboardPath <motion-storyboard.json> -StaticCertificationPath <static-certificate.json> -ReportPath <motion-report.json>
pwsh -File audit-motion.ps1 -DeckPath <motion.pptx> -OutputPath <motion-audit.json>
pwsh -File compare-renders.ps1 -BaselineDirectory <static-renders> -CandidateDirectory <motion-end-renders> -OutputPath <equivalence.json>
pwsh -File certify-release.ps1 -InputPath <release-input.json> -OutputPath <release-certificate.json>
```

`visual_assets_verified` receipt phải có metadata gồm `native_bindings_verified`, `native_visual_coverage_report_path`, `native_visual_coverage_report_sha256` và `native_visual_coverage_deck_sha256`. Certifier kiểm tra report, layout report, path, hash và deck binding; certificate summary lưu metadata đã chuẩn hóa. `visual-assets-evidence-receipt.schema.json` là schema chuyên biệt cho raw receipt.

Coverage report release-grade phải có `schema_version=1.0`, `blueprints_path`, `blueprints_sha256`, `assets_path`, `assets_sha256`, native layout path/hash, native deck path/hash, `slide_count`, `findings`, và native binding booleans. Blueprint/asset file phải còn tồn tại, không qua reparse point, hash khớp, schema version hợp lệ; blueprint và layout slide numbers phải unique, liên tục từ `1..slide_count`; layout `shape_count` phải khớp object records; coverage/layout không được chứa P0/P1 khi status là `PASS`.

Validate report độc lập bằng `native-layout-report.schema.json` và `native-visual-coverage-report.schema.json`; runtime invariants về hash equality, slide continuity và shape/object counts vẫn là gate bổ sung ngoài khả năng JSON Schema.

`apply-motion.ps1` từ chối static certification không phải `PASS`, output đã tồn tại, hoặc native visual binding summary/raw không trùng nhau. Storyboard bắt buộc `schema_version=1.0`, `replace_existing=true`, exact root/slide/beat properties; mỗi beat có explicit `duration`, `delay`, non-empty `narrative_purpose`. Không có timing default và không giữ effect cũ ngoài storyboard. Sau PowerPoint save, script đọc lại static certificate và chạy lại toàn bộ static validation; source, storyboard, certificate, raw receipt, coverage/layout report, blueprint, asset manifest hoặc deck đổi trong lúc COM chạy đều làm output motion bị xóa và trả `BLOCKED`. `render-pdf.ps1` export PDF sang path mới và kiểm tra source hash unchanged.

`certify-release.ps1` chỉ chấp nhận exact receipt-name set của profile, kiểm tra output path tồn tại và SHA-256 thực tế khớp `output_sha256`; malformed release input luôn ghi certificate fail-closed thay vì trả lỗi runtime không có receipt. Ngay trước ghi certificate, script rehash release input, source bindings, output, raw receipts và chạy lại native visual chain. Receipt timestamp phải timezone-qualified, không ở tương lai quá năm phút và không cũ hơn output quá năm phút. Receipt SHA-256 chỉ chống sửa sau khi tạo, không thay thế chữ ký số hoặc trusted attestation.

`Write-JsonFileMutable` chỉ dành cho manifest/cache được phép thay đổi. Writer từ chối target hoặc ancestor là reparse point, tạo temp bằng `CreateNew`, recheck target ngay trước atomic move, rồi xác nhận target cuối là regular file. Mọi report mutable do Python tạo cũng phải dùng atomic writer tương đương; không dùng `Path.write_text` trực tiếp cho capability/cache receipt.

Authoring starter chỉ export layout JSON; render PNG/PDF phải dùng `render-native.ps1` hoặc `render-pdf.ps1` qua PowerPoint native để tránh khác biệt renderer.

## ASR

```powershell
pwsh -File ensure-faster-whisper.ps1 -CacheRoot <isolated-cache> -ProbeOnly
pwsh -File ensure-faster-whisper.ps1 -CacheRoot <isolated-cache>
python probe-asr-runtime.py --output <isolated-cache>\asr\capability-report.json
python transcribe-media.py --input <media> --output <transcript.json> --model large-v3 --device cpu --compute-type int8
```

Probe-only không download package hoặc model weights. Installation dùng hash-pinned lock và isolated venv dưới `CacheRoot\asr`, có mutex chống concurrent install, không chấp nhận reparse-point ở `asr`, và rollback transaction khi post-install probe fail. Probe output là mutable cache report nhưng vẫn phải kiểm tra ancestor, regular-file target và atomic replace. `nvidia-smi` không được dùng làm bằng chứng duy nhất để chọn CUDA; capability CTranslate2 phải xác minh trước. Model download là transcription action explicit.
