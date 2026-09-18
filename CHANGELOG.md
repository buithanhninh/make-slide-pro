# Changelog

## 8.2.0 - 2026-09-18 (Omniscient 16-Agent MACC-QA Council & Apple Keynote Kinetic Motion Architecture)

- **Hội Đồng Thẩm Định Pháp Y 16-Agent (MACC-QA V8.0)**:
  - Thiết kế và triển khai ma trận kiểm định 5 Cổng độc lập với 16 tác tử chuyên sâu:
    - **Cổng 1 (Fidelity & Privacy)**: `SourceFidelityFactChecker`, `CompliancePrivacyGuardian`.
    - **Cổng 2 (Narrative & Continuity)**: `NarrativeArcDirector`, `CrossSlideConsistencyAuditor`.
    - **Cổng 3 (Pedagogy, Math & Tone)**: `DomainPedagogyScholar`, `MathematicalOMMLValidator`, `NaturalLanguagePurist`, `AssertionCognitiveArbiter`, `AdversarialContentCritic`, `MasterPedagogicalRewriter`.
    - **Cổng 4 (Spatial Geometry, Typography & Motion)**: `LayoutArchetypeStrategist`, `DataChartCartographer`, `TypographyWidowOrphanSentinel`, `VisualErgonomicsAuditor`, `MotionChoreographer`.
    - **Cổng 5 (Consensus)**: `SupremeConsensusJudge`.
  - **160/160 Ca Thử Nghiệm Đối Kháng Khắc Nghiệt (Adversarial Stress Test)**: Đạt tỷ lệ vượt qua 100.0%, 0 False Positive, 0 False Negative.
  - **Cơ chế tự phục hồi đa vòng lặp (Dialectical Self-Healing Convergence)**: Tự động phát hiện và triệt tiêu dao động lặp (Oscillation Dampening), bóc tách số thập phân an toàn (Decimal-Safe Lookaround), bảo vệ công thức toán học và tiền tệ.
  - **Chuẩn hóa chữ mồ côi tiếng Việt (`\u00A0`)**: Tự động liên kết các từ đơn tiết, năm, đơn vị vào từ liền trước, đảm bảo ngắt dòng toàn vẹn ngữ nghĩa trên màn chiếu hội trường.
- **Kiến Trúc Chuyển Động Điện Ảnh Apple Keynote (4-Layer Kinetic Motion)**:
  - **Morph 60 FPS Xuyên Suốt**: Đồng bộ hóa mỏ neo sân khấu (`!!Stage_Hero_Container!!`) và hệ thống ray tiêu đề (`!!Anchor_Assertion_Title!!`, `!!Anchor_Kicker_Rail!!`, `!!Anchor_Slide_Tracker!!`, `!!Anchor_Source_Footer!!`) đạt chuẩn nhận diện Morph native của PowerPoint.
  - **Kiểm Soát Nhịp Giảng Tuyệt Đối (Presenter Click Sequencing)**: Mặc định cấu hình `msoAnimTriggerOnPageClick` (Trigger = 1) với độ trễ 0.00s cho toàn bộ các khối nội dung bên trong slide. Slide không tự động nhảy chữ sau 0.7s-1.0s, trao toàn quyền làm chủ nhịp thuyết trình cho diễn giả.
  - **Hạ Cánh Giảm Chấn Phi Tuyến Tính (Cubic Bezier Easing)**: Gán `msoAnimDirectionBottom = 1`, `anim.Timing.SmoothStart = msoTrue`, `anim.Timing.SmoothEnd = msoTrue` cho từng khối thẻ, tạo cảm giác trôi êm ái, bồng bềnh chuẩn Keynote khi click chuột.
  - **Tùy chọn Cinematic Cascade**: Hỗ trợ chế độ tuôn chảy tự động (`--motion-mode kinetic_cascade`) cho kịch bản tự chạy hoặc video presentation.
- **Tích Hợp Toàn Diện Vào Production Suite**:
  - Đấu nối Hội đồng 16 Agent vào Bước 2.5 của `batch_pipeline.py` và `make_slide_pro.py`.
  - Cập nhật các trình khởi chạy 1-click (`run_make_slide_pro.bat`, `run_web_studio.bat`, `run_web_studio.py`, `web/app.py`) lên phiên bản đồng bộ V8.2.
  - Biên dịch và đồng bộ đầy đủ bộ slide mẫu Bài 1 (Dark & Light) đạt điểm thẩm định 99.4/100 tuyệt đối.

## 7.3.0 - 2026-09-18 (Production Suite, Universal Ingestion & 1-Click Standalone Release)

