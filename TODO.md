# MASTER TO-DO LIST (BẢN RÀ SOÁT TOÀN DIỆN 100% - ZERO GAP)
## MAKE SLIDE PRO SAAS V8.6.0 (ENTERPRISE EDITION)
**Mã tài liệu: MSP-TODO-V86-AUDITED | Đối chiếu chuẩn xác: `MSP-SDD-V86` (SYSTEM_DESIGN.md)**
*Ngày cập nhật: 2026-09-21 | Mức độ bao phủ kiến trúc: 100% Tuyệt đối*

---

## 1. MA TRẬN ĐỐI SOÁT KIẾN TRÚC & YÊU CẦU (TRACEABILITY MATRIX)

Bảng đối soát đảm bảo 100% yêu cầu kỹ thuật trong tài liệu kiến trúc `SYSTEM_DESIGN.md` đều có task thực thi tương ứng, không bỏ sót bất kỳ cấu phần nào:

| Mã YC Kiến Trúc | Nội dung yêu cầu kỹ thuật | Cấu phần chịu trách nhiệm | Mã Task thực thi | Mức độ bao phủ |
|---|---|---|---|---|
| **REQ-01** | Đăng nhập Google 1 chạm (Gmail OAuth 2.0) | `web/auth.py`, `web/database.py` | Task 1.1, 1.2, 1.4, 1.5, 5.3 | 100% (Backend + DB + UI) |
| **REQ-02** | Xử lý đa tệp đồng thời (.docx, .pdf, .pptx) | `scripts/ingest_content.py` | Task 2.1, 2.3, 2.4, 5.4 | 100% (Parser + Validator + UI) |
| **REQ-03** | Trích xuất link Google Docs tự động | `scripts/ingest_content.py` | Task 2.2, 2.5, 5.4 | 100% (Resolver + HTTP GET + UI) |
| **REQ-04** | Phân loại 7 chủ đề lĩnh vực chuyên ngành | `scripts/ai_brain.py`, `web/static/` | Task 3.3, 5.5 | 100% (System Prompt + Form Dropdown) |
| **REQ-05** | Quy chuẩn 10 cấp bậc số lượng slide | `scripts/ai_brain.py`, `scripts/blueprint_generator.py` | Task 3.2, 5.5 | 100% (Tier Config + Grid UI) |
| **REQ-06** | 5 preset màu thương hiệu + mã HEX tự do | `scripts/ai_brain.py`, `scripts/author_native_com.py` | Task 3.3, 4.4, 5.5 | 100% (Token Injection + Color Picker) |
| **REQ-07** | Định dạng nền: Dark, Light, Dual (ZIP) | `web/app.py`, `scripts/author_native_com.py` | Task 4.4, 4.5, 5.5, 5.7 | 100% (COM Render + Zip Packager) |
| **REQ-08** | Ghi chú yêu cầu bổ sung (Special Prompt) | `scripts/ai_brain.py`, `web/static/` | Task 3.3, 5.5 | 100% (Prompt Injection + UI Textarea) |
| **REQ-09** | Hàng đợi tác vụ & Tiến độ WebSocket | `web/app.py`, `web/static/` | Task 4.1, 4.5, 5.6 | 100% (Queue + WS Broadcaster + UI) |
| **REQ-10** | Tải 1-Click an toàn (chống IDOR) | `web/app.py`, `web/static/` | Task 1.3, 4.6, 5.7 | 100% (Tenant Guard + Stream Response) |
| **REQ-11** | Công khai Internet qua Cloudflare Tunnel | `cloudflared`, script khởi chạy | Task 6.1, 6.2, 6.3 | 100% (Tunnel Ingress + Batch Runner) |
| **ARCH-AI** | Multi-Provider (9Router model `plan` / Gemini) | `scripts/ai_brain.py`, `.env` | Task 3.1, 3.4, 3.6, 6.4 | 100% (Client + Fallback + Retry) |
| **ARCH-COM**| Cô lập STA & Watchdog timeout 120s | `web/app.py`, `author_native_com.py` | Task 4.1, 4.2, 4.3, 6.5 | 100% (asyncio.Lock + Taskkill Watchdog) |
| **ARCH-DB** | Toàn vẹn 4 bảng DDL & Indexes | `web/database.py`, `make_slide_pro.db`| Task 1.2, 1.3 | 100% (Users, Projects, Jobs, Blueprints) |
| **ARCH-OPS**| Tự động dọn dẹp file rác sau 24h | `web/app.py` (Background Janitor) | Task 6.6 | 100% (TTL Garbage Collector) |

