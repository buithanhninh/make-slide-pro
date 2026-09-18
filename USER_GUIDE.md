# SÁCH HƯỚNG DẪN SỬ DỤNG PHẦN MỀM MAKE SLIDE PRO (V7.3)
### Universal Document-to-PowerPoint AI Publishing & Multi-Agent Quality Certification System

---

## 1. Giới Thiệu Tổng Quan

**Make Slide Pro V7.3** là hệ sinh thái phần mềm tự động hóa biên dịch bài giảng và bài trình chiếu chuyên nghiệp, chuyển hóa bất kỳ tệp tài liệu nguồn nào (`.docx`, `.pdf`, `.txt`, `.md`) thành bài thuyết trình Microsoft PowerPoint (.pptx) chuẩn Executive.

### Các Tính Năng Đột Phá Đã Được Chuẩn Hóa:
1. **Không cắt xén, không làm tắt (Exhaustive Deep-Curriculum)**: Tự động phân tách tài liệu dài 30-40 trang thành số lượng slide tương xứng (20–40 slide), bảo toàn 100% tri thức và định nghĩa cốt lõi.
2. **Khôi phục công thức toán học (`FORMULA_CARD`)**: Hiển thị phương trình định lượng (như $CDR$, $TFR$, $ASFR$, $IMR$, hàm số mũ, logistic, v.v.) bằng các thẻ Hero Card nổi bật chuẩn typography, loại bỏ hoàn toàn ảnh mờ hay vỡ font.
3. **Bảng số liệu tương tác (`DATA_TABLE`)**: Tự động chuyển đổi các bảng biểu trong Word thành bảng PowerPoint native có zebra-striping và độ rộng cột tối ưu.
4. **Kho 22 dạng biểu đồ số liệu chuyên sâu (`CHART_AND_INSIGHTS`)**: Tích hợp tháp dân số, radar cơ cấu tuổi, heatmap mất cân bằng giới tính, waterfall tuổi thọ, Gompertz mortality curve, v.v. (độ phân giải 220 DPI).
5. **Thư viện minh họa AI 16:9 sắc nét (`EDITORIAL_HERO` & `COVER`)**: Phân bổ cân đối ~20% toàn bộ giáo trình với bo góc tự động (`pic.AutoShapeType`), viền sắc nét, kèm thẻ "THÔNG ĐIỆP CỐT LÕI". Không chứa ảnh vẽ thô hay thẻ lồng thẻ.
6. **Hệ màu kép Dual-Theme**: Xuất bản đồng thời 2 bản **Dark Theme** (Nền tối Obsidian sang trọng) và **Light Theme** (Nền sáng Corporate thanh lịch).
7. **Kiểm định pháp lý 100% (MACC-QA & Forensic Compliance)**: Tự động quét sạch từ sáo rỗng AI, nhãn robot ("Luận điểm X"), dấu ba chấm cụt và watermark.

---

## 2. Yêu Cầu Hệ Thống & Cài Đặt Trong 1 Phút

### Yêu Cầu Môi Trường:
- **Hệ điều hành**: Windows 10 hoặc Windows 11 (yêu cầu để chạy Microsoft PowerPoint COM Engine).
- **Phần mềm**: Microsoft PowerPoint (Office 2016, 2019, 2021 hoặc Microsoft 365).
- **Python**: Phiên bản 3.9 trở lên (đã cấu hình sẵn trong máy).

### Cài Đặt Thư Viện:
Mở terminal tại thư mục dự án và chạy:
```powershell
pip install -r requirements.txt
```
*(Các thư viện gồm: `python-docx`, `pywin32`, `matplotlib`, `numpy`, `PyMuPDF`, `pypdf`)*.

---

## 3. Ba Cách Khởi Chạy Make Slide Pro

### Cách 1: Kéo Thả 1-Click (Dễ Nhất)
1. Mở thư mục `Make Slide PPT`.
2. Kéo tệp tài liệu của bạn (ví dụ: `Tai_Lieu.docx` hoặc `Bao_Cao.pdf`) và **thả trực tiếp vào tệp `run_make_slide_pro.bat`**.
3. Phần mềm sẽ tự động nạp liệu, dựng slide, kiểm định QA và tự động mở file PowerPoint hoàn tất lên cho bạn!

### Cách 2: Chế Độ Menu Tương Tác (Interactive Mode)
Chỉ cần nhấp đúp vào `run_make_slide_pro.bat` hoặc gõ:
```powershell
python make_slide_pro.py
```
- Màn hình sẽ hiển thị danh sách các tệp tài liệu tìm thấy trong thư mục.
- Bạn chọn số thứ tự tài liệu cần làm slide.
- Chọn chủ đề (1: Cả Dark & Light, 2: Dark, 3: Light).
- Hệ thống sẽ tự động chạy toàn bộ quy trình.

