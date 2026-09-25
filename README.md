# Make Slide Pro (V9.3 - Canonical Official Enterprise Release with MAS-CLSH V9.5)

**Make Slide Pro V9.3** là phiên bản chính thức, duy nhất và mặc định của hệ sinh thái tự động hóa biên dịch, thẩm định đa tác tử và xuất bản slide thuyết trình PowerPoint chất lượng cao chuẩn Apple Keynote & McKinsey trực tiếp từ bất kỳ nguồn tài liệu nào (`.docx`, `.pdf`, `.txt`, `.md`).

---

## 1. Điểm Đột Phá Ở Phiên Bản Chính Thức V9.3 (KMCA V9.3 & MAS-CLSH V9.5)

- **Kiến Trúc Chuyển Tiếp Kinetic Morph Liền Mạch (Kinetic Morph Continuity Architecture - KMCA V9.3)**:
  - **100% Pure Continuous Morph By Word** (`ppEffectMorphByWord` = 3955, `Duration = 0.85s`) cho toàn bộ slide nội dung (Slide 2 đến N-1). Trượt biến hình không gian liền mạch, các từ khóa, câu từ và số liệu lướt bay mượt mà theo ngữ nghĩa chuẩn Apple Keynote.
  - **Khế Ước Cầu Nối Morph (Morph Bridge Contract)**: Thẻ mở đầu (Card 0 / `!!Kinetic_Card_1!!`) hiện diện trực tiếp trên slide canvas và tham gia trọn vẹn vào chuyển tiếp slide (0.85s Morph), loại bỏ hoàn toàn animation nội bộ gây chặn Morph.
  - **Khế Ước Định Danh Toàn Diện (Universal `!!Kinetic_Card_N!!` Contract)**: 100% thẻ nội dung và ray cố định (`!!Anchor_Assertion_Title!!`, `!!Anchor_Kicker_Rail!!`, `!!Anchor_Slide_Tracker!!`, `!!Kinetic_Card_N!!`) được gán nhãn đồng nhất trên Selection Pane.
  - **Cinematic Smooth Fade** (`ppTransitionFadeSmoothly` = 3849, 0.65s) trang trọng dành riêng cho Slide Bìa và Slide Kết Luận.
- **Bộ Đọc & Phân Tích Dữ Liệu Nguồn Chuyên Sâu (Deep Source Ingestion & Grounding Engine)**:
  - Loại bỏ hoàn toàn cơ chế cắt cụt 25 từ cơ học.
  - Trích xuất trọn vẹn câu sư phạm 45 từ bảo toàn cấu trúc ngữ pháp và dữ liệu định lượng chuyên sâu (tỷ số giới tính khi sinh, các tuần siêu âm hình thái học 18–22 tuần, phác đồ y tế, chỉ số nhân khẩu học...).
  - Thuật toán `derive_smart_concept_title` tự động chiết xuất tiêu đề thẻ mang tính khái niệm thực thụ, khử sạch 100% AI slop và placeholder generic.
- **Bộ Giải Hình Học & Phông Chữ Thích Ứng (Adaptive Geometry & Executive Typography)**:
  - **Khóa cứng sàn phông chữ (Typography Floor)**: Nội dung thẻ $\ge 15.5-16.5\text{pt}$ (không có chữ $< 14.5\text{pt}$), Tiêu đề thẻ $\ge 18.5-20\text{pt}$ bold, Tiêu đề Assertion $\ge 26-28\text{pt}$ bold.
  - **Thẻ cao $350-365\text{pt}$ lấp đầy canvas 16:9**, triệt tiêu hoàn toàn khoảng chết đen (zero dead space).
  - **Tái cấu trúc Bento/Split cards**: Cột phụ 2 thẻ xếp dọc rộng rãi (176–197pt/thẻ), triệt tiêu 100% va chạm và tràn chữ (zero collision).
