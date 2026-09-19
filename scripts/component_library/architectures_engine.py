"""
architectures_engine.py
Exhaustive System, Technology, and Hierarchy Architecture Engine for Make Slide Pro V8.5.0.
Generates 15 classic software, cloud, network, and organizational diagrams
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


class ArchitecturesEngine:
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}

    def _get_token(self, category: str, key: str, fallback: str) -> str:
        return self.tokens.get(category, {}).get(key, fallback)

    # =========================================================================
    # 61. ARCH_SYSTEM_LAYERED_STACK (Kiến Trúc Phân Tầng Hệ Thống)
    # =========================================================================
    def render_system_layered_stack(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("arch_data", {})
        layers = data.get("layers", [
            {"tier": "TẦNG 1: TRÌNH DIỄN (PRESENTATION)", "tech": "React, Next.js, Flutter, Tailwind", "desc": "Giao diện người dùng đa nền tảng, phản hồi tức thì."},
            {"tier": "TẦNG 2: CỔNG ĐIỀU HƯỚNG (API GATEWAY)", "tech": "Envoy, Kong, GraphQL, OAuth2", "desc": "Quản lý lưu lượng, bảo mật chứng thực, cân bằng tải."},
            {"tier": "TẦNG 3: DỊCH VỤ NGHIỆP VỤ (MICROSERVICES)", "tech": "Go, Python, gRPC, Temporal", "desc": "Logic kinh doanh, điều phối 16 AI Agents tự động."},
            {"tier": "TẦNG 4: KHO DỮ LIỆU CỐT LÕI (LAKEHOUSE)", "tech": "BigQuery, Spanner, Redis, Iceberg", "desc": "Lưu trữ phân tán quy mô Petabyte, truy vấn siêu tốc."}
        ])

        count = len(layers)
        layer_h = (height - (count - 1) * 10.0) / count

        for i in range(count):
            l_data = layers[i]
            ly = top + i * (layer_h + 10.0)
            is_top = (i == 0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ly, width, layer_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand if is_top else border)
            card.Line.Weight = 1.5 if is_top else 1.0
            shapes.append(card)

            # Left Tag Indicator
            tag = slide.Shapes.AddShape(msoShapeRectangle, left, ly, 8.0, layer_h)
            tag.Fill.Solid()
            tag.Fill.ForeColor.RGB = hex_to_bgr(brand)
            tag.Line.Visible = msoFalse
            shapes.append(tag)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, ly + 8, width - 40, layer_h - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{l_data.get('tier', '')}  |  "
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if is_top else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"Công Nghệ: {l_data.get('tech', '')} — {l_data.get('desc', '')}"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 62. ARCH_ORG_HIERARCHY_TREE (Cây Cơ Cấu Tổ Chức Doanh Nghiệp)
    # =========================================================================
    def render_org_hierarchy_tree(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("arch_data", {})
        top_node = data.get("top_node", {"role": "HỘI ĐỒNG QUẢN TRỊ & TỔNG GIÁM ĐỐC (CEO)", "name": "Định Hướng Chiến Lược Cốt Lõi"})
        sub_nodes = data.get("sub_nodes", [
            {"dept": "KHỐI CÔNG NGHỆ (CTO)", "desc": "R&D AI & Hạ Tầng Cloud"},
            {"dept": "KHỐI SẢN PHẨM (CPO)", "desc": "Thiết Kế Trải Nghiệm & UI/UX"},
            {"dept": "KHỐI KINH DOANH (CRO)", "desc": "Doanh Thu & Phát Triển Thị Trường"},
            {"dept": "KHỐI VẬN HÀNH (COO)", "desc": "Tài Chính, Pháp Lý & Nhân Sự"}
        ])

        # Top Executive Node
        top_w = width * 0.5
        top_x = left + (width - top_w) / 2.0
        top_h = 65.0

        top_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, top_x, top, top_w, top_h)
        top_card.Fill.Solid()
        top_card.Fill.ForeColor.RGB = hex_to_bgr(brand)
        top_card.Line.Visible = msoFalse
        shapes.append(top_card)

        ttf = top_card.TextFrame
        ttf.WordWrap = msoTrue
        tp = ttf.TextRange
        tp.Text = f"{top_node.get('role', '')}\n{top_node.get('name', '')}"
        tp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        tp.Font.Size = 11
        tp.Font.Bold = msoTrue
        tp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        tp.ParagraphFormat.Alignment = ppAlignCenter

        # Connecting Vertical Stem
        stem_y = top + top_h
        stem_h = 30.0
        stem = slide.Shapes.AddShape(msoShapeRectangle, left + width / 2.0 - 1.5, stem_y, 3.0, stem_h)
        stem.Fill.Solid()
        stem.Fill.ForeColor.RGB = hex_to_bgr(brand)
        stem.Line.Visible = msoFalse
        shapes.append(stem)

        # Department Sub Nodes
        sub_count = len(sub_nodes)
        sub_gap = 12.0
        sub_w = (width - (sub_count - 1) * sub_gap) / sub_count
        sub_y = stem_y + stem_h + 10.0
        sub_h = height - (sub_y - top)

        for i in range(sub_count):
            sn = sub_nodes[i]
            sx = left + i * (sub_w + sub_gap)

            scard = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, sub_y, sub_w, sub_h)
            scard.Fill.Solid()
            scard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            scard.Line.Visible = msoTrue
            scard.Line.ForeColor.RGB = hex_to_bgr(border)
            scard.Line.Weight = 1.2
            shapes.append(scard)

            stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 8, sub_y + 12, sub_w - 16, sub_h - 24)
            stf = stb.TextFrame
            stf.WordWrap = msoTrue
            sp1 = stf.TextRange.Paragraphs(1)
            sp1.Text = sn.get("dept", "") + "\n"
            sp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            sp1.Font.Size = 10.5
            sp1.Font.Bold = msoTrue
            sp1.Font.Color.RGB = hex_to_bgr(brand)
            sp1.ParagraphFormat.Alignment = ppAlignCenter

            sp2 = stf.TextRange.Paragraphs(2)
            sp2.Text = sn.get("desc", "")
            sp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            sp2.Font.Size = 9.0
            sp2.Font.Color.RGB = hex_to_bgr(muted)
            sp2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(stb)

        return shapes

    # =========================================================================
    # 63. ARCH_RADIAL_MIND_MAP (Sơ Đồ Tư Duy Tỏa Tia - Mind Map)
    # =========================================================================
    def render_radial_mind_map(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        data = spec.get("arch_data", {})
        center_topic = data.get("topic", "HỆ SINH THÁI\nMAKE SLIDE PRO")
        branches = data.get("branches", [
            {"title": "Lõi Sinh Tự Động", "desc": "16 Tác Tử AI MACC"},
            {"title": "Mô Hình Dữ Liệu", "desc": "110+ Archetypes Quốc Tế"},
            {"title": "Bảo Mật Cấp Cao", "desc": "Tuân Thủ Zero-Trust SOC2"},
            {"title": "Tích Hợp Office", "desc": "100% Native COM & Excel"}
        ])

        cx = left + width / 2.0
        cy = top + height / 2.0
        c_radius = 60.0

        # Center Topic
        c_shape = slide.Shapes.AddShape(msoShapeOval, cx - c_radius, cy - c_radius, c_radius * 2, c_radius * 2)
        c_shape.Fill.Solid()
        c_shape.Fill.ForeColor.RGB = hex_to_bgr(brand)
        c_shape.Line.Visible = msoTrue
        c_shape.Line.ForeColor.RGB = hex_to_bgr("#FFFFFF")
        c_shape.Line.Weight = 2.0
        shapes.append(c_shape)

        ctf = c_shape.TextFrame
        ctf.WordWrap = msoTrue
        cp = ctf.TextRange
        cp.Text = center_topic
        cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cp.Font.Size = 10.5
        cp.Font.Bold = msoTrue
        cp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        cp.ParagraphFormat.Alignment = ppAlignCenter

        b_count = len(branches)
        bw = (width / 2.0) - c_radius - 25.0
        bh = (height / 2.0) - 20.0

        coords = [
            (left + 10, top + 10),                            # Top-Left
            (left + width - bw - 10, top + 10),               # Top-Right
            (left + 10, top + height - bh - 10),              # Bottom-Left
            (left + width - bw - 10, top + height - bh - 10)  # Bottom-Right
        ]

        for i in range(min(4, b_count)):
            bx, by = coords[i]
            b_info = branches[i]

            bcard = slide.Shapes.AddShape(msoShapeRoundedRectangle, bx, by, bw, bh)
            bcard.Fill.Solid()
            bcard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            bcard.Line.Visible = msoTrue
            bcard.Line.ForeColor.RGB = hex_to_bgr(brand)
            bcard.Line.Weight = 1.2
            shapes.append(bcard)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, bx + 10, by + 10, bw - 20, bh - 20)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"★ {b_info.get('title', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = b_info.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 64. ARCH_MICROSERVICES_MESH (Mạng Lưới Dịch Vụ Microservices)
    # =========================================================================
    def render_microservices_mesh(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        services = spec.get("arch_data", {}).get("services", [
            {"name": "Auth Service", "proto": "gRPC / OAuth2", "scale": "Autoscale 3-10 Pods"},
            {"name": "Blueprint AI Engine", "proto": "Gemini 2.5 Pro", "scale": "High Compute"},
            {"name": "COM Office Renderer", "proto": "Win32 Interop", "scale": "Dedicated Worker"},
            {"name": "Billing & SaaS API", "proto": "Stripe Webhook", "scale": "Zero-Downtime"},
            {"name": "Telemetry & Logs", "proto": "OpenTelemetry", "scale": "Elastic Ingest"},
            {"name": "File Storage CDN", "proto": "GCS / MinIO", "scale": "Global Edge"}
        ])

        cols = 3
        rows = 2
        card_w = (width - (cols - 1) * 14.0) / cols
        card_h = (height - (rows - 1) * 14.0) / rows

        for idx, svc in enumerate(services[:6]):
            r = idx // cols
            c = idx % cols
            sx = left + c * (card_w + 14.0)
            sy = top + r * (card_h + 14.0)

            scard = slide.Shapes.AddShape(msoShapeRoundedRectangle, sx, sy, card_w, card_h)
            scard.Fill.Solid()
            scard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            scard.Line.Visible = msoTrue
            scard.Line.ForeColor.RGB = hex_to_bgr(brand)
            scard.Line.Weight = 1.2
            shapes.append(scard)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, sx + 10, sy + 8, card_w - 20, card_h - 16)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"[DỊCH VỤ] {svc.get('name', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"Giao Thức: {svc.get('proto', '')}\nQuy Mô: {svc.get('scale', '')}"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.0
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 65. ARCH_DEFENSE_IN_DEPTH (Kiến Trúc Bảo Mật Đa Tầng)
    # =========================================================================
    def render_defense_in_depth(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        layers = spec.get("arch_data", {}).get("shields", [
            {"tier": "LỚP 1: VÀNH ĐAI MẠNG (EDGE)", "tool": "Cloudflare DDoS, WAF, DNSSEC"},
            {"tier": "LỚP 2: ĐIỀU PHỐI DANH TÍNH (IAM)", "tool": "MFA, Zero-Trust, RBAC Least Privilege"},
            {"tier": "LỚP 3: AN TOÀN ỨNG DỤNG (APPSEC)", "tool": "SAST/DAST, Token Encryption, Rate Limiting"},
            {"tier": "LỚP 4: BẢO VỆ DỮ LIỆU CỐT LÕI (DATA)", "tool": "AES-256 at Rest, TLS 1.3 in Transit, KMS HSM"}
        ])

        count = len(layers)
        layer_h = (height - (count - 1) * 8.0) / count

        for i in range(count):
            ly = top + i * (layer_h + 8.0)
            l_info = layers[i]
            is_core = (i == count - 1)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ly, width, layer_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(brand if is_core else surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 2.0 if is_core else 1.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 16, ly + 6, width - 32, layer_h - 12)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"🛡️ {l_info.get('tier', '')}: "
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_core else brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = l_info.get("tool", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0" if is_core else muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 66. ARCH_CLOUD_HYBRID_INFRA (Hạ Tầng Đám Mây Lai - Hybrid Cloud)
    # =========================================================================
    def render_cloud_hybrid_infra(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        col_w = (width - 40.0) / 2.0

        # Left Column: On-Premises Private Data Center
        l_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, col_w, height)
        l_card.Fill.Solid()
        l_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        l_card.Line.Visible = msoTrue
        l_card.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(l_card)

        ltb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 15, top + 15, col_w - 30, height - 30)
        ltf = ltb.TextFrame
        ltf.WordWrap = msoTrue
        lp1 = ltf.TextRange.Paragraphs(1)
        lp1.Text = "HẠ TẦNG NỘI BỘ (ON-PREMISES)\n\n"
        lp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        lp1.Font.Size = 12
        lp1.Font.Bold = msoTrue
        lp1.Font.Color.RGB = hex_to_bgr(ink)

        lp2 = ltf.TextRange.Paragraphs(2)
        lp2.Text = "• Cụm máy chủ Bare-Metal riêng\n• Dữ liệu tuyệt mật tuân thủ quy định\n• Kết nối VPN chuyên dụng Interconnect 10Gbps\n• Hệ thống lưu trữ SAN độ trễ thấp"
        lp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        lp2.Font.Size = 10
        lp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(ltb)

        # Right Column: Public Multi-Cloud (GCP / AWS)
        rx = left + col_w + 40.0
        r_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top, col_w, height)
        r_card.Fill.Solid()
        r_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        r_card.Line.Visible = msoTrue
        r_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        r_card.Line.Weight = 2.0
        shapes.append(r_card)

        rtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 15, top + 15, col_w - 30, height - 30)
        rtf = rtb.TextFrame
        rtf.WordWrap = msoTrue
        rp1 = rtf.TextRange.Paragraphs(1)
        rp1.Text = "ĐÁM MÂY CÔNG CỘNG (PUBLIC CLOUD)\n\n"
        rp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        rp1.Font.Size = 12
        rp1.Font.Bold = msoTrue
        rp1.Font.Color.RGB = hex_to_bgr(brand)

        rp2 = rtf.TextRange.Paragraphs(2)
        rp2.Text = "• Tự động co giãn theo tải (Serverless)\n• Tính toán AI GPU Cluster H100/TPU\n• Lưu trữ dữ liệu lớn Lakehouse\n• Khả năng dự phòng thảm họa đa vùng (Multi-Region)"
        rp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        rp2.Font.Size = 10
        rp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(rtb)

        # Interconnect Arrow
        arr = slide.Shapes.AddShape(msoShapeLeftRightArrow, left + col_w + 5.0, top + height/2.0 - 10.0, 30.0, 20.0)
        arr.Fill.Solid()
        arr.Fill.ForeColor.RGB = hex_to_bgr(brand)
        arr.Line.Visible = msoFalse
        shapes.append(arr)

        return shapes

    # =========================================================================
    # 67. ARCH_BUS_BAR_MODULAR (Kiến Trúc Trục Xe Buýt - Bus Bar)
    # =========================================================================
    def render_bus_bar_modular(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        # Central Event Bus Spine
        bus_y = top + height / 2.0 - 15.0
        bus = slide.Shapes.AddShape(msoShapeRectangle, left, bus_y, width, 30.0)
        bus.Fill.Solid()
        bus.Fill.ForeColor.RGB = hex_to_bgr(brand)
        bus.Line.Visible = msoFalse
        shapes.append(bus)

        btf = bus.TextFrame
        bp = btf.TextRange
        bp.Text = "KAFKA / PUBSUB EVENT BUS SPINE (10M EVENT/GIÂY)"
        bp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        bp.Font.Size = 11
        bp.Font.Bold = msoTrue
        bp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        bp.ParagraphFormat.Alignment = ppAlignCenter

        # 3 Modules on Top (Producers), 3 Modules on Bottom (Consumers)
        mod_w = (width - 2 * 14.0) / 3.0
        mod_h = (height / 2.0) - 35.0

        for i in range(3):
            mx = left + i * (mod_w + 14.0)
            # Top Module
            tm = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx, top, mod_w, mod_h)
            tm.Fill.Solid()
            tm.Fill.ForeColor.RGB = hex_to_bgr(surface)
            tm.Line.Visible = msoTrue
            tm.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(tm)

            t_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, mx + 8, top + 6, mod_w - 16, mod_h - 12)
            t_tf = t_tb.TextFrame
            t_tf.WordWrap = msoTrue
            tp1 = t_tf.TextRange
            tp1.Text = f"NGUỒN PHÁT 0{i+1}\n(Event Producer {i+1})"
            tp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            tp1.Font.Size = 9.5
            tp1.Font.Bold = msoTrue
            tp1.Font.Color.RGB = hex_to_bgr(ink)
            tp1.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(t_tb)

            # Bottom Module
            bm_y = bus_y + 45.0
            bm = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx, bm_y, mod_w, mod_h)
            bm.Fill.Solid()
            bm.Fill.ForeColor.RGB = hex_to_bgr(surface)
            bm.Line.Visible = msoTrue
            bm.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(bm)

            b_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, mx + 8, bm_y + 6, mod_w - 16, mod_h - 12)
            b_tf = b_tb.TextFrame
            b_tf.WordWrap = msoTrue
            bp1 = b_tf.TextRange
            bp1.Text = f"BỘ TIÊU THỤ 0{i+1}\n(Event Consumer {i+1})"
            bp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            bp1.Font.Size = 9.5
            bp1.Font.Bold = msoTrue
            bp1.Font.Color.RGB = hex_to_bgr(brand)
            bp1.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(b_tb)

        return shapes

    # =========================================================================
    # 68. ARCH_HEXAGONAL_PORTS (Kiến Trúc Lục Giác - Ports/Adapters)
    # =========================================================================
    def render_hexagonal_ports(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        cx = left + width / 2.0
        cy = top + height / 2.0
        hex_w = min(width * 0.45, 240.0)
        hex_h = min(height * 0.75, 200.0)

        # Center Hexagon: Core Business Domain
        core = slide.Shapes.AddShape(msoShapeHexagon, cx - hex_w/2.0, cy - hex_h/2.0, hex_w, hex_h)
        core.Fill.Solid()
        core.Fill.ForeColor.RGB = hex_to_bgr(surface)
        core.Line.Visible = msoTrue
        core.Line.ForeColor.RGB = hex_to_bgr(brand)
        core.Line.Weight = 2.5
        shapes.append(core)

        ctb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx - hex_w/2.0 + 20, cy - 40, hex_w - 40, 80)
        ctf = ctb.TextFrame
        ctf.WordWrap = msoTrue
        cp = ctf.TextRange
        cp.Text = "LÕI NGHIỆP VỤ\n(DOMAIN ENTITIES)\nĐộc lập hoàn toàn"
        cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cp.Font.Size = 11
        cp.Font.Bold = msoTrue
        cp.Font.Color.RGB = hex_to_bgr(brand)
        cp.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(ctb)

        # Left Inbound Adapter Card
        in_w = (width - hex_w) / 2.0 - 20.0
        in_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + 20, in_w, height - 40)
        in_card.Fill.Solid()
        in_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        in_card.Line.Visible = msoTrue
        in_card.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(in_card)

        itb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 10, top + 35, in_w - 20, height - 70)
        itf = itb.TextFrame
        itf.WordWrap = msoTrue
        ip = itf.TextRange
        ip.Text = "CỔNG VÀO (INBOUND)\n\n• REST Controller\n• GraphQL Resolvers\n• CLI Commands\n• Webhook Listeners"
        ip.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        ip.Font.Size = 10
        ip.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(itb)

        # Right Outbound Adapter Card
        rx = cx + hex_w/2.0 + 20.0
        out_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top + 20, in_w, height - 40)
        out_card.Fill.Solid()
        out_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        out_card.Line.Visible = msoTrue
        out_card.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(out_card)

        otb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, rx + 10, top + 35, in_w - 20, height - 70)
        otf = otb.TextFrame
        otf.WordWrap = msoTrue
        op = otf.TextRange
        op.Text = "CỔNG RA (OUTBOUND)\n\n• Database Repositories\n• External API Clients\n• Message Queue Pubs\n• File Cloud S3"
        op.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        op.Font.Size = 10
        op.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(otb)

        return shapes

    # =========================================================================
    # 69. ARCH_ECOSYSTEM_NETWORK (Mạng Lưới Giá Trị Hệ Sinh Thái)
    # =========================================================================
    def render_ecosystem_network(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        # 4 Blocks in Value Chain Loop: Suppliers -> Platform -> Developers -> End Consumers
        col_w = (width - 3 * 12.0) / 4.0
        items = [
            {"role": "NHÀ CUNG CẤP", "desc": "Nguồn nội dung & Dữ liệu API"},
            {"role": "NỀN TẢNG MAKE SLIDE", "desc": "Lõi điều phối AI & Engine đồ họa"},
            {"role": "CỘNG TÁC VIÊN", "desc": "Nhà phát triển Template & Plugin"},
            {"role": "NGƯỜI DÙNG CUỐI", "desc": "Doanh nghiệp, Giảng viên & Học sinh"}
        ]

        for i in range(4):
            it = items[i]
            ix = left + i * (col_w + 12.0)
            is_platform = (i == 1)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, ix, top + 20, col_w, height - 40)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(brand if is_platform else surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 2.0 if is_platform else 1.0
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, ix + 8, top + 35, col_w - 16, height - 70)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"0{i+1}\n{it.get('role', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_platform else brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = it.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr("#E2E8F0" if is_platform else muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 70. ARCH_MATRIX_ORGANIZATION (Cơ Cấu Tổ Chức Dạng Ma Trận)
    # =========================================================================
    def render_matrix_organization(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        # 3 Projects (Rows) x 3 Functional Units (Cols)
        header_h = 30.0
        label_w = 120.0
        col_w = (width - label_w - 20.0) / 3.0
        row_h = (height - header_h - 20.0) / 3.0

        depts = ["Đội Ngũ AI", "Đội Ngũ Frontend", "Đội Ngũ QA"]
        projects = ["Dự Án Alpha", "Dự Án Beta", "Dự Án Enterprise"]

        # Department Column Headers
        for c in range(3):
            cx = left + label_w + 10.0 + c * (col_w + 5.0)
            chdr = slide.Shapes.AddShape(msoShapeRectangle, cx, top, col_w, header_h)
            chdr.Fill.Solid()
            chdr.Fill.ForeColor.RGB = hex_to_bgr(brand)
            chdr.Line.Visible = msoFalse
            shapes.append(chdr)

            ctf = chdr.TextFrame
            cp = ctf.TextRange
            cp.Text = depts[c]
            cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            cp.Font.Size = 10
            cp.Font.Bold = msoTrue
            cp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            cp.ParagraphFormat.Alignment = ppAlignCenter

        # Project Rows
        for r in range(3):
            ry = top + header_h + 10.0 + r * (row_h + 5.0)
            rhdr = slide.Shapes.AddShape(msoShapeRectangle, left, ry, label_w, row_h)
            rhdr.Fill.Solid()
            rhdr.Fill.ForeColor.RGB = hex_to_bgr(surface)
            rhdr.Line.Visible = msoTrue
            rhdr.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(rhdr)

            rtf = rhdr.TextFrame
            rp = rtf.TextRange
            rp.Text = projects[r]
            rp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            rp.Font.Size = 10
            rp.Font.Bold = msoTrue
            rp.Font.Color.RGB = hex_to_bgr(ink)
            rp.ParagraphFormat.Alignment = ppAlignCenter

            for c in range(3):
                cx = left + label_w + 10.0 + c * (col_w + 5.0)
                cell = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, ry, col_w, row_h)
                cell.Fill.Solid()
                cell.Fill.ForeColor.RGB = hex_to_bgr(surface)
                cell.Line.Visible = msoTrue
                cell.Line.ForeColor.RGB = hex_to_bgr(border)
                shapes.append(cell)

                cell_tf = cell.TextFrame
                cp_cell = cell_tf.TextRange
                cp_cell.Text = f"Nhân Sự {depts[c][:4]} - {projects[r][-1]}"
                cp_cell.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
                cp_cell.Font.Size = 9.0
                cp_cell.Font.Color.RGB = hex_to_bgr(muted)
                cp_cell.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # =========================================================================
    # 71. ARCH_API_GATEWAY_HUB (Trung Tâm Điều Phối Cổng API)
    # =========================================================================
    def render_api_gateway_hub(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        client_w = width * 0.22
        gw_w = width * 0.32
        svc_w = width * 0.38

        # 1. Clients (Left)
        c_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + 20, client_w, height - 40)
        c_box.Fill.Solid()
        c_box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        c_box.Line.Visible = msoTrue
        c_box.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(c_box)

        ctb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 8, top + 35, client_w - 16, height - 70)
        ctf = ctb.TextFrame
        ctf.WordWrap = msoTrue
        cp = ctf.TextRange
        cp.Text = "KHÁCH HÀNG\n\n• Web Browser\n• Mobile iOS/Android\n• Public REST API\n• SDK Third-Party"
        cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cp.Font.Size = 10
        cp.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(ctb)

        # 2. Central API Gateway Hub
        gw_x = left + client_w + 15.0
        gw_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, gw_x, top, gw_w, height)
        gw_box.Fill.Solid()
        gw_box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        gw_box.Line.Visible = msoTrue
        gw_box.Line.ForeColor.RGB = hex_to_bgr(brand)
        gw_box.Line.Weight = 2.5
        shapes.append(gw_box)

        gtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, gw_x + 10, top + 15, gw_w - 20, height - 30)
        gtf = gtb.TextFrame
        gtf.WordWrap = msoTrue
        gp1 = gtf.TextRange.Paragraphs(1)
        gp1.Text = "API GATEWAY TRUNG TÂM\n\n"
        gp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        gp1.Font.Size = 11.5
        gp1.Font.Bold = msoTrue
        gp1.Font.Color.RGB = hex_to_bgr(brand)
        gp1.ParagraphFormat.Alignment = ppAlignCenter

        gp2 = gtf.TextRange.Paragraphs(2)
        gp2.Text = "• Cân Bằng Tải (Load Balancer)\n• Xác Thực Token JWT & Rate Limit\n• Chuyển Đổi Giao Thức (REST → gRPC)\n• Bộ Nhớ Đệm Redis Cache Phản Hồi"
        gp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        gp2.Font.Size = 9.5
        gp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(gtb)

        # 3. Microservices (Right)
        svc_x = left + width - svc_w
        svc_box = slide.Shapes.AddShape(msoShapeRoundedRectangle, svc_x, top + 20, svc_w, height - 40)
        svc_box.Fill.Solid()
        svc_box.Fill.ForeColor.RGB = hex_to_bgr(surface)
        svc_box.Line.Visible = msoTrue
        svc_box.Line.ForeColor.RGB = hex_to_bgr(border)
        shapes.append(svc_box)

        stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, svc_x + 8, top + 35, svc_w - 16, height - 70)
        stf = stb.TextFrame
        stf.WordWrap = msoTrue
        sp = stf.TextRange
        sp.Text = "CỤM DỊCH VỤ NỘI BỘ\n\n• Dịch Vụ Tạo Bài Học AI\n• Dịch Vụ Render PowerPoint COM\n• Dịch Vụ Thanh Toán & Thuê Bao\n• Dịch Vụ Quản Lý Tài Khoản"
        sp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        sp.Font.Size = 10
        sp.Font.Color.RGB = hex_to_bgr(ink)
        shapes.append(stb)

        return shapes

    # =========================================================================
    # 72. ARCH_DATA_GOVERNANCE_MESH (Lưới Quản Trị & Xuất Xứ Dữ Liệu)
    # =========================================================================
    def render_data_governance_mesh(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        domains = [
            {"name": "Domain Khách Hàng", "owner": "Data Team CRM", "sla": "99.9% Uptime"},
            {"name": "Domain Tài Chính", "owner": "Data Team ERP", "sla": "Strict Zero-Loss"},
            {"name": "Domain AI Models", "owner": "MLOps Engine", "sla": "Daily Retrain"},
            {"name": "Domain Vận Hành", "owner": "Platform Infra", "sla": "Realtime CDC"}
        ]

        count = len(domains)
        col_w = (width - (count - 1) * 12.0) / count

        for i in range(count):
            dm = domains[i]
            dx = left + i * (col_w + 12.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, dx, top, col_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(brand)
            card.Line.Weight = 1.2
            shapes.append(card)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, dx + 8, top + 15, col_w - 16, height - 30)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"{dm.get('name', '')}\n\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 11
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"• Quản Trị: {dm.get('owner', '')}\n• Tiêu Chuẩn: {dm.get('sla', '')}\n• Xuất Xứ: Lineage Tracked\n• Bảo Mật: PII Masked"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 9.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(tb)

        return shapes

    # =========================================================================
    # 73. ARCH_CLEAN_ONION_STACK (Kiến Trúc Củ Hành - Clean Onion)
    # =========================================================================
    def render_clean_onion_stack(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")

        cx = left + width / 2.0
        cy = top + height / 2.0
        max_r = min(width, height) * 0.46

        # 3 Concentric Rings
        radii = [max_r, max_r * 0.72, max_r * 0.42]
        labels = [
            "VÒNG NGOÀI: HẠ TẦNG & GIAO DIỆN (UI, DB, DEVICES)",
            "VÒNG GIỮA: TRÌNH ĐIỀU PHỐI (USE CASES)",
            "LÕI TRONG:\nTHỰC THỂ\n(ENTITIES)"
        ]

        for i in range(3):
            r = radii[i]
            circle = slide.Shapes.AddShape(msoShapeOval, cx - r, cy - r, r * 2, r * 2)
            circle.Fill.Solid()
            circle.Fill.ForeColor.RGB = hex_to_bgr(brand if i == 2 else surface)
            circle.Line.Visible = msoTrue
            circle.Line.ForeColor.RGB = hex_to_bgr(brand)
            circle.Line.Weight = 2.0
            shapes.append(circle)

        # Center Text
        ctb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx - radii[2] + 10, cy - 35, radii[2] * 2 - 20, 70)
        ctf = ctb.TextFrame
        ctf.WordWrap = msoTrue
        cp = ctf.TextRange
        cp.Text = labels[2]
        cp.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        cp.Font.Size = 10.5
        cp.Font.Bold = msoTrue
        cp.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        cp.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(ctb)

        return shapes

    # =========================================================================
    # 74. ARCH_CONTAINER_CLUSTER_K8S (Cụm Điều Phối Container - K8s)
    # =========================================================================
    def render_container_cluster_k8s(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        master_w = width * 0.32
        worker_w = (width - master_w - 30.0) / 2.0

        # Master Node (Control Plane)
        m_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, master_w, height)
        m_card.Fill.Solid()
        m_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
        m_card.Line.Visible = msoTrue
        m_card.Line.ForeColor.RGB = hex_to_bgr(brand)
        m_card.Line.Weight = 2.0
        shapes.append(m_card)

        mtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 12, top + 15, master_w - 24, height - 30)
        mtf = mtb.TextFrame
        mtf.WordWrap = msoTrue
        mp1 = mtf.TextRange.Paragraphs(1)
        mp1.Text = "K8S CONTROL PLANE (MASTER)\n\n"
        mp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        mp1.Font.Size = 11
        mp1.Font.Bold = msoTrue
        mp1.Font.Color.RGB = hex_to_bgr(brand)

        mp2 = mtf.TextRange.Paragraphs(2)
        mp2.Text = "• kube-apiserver: Cổng điều khiển trung tâm\n• etcd: Kho lưu trạng thái phân tán\n• kube-scheduler: Phân bổ tài nguyên Pod\n• controller-manager: Duy trì trạng thái mong muốn"
        mp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        mp2.Font.Size = 9.5
        mp2.Font.Color.RGB = hex_to_bgr(muted)
        shapes.append(mtb)

        # 2 Worker Nodes
        for w_idx in range(2):
            wx = left + master_w + 15.0 + w_idx * (worker_w + 15.0)
            w_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, wx, top, worker_w, height)
            w_card.Fill.Solid()
            w_card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            w_card.Line.Visible = msoTrue
            w_card.Line.ForeColor.RGB = hex_to_bgr(border)
            shapes.append(w_card)

            wtb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, wx + 10, top + 15, worker_w - 20, height - 30)
            wtf = wtb.TextFrame
            wtf.WordWrap = msoTrue
            wp1 = wtf.TextRange.Paragraphs(1)
            wp1.Text = f"WORKER NODE 0{w_idx+1}\n\n"
            wp1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            wp1.Font.Size = 11
            wp1.Font.Bold = msoTrue
            wp1.Font.Color.RGB = hex_to_bgr(ink)

            wp2 = wtf.TextRange.Paragraphs(2)
            wp2.Text = "• kubelet & kube-proxy\n• Container Runtime (containerd)\n• Pod 1: AI Reasoning Engine\n• Pod 2: PowerPoint COM Worker"
            wp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            wp2.Font.Size = 9.5
            wp2.Font.Color.RGB = hex_to_bgr(muted)
            shapes.append(wtb)

        return shapes

    # =========================================================================
    # 75. ARCH_AI_AGENT_ORCHESTRATOR (Kiến Trúc Điều Phối Đa Tác Tử AI)
    # =========================================================================
    def render_ai_agent_orchestrator(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#CBD5E1")
        border = self._get_token("colors", "card_border", "#1E293B")

        # Top Center Orchestrator
        orch_w = width * 0.6
        orch_x = left + (width - orch_w) / 2.0
        orch_h = 65.0

        orch = slide.Shapes.AddShape(msoShapeRoundedRectangle, orch_x, top, orch_w, orch_h)
        orch.Fill.Solid()
        orch.Fill.ForeColor.RGB = hex_to_bgr(brand)
        orch.Line.Visible = msoFalse
        shapes.append(orch)

        otf = orch.TextFrame
        otf.WordWrap = msoTrue
        op = otf.TextRange
        op.Text = "AI AGENT ORCHESTRATOR TRUNG TÂM\nĐiều Phối & Tổng Hợp Kết Quả Đa Chiều"
        op.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        op.Font.Size = 11.5
        op.Font.Bold = msoTrue
        op.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        op.ParagraphFormat.Alignment = ppAlignCenter

        # 4 Specialist Agent Pods below
        agents = [
            {"role": "CHUYÊN GIA DỮ LIỆU", "task": "Kiểm định số liệu & công thức kế toán"},
            {"role": "KIẾN TRÚC SƯ BLUEPRINT", "task": "Bố cục thị giác & phân bổ tỷ lệ vàng"},
            {"role": "CHUYÊN GIA VECTOR SHAPE", "task": "Sinh 110+ mô hình hình học chuẩn xác"},
            {"role": "HỘI ĐỒNG KIỂM ĐỊNH MACC", "task": "34 tiêu chí chất lượng tự động hóa"}
        ]

        count = len(agents)
        card_w = (width - (count - 1) * 12.0) / count
        card_y = top + orch_h + 30.0
        card_h = height - (card_y - top)

        for i in range(count):
            ag = agents[i]
            ax = left + i * (card_w + 12.0)

            acard = slide.Shapes.AddShape(msoShapeRoundedRectangle, ax, card_y, card_w, card_h)
            acard.Fill.Solid()
            acard.Fill.ForeColor.RGB = hex_to_bgr(surface)
            acard.Line.Visible = msoTrue
            acard.Line.ForeColor.RGB = hex_to_bgr(brand)
            acard.Line.Weight = 1.2
            shapes.append(acard)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, ax + 8, card_y + 12, card_w - 16, card_h - 24)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = f"TÁC TỬ 0{i+1}\n{ag.get('role', '')}\n"
            p1.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            p1.Font.Size = 10
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = ag.get("task", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 8.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes
