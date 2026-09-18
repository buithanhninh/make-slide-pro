# Make Slide Pro (V8.2 - Enterprise Production Suite)

**Make Slide Pro** là hệ sinh thái phần mềm tự động hóa biên dịch, thẩm định đa tác tử và xuất bản slide thuyết trình PowerPoint chất lượng cao chuẩn Executive trực tiếp từ bất kỳ nguồn tài liệu nào (`.docx`, `.pdf`, `.txt`, `.md`).

---

## 1. Điểm Đột Phá Ở Bản Đóng Gói V8.2

- **Hội Đồng Thẩm Định Pháp Y 16-Agent (MACC-QA V8.0)**: 
  - Quy tụ 16 chuyên gia và thẩm phán độc lập chia thành 5 Cổng (Gates): Thẩm định nguồn tin & tuân thủ, đạo diễn cốt truyện Minto, học giả chuyên ngành & toán học OMML, kiến trúc hình học & công thái học WCAG AAA, và Thẩm phán Tối cao hội tụ đa vòng lặp.
  - Vượt qua **160/160 ca kiểm thử đối kháng khắc nghiệt** (100% Pass, 0 False Positive, 0 False Negative).
  - Tự động thanh trừng ảo giác số liệu, triệt tiêu từ sáo rỗng AI và xử lý dứt điểm từ mồ côi tiếng Việt (`\u00A0`).
- **Kiến Trúc Chuyển Động Điện Ảnh Apple Keynote (4-Layer Kinetic Motion)**:
  - **Morph 60 FPS Xuyên Suốt**: Mỏ neo sân khấu đồng bộ liên slide (`!!Stage_Hero_Container!!`, `!!Anchor_Assertion_Title!!`,...), loại bỏ 100% hiện tượng chớp nhấp nháy nền.
  - **Kiểm Soát Nhịp Giảng Tuyệt Đối (Presenter Click Sequencing)**: Các khối nội dung chi tiết trong slide chỉ xuất hiện khi diễn giả click chuột (`AdvanceOnClick`), không tự động hiện ra gây phân tâm người nghe.
  - **Hạ Cánh Giảm Chấn Phi Tuyến Tính (Cubic Bezier Easing)**: Trôi êm ái từ dưới lên trên (`SmoothStart`, `SmoothEnd`), mang lại trải nghiệm thuyết trình đẳng cấp thế giới.
- **Hỗ Trợ Mọi Định Dạng Tài Liệu**: Bóc tách tự động tài liệu Word, PDF, văn bản thuần và Markdown; tự động nhận diện cấu trúc tiêu đề, bảng biểu, công thức toán học và số liệu định lượng.
- **Bảo Toàn Chi Tiết Toàn Diện (Exhaustive Deep-Curriculum)**: Phân tách sư phạm chi tiết 2–3 ý/slide, bám sát 100% nội dung gốc mà không nén cụt lủn.
- **Khôi Phục & Chuẩn Hóa Công Thức Toán (`FORMULA_CARD`)**: Hiển thị phương trình định lượng (CDR, TFR, CBR, ASFR, ASDR, hàm số mũ, logistic, v.v.) trong các Hero Card sắc nét.
- **Bảng Số Liệu Tương Tác Native (`DATA_TABLE`)**: Tự động chuyển bảng biểu sang bảng native PowerPoint với zebra-striping và tự động căn tỷ lệ cột.
- **Thư Viện Minh Họa AI 16:9 Đạt Chuẩn (`EDITORIAL_HERO`)**: Tích hợp các tác phẩm AI nghệ thuật chuẩn 16:9 ($1376 \times 768$), bo góc mềm mại kèm thông điệp cốt lõi.
- **22 Dạng Biểu Đồ Số Liệu Chuyên Ngành (`CHART_AND_INSIGHTS`)**: Tháp dân số, radar cơ cấu tuổi, heatmap, waterfall, Gompertz curve, v.v. (220 DPI).
- **Xuất Bản Hai Nền Song Hành (Dual-Theme)**: Tạo đồng thời bản **Dark Luxury Obsidian** và **Light Editorial Pearl** đồng bộ 100% màu sắc.
- **Trình Khởi Chạy 1-Click (`run_make_slide_pro.bat` & `make_slide_pro.py`)**: Kéo thả tệp tài liệu vào file `.bat` để hoàn thành bài giảng trong tích tắc.

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