### Cách 3: Dòng Lệnh Nâng Cao (CLI Dành Cho Chuyên Gia)
Bạn có thể tùy biến mọi tham số trực tiếp qua terminal:

```powershell
# Tạo cả 2 bản Dark & Light từ file Word:
python make_slide_pro.py --input "duong_dan/tai_lieu.docx"

# Chỉ tạo bản Dark Theme và tự động mở slide khi xong:
python make_slide_pro.py --input "duong_dan/tai_lieu.pdf" --theme DARK --open

# Chỉ định thư mục xuất kết quả:
python make_slide_pro.py --input "tai_lieu.docx" --output "Thu_Muc_Slide"

# Xử lý hàng loạt toàn bộ tệp trong một thư mục:
python make_slide_pro.py --input "Du An/A Tuan Dan So" --theme ALL
```

---

## 4. Hướng Dẫn Soạn Thảo Tài Liệu Nguồn Tối Ưu

Để bài giảng đạt chất lượng bố cục và đồ họa đẹp nhất, tài liệu nguồn nên tuân thủ các quy chuẩn đơn giản sau:

| Thành Phần | Cách Trình Bày Trong Tài Liệu Nguồn | Kết Quả Slide Tạo Ra |
| :--- | :--- | :--- |
| **Tiêu đề lớn / Bài** | Định dạng Style `Heading 1` hoặc viết hoa có đánh số (ví dụ: `BÀI 1. TỔNG QUAN`) | Slide Bìa (`COVER`) với ảnh nghệ thuật AI 16:9 và luận đề chính. |
| **Tiêu đề mục** | Định dạng Style `Heading 2`, `Heading 3` hoặc `I.`, `1.1`, `a.` | Phân chia thành các slide chuyên đề liên hoàn. |
| **Bảng số liệu** | Tạo bảng chuẩn trong Word (`Insert Table`) | Tự động tạo slide `DATA_TABLE` native PowerPoint với màu sắc đồng bộ và zebra-striping. |
| **Công thức toán** | Viết công thức rõ ràng, ví dụ: `CDR = (D / P_tb) * 1000` | Tự động đưa vào slide `FORMULA_CARD` với Hero Box viền sapphire/emerald nổi bật. |
| **Số liệu thống kê** | Chứa các tỷ lệ %, số lượng, xu hướng tăng giảm | Tự động điều hướng sang slide `CHART_AND_INSIGHTS` với biểu đồ nhân khẩu học chuyên sâu. |
| **Đoạn văn dài** | Chia các đoạn ngắn (mỗi đoạn 1 luận điểm) | Tự động chia thành các slide 2-3 thẻ (`CARDS`, `BENTO_GRID`, `PROCESS`, `COMPARISON`). |

---

## 5. Cấu Trúc Thư Mục Kết Quả (Outputs)

Khi biên dịch một tài liệu, kết quả được tổ chức khoa học:

```
Du_An_Outputs/
└── Ten_Tai_Lieu/
    ├── Ten_Tai_Lieu_Dark.pptx          <-- Slide bản Nền Tối hoàn chỉnh
    ├── Ten_Tai_Lieu_Light.pptx         <-- Slide bản Nền Sáng hoàn chỉnh
    ├── canonical-content.json          <-- Dữ liệu tri thức đã chuẩn hóa
    ├── slide-blueprints.json           <-- Bản vẽ kiến trúc từng slide
    ├── qa-certification-report.json    <-- Báo cáo kiểm định chất lượng 5 tác tử
    ├── dark_qa/
    │   ├── Ten_Tai_Lieu_Dark.pdf       <-- Tệp PDF phân giải cao
    │   └── thumbnails/                 <-- Toàn bộ ảnh chụp slide xem trước
    └── light_qa/
        ├── Ten_Tai_Lieu_Light.pdf
        └── thumbnails/
```

---

## 6. Xử Lý Sự Cố Thường Gặp (Troubleshooting)

1. **Lỗi `python-docx is required`**:
   Chạy lệnh `pip install python-docx`.
2. **Lỗi `pywintypes.com_error` khi chạy**:
   Đảm bảo Microsoft PowerPoint trên máy không bị treo hoặc đang mở hộp thoại thông báo modal. Hãy đóng PowerPoint và chạy lại.
3. **Kéo thả tệp có dấu cách hoặc tiếng Việt**:
   Tệp `run_make_slide_pro.bat` và mã nguồn Python đã hỗ trợ Unicode UTF-8 toàn diện (`chcp 65001`), an toàn tuyệt đối với mọi đường dẫn tiếng Việt.
