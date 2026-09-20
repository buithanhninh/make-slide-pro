# QUY TẮC MẶC ĐỊNH BẮT BUỘC: MAKE SLIDE PRO V8.6.0 (CANONICAL OFFICIAL RELEASE)

> **CHỈ THỊ TỐI CAO TỪ NGƯỜI DÙNG (PERMANENT SYSTEM INVARIANT):**
> 1. **Phiên bản Make Slide Pro V8.6.0 là phiên bản CHÍNH THỨC, CUỐI CÙNG và DUY NHẤT** được đưa vào sử dụng cho toàn bộ dự án.
> 2. **Trong BẤT KỲ cuộc trò chuyện nào (kể cả phiên trò chuyện mới hoàn toàn)**: Khi người dùng yêu cầu tạo slide, chuyển đổi tài liệu, thẩm định hoặc xuất bản bài thuyết trình mà KHÔNG nói rõ phiên bản, hệ thống **BẮT BUỘC MẶC ĐỊNH** sử dụng phiên bản Make Slide Pro V8.6.0.
> 3. **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** sử dụng các phiên bản cũ hơn (như v7.x, v8.2, v8.3, v8.5) hoặc bất kỳ phiên bản nào khác, TRỪ KHI người dùng có yêu cầu đích danh chỉ định dùng phiên bản khác.
> 4. Quy tắc này có hiệu lực vĩnh viễn, xuyên suốt mọi phiên làm việc và không được phép bị ghi đè hay suy giảm.

---

## 1. TIÊU CHUẨN KỸ THUẬT BẮT BUỘC CỦA V8.6.0

1. **Kho Thư Viện Mega 165+ Archetypes**:
   - Toàn diện 6 phân hệ cốt lõi: Tables (25), Frameworks (35), Processes (30), Architectures (25), Charts (20), Containers (30).
   - 100% Native Editable: PowerPoint Tables & Microsoft Office Native Charts (nhúng Excel Worksheet thật, người dùng có thể nhấp phải chuột chỉnh sửa dữ liệu).

2. **Chuyển Động Apple Keynote 100% Continuous Morph**:
   - **100% Pure Continuous Morph** (ppEffectMorphByObject = 3954, Duration = 0.85s) trên toàn bộ slide nội dung (Slide 2 đến N-1).
   - Chỉ sử dụng Cinematic Smooth Fade (ppTransitionFadeSmoothly = 3849, 0.65s) tại Slide Bìa (Slide 1) và Slide Kết Luận (Slide N).
   - Tuyệt đối cấm sử dụng các hiệu ứng gây rối mắt, giật cục như Push Left, Push Up, Reveal hay Wipe giữa các slide nội dung.

3. **Kiểm Soát Nhịp Trình Chiếu Nguyên Khối (Atomic Card Presenter Sequencing)**:
   - Sử dụng safe_group từ scripts.component_library.utils để nhóm toàn bộ các thành phần của một thẻ thành 1 Shape nguyên khối duy nhất trước khi gán animation.
   - Mỗi click chuột (msoAnimTriggerOnPageClick) mở ra trọn vẹn 1 thẻ (Khung + Huy hiệu + Tiêu đề + Phân cách + Nội dung + Chip KPI).
   - Tuyệt đối không để xảy ra hiện tượng click hiện khung rỗng hoặc chữ bay rời rạc.
   - Giữ cố định ray tiêu đề (ssertion_title, kicker) để Morph giữa các slide không bị giật/nhấp nháy.

4. **Triệt Tiêu 100% Khoảng Trống Thừa (Zero Dead Space) & Tỷ Lệ Vàng**:
   - Định cỡ chiều cao thẻ theo kích thước tự nhiên (250–300pt), căn giữa trục Y (cy).
   - Phân tầng thông tin dày dặn, giàu giá trị: Header Pill -> Tiêu đề in đậm -> Đường kẻ phân cách -> Nội dung phân điểm -> Chip trạng thái / KPI thực chứng.
   - Luôn sử dụng Vector Connectors native (dd_vector_connector) với mũi tên tam giác cho các sơ đồ quy trình và kiến trúc (DevSecOps, CPM, Medallion, RAG).

5. **Tự Động Chuẩn Hóa Biểu Đồ Tương Phản Cao (Auto-Themed High-Contrast Charts)**:
   - Tự động áp dụng font chữ màu sáng (#E2E8F0) cho ChartArea, Axes(1), Axes(2) và Legend trên nền tối, không để chữ đen chìm vào nền Dark Canvas.
   - Loại bỏ viền và nền xám mặc định của Excel (Fill.Visible = msoFalse, Line.Visible = msoFalse).

6. **Hội Đồng Thẩm Định Pháp Y 16-Agent (MACC-QA)**:
   - Đảm bảo chất lượng qua 5 Cổng thẩm định khắt khe trước khi xuất bản.
