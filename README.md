# Make Slide Pro (V7.3 - Production Suite)

**Make Slide Pro** là hệ thống phần mềm tự động hóa biên dịch và xuất bản slide thuyết trình PowerPoint chất lượng cao trực tiếp từ bất kỳ nguồn tài liệu nào (`.docx`, `.pdf`, `.txt`, `.md`).

---

## 1. Điểm Nổi Bật Ở Bản Đóng Gói V7.3

- **Hỗ Trợ Mọi Định Dạng Tài Liệu**: Bóc tách tự động tài liệu Word, PDF, văn bản thuần và Markdown; tự động nhận diện cấu trúc tiêu đề, bảng biểu, công thức toán học và số liệu định lượng.
- **Bảo Toàn Chi Tiết Toàn Diện (Exhaustive Deep-Curriculum)**: Không còn tình trạng tài liệu 30-40 trang bị thu gọn thành vài slide; hệ thống tự động phân tách sư phạm chi tiết 2–3 ý/slide, bám sát 100% nội dung gốc.
- **Khôi Phục & Chuẩn Hóa Công Thức Toán (`FORMULA_CARD`)**: Hiển thị phương trình định lượng (CDR, TFR, CBR, ASFR, ASDR, hàm số mũ, logistic, v.v.) trong các Hero Card sắc nét, typography chuẩn quốc tế.
- **Bảng Số Liệu Tương Tác Native (`DATA_TABLE`)**: Tự động chuyển bảng biểu từ tài liệu sang bảng gốc của PowerPoint với zebra-striping và tự động căn chỉnh tỷ lệ cột.
- **Thư Viện Minh Họa AI 16:9 Đạt Tỷ Lệ ~20% (`EDITORIAL_HERO`)**: Tích hợp các tác phẩm AI nghệ thuật chuẩn 16:9 ($1376 \times 768$), bo góc mềm mại, không có khung giả hay viền lỗi.
- **22 Dạng Biểu Đồ Số Liệu Chuyên Ngành (`CHART_AND_INSIGHTS`)**: Tháp dân số, radar cơ cấu tuổi, heatmap mất cân bằng giới tính, waterfall tuổi thọ, Gompertz mortality curve, v.v. (220 DPI).
- **Xuất Bản Hai Nền Song Hành (Dual-Theme)**: Tạo đồng thời bản **Dark Theme** (Nền tối Obsidian) và **Light Theme** (Nền sáng Corporate) đồng bộ 100% màu sắc.
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

### Cách 1: Kéo thả 1-Click
Kéo bất kỳ file `.docx`, `.pdf`, `.txt`, hoặc `.md` thả trực tiếp vào tệp `run_make_slide_pro.bat`.

### Cách 2: Giao diện tương tác
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
