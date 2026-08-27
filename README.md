# Make Slide Pro

Make Slide Pro là Codex skill xây dựng, sửa, thiết kế lại, kiểm định và chứng nhận PowerPoint theo pipeline fail-closed G0-G15.

## Phiên bản

- Bản hiện hành: `6.2.0`
- Ngày phát hành: `2026-08-27`
- Trạng thái: bản phát hành đã được kiểm chứng bằng test tự động; không tuyên bố hoàn hảo tuyệt đối ngoài evidence hiện có.

## Năng lực chính

- Sàng lọc PPTX, DOCX, PDF, spreadsheet, text, audio, video, image, archive và nguồn hỗn hợp.
- Bảo toàn claim, số liệu, đơn vị, mốc thời gian, điều kiện, phủ định, bất định và nguồn dẫn.
- Xây narrative, slide blueprint, visual system hiện đại tinh tế, chart/table editable, icon và hình minh họa có truy vết.
- Tạo native motion sau khi static deck vượt qua các gate nội dung, dữ liệu, layout, typography, visual và render.
- Điều phối G0-G15 bằng event journal append-only, hash chain, CAS revision, lease và recovery fail-closed.
- Chứng nhận release theo ba profile: `STATIC_READY_FOR_MOTION`, `FINAL_RELEASE_STATIC`, `FINAL_RELEASE_MOTION`.

## Cài đặt

Clone repository vào thư mục Codex skills:

```powershell
git clone https://github.com/buithanhninh/make-slide-pro "$HOME\.codex\skills\make-slide-pro"
```

Skill cần các engine được nêu trong `SKILL.md`, gồm `presentations:Presentations`, `@oai/artifact-tool`, Microsoft PowerPoint COM cho native authoring/QA, Python, Node.js và các adapter theo loại nguồn.

## Kiểm chứng

```powershell
python -m pytest -q tests/test_v6_2.py tests/test_make_slide_pro.py
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```

Baseline phát hành `v6.2.0`: `178 passed, 121 subtests passed`; Python compile, PowerShell parse, Node syntax và skill validation đều đạt.

## Điểm vào

- `SKILL.md`: hợp đồng vận hành chính.
- `assets/pipeline/gate-registry.json`: registry declarative G0-G15, `pipeline_version=6.2.0`.
- `scripts/orchestrator_core.py`: control plane, journal, lease, validation và recovery.
- `schemas/`: hợp đồng JSON Schema cho machine artifacts.
- `tests/`: regression suite và corpus manifest.

Không commit deck riêng tư hoặc dữ liệu khách hàng vào repository.
