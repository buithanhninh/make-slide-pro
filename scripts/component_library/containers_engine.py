"""
containers_engine.py
Advanced Visual Containers & Layout Engine for Make Slide Pro V8.4.0.
Implements 7 elite keynote containers (Apple Keynote, Pitch.com, Stripe)
using 100% Native Vector Shapes.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

# Win32 Constants
msoShapeRectangle = 1
msoShapeRoundedRectangle = 5
msoShapeOval = 9
msoShapeChevron = 55
msoShapeRightArrow = 13
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


class AdvancedContainersEngine:
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}

    def _get_token(self, category: str, key: str, fallback: str) -> str:
        return self.tokens.get(category, {}).get(key, fallback)

    # -------------------------------------------------------------
    # 1. ASYMMETRICAL APPLE-STYLE BENTO GRID (4 Khối Bất Đối Xứng)
    # -------------------------------------------------------------
    def render_bento_complex(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        atoms = spec.get("atoms", [
            {"title": "Trọng Tâm Đột Phá", "text": "Hệ thống tự động hóa toàn diện quy trình xử lý dữ liệu và thiết kế bài giảng thông minh.", "badge": "TIÊU ĐIỂM"},
            {"title": "Tốc Độ Xử Lý", "text": "Xử lý tức thời trong dưới 25 giây cho toàn bộ bài học 20 slide.", "badge": "TỐC ĐỘ"},
            {"title": "Độ Chính Xác 100%", "text": "Bảo toàn số liệu thống kê qua 16 tác tử kiểm định chất lượng nghiêm ngặt.", "badge": "BẢO MẬT"},
            {"title": "Chỉ Số Hiệu Năng", "text": "98.5% người dùng đánh giá bài giảng xuất sắc.", "badge": "HIỆU NĂNG"}
        ])

        hero_w = width * 0.56
        sub_w = width * 0.41
        gap_x = width * 0.03
        right_left = left + hero_w + gap_x

        bot_strip_h = 75.0
        main_h = height - bot_strip_h - 12.0

        # 1. Hero Left Card (Spanning full main height)
        hero_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, hero_w, main_h)
        hero_card.Fill.Solid()
        hero_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        hero_card.Line.Visible = msoTrue
        hero_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        hero_card.Line.Weight = 2.0
        shapes.append(hero_card)

        # Hero Badge
        h_pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 18, top + 16, 95, 20)
        h_pill.Fill.Solid()
        h_pill.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "badge_bg", "#082F49"))
        h_pill.Line.Visible = msoFalse
        pt = h_pill.TextFrame.TextRange
        pt.Text = atoms[0].get("badge", "TIÊU ĐIỂM")
        pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        pt.Font.Size = 9.5
        pt.Font.Bold = msoTrue
        pt.Font.Color.RGB = hex_to_bgr(brand)
        pt.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(h_pill)

        # Hero Content
        htb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 18, top + 48, hero_w - 36, main_h - 60)
        htf = htb.TextFrame
        htf.WordWrap = msoTrue
        hp1 = htf.TextRange.Paragraphs(1)
        hp1.Text = atoms[0].get("title", "Luận Điểm Trọng Yếu") + "\n"
        hp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        hp1.Font.Size = 18
        hp1.Font.Bold = msoTrue
        hp1.Font.Color.RGB = hex_to_bgr(ink)
        hp1.ParagraphFormat.SpaceAfter = 8

        hp2 = htf.TextRange.Paragraphs(2)
        hp2.Text = atoms[0].get("text", "")
        hp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        hp2.Font.Size = 13.5
        hp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(htb)

        # 2. Right Two Stacked Cards
        sub_h = (main_h - 12.0) / 2.0
        for i in range(1, 3):
            cur_top = top + (i - 1) * (sub_h + 12.0)
            a_data = atoms[i] if i < len(atoms) else {"title": f"Yếu Tố {i}", "text": "Mô tả chi tiết"}
            rcard = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left, cur_top, sub_w, sub_h)
            rcard.Fill.Solid()
            rcard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            rcard.Line.Visible = msoTrue
            rcard.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(rcard)

            rtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, right_left + 14, cur_top + 10, sub_w - 28, sub_h - 20)
            rtf = rtb.TextFrame
            rtf.WordWrap = msoTrue
            rp1 = rtf.TextRange.Paragraphs(1)
            rp1.Text = a_data.get("title", "") + "\n"
            rp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            rp1.Font.Size = 13
            rp1.Font.Bold = msoTrue
            rp1.Font.Color.RGB = hex_to_bgr(brand)
            rp1.ParagraphFormat.SpaceAfter = 4

            rp2 = rtf.TextRange.Paragraphs(2)
            rp2.Text = a_data.get("text", "")
            rp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            rp2.Font.Size = 11.5
            rp2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(rtb)

        # 3. Bottom Full-Width Horizontal Metric Strip
        bot_top = top + main_h + 12.0
        bot_strip = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, bot_top, width, bot_strip_h)
        bot_strip.Fill.Solid()
        bot_strip.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E2E8F0")
        bot_strip.Line.Visible = msoFalse
        shapes.append(bot_strip)

        last_atom = atoms[3] if len(atoms) > 3 else atoms[-1]
        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, bot_top + 14, width - 40, bot_strip_h - 28)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        bp1 = btf.TextRange.Paragraphs(1)
        bp1.Text = f"★ {last_atom.get('title', 'TỔNG KẾT')}: {last_atom.get('text', '')}"
        bp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp1.Font.Size = 12
        bp1.Font.Bold = msoTrue
        bp1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
        shapes.append(btb)

        return shapes

    # -------------------------------------------------------------
    # 2. STAT CALLOUT CARDS WITH DELTA CHIP (Chỉ Số Lớn + Chip Tăng Trưởng)
    # -------------------------------------------------------------
    def render_kpi_stat_delta(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        kpi_list = spec.get("kpi_stats", [
            {"metric": "100.3 Tr", "delta": "+0.84% YoY", "is_positive": True, "label": "Quy Mô Dân Số", "desc": "Cột mốc lịch sử đạt 100 triệu người"},
            {"metric": "1.96", "delta": "-7.1% vs Chuẩn", "is_positive": False, "label": "Mức Sinh (TFR)", "desc": "Dưới mức sinh thay thế 2.10 con"},
            {"metric": "42.5%", "delta": "+1.8% YoY", "is_positive": True, "label": "Tỷ Lệ Đô Thị Hóa", "desc": "Động lực phát triển kinh tế vùng"}
        ])

        count = len(kpi_list)
        gap = 16.0
        card_w = (width - (gap * (count - 1))) / count

        for idx, k in enumerate(kpi_list):
            cx = left + idx * (card_w + gap)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            card.Line.Weight = 2.0 if idx == 0 else 1.0
            shapes.append(card)

            # Giant Metric
            mtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 16, top + 20, card_w - 32, 60)
            mt = mtb.TextFrame.TextRange
            mt.Text = k["metric"]
            mt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            mt.Font.Size = 38
            mt.Font.Bold = msoTrue
            mt.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else ink)
            shapes.append(mtb)

            # Delta Chip Badge
            is_pos = k.get("is_positive", True)
            chip_bg = ("#064E3B", "#10B981") if is_pos else ("#7F1D1D", "#EF4444")
            if self.theme == "LIGHT":
                chip_bg = ("#DCFCE7", "#15803D") if is_pos else ("#FEE2E2", "#DC2626")

            chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 16, top + 88, 110, 22)
            chip.Fill.Solid()
            chip.Fill.ForeColor.RGB = hex_to_bgr(chip_bg[0])
            chip.Line.Visible = msoFalse
            ct = chip.TextFrame.TextRange
            icon_arrow = "▲ " if is_pos else "▼ "
            ct.Text = icon_arrow + k["delta"]
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 9.5
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(chip_bg[1])
            ct.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(chip)

            # Label & Description
            ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 16, top + 120, card_w - 32, height - 135)
            ltf = ltb.TextFrame
            ltf.WordWrap = msoTrue
            lp1 = ltf.TextRange.Paragraphs(1)
            lp1.Text = k["label"] + "\n"
            lp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            lp1.Font.Size = 15
            lp1.Font.Bold = msoTrue
            lp1.Font.Color.RGB = hex_to_bgr(ink)
            lp1.ParagraphFormat.SpaceAfter = 6

            lp2 = ltf.TextRange.Paragraphs(2)
            lp2.Text = k["desc"]
            lp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            lp2.Font.Size = 12
            lp2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            shapes.append(ltb)

        return shapes

    # -------------------------------------------------------------
    # 3. BEFORE VS. AFTER CONTRAST SPLIT (Thực Trạng vs. Giải Pháp)
    # -------------------------------------------------------------
    def render_before_after(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        gap = 18.0
        col_w = (width - gap) / 2.0

        data = spec.get("contrast_data", {})
        before_title = data.get("before_title", "HIỆN TRẠNG & THÁCH THỨC")
        before_items = data.get("before_items", [
            "Dữ liệu phân tán ở nhiều phòng ban, thiếu tính đồng bộ",
            "Báo cáo thủ công mất từ 5-7 ngày làm việc",
            "Mô hình dự báo đơn biến, sai số biến động cao"
        ])
        after_title = data.get("after_title", "MỤC TIÊU & GIẢI PHÁP ĐỘT PHÁ")
        after_items = data.get("after_items", [
            "Kiến trúc dữ liệu hồ dữ liệu tập trung (Single Source of Truth)",
            "Tự động hóa xuất báo cáo phân tích theo thời gian thực",
            "Thuật toán AI đa biến nâng độ chính xác dự báo lên 98.5%"
        ])

        # Left: Before (Muted/Red tint)
        b_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, col_w, height)
        b_card.Fill.Solid()
        b_card.Fill.ForeColor.RGB = hex_to_bgr("#1E1E2E" if self.theme == "DARK" else "#F1F5F9")
        b_card.Line.Visible = msoTrue
        b_card.Line.ForeColor.RGB = hex_to_bgr("#EF4444" if self.theme == "DARK" else "#DC2626")
        b_card.Line.Weight = 1.5
        shapes.append(b_card)

        # Before Header
        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 18, top + 16, col_w - 36, height - 32)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        bp1 = btf.TextRange.Paragraphs(1)
        bp1.Text = "✕ " + before_title + "\n\n"
        bp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp1.Font.Size = 14
        bp1.Font.Bold = msoTrue
        bp1.Font.Color.RGB = hex_to_bgr("#EF4444" if self.theme == "DARK" else "#DC2626")

        bp2 = btf.TextRange.Paragraphs(2)
        bp2.Text = "\n\n".join([f"• {it}" for it in before_items])
        bp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp2.Font.Size = 12
        bp2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
        shapes.append(btb)

        # Right: After (Brand/Green tint)
        ax = left + col_w + gap
        a_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, ax, top, col_w, height)
        a_card.Fill.Solid()
        a_card.Fill.ForeColor.RGB = hex_to_bgr("#064E3B" if self.theme == "DARK" else "#DCFCE7")
        a_card.Line.Visible = msoTrue
        a_card.Line.ForeColor.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#15803D")
        a_card.Line.Weight = 2.0
        shapes.append(a_card)

        atb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, ax + 18, top + 16, col_w - 36, height - 32)
        atf = atb.TextFrame
        atf.WordWrap = msoTrue
        ap1 = atf.TextRange.Paragraphs(1)
        ap1.Text = "✓ " + after_title + "\n\n"
        ap1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ap1.Font.Size = 14
        ap1.Font.Bold = msoTrue
        ap1.Font.Color.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#15803D")

        ap2 = atf.TextRange.Paragraphs(2)
        ap2.Text = "\n\n".join([f"✔ {it}" for it in after_items])
        ap2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ap2.Font.Size = 12
        ap2.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
        shapes.append(atb)

        return shapes

    # -------------------------------------------------------------
    # 4. EXECUTIVE PULL QUOTE BANNER (Khối Trích Dẫn Phong Cách Báo Chí)
    # -------------------------------------------------------------
    def render_executive_quote(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        data = spec.get("quote_data", {})
        quote_text = data.get("quote", "Dân số không chỉ là những con số thống kê cơ học, mà là động lực tối thượng quyết định sự thịnh suy kinh tế và vị thế quốc gia trên trường quốc tế trong thế kỷ 21.")
        author_name = data.get("author", "GS. TS. Nguyễn Văn A")
        author_title = data.get("title", "Chủ tịch Hội đồng Khoa học Dân số & Phát triển Bền vững")

        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr(brand)
        card.Line.Weight = 2.0
        shapes.append(card)

        # Huge Decorative Quotation Marks
        q_mark = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 28, top + 10, 80, 70)
        qt = q_mark.TextFrame.TextRange
        qt.Text = "“"
        qt.Font.Name = "Georgia"
        qt.Font.Size = 72
        qt.Font.Bold = msoTrue
        qt.Font.Color.RGB = hex_to_bgr(brand)
        shapes.append(q_mark)

        # Quote Body Text
        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 100, top + 36, width - 130, height - 100)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = f'"{quote_text}"\n\n'
        p1.Font.Name = "Georgia"
        p1.Font.Italic = msoTrue
        p1.Font.Size = 17
        p1.Font.Color.RGB = hex_to_bgr(ink)
        p1.ParagraphFormat.LineRuleWithin = msoTrue
        p1.ParagraphFormat.SpaceWithin = 1.3

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = f"— {author_name.upper()}  |  {author_title}"
        p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p2.Font.Size = 12
        p2.Font.Bold = msoTrue
        p2.Font.Color.RGB = hex_to_bgr(brand)
        shapes.append(tb)

        return shapes

    # -------------------------------------------------------------
    # 5. VERTICAL TIMELINE WITH GLOWING NODES (Dòng Thời Gian Dọc)
    # -------------------------------------------------------------
    def render_timeline_flow(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        milestones = spec.get("timeline_milestones", [
            {"year": "NĂM 1979", "title": "Tổng Điều Tra Toàn Quốc Lần 1", "desc": "Quy mô 52.7 triệu dân, thời kỳ tái thiết đất nước sau chiến tranh"},
            {"year": "NĂM 1999", "title": "Bắt Đầu Cơ Cấu Dân Số Vàng", "desc": "Quy mô 76.3 triệu dân, tỷ suất sinh giảm mạnh xuống mức 2.33"},
            {"year": "NĂM 2019", "title": "Chạm Mốc 96.2 Triệu Người", "desc": "Bắt đầu tiến trình già hóa dân số với tốc độ nhanh nhất thế giới"},
            {"year": "NĂM 2024+", "title": "Vượt Ngưỡng 100 Triệu Dân", "desc": "Quy mô đứng thứ 15 thế giới, chuyển dịch sang nâng cao chất lượng dân số"}
        ])

        count = len(milestones)
        row_h = (height - (10.0 * (count - 1))) / count
        node_x = left + 90.0

        # Central Vertical Line
        line = slide.Shapes.AddShape(msoShapeRectangle, node_x + 9, top + 10, 4, height - 20)
        line.Fill.Solid()
        line.Fill.ForeColor.RGB = hex_to_bgr(brand)
        line.Line.Visible = msoFalse
        shapes.append(line)

        for i, m in enumerate(milestones):
            my = top + i * (row_h + 10.0)

            # Year Label on Left
            ytb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left, my + (row_h / 2.0) - 12, 80, 24)
            yt = ytb.TextFrame.TextRange
            yt.Text = m["year"]
            yt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            yt.Font.Size = 11
            yt.Font.Bold = msoTrue
            yt.Font.Color.RGB = hex_to_bgr(brand)
            yt.ParagraphFormat.Alignment = ppAlignRight
            shapes.append(ytb)

            # Glowing Node (Circle)
            node = slide.Shapes.AddShape(msoShapeOval, node_x, my + (row_h / 2.0) - 11, 22, 22)
            node.Fill.Solid()
            node.Fill.ForeColor.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else brand)
            node.Line.Visible = msoTrue
            node.Line.ForeColor.RGB = hex_to_bgr(brand)
            node.Line.Weight = 3.0
            shapes.append(node)

            # Detail Card on Right
            card_x = node_x + 36.0
            card_w = width - (card_x - left)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, card_x, my, card_w, row_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, card_x + 12, my + 6, card_w - 24, row_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = m["title"] + "  —  "
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = m["desc"]
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11
            p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
            shapes.append(tb)

        return shapes

    # -------------------------------------------------------------
    # 6. MULTI-STEP CHEVRON PROCESS ARROW (Quy Trình Mũi Tên Vát)
    # -------------------------------------------------------------
    def render_process_chevron(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        steps = spec.get("process_steps", [
            {"step": "01. THU THẬP", "desc": "Dữ liệu tổng điều tra & hộ tịch điện tử"},
            {"step": "02. LÀM SẠCH", "desc": "Loại bỏ trùng lặp và chuẩn hóa trường thông tin"},
            {"step": "03. MÔ HÌNH HÓA", "desc": "Áp dụng thuật toán thành phần Cohort"},
            {"step": "04. DỰ BÁO", "desc": "Xuất kịch bản biến động 10 năm"},
            {"step": "05. HOẠCH ĐỊNH", "desc": "Tích hợp chính sách phát triển bền vững"}
        ])

        count = len(steps)
        ch_w = (width - 20.0) / count
        COLORS = ["#0284C7", "#0369A1", "#075985", "#0C4A6E", "#082F49"] if self.theme == "DARK" else ["#0284C7", "#0D9488", "#10B981", "#059669", "#047857"]

        for i, s_data in enumerate(steps):
            cx = left + i * ch_w
            chev = slide.Shapes.AddShape(msoShapeChevron, cx, top, ch_w + 14, height)
            chev.Fill.Solid()
            chev.Fill.ForeColor.RGB = hex_to_bgr(COLORS[i % len(COLORS)])
            chev.Line.Visible = msoTrue
            chev.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#CBD5E1")
            chev.Line.Weight = 1.0
            shapes.append(chev)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 18, top + (height / 2.0) - 30, ch_w - 24, 60)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = s_data["step"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = s_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0")
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # -------------------------------------------------------------
    # 7. PILLAR ARCHITECTURE WITH ACCENT BORDERS (Cột Trụ Độc Lập)
    # -------------------------------------------------------------
    def render_pillar_3d(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        border = self._get_token("colors", "card_border", "#1E293B")

        pillars = spec.get("pillars", [
            {"title": "Trụ Cột Kinh Tế", "sub": "Tận dụng tối đa Dư lợi Dân số vàng để bứt phá thu nhập bình quân", "kpi": "GDP +6.8%"},
            {"title": "Trụ Cột Xã Hội", "sub": "Mở rộng bao phủ an sinh và bảo hiểm y tế toàn dân ứng phó già hóa", "kpi": "BHYT 95%"},
            {"title": "Trụ Cột Thể Chế", "sub": "Hoàn thiện pháp luật và chính sách dân số đồng bộ với chiến lược số", "kpi": "100% Số Hóa"}
        ])

        count = len(pillars)
        gap = 16.0
        col_w = (width - (gap * (count - 1))) / count

        for idx, p in enumerate(pillars):
            px = left + idx * (col_w + gap)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            card.Line.Weight = 2.0 if idx == 0 else 1.0
            shapes.append(card)

            # Top Accent Color Bar
            top_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, top, col_w, 6)
            top_bar.Fill.Solid()
            top_bar.Fill.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else ("#0D9488" if idx == 1 else "#10B981"))
            top_bar.Line.Visible = msoFalse
            shapes.append(top_bar)

            # Text inside Pillar
            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 16, top + 18, col_w - 32, height - 36)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"TRỤ CỘT 0{idx + 1}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.SpaceAfter = 4

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p["title"] + "\n\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = p.get("sub", "") + "\n\n"
            p3.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p3.Font.Size = 12
            p3.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))

            p4 = tf.TextRange.Paragraphs(4)
            p4.Text = f"Mục Tiêu: {p.get('kpi', '')}"
            p4.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p4.Font.Size = 13
            p4.Font.Bold = msoTrue
            p4.Font.Color.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#059669")
            shapes.append(tb)

        return shapes

    # =============================================================
    # 8. CONTAINER_BENTO_GRID_3X3 (Lưới Bento Modular 9 Ô Đồng Đều)
    # =============================================================
    def render_bento_grid_3x3(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        items = spec.get("grid_items", [
            {"num": "01", "title": "Phân Tích AI", "desc": "Mô hình xử lý ngôn ngữ"},
            {"num": "02", "title": "Native Table", "desc": "Bảng biểu Excel nhúng"},
            {"num": "03", "title": "Vector 2D/3D", "desc": "Hình khối PowerPoint gốc"},
            {"num": "04", "title": "MACC Council", "desc": "16 Tác tử kiểm định QA"},
            {"num": "05", "title": "Auto Styling", "desc": "Dark/Light Luxury Theme"},
            {"num": "06", "title": "Xuất Bản 4K", "desc": "Độ phân giải siêu nét"},
            {"num": "07", "title": "Tối Ưu Tốc Độ", "desc": "Xử lý dưới 25 giây"},
            {"num": "08", "title": "Bảo Mật Cao", "desc": "Mã hóa tiêu chuẩn SOC2"},
            {"num": "09", "title": "Tích Hợp API", "desc": "Sẵn sàng scale đa kênh"}
        ])

        cols, rows = 3, 3
        gap = 10.0
        cell_w = (width - (cols - 1) * gap) / cols
        cell_h = (height - (rows - 1) * gap) / rows

        for idx, itm in enumerate(items[:9]):
            r = idx // cols
            c = idx % cols
            cx = left + c * (cell_w + gap)
            cy = top + r * (cell_h + gap)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy, cell_w, cell_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 4 else border)
            card.Line.Weight = 1.5 if idx == 4 else 1.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 8, cy + 6, cell_w - 16, cell_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{itm.get('num', '')} | {itm.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = itm.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 8.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 9. CONTAINER_PILLAR_4_COLUMNS (Bộ 4 Cột Trụ Doanh Nghiệp)
    # =============================================================
    def render_pillar_4_columns(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        pillars = spec.get("pillars", [
            {"num": "TRỤ CỘT 01", "title": "Chiến Lược Số", "desc": "Định vị sản phẩm dẫn đầu thị trường.", "kpi": "Tăng trưởng +45%"},
            {"num": "TRỤ CỘT 02", "title": "Xuất Sắc Vận Hành", "desc": "Tự động hóa 90% quy trình thủ công.", "kpi": "Tiết kiệm 3.2 Tỷ"},
            {"num": "TRỤ CỘT 03", "title": "Khách Hàng Trọng Tâm", "desc": "Nâng cao chỉ số hài lòng toàn diện.", "kpi": "NPS 88 Điểm"},
            {"num": "TRỤ CỘT 04", "title": "Đổi Mới Văn Hóa", "desc": "Đào tạo nhân sự làm chủ công nghệ AI.", "kpi": "100% Nhân Sự"}
        ])

        gap = 12.0
        col_w = (width - 3 * gap) / 4.0

        for i, p in enumerate(pillars[:4]):
            px = left + i * (col_w + gap)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 10, top + 15, col_w - 20, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = p.get("num", f"0{i+1}") + "\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p.get("title", "") + "\n\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 12
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = p.get("desc", "") + "\n\n"
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 9.5
            p3.Font.Color.RGB = hex_to_bgr(muted)

            p4 = tf.TextRange.Paragraphs(4)
            p4.Text = f"★ {p.get('kpi', '')}"
            p4.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p4.Font.Size = 10.5
            p4.Font.Bold = msoTrue
            p4.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "success", "#10B981"))
            shapes.append(tb)

        return shapes

    # =============================================================
    # 10. CONTAINER_PROBLEM_SOL_3STEP (Chuỗi Vấn Đề - Hệ Quả - Giải Pháp)
    # =============================================================
    def render_problem_sol_3step(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        danger = self._get_token("colors", "danger", "#EF4444")
        warning = self._get_token("colors", "warning", "#F59E0B")
        success = self._get_token("colors", "success", "#10B981")

        steps = [
            {"tag": "BƯỚC 1: VẤN ĐỀ CỐT LÕI", "title": "Dữ Liệu Bị Phân Mảnh", "desc": "Hơn 5 nguồn dữ liệu độc lập không đồng bộ, gây chậm trễ báo cáo hàng tuần.", "color": danger},
            {"tag": "BƯỚC 2: HỆ QUẢ NGHIÊM TRỌNG", "title": "Tổn Thất Chi Phí Vận Hành", "desc": "Mất 14 giờ lao động mỗi tuần cho xử lý thủ công, tỷ lệ sai sót lên tới 8.5%.", "color": warning},
            {"tag": "BƯỚC 3: GIẢI PHÁP ĐỘT PHÁ", "title": "Tự Động Hóa Với Make Slide Pro", "desc": "Hợp nhất toàn bộ dữ liệu vào 1 pipeline, sinh slide chuẩn quốc tế tức thì.", "color": success}
        ]

        gap = 14.0
        col_w = (width - 2 * gap) / 3.0

        for i, s in enumerate(steps):
            sx = left + i * (col_w + gap)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(s["color"])
            card.Line.Weight = 2.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 12, top + 15, col_w - 24, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = s["tag"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(s["color"])

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = s["title"] + "\n\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 13
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = s["desc"]
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 10
            p3.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 11. CONTAINER_TARGET_BULLSEYE (Khối Bia Bắn Mục Tiêu Bullseye)
    # =============================================================
    def render_target_bullseye(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        danger = self._get_token("colors", "danger", "#EF4444")

        cx = left + width * 0.32
        cy = top + height / 2.0
        max_r = min(width * 0.3, height * 0.45)

        # 3 Concentric Target Rings
        radii = [max_r, max_r * 0.68, max_r * 0.36]
        colors = [surface, brand, danger]

        for i in range(3):
            r = radii[i]
            ring = slide.Shapes.AddShape(msoShapeOval, cx - r, cy - r, r * 2, r * 2)
            ring.Fill.Solid()
            ring.Fill.ForeColor.RGB = hex_to_bgr(colors[i])
            ring.Line.Visible = msoTrue
            ring.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
            ring.Line.Weight = 2.0
            shapes.append(ring)

        # Explanatory Cards on Right
        rx = left + width * 0.65
        rw = width * 0.35
        levels = [
            {"name": "HỒNG TÂM (CORE)", "target": "Khách Hàng Doanh Nghiệp Lớn", "desc": "Đem lại 70% ARR"},
            {"name": "VÒNG TRONG (INNER)", "target": "Khối Cơ Quan & Giáo Dục", "desc": "Quy mô 25% thị trường"},
            {"name": "VÒNG NGOÀI (OUTER)", "target": "Người Dùng Cá Nhân Pro", "desc": "Kênh lan tỏa thương hiệu"}
        ]

        card_h = (height - 20.0) / 3.0
        for i, lv in enumerate(levels):
            cy_card = top + i * (card_h + 10.0)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, cy_card, rw, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(colors[2 - i])
            card.Line.Weight = 1.5
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, cy_card + 6, rw - 20, card_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{lv.get('name', '')}: {lv.get('target', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(colors[2 - i])

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = lv.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 12. CONTAINER_BALANCE_SEESAW (Cán Cân Cân Bằng Seesaw Scale)
    # =============================================================
    def render_balance_seesaw(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        danger = self._get_token("colors", "danger", "#EF4444")
        success = self._get_token("colors", "success", "#10B981")

        side_w = (width - 40.0) / 2.0

        # Left Pan (Cost / Investment)
        l_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + 20, side_w, height - 40)
        l_card.Fill.Solid()
        l_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        l_card.Line.Visible = msoTrue
        l_card.Line.ForeColor.RGB = hex_to_bgr(danger)
        l_card.Line.Weight = 2.0
        shapes.append(l_card)

        ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 15, top + 35, side_w - 30, height - 70)
        ltf = ltb.TextFrame
        ltf.WordWrap = msoTrue
        lp1 = ltf.TextRange.Paragraphs(1)
        lp1.Text = "CHI PHÍ ĐẦU TƯ BAN ĐẦU\n\n"
        lp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        lp1.Font.Size = 12
        lp1.Font.Bold = msoTrue
        lp1.Font.Color.RGB = hex_to_bgr(danger)

        lp2 = ltf.TextRange.Paragraphs(2)
        lp2.Text = "• Chi phí bản quyền hệ thống AI\n• Thời gian đào tạo chuyển giao 2 tuần\n• Thiết lập hạ tầng Sandbox thử nghiệm\n• Ngân sách dự phòng rủi ro 10%"
        lp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        lp2.Font.Size = 10
        lp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(ltb)

        # Right Pan (Value / ROI)
        rx = left + side_w + 40.0
        r_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top + 20, side_w, height - 40)
        r_card.Fill.Solid()
        r_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        r_card.Line.Visible = msoTrue
        r_card.Line.ForeColor.RGB = hex_to_bgr(success)
        r_card.Line.Weight = 2.0
        shapes.append(r_card)

        rtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 15, top + 35, side_w - 30, height - 70)
        rtf = rtb.TextFrame
        rtf.WordWrap = msoTrue
        rp1 = rtf.TextRange.Paragraphs(1)
        rp1.Text = "GIÁ TRỊ THU HỒI VƯỢT TRỘI (ROI)\n\n"
        rp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        rp1.Font.Size = 12
        rp1.Font.Bold = msoTrue
        rp1.Font.Color.RGB = hex_to_bgr(success)

        rp2 = rtf.TextRange.Paragraphs(2)
        rp2.Text = "• Hoàn vốn sau 3.5 tháng vận hành\n• Giảm 75% chi phí thuê ngoài thiết kế\n• Tốc độ phát hành tài liệu tăng gấp 10 lần\n• Chuẩn hóa 100% tài sản trí tuệ doanh nghiệp"
        rp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        rp2.Font.Size = 10
        rp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(rtb)

        return shapes

    # =============================================================
    # 13. CONTAINER_GAUGE_METER_DIAL (Đồng Hồ Đo Áp Suất / Mức Rủi Ro)
    # =============================================================
    def render_gauge_meter_dial(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        success = self._get_token("colors", "success", "#10B981")
        warning = self._get_token("colors", "warning", "#F59E0B")
        danger = self._get_token("colors", "danger", "#EF4444")

        # 3 Speedometer Zones
        zone_w = (width - 24.0) / 3.0
        zones = [
            {"zone": "VÙNG AN TOÀN", "range": "0 - 30%", "status": "RỦI RO THẤP", "desc": "Hệ thống vận hành trơn tru, tài nguyên dư thừa dồi dào.", "color": success},
            {"zone": "VÙNG CẢNH BÁO", "range": "31 - 70%", "status": "MỨC TRUNG BÌNH", "desc": "Cần theo dõi ngưỡng tải đỉnh điểm vào cuối tháng.", "color": warning},
            {"zone": "VÙNG NGUY HIỂM", "range": "71 - 100%", "status": "BÁO ĐỘNG ĐỎ", "desc": "Cần kích hoạt cơ chế tự động mở rộng khẩn cấp.", "color": danger}
        ]

        for i, z in enumerate(zones):
            zx = left + i * (zone_w + 12.0)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, zx, top, zone_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(z["color"])
            card.Line.Weight = 2.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, zx + 10, top + 15, zone_w - 20, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{z['zone']}\n{z['range']}\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 13
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(z["color"])
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"[{z['status']}]\n\n{z['desc']}"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # =============================================================
    # 14. CONTAINER_GLASSMORPHIC_HERO (Khối Kính Mờ Frosted Glass)
    # =============================================================
    def render_glassmorphic_hero(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr(brand)
        card.Line.Weight = 2.5
        shapes.append(card)

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 25, top + 25, width - 50, height - 50)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = spec.get("hero_title", "ĐỘT PHÁ CÔNG NGHỆ BÀI GIẢNG 2026") + "\n\n"
        p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p1.Font.Size = 18
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(brand)

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = spec.get("hero_body", "Make Slide Pro đại diện cho chuẩn mực thiết kế bài thuyết trình tương lai. Với kiến trúc 16 Tác tử AI và bộ thư viện 110+ Archetypes gốc, từng slide trở thành một tác phẩm nghệ thuật chuẩn mực quốc tế.")
        p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        p2.Font.Size = 11.5
        p2.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(tb)

        return shapes

    # =============================================================
    # 15. CONTAINER_HERO_SPLIT_CARDS (Bố Cục Tách Đôi Khối Trọng Tâm)
    # =============================================================
    def render_hero_split_cards(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        half_w = (width - 16.0) / 2.0

        # Left Hero Card (50%)
        l_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, half_w, height)
        l_card.Fill.Solid()
        l_card.Fill.ForeColor.RGB = hex_to_bgr(brand)
        l_card.Line.Visible = msoFalse
        shapes.append(l_card)

        ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 18, top + 25, half_w - 36, height - 50)
        ltf = ltb.TextFrame
        ltf.WordWrap = msoTrue
        lp1 = ltf.TextRange.Paragraphs(1)
        lp1.Text = "TRỌNG TÂM CHIẾN LƯỢC\n\n"
        lp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        lp1.Font.Size = 14
        lp1.Font.Bold = msoTrue
        lp1.Font.Color.RGB = hex_to_bgr("#FFFFFF")

        lp2 = ltf.TextRange.Paragraphs(2)
        lp2.Text = "Tập trung 100% nguồn lực vào nghiên cứu thuật toán sinh bố cục tối ưu, nâng tầm trải nghiệm người dùng lên tiêu chuẩn Fortune 500."
        lp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        lp2.Font.Size = 11
        lp2.Font.Color.RGB = hex_to_bgr("#F0FDF4")
        shapes.append(ltb)

        # Right 3 Sub-Cards
        rx = left + half_w + 16.0
        sub_h = (height - 20.0) / 3.0
        sub_items = [
            {"title": "Mô Hình Dữ Liệu", "desc": "100% Bảng biểu & Biểu đồ gốc có thể chỉnh sửa trực tiếp."},
            {"title": "Tính Năng Co Giãn", "desc": "Tự động cân đối tỷ lệ từ 2 đến 8 phần tử linh hoạt."},
            {"title": "Kiểm Định Tự Động", "desc": "Bộ quy chuẩn 34 tiêu chí chất lượng nghiêm ngặt."}
        ]

        for i, s in enumerate(sub_items):
            sy = top + i * (sub_h + 10.0)
            scard = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, sy, half_w, sub_h)
            scard.Fill.Solid()
            scard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            scard.Line.Visible = msoTrue
            scard.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(scard)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, sy + 6, half_w - 20, sub_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"✓ {s.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = s.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 16. CONTAINER_DIAGONAL_SPLIT (Bố Cục Vát Chéo Năng Động)
    # =============================================================
    def render_diagonal_split(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        half_w = (width - 20.0) / 2.0

        c1 = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, half_w, height)
        c1.Fill.Solid()
        c1.Fill.ForeColor.RGB = hex_to_bgr(surface)
        c1.Line.Visible = msoTrue
        c1.Line.ForeColor.RGB = hex_to_bgr(brand)
        shapes.append(c1)

        tb1 = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 15, top + 20, half_w - 30, height - 40)
        tf1 = tb1.TextFrame
        tf1.WordWrap = msoTrue
        tp1 = tf1.TextRange
        tp1.Text = "PHẦN 1: TƯ DUY NỀN TẢNG\n\nXây dựng tư duy hệ thống và thấu hiểu nguyên lý phân bổ thị giác là chìa khóa then chốt giúp các nhà lãnh đạo truyền đạt thông điệp thuyết phục."
        tp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        tp1.Font.Size = 11
        tp1.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(tb1)

        c2 = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + half_w + 20.0, top, half_w, height)
        c2.Fill.Solid()
        c2.Fill.ForeColor.RGB = hex_to_bgr(brand)
        c2.Line.Visible = msoFalse
        shapes.append(c2)

        tb2 = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + half_w + 35.0, top + 20, half_w - 30, height - 40)
        tf2 = tb2.TextFrame
        tf2.WordWrap = msoTrue
        tp2 = tf2.TextRange
        tp2.Text = "PHẦN 2: THỰC THI ĐỘT PHÁ\n\nChuyển hóa chiến lược thành hành động với tốc độ thần tốc, bảo đảm mọi chi tiết kỹ thuật đều hoàn hảo khi đưa vào vận hành thực tế."
        tp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        tp2.Font.Size = 11
        tp2.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        shapes.append(tb2)

        return shapes

    # =============================================================
    # 17. CONTAINER_NOTIFICATION_TAGS (Thẻ Dịch Vụ Có Huy Hiệu Ribbon)
    # =============================================================
    def render_notification_tags(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        cards = [
            {"badge": "MỚI NHẤT", "title": "Engine Sinh Vector", "desc": "110+ mô hình hình học hoàn chỉnh."},
            {"badge": "ĐỀ XUẤT", "title": "Bảng Biểu Chuẩn P&L", "desc": "Hỗ trợ sửa số liệu Excel trực tiếp."},
            {"badge": "NÂNG CAO", "title": "16 Tác Tử MACC", "desc": "Tự động kiểm định chất lượng 4K."}
        ]

        col_w = (width - 2 * 14.0) / 3.0
        for i, c in enumerate(cards):
            cx = left + i * (col_w + 14.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if i == 1 else border)
            card.Line.Weight = 2.0 if i == 1 else 1.0
            shapes.append(card)

            # Badge pill
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 12, top + 12, 85, 22)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(brand)
            pill.Line.Visible = msoFalse
            shapes.append(pill)

            ptf = pill.TextFrame
            pt = ptf.TextRange
            pt.Text = c["badge"]
            pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            pt.Font.Size = 9.0
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            pt.ParagraphFormat.Alignment = ppAlignCenter

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 12, top + 45, col_w - 24, height - 55)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = c["title"] + "\n\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = c["desc"]
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 10
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 18. CONTAINER_CUSTOMER_JOURNEY (Bản Đồ Hành Trình Khách Hàng)
    # =============================================================
    def render_customer_journey(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        stages = [
            {"stage": "NHẬN BIẾT", "mood": "🙂 Tò Mò", "touchpoint": "Quảng cáo, Mạng Xã Hội", "action": "Tìm kiếm giải pháp"},
            {"stage": "CÂN NHẮC", "mood": "🤔 Đắn Đo", "touchpoint": "Website, Bảng Giá", "action": "So sánh tính năng"},
            {"stage": "MUA HÀNG", "mood": "😃 Hài Lòng", "touchpoint": "Cổng Thanh Toán", "action": "Kích hoạt tài khoản"},
            {"stage": "SỬ DỤNG", "mood": "🤩 Ấn Tượng", "touchpoint": "PowerPoint Add-in", "action": "Sinh slide tự động"},
            {"stage": "TRUNG THÀNH", "mood": "❤️ Tận Tụy", "touchpoint": "Cộng Đồng, Hỗ Trợ", "action": "Giới thiệu bạn bè"}
        ]

        count = len(stages)
        col_w = (width - (count - 1) * 8.0) / count

        for i, st in enumerate(stages):
            sx = left + i * (col_w + 8.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 8, top + 10, col_w - 16, height - 20)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"CHẶNG 0{i+1}\n{st['stage']}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"\nCảm Xúc:\n{st['mood']}\n\nĐiểm Chạm:\n{st['touchpoint']}\n\nHành Động:\n{st['action']}"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 8.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 19. CONTAINER_ISOMETRIC_STACK (Chồng Thẻ 3D Xếp Lớp Chiều Sâu)
    # =============================================================
    def render_isometric_stack(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        layers = [
            {"tier": "TẦNG 1: DỮ LIỆU ĐẦU VÀO", "desc": "Giáo án thô, tài liệu phân tích, ghi chú họp."},
            {"tier": "TẦNG 2: XỬ LÝ TRÍ TUỆ NHÂN TẠO", "desc": "Tách ý chính, xây dựng cấu trúc luận điểm khoa học."},
            {"tier": "TẦNG 3: XUẤT BẢN THỊ GIÁC ĐỈNH CAO", "desc": "Mô hình đồ họa PowerPoint 100% vector nguyên bản."}
        ]

        card_h = (height - 30.0) / 3.0
        for i, lyr in enumerate(layers):
            offset_x = i * 25.0
            card_y = top + i * (card_h + 10.0)
            card_w = width - 50.0

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + offset_x, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(brand if i == 2 else surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 2.0 if i == 2 else 1.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + offset_x + 15, card_y + 8, card_w - 30, card_h - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = lyr["tier"] + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if i == 2 else brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = lyr["desc"]
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0" if i == 2 else muted)
            shapes.append(tb)

        return shapes

    # =============================================================
    # 20. CONTAINER_TABBED_OVERVIEW (Giao Diện Tab Điều Hướng Ảo)
    # =============================================================
    def render_tabbed_overview(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        tabs = ["TAB 1: TỔNG QUAN", "TAB 2: THÔNG SỐ", "TAB 3: TRIỂN KHAI"]
        tab_w = width / 3.0

        for i, t in enumerate(tabs):
            tab_btn = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + i * tab_w, top, tab_w - 4.0, 32.0)
            tab_btn.Fill.Solid()
            tab_btn.Fill.ForeColor.RGB = hex_to_bgr(brand if i == 0 else surface)
            tab_btn.Line.Visible = msoTrue
            tab_btn.Line.ForeColor.RGB = hex_to_bgr(brand if i == 0 else border)
            shapes.append(tab_btn)

            ttf = tab_btn.TextFrame
            tp = ttf.TextRange
            tp.Text = t
            tp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            tp.Font.Size = 10
            tp.Font.Bold = msoTrue
            tp.Font.Color.RGB = hex_to_bgr("#FFFFFF" if i == 0 else muted)
            tp.ParagraphFormat.Alignment = ppAlignCenter

        content_y = top + 38.0
        content_h = height - 38.0
        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, content_y, width, content_h)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr(brand)
        card.Line.Weight = 1.5
        shapes.append(card)

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, content_y + 20, width - 40, content_h - 40)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = "NỘI DUNG CHI TIẾT TAB HIỆN TẠI (ĐANG KÍCH HOẠT)\n\n"
        p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p1.Font.Size = 13
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(brand)

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = "Kiến trúc tab điều hướng ảo cho phép tối ưu không gian trình bày, phân bổ thông tin thành từng lớp logic mạch lạc giúp người nghe dễ dàng theo dõi theo từng giai đoạn triển khai dự án."
        p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        p2.Font.Size = 11
        p2.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(tb)

        return shapes

    # =============================================================
    # 21. CONTAINER_EXECUTIVE_DASHBOARD (Bảng Điều Khiển Tổng Giám Đốc)
    # =============================================================
    def render_executive_dashboard(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        # Top Banner (Headline Claim)
        banner_h = 55.0
        banner = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, banner_h)
        banner.Fill.Solid()
        banner.Fill.ForeColor.RGB = hex_to_bgr(surface)
        banner.Line.Visible = msoTrue
        banner.Line.ForeColor.RGB = hex_to_bgr(brand)
        shapes.append(banner)

        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 15, top + 8, width - 30, banner_h - 16)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        bp = btf.TextRange
        bp.Text = "★ BÁO CÁO ĐIỀU HÀNH TỔNG THỂ: TĂNG TRƯỞNG VƯỢT KỲ VỌNG 135% TOÀN CÔNG TY"
        bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp.Font.Size = 11.5
        bp.Font.Bold = msoTrue
        bp.Font.Color.RGB = hex_to_bgr(brand)
        bp.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(btb)

        # 3 KPI Stat Cards below banner
        card_y = top + banner_h + 12.0
        card_h = height - banner_h - 12.0
        card_w = (width - 2 * 12.0) / 3.0

        kpis = [
            {"val": "24.8 Tỷ", "label": "Tổng Doanh Thu ARR", "delta": "+42% YoY"},
            {"val": "128,000", "label": "Khách Hàng Hoạt Động", "delta": "+85% MAU"},
            {"val": "99.98%", "label": "Độ Ổn Định Hạ Tầng", "delta": "SLA Đạt Chuẩn"}
        ]

        for i, k in enumerate(kpis):
            kx = left + i * (card_w + 12.0)
            k_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, kx, card_y, card_w, card_h)
            k_card.Fill.Solid()
            k_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            k_card.Line.Visible = msoTrue
            k_card.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(k_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, kx + 10, card_y + 15, card_w - 20, card_h - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = k["val"] + "\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 22
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = k["label"] + "\n\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = f"▲ {k['delta']}"
            p3.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p3.Font.Size = 11
            p3.Font.Bold = msoTrue
            p3.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "success", "#10B981"))
            p3.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # =============================================================
    # 22. CONTAINER_CLOSING_CTA_HERO (Thẻ Kêu Gọi Hành Động Khép Lại)
    # =============================================================
    def render_closing_cta_hero(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        box = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        box.Fill.Solid()
        box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        box.Line.Visible = msoTrue
        box.Line.ForeColor.RGB = hex_to_bgr(brand)
        box.Line.Weight = 2.5
        shapes.append(box)

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 30, top + 25, width - 60, height - 100)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = spec.get("cta_headline", "SẴN SÀNG CHUYỂN ĐỔI BÀI GIẢNG SỐ NGAY HÔM NAY?") + "\n\n"
        p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p1.Font.Size = 16
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(brand)
        p1.ParagraphFormat.Alignment = ppAlignCenter

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = spec.get("cta_sub", "Liên hệ ngay với đội ngũ chuyên gia của chúng tôi để nhận bản dùng thử miễn phí và hỗ trợ triển khai hệ thống toàn diện trong 24 giờ.")
        p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        p2.Font.Size = 11
        p2.Font.Color.RGB = hex_to_bgr(muted)
        p2.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(tb)

        # Action Button
        btn_w, btn_h = 240.0, 42.0
        btn_x = left + (width - btn_w) / 2.0
        btn_y = top + height - btn_h - 25.0

        btn = slide.Shapes.AddShape(msoShapeRoundedRectangle, btn_x, btn_y, btn_w, btn_h)
        btn.Fill.Solid()
        btn.Fill.ForeColor.RGB = hex_to_bgr(brand)
        btn.Line.Visible = msoFalse
        shapes.append(btn)

        btf = btn.TextFrame
        bp = btf.TextRange
        bp.Text = spec.get("cta_btn", "ĐĂNG KÝ TRẢI NGHIỆM NGAY →")
        bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp.Font.Size = 11
        bp.Font.Bold = msoTrue
        bp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        bp.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 23. CONTAINER_DEVICE_MOCKUP_FRAME (Khung Viền Màn Hình Thiết Bị)
    def render_device_mockup_frame(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Outer Laptop/Monitor Bezel Frame
        outer = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height * 0.88)
        outer.Fill.Solid()
        outer.Fill.ForeColor.RGB = hex_to_bgr("#1E293B")
        outer.Line.Visible = msoTrue
        outer.Line.ForeColor.RGB = hex_to_bgr("#475569")
        outer.Line.Weight = 2.0
        shapes.append(outer)

        # Inner Screen Glass Area
        pad = 12.0
        screen = slide.Shapes.AddShape(msoShapeRectangle, left + pad, top + pad + 14.0, width - 2 * pad, height * 0.88 - 2 * pad - 14.0)
        screen.Fill.Solid()
        screen.Fill.ForeColor.RGB = hex_to_bgr(surface)
        screen.Line.Visible = msoFalse
        shapes.append(screen)

        tr = screen.TextFrame.TextRange
        tr.Text = f"GIAO DIỆN MAKE SLIDE PRO V8.6\n\n{spec.get('mockup_text', '165+ Archetypes Chuẩn Quốc Tế & Hệ Thống Chuyển Động Apple Morph Motion')}"
        tr.Font.Size = 12.0
        tr.Font.Bold = msoTrue
        tr.Font.Color.RGB = hex_to_bgr(brand)
        tr.ParagraphFormat.Alignment = ppAlignCenter

        # Laptop Base / Stand Below
        base_w = width * 0.40
        base_h = height * 0.08
        base_x = left + (width - base_w) / 2.0
        base_y = top + height * 0.88 + 4.0
        base = slide.Shapes.AddShape(msoShapeRoundedRectangle, base_x, base_y, base_w, base_h)
        base.Fill.Solid()
        base.Fill.ForeColor.RGB = hex_to_bgr("#334155")
        base.Line.Visible = msoFalse
        shapes.append(base)

        return shapes

    # 24. CONTAINER_METRIC_MARQUEE_BANNER (Dải Banner 4 Chỉ Số Nổi Bật)
    def render_metric_marquee_banner(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Background Banner Stripe
        stripe = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        stripe.Fill.Solid()
        stripe.Fill.ForeColor.RGB = hex_to_bgr("#082F49")
        stripe.Line.Visible = msoTrue
        stripe.Line.ForeColor.RGB = hex_to_bgr(brand)
        stripe.Line.Weight = 2.0
        shapes.append(stripe)

        stats = spec.get("marquee_stats", [
            {"val": "165+", "label": "Archetypes Toàn Cầu"},
            {"val": "100%", "label": "Native & Excel Embedded"},
            {"val": "0.85s", "label": "Apple Morph Motion"},
            {"val": "48/48", "label": "Tests Pass Tuyệt Đối"}
        ])

        col_w = width / len(stats)
        for i, st in enumerate(stats):
            cx = left + i * col_w
            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 10, top + 15, col_w - 20, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{st['val']}\n"
            p1.Font.Size = 28.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#38BDF8")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = st['label']
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 25. CONTAINER_THREE_PILLARS_CARDS (Bộ 3 Thẻ Kính Mờ Nâng Cao)
    def render_three_pillars_cards(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        pillars = [
            ("TRỤ CỘT 1: THƯ VIỆN KHỔNG LỒ", "165+ Archetypes bao phủ 6 phân hệ chuyên sâu từ tư vấn đến kiến trúc hệ thống", "#0284C7"),
            ("TRỤ CỘT 2: KHẢ NĂNG CHỈNH SỬA", "100% Native PowerPoint Tables và Office Charts nhúng Excel trực tiếp", "#10B981"),
            ("TRỤ CỘT 3: CHUYỂN ĐỘNG APPLE", "Chuyển tiếp Morph ma thuật và xuất hiện so le thác nước Staggered", "#8B5CF6")
        ]

        card_w = (width - 32.0) / 3.0
        for i, (p_title, p_desc, color) in enumerate(pillars):
            cx = left + i * (card_w + 16.0)

            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, height)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(color)
            c.Line.Weight = 2.0
            shapes.append(c)

            # Top accent bar
            bar = slide.Shapes.AddShape(msoShapeRectangle, cx + 15, top + 15, card_w - 30, 4.0)
            bar.Fill.Solid()
            bar.Fill.ForeColor.RGB = hex_to_bgr(color)
            bar.Line.Visible = msoFalse
            shapes.append(bar)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 15, top + 35, card_w - 30, height - 50)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{p_title}\n\n"
            p1.Font.Size = 12.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(color)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p_desc
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 26. CONTAINER_PROBLEM_SOLUTION_IMPACT (Bộ 3 Thẻ Dẫn Dắt Câu Chuyện)
    def render_problem_solution_impact(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        cards = [
            ("1. NỖI ĐAU (PROBLEM)", "Slide xuất ra bị cứng nhắc, bảng biểu là ảnh tĩnh không sửa được, thiếu hiệu ứng chuyển động đẳng cấp.", "#EF4444"),
            ("2. GIẢI PHÁP (SOLUTION)", "Kho Mega 165+ Archetypes, 100% Native COM, tích hợp công nghệ Apple Morph Motion ma thuật.", "#0284C7"),
            ("3. TÁC ĐỘNG (IMPACT)", "Tiết kiệm 90% thời gian biên soạn, thuyết phục tuyệt đối hội đồng thẩm định và các nhà đầu tư.", "#10B981")
        ]

        card_w = (width - 32.0) / 3.0
        for i, (title, desc, color) in enumerate(cards):
            cx = left + i * (card_w + 16.0)

            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, height)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(color)
            c.Line.Weight = 2.0
            shapes.append(c)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 15, top + 25, card_w - 30, height - 50)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{title}\n\n"
            p1.Font.Size = 12.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(color)
            p1.ParagraphFormat.Alignment = ppAlignLeft

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = desc
            p2.Font.Size = 11.0
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignLeft
            shapes.append(tb)

        return shapes

    # 27. CONTAINER_FEATURE_HEX_CLUSTER (Cụm 7 Khối Lục Giác Liên Kết)
    def render_feature_hex_cluster(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Center Hexagon Core
        hex_w = width * 0.22
        hex_h = height * 0.38
        cx = left + (width - hex_w) / 2.0
        cy = top + (height - hex_h) / 2.0

        core = slide.Shapes.AddShape(msoShapeHexagon, cx, cy, hex_w, hex_h)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Visible = msoTrue
        core.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        core.Line.Weight = 2.0
        shapes.append(core)
        tr = core.TextFrame.TextRange
        tr.Text = "MAKE SLIDE PRO\nV8.6 CORE"
        tr.Font.Size = 10.5
        tr.Font.Bold = msoTrue
        tr.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        tr.ParagraphFormat.Alignment = ppAlignCenter

        # 6 Outer Hexagons
        import math
        center_x = left + width / 2.0
        center_y = top + height / 2.0
        orbit_r = min(width, height) * 0.36
        features = ["165+ Mẫu", "100% Native", "Excel Nhúng", "Apple Morph", "16 Tác Tử", "Zero P0"]

        for i, feat in enumerate(features):
            angle = i * (2 * math.pi / 6)
            hx = center_x + orbit_r * math.cos(angle) - hex_w / 2.0
            hy = center_y + orbit_r * math.sin(angle) - hex_h / 2.0

            h = slide.Shapes.AddShape(msoShapeHexagon, hx, hy, hex_w, hex_h)
            h.Fill.Solid()
            h.Fill.ForeColor.RGB = hex_to_bgr(surface)
            h.Line.Visible = msoTrue
            h.Line.ForeColor.RGB = hex_to_bgr(brand)
            h.Line.Weight = 1.5
            shapes.append(h)

            htr = h.TextFrame.TextRange
            htr.Text = feat
            htr.Font.Size = 10.0
            htr.Font.Bold = msoTrue
            htr.Font.Color.RGB = hex_to_bgr(ink)
            htr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 28. CONTAINER_TESTIMONIAL_CAROUSEL_ROW (Hàng 3 Thẻ Nhận Xét Khách Hàng)
    def render_testimonial_carousel_row(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        reviews = [
            ("★★★★★", "\"Kho 165+ Archetypes và khả năng sửa Excel trực tiếp đã thay đổi hoàn toàn cách chúng tôi làm slide tư vấn cho khách hàng.\"", "Giám Đốc Chiến Lược, Big 4 Consulting"),
            ("★★★★★", "\"Hiệu ứng chuyển cảnh Apple Morph mượt mà ngoài sức tưởng tượng. Thuyết trình trước hội đồng đầu tư thành công rực rỡ!\"", "CEO & Founder, YC Backed Startup"),
            ("★★★★★", "\"Hệ thống kiểm toán 16 tác tử MACC bảo đảm tính chính xác dữ liệu 100%. Không bao giờ gặp lỗi vỡ hình hay lệch tỷ lệ.\"", "Trưởng Ban Chuyển Đổi Số, Tập Đoàn FinTech")
        ]

        card_w = (width - 32.0) / 3.0
        for i, (stars, quote, author) in enumerate(reviews):
            cx = left + i * (card_w + 16.0)

            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, height)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(brand)
            c.Line.Weight = 1.5
            shapes.append(c)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 15, top + 20, card_w - 30, height - 40)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{stars}\n\n"
            p1.Font.Size = 14.0
            p1.Font.Color.RGB = hex_to_bgr("#F59E0B")
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"{quote}\n\n"
            p2.Font.Size = 10.5
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = author
            p3.Font.Size = 9.5
            p3.Font.Bold = msoTrue
            p3.Font.Color.RGB = hex_to_bgr("#38BDF8")
            p3.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 29. CONTAINER_STAT_HERO_SPLIT_60_40 (Chia Đôi 60% Chỉ Số Lớn + 40% Giải Trình)
    def render_stat_hero_split_60_40(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        left_w = width * 0.58
        right_w = width * 0.38
        gap = width * 0.04

        # Left 60%: Giant Number Hero Card
        left_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, left_w, height)
        left_card.Fill.Solid()
        left_card.Fill.ForeColor.RGB = hex_to_bgr("#082F49")
        left_card.Line.Visible = msoTrue
        left_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        left_card.Line.Weight = 2.5
        shapes.append(left_card)

        tb_l = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, top + 35, left_w - 40, height - 70)
        tf_l = tb_l.TextFrame
        tf_l.WordWrap = msoTrue
        p1 = tf_l.TextRange.Paragraphs(1)
        p1.Text = "165+\n"
        p1.Font.Size = 56.0
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr("#38BDF8")
        p1.ParagraphFormat.Alignment = ppAlignCenter

        p2 = tf_l.TextRange.Paragraphs(2)
        p2.Text = "ARCHETYPES CHUẨN THẾ GIỚI\nĐẦY ĐỦ TRÊN 6 PHÂN HỆ"
        p2.Font.Size = 13.0
        p2.Font.Bold = msoTrue
        p2.Font.Color.RGB = hex_to_bgr(ink)
        p2.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(tb_l)

        # Right 40%: Detail Explanations
        right_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + left_w + gap, top, right_w, height)
        right_card.Fill.Solid()
        right_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        right_card.Line.Visible = msoTrue
        right_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        right_card.Line.Weight = 1.5
        shapes.append(right_card)

        tb_r = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + left_w + gap + 15, top + 25, right_w - 30, height - 50)
        tf_r = tb_r.TextFrame
        tf_r.WordWrap = msoTrue
        rp = tf_r.TextRange
        rp.Text = "Ý NGHĨA ĐỐI VỚI DOANH NGHIỆP:\n\n• Đa dạng hóa 100% hình thái biểu diễn\n• Phục vụ toàn diện mọi nhu cầu từ kinh doanh đến công nghệ\n• Tương thích hoàn hảo với hệ thống chuyển động Apple Morph\n• Tự động co giãn tham số linh hoạt từ 2 đến 8 hạng mục"
        rp.Font.Size = 11.0
        rp.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(tb_r)

        return shapes

    # 30. CONTAINER_MINIMALIST_APPLE_QUOTE (Khối Trích Dẫn Phong Cách Tối Giản Apple)
    def render_minimalist_apple_quote(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Sleek Minimal Glass Card
        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        card.Line.Weight = 1.5
        shapes.append(card)

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 40, top + 40, width - 80, height - 80)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue

        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = spec.get("quote_text", "“Thiết kế không chỉ là vẻ bề ngoài hay cảm giác khi nhìn vào. Thiết kế là cách mà mọi thứ vận hành một cách hoàn hảo và liền mạch.”\n\n")
        p1.Font.Name = self._get_token("fonts", "primary", "Georgia")
        p1.Font.Size = 16.0
        p1.Font.Italic = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(ink)
        p1.ParagraphFormat.Alignment = ppAlignCenter

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = spec.get("quote_author", "— STEVE JOBS | TRIẾT LÝ THIẾT KẾ APPLE KEYNOTE")
        p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p2.Font.Size = 11.0
        p2.Font.Bold = msoTrue
        p2.Font.Color.RGB = hex_to_bgr(brand)
        p2.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(tb)

        return shapes


