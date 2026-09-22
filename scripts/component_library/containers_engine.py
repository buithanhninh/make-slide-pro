"""
containers_engine.py
Advanced Visual Containers & Layout Engine for Make Slide Pro V8.4.0.
Implements 7 elite keynote containers (Apple Keynote, Pitch.com, Stripe)
using 100% Native Vector Shapes.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

from .utils import safe_group, add_vector_connector

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

        # Hero Badge
        h_pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 18, top + 16, 95, 22)
        h_pill.Fill.Solid()
        h_pill.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "badge_bg", "#082F49"))
        h_pill.Line.Visible = msoFalse
        pt = h_pill.TextFrame.TextRange
        pt.Text = atoms[0].get("badge", "TIÊU ĐIỂM")
        pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        pt.Font.Size = 10.0
        pt.Font.Bold = msoTrue
        pt.Font.Color.RGB = hex_to_bgr(brand)
        pt.ParagraphFormat.Alignment = ppAlignCenter

        # Hero Content
        htb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 18, top + 48, hero_w - 36, main_h - 60)
        htf = htb.TextFrame
        htf.WordWrap = msoTrue
        hp1 = htf.TextRange.Paragraphs(1)
        hp1.Text = atoms[0].get("title", "Luận Điểm Trọng Yếu") + "\n"
        hp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        hp1.Font.Size = 20.0
        hp1.Font.Bold = msoTrue
        hp1.Font.Color.RGB = hex_to_bgr(ink)
        hp1.ParagraphFormat.SpaceAfter = 10

        hp2 = htf.TextRange.Paragraphs(2)
        hp2.Text = atoms[0].get("text", "")
        hp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        hp2.Font.Size = 14.0
        hp2.Font.Color.RGB = hex_to_bgr(muted)
        hp2.ParagraphFormat.LineRuleWithin = msoTrue
        hp2.ParagraphFormat.SpaceWithin = 1.25

        # Group Hero Card 1 atomically so text is permanently locked on top of background
        hero_grp = safe_group(slide, [hero_card, h_pill, htb], "Bento_Hero_Card")
        shapes.append(hero_grp)

        # 2. Right Two Stacked Cards
        sub_h = (main_h - 12.0) / 2.0
        for i in range(1, 3):
            sub_shapes = []
            cur_top = top + (i - 1) * (sub_h + 12.0)
            a_data = atoms[i] if i < len(atoms) else {"title": f"Yếu Tố {i}", "text": "Mô tả chi tiết"}
            rcard = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left, cur_top, sub_w, sub_h)
            rcard.Fill.Solid()
            rcard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            rcard.Line.Visible = msoTrue
            rcard.Line.ForeColor.RGB = hex_to_bgr(border)
            sub_shapes.append(rcard)

            rtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, right_left + 16, cur_top + 12, sub_w - 32, sub_h - 24)
            rtf = rtb.TextFrame
            rtf.WordWrap = msoTrue
            rp1 = rtf.TextRange.Paragraphs(1)
            rp1.Text = a_data.get("title", "") + "\n"
            rp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            rp1.Font.Size = 14.5
            rp1.Font.Bold = msoTrue
            rp1.Font.Color.RGB = hex_to_bgr(brand)
            rp1.ParagraphFormat.SpaceAfter = 6

            rp2 = rtf.TextRange.Paragraphs(2)
            rp2.Text = a_data.get("text", "")
            rp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            rp2.Font.Size = 12.5
            rp2.Font.Color.RGB = hex_to_bgr(muted)
            rp2.ParagraphFormat.LineRuleWithin = msoTrue
            rp2.ParagraphFormat.SpaceWithin = 1.2
            sub_shapes.append(rtb)

            rcard_grp = safe_group(slide, sub_shapes, f"Bento_Sub_Card_{i}")
            shapes.append(rcard_grp)

        # 3. Bottom Full-Width Horizontal Metric Strip
        bot_top = top + main_h + 12.0
        bot_strip = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, bot_top, width, bot_strip_h)
        bot_strip.Fill.Solid()
        bot_strip.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E2E8F0")
        bot_strip.Line.Visible = msoFalse

        last_atom = atoms[3] if len(atoms) > 3 else atoms[-1]
        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, bot_top + 14, width - 40, bot_strip_h - 28)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        bp1 = btf.TextRange.Paragraphs(1)
        bp1.Text = f"★ {last_atom.get('title', 'TỔNG KẾT')}: {last_atom.get('text', '')}"
        bp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp1.Font.Size = 13.0
        bp1.Font.Bold = msoTrue
        bp1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")

        bot_grp = safe_group(slide, [bot_strip, btb], "Bento_Bottom_Strip")
        shapes.append(bot_grp)

        return shapes

    # -------------------------------------------------------------
    # 2. STAT CALLOUT CARDS WITH DELTA CHIP (Chỉ Số Lớn + Chip Tăng Trưởng)
    # -------------------------------------------------------------
    def render_kpi_stat_delta(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        kpi_list = spec.get("kpi_stats")
        if not kpi_list:
            atoms = spec.get("atoms", [])
            if atoms:
                kpi_list = []
                for idx, a in enumerate(atoms[:4]):
                    kpi_list.append({
                        "metric": a.get("metric", f"0{idx+1}"),
                        "delta": a.get("delta", "Mục Tiêu 2030"),
                        "is_positive": True,
                        "label": a.get("title", f"Chỉ Số 0{idx+1}"),
                        "desc": a.get("text", "")
                    })
            else:
                kpi_list = [
                    {"metric": "100.3 Tr", "delta": "+0.84% YoY", "is_positive": True, "label": "Quy Mô Dân Số", "desc": "Cột mốc lịch sử đạt 100 triệu người"},
                    {"metric": "1.96", "delta": "-7.1% vs Chuẩn", "is_positive": False, "label": "Mức Sinh (TFR)", "desc": "Dưới mức sinh thay thế 2.10 con"},
                    {"metric": "42.5%", "delta": "+1.8% YoY", "is_positive": True, "label": "Tỷ Lệ Đô Thị Hóa", "desc": "Động lực phát triển kinh tế vùng"}
                ]

        count = len(kpi_list)
        gap = 14.0
        card_w = (width - (gap * (count - 1))) / count

        for idx, k in enumerate(kpi_list):
            cx = left + idx * (card_w + gap)
            card_shapes = []

            # 1. Card Container
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            card.Line.Weight = 2.0 if idx == 0 else 1.0
            card_shapes.append(card)

            # 2. Giant Metric (Top Tier)
            mtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 16, top + 16, card_w - 32, 54)
            mt = mtb.TextFrame.TextRange
            mt.Text = k["metric"]
            mt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            mt.Font.Size = 34 if count > 3 else 38
            mt.Font.Bold = msoTrue
            mt.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else ink)
            mt.ParagraphFormat.Alignment = ppAlignLeft
            card_shapes.append(mtb)

            # 3. Delta Chip Badge
            is_pos = k.get("is_positive", True)
            chip_bg = ("#064E3B", "#10B981") if is_pos else ("#7F1D1D", "#EF4444")
            if self.theme == "LIGHT":
                chip_bg = ("#DCFCE7", "#15803D") if is_pos else ("#FEE2E2", "#DC2626")

            chip_w = min(120.0, card_w - 32.0)
            chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 16, top + 74, chip_w, 22)
            chip.Fill.Solid()
            chip.Fill.ForeColor.RGB = hex_to_bgr(chip_bg[0])
            chip.Line.Visible = msoFalse
            ct = chip.TextFrame.TextRange
            icon_arrow = "▲ " if is_pos else "▼ "
            ct.Text = icon_arrow + k.get("delta", "Mục tiêu")
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 10.0
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(chip_bg[1])
            ct.ParagraphFormat.Alignment = ppAlignCenter
            card_shapes.append(chip)

            # 4. Body Content Tier (Label & Description)
            content_top = top + 104.0
            content_h = height - 150.0
            ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 16, content_top, card_w - 32, content_h)
            ltf = ltb.TextFrame
            ltf.WordWrap = msoTrue
            ltf.MarginLeft = 0
            ltf.MarginTop = 0

            lp1 = ltf.TextRange.Paragraphs(1)
            lp1.Text = k["label"] + "\n"
            lp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            lp1.Font.Size = 15.0
            lp1.Font.Bold = msoTrue
            lp1.Font.Color.RGB = hex_to_bgr(ink)
            lp1.ParagraphFormat.SpaceAfter = 6

            lp2 = ltf.TextRange.Paragraphs(2)
            lp2.Text = k["desc"]
            lp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            lp2.Font.Size = 12.5
            lp2.Font.Color.RGB = hex_to_bgr(muted)
            lp2.ParagraphFormat.LineRuleWithin = msoTrue
            lp2.ParagraphFormat.SpaceWithin = 1.3
            card_shapes.append(ltb)

            # 5. Bottom Anchor Tier (Zero Dead Space Anchor)
            badge_y = top + height - 36.0
            badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 16, badge_y, card_w - 32, 22)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E2E8F0")
            badge.Line.Visible = msoTrue
            badge.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            badge.Line.Weight = 1.0
            bt = badge.TextFrame.TextRange
            bt.Text = "◈ Chỉ Tiêu Đến 2030"
            bt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bt.Font.Size = 10.0
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr(brand if idx == 0 else muted)
            bt.ParagraphFormat.Alignment = ppAlignCenter
            card_shapes.append(badge)

            # Atomic group for 100% synchronized presenter clicks
            card_grp = safe_group(slide, card_shapes, f"KPI_StatCard_{idx+1}")
            shapes.append(card_grp)

        return shapes

    # -------------------------------------------------------------
    # 3. BEFORE VS. AFTER CONTRAST SPLIT (Thực Trạng vs. Giải Pháp)
    # -------------------------------------------------------------
    def render_before_after(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        gap = 24.0
        col_w = (width - gap) / 2.0

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        font_name = self._get_token("fonts", "primary", "Segoe UI")

        data = spec.get("contrast_data", {})
        atoms = spec.get("atoms", [])

        # Default rich comparative criteria if none or sparse
        def_before_items = [
            "Hình Thái Vật Chất: Tồn tại dưới dạng vật thể rõ ràng, có kích thước, khối lượng, hình dáng, màu sắc và bao bì cụ thể.",
            "Kiểm Định Chất Lượng: Khách hàng có thể quan sát, cầm nắm, cân đong đo đếm và kiểm tra tính năng kỹ thuật trước khi mua.",
            "Quyền Sở Hữu & Tồn Trữ: Được chuyển giao quyền sở hữu hoàn toàn sau giao dịch; có thể lưu trữ trong kho bãi qua nhiều thời kỳ."
        ]
        def_after_items = [
            "Bản Chất Phi Vật Thể: Không có hình thái vật lý, là chuỗi hoạt động chuyển giao đồng thời giữa người cung ứng và thụ hưởng.",
            "Kiểm Định Qua Trải Nghiệm: Chỉ có thể cảm nhận và đánh giá mức độ hài lòng trong và sau toàn bộ quá trình trực tiếp tiếp nhận.",
            "Quyền Thụ Hưởng Trải Nghiệm: Khách hàng chỉ sở hữu lợi ích chăm sóc sức khỏe và trải nghiệm dịch vụ, hoàn toàn không thể tồn kho."
        ]

        if data:
            before_title = data.get("before_title", "HÀNG HÓA HỮU HÌNH (GOODS)")
            b_raw_items = data.get("before_items", [])
            after_title = data.get("after_title", "SẢN PHẨM DỊCH VỤ (SERVICES)")
            a_raw_items = data.get("after_items", [])
            before_pill = data.get("before_pill", "✕ HÀNG HÓA HỮU HÌNH")
            after_pill = data.get("after_pill", "✓ SẢN PHẨM DỊCH VỤ")
            before_badge = data.get("before_badge", "Góc Nhìn Thực Thể Đo Lường Được")
            after_badge = data.get("after_badge", "Góc Nhìn Trải Nghiệm Giá Trị Vô Hình")
        elif atoms and len(atoms) >= 2:
            before_title = atoms[0].get("title", "HÀNG HÓA HỮU HÌNH (GOODS)")
            b_raw_items = atoms[0].get("items", []) or ([atoms[0].get("text", "")] if atoms[0].get("text") else [])
            after_title = atoms[1].get("title", "SẢN PHẨM DỊCH VỤ (SERVICES)")
            a_raw_items = atoms[1].get("items", []) or ([atoms[1].get("text", "")] if atoms[1].get("text") else [])
            before_pill = atoms[0].get("pill", "✕ HÀNG HÓA HỮU HÌNH")
            after_pill = atoms[1].get("pill", "✓ SẢN PHẨM DỊCH VỤ")
            before_badge = atoms[0].get("badge", "Chuẩn Mực Thực Thể Vật Chất")
            after_badge = atoms[1].get("badge", "Chuẩn Mực Trải Nghiệm & Vô Hình")
        else:
            before_title = "HÀNG HÓA HỮU HÌNH (GOODS)"
            b_raw_items = []
            after_title = "SẢN PHẨM DỊCH VỤ (SERVICES)"
            a_raw_items = []
            before_pill = "✕ HÀNG HÓA HỮU HÌNH"
            after_pill = "✓ SẢN PHẨM DỊCH VỤ"
            before_badge = "Chuẩn Mực Thực Thể Vật Chất"
            after_badge = "Chuẩn Mực Trải Nghiệm & Vô Hình"

        # Ensure at least 3 detailed bullets to eliminate dead space completely
        before_bullets = b_raw_items if len(b_raw_items) >= 2 else def_before_items
        after_bullets = a_raw_items if len(a_raw_items) >= 2 else def_after_items

        pill_w = min(240.0, col_w - 40.0)
        pill_h = 26.0
        badge_h = 28.0
        badge_y = top + height - badge_h - 14.0
        tb_top = top + 50.0
        tb_h = badge_y - tb_top - 8.0

        # -------------------------------------------------------------
        # Left Card: Before (Rose / Red High Contrast Accent)
        # -------------------------------------------------------------
        b_shapes = []
        b_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, col_w, height)
        b_card.Fill.Solid()
        b_card.Fill.ForeColor.RGB = hex_to_bgr("#0B132B" if self.theme == "DARK" else "#FFFFFF")
        b_card.Line.Visible = msoTrue
        b_card.Line.ForeColor.RGB = hex_to_bgr("#F43F5E" if self.theme == "DARK" else "#E11D48")
        b_card.Line.Weight = 1.8
        b_shapes.append(b_card)

        # Top Accent Pill
        b_pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 20, top + 16, pill_w, pill_h)
        b_pill.Fill.Solid()
        b_pill.Fill.ForeColor.RGB = hex_to_bgr("#2D121B" if self.theme == "DARK" else "#FFE4E6")
        b_pill.Line.Visible = msoTrue
        b_pill.Line.ForeColor.RGB = hex_to_bgr("#F43F5E" if self.theme == "DARK" else "#E11D48")
        b_pill.Line.Weight = 1.0
        pt1 = b_pill.TextFrame.TextRange
        pt1.Text = before_pill
        pt1.Font.Name = font_name
        pt1.Font.Size = 10.5
        pt1.Font.Bold = msoTrue
        pt1.Font.Color.RGB = hex_to_bgr("#FB7185" if self.theme == "DARK" else "#BE123C")
        pt1.ParagraphFormat.Alignment = ppAlignCenter
        b_shapes.append(b_pill)

        # Bottom Badge Strip
        b_badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 20, badge_y, col_w - 40.0, badge_h)
        b_badge.Fill.Solid()
        b_badge.Fill.ForeColor.RGB = hex_to_bgr("#1E1E2E" if self.theme == "DARK" else "#F1F5F9")
        b_badge.Line.Visible = msoFalse
        bb_txt = b_badge.TextFrame.TextRange
        bb_txt.Text = f"◈ {before_badge}"
        bb_txt.Font.Name = font_name
        bb_txt.Font.Size = 11.0
        bb_txt.Font.Bold = msoTrue
        bb_txt.Font.Color.RGB = hex_to_bgr("#FDA4AF" if self.theme == "DARK" else "#9F1239")
        bb_txt.ParagraphFormat.Alignment = ppAlignCenter
        b_shapes.append(b_badge)

        # Textbox
        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, tb_top, col_w - 40.0, tb_h)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        btf.MarginTop = 0
        btf.MarginBottom = 0
        btf.MarginLeft = 0
        btf.MarginRight = 0

        bp1 = btf.TextRange.Paragraphs(1)
        bp1.Text = before_title + "\n"
        bp1.Font.Name = font_name
        bp1.Font.Size = 16.0
        bp1.Font.Bold = msoTrue
        bp1.Font.Color.RGB = hex_to_bgr("#F43F5E" if self.theme == "DARK" else "#BE123C")
        bp1.ParagraphFormat.SpaceAfter = 8

        bp2 = btf.TextRange.Paragraphs(2)
        bp2.Text = "\n".join([f"• {it}" for it in before_bullets])
        bp2.Font.Name = font_name
        bp2.Font.Size = 13.0
        bp2.Font.Color.RGB = hex_to_bgr(muted)
        bp2.ParagraphFormat.LineRuleWithin = msoTrue
        bp2.ParagraphFormat.SpaceWithin = 1.22
        b_shapes.append(btb)

        before_group = safe_group(slide, b_shapes, "Before_Card_Group")
        shapes.append(before_group)

        # -------------------------------------------------------------
        # Right Card: After (Emerald / Green High Contrast Accent)
        # -------------------------------------------------------------
        ax = left + col_w + gap
        a_shapes = []
        a_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, ax, top, col_w, height)
        a_card.Fill.Solid()
        a_card.Fill.ForeColor.RGB = hex_to_bgr("#0B132B" if self.theme == "DARK" else "#FFFFFF")
        a_card.Line.Visible = msoTrue
        a_card.Line.ForeColor.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#059669")
        a_card.Line.Weight = 1.8
        a_shapes.append(a_card)

        # Top Accent Pill
        a_pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, ax + 20, top + 16, pill_w, pill_h)
        a_pill.Fill.Solid()
        a_pill.Fill.ForeColor.RGB = hex_to_bgr("#062E21" if self.theme == "DARK" else "#DCFCE7")
        a_pill.Line.Visible = msoTrue
        a_pill.Line.ForeColor.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#059669")
        a_pill.Line.Weight = 1.0
        pt2 = a_pill.TextFrame.TextRange
        pt2.Text = after_pill
        pt2.Font.Name = font_name
        pt2.Font.Size = 10.5
        pt2.Font.Bold = msoTrue
        pt2.Font.Color.RGB = hex_to_bgr("#34D399" if self.theme == "DARK" else "#047857")
        pt2.ParagraphFormat.Alignment = ppAlignCenter
        a_shapes.append(a_pill)

        # Bottom Badge Strip
        a_badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, ax + 20, badge_y, col_w - 40.0, badge_h)
        a_badge.Fill.Solid()
        a_badge.Fill.ForeColor.RGB = hex_to_bgr("#064E3B" if self.theme == "DARK" else "#DCFCE7")
        a_badge.Line.Visible = msoFalse
        ab_txt = a_badge.TextFrame.TextRange
        ab_txt.Text = f"★ {after_badge}"
        ab_txt.Font.Name = font_name
        ab_txt.Font.Size = 11.0
        ab_txt.Font.Bold = msoTrue
        ab_txt.Font.Color.RGB = hex_to_bgr("#6EE7B7" if self.theme == "DARK" else "#065F46")
        ab_txt.ParagraphFormat.Alignment = ppAlignCenter
        a_shapes.append(a_badge)

        # Textbox
        atb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, ax + 20, tb_top, col_w - 40.0, tb_h)
        atf = atb.TextFrame
        atf.WordWrap = msoTrue
        atf.MarginTop = 0
        atf.MarginBottom = 0
        atf.MarginLeft = 0
        atf.MarginRight = 0

        ap1 = atf.TextRange.Paragraphs(1)
        ap1.Text = after_title + "\n"
        ap1.Font.Name = font_name
        ap1.Font.Size = 16.0
        ap1.Font.Bold = msoTrue
        ap1.Font.Color.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#047857")
        ap1.ParagraphFormat.SpaceAfter = 8

        ap2 = atf.TextRange.Paragraphs(2)
        ap2.Text = "\n".join([f"✔ {it}" for it in after_bullets])
        ap2.Font.Name = font_name
        ap2.Font.Size = 13.0
        ap2.Font.Color.RGB = hex_to_bgr("#FFFFFF" if self.theme == "DARK" else "#0F172A")
        ap2.ParagraphFormat.LineRuleWithin = msoTrue
        ap2.ParagraphFormat.SpaceWithin = 1.22
        a_shapes.append(atb)

        after_group = safe_group(slide, a_shapes, "After_Card_Group")
        shapes.append(after_group)

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
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        pillars_raw = spec.get("pillars")
        if pillars_raw:
            pillars = pillars_raw
        else:
            atoms = spec.get("atoms", [])
            if atoms:
                pillars = []
                for i, a in enumerate(atoms[:3]):
                    t = a.get("title", f"Trọng Tâm 0{i+1}")
                    s = a.get("text") or a.get("desc") or ""
                    k = a.get("kpi") or a.get("badge") or f"Trụ Cột 0{i+1}"
                    pillars.append({"title": t, "sub": s, "kpi": k})
            else:
                pillars = [
                    {"title": "Trụ Cột Kinh Tế", "sub": "Tận dụng tối đa Dư lợi Dân số vàng để bứt phá thu nhập bình quân", "kpi": "GDP +6.8%"},
                    {"title": "Trụ Cột Xã Hội", "sub": "Mở rộng bao phủ an sinh và bảo hiểm y tế toàn dân ứng phó già hóa", "kpi": "BHYT 95%"},
                    {"title": "Trụ Cột Thể Chế", "sub": "Hoàn thiện pháp luật và chính sách dân số đồng bộ với chiến lược số", "kpi": "100% Số Hóa"}
                ]

        count = len(pillars)
        gap = 16.0
        col_w = (width - (gap * (count - 1))) / count

        for idx, p in enumerate(pillars):
            px = left + idx * (col_w + gap)
            pillar_shapes = []

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            card.Line.Weight = 2.0 if idx == 0 else 1.0
            pillar_shapes.append(card)

            # Top Accent Color Bar
            top_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, top, col_w, 6)
            top_bar.Fill.Solid()
            top_bar.Fill.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else ("#0D9488" if idx == 1 else "#10B981"))
            top_bar.Line.Visible = msoFalse
            pillar_shapes.append(top_bar)

            # Text inside Pillar
            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 16, top + 18, col_w - 32, height - 60)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginTop = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"TRỤ CỘT 0{idx + 1}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.SpaceAfter = 4

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p["title"] + "\n\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 15.5
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.SpaceAfter = 6

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = p.get("sub", "")
            p3.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p3.Font.Size = 12.5
            p3.Font.Color.RGB = hex_to_bgr(muted)
            p3.ParagraphFormat.LineRuleWithin = msoTrue
            p3.ParagraphFormat.SpaceWithin = 1.3
            pillar_shapes.append(tb)

            # Bottom Anchor Badge
            kpi_val = p.get("kpi", f"Chuẩn Đầu Ra 0{idx+1}")
            badge_y = top + height - 36.0
            badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, px + 16, badge_y, col_w - 32, 22)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E2E8F0")
            badge.Line.Visible = msoTrue
            badge.Line.ForeColor.RGB = hex_to_bgr(brand if idx == 0 else border)
            badge.Line.Weight = 1.0
            bt = badge.TextFrame.TextRange
            bt.Text = f"★ {kpi_val}"
            bt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            bt.Font.Size = 11.0
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr("#10B981" if self.theme == "DARK" else "#059669")
            bt.ParagraphFormat.Alignment = ppAlignCenter
            pillar_shapes.append(badge)

            col_grp = safe_group(slide, pillar_shapes, f"Pillar_Col_{idx+1}")
            shapes.append(col_grp)

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

        pillars_raw = spec.get("pillars", [])
        atoms = spec.get("atoms", [])
        if pillars_raw:
            pillars = pillars_raw
        elif atoms:
            pillars = []
            for i, a in enumerate(atoms[:4]):
                title = a.get("title", f"Trọng Tâm 0{i+1}") if isinstance(a, dict) else f"Trọng Tâm 0{i+1}"
                desc = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                num = a.get("num") or a.get("pill") or f"TRỌNG TÂM 0{i+1}"
                kpi = a.get("kpi") or a.get("chip") or a.get("badge") or ""
                pillars.append({"num": num, "title": title, "desc": desc, "kpi": kpi})
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa y tế dân số.")
            pillars = [
                {"num": f"TRỌNG TÂM 0{i+1}", "title": f"Yếu Tố Cốt Lõi 0{i+1}", "desc": claim, "kpi": ""}
                for i in range(4)
            ]

        gap = 12.0
        col_w = (width - 3 * gap) / 4.0

        for i, p in enumerate(pillars[:4]):
            px = left + i * (col_w + gap)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if i == 0 else border)
            card.Line.Weight = 1.5 if i == 0 else 1.0

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 12, top + 16, col_w - 24, height - 32)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = p.get("num", f"0{i+1}") + "\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 11.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.SpaceAfter = 4

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p.get("title", "") + "\n\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 14.0
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.SpaceAfter = 6

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = p.get("desc", "") + "\n\n"
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 12.0
            p3.Font.Color.RGB = hex_to_bgr(muted)
            p3.ParagraphFormat.LineRuleWithin = msoTrue
            p3.ParagraphFormat.SpaceWithin = 1.2

            if p.get("kpi"):
                p4 = tf.TextRange.Paragraphs(4)
                p4.Text = f"★ {p.get('kpi', '')}"
                p4.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
                p4.Font.Size = 11.5
                p4.Font.Bold = msoTrue
                p4.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "success", "#10B981"))

            col_grp = safe_group(slide, [card, tb], f"Pillar4_Col_{i+1}")
            shapes.append(col_grp)

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

        steps_raw = spec.get("steps", [])
        atoms = spec.get("atoms", [])
        colors = [danger, warning, success]
        tags = ["BƯỚC 1: ĐẶT VẤN ĐỀ", "BƯỚC 2: PHÂN TÍCH", "BƯỚC 3: GIẢI PHÁP CAN THIỆP"]
        if steps_raw:
            steps = steps_raw
        elif atoms:
            steps = []
            for i, a in enumerate(atoms[:3]):
                title = a.get("title", f"Giai Đoạn 0{i+1}") if isinstance(a, dict) else f"Giai Đoạn 0{i+1}"
                desc = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                tag = a.get("tag") or a.get("pill") or tags[i % len(tags)]
                steps.append({"tag": tag, "title": title, "desc": desc, "color": colors[i % len(colors)]})
        else:
            claim = spec.get("primary_claim", "Trọng tâm bài giảng y tế dân số.")
            steps = [
                {"tag": tags[i], "title": f"Mục Tiêu Trọng Điểm 0{i+1}", "desc": claim, "color": colors[i]}
                for i in range(3)
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
        levels_raw = spec.get("levels", [])
        atoms = spec.get("atoms", [])
        default_names = ["HỒNG TÂM (CỐT LÕI)", "VÒNG TRONG (TRỌNG YẾU)", "VÒNG NGOÀI (MỞ RỘNG)"]
        if levels_raw:
            levels = levels_raw
        elif atoms:
            levels = []
            for i, a in enumerate(atoms[:3]):
                name = a.get("name") or a.get("pill") or default_names[i % len(default_names)]
                target = a.get("title", f"Mục Tiêu 0{i+1}") if isinstance(a, dict) else f"Mục Tiêu 0{i+1}"
                desc = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                levels.append({"name": name, "target": target, "desc": desc})
        else:
            claim = spec.get("primary_claim", "Nội dung trọng tâm đào tạo y tế dân số.")
            levels = [
                {"name": default_names[i], "target": f"Đối Tượng Mục Tiêu 0{i+1}", "desc": claim}
                for i in range(3)
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

        atoms = spec.get("atoms", [])
        gap = 16.0

        if len(atoms) == 2:
            # Symmetrical Split for 2 contrasting/paired concepts
            col_w = (width - gap) / 2.0
            for idx, a in enumerate(atoms):
                cx = left + idx * (col_w + gap)
                card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, col_w, height)
                card.Fill.Solid()
                card.Fill.ForeColor.RGB = hex_to_bgr(surface)
                card.Line.Visible = msoTrue
                accent_c = brand if idx == 0 else "#10B981"
                card.Line.ForeColor.RGB = hex_to_bgr(accent_c)
                card.Line.Weight = 2.0

                # Accent badge
                pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 18, top + 18, 140, 26)
                pill.Fill.Solid()
                pill.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "badge_bg", "#082F49"))
                pill.Line.Visible = msoFalse
                pt = pill.TextFrame.TextRange
                pt.Text = f"THUỘC TÍNH 0{idx+1}" if "Thuộc Tính" in a.get("title", "") else f"TRỌNG TÂM 0{idx+1}"
                pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
                pt.Font.Size = 11.0
                pt.Font.Bold = msoTrue
                pt.Font.Color.RGB = hex_to_bgr(accent_c)
                pt.ParagraphFormat.Alignment = ppAlignCenter

                tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 18, top + 56, col_w - 36, height - 74)
                tf = tb.TextFrame
                tf.WordWrap = msoTrue
                p1 = tf.TextRange.Paragraphs(1)
                p1.Text = a.get("title", "") + "\n\n"
                p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
                p1.Font.Size = 17.0
                p1.Font.Bold = msoTrue
                p1.Font.Color.RGB = hex_to_bgr(ink)
                p1.ParagraphFormat.SpaceAfter = 8

                p2 = tf.TextRange.Paragraphs(2)
                p2.Text = a.get("text", "")
                p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
                p2.Font.Size = 13.5
                p2.Font.Color.RGB = hex_to_bgr(muted)
                p2.ParagraphFormat.SpaceWithin = 1.25

                col_grp = safe_group(slide, [card, pill, tb], f"Hero_Split_Col_{idx+1}")
                shapes.append(col_grp)

            return shapes

        half_w = (width - gap) / 2.0
        hero_atom = atoms[0] if atoms else {"title": "TRỌNG TÂM CHIẾN LƯỢC", "text": spec.get("primary_claim", "Tập trung 100% nguồn lực vào nghiên cứu thuật toán sinh bố cục tối ưu.")}

        # Left Hero Card (50%)
        l_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, half_w, height)
        l_card.Fill.Solid()
        l_card.Fill.ForeColor.RGB = hex_to_bgr(brand)
        l_card.Line.Visible = msoFalse

        ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, top + 25, half_w - 40, height - 50)
        ltf = ltb.TextFrame
        ltf.WordWrap = msoTrue
        lp1 = ltf.TextRange.Paragraphs(1)
        lp1.Text = hero_atom.get("title", "TRỌNG TÂM CHIẾN LƯỢC") + "\n\n"
        lp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        lp1.Font.Size = 18.0
        lp1.Font.Bold = msoTrue
        lp1.Font.Color.RGB = hex_to_bgr("#FFFFFF")

        lp2 = ltf.TextRange.Paragraphs(2)
        lp2.Text = hero_atom.get("text", spec.get("primary_claim", ""))
        lp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        lp2.Font.Size = 13.5
        lp2.Font.Color.RGB = hex_to_bgr("#F0FDF4")
        lp2.ParagraphFormat.SpaceWithin = 1.25

        hero_grp = safe_group(slide, [l_card, ltb], "Hero_Split_Left")
        shapes.append(hero_grp)

        # Right Sub-Cards
        rx = left + half_w + gap
        sub_items = atoms[1:] if len(atoms) > 1 else [
            {"title": "Mô Hình Dữ Liệu", "text": "100% Bảng biểu & Biểu đồ gốc có thể chỉnh sửa trực tiếp."},
            {"title": "Tính Năng Co Giãn", "text": "Tự động cân đối tỷ lệ từ 2 đến 8 phần tử linh hoạt."},
            {"title": "Kiểm Định Tự Động", "text": "Bộ quy chuẩn 34 tiêu chí chất lượng nghiêm ngặt."}
        ]
        sub_count = len(sub_items)
        sub_h = (height - (sub_count - 1) * 10.0) / float(sub_count)

        for i, s in enumerate(sub_items):
            sy = top + i * (sub_h + 10.0)
            scard = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, sy, half_w, sub_h)
            scard.Fill.Solid()
            scard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            scard.Line.Visible = msoTrue
            scard.Line.ForeColor.RGB = hex_to_bgr(border)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 14, sy + 6, half_w - 28, sub_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"✓ {s.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 13.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = s.get("text", s.get("desc", ""))
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 12.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.SpaceWithin = 1.2

            sub_grp = safe_group(slide, [scard, tb], f"Hero_Split_Sub_{i+1}")
            shapes.append(sub_grp)

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

        atoms = spec.get("atoms", [])
        default_badges = ["TIÊU ĐIỂM", "TRỌNG TÂM", "MỞ RỘNG"]
        if spec.get("cards"):
            cards = spec["cards"]
        elif atoms:
            cards = []
            for i, a in enumerate(atoms[:3]):
                t = a.get("title", f"Nội Dung 0{i+1}") if isinstance(a, dict) else f"Nội Dung 0{i+1}"
                d = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                b = a.get("badge") or a.get("chip") or default_badges[i % len(default_badges)]
                cards.append({"badge": b, "title": t, "desc": d})
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa đào tạo.")
            cards = [
                {"badge": default_badges[i], "title": f"Mục Tiêu 0{i+1}", "desc": claim}
                for i in range(3)
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
        muted = self._get_token("colors", "muted", "#94A3B8")
        border = self._get_token("colors", "card_border", "#1E293B")
        success = self._get_token("colors", "success", "#10B981")

        # Top Banner Group
        banner_h = 48.0
        b_shapes = []
        banner = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, banner_h)
        banner.Fill.Solid()
        banner.Fill.ForeColor.RGB = hex_to_bgr(surface)
        banner.Line.Visible = msoTrue
        banner.Line.ForeColor.RGB = hex_to_bgr(brand)
        banner.Line.Weight = 1.5
        b_shapes.append(banner)

        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 15, top + 8, width - 30, banner_h - 16)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        bp = btf.TextRange
        bp.Text = "★  BÁO CÁO ĐIỀU HÀNH TỔNG THỂ: TĂNG TRƯỞNG VƯỢT KỲ VỌNG 135% TOÀN CÔNG TY  ★"
        bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp.Font.Size = 12.0
        bp.Font.Bold = msoTrue
        bp.Font.Color.RGB = hex_to_bgr(brand)
        bp.ParagraphFormat.Alignment = ppAlignCenter
        b_shapes.append(btb)

        banner_group = safe_group(slide, b_shapes, "Exec_Banner_Group")
        shapes.append(banner_group)

        # 3 KPI Stat Cards below banner
        card_y = top + banner_h + 16.0
        card_h = min(height - banner_h - 16.0, 250.0)
        card_w = (width - 2 * 16.0) / 3.0

        kpis = [
            {"cat": "DOANH THU & TÀI CHÍNH", "val": "24.8 Tỷ", "label": "Tổng Doanh Thu ARR", "delta": "+42% YoY", "color": "#0284C7", "progress": 0.85},
            {"cat": "QUY MÔ NGƯỜI DÙNG", "val": "128,000", "label": "Khách Hàng Hoạt Động", "delta": "+85% MAU", "color": "#10B981", "progress": 0.92},
            {"cat": "HẠ TẦNG & CHẤT LƯỢNG", "val": "99.98%", "label": "Độ Ổn Định Hạ Tầng", "delta": "SLA Đạt Chuẩn", "color": "#8B5CF6", "progress": 0.99}
        ]

        for i, k in enumerate(kpis):
            k_shapes = []
            kx = left + i * (card_w + 16.0)
            k_color = k["color"]

            k_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, kx, card_y, card_w, card_h)
            k_card.Fill.Solid()
            k_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            k_card.Line.Visible = msoTrue
            k_card.Line.ForeColor.RGB = hex_to_bgr(k_color)
            k_card.Line.Weight = 1.8
            k_shapes.append(k_card)

            # Category pill badge
            pill_w = card_w - 32.0
            pill_h = 22.0
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, kx + 16.0, card_y + 14.0, pill_w, pill_h)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = k["cat"]
            pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            pt.Font.Size = 9.0
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr(k_color)
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            k_shapes.append(pill)

            # Big Numeric Stat
            tb_num = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, kx + 10, card_y + 44.0, card_w - 20, 50.0)
            ntf = tb_num.TextFrame
            ntf.WordWrap = msoTrue
            np = ntf.TextRange
            np.Text = k["val"]
            np.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            np.Font.Size = 32
            np.Font.Bold = msoTrue
            np.Font.Color.RGB = hex_to_bgr(k_color)
            np.ParagraphFormat.Alignment = ppAlignCenter
            k_shapes.append(tb_num)

            # Label Text
            tb_label = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, kx + 10, card_y + 98.0, card_w - 20, 30.0)
            ltf = tb_label.TextFrame
            ltf.WordWrap = msoTrue
            lp = ltf.TextRange
            lp.Text = k["label"]
            lp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            lp.Font.Size = 12.0
            lp.Font.Bold = msoTrue
            lp.Font.Color.RGB = hex_to_bgr(ink)
            lp.ParagraphFormat.Alignment = ppAlignCenter
            k_shapes.append(tb_label)

            # Delta Badge
            delta_w = card_w - 60.0
            delta_h = 24.0
            delta_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, kx + 30.0, card_y + 134.0, delta_w, delta_h)
            delta_box.Fill.Solid()
            delta_box.Fill.ForeColor.RGB = hex_to_bgr("#064E3B" if self.theme == "DARK" else "#DCFCE7")
            delta_box.Line.Visible = msoTrue
            delta_box.Line.ForeColor.RGB = hex_to_bgr(success)
            delta_box.Line.Weight = 1.0
            dt = delta_box.TextFrame.TextRange
            dt.Text = f"▲  {k['delta']}"
            dt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            dt.Font.Size = 10.5
            dt.Font.Bold = msoTrue
            dt.Font.Color.RGB = hex_to_bgr(success)
            delta_box.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            k_shapes.append(delta_box)

            # Mini Progress Track & Bar
            bar_track_w = card_w - 40.0
            bar_track_h = 6.0
            bar_track_y = card_y + card_h - 26.0
            track = slide.Shapes.AddShape(msoShapeRoundedRectangle, kx + 20.0, bar_track_y, bar_track_w, bar_track_h)
            track.Fill.Solid()
            track.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            track.Line.Visible = msoFalse
            k_shapes.append(track)

            fill_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, kx + 20.0, bar_track_y, bar_track_w * k["progress"], bar_track_h)
            fill_bar.Fill.Solid()
            fill_bar.Fill.ForeColor.RGB = hex_to_bgr(k_color)
            fill_bar.Line.Visible = msoFalse
            k_shapes.append(fill_bar)

            card_group = safe_group(slide, k_shapes, f"Exec_KPI_Card_{i+1}")
            shapes.append(card_group)

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
        muted = self._get_token("colors", "muted", "#94A3B8")

        mockup_h = min(height, 310.0)
        mockup_y = top + (height - mockup_h) / 2.0
        mockup_w = min(width, 760.0)
        mockup_x = left + (width - mockup_w) / 2.0

        m_shapes = []
        screen_h = mockup_h * 0.88

        # Outer Laptop / Monitor Bezel Frame
        outer = slide.Shapes.AddShape(msoShapeRoundedRectangle, mockup_x, mockup_y, mockup_w, screen_h)
        outer.Fill.Solid()
        outer.Fill.ForeColor.RGB = hex_to_bgr("#0F172A")
        outer.Line.Visible = msoTrue
        outer.Line.ForeColor.RGB = hex_to_bgr("#334155")
        outer.Line.Weight = 2.0
        m_shapes.append(outer)

        # Top Window Chrome Bar
        pad = 8.0
        chrome_h = 24.0
        chrome = slide.Shapes.AddShape(msoShapeRoundedRectangle, mockup_x + pad, mockup_y + pad, mockup_w - 2 * pad, chrome_h)
        chrome.Fill.Solid()
        chrome.Fill.ForeColor.RGB = hex_to_bgr("#1E293B")
        chrome.Line.Visible = msoFalse
        m_shapes.append(chrome)

        # 3 macOS traffic light window dots (Red, Yellow, Green)
        dot_colors = ["#EF4444", "#F59E0B", "#10B981"]
        for d_idx, dc in enumerate(dot_colors):
            dot = slide.Shapes.AddShape(msoShapeOval, mockup_x + pad + 10.0 + d_idx * 14.0, mockup_y + pad + 7.0, 10.0, 10.0)
            dot.Fill.Solid()
            dot.Fill.ForeColor.RGB = hex_to_bgr(dc)
            dot.Line.Visible = msoFalse
            m_shapes.append(dot)

        # Window Title in Chrome
        w_title = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, mockup_x + 80.0, mockup_y + pad + 2.0, mockup_w - 160.0, 20.0)
        wt = w_title.TextFrame.TextRange
        wt.Text = "Make Slide Pro V8.6 — Executive Studio Workspace"
        wt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        wt.Font.Size = 9.0
        wt.Font.Color.RGB = hex_to_bgr(muted)
        wt.ParagraphFormat.Alignment = ppAlignCenter
        m_shapes.append(w_title)

        # Inner Screen Glass Area
        screen_y = mockup_y + pad + chrome_h + 4.0
        screen_inner_h = screen_h - (pad * 2) - chrome_h - 8.0
        screen = slide.Shapes.AddShape(msoShapeRectangle, mockup_x + pad, screen_y, mockup_w - 2 * pad, screen_inner_h)
        screen.Fill.Solid()
        screen.Fill.ForeColor.RGB = hex_to_bgr(surface)
        screen.Line.Visible = msoFalse
        m_shapes.append(screen)

        # Inside Screen UI: Sidebar (left) + Main Canvas (right)
        sb_w = 110.0
        sb = slide.Shapes.AddShape(msoShapeRectangle, mockup_x + pad, screen_y, sb_w, screen_inner_h)
        sb.Fill.Solid()
        sb.Fill.ForeColor.RGB = hex_to_bgr("#080D1A")
        sb.Line.Visible = msoTrue
        sb.Line.ForeColor.RGB = hex_to_bgr("#1E293B")
        sb.Line.Weight = 1.0
        m_shapes.append(sb)

        sb_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, mockup_x + pad + 8.0, screen_y + 12.0, sb_w - 16.0, screen_inner_h - 24.0)
        sb_tf = sb_tb.TextFrame
        sb_tf.WordWrap = msoTrue
        sb_tr = sb_tf.TextRange
        sb_tr.Text = "⚡ TÁC TỬ MACC\n\n📁 Thư Viện 165+\n📊 Native Tables\n📈 Office Charts\n✨ Apple Motion\n⚙ Thiết Lập"
        sb_tr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        sb_tr.Font.Size = 8.5
        sb_tr.Font.Color.RGB = hex_to_bgr(muted)
        m_shapes.append(sb_tb)

        # Main Workspace inside Screen: Top 3 KPI metric tiles
        main_x = mockup_x + pad + sb_w + 14.0
        main_w = mockup_w - 2 * pad - sb_w - 28.0
        tile_w = (main_w - 16.0) / 3.0
        tile_h = 42.0

        mini_stats = [
            ("165+", "Archetypes Khổng Lồ", "#0284C7"),
            ("0.85s", "Apple Morph Motion", "#10B981"),
            ("100%", "Native Office Objects", "#38BDF8")
        ]
        for m_idx, (m_val, m_lbl, m_col) in enumerate(mini_stats):
            tx = main_x + m_idx * (tile_w + 8.0)
            tile = slide.Shapes.AddShape(msoShapeRoundedRectangle, tx, screen_y + 12.0, tile_w, tile_h)
            tile.Fill.Solid()
            tile.Fill.ForeColor.RGB = hex_to_bgr("#111C3A" if self.theme == "DARK" else "#F1F5F9")
            tile.Line.Visible = msoTrue
            tile.Line.ForeColor.RGB = hex_to_bgr(m_col)
            tile.Line.Weight = 1.0
            m_shapes.append(tile)

            ttb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, tx + 4.0, screen_y + 14.0, tile_w - 8.0, tile_h - 4.0)
            ttf = ttb.TextFrame
            ttf.WordWrap = msoTrue
            ttf.MarginLeft = 0
            p1 = ttf.TextRange.Paragraphs(1)
            p1.Text = f"{m_val}  "
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 11.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(m_col)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = ttf.TextRange.Paragraphs(2)
            p2.Text = m_lbl
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 8.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            m_shapes.append(ttb)

        # Center Mockup Slide Preview Canvas inside screen
        prev_y = screen_y + 62.0
        prev_h = screen_inner_h - 72.0
        prev_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, main_x, prev_y, main_w, prev_h)
        prev_card.Fill.Solid()
        prev_card.Fill.ForeColor.RGB = hex_to_bgr("#050914")
        prev_card.Line.Visible = msoTrue
        prev_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        prev_card.Line.Weight = 1.2
        m_shapes.append(prev_card)

        prev_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, main_x + 15.0, prev_y + 10.0, main_w - 30.0, prev_h - 20.0)
        ptf = prev_tb.TextFrame
        ptf.WordWrap = msoTrue
        pp1 = ptf.TextRange.Paragraphs(1)
        pp1.Text = "KHUNG THIẾT BỊ ĐỈNH CAO: TRỰC QUAN HÓA TOÀN BỘ HỆ SINH THÁI MAKE SLIDE PRO\n"
        pp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        pp1.Font.Size = 11.0
        pp1.Font.Bold = msoTrue
        pp1.Font.Color.RGB = hex_to_bgr("#38BDF8")
        pp1.ParagraphFormat.Alignment = ppAlignCenter

        pp2 = ptf.TextRange.Paragraphs(2)
        pp2.Text = "Tự động hóa trình chiếu trực tiếp trên PowerPoint Native COM • Sẵn sàng cho hội nghị C-Level & Apple Keynote"
        pp2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        pp2.Font.Size = 9.5
        pp2.Font.Color.RGB = hex_to_bgr(ink)
        pp2.ParagraphFormat.Alignment = ppAlignCenter
        m_shapes.append(prev_tb)

        # Laptop Base / Stand Below
        base_w = mockup_w * 0.42
        base_h = mockup_h * 0.07
        base_x = mockup_x + (mockup_w - base_w) / 2.0
        base_y = mockup_y + screen_h + 3.0
        base = slide.Shapes.AddShape(msoShapeRoundedRectangle, base_x, base_y, base_w, base_h)
        base.Fill.Solid()
        base.Fill.ForeColor.RGB = hex_to_bgr("#334155")
        base.Line.Visible = msoFalse
        m_shapes.append(base)

        mockup_grp = safe_group(slide, m_shapes, "Device_Mockup_Frame")
        shapes.append(mockup_grp)

        return shapes

    # 24. CONTAINER_METRIC_MARQUEE_BANNER (Dải Banner 4 Chỉ Số Nổi Bật)
    def render_metric_marquee_banner(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")

        banner_h = 120.0
        banner_y = top + (height - banner_h) / 2.0

        # Background Stripe Card
        stripe = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, banner_y, width, banner_h)
        stripe.Fill.Solid()
        stripe.Fill.ForeColor.RGB = hex_to_bgr("#082F49" if self.theme == "DARK" else "#E0F2FE")
        stripe.Line.Visible = msoTrue
        stripe.Line.ForeColor.RGB = hex_to_bgr(brand)
        stripe.Line.Weight = 2.0
        shapes.append(stripe)

        atoms = spec.get("atoms", [])
        colors = ["#38BDF8", "#10B981", "#F59E0B", "#A855F7"]
        badges = ["TIÊU ĐIỂM", "HIỆU QUẢ", "TIẾN ĐỘ", "CHẤT LƯỢNG"]
        if spec.get("marquee_stats"):
            stats = spec["marquee_stats"]
        elif atoms:
            stats = []
            for i, a in enumerate(atoms[:4]):
                val = a.get("val") or a.get("num") or a.get("metric") or f"0{i+1}"
                lbl = a.get("title", f"Chỉ Số {i+1}") if isinstance(a, dict) else str(a)
                badge = a.get("badge") or a.get("chip") or badges[i % len(badges)]
                stats.append({"val": str(val), "label": lbl, "badge": badge, "color": colors[i % len(colors)]})
        else:
            stats = [
                {"val": f"10{i}%", "label": f"Mục Tiêu Chuẩn Hóa 0{i+1}", "badge": badges[i], "color": colors[i]}
                for i in range(4)
            ]

        col_w = width / len(stats)
        for i, st in enumerate(stats):
            col_shapes = []
            cx = left + i * col_w

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 8, banner_y + 12, col_w - 16, banner_h - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{st['val']}\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 28.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(st["color"])
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"{st['label']}\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 11.0
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = st["badge"]
            p3.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p3.Font.Size = 9.0
            p3.Font.Bold = msoTrue
            p3.Font.Color.RGB = hex_to_bgr(st["color"])
            p3.ParagraphFormat.Alignment = ppAlignCenter
            col_shapes.append(tb)

            if i < len(stats) - 1:
                v_div = slide.Shapes.AddShape(msoShapeRectangle, cx + col_w - 1.0, banner_y + 18.0, 1.5, banner_h - 36.0)
                v_div.Fill.Solid()
                v_div.Fill.ForeColor.RGB = hex_to_bgr("#0284C7")
                v_div.Line.Visible = msoFalse
                col_shapes.append(v_div)

            stat_col_grp = safe_group(slide, col_shapes, f"Marquee_Stat_{i+1}")
            shapes.append(stat_col_grp)

        return shapes

    # 25. CONTAINER_THREE_PILLARS_CARDS (Bộ 3 Thẻ Kính Mờ Nâng Cao)
    def render_three_pillars_cards(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")

        card_h = min(height, 280.0)
        card_y = top + (height - card_h) / 2.0
        gap = 18.0
        card_w = (width - 2 * gap) / 3.0

        atoms = spec.get("atoms", [])
        palette = [
            self._get_token("colors", "brand", "#0284C7"),
            self._get_token("colors", "success", "#10B981"),
            self._get_token("colors", "accent", "#8B5CF6")
        ]
        if atoms:
            pillars = []
            for i, atom in enumerate(atoms[:3]):
                title = atom.get("title", f"Trọng Tâm 0{i+1}") if isinstance(atom, dict) else f"Trọng Tâm 0{i+1}"
                text = atom.get("text") or atom.get("body") or atom.get("desc") or str(atom) if isinstance(atom, dict) else str(atom)
                raw_bullets = [b.strip().lstrip("•- ") for b in text.split("\n") if b.strip()]
                if not raw_bullets:
                    raw_bullets = [text]
                formatted_bullets = [f"• {b}" if not b.startswith("•") else b for b in raw_bullets]
                pill_label = atom.get("pill") or (f"TRỤ CỘT 0{i+1}" if "trụ cột" in title.lower() else f"TRỌNG TÂM 0{i+1}")
                chip_label = atom.get("chip") or atom.get("badge") or ""
                if "tiêu chuẩn" in chip_label.lower() or "watermark" in chip_label.lower():
                    chip_label = ""
                pillars.append({
                    "pill": pill_label,
                    "title": title,
                    "color": palette[i % len(palette)],
                    "bullets": formatted_bullets,
                    "chip": chip_label
                })
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa y tế dân số.")
            pillars = [
                {
                    "pill": f"TRỌNG TÂM 0{i+1}",
                    "title": f"Mục Tiêu Trọng Yếu 0{i+1}",
                    "color": palette[i % len(palette)],
                    "bullets": [f"• {claim}"],
                    "chip": ""
                }
                for i in range(3)
            ]

        for i, item in enumerate(pillars):
            p_shapes = []
            cx = left + i * (card_w + gap)
            color = item["color"]

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(color)
            card.Line.Weight = 2.0
            p_shapes.append(card)

            # Top Accent Pill
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 16.0, card_y + 14.0, card_w - 32.0, 26.0)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(color)
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = item["pill"]
            pt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            pt.Font.Size = 11.0
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr(ink)
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            p_shapes.append(pill)

            # Title
            tb_title = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 12.0, card_y + 48.0, card_w - 24.0, 36.0)
            ttf = tb_title.TextFrame
            ttf.WordWrap = msoTrue
            ttt = ttf.TextRange
            ttt.Text = item["title"]
            ttt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ttt.Font.Size = 14.5
            ttt.Font.Bold = msoTrue
            ttt.Font.Color.RGB = hex_to_bgr(ink)
            ttt.ParagraphFormat.Alignment = ppAlignCenter
            p_shapes.append(tb_title)

            # Divider line
            div = slide.Shapes.AddShape(msoShapeRectangle, cx + 20.0, card_y + 88.0, card_w - 40.0, 1.0)
            div.Fill.Solid()
            div.Fill.ForeColor.RGB = hex_to_bgr(color)
            div.Line.Visible = msoFalse
            p_shapes.append(div)

            # Structured Bullets
            bullets_h = card_h - 105.0 if not item.get("chip") else card_h - 135.0
            tb_desc = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 14.0, card_y + 94.0, card_w - 28.0, bullets_h)
            dtf = tb_desc.TextFrame
            dtf.WordWrap = msoTrue
            dtf.MarginLeft = 0
            dtf.MarginRight = 0
            dtt = dtf.TextRange
            dtt.Text = "\n\n".join(item["bullets"])
            dtt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            dtt.Font.Size = 12.5
            dtt.Font.Color.RGB = hex_to_bgr(muted)
            dtt.ParagraphFormat.Alignment = ppAlignLeft
            dtt.ParagraphFormat.SpaceWithin = 1.2
            p_shapes.append(tb_desc)

            # Bottom Highlight Chip (Only if explicit chip provided)
            if item.get("chip"):
                chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 14.0, card_y + card_h - 32.0, card_w - 28.0, 22.0)
                chip.Fill.Solid()
                chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
                chip.Line.Visible = msoFalse
                ct = chip.TextFrame.TextRange
                ct.Text = f"✔  {item['chip']}"
                ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
                ct.Font.Size = 9.5
                ct.Font.Bold = msoTrue
                ct.Font.Color.RGB = hex_to_bgr(color)
                chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
                p_shapes.append(chip)

            pillar_grp = safe_group(slide, p_shapes, f"Three_Pillars_Card_{i+1}")
            shapes.append(pillar_grp)

        return shapes

    # 26. CONTAINER_PROBLEM_SOLUTION_IMPACT (Bộ 3 Thẻ Dẫn Dắt Câu Chuyện)
    def render_problem_solution_impact(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")

        card_h = min(height, 280.0)
        card_y = top + (height - card_h) / 2.0
        gap = 40.0
        card_w = (width - 2 * gap) / 3.0

        atoms = spec.get("atoms", [])
        colors = ["#EF4444", "#0284C7", "#10B981"]
        badges = ["01. THỰC TRẠNG & THÁCH THỨC", "02. MỤC TIÊU & GIẢI PHÁP", "03. KẾT QUẢ ĐẠT ĐƯỢC"]
        if spec.get("stages"):
            stages = spec["stages"]
        elif atoms:
            stages = []
            for i, a in enumerate(atoms[:3]):
                title = a.get("title", f"Giai Đoạn 0{i+1}") if isinstance(a, dict) else f"Giai Đoạn 0{i+1}"
                text = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                raw_bullets = [b.strip().lstrip("•- ") for b in text.split("\n") if b.strip()]
                if not raw_bullets:
                    raw_bullets = [text]
                formatted_bullets = [f"• {b}" if not b.startswith("•") else b for b in raw_bullets]
                chip = a.get("chip") or a.get("badge") or ""
                if "tiêu chuẩn" in chip.lower() or "watermark" in chip.lower():
                    chip = ""
                stages.append({
                    "badge": a.get("badge", badges[i % len(badges)]),
                    "title": title,
                    "color": colors[i % len(colors)],
                    "bullets": formatted_bullets,
                    "chip": chip
                })
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa y tế dân số.")
            stages = [
                {
                    "badge": badges[i],
                    "title": f"Mục Tiêu Trọng Điểm 0{i+1}",
                    "color": colors[i],
                    "bullets": [f"• {claim}"],
                    "chip": ""
                }
                for i in range(3)
            ]

        card_coords = []
        for i, item in enumerate(stages):
            c_shapes = []
            cx = left + i * (card_w + gap)
            card_coords.append((cx, card_y))
            color = item["color"]

            # Dynamic Vector Connector incoming from previous card
            if i > 0 and len(card_coords) > 1:
                x_start = card_coords[i - 1][0] + card_w
                y_mid = card_y + card_h / 2.0
                x_end = cx
                conn = add_vector_connector(slide, x_start, y_mid, x_end, y_mid, color="#38BDF8", weight=2.5, arrowhead=True)
                if conn:
                    c_shapes.append(conn)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(color)
            card.Line.Weight = 2.0
            c_shapes.append(card)

            # Top Badge Pill
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 16.0, card_y + 14.0, card_w - 32.0, 26.0)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(color)
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = item["badge"]
            pt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            pt.Font.Size = 10.5
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            c_shapes.append(pill)

            # Title
            tb_title = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 12.0, card_y + 46.0, card_w - 24.0, 36.0)
            ttf = tb_title.TextFrame
            ttf.WordWrap = msoTrue
            ttf.MarginLeft = 0
            ttf.MarginRight = 0
            ttt = ttf.TextRange
            ttt.Text = item["title"]
            ttt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ttt.Font.Size = 12.5
            ttt.Font.Bold = msoTrue
            ttt.Font.Color.RGB = hex_to_bgr(ink)
            ttt.ParagraphFormat.Alignment = ppAlignCenter
            c_shapes.append(tb_title)

            # Divider line
            div = slide.Shapes.AddShape(msoShapeRectangle, cx + 18.0, card_y + 86.0, card_w - 36.0, 1.5)
            div.Fill.Solid()
            div.Fill.ForeColor.RGB = hex_to_bgr(color)
            div.Line.Visible = msoFalse
            c_shapes.append(div)

            # Bullets
            bullets_h = card_h - 110.0 if not item.get("chip") else card_h - 138.0
            tb_desc = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 12.0, card_y + 94.0, card_w - 24.0, bullets_h)
            dtf = tb_desc.TextFrame
            dtf.WordWrap = msoTrue
            dtf.MarginLeft = 0
            dtf.MarginRight = 0
            dtt = dtf.TextRange
            dtt.Text = "\n\n".join(item["bullets"])
            dtt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            dtt.Font.Size = 10.0
            dtt.Font.Color.RGB = hex_to_bgr(muted)
            dtt.ParagraphFormat.Alignment = ppAlignLeft
            c_shapes.append(tb_desc)

            # Bottom Highlight Chip (Only if explicit chip provided)
            if item.get("chip"):
                chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 14.0, card_y + card_h - 32.0, card_w - 28.0, 22.0)
                chip.Fill.Solid()
                chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
                chip.Line.Visible = msoFalse
                ct = chip.TextFrame.TextRange
                ct.Text = f"▲  {item['chip']}"
                ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
                ct.Font.Size = 9.5
                ct.Font.Bold = msoTrue
                ct.Font.Color.RGB = hex_to_bgr(color)
                chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
                c_shapes.append(chip)

            card_grp = safe_group(slide, c_shapes, f"PSI_Card_{i+1}")
            shapes.append(card_grp)

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

        center_label = spec.get("center_title") or spec.get("assertion_title") or "TRỌNG TÂM CỐT LÕI"
        if len(center_label) > 28:
            center_label = center_label[:26] + "..."

        core = slide.Shapes.AddShape(msoShapeHexagon, cx, cy, hex_w, hex_h)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Visible = msoTrue
        core.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        core.Line.Weight = 2.0
        shapes.append(core)
        tr = core.TextFrame.TextRange
        tr.Text = f"TRỌNG TÂM\n{center_label.upper()}"
        tr.Font.Size = 10.0
        tr.Font.Bold = msoTrue
        tr.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        tr.ParagraphFormat.Alignment = ppAlignCenter

        # 6 Outer Hexagons
        import math
        center_x = left + width / 2.0
        center_y = top + height / 2.0
        orbit_r = min(width, height) * 0.36
        
        atoms = spec.get("atoms", [])
        if spec.get("features"):
            features = spec["features"][:6]
        elif atoms:
            features = [a.get("title", f"Yếu Tố {i+1}") if isinstance(a, dict) else str(a) for i, a in enumerate(atoms[:6])]
            while len(features) < 6:
                features.append(f"Thuộc Tính 0{len(features)+1}")
        else:
            features = [f"Yếu Tố 0{i+1}" for i in range(6)]

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

        atoms = spec.get("atoms", [])
        if spec.get("reviews"):
            reviews = spec["reviews"]
        elif atoms:
            reviews = []
            for i, a in enumerate(atoms[:3]):
                stars = a.get("stars", "★★★★★")
                quote = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                author = a.get("title", f"Chuyên Gia Y Tế 0{i+1}") if isinstance(a, dict) else f"Chuyên Gia 0{i+1}"
                reviews.append((stars, f"\"{quote}\"", author))
        else:
            claim = spec.get("primary_claim", "Khuyến nghị chuẩn hóa chuyên môn y tế dân số.")
            reviews = [
                ("★★★★★", f"\"{claim}\"", f"Hội Đồng Chuyên Môn 0{i+1}")
                for i in range(3)
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

        atoms = spec.get("atoms", [])
        stat_val = spec.get("stat_value") or (atoms[0].get("title", "100%") if atoms else "100%")
        stat_label = spec.get("stat_label") or (atoms[0].get("text", "CHỈ SỐ TRỌNG YẾU") if atoms else "CHỈ SỐ TRỌNG YẾU")
        detail_title = spec.get("detail_title", "Ý NGHĨA CHUYÊN MÔN:")
        
        if len(atoms) > 1:
            detail_bullets = [f"• {a.get('title', '')}: {a.get('text', '')}" if isinstance(a, dict) else f"• {str(a)}" for a in atoms[1:]]
        else:
            claim = spec.get("primary_claim", "Trọng tâm bài giảng y tế dân số chuẩn hóa.")
            detail_bullets = [f"• {claim}"]

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
        p1.Text = f"{stat_val}\n"
        p1.Font.Size = 48.0 if len(str(stat_val)) > 5 else 56.0
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr("#38BDF8")
        p1.ParagraphFormat.Alignment = ppAlignCenter

        p2 = tf_l.TextRange.Paragraphs(2)
        p2.Text = stat_label.upper()
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
        rp.Text = f"{detail_title}\n\n" + "\n\n".join(detail_bullets)
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

        quote_h = min(height, 220.0)
        quote_y = top + (height - quote_h) / 2.0
        quote_w = width * 0.86
        quote_x = left + (width - quote_w) / 2.0

        q_shapes = []

        # Sleek Glassmorphic Card
        card = slide.Shapes.AddShape(msoShapeRoundedRectangle, quote_x, quote_y, quote_w, quote_h)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        card.Line.Visible = msoTrue
        card.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        card.Line.Weight = 1.8
        q_shapes.append(card)

        # Large Decorative Quotation Glyph
        q_glyph = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, quote_x + 24.0, quote_y + 12.0, 60.0, 50.0)
        q_glyph.TextFrame.WordWrap = msoFalse
        q_glyph.TextFrame.MarginLeft = 0
        q_glyph.TextFrame.MarginTop = 0
        gt = q_glyph.TextFrame.TextRange
        gt.Text = "“"
        gt.Font.Name = "Georgia"
        gt.Font.Size = 48
        gt.Font.Bold = msoTrue
        gt.Font.Color.RGB = hex_to_bgr("#38BDF8")
        q_shapes.append(q_glyph)

        # Main Quote Text
        tb_quote = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, quote_x + 50.0, quote_y + 40.0, quote_w - 100.0, 95.0)
        tf_q = tb_quote.TextFrame
        tf_q.WordWrap = msoTrue
        tf_q.MarginLeft = 0
        tf_q.MarginRight = 0
        qp = tf_q.TextRange
        qp.Text = spec.get("quote_text", "“Thiết kế không chỉ là vẻ bề ngoài hay cảm giác khi nhìn vào. Thiết kế là cách mà mọi thứ vận hành một cách hoàn hảo và liền mạch.”")
        qp.Font.Name = "Georgia"
        qp.Font.Size = 16.0
        qp.Font.Italic = msoTrue
        qp.Font.Color.RGB = hex_to_bgr(ink)
        qp.ParagraphFormat.Alignment = ppAlignCenter
        q_shapes.append(tb_quote)

        # Author Signature Pill at Bottom
        author_text = spec.get("quote_author", "— STEVE JOBS | TRIẾT LÝ THIẾT KẾ APPLE KEYNOTE")
        pill_w = quote_w * 0.58
        pill_h = 28.0
        pill_x = quote_x + (quote_w - pill_w) / 2.0
        pill_y = quote_y + quote_h - 38.0

        pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, pill_x, pill_y, pill_w, pill_h)
        pill.Fill.Solid()
        pill.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
        pill.Line.Visible = msoTrue
        pill.Line.ForeColor.RGB = hex_to_bgr(brand)
        pill.Line.Weight = 1.0
        pt = pill.TextFrame.TextRange
        pt.Text = author_text
        pt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        pt.Font.Size = 10.5
        pt.Font.Bold = msoTrue
        pt.Font.Color.RGB = hex_to_bgr("#38BDF8")
        pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        q_shapes.append(pill)

        quote_grp = safe_group(slide, q_shapes, "Minimalist_Quote_Card")
        shapes.append(quote_grp)

        return shapes