---

## 2. CHI TIẾT 44 HẠNG MỤC CÔNG VIỆC THỰC THI (DETAILED WORK BREAKDOWN)

### PHASE 1: XÁC THỰC GOOGLE OAUTH 2.0, BẢO MẬT & TOÀN VẸN CSDL (SPRINT 1)
*Mục tiêu: Đăng nhập Gmail một chạm, bảo mật chống IDOR, cấu trúc đầy đủ 4 bảng CSDL theo DDL chuẩn.*

- [ ] **Task 1.1: Khởi tạo cấu hình biến môi trường bảo mật**
  * Tệp tác động: `.env`, `.env.example`
  * Nội dung: Khai báo đầy đủ `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `JWT_SECRET_KEY`, `JWT_ALGORITHM=HS256`, `ACCESS_TOKEN_EXPIRE_DAYS=7`, `APP_PORT=8000`.
  * Tiêu chí hoàn thành: File `.env` được tải an toàn, có fallback cảnh báo nếu thiếu secret key.

- [ ] **Task 1.2: Nâng cấp toàn diện Schema SQLAlchemy cho 4 bảng CSDL**
  * Tệp tác động: `web/database.py`
  * Nội dung: 
    * Bảng `User`: Thêm `google_id` (Unique, Index), `avatar_url`, `credits` (default=5), `role`, `tier`, cho phép `hashed_password` nullable khi login Google.
    * Bảng `Project`: Thêm `source_doc_url`, `topic_domain`, `slide_tier` (1-10), `accent_color`, `theme_mode` (DARK/LIGHT/DUAL), `special_notes`.
    * Bảng `RenderJob`: Thêm `stage_detail`, `output_pptx_dark`, `output_pptx_light`, `output_zip`, `total_slides`, `macc_score`, `execution_time_seconds`.
    * Bảng `Blueprint`: Lưu trữ nguyên vẹn `slides_json`, `total_slides`, `deck_title`.
  * Tiêu chí hoàn thành: Khởi tạo database `make_slide_pro.db` không lỗi cú pháp, toàn bộ các bảng và index được sinh tự động.

- [ ] **Task 1.3: Cài đặt và cấu hình thư viện xác thực Google Client**
  * Tệp tác động: `requirements.txt`
  * Nội dung: Bổ sung `google-auth>=2.28.0`, `requests>=2.31.0`, `aiofiles>=23.2.0`.
  * Tiêu chí hoàn thành: Môi trường ảo Python cài đặt sạch sẽ, không xung đột dependency.

- [ ] **Task 1.4: Xây dựng hàm thẩm định Google ID Token trong module bảo mật**
  * Tệp tác động: `web/auth.py`
  * Nội dung: Viết hàm `verify_google_token(token: str) -> dict` sử dụng `id_token.verify_oauth2_token`. Kiểm tra chặt chẽ audience, expiration và issuer (`accounts.google.com`).
  * Tiêu chí hoàn thành: Token giả mạo hoặc hết hạn bị ném `HTTPException 401`; token hợp lệ trích xuất đúng `email`, `sub`, `name`, `picture`.

- [ ] **Task 1.5: Xây dựng REST API Endpoint `/api/auth/google`**
  * Tệp tác động: `web/app.py`
  * Nội dung: Nhận payload `{ credential: str }`. Truy vấn User qua `google_id` hoặc `email`. Nếu người dùng mới -> tự động tạo bản ghi với 5 credits miễn phí. Tạo JWT Access Token hạn 7 ngày chứa `sub: user.id`.
  * Tiêu chí hoàn thành: Trả về HTTP 200 kèm JWT token và user profile hoàn chỉnh.

- [ ] **Task 1.6: Xây dựng Middleware / Dependency kiểm tra quyền sở hữu Tenant (Chống IDOR)**
  * Tệp tác động: `web/auth.py`
  * Nội dung: Hàm `verify_project_ownership(project_id: str, current_user: User, db: Session) -> Project`. Chặn mọi truy cập trái phép nếu dự án không thuộc sở hữu của người dùng hiện tại.
  * Tiêu chí hoàn thành: Thử truy cập project của user khác trả về HTTP 403 Forbidden.

- [ ] **Task 1.7: Viết bộ kiểm thử tự động cho Tầng Xác thực & Database**
  * Tệp tác động: `tests/test_auth_flow.py`
  * Nội dung: Kiểm thử tạo user, sinh token, giải mã token, kiểm tra IDOR, xác thực token Google giả lập.
  * Tiêu chí hoàn thành: `pytest tests/test_auth_flow.py` pass 100%.

---

### PHASE 2: TIẾP NHẬN TÀI LIỆU ĐA NGUỒN & GOOGLE DOCS PARSER (SPRINT 2)
*Mục tiêu: Kéo thả nhiều tệp, dán link Google Docs, tự động bóc tách cấu trúc và làm sạch văn bản.*

- [ ] **Task 2.1: Mở rộng `scripts/ingest_content.py` hỗ trợ xử lý đa tệp**
  * Tệp tác động: `scripts/ingest_content.py`
  * Nội dung: Xây dựng hàm `ingest_multiple_documents(file_paths: List[Path], session_dir: Path) -> Dict[str, Any]`. Lần lượt bóc tách Word (`.docx`), PDF (`.pdf`), PowerPoint (`.pptx`), sau đó hợp nhất danh sách phân đoạn (`sections`), bảo toàn thứ tự logic.
  * Tiêu chí hoàn thành: Gộp thành công 3 file khác định dạng thành một file `canonical-content.json` duy nhất.

- [ ] **Task 2.2: Xây dựng bộ phân giải liên kết Google Docs (Google Docs Resolver)**
  * Tệp tác động: `scripts/ingest_content.py`
  * Nội dung: Viết hàm `resolve_google_docs_url(url: str, output_dir: Path) -> Path`. Sử dụng Regex tách `DOC_ID` từ chuỗi URL Google Docs:
    Pattern: `https://docs.google.com/document/d/([a-zA-Z0-9-_]+)`
    Gửi request HTTP GET tải trực tiếp định dạng DOCX qua link:
    `https://docs.google.com/document/d/{DOC_ID}/export?format=docx`
    Bắt các ngoại lệ URL riêng tư (HTTP 401/403/404) và trả về thông báo lỗi thân thiện.
  * Tiêu chí hoàn thành: Dán URL công khai -> tải về file `.docx` hợp lệ và đẩy vào quy trình bóc tách.

- [ ] **Task 2.3: Thiết lập các chốt chặn kiểm soát an toàn tải tệp (Upload Guards)**
  * Tệp tác động: `web/app.py`
  * Nội dung: Kiểm tra định dạng tệp thông qua phần mở rộng và Magic Bytes (chống đổi tên file nguy hại). Giới hạn tổng dung lượng tệp tải lên <= 50MB. Chặn tệp rỗng (0 KB).
  * Tiêu chí hoàn thành: File không hợp lệ bị từ chối với mã lỗi HTTP 400 kèm giải thích chi tiết.

- [ ] **Task 2.4: Bảo tồn trọn vẹn số liệu thống kê (Data Ledger) & Bảng biểu (Claim Ledger)**
  * Tệp tác động: `scripts/ingest_content.py`
  * Nội dung: Đảm bảo khi gộp nhiều tệp, các chỉ số đo lường (`contains_metric`), công thức (`is_formula`) và bảng biểu (`is_table`) được gắn nhãn nguồn gốc tệp ban đầu.
  * Tiêu chí hoàn thành: Xuất ra `claim-ledger.json` và `data-ledger.json` đầy đủ số liệu phục vụ vẽ biểu đồ.

- [ ] **Task 2.5: Làm sạch và chuẩn hóa ngữ nghĩa văn bản tiếng Việt**
  * Tệp tác động: `scripts/ingest_content.py`
  * Nội dung: Loại bỏ ký tự điều khiển lạ, khoảng trắng thừa, chuẩn hóa dấu ngoặc và định dạng số thập phân.
  * Tiêu chí hoàn thành: Văn bản nguồn sau khi làm sạch đạt chuẩn UTF-8, không lỗi font.

- [ ] **Task 2.6: Viết kiểm thử tích hợp Ingestion đa nguồn**
  * Tệp tác động: `tests/test_multi_ingest.py`
  * Nội dung: Kiểm thử gộp 1 Word + 1 PDF + 1 PPTX mẫu; kiểm thử tải link Google Docs hợp lệ và link riêng tư.
  * Tiêu chí hoàn thành: Kiểm thử tự động chạy pass 100%.

---

### PHASE 3: BỘ NÃO AI SUY LUẬN ĐA NHÀ CUNG CẤP (9ROUTER / GEMINI) (SPRINT 3)
*Mục tiêu: Gọi model `plan` qua 9Router (hoặc Gemini dự phòng), sinh kịch bản JSON V8.6.0 tuân thủ 10 bậc slide, 7 lĩnh vực và 165+ Archetypes.*

- [ ] **Task 3.1: Xây dựng module AI Adapter đa nhà cung cấp (`scripts/ai_brain.py`)**
  * Tệp tác động: `scripts/ai_brain.py`
  * Nội dung: Xây dựng class `AIBrainAdapter` đọc biến môi trường `AI_PROVIDER` (mặc định `9router`):
    * Mode `9router`: Gọi OpenAI client với `base_url="https://9router.caqa.io.vn/v1"`, `api_key=NINEROUTER_API_KEY`, `model="plan"`.
    * Mode `gemini`: Gọi SDK `google-genai` với `model="gemini-2.5-pro"` hoặc `"gemini-2.0-flash"`.
  * Tiêu chí hoàn thành: Gửi prompt mẫu -> nhận phản hồi thành công từ cả 2 chế độ provider.

- [ ] **Task 3.2: Lập trình từ điển ánh xạ 10 Cấp bậc số lượng slide**
  * Tệp tác động: `scripts/ai_brain.py`, `scripts/blueprint_generator.py`
  * Nội dung: Cấu hình bảng 10 nấc:
    * Nấc 1: 3 – 5 slide (Quick Pitch)
    * Nấc 2: 5 – 8 slide (Executive Summary)
    * Nấc 3: 8 – 12 slide (Standard Meeting Deck)
    * Nấc 4: 12 – 16 slide (Mid-level Review)
    * Nấc 5: 16 – 20 slide (Standard 45-min Lecture)
    * Nấc 6: 20 – 25 slide (Advanced 60-90 min Seminar)
    * Nấc 7: 25 – 30 slide (Full Project Dossier)
    * Nấc 8: 30 – 40 slide (Half-day Training Curriculum)
    * Nấc 9: 40 – 50 slide (Course Module System)
    * Nấc 10: 50+ slide (Master Curriculum Deck)
  * Tiêu chí hoàn thành: AI nhận cấp bậc -> sinh ra số lượng slide nằm chính xác trong khoảng quy định.

- [ ] **Task 3.3: Lập trình System Prompt điều phối 7 lĩnh vực & Đồng bộ Accent Color**
  * Tệp tác động: `scripts/ai_brain.py`
  * Nội dung: Hàm `build_pedagogical_system_prompt(...)`:
    * Chèn kiến thức miền theo 7 nhóm: `KINH_TE`, `Y_TE`, `GIAO_DUC`, `CONG_NGHE`, `QUAN_TRI`, `MARKETING`, `TONG_HOP`.
    * Ép buộc tích hợp mã màu `accent_color` vào hệ thống Visual Tokens của từng slide.
    * Đưa yêu cầu trong `special_notes` thành chỉ dẫn ưu tiên số 1 khi lập dàn ý.
  * Tiêu chí hoàn thành: Prompt hoàn chỉnh truyền vào mô hình với đầy đủ quy chuẩn thiết kế V8.6.0.

- [ ] **Task 3.4: Xây dựng cơ chế lựa chọn tối ưu trong 165+ Mega Archetypes**
  * Tệp tác động: `scripts/ai_brain.py`
  * Nội dung: Danh mục mã Archetype chuẩn (ví dụ: `MEGA_HERO_SPLIT`, `BENTO_GRID_3COL`, `DATA_TABLE_ACCENT`, `FORMULA_CARD_DUAL`, `METRIC_CARDS_4X`, `PROCESS_STEP_CHEVRON`, `COMPARISON_PROS_CONS`, `TIMELINE_HORIZONTAL`).
  * Tiêu chí hoàn thành: Mỗi slide trong blueprint có `archetype` và `visual_job` hợp lệ với thư viện `scripts/component_library/`.

- [ ] **Task 3.5: Bộ trích xuất & Thẩm định cú pháp JSON Blueprint V8.6.0**
  * Tệp tác động: `scripts/ai_brain.py`
  * Nội dung: Regex parser trích xuất khối JSON từ Markdown, xác thực cấu trúc qua Pydantic schema (`deck_title`, `topic_domain`, `accent_color`, `total_slides`, `slides`).
  * Tiêu chí hoàn thành: Bắt lỗi và chuẩn hóa các trường thiếu sót trước khi chuyển sang bước dựng slide.

