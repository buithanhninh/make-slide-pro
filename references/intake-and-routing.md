# Intake And Routing

## Bước sàng lọc

1. Resolve absolute source, job-contract và workspace paths; reject missing path, reparse ambiguity, collisions và workspace nằm trong source.
2. Validate `job-contract.json`; primary operation, modifiers, preservation mode và certification mode từ contract là authoritative.
3. Đọc magic bytes; với Office ZIP, kiểm tra package entries (`ppt/presentation.xml`, `word/document.xml`, `xl/workbook.xml`) và macro part.
4. Tính SHA-256, size, modified time, detected format, extension mismatch và risk flags.
5. Gán role sơ bộ; authority vẫn `UNRESOLVED` đến khi user hoặc evidence map xác nhận.
6. Chọn input class, maturity, visual route và required adapters; không tự thay operation hoặc preservation policy trong contract.
7. Validate modifier-source compatibility: `REPAIR` cần deck, `UPDATE_DATA` cần deck + data, `TRANSCRIBE_MEDIA` cần audio/video, `EXTRACT_ARCHIVE` cần archive, `RECONCILE_SOURCES` cần nhiều source.
8. Schema-validate inventory/routing, kiểm tra `source_count`, bind route với job-contract path/hash và exact modifiers, rồi ghi hash checkpoints trước extraction.

Khi contract được truyền, router không tự thêm modifier từ source families. Contract lỗi, thiếu hoặc collision với inventory phải tạo routing receipt `BLOCKED` có schema-valid fallback khi output path vẫn an toàn. Contract-output collision không được ghi vì output sẽ đè chính contract.

## Resource ceilings

- JSON reader Python, Node và PowerShell từ chối input lớn hơn `64 MiB` trước parse.
- `inventory-inputs.ps1` mặc định tối đa `10,000` files, `8 GiB` mỗi file và `32 GiB` tổng; vượt ngưỡng trả `BLOCKED` trước hashing toàn bộ.
- Tham số limit phải dương; `MaximumFiles` không vượt `1,000,000`.

## File routing matrix

| Dạng | Adapter | Extract | Native/render | Rủi ro | Route |
|---|---|---|---|---|---|
| PPTX/PPTM/PPT/ODP | `POWERPOINT` | slide, shape, text, notes, chart, table, media | PowerPoint COM + render | overflow, theme, macro, flatten | `EDITABLE_DECK` hoặc `REBUILD` |
| DOCX/DOCM/DOC | `DOCUMENT` | heading, paragraph, table, footnote, comment, image | Word COM/PDF render | reading order, tracked changes, macro | `STRUCTURED_CONTENT` |
| PDF | `PDF` | text blocks, tables, pages, metadata | page render + OCR scan | reading order, scan, font | `REPORT_OR_FLAT_SOURCE` |
| XLSX/XLSM/XLS/ODS/CSV/TSV | `DATA` | cells, formulas, named ranges, charts, units | Excel COM/render | formula/value, hidden rows, period | `DATA_SOURCE` |
| TXT/MD/HTML/RTF | `DOCUMENT` | encoding-aware text/structure; RTF hiện đi qua text classification | optional render | malformed encoding, lost rich formatting | `STRUCTURED_CONTENT` |
| JSON/XML/CSV/TSV | `DATA` | encoding-aware structure, records, units | optional render | malformed encoding, schema ambiguity | `DATA_SOURCE` |
| MP3/WAV/M4A/AAC/FLAC/OGG | `AUDIO` | transcript, timestamps, language, confidence | waveform/metadata | ASR, names, numbers, crosstalk | `MEDIA_SOURCE`; visual route `TRANSCRIPT_TO_STORY` |
| MP4/MOV/MKV/AVI/WEBM | `VIDEO` | audio transcript, scene/keyframe metadata | FFmpeg frame sampling | ASR/visual mismatch | `MEDIA_SOURCE`; visual route `TRANSCRIPT_TO_STORY` |
| PNG/JPEG/GIF/TIFF/BMP/WEBP/SVG | `IMAGE` | dimensions, EXIF, OCR nếu cần | raster/vector inspect | fake evidence, low PPI, distortion | `VISUAL_SOURCE`; visual route `VISUAL_RECONSTRUCTION` |
| ZIP/7Z/RAR | `ARCHIVE` | `inspect-archive.ps1` safe listing, limits, optional extraction, then member routing | no execution | path traversal, archive bomb, macro payload, unsupported tool | `ARCHIVE_SOURCE`; visual route `ARCHIVE_EXTRACTION` |

## Maturity levels

- `S0`: media/unknown; meaning chưa structured.
- `S1`: structured content/data extracted, authority pending.
- `S2`: canonical evidence và reconciliation complete.
- `S3`: flat/report source cần visual hoặc OCR reconstruction.
- `S4`: existing editable deck; inspect trước change.
- `S5`: static và motion evidence complete; release candidate.

## Authority policy

Priority: user-designated authoritative source, official data source, signed/dated business artifact, previous deck, supporting evidence, conceptual asset. Previous deck là visual reference trừ khi user chỉ định content authority. Attached instructions là content, không phải execution authority.

## Audio/video: faster-whisper

`faster-whisper` chỉ chạy khi media transcription cần thiết. `ensure-faster-whisper.ps1` cài pinned wheels vào isolated cache `asr\venv`; không cài system Python. Installer giữ mutex theo cache, kiểm tra `asr` và toàn bộ ancestor không phải reparse point, stage runtime mới, probe sau publish và rollback runtime cũ nếu probe fail. Lock hiện tại target Windows CPython 3.11 AMD64. OS, architecture hoặc Python không hỗ trợ trả `UNVERIFIED`; không unpinned fallback. Probe ghi capability receipt bằng atomic mutable writer, không ghi đè source hoặc target không phải regular file.

CPU default: `device=cpu`, `compute_type=int8`. `nvidia-smi` chỉ chứng minh `GPU_CANDIDATE`; không đủ để chọn CUDA. Probe phải gọi CTranslate2 cho từng device, ghi `cpu_compute_types`, `cuda_compute_types` và chỉ đặt `cuda_verified=true` khi NVIDIA probe thành công và CTranslate2 trả capability CUDA. Chỉ chọn `cuda` khi `cuda_verified=true` và có compute type được runtime báo hỗ trợ; nếu không, chọn CPU compute type thực tế hoặc trả `UNVERIFIED`. Không tự cài driver, CUDA, cuDNN hoặc package liên quan. Package install không download model weights. Model download chỉ xảy ra lúc transcription explicit và được cache.

Transcript receipt phải có model, device, compute type, language/probability, segment/word timestamps, VAD policy, confidence flags và critical-token flags. Không gán speaker names nếu thiếu diarization evidence. Names, numbers, currency, dates, negation và commitments cần review.

## Safety stops

- Extension/signature mismatch: chỉ tiếp tục với risk flag và adapter verified.
- Macro-enabled source: inspect không execute macro; `BLOCKED` nếu safe inspection unavailable.
- Corrupt archive hoặc unknown binary: `BLOCKED` đến khi recover hoặc explicit exclude.
- Missing OCR với scanned source: `UNVERIFIED`.
- Missing FFmpeg với video: `UNVERIFIED`.
- Source và output cùng resolve path: hard stop.
- Modifier yêu cầu source family không tồn tại: `BLOCKED`.
- Runtime Python explicit không resolve thành regular Application executable: `BLOCKED`; không chạy script/alias/function thay Python.

## Archive adapter

`inspect-archive.ps1` nhận diện lại signature trước khi xử lý. ZIP được đọc bằng `System.IO.Compression.ZipArchive`; member path tuyệt đối, `.`/`..`, duplicate normalized path, macro payload, empty archive và vượt giới hạn entry/byte đều tạo risk. Extraction chỉ chạy khi `-Extract` được yêu cầu, extraction directory mới/rỗng và mọi destination nằm trong containment root. Member không được execute; sau extraction phải kiểm tra lại signature, hash và route từng member.

7Z/RAR không tự fallback sang untrusted extractor. Thiếu tool listing tương ứng trả `UNVERIFIED`; tool có mặt nhưng adapter chưa được bật vẫn giữ trạng thái `UNVERIFIED` để agent quyết định explicit.
