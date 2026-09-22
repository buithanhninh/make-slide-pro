# Make Slide Pro (V9.3 - Canonical Official Enterprise Release)

**Make Slide Pro V9.3** là phiên bản chính thức, duy nhất và mặc định của hệ sinh thái tự động hóa biên dịch, thẩm định đa tác tử và xuất bản slide thuyết trình PowerPoint chất lượng cao chuẩn Apple Keynote & McKinsey trực tiếp từ bất kỳ nguồn tài liệu nào (`.docx`, `.pdf`, `.txt`, `.md`).

---

## 1. Điểm Đột Phá Ở Phiên Bản Chính Thức V9.3 (KMCA V9.3)

- **Kiến Trúc Chuyển Tiếp Kinetic Morph Liền Mạch (Kinetic Morph Continuity Architecture - KMCA V9.3)**:
  - **100% Pure Continuous Morph By Word** (`ppEffectMorphByWord` = 3955, `Duration = 0.85s`) cho toàn bộ slide nội dung (Slide 2 đến N-1). Trượt biến hình không gian liền mạch, các từ khóa, câu từ và số liệu lướt bay mượt mà theo ngữ nghĩa chuẩn Apple Keynote.
  - **Khế Ước Cầu Nối Morph (Morph Bridge Contract)**: Thẻ mở đầu (Card 0 / `!!Kinetic_Card_1!!`) hiện diện trực tiếp trên slide canvas và tham gia trọn vẹn vào chuyển tiếp slide (0.85s Morph), loại bỏ hoàn toàn animation nội bộ gây chặn Morph.
  - **Khế Ước Định Danh Toàn Diện (Universal `!!Kinetic_Card_N!!` Contract)**: 100% thẻ nội dung và ray cố định (`!!Anchor_Assertion_Title!!`, `!!Anchor_Kicker_Rail!!`, `!!Anchor_Slide_Tracker!!`, `!!Kinetic_Card_N!!`) được gán nhãn đồng nhất trên Selection Pane.
  - **Cinematic Smooth Fade** (`ppTransitionFadeSmoothly` = 3849, 0.65s) trang trọng dành riêng cho Slide Bìa và Slide Kết Luận.
- **Kiểm Soát Nhịp Trình Chiếu Chuẩn Sư Phạm (Presenter Pacing Sequencing)**:
  - Tự động nhóm các thành phần của từng thẻ qua cơ chế `safe_group`.
  - Thẻ mở đầu (Hero Card 0) xuất hiện cùng slide qua Morph (chống lỗi màn hình trống); mỗi lần click chuột (`msoAnimTriggerOnPageClick`) mở ra trọn vẹn 1 thẻ thông tin hoàn chỉnh.
  - Giới hạn cứng số clicks $\le 4$ clicks/slide, triệt tiêu 100% lỗi runaway clicks.
- **Kho Thư Viện Mega 165+ Archetypes Chuẩn Toàn Cầu**:
  - **Tables (25)**: Bảng ma trận so sánh SaaS, Heatmap 5x5, Thẻ điểm cân bằng BSC, Ma trận phân quyền RACI, So sánh song hành, v.v.
  - **Strategic Frameworks (35)**: Kim tự tháp Minto, Mô hình STEEPLE 7 trục, Khung Osterwalder Value Proposition Canvas, Ngôi nhà chiến lược Strategy House 2030, McKinsey 7S, SWOT 2x2, Ansoff, v.v.
  - **Processes & Timelines (30)**: Chu trình vòng lặp vô cực DevSecOps, Phương pháp đường găng Critical Path CPM, Lộ trình công nghệ 4 quý, Vòng đời Agile Scrum, v.v.
  - **Architectures & Systems (25)**: Hồ dữ liệu Data Lakehouse Medallion, Đường ống RAG AI Pipeline, Microservices Event-Driven, Mô hình Zero Trust, v.v.
  - **Microsoft Office Native Charts (20)**: Pareto 80/20, Radar đa trục lấp đầy, Histogram tần suất, Waterfall tài chính, Phễu chuyển đổi Sales Funnel (100% nhúng Excel Worksheet thật).
  - **Keynote Containers & Accents (30)**: Khung thiết bị Mockup MacBook Retina, Dải Marquee 4 chỉ số, 3 Trụ cột kính mờ Glassmorphism, Chuỗi Vấn đề - Giải pháp - Tác động (PSI), Executive Dashboard, Châm ngôn tối giản Apple, v.v.
- **Xóa Bỏ 100% Khoảng Trống Thừa (Zero Dead Space) & Cân Bằng Tỷ Lệ Vàng**:
  - Chuẩn hóa cấu trúc 3 tầng cho mọi card (Metric -> Body -> Anchor Badge đáy), triệt tiêu 100% khoảng trống chết.
- **Tự Động Chuẩn Hóa Biểu Đồ Tương Phản Cao (Auto-Themed High-Contrast Charts)**:
  - Tự động gán màu chữ sáng `#E2E8F0` cho trục và chú giải trên nền Dark Obsidian Canvas, loại bỏ viền xám mặc định của Excel.
- **Cổng Thẩm Định Pháp Y Sâu Đa Tầng (`audit_deck_deep_v92.py` & MAS-CLSH V9.3)**:
  - Tự động quét và thẩm định 100% file PPTX sau xuất bản, đảm bảo 0 lỗi P0, 0 lỗi P1 và 100% Kinetic Morph liên tục.

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