- [ ] **Task 3.6: Tích hợp Hội đồng Thẩm định 16-Agent MACC-QA**
  * Tệp tác động: `scripts/ai_brain.py`
  * Nội dung: Gọi `MultiRoundCouncilOrchestrator` trong `scripts/macc_council.py`. Chạy tối đa 3 vòng đối kháng giữa 16 agents (Pedagogy, Fact, Layout, Contrast, Typography...). Cập nhật `macc_score` và remediated slides.
  * Tiêu chí hoàn thành: Kịch bản được phê duyệt có điểm hội đồng >= 90/100, lưu báo cáo `macc-council-report.json`.

- [ ] **Task 3.7: Cơ chế tự động hồi phục khi LLM trả về lỗi (Fallback & Auto-Retry)**
  * Tệp tác động: `scripts/ai_brain.py`
  * Nội dung: Nếu model `plan` gặp lỗi 429/500 hoặc cú pháp hỏng -> tự động retry 1 lần với temperature thấp hơn (0.2); nếu tiếp tục lỗi -> tự động chuyển sang Google Gemini API.
  * Tiêu chí hoàn thành: Không để gián đoạn luồng người dùng vì lỗi ngắt mạng của LLM.

- [ ] **Task 3.8: Viết kiểm thử tự động cho Tầng AI Brain**
  * Tệp tác động: `tests/test_ai_brain.py`
  * Nội dung: Kiểm thử sinh blueprint cho tài liệu mẫu với các cấp bậc khác nhau (Bậc 1, Bậc 3, Bậc 5).
  * Tiêu chí hoàn thành: Toàn bộ test case chạy thành công, thời gian xử lý phản hồi < 20s.

---

### PHASE 4: POWERPOINT COM SANDBOX, HÀNG ĐỢI TUẦN TỰ & WATCHDOG (SPRINT 4)
*Mục tiêu: Điều khiển Microsoft PowerPoint native an toàn, chống nghẽn bộ nhớ STA, tự động hồi phục và đóng gói ZIP Dual-Theme.*

- [ ] **Task 4.1: Thiết lập khóa đơn luồng hàng đợi (`COM_LOCK = asyncio.Lock()`)**
  * Tệp tác động: `web/app.py`
  * Nội dung: Khởi tạo biến khóa toàn cục `COM_LOCK`. Bao bọc toàn bộ khối thực thi dựng slide PowerPoint trong `async with COM_LOCK`.
  * Tiêu chí hoàn thành: Tại một thời điểm chỉ duy nhất 1 tác vụ được chiếm dụng Office COM, các tác vụ khác tự động giữ trạng thái `QUEUED`.

- [ ] **Task 4.2: Chuẩn hóa bọc cách ly luồng STA Apartment (CoInitialize / CoUninitialize)**
  * Tệp tác động: `web/app.py`, `scripts/author_native_com.py`
  * Nội dung: Hàm worker chạy trong `ThreadPoolExecutor` bắt buộc gọi:
    ```python
    import pythoncom
    pythoncom.CoInitialize()
    try:
        author = NativeDeckAuthor(visible=False, theme=theme, motion_mode="presenter_click")
        author.create_deck(bp_path, out_pptx_path)
    finally:
        pythoncom.CoUninitialize()
    ```
  * Tiêu chí hoàn thành: Không xảy ra lỗi Apartment threading state hoặc rò rỉ con trỏ COM.

- [ ] **Task 4.3: Xây dựng cơ chế giám sát Watchdog Timeout 120s & Cưỡng chế thu hồi COM**
  * Tệp tác động: `web/app.py`
  * Nội dung: Bọc worker trong `asyncio.wait_for(..., timeout=120.0)`. Nếu timeout:
    1. Thực thi: `subprocess.run(["taskkill", "/f", "/im", "POWERPNT.EXE"])`.
    2. Ghi nhận `RenderJob.status = "FAILED"`, `error_message = "Quá thời gian xử lý 120s"`.
    3. Gửi thông báo WebSocket lỗi cấp `"error"`.
    4. Giải phóng khóa `COM_LOCK`.
  * Tiêu chí hoàn thành: Máy chủ không bị treo khi file lỗi làm đơ PowerPoint, tự giải phóng để chạy bài tiếp theo.

- [ ] **Task 4.4: Tái tạo định kỳ tiến trình PowerPoint chống rò rỉ RAM (Process Recycling)**
  * Tệp tác động: `web/app.py`
  * Nội dung: Đếm số lượng tác vụ đã render. Cứ sau mỗi 10 tác vụ, tự động thực hiện lệnh dọn dẹp tiến trình ngầm `POWERPNT.EXE` để làm mới hoàn toàn bộ nhớ đệm Windows COM.
  * Tiêu chí hoàn thành: Bộ nhớ RAM của tiến trình Office duy trì ổn định < 500MB sau hàng chục lần render.