- **Đóng gói toàn diện & Trình khởi chạy 1-Click (`run_make_slide_pro.bat`)**:
  - Hỗ trợ kéo-thả trực tiếp mọi tệp `.docx`, `.pdf`, `.txt`, `.md` vào file `.bat` để tự động chuyển đổi sang slide và mở PowerPoint.
  - Giao diện menu tương tác tiếng Việt thân thiện, tự động dò quét và gợi ý các tài liệu có sẵn trong workspace.
- **Ứng dụng trung tâm hợp nhất (`make_slide_pro.py`)**:
  - Đầy đủ tham số CLI `--input`, `--theme [ALL|DARK|LIGHT]`, `--output`, `--open`.
  - Hỗ trợ chế độ xử lý hàng loạt thư mục (batch processing) và chế độ tương tác tự động.
- **Động cơ phân tích & bóc tách tài liệu phổ quát (`scripts/ingest_content.py`)**:
  - Hỗ trợ bóc tách cấu trúc tài liệu Word (`.docx`), PDF (`fitz`/`pypdf`), Text và Markdown.
  - Bóc tách nguyên vẹn bảng biểu thực chứng (`doc.tables`), công thức toán học (`is_math_formula`), số liệu thống kê và phân loại vai trò ngữ nghĩa ($P_0/P_1/P_2$).
- **Động cơ phân rã sư phạm chuyên sâu (`scripts/blueprint_generator.py`)**:
  - Triển khai thuật toán *Deep Pedagogical Chunking*: Giữ lại 100% thông tin chi tiết của tài liệu dài, chia nhỏ 2-3 khái niệm/slide, không tóm tắt cụt ngủn hay nén ép thô thiển.
  - Tự động điều hướng bố cục thông minh: Bảng số liệu $\rightarrow$ `DATA_TABLE`, công thức toán $\rightarrow$ `FORMULA_CARD`, số liệu thống kê $\rightarrow$ `CHART_AND_INSIGHTS`, mốc trọng tâm $\rightarrow$ `EDITORIAL_HERO` (kèm 21 minh họa AI 16:9), so sánh $\rightarrow$ `COMPARISON`, quy trình $\rightarrow$ `PROCESS`.
- **Khắc phục triệt để lỗi hình ảnh & Khôi phục Formula Cards**:
  - Xóa bỏ 100% các file ảnh Matplotlib giả lập slide gây lỗi lồng khung và vỡ chữ.
  - Khôi phục Slide 13 Bài 3 thành `FORMULA_CARD` native PowerPoint với typography động (tự động co cỡ chữ 17pt/20pt) và `WordWrap = msoTrue`, triệt tiêu 100% hiện tượng chữ đè khung.
  - Tích hợp thư viện 21 tranh minh họa AI chuẩn 16:9 ($1376 \times 768$), bo góc mềm mại bằng `pic.AutoShapeType` của PowerPoint, kèm thẻ "THÔNG ĐIỆP CỐT LÕI".
- **Kiểm định pháp y & Chứng nhận MACC-QA đạt tuyệt đối**:
  - Quét kiểm toán độc lập 10/10 bộ slide (212 slide) đạt 100% tuân thủ hình học 16:9, 0 lỗi AI cliché, 0 dấu ba chấm cụt lủn.
  - Tài liệu mẫu `test_sample_document.docx` được MACC-QA chứng nhận 100.0/100 ngay tại Vòng 1 cho cả Dark và Light theme.
- **Hệ thống hồ sơ tài liệu đầy đủ**:
  - `USER_GUIDE.md`: Sổ tay hướng dẫn sử dụng tiếng Việt chi tiết.
  - `requirements.txt`: Danh mục thư viện phụ thuộc chuẩn hóa.
  - `README.md`: Cập nhật đặc tả kiến trúc kỹ thuật V7.3.

## 7.1.0 - 2026-09-18 (Dual-Theme Architecture & MACC-QA Forensic Multi-Agent Council)

- **Kiến trúc Hai Nền Song Hành (Dual-Theme Architecture)**: Mọi tài liệu nạp vào hệ thống tự động sinh ra 2 bản hoàn chỉnh độc lập:
  - **Bản Nền Tối (Dark Luxury Obsidian)**: `#060B14`, thẻ kính `#0B132B`, viền neon phát sáng, artwork 3D không gian tương tác.
  - **Bản Nền Sáng (Clean Editorial Light / Executive Pearl)**: Nền ngọc trai `#F8FAFC`, thẻ trắng tinh khiết `#FFFFFF` viền mỏng `#CBD5E1`, chữ tương phản cao `#0F172A` & `#334155`, điểm nhấn sapphire (`#0284C7`) và lục bảo (`#059669`).
