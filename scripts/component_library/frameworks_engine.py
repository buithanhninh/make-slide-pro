"""
frameworks_engine.py
Exhaustive Strategic Frameworks Engine for Make Slide Pro V8.5.0.
Generates 25 classic management consulting, business strategy, and intellectual models
using 100% Microsoft PowerPoint Native Vector Shapes.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

from .utils import safe_group, add_vector_connector

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
            q_shapes = []
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, qx, qy, qw, qh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(brand if (is_hl and self.theme == "DARK") else (surface if not is_hl else "#E0F2FE"))
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if is_hl else border)
            card.Line.Weight = 2.0 if is_hl else 1.0
            q_shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, qx + 16, qy + 14, qw - 32, qh - 28)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = q.get("title", f"PHÂN VÙNG 0{i+1}") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 14
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if (is_hl and self.theme == "DARK") else (brand if is_hl else ink))
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = q.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0" if (is_hl and self.theme == "DARK") else muted)
            try:
                p2.ParagraphFormat.SpaceWithin = 1.25
            except Exception:
                pass
            q_shapes.append(tb)

            grp = safe_group(slide, q_shapes, f"Matrix_Quadrant_{i+1}")
            shapes.append(grp)

        ax_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left, matrix_top + 2 * qh + gap + 4.0, width, 24)
        at = ax_tb.TextFrame.TextRange
        if axis_y and axis_y != "Giá Trị Tác Động Chiến Lược →":
            at.Text = f"▲ {axis_y}   •   ► {axis_x}"
        else:
            at.Text = axis_x
        at.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        at.Font.Size = 14.5
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
            p1.Font.Size = 15.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"[{tag}]"
            p2.Font.Size = 14.5
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
        ct.Font.Size = 15.0
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
            bt.Font.Size = 14.5
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
            st.Font.Size = 14.5
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
            pt.Font.Size = 14.5
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
        mt.Font.Size = 14.5
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

        atoms = spec.get("atoms", [])
        default_swot = [
            {"letter": "S", "title": "ĐIỂM MẠNH (STRENGTHS)", "color": "#10B981"},
            {"letter": "W", "title": "ĐIỂM YẾU (WEAKNESSES)", "color": "#EF4444"},
            {"letter": "O", "title": "CƠ HỘI (OPPORTUNITIES)", "color": "#0284C7"},
            {"letter": "T", "title": "THÁCH THỨC (THREATS)", "color": "#F59E0B"}
        ]
        swot_raw = spec.get("swot") or spec.get("swot_data")
        if swot_raw:
            swot_data = swot_raw
        elif atoms and len(atoms) >= 4:
            swot_data = []
            for i, a in enumerate(atoms[:4]):
                t = a.get("title", default_swot[i]["title"]) if isinstance(a, dict) else default_swot[i]["title"]
                d = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                bullets = [b.strip() for b in d.split("\n") if b.strip()]
                if not bullets:
                    bullets = [d]
                swot_data.append({
                    "letter": default_swot[i]["letter"],
                    "title": t,
                    "items": bullets,
                    "color": default_swot[i]["color"]
                })
        else:
            claim = spec.get("primary_claim", "Nội dung phân tích bối cảnh chuyên môn.")
            swot_data = [
                {"letter": default_swot[i]["letter"], "title": default_swot[i]["title"], "items": [claim], "color": default_swot[i]["color"]}
                for i in range(4)
            ]

        gap = 14.0
        qw = (width - gap) / 2.0
        qh = (height - gap) / 2.0
        coords = [(left, top), (left + qw + gap, top), (left, top + qh + gap), (left + qw + gap, top + qh + gap)]

        for idx, (item, (cx, cy)) in enumerate(zip(swot_data[:4], coords)):
            q_shapes = []
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy, qw, qh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(item["color"])
            card.Line.Weight = 2.0
            q_shapes.append(card)

            # Giant Letter Badge (S, W, O, T)
            badge = slide.Shapes.AddShape(msoShapeOval, cx + 16, cy + 14, 38, 38)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr(item["color"])
            badge.Line.Visible = msoFalse
            bt = badge.TextFrame.TextRange
            bt.Text = item["letter"]
            bt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            bt.Font.Size = 18
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            q_shapes.append(badge)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 62, cy + 14, qw - 76, qh - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = item["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 16.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(item["color"])
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = "\n".join([f"• {x}" for x in item.get("items", [])])
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            try:
                p2.ParagraphFormat.SpaceWithin = 1.2
            except Exception:
                pass
            q_shapes.append(tb)

            grp = safe_group(slide, q_shapes, f"SWOT_Card_{item.get('letter', idx+1)}")
            shapes.append(grp)

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
            p1.Font.Size = 15.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(COLORS[idx % len(COLORS)])
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = item.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 14.5
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
            p1.Font.Size = 16.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(item["color"])
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = "\n".join([f"• {g}" for g in item.get("goals", [])])
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15.0
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
        muted = self._get_token("colors", "muted", "#94A3B8")

        data = spec.get("house_data", {})
        atoms = spec.get("atoms", [])
        roof_title = data.get("roof") or spec.get("assertion_title", "TẦM NHÌN & ĐỊNH HƯỚNG CHIẾN LƯỢC QUỐC GIA")
        if data.get("pillars"):
            pillars = data["pillars"]
        elif atoms:
            pillars = []
            for i, a in enumerate(atoms[:4]):
                t = a.get("title", f"Trụ Cột 0{i+1}") if isinstance(a, dict) else f"Trụ Cột 0{i+1}"
                d = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                pillars.append({"title": t, "desc": d})
            while len(pillars) < 4:
                pillars.append({"title": f"Trụ Cột 0{len(pillars)+1}", "desc": "Giải pháp bổ trợ chuẩn hóa."})
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa chuyên môn.")
            pillars = [
                {"title": f"Trụ Cột 0{i+1}: Yếu Tố Cốt Lõi", "desc": claim}
                for i in range(4)
            ]
        foundation = data.get("foundation", "NỀN MÓNG CỐT LÕI: HỆ THỐNG CHÍNH SÁCH • NĂNG LỰC CHUYÊN MÔN • VẬN HÀNH THỰC TIỄN")

        roof_h = 52.0
        found_h = 44.0
        gap = 14.0
        pillar_h = height - roof_h - found_h - (gap * 2)

        # 1. Roof Group
        roof_shapes = []
        roof_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, roof_h)
        roof_bar.Fill.Solid()
        roof_bar.Fill.ForeColor.RGB = hex_to_bgr(brand)
        roof_bar.Line.Visible = msoFalse
        roof_shapes.append(roof_bar)

        rt = roof_bar.TextFrame.TextRange
        rt.Text = f"★  {roof_title}  ★"
        rt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        rt.Font.Size = 16.0.5
        rt.Font.Bold = msoTrue
        rt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        roof_bar.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        roof_group = safe_group(slide, roof_shapes, "House_Roof_Group")
        shapes.append(roof_group)

        # 2. Pillars Groups
        p_count = len(pillars)
        pw = (width - (gap * (p_count - 1))) / p_count
        py = top + roof_h + gap
        pillar_colors = ["#0284C7", "#38BDF8", "#10B981", "#8B5CF6", "#F59E0B"]

        for idx, pil in enumerate(pillars):
            p_shapes = []
            px = left + idx * (pw + gap)
            p_color = pillar_colors[idx % len(pillar_colors)]

            p_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, py, pw, pillar_h)
            p_card.Fill.Solid()
            p_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            p_card.Line.Visible = msoTrue
            p_card.Line.ForeColor.RGB = hex_to_bgr(p_color)
            p_card.Line.Weight = 2.0
            p_shapes.append(p_card)

            # Top Number Pill
            pill_w = 64.0
            pill_h = 24.0
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, px + (pw - pill_w) / 2.0, py + 14.0, pill_w, pill_h)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(p_color)
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = f"0{idx+1}"
            pt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            pt.Font.Size = 15.5
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            p_shapes.append(pill)

            # Pillar Title
            tb_title = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 10, py + 46.0, pw - 20, 38)
            ttf = tb_title.TextFrame
            ttf.WordWrap = msoTrue
            ttf.MarginLeft = 0
            ttf.MarginRight = 0
            ttr = ttf.TextRange
            ttr.Text = pil.get("title", f"Trụ Cột {idx+1}")
            ttr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ttr.Font.Size = 15.5
            ttr.Font.Bold = msoTrue
            ttr.Font.Color.RGB = hex_to_bgr(ink)
            ttr.ParagraphFormat.Alignment = ppAlignCenter
            p_shapes.append(tb_title)

            # Divider line
            div_line = slide.Shapes.AddShape(msoShapeRectangle, px + 18, py + 90.0, pw - 36, 1.5)
            div_line.Fill.Solid()
            div_line.Fill.ForeColor.RGB = hex_to_bgr(p_color)
            div_line.Line.Visible = msoFalse
            p_shapes.append(div_line)

            # Structured Description / Bullets
            desc_text = pil.get("desc", "")
            tb_desc = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 12, py + 100.0, pw - 24, pillar_h - 145)
            dtf = tb_desc.TextFrame
            dtf.WordWrap = msoTrue
            dtf.MarginLeft = 0
            dtf.MarginRight = 0
            dtr = dtf.TextRange
            dtr.Text = desc_text
            dtr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            dtr.Font.Size = 14.5
            dtr.Font.Color.RGB = hex_to_bgr(muted)
            dtr.ParagraphFormat.Alignment = ppAlignCenter
            p_shapes.append(tb_desc)

            # Bottom KPI chip
            chip_label = pil.get("kpi") or pil.get("chip") or pil.get("badge")
            if not chip_label:
                chip_label = f"Mục Tiêu 0{idx+1}: Trọng Tâm"
            chip_w = pw - 32.0
            chip_h = 24.0
            chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, px + 16.0, py + pillar_h - 34.0, chip_w, chip_h)
            chip.Fill.Solid()
            chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            chip.Line.Visible = msoTrue
            chip.Line.ForeColor.RGB = hex_to_bgr(p_color)
            chip.Line.Weight = 1.0
            ct = chip.TextFrame.TextRange
            ct.Text = f"✔ {chip_label}"
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 14.5
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(p_color)
            chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            p_shapes.append(chip)

            pillar_group = safe_group(slide, p_shapes, f"House_Pillar_Group_{idx+1}")
            shapes.append(pillar_group)

        # 3. Foundation Group
        found_shapes = []
        fy = top + height - found_h
        found_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, fy, width, found_h)
        found_bar.Fill.Solid()
        found_bar.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
        found_bar.Line.Visible = msoTrue
        found_bar.Line.ForeColor.RGB = hex_to_bgr(border)
        found_bar.Line.Weight = 1.5
        found_shapes.append(found_bar)

        ft = found_bar.TextFrame.TextRange
        ft.Text = foundation
        ft.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ft.Font.Size = 15.0
        ft.Font.Bold = msoTrue
        ft.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
        found_bar.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        found_group = safe_group(slide, found_shapes, "House_Foundation_Group")
        shapes.append(found_group)

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

        tier_groups = []
        for i, l_data in enumerate(layers):
            ly = top + i * (layer_h + 8.0)
            w_cur = pyr_w * (0.45 + (i * (0.55 / max(1, n - 1))))
            lx = left + (pyr_w - w_cur) / 2.0

            shape = slide.Shapes.AddShape(msoShapeRoundedRectangle, lx, ly, w_cur, layer_h)
            shape.Fill.Solid()
            shape.Fill.ForeColor.RGB = hex_to_bgr(COLORS[i % len(COLORS)])
            shape.Line.Visible = msoFalse

            st = shape.TextFrame.TextRange
            st.Text = l_data["tier"]
            st.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            st.Font.Size = 15.5
            st.Font.Bold = msoTrue
            st.Font.Color.RGB = hex_to_bgr("#FFFFFF" if i < 3 or self.theme == "DARK" else "#0F172A")
            shape.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, detail_left, ly, detail_w, layer_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "card_border", "#1E293B"))

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, detail_left + 14, ly + 6, detail_w - 28, layer_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = l_data["title"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 16.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if i == 0 else ink)
            p1.ParagraphFormat.SpaceAfter = 4

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = l_data["desc"]
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15.0
            p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            try:
                p2.ParagraphFormat.SpaceWithin = 1.2
            except Exception:
                pass

            tier_grp = safe_group(slide, [shape, card, tb], f"Pyramid_Tier_{i+1}")
            tier_groups.append(tier_grp)

        # Pedagogical Inversion: Presentation reveals from Foundation (Base) up to Peak!
        return list(reversed(tier_groups))

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
            bt.Font.Size = 14.5
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
            p1.Font.Size = 15.0
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
        ct.Font.Size = 14.5
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
            p1.Font.Size = 15.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if i == 0 else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = n_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 14.5
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
        ht.Font.Size = 15.0
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
            p1.Font.Size = 15.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = sp_item.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 14.5
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
            p1.Font.Size = 15.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(COLORS[idx])

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = r_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15.0
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
        st.Font.Size = 15.0
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
        p2.Font.Size = 15.0
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
        p2.Font.Size = 15.0
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
            ct.Font.Size = 15.0
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
        ct.Font.Size = 16.0.5
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
            st.Font.Size = 14.5
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
        c_text.Font.Size = 15.0
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
        p2.Font.Size = 15.0
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
            p1.Font.Size = 14.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = s_data["desc"]
            p2.Font.Size = 16.0.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0")
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 22. FRAMEWORK_VRIO_MATRIX (Khung Năng Lực VRIO)
    def render_vrio_matrix(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        spec_vrio = dict(spec)
        atoms = spec.get("atoms", [])
        if not spec_vrio.get("table_data"):
            headers = ["Năng Lực / Tài Sản Cốt Lõi", "Giá Trị (V)", "Độ Hiếm (R)", "Khó Sao Chép (I)", "Tổ Chức (O)", "Hàm Ý Cạnh Tranh"]
            if atoms:
                rows = []
                for i, a in enumerate(atoms[:4]):
                    t = a.get("title", f"Năng Lực 0{i+1}") if isinstance(a, dict) else str(a)
                    rows.append([t, "Có (Yes)", "Có (Yes)", "Có (Yes)", "Có (Yes)", "LỢI THẾ BỀN VỮNG"])
            else:
                rows = [
                    ["1. Đội ngũ nhân lực chuyên môn cao", "Có (Yes)", "Có (Yes)", "Có (Yes)", "Có (Yes)", "LỢI THẾ BỀN VỮNG"],
                    ["2. Mạng lưới dịch vụ phủ khắp cơ sở", "Có (Yes)", "Có (Yes)", "Có (Yes)", "Có (Yes)", "LỢI THẾ BỀN VỮNG"],
                    ["3. Trang thiết bị y tế chuyên dụng", "Có (Yes)", "Không", "Không", "Có (Yes)", "NGANG BẰNG CẠNH TRANH"],
                    ["4. Quy trình chuyên môn chuẩn hóa", "Có (Yes)", "Có (Yes)", "Không", "Có (Yes)", "LỢI THẾ TẠM THỜI"]
                ]
            spec_vrio["table_data"] = {"headers": headers, "rows": rows}
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
        tt.Font.Size = 14.5
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
        bt.Font.Size = 15.0
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
        t1.Font.Size = 15.0
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
        t2.Font.Size = 15.0
        t2.Font.Bold = msoTrue
        t2.Font.Color.RGB = hex_to_bgr("#10B981")
        d2.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 26. FRAMEWORK_STEEPLE (Mô Hình STEEPLE 7 Yếu Tố Vĩ Mô)
    def render_steeple(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")
        items = spec.get("framework_items", [
            {"letter": "S", "label": "XÃ HỘI", "full": "Social", "desc": "Già hóa dân số, dịch chuyển lao động số & nhu cầu học tập liên tục"},
            {"letter": "T", "label": "CÔNG NGHỆ", "full": "Tech", "desc": "Trí tuệ nhân tạo GenAI, tự động hóa & điện toán đám mây"},
            {"letter": "E", "label": "KINH TẾ", "full": "Economic", "desc": "Lạm phát, lãi suất biến động & áp lực tối ưu hóa chi phí vận hành"},
            {"letter": "E", "label": "MÔI TRƯỜNG", "full": "Environmental", "desc": "Chuyển đổi xanh ESG, giảm thiểu phát thải carbon & Net Zero 2050"},
            {"letter": "P", "label": "CHÍNH TRỊ", "full": "Political", "desc": "Khung pháp lý chuyển đổi số, ưu đãi đầu tư công nghệ cao"},
            {"letter": "L", "label": "PHÁP LÝ", "full": "Legal", "desc": "Luật bảo vệ dữ liệu cá nhân (GDPR, PDPA) & an toàn không gian mạng"},
            {"letter": "E", "label": "ĐẠO ĐỨC", "full": "Ethical", "desc": "Minh bạch mô hình AI, trách nhiệm giải trình thuật toán & văn hóa số"}
        ])

        n = len(items)
        gap = 10.0
        card_w = (width - gap * (n - 1)) / float(n)
        card_h = min(height, 300.0)
        card_y = top + (height - card_h) / 2.0

        steeple_colors = ["#0284C7", "#38BDF8", "#10B981", "#059669", "#F59E0B", "#8B5CF6", "#EC4899"]

        for i, item in enumerate(items):
            col_shapes = []
            cx = left + i * (card_w + gap)
            color = steeple_colors[i % len(steeple_colors)]

            # Card background
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(color)
            card.Line.Weight = 1.8
            col_shapes.append(card)

            # Top Circular Letter Badge
            circle_size = 38.0
            circle_x = cx + (card_w - circle_size) / 2.0
            circle_y = card_y + 14.0
            circle = slide.Shapes.AddShape(msoShapeOval, circle_x, circle_y, circle_size, circle_size)
            circle.Fill.Solid()
            circle.Fill.ForeColor.RGB = hex_to_bgr(color)
            circle.Line.Visible = msoFalse
            ct = circle.TextFrame.TextRange
            letter = item.get("letter", item.get("label", "S")[:1])
            ct.Text = letter
            ct.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            ct.Font.Size = 17
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            circle.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            col_shapes.append(circle)

            # Factor label
            tb_title = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 4, card_y + 58.0, card_w - 8, 34)
            ttf = tb_title.TextFrame
            ttf.WordWrap = msoTrue
            ttf.MarginLeft = 0
            ttf.MarginRight = 0
            ttr = ttf.TextRange
            ttr.Text = item.get("label", f"Yếu Tố {i+1}")
            ttr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ttr.Font.Size = 15.0
            ttr.Font.Bold = msoTrue
            ttr.Font.Color.RGB = hex_to_bgr(color)
            ttr.ParagraphFormat.Alignment = ppAlignCenter
            col_shapes.append(tb_title)

            # Divider line
            div = slide.Shapes.AddShape(msoShapeRectangle, cx + 10, card_y + 94.0, card_w - 20, 1.5)
            div.Fill.Solid()
            div.Fill.ForeColor.RGB = hex_to_bgr(color)
            div.Line.Visible = msoFalse
            col_shapes.append(div)

            # Description
            tb_desc = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 6, card_y + 102.0, card_w - 12, card_h - 142)
            dtf = tb_desc.TextFrame
            dtf.WordWrap = msoTrue
            dtf.MarginLeft = 0
            dtf.MarginRight = 0
            dtr = dtf.TextRange
            dtr.Text = item.get("desc", "")
            dtr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            dtr.Font.Size = 14.5
            dtr.Font.Color.RGB = hex_to_bgr(muted)
            dtr.ParagraphFormat.Alignment = ppAlignCenter
            col_shapes.append(tb_desc)

            # Bottom impact tag
            tag_w = card_w - 16.0
            tag_h = 22.0
            tag = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 8.0, card_y + card_h - 30.0, tag_w, tag_h)
            tag.Fill.Solid()
            tag.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            tag.Line.Visible = msoFalse
            tt = tag.TextFrame.TextRange
            tt.Text = "Tác Động Cao"
            tt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            tt.Font.Size = 16.0.5
            tt.Font.Bold = msoTrue
            tt.Font.Color.RGB = hex_to_bgr(color)
            tag.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            col_shapes.append(tag)

            grp = safe_group(slide, col_shapes, f"Steeple_Card_{i+1}")
            shapes.append(grp)

        return shapes

    # 27. FRAMEWORK_KANO_MODEL (Mô Hình Kano Phân Loại Tính Năng)
    def render_kano_model(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        lane_h = (height - 24.0) / 3.0
        atoms = spec.get("atoms", [])
        default_tiers = [
            ("1. ĐỘT PHÁ & GIÁ TRỊ VƯỢT TRỘI", "#10B981"),
            ("2. HIỆU QUẢ VẬN HÀNH & TỶ LỆ THUẬN", "#0284C7"),
            ("3. TIÊU CHUẨN BẮT BUỘC NỀN TẢNG", "#F59E0B")
        ]
        if spec.get("lanes"):
            lanes = spec["lanes"]
        elif atoms:
            lanes = []
            for idx, a in enumerate(atoms[:3]):
                t = a.get("title", f"Phân Cấp 0{idx+1}") if isinstance(a, dict) else f"Phân Cấp 0{idx+1}"
                d = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                tier_name, color = default_tiers[idx % len(default_tiers)]
                lanes.append({"tier": f"{tier_name}: {t}", "color": color, "desc": d})
        else:
            claim = spec.get("primary_claim", "Nội dung phân loại tính năng chuyên môn.")
            lanes = [
                {"tier": default_tiers[i][0], "color": default_tiers[i][1], "desc": claim}
                for i in range(3)
            ]

        for idx, lane in enumerate(lanes):
            ly = top + idx * (lane_h + 12.0)
            sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ly, width, lane_h)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = hex_to_bgr(surface)
            sh.Line.Visible = msoTrue
            sh.Line.ForeColor.RGB = hex_to_bgr(lane["color"])
            sh.Line.Weight = 2.0
            shapes.append(sh)

            tr = sh.TextFrame.TextRange
            tr.Text = f"{lane['tier']}\n{lane['desc']}"
            tr.Font.Size = 15.5
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 28. FRAMEWORK_LEAN_CANVAS (Mô Hình Kinh Doanh Tinh Gọn 9 Ô)
    def render_lean_canvas(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # 5 upper columns, 2 lower rows
        col_w = width / 5.0
        upper_h = height * 0.65
        lower_h = height * 0.32
        gap = 4.0

        atoms = spec.get("atoms", [])
        claim = spec.get("primary_claim", "Trọng tâm bài giảng chuyên môn.")
        a_texts = [a.get("text") or a.get("title") or str(a) if isinstance(a, dict) else str(a) for a in atoms]
        while len(a_texts) < 9:
            a_texts.append(claim)

        boxes = [
            # Upper row (5 primary sectors)
            (left, top, col_w - gap, upper_h, f"1. VẤN ĐỀ & BỐI CẢNH\n\n• {a_texts[0]}"),
            (left + col_w, top, col_w - gap, upper_h * 0.48, f"2. GIẢI PHÁP\n• {a_texts[1]}"),
            (left + col_w, top + upper_h * 0.52, col_w - gap, upper_h * 0.48, f"8. CHỈ SỐ THEN CHỐT\n• {a_texts[7]}"),
            (left + 2 * col_w, top, col_w - gap, upper_h, f"3. GIÁ TRỊ CỐT LÕI\n\n{a_texts[2]}"),
            (left + 3 * col_w, top, col_w - gap, upper_h * 0.48, f"9. LỢI THẾ CHUYÊN MÔN\n• {a_texts[8]}"),
            (left + 3 * col_w, top + upper_h * 0.52, col_w - gap, upper_h * 0.48, f"4. PHƯƠNG THỨC TIẾP CẬN\n• {a_texts[3]}"),
            (left + 4 * col_w, top, col_w - gap, upper_h, f"5. ĐỐI TƯỢNG THỤ HƯỞNG\n\n• {a_texts[4]}"),
            # Lower row (Cost structure & Revenue streams)
            (left, top + upper_h + 8.0, width * 0.5 - gap, lower_h, f"7. NGUỒN LỰC & CHI PHÍ\n• {a_texts[6]}"),
            (left + width * 0.5, top + upper_h + 8.0, width * 0.5, lower_h, f"6. HIỆU QUẢ KINH TẾ - XÃ HỘI\n• {a_texts[5]}")
        ]

        for bx, by, bw, bh, text in boxes:
            b = slide.Shapes.AddShape(msoShapeRoundedRectangle, bx, by, bw, bh)
            b.Fill.Solid()
            b.Fill.ForeColor.RGB = hex_to_bgr(surface)
            b.Line.Visible = msoTrue
            b.Line.ForeColor.RGB = hex_to_bgr(brand)
            b.Line.Weight = 1.0
            shapes.append(b)

            tr = b.TextFrame.TextRange
            tr.Text = text
            tr.Font.Size = 16.0.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 29. FRAMEWORK_VALUE_PROPOSITION_CANVAS (Bản Đồ Đề Xuất Giá Trị Osterwalder)
    def render_value_proposition_canvas(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        accent = self._get_token("colors", "accent", "#38BDF8")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")
        success = self._get_token("colors", "success", "#10B981")

        canvas_h = min(height, 310.0)
        canvas_y = top + (height - canvas_h) / 2.0

        center_gap = 70.0
        side_w = (width - center_gap) / 2.0

        # =========================================================
        # 1. LEFT CONTAINER: BẢN ĐỒ GIÁ TRỊ (VALUE MAP - SQUARE)
        # =========================================================
        left_shapes = []
        vm_bg = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, canvas_y, side_w, canvas_h)
        vm_bg.Fill.Solid()
        vm_bg.Fill.ForeColor.RGB = hex_to_bgr(surface)
        vm_bg.Line.Visible = msoTrue
        vm_bg.Line.ForeColor.RGB = hex_to_bgr(brand)
        vm_bg.Line.Weight = 2.0
        left_shapes.append(vm_bg)

        # Value Map Header Badge
        vm_badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 14, canvas_y + 12, side_w - 28, 28)
        vm_badge.Fill.Solid()
        vm_badge.Fill.ForeColor.RGB = hex_to_bgr(brand)
        vm_badge.Line.Visible = msoFalse
        vmt = vm_badge.TextFrame.TextRange
        vmt.Text = "■  BẢN ĐỒ GIÁ TRỊ (VALUE MAP) - SẢN PHẨM"
        vmt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        vmt.Font.Size = 15.0
        vmt.Font.Bold = msoTrue
        vmt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        vm_badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        left_shapes.append(vm_badge)

        # 3 Sub-Cards for Value Map
        sub_gap = 7.0
        sub_h = (canvas_h - 58.0 - (2 * sub_gap)) / 3.0
        vm_subcards = [
            ("1. Sản Phẩm & Dịch Vụ", "Gói giải pháp dịch vụ chăm sóc sức khỏe ban đầu và tư vấn chuyên sâu toàn diện.", "#0284C7"),
            ("2. Giảm Thiểu Rủi Ro (Pain Relievers)", "Khắc phục triệt để rào cản địa lý, tiết kiệm chi phí đi lại và thời gian chờ đợi cho người dân.", "#38BDF8"),
            ("3. Yếu Tố Tạo Lợi Ích (Gain Creators)", "Nâng cao chất lượng sống, chẩn đoán phát hiện sớm nguy cơ bệnh và cải thiện chỉ số sức khỏe.", "#10B981")
        ]
        for idx, (stitle, sdesc, scolor) in enumerate(vm_subcards):
            sy = canvas_y + 48.0 + idx * (sub_h + sub_gap)
            sub_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 14, sy, side_w - 28, sub_h)
            sub_card.Fill.Solid()
            sub_card.Fill.ForeColor.RGB = hex_to_bgr("#111C3A" if self.theme == "DARK" else "#F1F5F9")
            sub_card.Line.Visible = msoTrue
            sub_card.Line.ForeColor.RGB = hex_to_bgr(scolor)
            sub_card.Line.Weight = 1.0
            left_shapes.append(sub_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 22, sy + 5, side_w - 44, sub_h - 10)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = stitle + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 14.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(scolor)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = sdesc
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 16.0.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            left_shapes.append(tb)

        val_map_group = safe_group(slide, left_shapes, "Value_Map_Group")
        shapes.append(val_map_group)

        # =========================================================
        # 2. CENTER NEXUS: ĐỒNG BỘ PHÙ HỢP (FIT CONNECTOR)
        # =========================================================
        center_shapes = []
        cx = left + side_w + (center_gap - 54.0) / 2.0
        cy = canvas_y + (canvas_h - 88.0) / 2.0
        fit_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy, 54.0, 88.0)
        fit_box.Fill.Solid()
        fit_box.Fill.ForeColor.RGB = hex_to_bgr("#1E293B")
        fit_box.Line.Visible = msoTrue
        fit_box.Line.ForeColor.RGB = hex_to_bgr(success)
        fit_box.Line.Weight = 2.0
        center_shapes.append(fit_box)

        ftb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 2, cy + 6, 50.0, 76.0)
        ftf = ftb.TextFrame
        ftf.WordWrap = msoTrue
        ftf.MarginLeft = 0
        ftf.MarginRight = 0
        ftr = ftf.TextRange
        ftr.Text = "◄ FIT ►\nĐỒNG\nBỘ"
        ftr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ftr.Font.Size = 16.0.5
        ftr.Font.Bold = msoTrue
        ftr.Font.Color.RGB = hex_to_bgr(success)
        ftr.ParagraphFormat.Alignment = ppAlignCenter
        center_shapes.append(ftb)

        fit_group = safe_group(slide, center_shapes, "Canvas_Fit_Group")
        shapes.append(fit_group)

        # =========================================================
        # 3. RIGHT CONTAINER: HỒ SƠ KHÁCH HÀNG (CUSTOMER PROFILE)
        # =========================================================
        right_shapes = []
        rx = left + side_w + center_gap
        cp_bg = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, canvas_y, side_w, canvas_h)
        cp_bg.Fill.Solid()
        cp_bg.Fill.ForeColor.RGB = hex_to_bgr(surface)
        cp_bg.Line.Visible = msoTrue
        cp_bg.Line.ForeColor.RGB = hex_to_bgr(accent)
        cp_bg.Line.Weight = 2.0
        right_shapes.append(cp_bg)

        # Customer Profile Header Badge
        cp_badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx + 14, canvas_y + 12, side_w - 28, 28)
        cp_badge.Fill.Solid()
        cp_badge.Fill.ForeColor.RGB = hex_to_bgr(accent)
        cp_badge.Line.Visible = msoFalse
        cpt = cp_badge.TextFrame.TextRange
        cpt.Text = "●  HỒ SƠ KHÁCH HÀNG (CUSTOMER PROFILE)"
        cpt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cpt.Font.Size = 15.0
        cpt.Font.Bold = msoTrue
        cpt.Font.Color.RGB = hex_to_bgr("#0F172A")
        cp_badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        right_shapes.append(cp_badge)

        # 3 Sub-Cards for Customer Profile
        cp_subcards = [
            ("1. Việc Cần Làm (Customer Jobs)", "Cần tiếp cận dịch vụ y tế an toàn, đáng tin cậy, bảo mật và thủ tục nhanh gọn.", "#10B981"),
            ("2. Nỗi Đau (Customer Pains)", "Lo ngại chi phí ngoài danh mục, thông tin truyền thông sai lệch và e ngại định kiến.", "#EF4444"),
            ("3. Lợi Ích Kỳ Vọng (Gains)", "Bảo vệ sức khỏe gia đình trọn vẹn, được tư vấn tận tâm và chất lượng dịch vụ bảo đảm.", "#F59E0B")
        ]
        for idx, (stitle, sdesc, scolor) in enumerate(cp_subcards):
            sy = canvas_y + 48.0 + idx * (sub_h + sub_gap)
            sub_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx + 14, sy, side_w - 28, sub_h)
            sub_card.Fill.Solid()
            sub_card.Fill.ForeColor.RGB = hex_to_bgr("#111C3A" if self.theme == "DARK" else "#F1F5F9")
            sub_card.Line.Visible = msoTrue
            sub_card.Line.ForeColor.RGB = hex_to_bgr(scolor)
            sub_card.Line.Weight = 1.0
            right_shapes.append(sub_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 22, sy + 5, side_w - 44, sub_h - 10)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = stitle + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 14.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(scolor)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = sdesc
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 16.0.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            right_shapes.append(tb)

        cust_group = safe_group(slide, right_shapes, "Customer_Profile_Group")
        shapes.append(cust_group)

        return shapes

    # 30. FRAMEWORK_CYNEFIN (Khung Ra Quyết Định Cynefin)
    def render_cynefin(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        qw = (width - 16.0) / 2.0
        qh = (height - 16.0) / 2.0

        quads = [
            (left, top, qw, qh, "RẮC RỐI (COMPLEX)\n\n• Thăm dò -> Cảm nhận -> Ứng phó\n• Thực tiễn mới xuất hiện (Emergent Practice)\n• Áp dụng: Nghiên cứu mô hình dân số mới & can thiệp thích ứng", "#3B82F6"),
            (left + qw + 16.0, top, qw, qh, "PHỨC TẠP (COMPLICATED)\n\n• Cảm nhận -> Phân tích -> Ứng phó\n• Thực tiễn tối ưu (Good Practice)\n• Áp dụng: Phân tích số liệu nhân khẩu học & chuyên môn y tế", "#10B981"),
            (left, top + qh + 16.0, qw, qh, "HỖN LOẠN (CHAOTIC)\n\n• Hành động -> Cảm nhận -> Ứng phó\n• Thực tiễn đổi mới đột phá (Novel Practice)\n• Áp dụng: Ứng phó dịch bệnh khẩn cấp & can thiệp đột xuất", "#EF4444"),
            (left + qw + 16.0, top + qh + 16.0, qw, qh, "RÕ RÀNG (CLEAR / SIMPLE)\n\n• Cảm nhận -> Phân loại -> Ứng phó\n• Thực tiễn tốt nhất (Best Practice)\n• Áp dụng: Quy trình cấp phát phương tiện tránh thai & phác đồ chuẩn", "#F59E0B")
        ]

        for qx, qy, qwidth, qheight, text, color in quads:
            q = slide.Shapes.AddShape(msoShapeRoundedRectangle, qx, qy, qwidth, qheight)
            q.Fill.Solid()
            q.Fill.ForeColor.RGB = hex_to_bgr(surface)
            q.Line.Visible = msoTrue
            q.Line.ForeColor.RGB = hex_to_bgr(color)
            q.Line.Weight = 2.0
            shapes.append(q)

            tr = q.TextFrame.TextRange
            tr.Text = text
            tr.Font.Size = 15.0
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 31. FRAMEWORK_BOW_TIE (Mô Hình Quản Lý Rủi Ro Nơ Bướm)
    def render_bow_tie(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        wing_w = width * 0.38
        knot_w = width * 0.20
        gap = 8.0

        # Left Wing (Threats & Preventive Barriers)
        lw = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, wing_w, height)
        lw.Fill.Solid()
        lw.Fill.ForeColor.RGB = hex_to_bgr(surface)
        lw.Line.Visible = msoTrue
        lw.Line.ForeColor.RGB = hex_to_bgr("#F59E0B")
        lw.Line.Weight = 2.0
        shapes.append(lw)
        atoms = spec.get("atoms", [])
        claim = spec.get("primary_claim", "Nội dung nhận diện rủi ro y tế dân số.")

        t_lw = lw.TextFrame.TextRange
        lw_items = [f"• {a.get('title', '')}: {a.get('text', '')}" if isinstance(a, dict) else f"• {str(a)}" for a in atoms[:2]] if atoms else [f"• Yếu tố nguy cơ: {claim}"]
        t_lw.Text = "NGUYÊN NHÂN & RÀO CHẮN PHÒNG NGỪA\n\n" + "\n".join(lw_items)
        t_lw.Font.Size = 14.5
        t_lw.Font.Color.RGB = hex_to_bgr(ink)

        # Center Knot (Top Critical Event)
        knot = slide.Shapes.AddShape(msoShapeOval, left + wing_w + gap, top + height * 0.15, knot_w, height * 0.70)
        knot.Fill.Solid()
        knot.Fill.ForeColor.RGB = hex_to_bgr("#DC2626")
        knot.Line.Visible = msoTrue
        knot.Line.ForeColor.RGB = hex_to_bgr("#F87171")
        knot.Line.Weight = 2.5
        shapes.append(knot)
        t_k = knot.TextFrame.TextRange
        t_k.Text = "SỰ CỐ TRỌNG YẾU\n(TOP EVENT)\n\nNguy Cơ\nSức Khỏe"
        t_k.Font.Size = 15.0
        t_k.Font.Bold = msoTrue
        t_k.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        t_k.ParagraphFormat.Alignment = ppAlignCenter

        # Right Wing (Mitigation Barriers & Consequences)
        rw = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + wing_w + knot_w + 2 * gap, top, wing_w, height)
        rw.Fill.Solid()
        rw.Fill.ForeColor.RGB = hex_to_bgr(surface)
        rw.Line.Visible = msoTrue
        rw.Line.ForeColor.RGB = hex_to_bgr("#10B981")
        rw.Line.Weight = 2.0
        shapes.append(rw)
        t_rw = rw.TextFrame.TextRange
        rw_items = [f"• {a.get('title', '')}: {a.get('text', '')}" if isinstance(a, dict) else f"• {str(a)}" for a in atoms[2:4]] if len(atoms) > 2 else [f"• Biện pháp can thiệp: Giám sát chủ động và điều trị kịp thời", f"• Kết quả bảo vệ: Nâng cao chất lượng dân số toàn diện"]
        t_rw.Text = "RÀO CHẮN GIẢM THIỂU & HẬU QUẢ\n\n" + "\n".join(rw_items)
        t_rw.Font.Size = 14.5
        t_rw.Font.Color.RGB = hex_to_bgr(ink)

        return shapes

    # 32. FRAMEWORK_BLUE_OCEAN_ERRC (Ma Trận Đại Dương Xanh ERRC)
    def render_blue_ocean_errc(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        qw = (width - 16.0) / 2.0
        qh = (height - 16.0) / 2.0

        atoms = spec.get("atoms", [])
        errc_labels = ["LOẠI BỎ (ELIMINATE)", "NÂNG CAO (RAISE)", "CẮT GIẢM (REDUCE)", "TẠO MỚI (CREATE)"]
        errc_colors = ["#EF4444", "#10B981", "#F59E0B", "#0284C7"]
        coords = [(left, top), (left + qw + 16.0, top), (left, top + qh + 16.0), (left + qw + 16.0, top + qh + 16.0)]
        quads = []
        if atoms:
            for i in range(4):
                a = atoms[i] if i < len(atoms) else {}
                t = a.get("title", f"Yếu Tố {i+1}") if isinstance(a, dict) else str(a)
                d = a.get("text") or a.get("desc") or "" if isinstance(a, dict) else ""
                cx, cy = coords[i]
                quads.append((cx, cy, qw, qh, f"{errc_labels[i]}\n\n• {t}\n• {d}" if d else f"{errc_labels[i]}\n\n• {t}", errc_colors[i]))
        else:
            claim = spec.get("primary_claim", "Chiến lược nâng cao chất lượng chuyên môn.")
            for i in range(4):
                cx, cy = coords[i]
                quads.append((cx, cy, qw, qh, f"{errc_labels[i]}\n\n• {claim}", errc_colors[i]))

        for qx, qy, qwidth, qheight, text, color in quads:
            q = slide.Shapes.AddShape(msoShapeRoundedRectangle, qx, qy, qwidth, qheight)
            q.Fill.Solid()
            q.Fill.ForeColor.RGB = hex_to_bgr(surface)
            q.Line.Visible = msoTrue
            q.Line.ForeColor.RGB = hex_to_bgr(color)
            q.Line.Weight = 2.0
            shapes.append(q)

            tr = q.TextFrame.TextRange
            tr.Text = text
            tr.Font.Size = 15.0
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 33. FRAMEWORK_NORTH_STAR_METRIC (Cây Chỉ Số Bắc Đẩu)
    def render_north_star_metric(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Top Star Node
        star_w = width * 0.55
        star_h = height * 0.32
        star_x = left + (width - star_w) / 2.0
        sn = slide.Shapes.AddShape(msoShapeRoundedRectangle, star_x, top, star_w, star_h)
        sn.Fill.Solid()
        sn.Fill.ForeColor.RGB = hex_to_bgr(brand)
        sn.Line.Visible = msoTrue
        sn.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        sn.Line.Weight = 2.5
        shapes.append(sn)
        atoms = spec.get("atoms", [])
        ns_title = spec.get("north_star_title") or spec.get("assertion_title", "CHỈ SỐ ĐỊNH HƯỚNG TRỌNG TÂM")
        claim = spec.get("primary_claim", "Nội dung chuẩn hóa chuyên môn.")

        t_sn = sn.TextFrame.TextRange
        t_sn.Text = f"★ CHỈ SỐ TRỌNG YẾU (CORE METRIC)\n\n{ns_title}"
        t_sn.Font.Size = 15.5
        t_sn.Font.Bold = msoTrue
        t_sn.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        t_sn.ParagraphFormat.Alignment = ppAlignCenter

        # 3 Driver Pillars Below
        card_w = (width - 32.0) / 3.0
        card_h = height * 0.60
        card_y = top + star_h + 18.0

        if spec.get("drivers"):
            drivers = spec["drivers"]
        elif atoms:
            drivers = []
            for i, a in enumerate(atoms[:3]):
                t = a.get("title", f"Trụ Cột 0{i+1}") if isinstance(a, dict) else f"Trụ Cột 0{i+1}"
                d = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                m = a.get("metric") or a.get("badge") or f"Chỉ Số 0{i+1}"
                drivers.append({"title": t, "metric": m, "desc": d})
        else:
            drivers = [
                {"title": f"YẾU TỐ 0{i+1}", "metric": "Chuẩn Hóa", "desc": claim}
                for i in range(3)
            ]

        for i, d in enumerate(drivers):
            cx = left + i * (card_w + 16.0)
            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, card_y, card_w, card_h)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(brand)
            c.Line.Weight = 1.5
            shapes.append(c)

            tr = c.TextFrame.TextRange
            tr.Text = f"{d['title']}\n\nChỉ số: {d['metric']}\n\n{d['desc']}"
            tr.Font.Size = 15.0
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 34. FRAMEWORK_GROW_COACHING (Mô Hình Huấn Luyện GROW)
    def render_grow_coaching(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        atoms = spec.get("atoms", [])
        colors = ["#0284C7", "#F59E0B", "#10B981", "#8B5CF6"]
        letters = ["G - MỤC TIÊU (GOAL)", "R - THỰC TRẠNG (REALITY)", "O - GIẢI PHÁP (OPTIONS)", "W - KẾ HOẠCH HÀNH ĐỘNG (WILL)"]
        if spec.get("steps"):
            steps = spec["steps"]
        elif atoms:
            steps = []
            for i, a in enumerate(atoms[:4]):
                t = a.get("title", f"Nội Dung 0{i+1}") if isinstance(a, dict) else str(a)
                d = a.get("text") or a.get("desc") or "" if isinstance(a, dict) else ""
                steps.append((f"{letters[i]}: {t}", d, colors[i % len(colors)]))
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa đào tạo.")
            steps = [
                (letters[i], claim, colors[i])
                for i in range(4)
            ]

        card_w = (width - 36.0) / 4.0
        for i, (title, desc, color) in enumerate(steps):
            cx = left + i * (card_w + 12.0)
            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, height)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(color)
            c.Line.Weight = 2.0
            shapes.append(c)

            tr = c.TextFrame.TextRange
            tr.Text = f"{title}\n\n{desc}"
            tr.Font.Size = 15.0
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 35. FRAMEWORK_PIRATE_AARRR (Phễu Tăng Trưởng Khởi Nghiệp AARRR)
    def render_pirate_aarrr(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        atoms = spec.get("atoms", [])
        colors = ["#0284C7", "#38BDF8", "#10B981", "#F59E0B", "#EC4899"]
        w_factors = [1.00, 0.88, 0.76, 0.64, 0.52]
        default_names = ["1. TIẾP CẬN (ACQUISITION)", "2. KÍCH HOẠT (ACTIVATION)", "3. DUY TRÌ (RETENTION)", "4. GIÁ TRỊ (REVENUE)", "5. LAN TỎA (REFERRAL)"]
        if spec.get("stages"):
            stages = spec["stages"]
        elif atoms:
            stages = []
            for i, a in enumerate(atoms[:5]):
                t = a.get("title", default_names[i]) if isinstance(a, dict) else str(a)
                d = a.get("text") or a.get("desc") or "" if isinstance(a, dict) else ""
                stages.append((f"{default_names[i]}: {t}", d, colors[i % len(colors)], w_factors[i % len(w_factors)]))
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa phễu phát triển.")
            stages = [
                (default_names[i], claim, colors[i], w_factors[i])
                for i in range(5)
            ]

        row_h = (height - 20.0) / len(stages)
        for i, (title, desc, color, w_factor) in enumerate(stages):
            ry = top + i * (row_h + 5.0)
            rw = width * w_factor
            rx = left + (width - rw) / 2.0

            s = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rw, row_h)
            s.Fill.Solid()
            s.Fill.ForeColor.RGB = hex_to_bgr(surface)
            s.Line.Visible = msoTrue
            s.Line.ForeColor.RGB = hex_to_bgr(color)
            s.Line.Weight = 2.0
            shapes.append(s)

            tr = s.TextFrame.TextRange
            tr.Text = f"{title}: {desc}"
            tr.Font.Size = 14.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