- [ ] **Task 4.5: Xây dựng module đóng gói Dual-Theme thành tệp ZIP**
  * Tệp tác động: `web/app.py`
  * Nội dung: Khi người dùng chọn `theme_mode == "DUAL"`, hệ thống tự động render lần lượt `Presentation_Dark.pptx` và `Presentation_Light.pptx`. Dùng `zipfile` đóng gói 2 file vào `Presentation_Dual.zip` kèm file tóm tắt `README.txt`.
  * Tiêu chí hoàn thành: Tệp ZIP sinh ra hợp lệ, giải nén mở được trọn vẹn cả 2 bản trình chiếu native.

- [ ] **Task 4.6: Cập nhật API Endpoint `/api/projects/submit`**
  * Tệp tác động: `web/app.py`
  * Nội dung: Nhận multipart data -> lưu file nguồn vào `Du_An_Outputs/web_sessions/{project_id}` -> tạo bản ghi `Project` & `RenderJob` -> kích hoạt worker nền -> trả về `job_id`.
  * Tiêu chí hoàn thành: Endpoint phản hồi trong < 500ms, trả về HTTP 200 kèm `status: "QUEUED"`.

- [ ] **Task 4.7: Cập nhật kênh WebSocket phát sóng tiến độ 4 giai đoạn (`/ws/jobs/{job_id}`)**
  * Tệp tác động: `web/app.py`
  * Nội dung: Kết nối WebSocket quản lý theo `ConnectionManager`, phát sóng tiến độ theo 4 bước:
    * `[1/4] INGESTION` (20%): Đang bóc tách và làm sạch tài liệu nguồn...
    * `[2/4] AI_SYNTHESIS` (45%): Model `plan` phân tầng sư phạm & chọn 165+ Archetypes...
    * `[3/4] MACC_QA` (70%): Hội đồng 16-Agent thẩm định chất lượng kịch bản...
    * `[4/4] COM_RENDER` (95%): PowerPoint COM vẽ slide native, nhúng biểu đồ Excel, gắn Morph...
    * `COMPLETED` (100%): Hoàn tất! Sẵn sàng tải về.
  * Tiêu chí hoàn thành: Sự kiện phát đúng thứ tự, có kèm metadata chi tiết ở từng bước.

- [ ] **Task 4.8: Hoàn thiện API Endpoint tải tệp có bảo vệ quyền sở hữu (`/api/download/{project_id}/{file_type}`)**
  * Tệp tác động: `web/app.py`
  * Nội dung: Hỗ trợ `file_type`: `pptx-dark`, `pptx-light`, `zip`. Xác thực JWT token qua header hoặc query param `?token=...`. Kiểm tra `project.user_id == current_user.id`. Trả về `FileResponse` kèm header download.
  * Tiêu chí hoàn thành: Tải file thành công, ngăn chặn hoàn toàn việc người khác tải trộm dữ liệu.

---

### PHASE 5: GIAO DIỆN WEB STUDIO WIZARD 4 BƯỚC TINH GỌN (SPRINT 5)
*Mục tiêu: Xây dựng giao diện Single Page Application phong cách Dark Luxury Obsidian Studio, tối giản, mượt mà, không tải lại trang.*

- [ ] **Task 5.1: Xây dựng cấu trúc HTML5 SPA tinh giản 4 trạng thái (`web/static/index.html`)**
  * Tệp tác động: `web/static/index.html`
  * Nội dung: 
    * `State 0: Auth Screen`: Form đăng nhập tối giản trung tâm, nút Google Identity và thông tin bảo mật.
    * `State 1: Ingestion & Configurator`: Dropzone đa tệp, ô link Google Docs, bộ chọn 5 thông số.
    * `State 2: Telemetry Screen`: Thanh tiến trình 4 giai đoạn, radar chart chỉ số, stream log thời gian thực.
    * `State 3: Delivery Screen`: Thẻ hiển thị thành phẩm, điểm thẩm định MACC-QA, nút bấm 1-Click Download PPTX/ZIP.
  * Tiêu chí hoàn thành: Chuyển đổi trạng thái mượt mà bằng JavaScript DOM manipulation, không giật lag.

- [ ] **Task 5.2: Xây dựng CSS Design Tokens chuẩn Luxury Dark Obsidian (`web/static/css/style.css`)**
  * Tệp tác động: `web/static/css/style.css`
  * Nội dung: Tone màu nền `#0B0F19`, thẻ kính mờ `rgba(30, 41, 59, 0.7)`, viền ánh kim tinh tế `rgba(255, 255, 255, 0.08)`, typography chuẩn Apple SF Pro / Inter. Responsive từ Mobile 375px đến Desktop 4K.
  * Tiêu chí hoàn thành: Giao diện đạt độ hoàn thiện cao cấp, không vỡ layout trên mọi độ phân giải.

- [ ] **Task 5.3: Tích hợp Google Identity Services (GSI) SDK trên Frontend**
  * Tệp tác động: `web/static/index.html`, `web/static/js/app.js`
  * Nội dung: Nhúng script `accounts.google.com/gsi/client`. Khởi tạo `google.accounts.id.initialize` với `GOOGLE_CLIENT_ID`, render nút Google Sign-In chuẩn. Bắt callback, gửi token về `/api/auth/google`, lưu JWT vào `localStorage`.
  * Tiêu chí hoàn thành: Bấm đăng nhập Google -> lưu session và chuyển ngay sang màn hình Wizard trong 1 giây.

- [ ] **Task 5.4: Xây dựng tương tác Bước 1: Kéo thả đa tệp & Dán Google Docs Link**
  * Tệp tác động: `web/static/js/app.js`
  * Nội dung: Kéo thả file kèm hiệu ứng highlight viền; hiển thị danh sách chip tệp đã chọn kèm dung lượng và nút xóa; kiểm tra hợp lệ đuôi `.docx`, `.pdf`, `.pptx`. Input dán link Google Docs kèm nút kiểm tra link.
  * Tiêu chí hoàn thành: Kéo thả 3 file cùng lúc hiển thị đầy đủ, cho phép thêm bớt tệp linh hoạt.

- [ ] **Task 5.5: Xây dựng tương tác Bước 2: Bộ chọn 5 thông số Wizard**
  * Tệp tác động: `web/static/js/app.js`
  * Nội dung:
    * Dropdown 7 lĩnh vực chuẩn có icon đại diện.
    * Grid 10 nút bấm chọn nhanh cấp bậc slide (từ Bậc 1 đến Bậc 10 kèm số lượng slide ước tính).
    * 5 swatch màu preset (Ocean Blue `#0284C7`, Emerald Green `#10B981`, Royal Violet `#8B5CF6`, Crimson Red `#EF4444`, Amber Gold `#F59E0B`) + ô chọn màu Color Picker tự do đồng bộ preview.
    * Nhóm radio card chọn nền: Dark Obsidian, Light Pearl, Dual-Theme (ZIP).
    * Textarea ghi chú yêu cầu bổ sung (`special_notes`).
  * Tiêu chí hoàn thành: Form kiểm tra hợp lệ đầy đủ trước khi kích hoạt nút "Tạo Bài Trình Chiếu".

- [ ] **Task 5.6: Xây dựng tương tác Bước 3: Giám sát tiến độ qua WebSocket Real-time & Auto-Reconnect**
  * Tệp tác động: `web/static/js/app.js`
  * Nội dung: Kết nối `WebSocket` tới `/ws/jobs/{job_id}`. Cập nhật tiến độ % và chuyển đổi 4 step icon:
    * `[1/4] Ingestion` -> `[2/4] AI model plan` -> `[3/4] MACC-QA Review` -> `[4/4] PowerPoint COM`.
    * Tự động kết nối lại (Exponential Backoff) nếu mạng chập chờn.
  * Tiêu chí hoàn thành: Thanh tiến trình hiển thị trực quan, log chi tiết hiển thị mượt mà.

- [ ] **Task 5.7: Xây dựng tương tác Bước 4: Tải kết quả 1-Click & Thẻ thông số thành phẩm**
  * Tệp tác động: `web/static/js/app.js`
  * Nội dung: Khi nhận trạng thái `COMPLETED` từ WebSocket -> hiển thị nút tải nổi bật kèm định dạng file (`.pptx` hoặc `.zip`). Thẻ hiển thị tổng số slide và điểm MACC-QA. Nút "Tạo bài trình chiếu mới" để reset form.
  * Tiêu chí hoàn thành: Nhấp nút tải -> file tự động tải về máy tính trong 1 giây.

