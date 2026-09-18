# Cinematic Spatial Keynote Architecture Standard (Make Slide Pro Definitive V7.0)

> [!IMPORTANT]
> **Định Chuẩn Kiến Trúc Bắt Buộc (Definitive Architecture Standard)**:
> Mọi slide deck được tạo ra bởi Make Slide Pro từ phiên bản này trở đi PHẢI tuân thủ 100% các nguyên tắc kiến trúc sau đây. Đây là tiêu chuẩn chất lượng cao nhất, không được hạ cấp (fail-closed downgrade prevention).

---

## 1. Hệ Ngôn Ngữ Thiết Kế: Dark Luxury Obsidian & Glassmorphism

- **Màu nền chủ đạo (Canvas Backdrop)**:
  - Tông đen nguyên khối sâu thẳm: `#060B14` (Obsidian Base). Tuyệt đối không dùng nền trắng văn phòng nhàm chán (`#F8FAFC`).
- **Khối bề mặt thẻ (Card Surfaces)**:
  - Màu thẻ nền tối: `#0B132B` (Midnight Slate).
  - Bo góc mềm mại: Bán kính 8pt – 14pt (`msoShapeRoundedRectangle`).
  - Viền phát quang siêu mỏng (Neon Edge Catch): 1.0pt – 1.5pt với các màu điểm nhấn:
    - **Cyan Accent**: `#06B6D4` (Viền thẻ), `#38BDF8` (Text highlight & badge).
    - **Emerald Accent**: `#10B981` (Viền thẻ), `#34D399` (Text highlight & badge).
    - **Amber Accent**: `#F59E0B` (Viền thẻ), `#FBBF24` (Text highlight & badge).
    - **Violet Accent**: `#8B5CF6` (Viền thẻ), `#A78BFA` (Text highlight & badge).
- **Hệ Thống Phông Chữ (Typography Hierarchy)**:
  - Tiêu đề chính: `Segoe UI` Bold, màu trắng ngọc trai `#FFFFFF` (26pt – 36pt).
  - Nội dung diễn giải: `Segoe UI` Regular, màu xám ánh kim `#CBD5E1` hoặc `#94A3B8` (12.5pt – 15pt), line spacing 1.25x – 1.35x.
  - Số liệu thống kê lớn: Font cơ điện tử `Bahnschrift` Bold (34pt – 44pt), màu neon nổi bật (`#38BDF8`, `#34D399`, `#FBBF24`). Tương phản WCAG AAA > 12:1.

---

## 2. Nguyên Tắc Tối Giản Tuyệt Đối: Zero Information Noise

- **Tuyệt đối CẤM chèn Watermark hệ thống**:
  - Không được phép chèn các dòng chữ meta như `Make Slide Cinematic Keynote...` hay `Make Slide Pro Certified...` vào chân trang slide.
- **Tuyệt đối CẤM chèn nhãn tiếng Anh đè lên tác phẩm 3D**:
  - Không đặt các pill badge như `SPATIAL DEMOGRAPHIC NEXUS`, `3D SPATIAL SYSTEM: DYNAMICS MATRIX` lên mặt tranh. Tác phẩm không gian 3D AI phải được hiển thị trọn vẹn, thanh thoát, không có chi tiết thừa gây phân tán thị giác người học.

---

## 3. Tranh Minh Họa Không Gian 3D AI Độc Bản (Bespoke Spatial Artworks)

- Mỗi bài giảng / chuyên đề đều phải có tác phẩm 3D AI chuyên biệt được tạo từ mô hình AI hàng đầu:
  - **Bài 1**: Quả địa cầu dữ liệu 3D Holographic phát quang (`assets/illustrations/cinematic_bai_1_hero.jpg`).
  - **Ma trận hệ thống**: Mô hình không gian 3D Glassmorphic đa tầng (`assets/illustrations/cinematic_bai_1_system.jpg`).
- Tác phẩm 3D đóng vai trò là mỏ neo thị giác trung tâm (Visual Stage Anchor), tạo cảm giác hoành tráng như sự kiện ra mắt sản phẩm của Apple hoặc TED Talk.

---

## 4. Chuyển Động Không Gian Xuyên Suốt (Unbroken Morph Zoom-Through)

- **Mỏ Neo Sân Khấu Duy Nhất (`!!Stage_Hero_Container`)**:
  - Khi chuyển từ Slide 1 sang Slide 2, quả cầu 3D khổng lồ từ bên phải tự động thu nhỏ và lướt mượt mà sang bên trái làm mỏ neo ngữ cảnh (`ppEffectMorphByObject = 3954`, Duration = 0.9s).
  - Sang Slide 3, container morph thành Trụ cột 1. Sang Slide 4, container morph sang phải đón nhận Ma trận 3D. Sang Slide 6, container biến hóa thành Dải băng Tổng kết Chiến lược.
- **Quy Tắc Chống Chớp Nháy Nền (Anti-Flicker Invariant)**:
  - Thể container `!!Stage_Hero_Container` trên slide đích **KHÔNG ĐƯỢC CÓ entrance animation**. Phải để PowerPoint Morph tự do biến đổi toạ độ và kích thước, triệt tiêu hoàn toàn hiện tượng chớp nháy hoặc biến mất đột ngột.

---

## 5. Kiểm Soát Nhịp Trình Bày Từng Click (In-Slide Click Sequencing)

- **Quy trình kích hoạt tuần tự (`AdvanceOnClick = True`)**:
  - Khi diễn giả bấm Next sang slide mới: Hiệu ứng Morph chuyển cảnh diễn ra êm ái (0.9s), cố định bộ khung nền và tiêu đề. **TẤT CẢ các thẻ nội dung chi tiết vẫn ẩn**.
  - **Click 1**: Thẻ nội dung 1 (`Card 1`) trượt nhẹ và mờ dần vào vị trí (`Fly / Fade on Click`).
  - **Click 2**: Thẻ nội dung 2 (`Card 2`) trượt nhẹ vào vị trí.
  - **Click 3**: Thẻ nội dung 3 (`Card 3`) trượt nhẹ vào vị trí.
  - **Click tiếp theo**: Chuyển tiếp sang slide kế tiếp.
- Diễn giả nắm toàn quyền kiểm soát nhịp độ bài giảng, không bị hiện tượng nội dung tràn ra cùng lúc gây mất tập trung.

---

## 6. Lộ Trình Triển Khai Trong Mã Nguồn

- `scripts/author_cinematic_keynote.py`: Flagship Authoring Engine cho định dạng Cinematic Spatial Keynote.
- `scripts/author_native_com.py`: Được đồng bộ toàn bộ bảng màu Obsidian và loại bỏ watermark/noise.
- `scripts/batch_pipeline.py`: Tự động định tuyến các bài giảng sang động cơ Cinematic Spatial Keynote, tự động render 1080p slide previews và đồng bộ đồng thời vào cả `Du_An_Outputs/` và `Du An/A Tuan Dan So/`.
