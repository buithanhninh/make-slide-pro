# QUY TẮC MẶC ĐỊNH BẮT BUỘC: MAKE SLIDE PRO V9.3 (CANONICAL OFFICIAL ENTERPRISE RELEASE)

> **CHỈ THỊ TỐI CAO TỪ NGƯỜI DÙNG (PERMANENT SYSTEM INVARIANT):**
> 1. **Phiên bản Make Slide Pro V9.3 là phiên bản CHÍNH THỨC, CUỐI CÙNG và DUY NHẤT** được đưa vào sử dụng cho toàn bộ dự án.
> 2. **Trong BẤT KỲ cuộc trò chuyện nào (kể cả phiên trò chuyện mới hoàn toàn)**: Khi người dùng yêu cầu tạo slide, chuyển đổi tài liệu, thẩm định hoặc xuất bản bài thuyết trình mà KHÔNG nói rõ phiên bản, hệ thống **BẮT BUỘC MẶC ĐỊNH** sử dụng phiên bản Make Slide Pro V9.3.
> 3. **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** sử dụng các phiên bản cũ hơn (như v7.x, v8.2, v8.3, v8.5, v8.6, v9.0) hoặc bất kỳ phiên bản nào khác, TRỪ KHI người dùng có yêu cầu đích danh chỉ định dùng phiên bản khác.
> 4. Quy tắc này có hiệu lực vĩnh viễn, xuyên suốt mọi phiên làm việc và không được phép bị ghi đè hay suy giảm.

---

## 1. TIÊU CHUẨN KỸ THUẬT BẮT BUỘC CỦA V9.3 (KMCA V9.3)

1. **Kiến Trúc Chuyển Tiếp Kinetic Morph Liền Mạch (Kinetic Morph Continuity Architecture - KMCA V9.3)**:
   - **100% Pure Continuous Morph By Word** (`ppEffectMorphByWord` = 3955, Duration = 0.85s) trên toàn bộ slide nội dung (Slide 2 đến N-1).
   - **Khế Ước Cầu Nối Morph (Morph Bridge Contract)**:
     - Thẻ mở đầu (Hero Card 0 / `!!Kinetic_Card_1!!`) hiện diện trực tiếp trên slide canvas và tham gia trọn vẹn vào chuyển tiếp slide (0.85s Morph).
     - **Tuyệt đối KHÔNG gán hiệu ứng intra-slide animation trong `TimeLine.MainSequence` cho Card 0** nhằm chống hiện tượng PowerPoint tự động ẩn shape và hủy bỏ Morph.
   - **Khế Ước Định Danh Toàn Diện (Universal `!!Kinetic_Card_N!!` Contract)**:
     - 100% slide nội dung phải tuân thủ chuẩn định danh Selection Pane:
       - Header: `!!Anchor_Assertion_Title!!`, `!!Anchor_Kicker_Rail!!`, `!!Anchor_Slide_Tracker!!`
       - Footer: `!!Anchor_Source_Footer!!`
       - Thẻ nội dung: `!!Kinetic_Card_1!!`, `!!Kinetic_Card_2!!`, `!!Kinetic_Card_3!!`, `!!Kinetic_Card_4!!`...
   - **Chuyển tiếp Cinematic Smooth Fade** (`ppTransitionFadeSmoothly` = 3849, 0.65s) chỉ áp dụng riêng cho Slide Bìa (Slide 1) và Slide Kết Luận (Slide N).

2. **Kiểm Soát Nhịp Trình Chiếu Chuẩn Sư Phạm (Presenter Pacing Sequencing)**:
   - Sử dụng `safe_group` nhóm toàn bộ các thành phần của từng thẻ thành 1 Shape nguyên khối duy nhất trước khi gán animation.
   - Thẻ mở đầu (Card 0) xuất hiện cùng slide qua Morph (chống lỗi màn hình trống); các thẻ bổ trợ tiếp theo (Cards 1..N) mở lần lượt qua từng click chuột (`OnPageClick`, trigger = 1).
   - Khóa cứng trần số lượng click chuột ($\le 4$ clicks/slide), triệt tiêu 100% lỗi runaway clicks.

3. **Kho Thư Viện Mega 165+ Archetypes**:
   - Toàn diện 6 phân hệ cốt lõi: Tables (25), Frameworks (35), Processes (30), Architectures (25), Charts (20), Containers (30).
   - 100% Native Editable: PowerPoint Tables & Microsoft Office Native Charts (nhúng Excel Worksheet thật).

4. **Tự Động Chuẩn Hóa Biểu Đồ Tương Phản Cao (Auto-Themed High-Contrast Charts)**:
   - Tự động áp dụng font chữ màu sáng (#E2E8F0) cho ChartArea, Axes(1), Axes(2) và Legend trên nền Dark Obsidian.
   - Loại bỏ viền và nền xám mặc định của Excel (Fill.Visible = msoFalse, Line.Visible = msoFalse).

5. **Cổng Thẩm Định Pháp Y Sâu Đa Tầng (`audit_deck_deep_v92.py` & MAS-CLSH V9.3)**:
   - Tự động quét 100% slide sau khi xuất bản:
     - Phạt lỗi nếu phát hiện Card 0 bị gán animation chặn Morph.
     - Xác nhận tỷ lệ hiện diện của `!!Kinetic_Card_1!!` và các ray cố định.
     - Quét sạch 100% chuỗi IT mock/slop (SLA 99%, 165+ mẫu, Morph 0.85s...).
     - Đảm bảo 100% slide đạt PASS (0 lỗi P0, 0 lỗi P1).