- [ ] **Task 5.8: Kiểm thử giao diện trên các trình duyệt phổ biến**
  * Tệp tác động: Toàn bộ thư mục `web/static/`
  * Nội dung: Kiểm thử trên Google Chrome, Microsoft Edge, Mozilla Firefox và Safari.
  * Tiêu chí hoàn thành: Giao diện đồng nhất 100%, không lỗi JavaScript console.

---

### PHASE 6: PUBLIC INGRESS CLOUDFLARE, AUTO-CLEANUP & KIỂM THỬ TOÀN DIỆN (SPRINT 6)
*Mục tiêu: Đưa ứng dụng công khai ra Internet an toàn qua Cloudflare Tunnel, tự động dọn rác và kiểm thử toàn trình.*

- [ ] **Task 6.1: Cài đặt và cấu hình Cloudflare Tunnel (`cloudflared`) trên máy chủ**
  * Tệp tác động: Máy chủ Windows, thư mục gốc
  * Nội dung: Cài đặt `cloudflared.exe`. Cấu hình tunnel định tuyến cổng `8000` của FastAPI.
  * Tiêu chí hoàn thành: Sinh ra URL HTTPS công khai (ví dụ: `https://xxx.trycloudflare.com` hoặc domain riêng), truy cập được từ thiết bị di động mạng ngoài.

- [ ] **Task 6.2: Viết script khởi chạy một chạm `run_server_public.bat`**
  * Tệp tác động: `run_server_public.bat`
  * Nội dung: Script Windows batch tự động kích hoạt song song 2 tiến trình:
    1. FastAPI Server: `python -m uvicorn web.app:app --host 0.0.0.0 --port 8000`
    2. Cloudflare Tunnel: `cloudflared tunnel --url http://localhost:8000`
    Hiển thị thông báo trạng thái và link truy cập công khai trên màn hình console.
  * Tiêu chí hoàn thành: Nhấp đúp file `.bat` -> cả máy chủ web và đường hầm public đều khởi động trơn tru.

- [ ] **Task 6.3: Xây dựng tiến trình dọn dẹp file tạm tự động sau 24h (Background Janitor)**
  * Tệp tác động: `web/app.py`
  * Nội dung: Background task chạy mỗi 60 phút quét thư mục `Du_An_Outputs/web_sessions/`. Xóa các thư mục phiên làm việc có thời gian tạo vượt quá 24 giờ.
  * Tiêu chí hoàn thành: Ổ đĩa máy chủ không bị đầy sau nhiều ngày vận hành liên tục.

- [ ] **Task 6.4: Kiểm thử toàn trình End-to-End (E2E Integration Testing)**
  * Tệp tác động: Toàn hệ thống
  * Kịch bản:
    1. Truy cập URL Cloudflare trên mạng 4G ngoài máy chủ.
    2. Đăng nhập Gmail thành công.
    3. Tải lên tệp Word mẫu `test_sample_document.docx` + link Google Docs.
    4. Chọn chủ đề `KINH_TE`, Bậc 3 (8-12 slide), màu `Ocean Blue`, chế độ `DUAL`.
    5. Theo dõi tiến trình WebSocket đạt 100%.
    6. Tải tệp `.zip`, giải nén và mở kiểm tra trực tiếp trên Microsoft PowerPoint.
  * Tiêu chí hoàn thành: Cả 2 file PPTX mở thành công, hiệu ứng Morph và biểu đồ Excel hiển thị sắc nét.

- [ ] **Task 6.5: Kiểm thử chịu tải và khả năng tự hồi phục (Resilience & Chaos Testing)**
  * Tệp tác động: `tests/test_chaos_resilience.py`
  * Kịch bản: Gửi đồng thời 5 request tạo slide; cưỡng chế tắt tiến trình `POWERPNT.EXE` trong khi đang render; kiểm tra cơ chế Watchdog tự động thu hồi và phục vụ các tác vụ kế tiếp.
  * Tiêu chí hoàn thành: Máy chủ không bị treo, hàng đợi tiếp tục xử lý các tác vụ sau thành công.

- [ ] **Task 6.6: Rà soát an ninh mã nguồn & Đóng gói tài liệu vận hành**
  * Tệp tác động: `docs/USER_OPERATIONS_MANUAL.md`, `README.md`
  * Nội dung: Rà soát không để lộ API key trong code tĩnh; hoàn thiện tài liệu hướng dẫn vận hành chi tiết cho người quản trị.
  * Tiêu chí hoàn thành: Bàn giao trọn gói hệ thống sẵn sàng vận hành sản xuất.
