"""
processes_engine.py
Exhaustive Process, Mechanism, and Flow Engine for Make Slide Pro V8.5.0.
Generates 20 classic process, timeline, mechanism, and roadmap models
using 100% Microsoft PowerPoint Native Vector Shapes.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

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
        steps = data.get("steps", [
            {"step": "01", "title": "Khảo Sát Hiện Trạng", "desc": "Thu thập dữ liệu thực địa, phỏng vấn chuyên sâu các phòng ban."},
            {"step": "02", "title": "Phân Tích Khoảng Trống", "desc": "Xác định điểm nghẽn quy trình và định lượng tổn thất vận hành."},
            {"step": "03", "title": "Thiết Kế Kiến Trúc", "desc": "Mô hình hóa giải pháp số hóa thế hệ mới chuẩn quốc tế."},
            {"step": "04", "title": "Triển Khai & Kiểm Thử", "desc": "Thiết lập môi trường Sandbox, chạy thử nghiệm pilot 30 ngày."},
            {"step": "05", "title": "Bàn Giao & Mở Rộng", "desc": "Đào tạo nhân sự toàn diện và bàn giao tài liệu kỹ thuật."}
        ])

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

            # Chevron Header Shape
            chev = slide.Shapes.AddShape(msoShapeChevron, sx, top, step_w, chevron_h)
            chev.Fill.Solid()
            chev.Fill.ForeColor.RGB = hex_to_bgr(brand if is_active else surface)
            chev.Line.Visible = msoTrue
            chev.Line.ForeColor.RGB = hex_to_bgr(brand if is_active else border)
            chev.Line.Weight = 1.5
            shapes.append(chev)

            ctf = chev.TextFrame
            ctf.WordWrap = msoTrue
            cp = ctf.TextRange
            cp.Text = f"BƯỚC {s.get('step', str(i+1))}\n{s.get('title', f'Giai Đoạn {i+1}')}"
            cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            cp.Font.Size = 10 if count > 4 else 11.5
            cp.Font.Bold = msoTrue
            cp.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_active else ink)
            cp.ParagraphFormat.Alignment = ppAlignCenter

            # Body Card below
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, card_top, step_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if is_active else border)
            card.Line.Weight = 1.2
            shapes.append(card)

            btb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 8, card_top + 10, step_w - 16, card_h - 20)
            btf = btb.TextFrame
            btf.WordWrap = msoTrue
            bp = btf.TextRange
            bp.Text = s.get("desc", "")
            bp.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            bp.Font.Size = 9.5 if count > 4 else 10.5
            bp.Font.Color.RGB = hex_to_bgr(muted)
            bp.ParagraphFormat.Alignment = ppAlignLeft
            shapes.append(btb)

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
        radius = min(width, height) * 0.38

        core_r = min(width, height) * 0.18
        core = slide.Shapes.AddShape(msoShapeOval, cx - core_r, cy - core_r, core_r * 2, core_r * 2)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(surface)
        core.Line.Visible = msoTrue
        core.Line.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Weight = 2.5
        shapes.append(core)

        ctf = core.TextFrame
        ctf.WordWrap = msoTrue
        cp = ctf.TextRange
        cp.Text = cycle_name
        cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cp.Font.Size = 11
        cp.Font.Bold = msoTrue
        cp.Font.Color.RGB = hex_to_bgr(brand)
        cp.ParagraphFormat.Alignment = ppAlignCenter

        node_w = min(width * 0.28, 170.0)
        node_h = min(height * 0.24, 90.0)

        for i in range(count):
            nd = nodes[i]
            angle = (2 * math.pi / count) * i - (math.pi / 2.0)
            nx = cx + radius * math.cos(angle) - (node_w / 2.0)
            ny = cy + radius * math.sin(angle) - (node_h / 2.0)

            n_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, nx, ny, node_w, node_h)
            n_card.Fill.Solid()
            n_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            n_card.Line.Visible = msoTrue
            n_card.Line.ForeColor.RGB = hex_to_bgr(border)
            n_card.Line.Weight = 1.5
            shapes.append(n_card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, nx + 8, ny + 6, node_w - 16, node_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{nd.get('step', '')}: {nd.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = nd.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

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
        lanes = data.get("lanes", [
            {"dept": "KHÁCH HÀNG", "task": "Gửi yêu cầu dịch vụ trực tuyến qua Mobile App."},
            {"dept": "HỆ THỐNG AI", "task": "Tự động phân tích hồ sơ và chấm điểm rủi ro."},
            {"dept": "CHUYÊN VIÊN", "task": "Phê duyệt các trường hợp đặc biệt ngoài luồng."},
            {"dept": "KHO BẠC / TÀI CHÍNH", "task": "Giải ngân trực tiếp vào tài khoản trong 5 phút."}
        ])

        count = len(lanes)
        lane_h = (height - (count - 1) * 8.0) / count
        header_w = 140.0

        for i in range(count):
            ln = lanes[i]
            ly = top + i * (lane_h + 8.0)

            hdr = slide.Shapes.AddShape(msoShapeRectangle, left, ly, header_w, lane_h)
            hdr.Fill.Solid()
            hdr.Fill.ForeColor.RGB = hex_to_bgr(brand)
            hdr.Line.Visible = msoFalse
            shapes.append(hdr)

            htf = hdr.TextFrame
            htf.WordWrap = msoTrue
            hp = htf.TextRange
            hp.Text = ln.get("dept", f"LÀN {i+1}")
            hp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            hp.Font.Size = 10.5
            hp.Font.Bold = msoTrue
            hp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            hp.ParagraphFormat.Alignment = ppAlignCenter

            track_w = width - header_w - 6.0
            track = slide.Shapes.AddShape(msoShapeRectangle, left + header_w + 6.0, ly, track_w, lane_h)
            track.Fill.Solid()
            track.Fill.ForeColor.RGB = hex_to_bgr(surface)
            track.Line.Visible = msoTrue
            track.Line.ForeColor.RGB = hex_to_bgr(border)
            track.Line.Weight = 1.0
            shapes.append(track)

            box_w = track_w * 0.75
            box_x = left + header_w + 20.0 + (i * (track_w * 0.2) / count)
            tbox = slide.Shapes.AddShape(msoShapeRoundedRectangle, box_x, ly + 6.0, box_w, lane_h - 12.0)
            tbox.Fill.Solid()
            tbox.Fill.ForeColor.RGB = hex_to_bgr(self._get_token("colors", "badge_bg", "#082F49"))
            tbox.Line.Visible = msoTrue
            tbox.Line.ForeColor.RGB = hex_to_bgr(brand)
            tbox.Line.Weight = 1.0
            shapes.append(tbox)

            tbt = tbox.TextFrame
            tbt.WordWrap = msoTrue
            tp = tbt.TextRange
            tp.Text = ln.get("task", "")
            tp.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            tp.Font.Size = 10
            tp.Font.Color.RGB = hex_to_bgr(ink)
            tp.ParagraphFormat.Alignment = ppAlignLeft

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
            shapes.append(step_box)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 8, sy + 10, step_w - 16, sh - 20)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{st.get('level', '')} ({st.get('kpi', '')})\n"
            p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_top else brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = st.get("title", "") + "\n"
            p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p2.Font.Size = 10.5
            p2.Font.Bold = msoTrue
            p2.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_top else ink)
            p2.ParagraphFormat.Alignment = ppAlignCenter

            p3 = tf.TextRange.Paragraphs(3)
            p3.Text = st.get("desc", "")
            p3.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p3.Font.Size = 9.0
            p3.Font.Color.RGB = hex_to_bgr("#E2E8F0" if is_top else muted)
            p3.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

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
        milestones = data.get("milestones", [
            {"date": "Q1/2024", "title": "Nghiên Cứu Khả Thi", "desc": "Đạt mốc 10.000 người dùng thử nghiệm."},
            {"date": "Q2/2024", "title": "Phát Hành Bản Beta", "desc": "Tích hợp thành công 12 module cốt lõi."},
            {"date": "Q3/2024", "title": "Bùng Nổ Doanh Thu", "desc": "Vượt chỉ tiêu 150% kế hoạch năm."},
            {"date": "Q4/2024", "title": "Vươn Tầm Quốc Tế", "desc": "Mở rộng 3 thị trường Đông Nam Á."}
        ])

        count = len(milestones)
        spine_y = top + 80.0
        ribbon = slide.Shapes.AddShape(msoShapeRectangle, left, spine_y, width, 6.0)
        ribbon.Fill.Solid()
        ribbon.Fill.ForeColor.RGB = hex_to_bgr(brand)
        ribbon.Line.Visible = msoFalse
        shapes.append(ribbon)

        col_w = (width - (count - 1) * 16.0) / count
        for i in range(count):
            m = milestones[i]
            mx = left + i * (col_w + 16.0)

            flag = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx + (col_w - 90)/2.0, top + 35.0, 90, 32)
            flag.Fill.Solid()
            flag.Fill.ForeColor.RGB = hex_to_bgr(brand)
            flag.Line.Visible = msoFalse
            shapes.append(flag)

            ftf = flag.TextFrame
            fp = ftf.TextRange
            fp.Text = m.get("date", f"MỐC {i+1}")
            fp.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            fp.Font.Size = 11
            fp.Font.Bold = msoTrue
            fp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            fp.ParagraphFormat.Alignment = ppAlignCenter

            card_y = spine_y + 24.0
            card_h = height - (card_y - top) - 10.0
            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx, card_y, col_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(border)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, mx + 10, card_y + 10, col_w - 20, card_h - 20)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = m.get("title", "") + "\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(ink)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = m.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

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
