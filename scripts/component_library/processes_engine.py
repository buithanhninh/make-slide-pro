"""
processes_engine.py
Exhaustive Process, Mechanism, and Flow Engine for Make Slide Pro V8.5.0.
Generates 20 classic process, timeline, mechanism, and roadmap models
using 100% Microsoft PowerPoint Native Vector Shapes.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

from .utils import safe_group, add_vector_connector

# Win32 Constants
msoShapeRectangle = 1
msoShapeTrapezoid = 3
msoShapeDiamond = 4
msoShapeRoundedRectangle = 5
msoShapeIsoscelesTriangle = 7
msoShapeOval = 9
msoShapeHexagon = 10
msoShapeRightArrow = 13
msoShapeLeftArrow = 14
msoShapeUpArrow = 15
msoShapeDownArrow = 16
msoShapeLeftRightArrow = 17
msoShapeDonut = 18
msoShapeChevron = 55
msoShapeFlowchartProcess = 61
msoShapeFlowchartDecision = 63
msoShapeCurvedRightArrow = 102
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


class ProcessesEngine:
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}

    def _get_token(self, category: str, key: str, fallback: str) -> str:
        return self.tokens.get(category, {}).get(key, fallback)

    # =========================================================================
    # 41. PROCESS_CHEVRON_LINEAR (Quy Trình Mũi Tên Vát Chevron)
    # =========================================================================
    def render_chevron_linear(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        atoms = spec.get("atoms", [])
        if data.get("steps"):
            steps = data["steps"]
        elif atoms:
            steps = []
            for i, a in enumerate(atoms):
                title = a.get("title", f"Bước {i+1}") if isinstance(a, dict) else f"Bước {i+1}"
                desc = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                step_num = a.get("step", f"{i+1:02d}") if isinstance(a, dict) else f"{i+1:02d}"
                steps.append({"step": step_num, "title": title, "desc": desc})
        else:
            claim = spec.get("primary_claim", "Nội dung quy trình chuẩn hóa.")
            steps = [
                {"step": f"{i+1:02d}", "title": f"Giai Đoạn 0{i+1}", "desc": claim}
                for i in range(3)
            ]

        count = max(2, min(len(steps), 7))
        gap = 8.0
        step_w = (width - (count - 1) * gap) / count
        chevron_h = min(height * 0.32, 85.0)
        card_h = height - chevron_h - 14.0
        card_top = top + chevron_h + 14.0

        for i in range(count):
            s = steps[i]
            sx = left + i * (step_w + gap)
            is_active = (i == count - 1) or s.get("highlight", False)
            step_shapes = []

            # Chevron Header Shape
            chev = slide.Shapes.AddShape(msoShapeChevron, sx, top, step_w, chevron_h)
            chev.Fill.Solid()
            chev.Fill.ForeColor.RGB = hex_to_bgr(brand if is_active else surface)
            chev.Line.Visible = msoTrue
            chev.Line.ForeColor.RGB = hex_to_bgr(brand if is_active else border)
            chev.Line.Weight = 1.5
            step_shapes.append(chev)

            ctf = chev.TextFrame
            ctf.WordWrap = msoTrue
            cp = ctf.TextRange
            cp.Text = f"BƯỚC {s.get('step', str(i+1))}\n{s.get('title', f'Giai Đoạn {i+1}')}"
            cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            cp.Font.Size = 11.5 if count > 4 else 13.5
            cp.Font.Bold = msoTrue
            cp.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_active else ink)
            cp.ParagraphFormat.Alignment = ppAlignCenter

            # Body Card below
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, card_top, step_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if is_active else border)
            card.Line.Weight = 1.5
            step_shapes.append(card)

            # Accent Pill inside card
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx + 14, card_top + 14, step_w - 28, 26.0)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "badge_bg", "#082F49"))
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = f"TIÊU ĐIỂM BƯỚC 0{i+1}"
            pt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            pt.Font.Size = 10.5
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr(brand if is_active else "#38BDF8")
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            step_shapes.append(pill)

            # Body Text Box
            tb_top = card_top + 48.0
            tb_h = card_h - 92.0
            btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 14, tb_top, step_w - 28, tb_h)
            btf = btb.TextFrame
            btf.WordWrap = msoTrue
            btf.MarginLeft = 0
            btf.MarginRight = 0
            bp = btf.TextRange
            bp.Text = s.get("desc", "")
            bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bp.Font.Size = 12.5 if count > 4 else 14.5
            bp.Font.Color.RGB = hex_to_bgr(ink if is_active else muted)
            bp.ParagraphFormat.Alignment = ppAlignLeft
            bp.ParagraphFormat.LineRuleWithin = msoTrue
            bp.ParagraphFormat.SpaceWithin = 1.3
            step_shapes.append(btb)

            # Bottom Key Takeaway Badge
            badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx + 14, card_top + card_h - 36.0, step_w - 28, 24.0)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E2E8F0")
            badge.Line.Visible = msoTrue
            badge.Line.ForeColor.RGB = hex_to_bgr(brand if is_active else border)
            badge.Line.Weight = 1.0
            bt = badge.TextFrame.TextRange
            bt.Text = f"✔ Chuẩn Đầu Ra 0{i+1}"
            bt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bt.Font.Size = 10.0
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr(brand if is_active else muted)
            badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            step_shapes.append(badge)

            # Pre-group each step atomically so clicks animate the entire step synchronously
            step_grp = safe_group(slide, step_shapes, f"Process_Step_{i+1}")
            shapes.append(step_grp)

        return shapes

    # =========================================================================
    # 42. PROCESS_CURVED_PIPELINE (Dòng Chảy Đường Cong Uốn Lượn)
    # =========================================================================
    def render_curved_pipeline(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        stations = data.get("stations", [
            {"num": "01", "name": "Thu Thập Dữ Liệu", "kpi": "100M+ Records/ngày", "desc": "Kết nối API thời gian thực và CDC streaming."},
            {"num": "02", "name": "Xác Thực & Làm Sạch", "kpi": "99.99% Chuẩn Hóa", "desc": "Bộ lọc Schema và thuật toán loại trừ bản ghi rác."},
            {"num": "03", "name": "Phân Tích AI Tức Thời", "kpi": "< 250ms Latency", "desc": "Mô hình Gemini & Embeddings tính điểm tín nhiệm."},
            {"num": "04", "name": "Kích Hoạt Hành Động", "kpi": "Tự Động Hóa 100%", "desc": "Gửi thông báo đa kênh và kích hoạt workflow điều hành."}
        ])

        count = max(2, min(len(stations), 5))
        pipe_y = top + height * 0.42
        pipe_h = 10.0
        pipe = slide.Shapes.AddShape(msoShapeRectangle, left + 40, pipe_y, width - 80, pipe_h)
        pipe.Fill.Solid()
        pipe.Fill.ForeColor.RGB = hex_to_bgr(brand)
        pipe.Line.Visible = msoFalse
        shapes.append(pipe)

        node_w = (width - 60) / count
        for i in range(count):
            st = stations[i]
            nx = left + 30 + i * node_w + (node_w - 50) / 2.0
            is_upper = (i % 2 == 0)

            node = slide.Shapes.AddShape(msoShapeOval, nx, pipe_y - 20, 50, 50)
            node.Fill.Solid()
            node.Fill.ForeColor.RGB = hex_to_bgr(brand)
            node.Line.Visible = msoTrue
            node.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
            node.Line.Weight = 2.5
            shapes.append(node)

            ntf = node.TextFrame
            np = ntf.TextRange
            np.Text = st.get("num", f"0{i+1}")
            np.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            np.Font.Size = 14
            np.Font.Bold = msoTrue
            np.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            np.ParagraphFormat.Alignment = ppAlignCenter

            card_w = node_w - 12.0
            card_h = height * 0.34
            card_x = left + 30 + i * node_w + 6.0
            card_y = top if is_upper else (pipe_y + 40)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, card_x, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, card_x + 10, card_y + 8, card_w - 20, card_h - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = st.get("name", f"Trạm {i+1}") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"★ {st.get('kpi', '')}\n" if st.get("kpi") else ""
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(brand)

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = st.get("desc", "")
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 9.5
            p3.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 43. PROCESS_CIRCULAR_CYCLE (Vòng Tuần Hoàn Quy Trình Khép Kín)
    # =========================================================================
    def render_circular_cycle(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        cycle_name = data.get("core_title", "CHU TRÌNH PDCA\nLIÊN TỤC")
        nodes = data.get("nodes", [
            {"step": "PLAN", "title": "Hoạch Định", "desc": "Thiết lập mục tiêu và kế hoạch hành động chi tiết."},
            {"step": "DO", "title": "Thực Thi", "desc": "Triển khai thí điểm các giải pháp đã được duyệt."},
            {"step": "CHECK", "title": "Kiểm Tra", "desc": "Đo lường các chỉ số KPI so với tiêu chuẩn đề ra."},
            {"step": "ACT", "title": "Cải Tiến", "desc": "Chuẩn hóa quy trình thành công và nhân rộng toàn hệ thống."}
        ])

        count = len(nodes)
        cx = left + width / 2.0
        cy = top + height / 2.0
        radius_x = width * 0.31
        radius_y = height * 0.35

        # Center core badge with outer accent ring (2 shapes -> valid msoGroup)
        core_w = 176.0
        core_h = 96.0
        ring = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx - core_w / 2.0 - 4.0, cy - core_h / 2.0 - 4.0, core_w + 8.0, core_h + 8.0)
        ring.Fill.Solid()
        ring.Fill.ForeColor.RGB = hex_to_bgr(surface)
        ring.Line.Visible = msoTrue
        ring.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "card_border", "#1E293B"))
        ring.Line.Weight = 1.0

        core = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx - core_w / 2.0, cy - core_h / 2.0, core_w, core_h)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(surface)
        core.Line.Visible = msoTrue
        core.Line.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Weight = 2.0

        ctf = core.TextFrame
        ctf.WordWrap = msoTrue
        ctf.MarginLeft = 6
        ctf.MarginRight = 6
        cp = ctf.TextRange
        cp.Text = f"🔄 {cycle_name}"
        cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cp.Font.Size = 12.5
        cp.Font.Bold = msoTrue
        cp.Font.Color.RGB = hex_to_bgr(brand)
        cp.ParagraphFormat.Alignment = ppAlignCenter
        core_grp = safe_group(slide, [ring, core], "Cycle_Core_Group")
        shapes.append(core_grp)

        node_w = 248.0
        node_h = 104.0

        for i in range(count):
            nd = nodes[i]
            angle = (2 * math.pi / count) * i - (math.pi / 2.0)
            nx = cx + radius_x * math.cos(angle) - (node_w / 2.0)
            ny = cy + radius_y * math.sin(angle) - (node_h / 2.0)

            n_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, nx, ny, node_w, node_h)
            n_card.Fill.Solid()
            n_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            n_card.Line.Visible = msoTrue
            n_card.Line.ForeColor.RGB = hex_to_bgr(brand if i == 0 else border)
            n_card.Line.Weight = 1.8 if i == 0 else 1.2

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, nx + 12, ny + 10, node_w - 24, node_h - 18)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{nd.get('step', f'BƯỚC 0{i+1}')}: {nd.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 13.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if i == 0 else ink)
            p1.ParagraphFormat.SpaceAfter = 5

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = nd.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 11.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            try:
                p2.ParagraphFormat.SpaceWithin = 1.22
            except Exception:
                pass

            node_grp = safe_group(slide, [n_card, tb], f"Cycle_Node_{i+1}")
            shapes.append(node_grp)

        return shapes

    # =========================================================================
    # 44. PROCESS_INTERLOCKING_GEARS (Cơ Chế Bánh Răng Ăn Khớp)
    # =========================================================================
    def render_interlocking_gears(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        gears = data.get("gears", [
            {"title": "BÁNH RĂNG DỮ LIỆU", "role": "Nhiên liệu cốt lõi", "desc": "Dữ liệu lớn thời gian thực nạp liên tục vào hệ thống."},
            {"title": "BÁNH RĂNG THUẬT TOÁN", "role": "Bộ máy xử lý", "desc": "Mô hình học máy tinh chỉnh tối ưu hóa theo chu kỳ."},
            {"title": "BÁNH RĂNG THỰC THI", "role": "Tác động đầu ra", "desc": "Quy trình vận hành chuyển hóa giải pháp thành doanh thu."}
        ])

        count = len(gears)
        col_w = (width - (count - 1) * 16.0) / count
        gear_d = min(col_w * 0.65, 120.0)

        for i in range(count):
            g = gears[i]
            gx = left + i * (col_w + 16.0)
            gy = top + (height - 240.0) / 2.0
            is_center = (i == 1)

            gear_shape = slide.Shapes.AddShape(msoShapeDonut, gx + (col_w - gear_d) / 2.0, gy, gear_d, gear_d)
            gear_shape.Fill.Solid()
            gear_shape.Fill.ForeColor.RGB = hex_to_bgr(brand if is_center else surface)
            gear_shape.Line.Visible = msoTrue
            gear_shape.Line.ForeColor.RGB = hex_to_bgr(brand)
            gear_shape.Line.Weight = 2.0
            shapes.append(gear_shape)

            in_lbl = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, gx + (col_w - gear_d) / 2.0, gy + (gear_d - 30)/2.0, gear_d, 30)
            in_tf = in_lbl.TextFrame
            in_tf.WordWrap = msoTrue
            inp = in_tf.TextRange
            inp.Text = f"GEAR 0{i+1}"
            inp.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            inp.Font.Size = 11
            inp.Font.Bold = msoTrue
            inp.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_center else brand)
            inp.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(in_lbl)

            card_y = gy + gear_d + 16.0
            card_h = 100.0
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, gx, card_y, col_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, gx + 10, card_y + 8, col_w - 20, card_h - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = g.get("title", f"Thành Phần {i+1}") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(ink)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = g.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 45. PROCESS_FISHBONE_ISHIKAWA (Biểu Đồ Xương Cá Ishikawa)
    # =========================================================================
    def render_fishbone_ishikawa(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")
        danger = self._get_token("colors", "danger", "#EF4444")

        data = spec.get("process_data", {})
        effect = data.get("effect", "VẤN ĐỀ TRỌNG YẾU\nCHƯA ĐẠT CHỈ TIÊU")
        causes = data.get("causes", [
            {"cat": "CON NGƯỜI (PEOPLE)", "items": "• Thiếu đào tạo chuyên sâu\n• Tỷ lệ biến động nhân sự cao"},
            {"cat": "QUY TRÌNH (PROCESS)", "items": "• Thiếu tiêu chuẩn SOP\n• Phê duyệt đa tầng kéo dài"},
            {"cat": "CÔNG NGHỆ (TECH)", "items": "• Hệ thống Legacy cũ kỹ\n• Dữ liệu phân tán nhiều nguồn"},
            {"cat": "CHÍNH SÁCH (POLICY)", "items": "• Cơ chế thưởng phạt chưa rõ\n• Ngân sách R&D bị cắt giảm"}
        ])

        head_w = 160.0
        head_h = 90.0
        head_x = left + width - head_w
        head_y = top + (height - head_h) / 2.0

        head = slide.Shapes.AddShape(msoShapeRoundedRectangle, head_x, head_y, head_w, head_h)
        head.Fill.Solid()
        head.Fill.ForeColor.RGB = hex_to_bgr(surface)
        head.Line.Visible = msoTrue
        head.Line.ForeColor.RGB = hex_to_bgr(danger)
        head.Line.Weight = 2.5
        shapes.append(head)

        htf = head.TextFrame
        htf.WordWrap = msoTrue
        hp = htf.TextRange
        hp.Text = effect
        hp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        hp.Font.Size = 11.5
        hp.Font.Bold = msoTrue
        hp.Font.Color.RGB = hex_to_bgr(danger)
        hp.ParagraphFormat.Alignment = ppAlignCenter

        spine_y = top + height / 2.0 - 4.0
        spine = slide.Shapes.AddShape(msoShapeRightArrow, left, spine_y, width - head_w - 10.0, 8.0)
        spine.Fill.Solid()
        spine.Fill.ForeColor.RGB = hex_to_bgr(brand)
        spine.Line.Visible = msoFalse
        shapes.append(spine)

        rib_w = (width - head_w - 40.0) / 2.0
        for i, c in enumerate(causes[:4]):
            col = i % 2
            is_top = (i < 2)
            rx = left + col * (rib_w + 12.0)
            ry = top + 10.0 if is_top else (spine_y + 35.0)
            rh = (height / 2.0) - 50.0

            rcard = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rib_w, rh)
            rcard.Fill.Solid()
            rcard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            rcard.Line.Visible = msoTrue
            rcard.Line.ForeColor.RGB = hex_to_bgr(brand)
            rcard.Line.Weight = 1.2
            shapes.append(rcard)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, ry + 6, rib_w - 20, rh - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = c.get("cat", "") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = c.get("items", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 46. PROCESS_DECISION_FLOW (Sơ Đồ Cây Quyết Định - Decision Tree)
    # =========================================================================
    def render_decision_flow(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")
        success = self._get_token("colors", "success", "#10B981")
        danger = self._get_token("colors", "danger", "#EF4444")

        data = spec.get("process_data", {})
        root_text = data.get("root", "1. Tiếp Nhận Yêu Cầu")
        decision_text = data.get("decision", "Đạt Tiêu Chuẩn\nĐầu Vào?")
        yes_outcome = data.get("yes_outcome", "Chấp Thuận: Kích Hoạt Tự Động")
        no_outcome = data.get("no_outcome", "Từ Chối: Chuyển Sang Thủ Công")

        col_w = width * 0.28
        r_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + (height - 65)/2.0, col_w, 65)
        r_box.Fill.Solid()
        r_box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        r_box.Line.Visible = msoTrue
        r_box.Line.ForeColor.RGB = hex_to_bgr(border)
        r_box.Line.Weight = 1.5
        shapes.append(r_box)

        rtf = r_box.TextFrame
        rtf.WordWrap = msoTrue
        rp = rtf.TextRange
        rp.Text = root_text
        rp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        rp.Font.Size = 11
        rp.Font.Bold = msoTrue
        rp.Font.Color.RGB = hex_to_bgr(ink)
        rp.ParagraphFormat.Alignment = ppAlignCenter

        arr1 = slide.Shapes.AddShape(msoShapeRightArrow, left + col_w + 5, top + height/2.0 - 4, 30, 8)
        arr1.Fill.Solid()
        arr1.Fill.ForeColor.RGB = hex_to_bgr(brand)
        arr1.Line.Visible = msoFalse
        shapes.append(arr1)

        dia_x = left + col_w + 40
        dia_w = width * 0.28
        dia_h = 100.0
        dia = slide.Shapes.AddShape(msoShapeDiamond, dia_x, top + (height - dia_h)/2.0, dia_w, dia_h)
        dia.Fill.Solid()
        dia.Fill.ForeColor.RGB = hex_to_bgr(brand)
        dia.Line.Visible = msoTrue
        dia.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
        dia.Line.Weight = 2.0
        shapes.append(dia)

        dtf = dia.TextFrame
        dtf.WordWrap = msoTrue
        dp = dtf.TextRange
        dp.Text = decision_text
        dp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        dp.Font.Size = 11
        dp.Font.Bold = msoTrue
        dp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        dp.ParagraphFormat.Alignment = ppAlignCenter

        out_x = dia_x + dia_w + 35
        out_w = width - (out_x - left)
        out_h = 75.0

        yes_y = top + 20.0
        yes_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, out_x, yes_y, out_w, out_h)
        yes_box.Fill.Solid()
        yes_box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        yes_box.Line.Visible = msoTrue
        yes_box.Line.ForeColor.RGB = hex_to_bgr(success)
        yes_box.Line.Weight = 2.0
        shapes.append(yes_box)

        ytf = yes_box.TextFrame
        ytf.WordWrap = msoTrue
        yp = ytf.TextRange
        yp.Text = f"[ĐẠT - YES]\n{yes_outcome}"
        yp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        yp.Font.Size = 10.5
        yp.Font.Bold = msoTrue
        yp.Font.Color.RGB = hex_to_bgr(success)
        yp.ParagraphFormat.Alignment = ppAlignCenter

        no_y = top + height - out_h - 20.0
        no_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, out_x, no_y, out_w, out_h)
        no_box.Fill.Solid()
        no_box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        no_box.Line.Visible = msoTrue
        no_box.Line.ForeColor.RGB = hex_to_bgr(danger)
        no_box.Line.Weight = 2.0
        shapes.append(no_box)

        ntf = no_box.TextFrame
        ntf.WordWrap = msoTrue
        np = ntf.TextRange
        np.Text = f"[KHÔNG ĐẠT - NO]\n{no_outcome}"
        np.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        np.Font.Size = 10.5
        np.Font.Bold = msoTrue
        np.Font.Color.RGB = hex_to_bgr(danger)
        np.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # =========================================================================
    # 47. PROCESS_SWIMLANE_TRACKS (Sơ Đồ Phân Làn Đa Tầng Swimlane)
    # =========================================================================
    def render_swimlane_tracks(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        lanes = data.get("lanes")
        if not lanes:
            atoms = spec.get("atoms", [])
            if atoms:
                lanes = []
                for i, a in enumerate(atoms[:4]):
                    d = a.get("title", f"CẤP ĐỘ 0{i+1}")
                    t = a.get("text") or a.get("desc") or ""
                    lanes.append({"dept": d, "task": t})
            else:
                lanes = [
                    {"dept": "TRUNG ƯƠNG", "task": "Ban hành chiến lược, khung pháp lý và phân bổ ngân sách quốc gia."},
                    {"dept": "TỈNH / THÀNH PHỐ", "task": "Lập kế hoạch hành động, điều phối mạng lưới và giám sát chất lượng."},
                    {"dept": "Y TẾ CƠ SỞ", "task": "Trực tiếp cung ứng dịch vụ dân số, tư vấn và quản lý địa bàn."},
                    {"dept": "CỘNG ĐỒNG", "task": "Chủ động tham gia, thụ hưởng và thực hiện trách nhiệm tài chính."}
                ]

        count = len(lanes)
        gap = 10.0
        lane_h = (height - (count - 1) * gap) / count
        header_w = 160.0

        for i in range(count):
            ln = lanes[i]
            ly = top + i * (lane_h + gap)
            lane_shapes = []

            # 1. Lane Header
            hdr = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ly, header_w, lane_h)
            hdr.Fill.Solid()
            hdr.Fill.ForeColor.RGB = hex_to_bgr(brand if i == 0 else "#1E293B")
            hdr.Line.Visible = msoTrue
            hdr.Line.ForeColor.RGB = hex_to_bgr(brand)
            hdr.Line.Weight = 1.5 if i == 0 else 1.0
            lane_shapes.append(hdr)

            htf = hdr.TextFrame
            htf.WordWrap = msoTrue
            hp = htf.TextRange
            hp.Text = ln.get("dept", f"LÀN 0{i+1}")
            hp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            hp.Font.Size = 12.0
            hp.Font.Bold = msoTrue
            hp.Font.Color.RGB = hex_to_bgr("#FFFFFF" if i == 0 else self._get_token("colors", "brand", "#38BDF8"))
            hp.ParagraphFormat.Alignment = ppAlignCenter

            # 2. Track Surface
            track_w = width - header_w - 8.0
            track = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + header_w + 8.0, ly, track_w, lane_h)
            track.Fill.Solid()
            track.Fill.ForeColor.RGB = hex_to_bgr(surface)
            track.Line.Visible = msoTrue
            track.Line.ForeColor.RGB = hex_to_bgr(border)
            track.Line.Weight = 1.0
            lane_shapes.append(track)

            # 3. Action Task Box inside track
            box_w = track_w - 32.0
            box_x = left + header_w + 24.0
            tbox = slide.Shapes.AddShape(msoShapeRoundedRectangle, box_x, ly + 8.0, box_w, lane_h - 16.0)
            tbox.Fill.Solid()
            tbox.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "badge_bg", "#082F49"))
            tbox.Line.Visible = msoTrue
            tbox.Line.ForeColor.RGB = hex_to_bgr(brand)
            tbox.Line.Weight = 1.0
            lane_shapes.append(tbox)

            tbt = tbox.TextFrame
            tbt.WordWrap = msoTrue
            tbt.MarginLeft = 14
            tbt.MarginRight = 14
            tp = tbt.TextRange
            tp.Text = ln.get("task", "")
            tp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            tp.Font.Size = 12.5
            tp.Font.Color.RGB = hex_to_bgr(ink)
            tp.ParagraphFormat.Alignment = ppAlignLeft
            tp.ParagraphFormat.LineRuleWithin = msoTrue
            tp.ParagraphFormat.SpaceWithin = 1.25

            # Atomic encapsulation per lane
            lane_grp = safe_group(slide, lane_shapes, f"Swimlane_Lane_{i+1}")
            shapes.append(lane_grp)

        return shapes

    # =========================================================================
    # 48. PROCESS_ASCENDING_STAIRS (Bậc Thang Tiến Độ Nâng Tầng)
    # =========================================================================
    def render_ascending_stairs(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        stairs = data.get("stairs", [
            {"level": "BẬC 1", "kpi": "15%", "title": "Khởi Đầu Thử Nghiệm", "desc": "Thiết lập hệ thống nền tảng."},
            {"level": "BẬC 2", "kpi": "40%", "title": "Chuẩn Hóa Quy Trình", "desc": "Áp dụng toàn bộ phòng ban."},
            {"level": "BẬC 3", "kpi": "75%", "title": "Mở Rộng Quy Mô", "desc": "Tích hợp đa kênh thị trường."},
            {"level": "BẬC 4", "kpi": "100%", "title": "Dẫn Đầu Thị Trường", "desc": "Tự động hóa hoàn toàn với AI."}
        ])

        count = len(stairs)
        step_w = (width - (count - 1) * 12.0) / count
        base_y = top + height

        for i in range(count):
            st = stairs[i]
            sx = left + i * (step_w + 12.0)
            sh = height * (0.35 + (0.65 * (i + 1) / count))
            sy = base_y - sh
            is_top = (i == count - 1)

            step_box = slide.Shapes.AddShape(msoShapeRectangle, sx, sy, step_w, sh)
            step_box.Fill.Solid()
            step_box.Fill.ForeColor.RGB = hex_to_bgr(brand if is_top else surface)
            step_box.Line.Visible = msoTrue
            step_box.Line.ForeColor.RGB = hex_to_bgr(brand)
            step_box.Line.Weight = 1.5

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 8, sy + 10, step_w - 16, sh - 20)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{st.get('level', '')} ({st.get('kpi', '')})\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 12
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_top else brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = st.get("title", "") + "\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 12
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_top else ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = st.get("desc", "")
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 10.5
            p3.Font.Color.RGB = hex_to_bgr("#E2E8F0" if is_top else muted)
            try:
                p3.ParagraphFormat.SpaceWithin = 1.2
            except Exception:
                pass
            p3.ParagraphFormat.Alignment = ppAlignCenter

            step_grp = safe_group(slide, [step_box, tb], f"Stairs_Step_{i+1}")
            shapes.append(step_grp)

        return shapes

    # =========================================================================
    # 49. PROCESS_TIMELINE_FLAG_RIBBON (Dải Ruy Băng Mốc Thời Gian)
    # =========================================================================
    def render_timeline_flag_ribbon(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        milestones = data.get("milestones")
        if not milestones:
            atoms = spec.get("atoms", [])
            if atoms:
                milestones = []
                for i, a in enumerate(atoms[:4]):
                    d = a.get("num") or f"GIAI ĐOẠN 0{i+1}"
                    t = a.get("title", f"Mốc 0{i+1}")
                    dsc = a.get("text") or a.get("desc") or ""
                    milestones.append({"date": d, "title": t, "desc": dsc})
            else:
                milestones = [
                    {"date": "Giai Đoạn 1", "title": "Khảo Sát & Đánh Giá", "desc": "Nghiên cứu thực trạng địa bàn và xác định nhu cầu dịch vụ thiết yếu."},
                    {"date": "Giai Đoạn 2", "title": "Thiết Kế Mô Hình", "desc": "Chuẩn hóa phác đồ can thiệp và tập huấn kỹ thuật cho đội ngũ y tế cơ sở."},
                    {"date": "Giai Đoạn 3", "title": "Triển Khai Cung Ứng", "desc": "Mở rộng độ bao phủ dịch vụ gắn liền tiếp thị xã hội và truyền thông."},
                    {"date": "Giai Đoạn 4", "title": "Đánh Giá Tác Động", "desc": "Nghiệm thu chỉ số đầu ra và duy trì tính bền vững tài chính."}
                ]

        count = len(milestones)
        spine_y = top + 75.0
        ribbon = slide.Shapes.AddShape(msoShapeRectangle, left, spine_y, width, 5.0)
        ribbon.Fill.Solid()
        ribbon.Fill.ForeColor.RGB = hex_to_bgr(brand)
        ribbon.Line.Visible = msoFalse
        shapes.append(ribbon)

        col_w = (width - (count - 1) * 16.0) / count
        for i in range(count):
            m = milestones[i]
            mx = left + i * (col_w + 16.0)
            step_shapes = []

            # 1. Flag Header
            flag = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx + (col_w - 110)/2.0, top + 32.0, 110, 32)
            flag.Fill.Solid()
            flag.Fill.ForeColor.RGB = hex_to_bgr(brand if i == 0 else "#0369A1")
            flag.Line.Visible = msoFalse
            step_shapes.append(flag)

            ftf = flag.TextFrame
            fp = ftf.TextRange
            fp.Text = m.get("date", f"MỐC 0{i+1}")
            fp.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            fp.Font.Size = 11.5
            fp.Font.Bold = msoTrue
            fp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            fp.ParagraphFormat.Alignment = ppAlignCenter

            # 2. Main Card Body
            card_y = spine_y + 20.0
            card_h = height - (card_y - top) - 10.0
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx, card_y, col_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if i == 0 else border)
            card.Line.Weight = 1.5 if i == 0 else 1.0
            step_shapes.append(card)

            # 3. Text Block
            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, mx + 12, card_y + 12, col_w - 24, card_h - 52)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginTop = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = m.get("title", "") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 14.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(ink)
            p1.ParagraphFormat.Alignment = ppAlignCenter
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = m.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 12.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            p2.ParagraphFormat.LineRuleWithin = msoTrue
            p2.ParagraphFormat.SpaceWithin = 1.3
            step_shapes.append(tb)

            # 4. Bottom Anchor Badge
            badge_y = card_y + card_h - 34.0
            badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx + 12, badge_y, col_w - 24, 22.0)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr("#0F172A" if self.theme == "DARK" else "#E2E8F0")
            badge.Line.Visible = msoTrue
            badge.Line.ForeColor.RGB = hex_to_bgr(brand if i == 0 else border)
            badge.Line.Weight = 1.0
            bt = badge.TextFrame.TextRange
            bt.Text = f"✔ Chuẩn Đầu Ra 0{i+1}"
            bt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bt.Font.Size = 10.0
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr(brand if i == 0 else muted)
            bt.ParagraphFormat.Alignment = ppAlignCenter
            step_shapes.append(badge)

            # Atomic encapsulation per milestone
            step_grp = safe_group(slide, step_shapes, f"Timeline_Step_{i+1}")
            shapes.append(step_grp)

        return shapes

    # =========================================================================
    # 50. PROCESS_VERTICAL_SPINE (Trục Xương Sống Thời Gian Dọc)
    # =========================================================================
    def render_vertical_spine(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        events = data.get("events", [
            {"year": "2021", "title": "Khởi Sự Nghiên Cứu", "desc": "Thành lập đội ngũ kiến trúc sư hạt nhân."},
            {"year": "2022", "title": "Xây Dựng Engine", "desc": "Ra mắt thế hệ render slide bán tự động đầu tiên."},
            {"year": "2023", "title": "Bùng Nổ Tác Tử AI", "desc": "Nâng cấp hệ sinh thái 16 chuyên gia AI độc lập."},
            {"year": "2024", "title": "Dẫn Đầu Quốc Tế", "desc": "Đạt chuẩn Mega Library 110+ Archetypes đỉnh cao."}
        ])

        count = len(events)
        cx = left + width / 2.0
        spine = slide.Shapes.AddShape(msoShapeRectangle, cx - 3.0, top, 6.0, height)
        spine.Fill.Solid()
        spine.Fill.ForeColor.RGB = hex_to_bgr(brand)
        spine.Line.Visible = msoFalse
        shapes.append(spine)

        row_h = (height - (count - 1) * 10.0) / count
        card_w = (width / 2.0) - 45.0

        for i in range(count):
            ev = events[i]
            ry = top + i * (row_h + 10.0)
            is_left = (i % 2 == 0)

            node = slide.Shapes.AddShape(msoShapeOval, cx - 12.0, ry + (row_h - 24.0)/2.0, 24, 24)
            node.Fill.Solid()
            node.Fill.ForeColor.RGB = hex_to_bgr(brand)
            node.Line.Visible = msoTrue
            node.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
            node.Line.Weight = 2.0
            shapes.append(node)

            card_x = (left + 10.0) if is_left else (cx + 35.0)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, card_x, ry, card_w, row_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, card_x + 10, ry + 6, card_w - 20, row_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"[{ev.get('year', '')}] {ev.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = ev.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 51. PROCESS_GANTT_ROADMAP (Sơ Đồ Thanh Tiến Độ Gantt)
    # =========================================================================
    def render_gantt_roadmap(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        columns = data.get("columns", ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6"])
        tasks = data.get("tasks", [
            {"name": "Giai Đoạn 1: Thiết Kế Kiến Trúc", "start": 0, "span": 2},
            {"name": "Giai Đoạn 2: Lập Trình Lõi Engine", "start": 1, "span": 3},
            {"name": "Giai Đoạn 3: Tích Hợp 16 AI Agents", "start": 3, "span": 2},
            {"name": "Giai Đoạn 4: Bàn Giao & Vận Hành", "start": 4, "span": 2}
        ])

        header_w = 160.0
        time_w = width - header_w - 10.0
        num_cols = len(columns)
        col_w = time_w / num_cols

        for c_idx, col in enumerate(columns):
            cx = left + header_w + 10.0 + c_idx * col_w
            chdr = slide.Shapes.AddShape(msoShapeRectangle, cx, top, col_w - 2.0, 26)
            chdr.Fill.Solid()
            chdr.Fill.ForeColor.RGB = hex_to_bgr(surface)
            chdr.Line.Visible = msoTrue
            chdr.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(chdr)

            ctf = chdr.TextFrame
            cp = ctf.TextRange
            cp.Text = col
            cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            cp.Font.Size = 9.5
            cp.Font.Bold = msoTrue
            cp.Font.Color.RGB = hex_to_bgr(muted)
            cp.ParagraphFormat.Alignment = ppAlignCenter

        row_h = (height - 35.0 - (len(tasks) - 1) * 8.0) / len(tasks)
        for r_idx, t in enumerate(tasks):
            ry = top + 35.0 + r_idx * (row_h + 8.0)

            thdr = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ry, header_w, row_h)
            thdr.Fill.Solid()
            thdr.Fill.ForeColor.RGB = hex_to_bgr(surface)
            thdr.Line.Visible = msoTrue
            thdr.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(thdr)

            ttf = thdr.TextFrame
            ttf.WordWrap = msoTrue
            tp = ttf.TextRange
            tp.Text = t.get("name", "")
            tp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            tp.Font.Size = 9.5
            tp.Font.Bold = msoTrue
            tp.Font.Color.RGB = hex_to_bgr(ink)
            tp.ParagraphFormat.Alignment = ppAlignLeft

            start_col = t.get("start", 0)
            span_cols = t.get("span", 1)
            bar_x = left + header_w + 10.0 + start_col * col_w
            bar_w = span_cols * col_w - 4.0

            bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, bar_x, ry + 4.0, bar_w, row_h - 8.0)
            bar.Fill.Solid()
            bar.Fill.ForeColor.RGB = hex_to_bgr(brand)
            bar.Line.Visible = msoFalse
            shapes.append(bar)

        return shapes

    # =========================================================================
    # 52. PROCESS_3_HORIZONS_ROADMAP (Lộ Trình 3 Chân Trời McKinsey)
    # =========================================================================
    def render_3_horizons_roadmap(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        horizons = data.get("horizons", [
            {"h": "CHÂN TRỜI 1 (HIỆN TẠI)", "time": "0 - 12 Tháng", "focus": "Bảo Vệ & Tối Ưu Lõi Kinh Doanh", "desc": "Nâng cao hiệu suất vận hành, giảm chi phí."},
            {"h": "CHÂN TRỜI 2 (CHUYỂN TIẾP)", "time": "1 - 3 Năm", "focus": "Nuôi Dưỡng Cơ Hội Đột Phá", "desc": "Mở rộng phân khúc khách hàng mới và đối tác."},
            {"h": "CHÂN TRỜI 3 (TƯƠNG LAI)", "time": "3 - 5 Năm", "focus": "Kiến Tạo Tương Lai Dài Hạn", "desc": "Đầu tư vào công nghệ AI tự chủ và thị trường toàn cầu."}
        ])

        col_w = (width - 2 * 16.0) / 3.0
        for i, h in enumerate(horizons[:3]):
            hx = left + i * (col_w + 16.0)
            card_h = height * (0.65 + i * 0.15)
            hy = top + (height - card_h)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, hx, hy, col_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.5 + i * 0.5
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, hx + 12, hy + 12, col_w - 24, card_h - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{h.get('h', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"Thời Gian: {h.get('time', '')}\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr(ink)

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = f"Trọng Tâm: {h.get('focus', '')}\n\n{h.get('desc', '')}"
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 9.0
            p3.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 53. PROCESS_AGILE_SCRUM_CYCLE (Chu Trình Agile / Scrum Sprint)
    # =========================================================================
    def render_agile_scrum_cycle(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        stage_w = width * 0.28
        center_w = width * 0.38
        gap = (width - 2 * stage_w - center_w) / 2.0

        b_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + 20, stage_w, height - 40)
        b_card.Fill.Solid()
        b_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        b_card.Line.Visible = msoTrue
        b_card.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(b_card)

        btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 10, top + 35, stage_w - 20, height - 70)
        btf = btb.TextFrame
        btf.WordWrap = msoTrue
        bp = btf.TextRange
        bp.Text = "PRODUCT BACKLOG\n\n• Yêu cầu người dùng\n• Tính năng mới\n• Sửa lỗi & Nâng cấp\n• Ưu tiên theo giá trị"
        bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp.Font.Size = 10
        bp.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(btb)

        cx = left + stage_w + gap
        s_card = slide.Shapes.AddShape(msoShapeOval, cx + (center_w - 180)/2.0, top + (height - 180)/2.0, 180, 180)
        s_card.Fill.Solid()
        s_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        s_card.Line.Visible = msoTrue
        s_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        s_card.Line.Weight = 3.0
        shapes.append(s_card)

        stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + (center_w - 160)/2.0, top + (height - 100)/2.0, 160, 100)
        stf = stb.TextFrame
        stf.WordWrap = msoTrue
        sp = stf.TextRange
        sp.Text = "SPRINT 2-4 TUẦN\n\n• Daily Standup\n• Sprint Review\n• Retrospective"
        sp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        sp.Font.Size = 10
        sp.Font.Bold = msoTrue
        sp.Font.Color.RGB = hex_to_bgr(brand)
        sp.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(stb)

        rx = left + stage_w + gap + center_w + gap
        o_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top + 20, stage_w, height - 40)
        o_card.Fill.Solid()
        o_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        o_card.Line.Visible = msoTrue
        o_card.Line.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "success", "#10B981"))
        o_card.Line.Weight = 2.0
        shapes.append(o_card)

        otb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, top + 35, stage_w - 20, height - 70)
        otf = otb.TextFrame
        otf.WordWrap = msoTrue
        op = otf.TextRange
        op.Text = "BÀN GIAO SẢN PHẨM\n\n• Tính năng hoàn chỉnh\n• Sẵn sàng triển khai\n• Phản hồi khách hàng\n• Đánh giá chất lượng"
        op.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        op.Font.Size = 10
        op.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(otb)

        return shapes

    # =========================================================================
    # 54. PROCESS_BRIDGE_MIGRATION (Cầu Nối Chuyển Dịch Hệ Thống)
    # =========================================================================
    def render_bridge_migration(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        as_is = data.get("as_is", "HIỆN TRẠNG (AS-IS)\n• Hạ tầng phân tán cũ\n• Thao tác thủ công 80%\n• Chi phí vận hành cao")
        to_be = data.get("to_be", "TƯƠNG LAI (TO-BE)\n• Đám mây hợp nhất\n• Tự động hóa 95%\n• Tối ưu 60% chi phí")
        bridge_steps = data.get("steps", ["1. Di Chuyển Data", "2. Tái Cấu Trúc Code", "3. Đào Tạo Nhân Sự"])

        pillar_w = width * 0.28
        bridge_w = width - 2 * pillar_w - 20.0

        lp = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + 20, pillar_w, height - 40)
        lp.Fill.Solid()
        lp.Fill.ForeColor.RGB = hex_to_bgr(surface)
        lp.Line.Visible = msoTrue
        lp.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(lp)

        ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 10, top + 35, pillar_w - 20, height - 70)
        ltf = ltb.TextFrame
        ltf.WordWrap = msoTrue
        lp_p = ltf.TextRange
        lp_p.Text = as_is
        lp_p.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        lp_p.Font.Size = 10
        lp_p.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(ltb)

        rx = left + width - pillar_w
        rp = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top + 20, pillar_w, height - 40)
        rp.Fill.Solid()
        rp.Fill.ForeColor.RGB = hex_to_bgr(surface)
        rp.Line.Visible = msoTrue
        rp.Line.ForeColor.RGB = hex_to_bgr(brand)
        rp.Line.Weight = 2.0
        shapes.append(rp)

        rtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, top + 35, pillar_w - 20, height - 70)
        rtf = rtb.TextFrame
        rtf.WordWrap = msoTrue
        rp_p = rtf.TextRange
        rp_p.Text = to_be
        rp_p.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        rp_p.Font.Size = 10
        rp_p.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(rtb)

        bx = left + pillar_w + 10.0
        by = top + height / 2.0 - 25.0
        b_span = slide.Shapes.AddShape(msoShapeRectangle, bx, by, bridge_w, 50.0)
        b_span.Fill.Solid()
        b_span.Fill.ForeColor.RGB = hex_to_bgr(brand)
        b_span.Line.Visible = msoFalse
        shapes.append(b_span)

        btf = b_span.TextFrame
        btf.WordWrap = msoTrue
        bp = btf.TextRange
        bp.Text = "CẦU NỐI CHUYỂN ĐỔI: " + " → ".join(bridge_steps)
        bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp.Font.Size = 9.5
        bp.Font.Bold = msoTrue
        bp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        bp.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # =========================================================================
    # 55. PROCESS_JIGSAW_PUZZLE (Mảnh Ghép Xếp Hình Interlocking)
    # =========================================================================
    def render_jigsaw_puzzle(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        pieces = spec.get("process_data", {}).get("pieces", [
            {"title": "MẢNH 1: CHIẾN LƯỢC", "desc": "Định hướng mục tiêu cốt lõi."},
            {"title": "MẢNH 2: CÔNG NGHỆ", "desc": "Hạ tầng thực thi mạnh mẽ."},
            {"title": "MẢNH 3: CON NGƯỜI", "desc": "Đội ngũ chuyên nghiệp tận tâm."},
            {"title": "MẢNH 4: VĂN HÓA", "desc": "Tương hỗ gắn kết bền vững."}
        ])

        pw = (width - 12.0) / 2.0
        ph = (height - 12.0) / 2.0
        coords = [
            (left, top),
            (left + pw + 12.0, top),
            (left, top + ph + 12.0),
            (left + pw + 12.0, top + ph + 12.0)
        ]

        for i in range(4):
            px, py = coords[i]
            p_data = pieces[i]
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, px, py, pw, ph)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.5
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, px + 12, py + 12, pw - 24, ph - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = p_data.get("title", "") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 56. PROCESS_HONEYCOMB_CHAIN (Chuỗi Mắt Xích Tổ Ong Lục Giác)
    # =========================================================================
    def render_honeycomb_chain(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        hexes = spec.get("process_data", {}).get("hexagons", [
            {"num": "1", "title": "Khám Phá", "desc": "Định vị bài toán."},
            {"num": "2", "title": "Định Nghĩa", "desc": "Xác lập tiêu chuẩn."},
            {"num": "3", "title": "Phát Triển", "desc": "Mã hóa giải pháp."},
            {"num": "4", "title": "Kiểm Thử", "desc": "Đảm bảo chất lượng."},
            {"num": "5", "title": "Vận Hành", "desc": "Duy trì bền vững."}
        ])

        count = len(hexes)
        hex_w = (width - (count - 1) * 8.0) / count
        hex_h = min(height * 0.7, 180.0)
        hy = top + (height - hex_h) / 2.0

        for i in range(count):
            hx = left + i * (hex_w + 8.0)
            h_data = hexes[i]

            h_shape = slide.Shapes.AddShape(msoShapeHexagon, hx, hy, hex_w, hex_h)
            h_shape.Fill.Solid()
            h_shape.Fill.ForeColor.RGB = hex_to_bgr(surface)
            h_shape.Line.Visible = msoTrue
            h_shape.Line.ForeColor.RGB = hex_to_bgr(brand)
            h_shape.Line.Weight = 1.5
            shapes.append(h_shape)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, hx + 10, hy + hex_h * 0.2, hex_w - 20, hex_h * 0.6)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"0{h_data.get('num', i+1)}\n{h_data.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = h_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 8.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 57. PROCESS_ETL_DATA_PIPELINE (Đường Ống Xử Lý Dữ Liệu ETL)
    # =========================================================================
    def render_etl_data_pipeline(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        stages = spec.get("process_data", {}).get("stages", [
            {"step": "EXTRACT", "name": "Thu Nạp Dữ Liệu", "tools": "Kafka, PubSub, CDC", "desc": "Hấp thụ nguồn dữ liệu thô từ IoT và DB."},
            {"step": "CLEAN", "name": "Làm Sạch & Lọc", "tools": "Dataform, dbt", "desc": "Loại bỏ trùng lặp và chuẩn hóa trường thông tin."},
            {"step": "TRANSFORM", "name": "Chuyển Đổi & ML", "tools": "BigQuery, Spark", "desc": "Mô hình hóa dữ liệu theo chuẩn đa chiều."},
            {"step": "SERVE", "name": "Xuất Bản Trực Quan", "tools": "Looker, PowerBI, App", "desc": "Cung cấp báo cáo thời gian thực cho ban điều hành."}
        ])

        count = len(stages)
        card_w = (width - (count - 1) * 12.0) / count

        for i in range(count):
            st = stages[i]
            sx = left + i * (card_w + 12.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, top, card_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 10, top + 15, card_w - 20, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"[{st.get('step', '')}]\n{st.get('name', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"Công Cụ: {st.get('tools', '')}\n\n{st.get('desc', '')}"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 58. PROCESS_LEVEL_UP_LADDER (Chiếc Thang Nâng Tầm Năng Lực)
    # =========================================================================
    def render_level_up_ladder(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        levels = spec.get("process_data", {}).get("levels", [
            {"lvl": "CẤP 1", "title": "Nhận Thức Cơ Bản", "desc": "Nắm vững lý thuyết cốt lõi."},
            {"lvl": "CẤP 2", "title": "Thực Hành Thành Thạo", "desc": "Áp dụng độc lập vào dự án."},
            {"lvl": "CẤP 3", "title": "Tối Ưu & Sáng Tạo", "desc": "Cải tiến phương pháp luận mới."},
            {"lvl": "CẤP 4", "title": "Dẫn Dắt & Đào Tạo", "desc": "Huấn luyện thế hệ kế thừa."}
        ])

        count = len(levels)
        rung_h = (height - (count - 1) * 10.0) / count

        for i in range(count):
            inv_idx = count - 1 - i
            lvl_data = levels[i]
            ly = top + inv_idx * (rung_h + 10.0)

            rung = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ly, width, rung_h)
            rung.Fill.Solid()
            rung.Fill.ForeColor.RGB = hex_to_bgr(surface)
            rung.Line.Visible = msoTrue
            rung.Line.ForeColor.RGB = hex_to_bgr(brand if inv_idx == 0 else border)
            rung.Line.Weight = 2.0 if inv_idx == 0 else 1.0
            shapes.append(rung)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 18, ly + 6, width - 36, rung_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"★ {lvl_data.get('lvl', '')} - {lvl_data.get('title', '')}: "
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if inv_idx == 0 else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = lvl_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 10
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 59. PROCESS_DOMINO_CASCADE (Chuỗi Phản Ứng Dây Chuyền Domino)
    # =========================================================================
    def render_domino_cascade(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        dominos = spec.get("process_data", {}).get("dominos", [
            {"num": "1", "title": "Kích Hoạt Đầu Tư", "desc": "Rót vốn R&D hạt nhân."},
            {"num": "2", "title": "Đột Phá Kỹ Thuật", "desc": "Thuật toán tối ưu gấp 10 lần."},
            {"num": "3", "title": "Chiếm Lĩnh Thị Phần", "desc": "Mở rộng 50.000 khách hàng mới."},
            {"num": "4", "title": "Bùng Nổ Lợi Nhuận", "desc": "Doanh thu tăng trưởng lũy thừa."}
        ])

        count = len(dominos)
        col_w = (width - (count - 1) * 14.0) / count

        for i in range(count):
            d = dominos[i]
            dx = left + i * (col_w + 14.0)
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, dx, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, dx + 10, top + 15, col_w - 20, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"DOMINO 0{d.get('num', i+1)}\n{d.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = d.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 60. PROCESS_RADIAL_PROGRESSION (Tiến Trình Tỏa Tia 360 Độ)
    # =========================================================================
    def render_radial_progression(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("process_data", {})
        hub_text = data.get("hub_text", "HẠT NHÂN\nPHÁT TRIỂN")
        rays = data.get("rays", [
            {"dir": "BẮC (NORTH)", "title": "Thị Trường Châu Á", "desc": "Tập trung Việt Nam, Singapore."},
            {"dir": "ĐÔNG (EAST)", "title": "Hạ Tầng Công Nghệ", "desc": "Trung tâm dữ liệu AI hiệu năng cao."},
            {"dir": "NAM (SOUTH)", "title": "Hệ Sinh Thái Đối Tác", "desc": "Liên kết 500+ doanh nghiệp liên minh."},
            {"dir": "TÂY (WEST)", "title": "Nguồn Vốn & Quỹ Đầu Tư", "desc": "Huy động vốn vòng Series B."}
        ])

        cx = left + width / 2.0
        cy = top + height / 2.0
        hub_r = 55.0

        hub = slide.Shapes.AddShape(msoShapeOval, cx - hub_r, cy - hub_r, hub_r * 2, hub_r * 2)
        hub.Fill.Solid()
        hub.Fill.ForeColor.RGB = hex_to_bgr(brand)
        hub.Line.Visible = msoTrue
        hub.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
        hub.Line.Weight = 2.0
        shapes.append(hub)

        htf = hub.TextFrame
        htf.WordWrap = msoTrue
        hp = htf.TextRange
        hp.Text = hub_text
        hp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        hp.Font.Size = 10.5
        hp.Font.Bold = msoTrue
        hp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        hp.ParagraphFormat.Alignment = ppAlignCenter

        rw = (width / 2.0) - hub_r - 20.0
        rh = (height / 2.0) - 20.0

        coords = [
            (cx - rw/2.0, top),
            (cx + hub_r + 15.0, cy - rh/2.0),
            (cx - rw/2.0, cy + hub_r + 10.0),
            (left, cy - rh/2.0)
        ]

        for i in range(min(4, len(rays))):
            rx, ry = coords[i]
            r_data = rays[i]

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rw, rh)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, ry + 8, rw - 20, rh - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{r_data.get('dir', '')}: {r_data.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = r_data.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # 21. PROCESS_CIRCULAR_LOOP_6STEP (Chu Trình Tuần Hoàn 6 Bước)
    def render_circular_loop_6step(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Center Core
        core_r = min(width, height) * 0.28
        cx = left + (width - core_r) / 2.0
        cy = top + (height - core_r) / 2.0
        core = slide.Shapes.AddShape(msoShapeOval, cx, cy, core_r, core_r)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Visible = msoFalse
        shapes.append(core)
        tr = core.TextFrame.TextRange
        tr.Text = "CHU TRÌNH\n6 BƯỚC\nLIÊN TỤC"
        tr.Font.Size = 11.0
        tr.Font.Bold = msoTrue
        tr.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        tr.ParagraphFormat.Alignment = ppAlignCenter

        # 6 Satellite Step Nodes in Ring
        steps = [
            ("1. Khảo Sát", "#38BDF8"), ("2. Thiết Kế", "#10B981"),
            ("3. Xây Dựng", "#059669"), ("4. Kiểm Thử", "#F59E0B"),
            ("5. Triển Khai", "#8B5CF6"), ("6. Tối Ưu", "#EC4899")
        ]
        import math
        center_x = left + width / 2.0
        center_y = top + height / 2.0
        orbit_r = min(width, height) * 0.38
        node_w = width * 0.18
        node_h = height * 0.18

        for i, (title, color) in enumerate(steps):
            angle = i * (2 * math.pi / 6) - (math.pi / 2)
            nx = center_x + orbit_r * math.cos(angle) - node_w / 2.0
            ny = center_y + orbit_r * math.sin(angle) - node_h / 2.0

            node = slide.Shapes.AddShape(msoShapeRoundedRectangle, nx, ny, node_w, node_h)
            node.Fill.Solid()
            node.Fill.ForeColor.RGB = hex_to_bgr(surface)
            node.Line.Visible = msoTrue
            node.Line.ForeColor.RGB = hex_to_bgr(color)
            node.Line.Weight = 1.5
            shapes.append(node)

            ntr = node.TextFrame.TextRange
            ntr.Text = title
            ntr.Font.Size = 10.5
            ntr.Font.Bold = msoTrue
            ntr.Font.Color.RGB = hex_to_bgr(ink)
            ntr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 22. PROCESS_SPIRAL_GROWTH (Vòng Xoắn Ốc Tăng Trưởng)
    def render_spiral_growth(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        atoms = spec.get("atoms", [])
        colors = ["#64748B", "#0284C7", "#38BDF8", "#10B981"]
        scales = [0.40, 0.60, 0.82, 1.00]
        if spec.get("levels"):
            levels = spec["levels"]
        elif atoms:
            levels = []
            for i, a in enumerate(atoms[:4]):
                t = a.get("title", f"Cấp Độ 0{i+1}") if isinstance(a, dict) else f"Cấp Độ 0{i+1}"
                d = a.get("text") or a.get("desc") or str(a) if isinstance(a, dict) else str(a)
                levels.append((t, d, scales[i % len(scales)], colors[i % len(colors)]))
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa tăng trưởng đào tạo.")
            levels = [
                (f"Giai Đoạn 0{i+1}", claim, scales[i], colors[i])
                for i in range(4)
            ]

        row_h = (height - 18.0) / len(levels)
        for i, (title, desc, scale, color) in enumerate(levels):
            ry = top + i * (row_h + 6.0)
            rw = width * scale
            rx = left

            sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rw, row_h)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = hex_to_bgr(surface)
            sh.Line.Visible = msoTrue
            sh.Line.ForeColor.RGB = hex_to_bgr(color)
            sh.Line.Weight = 2.0
            shapes.append(sh)

            tr = sh.TextFrame.TextRange
            tr.Text = f"{title}\n{desc}"
            tr.Font.Size = 10.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 23. PROCESS_HOURGLASS_WORKFLOW (Quy Trình Đồng Hồ Cát)
    def render_hourglass_workflow(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        stages = [
            ("1. THU NẬP Ý TƯỞNG DIỆN RỘNG (WIDE INPUT)", "Phân tích 1,000+ template slide thế giới, thu thập hàng triệu biến thể bố cục", 1.00, "#0284C7"),
            ("2. CHỌN LỌC TIÊU CHUẨN (SCREENING)", "Lọc ra 165+ cấu trúc tinh hoa nhất có tính ứng dụng cao", 0.75, "#38BDF8"),
            ("3. THẮT NÚT CHUYỂN HÓA (CORE SYNTHESIS)", "Chuẩn hóa thuật toán vẽ Native COM & Apple Motion Engine", 0.50, "#10B981"),
            ("4. ĐÓNG GÓI MODULE HÓA (PACKAGING)", "Tổ chức 6 Module Engines độc lập và cơ chế tự nhận dạng", 0.75, "#F59E0B"),
            ("5. PHÁT HÀNH ĐA KÊNH TOÀN CẦU (EXPANSION)", "Xuất bản Web Studio SaaS, Desktop API, Presentation PPTX", 1.00, "#8B5CF6")
        ]

        row_h = (height - 20.0) / len(stages)
        for i, (title, desc, scale, color) in enumerate(stages):
            ry = top + i * (row_h + 5.0)
            rw = width * scale
            rx = left + (width - rw) / 2.0

            sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rw, row_h)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = hex_to_bgr(surface)
            sh.Line.Visible = msoTrue
            sh.Line.ForeColor.RGB = hex_to_bgr(color)
            sh.Line.Weight = 1.5
            shapes.append(sh)

            tr = sh.TextFrame.TextRange
            tr.Text = f"{title}: {desc}"
            tr.Font.Size = 10.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 24. PROCESS_PARALLEL_STREAMS (3 Luồng Công Việc Chạy Song Song)
    def render_parallel_streams(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        streams = [
            ("LUỒNG 1: DỮ LIỆU & NATIVE COM", "Quản lý Shapes.AddTable và AddChart nhúng Excel không dùng ảnh tĩnh", "#0284C7"),
            ("LUỒNG 2: THỊ GIÁC & 165+ ARCHETYPES", "Xây dựng 6 Engine đồ họa vector thuần túy tự động co giãn tham số", "#10B981"),
            ("LUỒNG 3: CHUYỂN ĐỘNG APPLE MOTION", "Bộ điều phối Morph ma thuật và hiệu ứng so le thác nước Staggered", "#8B5CF6")
        ]

        row_h = (height - 24.0) / 3.0
        for i, (title, desc, color) in enumerate(streams):
            ry = top + i * (row_h + 12.0)
            sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ry, width, row_h)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = hex_to_bgr(surface)
            sh.Line.Visible = msoTrue
            sh.Line.ForeColor.RGB = hex_to_bgr(color)
            sh.Line.Weight = 2.0
            shapes.append(sh)

            tr = sh.TextFrame.TextRange
            tr.Text = f"{title}\n{desc}"
            tr.Font.Size = 11.5
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 25. PROCESS_STAGED_GATE_PHASES (Quy Trình 5 Giai Đoạn Kèm Cổng Quyết Định)
    def render_staged_gate_phases(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        phases = [
            ("Giai Đoạn 1", "Khảo Sát Nhu Cầu", "Gate 1: Duyệt Phạm Vi"),
            ("Giai Đoạn 2", "Thiết Kế Kiến Trúc", "Gate 2: Duyệt Cấu Trúc"),
            ("Giai Đoạn 3", "Lập Trình COM", "Gate 3: Vượt 48/48 Test"),
            ("Giai Đoạn 4", "Kiểm Định MACC", "Gate 4: Đạt Điểm 100"),
            ("Giai Đoạn 5", "Bàn Giao & Vận Hành", "Gate 5: Nghiệm Thu")
        ]

        card_w = (width - 32.0) / 5.0
        card_h = height * 0.70
        gate_h = height * 0.22

        for i, (g_title, g_desc, gate) in enumerate(phases):
            cx = left + i * (card_w + 8.0)

            # Phase Card
            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, card_h)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(brand)
            c.Line.Weight = 1.5
            shapes.append(c)

            tr = c.TextFrame.TextRange
            tr.Text = f"{g_title}\n\n{g_desc}"
            tr.Font.Size = 10.5
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

            # Gate Diamond / Pill Below
            g = slide.Shapes.AddShape(msoShapeDiamond, cx + card_w * 0.15, top + card_h + 8.0, card_w * 0.70, gate_h)
            g.Fill.Solid()
            g.Fill.ForeColor.RGB = hex_to_bgr("#065F46" if i < 4 else "#1E293B")
            g.Line.Visible = msoTrue
            g.Line.ForeColor.RGB = hex_to_bgr("#10B981" if i < 4 else "#64748B")
            g.Line.Weight = 1.2
            shapes.append(g)

            gtr = g.TextFrame.TextRange
            gtr.Text = gate
            gtr.Font.Size = 8.5
            gtr.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            gtr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 26. PROCESS_SERPENTINE_ROADMAP (Lộ Trình Uốn Lượn Chữ S)
    def render_serpentine_roadmap(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # 6 Points in S-Curve pattern (Row 1 left-to-right, Row 2 right-to-left)
        points = [
            ("Q1/2026: Kiến Trúc Nền Tảng", "#0284C7"),
            ("Q2/2026: Kho 112 Archetypes", "#38BDF8"),
            ("Q3/2026: 100% Native COM", "#10B981"),
            ("Q4/2026: Kho Mega 165+ Mẫu", "#059669"),
            ("Q1/2027: Apple Morph Motion", "#F59E0B"),
            ("Q2/2027: Hệ Sinh Thái Đa Tác Tử", "#8B5CF6")
        ]

        card_w = (width - 32.0) / 3.0
        card_h = (height - 24.0) / 2.0

        # Row 1 (Items 0, 1, 2)
        for i in range(3):
            cx = left + i * (card_w + 16.0)
            title, color = points[i]
            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top, card_w, card_h)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(color)
            c.Line.Weight = 2.0
            shapes.append(c)
            tr = c.TextFrame.TextRange
            tr.Text = f"MỐC {i+1} →\n\n{title}"
            tr.Font.Size = 11.0
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        # Row 2 (Items 5, 4, 3 reversed)
        for i in range(3):
            cx = left + (2 - i) * (card_w + 16.0)
            title, color = points[3 + i]
            c = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, top + card_h + 24.0, card_w, card_h)
            c.Fill.Solid()
            c.Fill.ForeColor.RGB = hex_to_bgr(surface)
            c.Line.Visible = msoTrue
            c.Line.ForeColor.RGB = hex_to_bgr(color)
            c.Line.Weight = 2.0
            shapes.append(c)
            tr = c.TextFrame.TextRange
            tr.Text = f"← MỐC {4+i}\n\n{title}"
            tr.Font.Size = 11.0
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 27. PROCESS_PIPELINE_FILTRATION (Đường Ống Lọc Đa Tầng)
    def render_pipeline_filtration(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        filters = [
            ("TẦNG 1: TỔNG QUAN DỮ LIỆU ĐẦU VÀO", "1,000 Tài liệu / Blueprints thô cần chuyển hóa", 1.00, "#0284C7"),
            ("TẦNG 2: BỘ LỌC CÚ PHÁP & NGUYÊN TỬ", "850 Đơn vị thông tin đạt chuẩn Pedagogical Chunking", 0.80, "#38BDF8"),
            ("TẦNG 3: BỘ LỌC ĐỊNH DẠNG NATIVE COM", "500 Slide thỏa mãn không dùng ảnh tĩnh", 0.60, "#10B981"),
            ("TẦNG 4: BỘ LỌC KIỂM TOÁN TÁC TỬ MACC", "100 Slide đạt chuẩn không lỗi hồi quy P0/P1", 0.40, "#F59E0B")
        ]

        row_h = (height - 18.0) / len(filters)
        for i, (title, desc, scale, color) in enumerate(filters):
            ry = top + i * (row_h + 6.0)
            rw = width * scale
            rx = left + (width - rw) / 2.0

            sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rw, row_h)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = hex_to_bgr(surface)
            sh.Line.Visible = msoTrue
            sh.Line.ForeColor.RGB = hex_to_bgr(color)
            sh.Line.Weight = 2.0
            shapes.append(sh)

            tr = sh.TextFrame.TextRange
            tr.Text = f"{title}: {desc}"
            tr.Font.Size = 10.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 28. PROCESS_CONTINUOUS_IMPROVEMENT_PDCA (Chu Trình Cải Tiến Liên Tục PDCA)
    def render_continuous_improvement_pdca(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        qw = (width - 16.0) / 2.0
        qh = (height - 16.0) / 2.0

        atoms = spec.get("atoms", [])
        colors = ["#0284C7", "#10B981", "#F59E0B", "#8B5CF6"]
        letters = ["P - KẾ HOẠCH (PLAN)", "D - THỰC HIỆN (DO)", "C - KIỂM TRA (CHECK)", "A - HÀNH ĐỘNG (ACT)"]
        coords = [
            (left, top),
            (left + qw + 16.0, top),
            (left, top + qh + 16.0),
            (left + qw + 16.0, top + qh + 16.0)
        ]
        quads = []
        if atoms:
            for i, a in enumerate(atoms[:4]):
                t = a.get("title", letters[i]) if isinstance(a, dict) else str(a)
                d = a.get("text") or a.get("desc") or "" if isinstance(a, dict) else ""
                body = f"{letters[i]}\n\n• {t}\n• {d}" if d else f"{letters[i]}\n\n• {t}"
                cx, cy = coords[i]
                quads.append((cx, cy, qw, qh, body, colors[i]))
        else:
            claim = spec.get("primary_claim", "Nội dung chuẩn hóa cải tiến liên tục.")
            for i in range(4):
                cx, cy = coords[i]
                quads.append((cx, cy, qw, qh, f"{letters[i]}\n\n• {claim}", colors[i]))

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
            tr.Font.Size = 11.0
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 29. PROCESS_DEVSECOPS_INFINITY_LOOP (Vòng Lặp Số 8 Vô Cực DevSecOps)
    def render_devsecops_infinity_loop(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")
        brand = self._get_token("colors", "brand", "#0284C7")
        accent = self._get_token("colors", "accent", "#38BDF8")
        success = self._get_token("colors", "success", "#10B981")

        loop_h = min(height, 310.0)
        loop_y = top + (height - loop_h) / 2.0

        nexus_w = 90.0
        loop_w = (width - nexus_w - 30.0) / 2.0

        # =========================================================
        # 1. LEFT CLUSTER: DEVELOPMENT (DEV LOOP)
        # =========================================================
        dev_shapes = []
        dev_bg = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, loop_y, loop_w, loop_h)
        dev_bg.Fill.Solid()
        dev_bg.Fill.ForeColor.RGB = hex_to_bgr(surface)
        dev_bg.Line.Visible = msoTrue
        dev_bg.Line.ForeColor.RGB = hex_to_bgr(brand)
        dev_bg.Line.Weight = 2.0
        dev_shapes.append(dev_bg)

        # Header Badge Dev
        dev_badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 14, loop_y + 12, loop_w - 28, 28)
        dev_badge.Fill.Solid()
        dev_badge.Fill.ForeColor.RGB = hex_to_bgr(brand)
        dev_badge.Line.Visible = msoFalse
        dbt = dev_badge.TextFrame.TextRange
        dbt.Text = "◄ PHÁT TRIỂN (DEVELOPMENT)"
        dbt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        dbt.Font.Size = 11.0
        dbt.Font.Bold = msoTrue
        dbt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        dev_badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        dev_shapes.append(dev_badge)

        dev_phases = [
            ("01. PLAN", "Lập kế hoạch & phân rã tính năng", "#0284C7"),
            ("02. CODE", "Phát triển mã nguồn theo chuẩn MACC", "#38BDF8"),
            ("03. BUILD", "Đóng gói container & build tự động", "#06B6D4"),
            ("04. TEST", "Kiểm thử 48/48 bài unit & regression", "#10B981")
        ]
        ph_gap = 6.0
        ph_h = (loop_h - 56.0 - (3 * ph_gap)) / 4.0
        for i, (p_title, p_desc, p_color) in enumerate(dev_phases):
            py = loop_y + 48.0 + i * (ph_h + ph_gap)
            p_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 14, py, loop_w - 28, ph_h)
            p_card.Fill.Solid()
            p_card.Fill.ForeColor.RGB = hex_to_bgr("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            p_card.Line.Visible = msoTrue
            p_card.Line.ForeColor.RGB = hex_to_bgr(p_color)
            p_card.Line.Weight = 1.2
            dev_shapes.append(p_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, py + 4, loop_w - 40, ph_h - 8)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{p_title}: "
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(p_color)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p_desc
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            dev_shapes.append(tb)

        dev_group = safe_group(slide, dev_shapes, "DevSecOps_Dev_Group")
        shapes.append(dev_group)

        # =========================================================
        # 2. CENTER CLUSTER: DEVSECOPS SECURITY SHIELD
        # =========================================================
        sec_shapes = []
        sx = left + loop_w + 15.0
        sy = loop_y + (loop_h - 140.0) / 2.0
        shield = slide.Shapes.AddShape(msoShapeDiamond, sx, sy, nexus_w, 140.0)
        shield.Fill.Solid()
        shield.Fill.ForeColor.RGB = hex_to_bgr("#7F1D1D" if self.theme == "DARK" else "#FEE2E2")
        shield.Line.Visible = msoTrue
        shield.Line.ForeColor.RGB = hex_to_bgr("#EF4444")
        shield.Line.Weight = 2.5
        sec_shapes.append(shield)

        stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 4, sy + 30, nexus_w - 8, 80)
        stf = stb.TextFrame
        stf.WordWrap = msoTrue
        stf.MarginLeft = 0
        stf.MarginRight = 0
        str_t = stf.TextRange
        str_t.Text = "★ AN NINH\nBẢO MẬT\nZERO\nTRUST"
        str_t.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        str_t.Font.Size = 9.5
        str_t.Font.Bold = msoTrue
        str_t.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        str_t.ParagraphFormat.Alignment = ppAlignCenter
        sec_shapes.append(stb)

        sec_group = safe_group(slide, sec_shapes, "DevSecOps_Shield_Group")
        shapes.append(sec_group)

        # =========================================================
        # 3. RIGHT CLUSTER: OPERATIONS (OPS LOOP)
        # =========================================================
        ops_shapes = []
        rx = sx + nexus_w + 15.0
        ops_bg = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, loop_y, loop_w, loop_h)
        ops_bg.Fill.Solid()
        ops_bg.Fill.ForeColor.RGB = hex_to_bgr(surface)
        ops_bg.Line.Visible = msoTrue
        ops_bg.Line.ForeColor.RGB = hex_to_bgr(success)
        ops_bg.Line.Weight = 2.0
        ops_shapes.append(ops_bg)

        # Header Badge Ops
        ops_badge = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx + 14, loop_y + 12, loop_w - 28, 28)
        ops_badge.Fill.Solid()
        ops_badge.Fill.ForeColor.RGB = hex_to_bgr(success)
        ops_badge.Line.Visible = msoFalse
        obt = ops_badge.TextFrame.TextRange
        obt.Text = "VẬN HÀNH (OPERATIONS) ►"
        obt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        obt.Font.Size = 11.0
        obt.Font.Bold = msoTrue
        obt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        ops_badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        ops_shapes.append(ops_badge)

        ops_phases = [
            ("05. RELEASE", "Đóng gói phiên bản & gắn tag semantic", "#10B981"),
            ("06. DEPLOY", "Triển khai hạ tầng không downtime", "#059669"),
            ("07. OPERATE", "Vận hành hệ thống & điều phối tài nguyên", "#047857"),
            ("08. MONITOR", "Giám sát hiệu năng APM & cảnh báo 24/7", "#065F46")
        ]
        for i, (p_title, p_desc, p_color) in enumerate(ops_phases):
            py = loop_y + 48.0 + i * (ph_h + ph_gap)
            p_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx + 14, py, loop_w - 28, ph_h)
            p_card.Fill.Solid()
            p_card.Fill.ForeColor.RGB = hex_to_bgr("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            p_card.Line.Visible = msoTrue
            p_card.Line.ForeColor.RGB = hex_to_bgr(p_color)
            p_card.Line.Weight = 1.2
            ops_shapes.append(p_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 20, py + 4, loop_w - 40, ph_h - 8)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{p_title}: "
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(p_color)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = p_desc
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            ops_shapes.append(tb)

        ops_group = safe_group(slide, ops_shapes, "DevSecOps_Ops_Group")
        shapes.append(ops_group)

        return shapes

    # 30. PROCESS_CRITICAL_PATH_CPM (Sơ Đồ Đường Găng PERT/CPM Có Mũi Tên Vector)
    def render_critical_path_cpm(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")

        # 5 Nodes across timeline
        # Nodes: (ID, Title, Duration, Float_str, is_critical, color)
        crit_nodes = spec.get("crit_nodes") or [
            ("NÚT 01", "Khởi Động & Khảo Sát Nhu Cầu", "T = 2 Ngày", "Float = 0", True, "#EF4444"),
            ("NÚT 02", "Phân Tích Nghiệp Vụ & Dữ Liệu", "T = 5 Ngày", "Float = 0", True, "#EF4444"),
            ("NÚT 03", "Thiết Kế Khung Can Thiệp", "T = 4 Ngày", "Float = 0", True, "#EF4444"),
            ("NÚT 04", "Nghiệm Thu & Triển Khai", "T = 2 Ngày", "Float = 0", True, "#EF4444")
        ]
        branch_node = spec.get("branch_node") or ("NÚT 2B", "Khảo Sát Thực Địa Bổ Trợ", "T = 3 Ngày", "Float = +2 Ngày", False, "#0284C7")

        gap = 46.0
        node_w = (width - (3 * gap)) / 4.0
        node_h = 100.0
        cy_main = top + 24.0

        # Create Bottom Legend Strip first to bind with Node 0
        leg_y = cy_main + node_h + 38.0 + node_h + 16.0
        leg_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, leg_y, width, 28)
        leg_bar.Fill.Solid()
        leg_bar.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
        leg_bar.Line.Visible = msoFalse
        lt = leg_bar.TextFrame.TextRange
        lt.Text = "★ Đường Găng (Critical Path, Float = 0: Tuyệt đối không được trễ)    |    ● Nhánh Phụ Song Song (Float = +2 Ngày: Có thể bù đắp thời gian)"
        lt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        lt.Font.Size = 10.0
        lt.Font.Bold = msoTrue
        lt.Font.Color.RGB = hex_to_bgr(ink)
        leg_bar.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        main_coords = []
        # Render 4 Critical Nodes
        for i, (nid, ntitle, ndur, nfloat, is_crit, color) in enumerate(crit_nodes):
            n_shapes = []
            cx = left + i * (node_w + gap)
            main_coords.append((cx, cy_main))

            # Critical Path Incoming Arrow
            if i > 0 and len(main_coords) > 1:
                x_start = main_coords[i - 1][0] + node_w
                y_mid = cy_main + node_h / 2.0
                conn = add_vector_connector(slide, x_start, y_mid, cx, y_mid, color="#EF4444", weight=2.5, arrowhead=True)
                if conn:
                    n_shapes.append(conn)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, cy_main, node_w, node_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(color)
            card.Line.Weight = 2.2 if is_crit else 1.2
            n_shapes.append(card)

            # Top Header Strip
            hdr = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 8, cy_main + 8, node_w - 16, 22)
            hdr.Fill.Solid()
            hdr.Fill.ForeColor.RGB = hex_to_bgr(color)
            hdr.Line.Visible = msoFalse
            ht = hdr.TextFrame.TextRange
            ht.Text = f"{nid}  •  {ndur}"
            ht.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            ht.Font.Size = 10.0
            ht.Font.Bold = msoTrue
            ht.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            hdr.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            n_shapes.append(hdr)

            # Title
            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 8, cy_main + 32, node_w - 16, 36)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0
            tf.MarginRight = 0
            ttr = tf.TextRange
            ttr.Text = ntitle
            ttr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ttr.Font.Size = 11.0
            ttr.Font.Bold = msoTrue
            ttr.Font.Color.RGB = hex_to_bgr(ink)
            ttr.ParagraphFormat.Alignment = ppAlignCenter
            n_shapes.append(tb)

            # Bottom Status Chip
            chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 12, cy_main + node_h - 26, node_w - 24, 18)
            chip.Fill.Solid()
            chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            chip.Line.Visible = msoFalse
            ct = chip.TextFrame.TextRange
            ct.Text = f"★ {nfloat} (ĐƯỜNG GĂNG)"
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 8.5
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(color)
            chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            n_shapes.append(chip)

            # Bind legend strip to Node 0 so it appears on transition
            if i == 0:
                n_shapes.append(leg_bar)

            node_grp = safe_group(slide, n_shapes, f"CPM_Node_{i+1}")
            shapes.append(node_grp)

        # Off-critical parallel branch node (Node 2B) below Node 2
        b_shapes = []
        cx_b = main_coords[1][0]
        cy_b = cy_main + node_h + 38.0
        b_nid, b_title, b_dur, b_float, _, b_color = branch_node

        # Branch Arrow Node 1 -> Node 2B
        conn_b1 = add_vector_connector(slide, main_coords[0][0] + node_w, cy_main + node_h * 0.75, cx_b, cy_b + node_h * 0.35, color="#0284C7", weight=1.8, dashed=True, arrowhead=True)
        if conn_b1:
            b_shapes.append(conn_b1)

        b_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx_b, cy_b, node_w, node_h)
        b_card.Fill.Solid()
        b_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        b_card.Line.Visible = msoTrue
        b_card.Line.ForeColor.RGB = hex_to_bgr(b_color)
        b_card.Line.Weight = 1.5
        b_shapes.append(b_card)

        b_hdr = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx_b + 8, cy_b + 8, node_w - 16, 22)
        b_hdr.Fill.Solid()
        b_hdr.Fill.ForeColor.RGB = hex_to_bgr(b_color)
        b_hdr.Line.Visible = msoFalse
        bht = b_hdr.TextFrame.TextRange
        bht.Text = f"{b_nid}  •  {b_dur}"
        bht.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
        bht.Font.Size = 10.0
        bht.Font.Bold = msoTrue
        bht.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        b_hdr.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        b_shapes.append(b_hdr)

        b_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx_b + 8, cy_b + 32, node_w - 16, 36)
        btf = b_tb.TextFrame
        btf.WordWrap = msoTrue
        btf.MarginLeft = 0
        btf.MarginRight = 0
        bttr = btf.TextRange
        bttr.Text = b_title
        bttr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bttr.Font.Size = 11.0
        bttr.Font.Bold = msoTrue
        bttr.Font.Color.RGB = hex_to_bgr(ink)
        bttr.ParagraphFormat.Alignment = ppAlignCenter
        b_shapes.append(b_tb)

        b_chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx_b + 12, cy_b + node_h - 26, node_w - 24, 18)
        b_chip.Fill.Solid()
        b_chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
        b_chip.Line.Visible = msoFalse
        bct = b_chip.TextFrame.TextRange
        bct.Text = f"● {b_float} (NHÁNH PHỤ)"
        bct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bct.Font.Size = 8.5
        bct.Font.Bold = msoTrue
        bct.Font.Color.RGB = hex_to_bgr(b_color)
        b_chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        b_shapes.append(b_chip)

        branch_grp = safe_group(slide, b_shapes, "CPM_Branch_2B")
        shapes.append(branch_grp)

        return shapes