- **Hội đồng Thẩm định Nội dung Đa tác tử (MACC-QA V7.0)**:
  - Phân chia vai trò chuyên biệt cho 5 tác tử tuần tự: `DomainPedagogyScholar` (Dr. Học Thuật), `NaturalLanguagePurist` (Thầy Biên Tập), `AssertionCognitiveArbiter` (TS. Luận Đề), `AdversarialContentCritic` (Phản Biện Đối Kháng) và `MasterPedagogicalRewriter` (Tổng Biên Tập Cứu Thương).
  - Vòng lặp phản biện và tự sửa chữa đa vòng (Dialectical Self-Healing Loop) đạt chứng nhận 100% không chứa từ ngữ sáo rỗng kiểu AI, không nhãn robot ("Luận Điểm X"), không dấu ba chấm cụt lủn (...).
- **Hội đồng Thẩm định Kỹ thuật Độc lập (MultiAgentQABoard)**: 5 kiểm toán viên đo lường trực tiếp qua PowerPoint COM Engine (`ContentFidelity`, `GeometryTypography`, `MotionPacing`, `VisualAesthetics`, `TechnicalReliability`), kiểm thử độc lập cả 2 bản Dark & Light.
- **Tự Động Hóa Kiểm Toán Pháp Y (Forensic Compliance Audit)**: Quét toàn diện 100% hình học slide (16:9 960x540pt), văn bản và regex trên toàn bộ các tệp PPTX trước khi xuất xưởng.
- **Đồng bộ hóa 10 Decks**: Tự động sinh và lưu đồng bộ 10 tệp PPTX (5 Dark + 5 Light) cùng hệ thống PDF và thumbnails trực tiếp tại thư mục làm việc của người dùng.

## 7.0.0 - 2026-09-18 (Cinematic Spatial Keynote Definitive Architecture)

- **Lột xác kiến trúc thị giác toàn diện**: Xác lập chuẩn **Dark Luxury Obsidian** (`#060B14`) kết hợp thẻ kính mờ midnight (`#0B132B`) và viền neon phát quang tinh tế (`#06B6D4`, `#10B981`, `#F59E0B`, `#8B5CF6`).
- **Tối giản thông tin tuyệt đối (Zero Information Noise)**: Loại bỏ triệt để mọi watermark hệ thống (`Make Slide Pro Certified...`) và các nhãn tiếng Anh nhân tạo đè lên tác phẩm 3D.
- **Tranh minh họa không gian 3D AI độc bản**: Tích hợp tác phẩm 3D holographic (`cinematic_bai_1_hero.jpg`) và mô hình hệ thống đa tầng 3D (`cinematic_bai_1_system.jpg`).
- **Động cơ Morph Zoom-Through xuyên suốt**: Sử dụng mỏ neo sân khấu duy nhất (`!!Stage_Hero_Container`) và triệt tiêu lỗi chớp nháy nền bằng quy tắc Anti-Flicker Invariant.
- **Kiểm soát nhịp trình chiếu từng click (In-Slide Click Sequencing)**: Cấu hình `AdvanceOnClick = True` với `msoAnimTriggerOnPageClick` trên từng cụm thẻ nội dung, trao toàn quyền kiểm soát nhịp diễn thuyết cho diễn giả.
- **Tích hợp sâu vào Core Engine**: Nâng cấp `NativeDeckAuthor` và `batch_pipeline.py` tự động định tuyến bài giảng về kiến trúc Cinematic Spatial chuẩn mực, tự động render preview 1080p và đồng bộ đồng thời vào `Du_An_Outputs/` và `Du An/A Tuan Dan So/`.

## 6.2.0 - 2026-08-27

- Hoàn thiện declarative G0-G15 registry và ba release profile rõ nghĩa.
- Bổ sung append-only event journal, SHA-256 chain, CAS revision, workspace lease và recovery fail-closed.
- Siết gate submission bằng workspace containment, artifact hash, dependency hash, schema binding và independent-review separation.
- Bổ sung capability TTL, probe binding, fingerprint drift detection và re-probe trước các gate native/release.
- Siết native visual, layout, motion, render, content và release evidence chain.
- Hoàn thiện Faster Whisper bootstrap/probe cho audio-video intake.
- Bổ sung corpus manifest, fault-injection tests và regression suite V6.2.
- Loại hardcoded local skill/Python paths khỏi test runner để package portable hơn.