- **Hệ Thống Đa Tác Tử Tự Phục Hồi Khép Kín (MAS-CLSH V9.5)**:
  - Hội đồng 4 thanh tra chuyên trách (`inspectors/`): *Content Grounding*, *Inter-Slide Motion*, *Layout Typography*, *DataViz Math*.
  - Bộ điều phối chẩn đoán gốc rễ (`RootCauseDiagnosticAgent`) hợp nhất chỉ thị phục hồi đa miền (`CONSOLIDATED`).
  - Bác sĩ phẫu thuật slide (`SurgicalSlideRemediator`) tái sinh slide khuyết tật qua PowerPoint COM và tự động kế thừa chuẩn Morph 0.85s liên tục.
- **Kiểm Soát Nhịp Trình Chiếu Chuẩn Sư Phạm (Presenter Pacing Sequencing)**:
  - Tự động nhóm các thành phần của từng thẻ qua cơ chế `safe_group`.
  - Thẻ mở đầu (Hero Card 0) xuất hiện cùng slide qua Morph (chống lỗi màn hình trống); mỗi lần click chuột (`msoAnimTriggerOnPageClick`) mở ra trọn vẹn 1 thẻ thông tin hoàn chỉnh.
  - Giới hạn cứng số clicks $\le 4$ clicks/slide, triệt tiêu 100% lỗi runaway clicks.
- **Kho Thư Viện Mega 165+ Archetypes Chuẩn Toàn Cầu**:
  - Tables (25), Strategic Frameworks (35), Processes & Timelines (30), Architectures & Systems (25), Native Office Charts (20 nhúng Excel thật), Keynote Containers (30).
  - Tự động chuẩn hóa phông chữ lớn $\ge 13.5-16\text{pt}$ trên toàn bộ 165+ mẫu.
- **Cổng Thẩm Định Pháp Y Sâu Đa Tầng (`audit_deck_deep_v92.py` & MAS-CLSH V9.5)**:
  - Tự động quét 100% slide sau xuất bản, đảm bảo 0 lỗi P0, 0 lỗi P1 và 100% Kinetic Morph liên tục. Đạt chứng nhận 100% PASS trên toàn bộ 391 slide thực tế.

---

## 2. Cài Đặt Nhanh

1. Cài đặt các thư viện phụ thuộc:
```powershell
pip install -r requirements.txt
```
2. Đảm bảo máy tính cài đặt Microsoft PowerPoint (Office 2016+).

---

## 3. Cách Sử Dụng

### Cách 0: Web Studio Trực Quan (Khuyến Nghị)
Khởi chạy ứng dụng Web Studio trên trình duyệt qua 1-click script:
- Nhấp đúp **`run_web_studio.bat`** (hoặc chạy `python run_web_studio.py`).
- Tự động mở trình duyệt tại `http://localhost:8000`: Kéo thả tài liệu, chỉnh sửa kịch bản storyboard trực quan, tương tác cùng trợ lý **AI Slide Copilot**, theo dõi tiến trình thời gian thực và trình chiếu toàn màn hình trực tiếp trên web!

### Cách 1: Kéo thả 1-Click
Kéo bất kỳ file `.docx`, `.pdf`, `.txt`, hoặc `.md` thả trực tiếp vào tệp `run_make_slide_pro.bat`.

### Cách 2: Giao diện dòng lệnh tương tác (Console Menu)
Nhấp đúp `run_make_slide_pro.bat` hoặc chạy:
```powershell
python make_slide_pro.py
```

### Cách 3: Dòng lệnh CLI
```powershell
# Xử lý 1 tệp tài liệu và tạo cả Dark & Light themes:
python make_slide_pro.py --input "duong_dan/tai_lieu.docx"

# Xử lý hàng loạt toàn bộ tài liệu trong một thư mục:
python make_slide_pro.py --input "duong_dan_thu_muc" --theme ALL
```

---

## 4. Tài Liệu Hướng Dẫn Chi Tiết

Vui lòng tham khảo tệp [USER_GUIDE.md](file:///d:/Make%20Slide%20PPT/USER_GUIDE.md) để xem hướng dẫn đầy đủ về cách soạn thảo tài liệu nguồn, tùy chỉnh giao diện và xử lý sự cố.
