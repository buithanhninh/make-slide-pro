"""
frameworks_engine.py
Exhaustive Strategic Frameworks Engine for Make Slide Pro V8.5.0.
Generates 25 classic management consulting, business strategy, and intellectual models
using 100% Microsoft PowerPoint Native Vector Shapes.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

# Win32 Constants
msoShapeRectangle = 1
msoShapeTrapezoid = 3
msoShapeRoundedRectangle = 5
msoShapeIsoscelesTriangle = 7
msoShapeOval = 9
msoShapeDiamond = 4
msoShapeHexagon = 10
msoShapeRightArrow = 13
msoShapeDownArrow = 16
msoShapeLeftArrow = 14
msoShapeUpArrow = 15
msoShapeLeftRightArrow = 17
msoShapeChevron = 55
msoShapeFlowchartProcess = 61
msoShapeCurvedRightArrow = 102
msoShapeDonut = 18
msoShapeBevel = 84
msoTextOrientationHorizontal = 1
ppAlignLeft = 1
ppAlignCenter = 2
ppAlignRight = 3
msoTrue = -1
msoFalse = 0


def hex_to_bgr(hex_color: str) -> int:
    hex_clean = hex_color.lstrip("#")
    if len(hex_clean) != 6:
        return 0
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return (b << 16) | (g << 8) | r


class StrategicFrameworksEngine:
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}

    def _get_token(self, category: str, key: str, fallback: str) -> str:
        return self.tokens.get(category, {}).get(key, fallback)

    # 1. FRAMEWORK_MATRIX_2X2 (Ma Trận 2x2)
    def render_matrix_2x2(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("matrix_data", {})
        axis_x = data.get("axis_x", "Mức Độ Khả Thi Kỹ Thuật →")
        axis_y = data.get("axis_y", "Giá Trị Tác Động Chiến Lược →")
        quadrants = data.get("quadrants", [
            {"title": "ĐỔI MỚI ĐỘT PHÁ (STRATEGIC BETS)", "desc": "Tác động rất lớn, cần đầu tư R&D sâu về thuật toán AI.", "highlight": False},
            {"title": "ƯU TIÊN HÀNG ĐẦU (QUICK WINS)", "desc": "Khả thi cao, tác động tức thì. Tập trung toàn lực thực thi.", "highlight": True},
            {"title": "CÂN NHẮC LOẠI BỎ (TIME SINKS)", "desc": "Khả thi thấp, giá trị thấp. Cắt giảm để tối ưu ngân sách.", "highlight": False},
            {"title": "DUY TRÌ NỀN TẢNG (FILL-INS)", "desc": "Khả thi cao, tác động trung bình. Thực hiện theo tiến độ chuẩn.", "highlight": False}
        ])

        gap = 14.0
        qw = (width - gap) / 2.0
        qh = (height - gap - 26.0) / 2.0
        matrix_top = top

        coords = [
            (left, matrix_top),
            (left + qw + gap, matrix_top),
            (left, matrix_top + qh + gap),
            (left + qw + gap, matrix_top + qh + gap)
        ]

        for i, q in enumerate(quadrants[:4]):
            qx, qy = coords[i]
            is_hl = q.get("highlight", (i == 1))
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, qx, qy, qw, qh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(brand if (is_hl and self.theme == "DARK") else (surface if not is_hl else "#E0F2FE"))
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if is_hl else border)
            card.Line.Weight = 2.0 if is_hl else 1.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, qx + 16, qy + 14, qw - 32, qh - 28)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = q.get("title", f"PHÂN VÙNG 0{i+1}") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 13
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if (is_hl and self.theme == "DARK") else (brand if is_hl else ink))
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = q.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0" if (is_hl and self.theme == "DARK") else muted)
            shapes.append(tb)

        ax_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left, matrix_top + 2 * qh + gap + 4.0, width, 20)
        at = ax_tb.TextFrame.TextRange
        at.Text = axis_x
        at.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        at.Font.Size = 10
        at.Font.Bold = msoTrue
        at.Font.Color.RGB = hex_to_bgr(brand)
        at.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(ax_tb)

        return shapes

    # 2. FRAMEWORK_MATRIX_3X3 (Ma Trận GE-McKinsey 9 Ô)
    def render_matrix_3x3(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("matrix_3x3", [
            {"title": "Đầu Tư Tăng Tốc", "tag": "ƯU TIÊN 1"}, {"title": "Đầu Tư Chọn Lọc", "tag": "ƯU TIÊN 2"}, {"title": "Bảo Vệ Thị Phần", "tag": "DUY TRÌ"},
            {"title": "Đầu Tư Chọn Lọc", "tag": "ƯU TIÊN 2"}, {"title": "Duy Trì Thu Hoạch", "tag": "DUY TRÌ"}, {"title": "Thu Hẹp Có Kiểm Soát", "tag": "RÚT LUI"},
            {"title": "Bảo Vệ Thị Phần", "tag": "DUY TRÌ"}, {"title": "Thu Hẹp Có Kiểm Soát", "tag": "RÚT LUI"}, {"title": "Thoái Vốn Hoàn Toàn", "tag": "LOẠI BỎ"}
        ])

        gap = 10.0
        cols, rows = 3, 3
        cell_w = (width - gap * (cols - 1)) / cols
        cell_h = (height - gap * (rows - 1)) / rows

        COLORS = {
            "ƯU TIÊN 1": ("#065F46", "#10B981"), "ƯU TIÊN 2": ("#0369A1", "#38BDF8"),
            "DUY TRÌ": ("#1E293B", "#CBD5E1"), "RÚT LUI": ("#78350F", "#F59E0B"), "LOẠI BỎ": ("#7F1D1D", "#EF4444")
        }

        for idx, item in enumerate(data[:9]):
            r = idx // cols
            c = idx % cols
            cx = left + c * (cell_w + gap)
            cy = top + r * (cell_h + gap)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy, cell_w, cell_h)
            card.Fill.Solid()
            tag = item.get("tag", "DUY TRÌ")
            bg_c, fg_c = COLORS.get(tag, ("#1E293B", "#CBD5E1"))
            card.Fill.ForeColor.RGB = hex_to_bgr(bg_c if self.theme == "DARK" else "#F1F5F9")
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(fg_c)
            card.Line.Weight = 1.5
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 10, cy + (cell_h / 2.0) - 22, cell_w - 20, 44)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = item["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"[{tag}]"
            p2.Font.Size = 10
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(fg_c)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 3. FRAMEWORK_PORTER_5_FORCES (Mô Hình 5 Áp Lực Cạnh Tranh)
    def render_porter_5_forces(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        forces = spec.get("forces", {
            "center": "1. MỨC ĐỘ CẠNH TRANH TRONG NGÀNH\n(Áp lực cạnh tranh gay gắt từ các doanh nghiệp lớn)",
            "top": "2. NGUY CƠ TỪ ĐỐI THỦ MỚI\n(Rào cản gia nhập thấp, xuất hiện công nghệ thay thế)",
            "bottom": "3. ĐE DỌA TỪ SẢN PHẨM THAY THẾ\n(AI Agent tự động thay thế các công cụ thủ công)",
            "left": "4. QUYỀN THƯƠNG LƯỢNG NHÀ CUNG CẤP\n(Phụ thuộc hạ tầng chip và GPU cao cấp)",
            "right": "5. QUYỀN THƯƠNG LƯỢNG KHÁCH HÀNG\n(Khách hàng đòi hỏi chuẩn mực cao và giá linh hoạt)"
        })

        box_w = width * 0.32
        box_h = height * 0.28
        center_x = left + (width - box_w) / 2.0
        center_y = top + (height - box_h) / 2.0

        # Center Box
        c_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, center_x, center_y, box_w, box_h)
        c_box.Fill.Solid()
        c_box.Fill.ForeColor.RGB = hex_to_bgr(brand)
        c_box.Line.Visible = msoFalse
        shapes.append(c_box)
        ct = c_box.TextFrame.TextRange
        ct.Text = forces["center"]
        ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ct.Font.Size = 11
        ct.Font.Bold = msoTrue
        ct.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        c_box.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        # 4 Surrounding Satellite Boxes
        coords = [
            (center_x, top, forces["top"]),                                     # Top
            (center_x, top + height - box_h, forces["bottom"]),                # Bottom
            (left, center_y, forces["left"]),                                   # Left
            (left + width - box_w, center_y, forces["right"])                   # Right
        ]

        for bx, by, text in coords:
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, bx, by, box_w, box_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(card)

            bt = card.TextFrame.TextRange
            bt.Text = text
            bt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bt.Font.Size = 10.5
            bt.Font.Color.RGB = hex_to_bgr(ink)
            card.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 4. FRAMEWORK_VALUE_CHAIN (Chuỗi Giá Trị Michael Porter)
    def render_value_chain(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        support_items = spec.get("support_activities", [
            "1. Cơ sở hạ tầng tổ chức & Quản trị rủi ro",
            "2. Quản trị và phát triển nguồn nhân lực chất lượng cao",
            "3. R&D công nghệ và hệ sinh thái đổi mới số"
        ])
        primary_items = spec.get("primary_activities", [
            "Hậu Cần Nhập", "Vận Hành", "Hậu Cần Xuất", "Marketing & Bán Hàng", "Dịch Vụ Hỗ Trợ"
        ])

        margin_w = 70.0
        main_w = width - margin_w - 10.0
        top_h = height * 0.42
        bottom_h = height * 0.52
        gap_y = height * 0.06

        sub_h = (top_h - 10.0) / len(support_items)
        for i, s_text in enumerate(support_items):
            sy = top + i * (sub_h + 5.0)
            strip = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, sy, main_w, sub_h)
            strip.Fill.Solid()
            strip.Fill.ForeColor.RGB = hex_to_bgr(surface)
            strip.Line.Visible = msoTrue
            strip.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(strip)

            st = strip.TextFrame.TextRange
            st.Text = f"  {s_text}"
            st.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            st.Font.Size = 10.5
            st.Font.Bold = msoTrue
            st.Font.Color.RGB = hex_to_bgr(ink)
            strip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignLeft

        by = top + top_h + gap_y
        prim_n = len(primary_items)
        prim_w = main_w / prim_n
        for j, p_text in enumerate(primary_items):
            px = left + j * prim_w
            chev = slide.Shapes.AddShape(msoShapeChevron, px, by, prim_w + 4, bottom_h)
            chev.Fill.Solid()
            chev.Fill.ForeColor.RGB = hex_to_bgr(brand if j % 2 == 1 else ("#0369A1" if self.theme == "DARK" else "#0D9488"))
            chev.Line.Visible = msoFalse
            shapes.append(chev)

            pt = chev.TextFrame.TextRange
            pt.Text = p_text
            pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            pt.Font.Size = 10.5
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            chev.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        margin_shape = slide.Shapes.AddShape(msoShapeRightArrow, left + main_w + 10, top, margin_w, height)
        margin_shape.Fill.Solid()
        margin_shape.Fill.ForeColor.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#059669")
        margin_shape.Line.Visible = msoFalse
        shapes.append(margin_shape)

        mt = margin_shape.TextFrame.TextRange
        mt.Text = "BIÊN\nLỢI\nNHUẬN\n(MARGIN)"
        mt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        mt.Font.Size = 10
        mt.Font.Bold = msoTrue
        mt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        margin_shape.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 5. FRAMEWORK_SWOT_ANALYSIS (Ma Trận SWOT 4 Ô Lớn)
    def render_swot_analysis(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        swot_data = spec.get("swot", [
            {"letter": "S", "title": "ĐIỂM MẠNH (STRENGTHS)", "items": ["Hệ thống 16 tác tử MACC tự phục hồi", "Kho 110+ Archetypes chuẩn quốc tế", "100% Native Object sửa trong Excel"], "color": "#10B981"},
            {"letter": "W", "title": "ĐIỂM YẾU (WEAKNESSES)", "items": ["Cần cài đặt bộ Office cục bộ trên Windows", "Phụ thuộc tài liệu đầu vào có cấu trúc", "Cần tối ưu thời gian khởi động COM"], "color": "#EF4444"},
            {"letter": "O", "title": "CƠ HỘI (OPPORTUNITIES)", "items": ["Mở rộng cung cấp dịch vụ Web SaaS toàn quốc", "Tích hợp công nghệ Generative AI đa phương thức", "Chuyển giao cho các trường đại học"], "color": "#0284C7"},
            {"letter": "T", "title": "THÁCH THỨC (THREATS)", "items": ["Cạnh tranh từ các nền tảng thiết kế toàn cầu", "Thay đổi chính sách cập nhật của Microsoft", "Đòi hỏi bảo mật dữ liệu PII nghiêm ngặt"], "color": "#F59E0B"}
        ])

        gap = 14.0
        qw = (width - gap) / 2.0
        qh = (height - gap) / 2.0
        coords = [(left, top), (left + qw + gap, top), (left, top + qh + gap), (left + qw + gap, top + qh + gap)]

        for idx, (item, (cx, cy)) in enumerate(zip(swot_data[:4], coords)):
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy, qw, qh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(item["color"])
            card.Line.Weight = 2.0
            shapes.append(card)

            # Giant Letter Badge (S, W, O, T)
            badge = slide.Shapes.AddShape(msoShapeOval, cx + 16, cy + 14, 38, 38)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr(item["color"])
            badge.Line.Visible = msoFalse
            shapes.append(badge)
            bt = badge.TextFrame.TextRange
            bt.Text = item["letter"]
            bt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            bt.Font.Size = 18
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 62, cy + 14, qw - 76, qh - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = item["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 13
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(item["color"])
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = "\n".join([f"• {x}" for x in item.get("items", [])])
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # 6. FRAMEWORK_PESTEL_HEX (Mô Hình PESTEL 6 Lục Giác)
    def render_pestel_hex(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        pestel = spec.get("pestel_data", [
            {"code": "P", "name": "Chính Trị (Political)", "desc": "Chính sách dân số & quy hoạch quốc gia"},
            {"code": "E", "name": "Kinh Tế (Economic)", "desc": "Tăng trưởng GDP & mức thu nhập bình quân"},
            {"code": "S", "name": "Xã Hội (Social)", "desc": "Tỷ suất sinh thấp & già hóa nhanh"},
            {"code": "T", "name": "Công Nghệ (Tech)", "desc": "Chuyển đổi số & ứng dụng AI dự báo"},
            {"code": "E", "name": "Môi Trường (Environ)", "desc": "Tác động biến đổi khí hậu & nguồn nước"},
            {"code": "L", "name": "Pháp Lý (Legal)", "desc": "Nghị định bảo vệ dữ liệu & luật dân số"}
        ])

        cols = 3
        rows = 2
        gap = 12.0
        hw = (width - gap * (cols - 1)) / cols
        hh = (height - gap * (rows - 1)) / rows
        COLORS = ["#0284C7", "#0D9488", "#10B981", "#38BDF8", "#F59E0B", "#8B5CF6"]

        for idx, item in enumerate(pestel[:6]):
            r = idx // cols
            c = idx % cols
            hx = left + c * (hw + gap)
            hy = top + r * (hh + gap)

            card = slide.Shapes.AddShape(msoShapeHexagon, hx, hy, hw, hh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(COLORS[idx % len(COLORS)])
            card.Line.Weight = 2.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, hx + 18, hy + (hh / 2.0) - 26, hw - 36, 52)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"[{item['code']}] {item['name']}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(COLORS[idx % len(COLORS)])
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = item.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 7. FRAMEWORK_BALANCED_SCORECARD (Thẻ Điểm Cân Bằng BSC)
    def render_balanced_scorecard(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        bsc = spec.get("bsc_perspectives", [
            {"title": "1. Khía Cạnh Tài Chính", "goals": ["Tăng trưởng doanh thu 30%", "Tối ưu hóa chi phí vận hành 25%"], "color": "#10B981"},
            {"title": "2. Khía Cạnh Khách Hàng", "goals": ["Chỉ số hài lòng CSAT > 95%", "Tỷ lệ giữ chân khách hàng 92%"], "color": "#0284C7"},
            {"title": "3. Khía Cạnh Quy Trình Nội Bộ", "goals": ["Tự động hóa 100% kiểm định slide", "Giảm thời gian xuất bản xuống 25s"], "color": "#8B5CF6"},
            {"title": "4. Học Tập & Phát Triển", "goals": ["100% nhân sự làm chủ công nghệ AI", "Phát triển văn hóa đổi mới liên tục"], "color": "#F59E0B"}
        ])

        gap = 14.0
        bw = (width - gap) / 2.0
        bh = (height - gap) / 2.0
        coords = [(left, top), (left + bw + gap, top), (left, top + bh + gap), (left + bw + gap, top + bh + gap)]

        for idx, (item, (bx, by)) in enumerate(zip(bsc[:4], coords)):
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, bx, by, bw, bh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(item["color"])
            card.Line.Weight = 2.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, bx + 16, by + 14, bw - 32, bh - 28)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = item["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 13
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(item["color"])
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = "\n".join([f"• {g}" for g in item.get("goals", [])])
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # 8. FRAMEWORK_STRATEGY_HOUSE (Ngôi Nhà Chiến Lược)
    def render_strategy_house(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("house_data", {})
        roof_title = data.get("roof", "TẦM NHÌN 2030: HỆ SINH THÁI TỰ ĐỘNG HÓA THUYẾT TRÌNH THÔNG MINH SỐ 1")
        pillars = data.get("pillars", [
            {"title": "Trụ Cột 1: Công Nghệ Lõi", "desc": "Kiến trúc 16 tác tử MACC & Native COM trực tiếp."},
            {"title": "Trụ Cột 2: Trải Nghiệm Đỉnh Cao", "desc": "110+ Archetypes quốc tế, hiệu ứng chuyển động mượt mà."},
            {"title": "Trụ Cột 3: Khả Năng Tùy Biến", "desc": "Tất cả thành phần đều là Native Object sửa 100% trong Excel."}
        ])
        foundation = data.get("foundation", "NỀN MÓNG CỐT LÕI: DỮ LIỆU ĐÁNG TIN CẬY - BẢO MẬT ZERO-TRUST - SỰ CHỈN CHU TUYỆT ĐỐI")

        roof_h = 50.0
        found_h = 45.0
        pillar_gap = 14.0
        pillar_h = height - roof_h - found_h - (pillar_gap * 2)

        # 1. Roof
        roof = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, roof_h)
        roof.Fill.Solid()
        roof.Fill.ForeColor.RGB = hex_to_bgr(brand)
        roof.Line.Visible = msoFalse
        shapes.append(roof)

        rt = roof.TextFrame.TextRange
        rt.Text = roof_title
        rt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        rt.Font.Size = 13
        rt.Font.Bold = msoTrue
        rt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        roof.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        # 2. Pillars
        p_count = len(pillars)
        pw = (width - (pillar_gap * (p_count - 1))) / p_count
        py = top + roof_h + pillar_gap

        for idx, pil in enumerate(pillars):
            px = left + idx * (pw + pillar_gap)
            p_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, py, pw, pillar_h)
            p_card.Fill.Solid()
            p_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            p_card.Line.Visible = msoTrue
            p_card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            p_card.Line.Weight = 1.5 if idx == 0 else 1.0
            shapes.append(p_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 14, py + 16, pw - 28, pillar_h - 32)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = pil["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 13
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else ink)
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = pil["desc"]
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11.5
            p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            shapes.append(tb)

        # 3. Foundation
        fy = top + height - found_h
        found = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, fy, width, found_h)
        found.Fill.Solid()
        found.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
        found.Line.Visible = msoFalse
        shapes.append(found)

        ft = found.TextFrame.TextRange
        ft.Text = foundation
        ft.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ft.Font.Size = 11
        ft.Font.Bold = msoTrue
        ft.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
        found.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 9. FRAMEWORK_PYRAMID_ASCENDING (Tháp Phân Cấp Chiến Lược)
    def render_pyramid_ascending(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        layers = spec.get("pyramid_layers", [
            {"tier": "ĐỈNH CAO", "title": "Tự Động Hóa Trí Tuệ Nhân Tạo (Autonomous AI)", "desc": "Hệ thống tự thích ứng và ra quyết định thời gian thực"},
            {"tier": "TẦNG 3", "title": "Phân Tích Dự Báo Nâng Cao (Predictive Insights)", "desc": "Mô hình toán học và thuật toán học máy chuyên sâu"},
            {"tier": "TẦNG 2", "title": "Kho Dữ Liệu Tập Trung (Single Source of Truth)", "desc": "Chuẩn hóa dữ liệu lớn và kiến trúc Data Lakehouse"},
            {"tier": "NỀN TẢNG", "title": "Hạ Tầng Điện Toán Đám Mây & An Ninh Mạng", "desc": "Nền tảng hạ tầng bảo mật Zero-Trust và độ sẵn sàng cao"}
        ])

        n = len(layers)
        layer_h = (height - (8.0 * (n - 1))) / n
        pyr_w = width * 0.45
        detail_w = width * 0.51
        detail_left = left + pyr_w + (width * 0.04)

        COLORS = ["#0284C7", "#0369A1", "#0D9488", "#1E293B"] if self.theme == "DARK" else ["#0284C7", "#0D9488", "#10B981", "#E2E8F0"]

        for i, l_data in enumerate(layers):
            ly = top + i * (layer_h + 8.0)
            w_cur = pyr_w * (0.45 + (i * (0.55 / max(1, n - 1))))
            lx = left + (pyr_w - w_cur) / 2.0

            shape = slide.Shapes.AddShape(msoShapeRoundedRectangle, lx, ly, w_cur, layer_h)
            shape.Fill.Solid()
            shape.Fill.ForeColor.RGB = hex_to_bgr(COLORS[i % len(COLORS)])
            shape.Line.Visible = msoFalse
            shapes.append(shape)

            st = shape.TextFrame.TextRange
            st.Text = l_data["tier"]
            st.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            st.Font.Size = 11
            st.Font.Bold = msoTrue
            st.Font.Color.RGB = hex_to_bgr("#FFFFFF" if i < 3 or self.theme == "DARK" else "#0F172A")
            shape.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, detail_left, ly, detail_w, layer_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "card_border", "#1E293B"))
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, detail_left + 14, ly + 6, detail_w - 28, layer_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = l_data["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if i == 0 else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = l_data["desc"]
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            shapes.append(tb)

        return shapes

    # 10. FRAMEWORK_INVERTED_PYRAMID (Tháp Ngược Ưu Tiên)
    def render_inverted_pyramid(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        # Reverse of ascending pyramid
        rev_spec = dict(spec)
        rev_spec["pyramid_layers"] = list(reversed(spec.get("pyramid_layers", [
            {"tier": "DIỆN RỘNG (100%)", "title": "Nhận Diện Dân Cư & Khảo Sát Cơ Bản", "desc": "Bao phủ toàn bộ đối tượng điều tra"},
            {"tier": "CHỌN LỌC (40%)", "title": "Sàng Lọc & Phân Tích Chuyên Sâu", "desc": "Tập trung nhóm mẫu nghiên cứu trọng điểm"},
            {"tier": "TINH HOA (10%)", "title": "Chính Sách & Giải Pháp Đột Phá", "desc": "Tác động vào nhóm mắt xích then chốt"}
        ])))
        return self.render_pyramid_ascending(slide, rev_spec, left, top, width, height)

    # 11. FRAMEWORK_CONVERSION_FUNNEL (Phễu Chuyển Đổi)
    def render_conversion_funnel(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        funnel_data = spec.get("funnel_data", [
            {"stage": "TIẾP CẬN TÀI LIỆU", "metric": "500,000+", "rate": "100%", "desc": "Nguồn tài liệu học tập và báo cáo nghiên cứu nhập môn"},
            {"stage": "BÓC TÁCH NỘI DUNG", "metric": "120,000", "rate": "24.0%", "desc": "Trích xuất cấu trúc ngữ nghĩa và bảng số liệu thực chứng"},
            {"stage": "TẠO BLUEPRINT BÀI HỌC", "metric": "24,000", "rate": "4.8%", "desc": "Tự động phân bổ archetype và bố cục thị giác tối ưu"},
            {"stage": "XUẤT BẢN SLIDE NATIVE", "metric": "5,000", "rate": "1.0%", "desc": "Sinh file PPTX hoàn chỉnh chất lượng giám đốc điều hành"}
        ])

        n = len(funnel_data)
        stage_h = (height - (8.0 * (n - 1))) / n
        funnel_w = width * 0.48
        detail_w = width * 0.48
        detail_left = left + funnel_w + (width * 0.04)

        COLORS = ["#0284C7", "#0369A1", "#075985", "#0C4A6E"] if self.theme == "DARK" else ["#0284C7", "#0D9488", "#10B981", "#059669"]

        for i, item in enumerate(funnel_data):
            cur_top = top + i * (stage_h + 8.0)
            taper_factor = 1.0 - (i * 0.14)
            w_cur = funnel_w * taper_factor
            x_cur = left + (funnel_w - w_cur) / 2.0

            bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, x_cur, cur_top, w_cur, stage_h)
            bar.Fill.Solid()
            bar.Fill.ForeColor.RGB = hex_to_bgr(COLORS[i % len(COLORS)])
            bar.Line.Visible = msoFalse
            shapes.append(bar)

            bt = bar.TextFrame.TextRange
            bt.Text = f"{item['stage']} | {item['metric']}"
            bt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bt.Font.Size = 10.5
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            bar.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, detail_left, cur_top, detail_w, stage_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "card_border", "#1E293B"))
            shapes.append(card)

            ctb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, detail_left + 12, cur_top + 4, detail_w - 24, stage_h - 8)
            ctf = ctb.TextFrame
            ctf.WordWrap = msoTrue
            p1 = ctf.TextRange.Paragraphs(1)
            p1.Text = f"Tỷ lệ: {item['rate']} - {item['desc']}"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Color.RGB = hex_to_bgr(ink)
            shapes.append(ctb)

        return shapes

    # 12. FRAMEWORK_GROWTH_FLYWHEEL (Vòng Quay Tăng Trưởng)
    def render_growth_flywheel(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        nodes = spec.get("flywheel_nodes", [
            {"title": "1. Trải Nghiệm Khách Hàng", "desc": "Sản phẩm tối ưu tạo sự hài lòng cao"},
            {"title": "2. Gia Tăng Lưu Lượng", "desc": "Lan tỏa tự nhiên & tỷ lệ quay lại cao"},
            {"title": "3. Mở Rộng Đối Tác", "desc": "Hệ sinh thái nhà cung cấp phong phú"},
            {"title": "4. Tối Ưu Chi Phí Quy Mô", "desc": "Giảm đơn giá và tái đầu tư vào công nghệ"}
        ])

        center_x = left + width / 2.0
        center_y = top + height / 2.0
        core_r = 55.0

        core = slide.Shapes.AddShape(msoShapeOval, center_x - core_r, center_y - core_r, core_r * 2, core_r * 2)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Visible = msoFalse
        shapes.append(core)

        ct = core.TextFrame.TextRange
        ct.Text = "LÕI ĐỘNG LỰC\nTĂNG TRƯỞNG"
        ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ct.Font.Size = 10
        ct.Font.Bold = msoTrue
        ct.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        core.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        card_w = (width - 150.0) / 2.0
        card_h = (height - 130.0) / 2.0
        positions = [
            (left, top),
            (left + width - card_w, top),
            (left + width - card_w, top + height - card_h),
            (left, top + height - card_h)
        ]

        for i, (n_data, (cx, cy)) in enumerate(zip(nodes[:4], positions)):
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if i == 0 else border)
            card.Line.Weight = 1.5 if i == 0 else 1.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 12, cy + 10, card_w - 24, card_h - 20)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = n_data["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if i == 0 else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = n_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            shapes.append(tb)

        return shapes

    # 13. FRAMEWORK_HUB_SPOKE (Hệ Sinh Thái Trọng Tâm & Vệ Tinh)
    def render_hub_spoke(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("hub_data", {})
        hub_title = data.get("hub", "NỀN TẢNG DỮ LIỆU\nTRUNG TÂM (CORE)")
        spokes = data.get("spokes", [
            {"title": "Cổng Dịch Vụ Công Trực Tuyến", "desc": "Giao diện công dân"},
            {"title": "Hệ Thống Phân Tích BI & Thống Kê", "desc": "Báo cáo điều hành"},
            {"title": "Cơ Sở Dữ Liệu Dân Cư Quốc Gia", "desc": "Định danh điện tử"},
            {"title": "Mạng Lưới Y Tế & An Sinh Xã Hội", "desc": "Liên thông liên ngành"}
        ])

        hub_w, hub_h = 160.0, 90.0
        hub_x = left + (width - hub_w) / 2.0
        hub_y = top + (height - hub_h) / 2.0

        hub = slide.Shapes.AddShape(msoShapeRoundedRectangle, hub_x, hub_y, hub_w, hub_h)
        hub.Fill.Solid()
        hub.Fill.ForeColor.RGB = hex_to_bgr(brand)
        hub.Line.Visible = msoFalse
        shapes.append(hub)

        ht = hub.TextFrame.TextRange
        ht.Text = hub_title
        ht.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ht.Font.Size = 11
        ht.Font.Bold = msoTrue
        ht.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        hub.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        sw = (width - hub_w - 80.0) / 2.0
        sh = (height - 30.0) / 2.0
        spoke_pos = [
            (left, top), (left + width - sw, top),
            (left, top + sh + 30.0), (left + width - sw, top + sh + 30.0)
        ]

        for idx, (sp_item, (sx, sy)) in enumerate(zip(spokes[:4], spoke_pos)):
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, sy, sw, sh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 12, sy + 12, sw - 24, sh - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = sp_item["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = sp_item.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            shapes.append(tb)

        return shapes

    # 14. FRAMEWORK_CONCENTRIC_RINGS (Vòng Tròn Đồng Tâm / Onion)
    def render_concentric_rings(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        rings = spec.get("rings", [
            {"name": "LÕI CỐT LÕI (CORE)", "desc": "Giá trị nền tảng & Sứ mệnh"},
            {"name": "VÒNG TRONG (INTERNAL)", "desc": "Năng lực công nghệ & Đội ngũ"},
            {"name": "VÒNG NGOÀI (ECOSYSTEM)", "desc": "Mạng lưới đối tác & Khách hàng"}
        ])

        center_x = left + (width * 0.35)
        center_y = top + (height / 2.0)
        max_r = min(height * 0.85, 230.0)
        n = len(rings)
        COLORS = ["#0284C7", "#0369A1", "#075985"]

        for i in range(n - 1, -1, -1):
            r_cur = max_r * ((i + 1) / n)
            circle = slide.Shapes.AddShape(msoShapeOval, center_x - (r_cur / 2.0), center_y - (r_cur / 2.0), r_cur, r_cur)
            circle.Fill.Solid()
            circle.Fill.ForeColor.RGB = hex_to_bgr(COLORS[i])
            circle.Line.Visible = msoTrue
            circle.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
            circle.Line.Weight = 1.5
            shapes.append(circle)

        # Right Callout Cards
        card_x = left + (width * 0.60)
        card_w = width * 0.40
        c_h = (height - (12.0 * (n - 1))) / n
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for idx, r_data in enumerate(rings):
            cy = top + idx * (c_h + 12.0)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, card_x, cy, card_w, c_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(COLORS[idx])
            card.Line.Weight = 1.5
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, card_x + 12, cy + 8, card_w - 24, c_h - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = r_data["name"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(COLORS[idx])

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = r_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11
            p2.Font.Color.RGB = hex_to_bgr(ink)
            shapes.append(tb)

        return shapes

    # 15. FRAMEWORK_VENN_2_SET (Sơ Đồ Giao Thoa 2 Vòng)
    def render_venn_2_set(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        accent = self._get_token("colors", "accent", "#10B981")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        venn_data = spec.get("venn_data", {})
        circle_left_title = venn_data.get("set_a", "Nhu Cầu Thực Tiễn Thị Trường")
        circle_right_title = venn_data.get("set_b", "Năng Lực Công Nghệ Cốt Lõi")
        intersection_title = venn_data.get("overlap", "ĐIỂM GIAO ĐỘT PHÁ\n(SWEET SPOT)")

        r = min(height * 0.78, 220.0)
        cy = top + (height - r) / 2.0
        cx_left = left + (width * 0.45) - (r * 0.7)
        cx_right = left + (width * 0.45) + (r * 0.1)

        c_a = slide.Shapes.AddShape(msoShapeOval, cx_left, cy, r, r)
        c_a.Fill.Solid()
        c_a.Fill.ForeColor.RGB = hex_to_bgr(brand)
        c_a.Fill.Transparency = 0.35
        c_a.Line.Visible = msoFalse
        shapes.append(c_a)

        c_b = slide.Shapes.AddShape(msoShapeOval, cx_right, cy, r, r)
        c_b.Fill.Solid()
        c_b.Fill.ForeColor.RGB = hex_to_bgr(accent)
        c_b.Fill.Transparency = 0.35
        c_b.Line.Visible = msoFalse
        shapes.append(c_b)

        center_x = (cx_left + cx_right + r) / 2.0
        stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, center_x - 70, cy + (r / 2.0) - 25, 140, 50)
        st = stb.TextFrame.TextRange
        st.Text = intersection_title
        st.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        st.Font.Size = 11
        st.Font.Bold = msoTrue
        st.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        stb.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(stb)

        expl_w = width * 0.36
        expl_left = left + width - expl_w
        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, expl_left, top, expl_w, height)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "card_border", "#1E293B"))
        shapes.append(card)

        etb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, expl_left + 16, top + 16, expl_w - 32, height - 32)
        etf = etb.TextFrame
        etf.WordWrap = msoTrue
        p1 = etf.TextRange.Paragraphs(1)
        p1.Text = "Phân Tích Vùng Giao Thoa Chiến Lược\n"
        p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p1.Font.Size = 14
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(brand)
        p1.ParagraphFormat.SpaceAfter = 10

        p2 = etf.TextRange.Paragraphs(2)
        p2.Text = f"• Tập Hợp A: {circle_left_title}\n• Tập Hợp B: {circle_right_title}\n\nĐiểm ngọt mang lại lợi thế độc quyền không thể sao chép khi công nghệ giải quyết triệt để bài toán thị trường."
        p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p2.Font.Size = 11.5
        p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
        shapes.append(etb)

        return shapes

    # 16. FRAMEWORK_VENN_3_SET (Sơ Đồ Giao Thoa 3 Vòng)
    def render_venn_3_set(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        r = min(height * 0.65, 180.0)
        cy_top = top + 10.0
        cy_bot = top + (height * 0.40)
        cx_mid = left + (width * 0.35)

        c1 = slide.Shapes.AddShape(msoShapeOval, cx_mid - (r / 2.0), cy_top, r, r)
        c1.Fill.Solid()
        c1.Fill.ForeColor.RGB = hex_to_bgr("#0284C7")
        c1.Fill.Transparency = 0.40
        c1.Line.Visible = msoFalse
        shapes.append(c1)

        c2 = slide.Shapes.AddShape(msoShapeOval, cx_mid - (r * 0.9), cy_bot, r, r)
        c2.Fill.Solid()
        c2.Fill.ForeColor.RGB = hex_to_bgr("#10B981")
        c2.Fill.Transparency = 0.40
        c2.Line.Visible = msoFalse
        shapes.append(c2)

        c3 = slide.Shapes.AddShape(msoShapeOval, cx_mid - (r * 0.1), cy_bot, r, r)
        c3.Fill.Solid()
        c3.Fill.ForeColor.RGB = hex_to_bgr("#F59E0B")
        c3.Fill.Transparency = 0.40
        c3.Line.Visible = msoFalse
        shapes.append(c3)

        # Right Detail
        card_w = width * 0.38
        card_left = left + width - card_w
        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, card_left, top, card_w, height)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "surface", "#0B132B"))
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "card_border", "#1E293B"))
        shapes.append(card)

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, card_left + 16, top + 16, card_w - 32, height - 32)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = "Mô Hình Giao Thoa 3 Yếu Tố Cốt Lõi\n"
        p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p1.Font.Size = 14
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "brand", "#0284C7"))

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = "1. Niềm Đam Mê & Sứ Mệnh (Xanh Lam)\n2. Năng Lực Cạnh Tranh Xuất Sắc (Xanh Ngọc)\n3. Hiệu Quả Kinh Tế & Khả Năng Sinh Lời (Vàng Cam)\n\nĐiểm giao giữa cả 3 yếu tố chính là Ikigai — định vị giá trị bền vững lâu dài của tổ chức."
        p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p2.Font.Size = 11.5
        p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
        shapes.append(tb)

        return shapes

    # 17. FRAMEWORK_DIAMOND_MODEL (Mô Hình Kim Cương Porter)
    def render_diamond_model(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        diamond_nodes = spec.get("diamond_nodes", [
            {"title": "ĐIỀU KIỆN CÁC YẾU TỐ SẢN XUẤT", "pos": "top"},
            {"title": "ĐIỀU KIỆN VỀ CẦU THỊ TRƯỜNG", "pos": "bottom"},
            {"title": "CÁC NGÀNH CÔNG NGHIỆP HỖ TRỢ", "pos": "left"},
            {"title": "CHIẾN LƯỢC, CƠ CẤU & ĐỐI THỦ", "pos": "right"}
        ])

        bw = width * 0.38
        bh = height * 0.30
        cx = left + (width - bw) / 2.0
        cy = top + (height - bh) / 2.0

        coords = [(cx, top), (cx, top + height - bh), (left, cy), (left + width - bw, cy)]
        for idx, (node, (nx, ny)) in enumerate(zip(diamond_nodes[:4], coords)):
            card = slide.Shapes.AddShape(msoShapeDiamond if idx == 0 else msoShapeRoundedRectangle, nx, ny, bw, bh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else "#1E293B")
            card.Line.Weight = 2.0 if idx == 0 else 1.0
            shapes.append(card)

            ct = card.TextFrame.TextRange
            ct.Text = node["title"]
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 11
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else ink)
            card.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 18. FRAMEWORK_ANSOFF_MATRIX (Ma Trận Ansoff)
    def render_ansoff_matrix(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        spec_ansoff = dict(spec)
        spec_ansoff["matrix_data"] = {
            "axis_x": "Thị Trường Hiện Tại  ──────────────→  Thị Trường Mới",
            "axis_y": "Sản Phẩm Mới  ↑  Sản Phẩm Hiện Tại",
            "quadrants": [
                {"title": "PHÁT TRIỂN SẢN PHẨM", "desc": "Tạo sản phẩm mới cho thị trường hiện tại (Nâng cấp V8.5)", "highlight": False},
                {"title": "ĐA DẠNG HÓA", "desc": "Sản phẩm mới thâm nhập thị trường hoàn toàn mới (Rủi ro cao)", "highlight": False},
                {"title": "THÂM NHẬP THỊ TRƯỜNG", "desc": "Đẩy mạnh sản phẩm hiện có trên thị trường quen thuộc (Ưu tiên)", "highlight": True},
                {"title": "PHÁT TRIỂN THỊ TRƯỜNG", "desc": "Đưa sản phẩm hiện có sang các vùng kinh tế/quốc gia mới", "highlight": False}
            ]
        }
        return self.render_matrix_2x2(slide, spec_ansoff, left, top, width, height)

    # 19. FRAMEWORK_MCKINSEY_7S (Mô Hình 7S McKinsey)
    def render_mckinsey_7s(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Center: Shared Values
        core_r = 60.0
        cx = left + width / 2.0
        cy = top + height / 2.0

        core = slide.Shapes.AddShape(msoShapeOval, cx - core_r, cy - core_r, core_r * 2, core_r * 2)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Visible = msoFalse
        shapes.append(core)
        ct = core.TextFrame.TextRange
        ct.Text = "SHARED\nVALUES\n(GIÁ TRỊ CỐT LÕI)"
        ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ct.Font.Size = 9.5
        ct.Font.Bold = msoTrue
        ct.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        core.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        # 6 Surrounding S's
        six_s = [
            "1. STRATEGY\n(Chiến Lược)", "2. STRUCTURE\n(Cơ Cấu)", "3. SYSTEMS\n(Hệ Thống)",
            "4. STYLE\n(Phong Cách)", "5. STAFF\n(Đội Ngũ)", "6. SKILLS\n(Kỹ Năng)"
        ]
        s_w, s_h = 130.0, 50.0
        positions = [
            (cx - s_w / 2.0, top),                                    # Top
            (cx + (width * 0.28), top + (height * 0.18)),             # Top-Right
            (cx + (width * 0.28), top + (height * 0.62)),             # Bottom-Right
            (cx - s_w / 2.0, top + height - s_h),                     # Bottom
            (cx - (width * 0.28) - s_w, top + (height * 0.62)),        # Bottom-Left
            (cx - (width * 0.28) - s_w, top + (height * 0.18))         # Top-Left
        ]

        for s_text, (sx, sy) in zip(six_s, positions):
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, sy, s_w, s_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr("#1E293B")
            shapes.append(card)

            st = card.TextFrame.TextRange
            st.Text = s_text
            st.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            st.Font.Size = 10
            st.Font.Bold = msoTrue
            st.Font.Color.RGB = hex_to_bgr(ink)
            card.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 20. FRAMEWORK_STRATEGY_CLOCK (Đồng Hồ Chiến Lược Bowman)
    def render_strategy_clock(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        # 8 positions along an octagon/clock
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        r = min(height * 0.82, 240.0)
        cx = left + (width * 0.35)
        cy = top + height / 2.0

        clock_face = slide.Shapes.AddShape(msoShapeOval, cx - r/2.0, cy - r/2.0, r, r)
        clock_face.Fill.Solid()
        clock_face.Fill.ForeColor.RGB = hex_to_bgr(surface)
        clock_face.Line.Visible = msoTrue
        clock_face.Line.ForeColor.RGB = hex_to_bgr(brand)
        clock_face.Line.Weight = 2.0
        shapes.append(clock_face)

        c_text = clock_face.TextFrame.TextRange
        c_text.Text = "ĐỒNG HỒ CHIẾN LƯỢC\n(BOWMAN CLOCK)"
        c_text.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        c_text.Font.Size = 11
        c_text.Font.Bold = msoTrue
        c_text.Font.Color.RGB = hex_to_bgr(brand)
        clock_face.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        # Right Legend
        rw = width * 0.45
        rx = left + width - rw
        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx, top + 10, rw, height - 20)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = "8 Vị Trí Cạnh Tranh Của Bowman\n"
        p1.Font.Size = 14
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(brand)

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = "1. Giá thấp / Giá trị thấp (No frills)\n2. Giá thấp chuẩn (Low price)\n3. Lai ghép Tối ưu (Hybrid - Khuyên dùng)\n4. Khác biệt hóa cao (Differentiation)\n5. Khác biệt hóa tập trung (Focused)\n6. Giá cao rủi ro (Risky high margins)\n7. Độc quyền độc đoán (Monopoly)\n8. Thất bại chắc chắn (Loss of market share)"
        p2.Font.Size = 11
        p2.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(tb)

        return shapes

    # 21. FRAMEWORK_CMMI_STAIRS (Tháp Bậc Thang CMMI)
    def render_cmmi_stairs(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        stairs = spec.get("cmmi_levels", [
            {"lvl": "CẤP 1: TÙY TIỆN", "desc": "Quy trình tự phát, phụ thuộc cá nhân"},
            {"lvl": "CẤP 2: QUẢN LÝ ĐƯỢC", "desc": "Đã có kế hoạch và giám sát dự án"},
            {"lvl": "CẤP 3: ĐÃ ĐỊNH NGHĨA", "desc": "Quy chuẩn hóa tài liệu toàn tổ chức"},
            {"lvl": "CẤP 4: ĐỊNH LƯỢNG", "desc": "Đo lường bằng chỉ số KPI & thống kê"},
            {"lvl": "CẤP 5: TỐI ƯU HÓA", "desc": "Cải tiến liên tục bằng AI tự động"}
        ])

        n = len(stairs)
        step_w = width / n
        base_h = height / n
        COLORS = ["#1E293B", "#075985", "#0369A1", "#0D9488", "#10B981"]

        for i, s_data in enumerate(stairs):
            cur_h = base_h * (i + 1)
            sx = left + i * step_w
            sy = top + height - cur_h

            block = slide.Shapes.AddShape(msoShapeRectangle, sx, sy, step_w - 6, cur_h)
            block.Fill.Solid()
            block.Fill.ForeColor.RGB = hex_to_bgr(COLORS[i % len(COLORS)])
            block.Line.Visible = msoFalse
            shapes.append(block)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 4, sy + 8, step_w - 14, 60)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = s_data["lvl"] + "\n"
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = s_data["desc"]
            p2.Font.Size = 9
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0")
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 22. FRAMEWORK_VRIO_MATRIX (Khung Năng Lực VRIO)
    def render_vrio_matrix(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        spec_vrio = dict(spec)
        spec_vrio["table_data"] = {
            "headers": ["Năng Lực / Tài Sản Cốt Lõi", "Giá Trị (V)", "Độ Hiếm (R)", "Khó Sao Chép (I)", "Tổ Chức (O)", "Hàm Ý Cạnh Tranh"],
            "rows": [
                ["Kiến trúc 16 tác tử MACC", "Có (Yes)", "Có (Yes)", "Có (Yes)", "Có (Yes)", "LỢI THẾ BỀN VỮNG"],
                ["Kho 110+ Archetypes chuẩn", "Có (Yes)", "Có (Yes)", "Có (Yes)", "Có (Yes)", "LỢI THẾ BỀN VỮNG"],
                ["Hạ tầng máy chủ đám mây", "Có (Yes)", "Không", "Không", "Có (Yes)", "NGANG BẰNG CẠNH TRANH"],
                ["Tài liệu đào tạo chuẩn hóa", "Có (Yes)", "Có (Yes)", "Không", "Có (Yes)", "LỢI THẾ TẠM THỜI"]
            ]
        }
        from .tables_engine import NativeTablesEngine
        t_engine = NativeTablesEngine(theme=self.theme, tokens=self.tokens)
        res = t_engine.render_comparison_table(slide, spec_vrio, left, top, width, height)
        return [res] if res else []

    # 23. FRAMEWORK_GOLDEN_CIRCLE (Simon Sinek Why-How-What)
    def render_golden_circle(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        spec_rings = dict(spec)
        spec_rings["rings"] = [
            {"name": "TẠI SAO? (WHY - TÂM ĐIỂM)", "desc": "Mục đích tối thượng, niềm tin và lý do tổ chức tồn tại"},
            {"name": "NHƯ THẾ NÀO? (HOW - PHƯƠNG THỨC)", "desc": "Hành động cụ thể và các giá trị tạo nên sự khác biệt"},
            {"name": "CÁI GÌ? (WHAT - KẾT QUẢ)", "desc": "Sản phẩm, dịch vụ và những giải pháp cụ thể trao tới tay người dùng"}
        ]
        return self.render_concentric_rings(slide, spec_rings, left, top, width, height)

    # 24. FRAMEWORK_ICEBERG_MODEL (Mô Hình Tảng Băng Chìm)
    def render_iceberg_model(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        water_y = top + (height * 0.32)

        # Sky
        sky = slide.Shapes.AddShape(msoShapeRectangle, left, top, width, height * 0.32)
        sky.Fill.Solid()
        sky.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E0F2FE")
        sky.Line.Visible = msoFalse
        shapes.append(sky)

        # Waterline
        water = slide.Shapes.AddShape(msoShapeRectangle, left, water_y, width, height * 0.68)
        water.Fill.Solid()
        water.Fill.ForeColor.RGB = hex_to_bgr("#082F49" if self.theme == "DARK" else "#0369A1")
        water.Line.Visible = msoFalse
        shapes.append(water)

        # Top Tip (10%)
        tip = slide.Shapes.AddShape(msoShapeIsoscelesTriangle, left + (width * 0.38), top + 20, width * 0.24, water_y - top - 20)
        tip.Fill.Solid()
        tip.Fill.ForeColor.RGB = hex_to_bgr("#FFFFFF")
        tip.Line.Visible = msoFalse
        shapes.append(tip)
        tt = tip.TextFrame.TextRange
        tt.Text = "PHẦN NỔI (10%)\nSự kiện nhìn thấy"
        tt.Font.Size = 10
        tt.Font.Bold = msoTrue
        tt.Font.Color.RGB = hex_to_bgr("#0F172A")
        tip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        # Bottom Bulk (90%)
        bulk = slide.Shapes.AddShape(msoShapeTrapezoid, left + (width * 0.22), water_y + 10, width * 0.56, height * 0.60)
        bulk.Fill.Solid()
        bulk.Fill.ForeColor.RGB = hex_to_bgr("#0284C7")
        bulk.Line.Visible = msoFalse
        shapes.append(bulk)
        bt = bulk.TextFrame.TextRange
        bt.Text = "PHẦN CHÌM (90% - BẢN CHẤT CỐT LÕI)\n\n• Xu hướng & Khuôn mẫu hành vi lặp lại\n• Cấu trúc hệ thống & Ràng buộc thể chế\n• Mô hình tâm trí & Niềm tin ngầm định sâu sắc"
        bt.Font.Size = 11.5
        bt.Font.Bold = msoTrue
        bt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        bulk.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 25. FRAMEWORK_DOUBLE_DIAMOND (Thiết Kế 2 Viên Kim Cương)
    def render_double_diamond(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        gap = 20.0
        dw = (width - gap) / 2.0
        dh = height * 0.75
        dy = top + (height - dh) / 2.0

        # Diamond 1: Problem Space
        d1 = slide.Shapes.AddShape(msoShapeDiamond, left, dy, dw, dh)
        d1.Fill.Solid()
        d1.Fill.ForeColor.RGB = hex_to_bgr(surface)
        d1.Line.Visible = msoTrue
        d1.Line.ForeColor.RGB = hex_to_bgr(brand)
        d1.Line.Weight = 2.0
        shapes.append(d1)
        t1 = d1.TextFrame.TextRange
        t1.Text = "KIM CƯƠNG 1: BÀI TOÁN (PROBLEM)\n\n1. Khám Phá (Discover)\n2. Định Nghĩa (Define)"
        t1.Font.Size = 11.5
        t1.Font.Bold = msoTrue
        t1.Font.Color.RGB = hex_to_bgr(brand)
        d1.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        # Diamond 2: Solution Space
        d2 = slide.Shapes.AddShape(msoShapeDiamond, left + dw + gap, dy, dw, dh)
        d2.Fill.Solid()
        d2.Fill.ForeColor.RGB = hex_to_bgr(surface)
        d2.Line.Visible = msoTrue
        d2.Line.ForeColor.RGB = hex_to_bgr("#10B981")
        d2.Line.Weight = 2.0
        shapes.append(d2)
        t2 = d2.TextFrame.TextRange
        t2.Text = "KIM CƯƠNG 2: GIẢI PHÁP (SOLUTION)\n\n3. Phát Triển (Develop)\n4. Bàn Giao (Deliver)"
        t2.Font.Size = 11.5
        t2.Font.Bold = msoTrue
        t2.Font.Color.RGB = hex_to_bgr("#10B981")
        d2.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes
