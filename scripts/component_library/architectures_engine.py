"""
architectures_engine.py
Exhaustive System, Technology, and Hierarchy Architecture Engine for Make Slide Pro V8.5.0.
Generates 15 classic software, cloud, network, and organizational diagrams
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
            p1.Font.Size = 15.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand if is_top else ink)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"Công Nghệ: {l_data.get('tech', '')} — {l_data.get('desc', '')}"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
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
        tp.Font.Size = 15.0
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
            sp1.Font.Size = 14.5
            sp1.Font.Bold = msoTrue
            sp1.Font.Color.RGB = hex_to_bgr(brand)
            sp1.ParagraphFormat.Alignment = ppAlignCenter

            sp2 = stf.TextRange.Paragraphs(2)
            sp2.Text = sn.get("desc", "")
            sp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            sp2.Font.Size = 16.0.5
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
        cp.Font.Size = 14.5
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
            p1.Font.Size = 15.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = b_info.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
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
            p1.Font.Size = 14.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"Giao Thức: {svc.get('proto', '')}\nQuy Mô: {svc.get('scale', '')}"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
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
            p1.Font.Size = 15.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_core else brand)

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = l_info.get("tool", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
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
        lp1.Font.Size = 15.5
        lp1.Font.Bold = msoTrue
        lp1.Font.Color.RGB = hex_to_bgr(ink)

        lp2 = ltf.TextRange.Paragraphs(2)
        lp2.Text = "• Cụm máy chủ Bare-Metal riêng\n• Dữ liệu tuyệt mật tuân thủ quy định\n• Kết nối VPN chuyên dụng Interconnect 10Gbps\n• Hệ thống lưu trữ SAN độ trễ thấp"
        lp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        lp2.Font.Size = 14.5
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
        rp1.Font.Size = 15.5
        rp1.Font.Bold = msoTrue
        rp1.Font.Color.RGB = hex_to_bgr(brand)

        rp2 = rtf.TextRange.Paragraphs(2)
        rp2.Text = "• Tự động co giãn theo tải (Serverless)\n• Tính toán AI GPU Cluster H100/TPU\n• Lưu trữ dữ liệu lớn Lakehouse\n• Khả năng dự phòng thảm họa đa vùng (Multi-Region)"
        rp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        rp2.Font.Size = 14.5
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
        bp.Font.Size = 15.0
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
            tp1.Font.Size = 16.0.5
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
            bp1.Font.Size = 16.0.5
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
        cp.Font.Size = 15.0
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
        ip.Font.Size = 14.5
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
        op.Font.Size = 14.5
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
            p1.Font.Size = 15.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr("#FFFFFF" if is_platform else brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = it.get("desc", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
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
            cp.Font.Size = 14.5
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
            rp.Font.Size = 14.5
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
                cp_cell.Font.Size = 16.0.5
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
        cp.Font.Size = 14.5
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
        gp1.Font.Size = 15.0
        gp1.Font.Bold = msoTrue
        gp1.Font.Color.RGB = hex_to_bgr(brand)
        gp1.ParagraphFormat.Alignment = ppAlignCenter

        gp2 = gtf.TextRange.Paragraphs(2)
        gp2.Text = "• Cân Bằng Tải (Load Balancer)\n• Xác Thực Token JWT & Rate Limit\n• Chuyển Đổi Giao Thức (REST → gRPC)\n• Bộ Nhớ Đệm Redis Cache Phản Hồi"
        gp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        gp2.Font.Size = 16.0.5
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
        sp.Font.Size = 14.5
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
            p1.Font.Size = 15.0
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = f"• Quản Trị: {dm.get('owner', '')}\n• Tiêu Chuẩn: {dm.get('sla', '')}\n• Xuất Xứ: Lineage Tracked\n• Bảo Mật: PII Masked"
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
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
        cp.Font.Size = 14.5
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
        mp1.Font.Size = 15.0
        mp1.Font.Bold = msoTrue
        mp1.Font.Color.RGB = hex_to_bgr(brand)

        mp2 = mtf.TextRange.Paragraphs(2)
        mp2.Text = "• kube-apiserver: Cổng điều khiển trung tâm\n• etcd: Kho lưu trạng thái phân tán\n• kube-scheduler: Phân bổ tài nguyên Pod\n• controller-manager: Duy trì trạng thái mong muốn"
        mp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
        mp2.Font.Size = 16.0.5
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
            wp1.Font.Size = 15.0
            wp1.Font.Bold = msoTrue
            wp1.Font.Color.RGB = hex_to_bgr(ink)

            wp2 = wtf.TextRange.Paragraphs(2)
            wp2.Text = "• kubelet & kube-proxy\n• Container Runtime (containerd)\n• Pod 1: AI Reasoning Engine\n• Pod 2: PowerPoint COM Worker"
            wp2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            wp2.Font.Size = 16.0.5
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
        op.Font.Size = 15.0
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
            p1.Font.Size = 14.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(brand)
            p1.ParagraphFormat.Alignment = ppAlignCenter

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = ag.get("task", "")
            p2.Font.Name = self._get_token("fonts", "secondary", "Segoe UI")
            p2.Font.Size = 16.0.5
            p2.Font.Color.RGB = hex_to_bgr(muted)
            p2.ParagraphFormat.Alignment = ppAlignCenter
            shapes.append(tb)

        return shapes

    # 16. ARCH_EVENT_DRIVEN_KAFKA (Kiến Trúc Hướng Sự Kiện Kafka)
    def render_event_driven_kafka(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        col_w = width * 0.28
        bus_w = width * 0.36
        gap = (width - 2 * col_w - bus_w) / 2.0

        # Left Column: Event Producers
        prod = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, col_w, height)
        prod.Fill.Solid()
        prod.Fill.ForeColor.RGB = hex_to_bgr(surface)
        prod.Line.Visible = msoTrue
        prod.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        prod.Line.Weight = 2.0
        shapes.append(prod)
        t_prod = prod.TextFrame.TextRange
        t_prod.Text = "NGUỒN PHÁT SỰ KIỆN\n(EVENT PRODUCERS)\n\n• Web Studio Frontend\n• AI Agent Workflow API\n• Batch PPTX Generator\n• Webhook Triggers"
        t_prod.Font.Size = 14.5
        t_prod.Font.Color.RGB = hex_to_bgr(ink)

        # Center Column: Kafka Event Streaming Bus
        bus = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + col_w + gap, top, bus_w, height)
        bus.Fill.Solid()
        bus.Fill.ForeColor.RGB = hex_to_bgr("#082F49")
        bus.Line.Visible = msoTrue
        bus.Line.ForeColor.RGB = hex_to_bgr(brand)
        bus.Line.Weight = 2.5
        shapes.append(bus)
        t_bus = bus.TextFrame.TextRange
        t_bus.Text = "CỤM KAFKA STREAMING BUS\n(DISTRIBUTED LOG TOPICS)\n\n[Topic 1: Deck_Creation_Requests]\n[Topic 2: Agent_Audit_Events]\n[Topic 3: Motion_Render_Tasks]\n[Topic 4: High_Res_PNG_Exports]"
        t_bus.Font.Size = 15.0
        t_bus.Font.Bold = msoTrue
        t_bus.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        t_bus.ParagraphFormat.Alignment = ppAlignCenter

        # Right Column: Event Consumers & Microservices
        cons = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + col_w + bus_w + 2 * gap, top, col_w, height)
        cons.Fill.Solid()
        cons.Fill.ForeColor.RGB = hex_to_bgr(surface)
        cons.Line.Visible = msoTrue
        cons.Line.ForeColor.RGB = hex_to_bgr("#10B981")
        cons.Line.Weight = 2.0
        shapes.append(cons)
        t_cons = cons.TextFrame.TextRange
        atoms = spec.get("atoms", [])
        if atoms and len(atoms) > 1:
            c_items = [f"• {a.get('title', '')}: {a.get('text', '')}" if isinstance(a, dict) else f"• {str(a)}" for a in atoms[1:4]]
            t_cons.Text = "TIẾP NHẬN & XỬ LÝ\n(DATA CONSUMERS)\n\n" + "\n".join(c_items)
        else:
            t_cons.Text = "TIẾP NHẬN & XỬ LÝ\n(DATA CONSUMERS)\n\n• Cơ sở y tế tiếp nhận\n• Đội ngũ cán bộ chuyên trách\n• Hệ thống lưu trữ hồ sơ\n• Báo cáo giám sát định kỳ"
        t_cons.Font.Size = 14.5
        t_cons.Font.Color.RGB = hex_to_bgr(ink)

        return shapes

    # 17. ARCH_SERVERLESS_EVENT_FLOW (Kiến Trúc Không Máy Chủ Serverless)
    def render_serverless_event_flow(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        steps = [
            ("1. KHÁCH HÀNG (CLIENT)", "Trình duyệt Web Studio / SDK Desktop gửi yêu cầu", "#64748B"),
            ("2. CỔNG API GATEWAY", "Xác thực JWT token & Điều phối hạn mức (Rate-limit)", "#0284C7"),
            ("3. HÀM CLOUD FUNCTIONS", "Tự động kích hoạt các worker tính toán không trạng thái", "#38BDF8"),
            ("4. CƠ SỞ DỮ LIỆU QUẢN TRỊ", "Lưu trữ cấu hình Blueprint & Lịch sử phiên bản", "#10B981")
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
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 18. ARCH_ZERO_TRUST_SECURITY (Kiến Trúc An Ninh Zero Trust 5 Lớp)
    def render_zero_trust_security(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        layers = [
            ("LỚP 1: XÁC THỰC DANH TÍNH (IDENTITY)", "MFA đa yếu tố & Chứng chỉ số PKI cho mọi phiên kết nối", "#0284C7"),
            ("LỚP 2: KIỂM SOÁT THIẾT BỊ (DEVICE)", "Đánh giá trạng thái tuân thủ bảo mật thiết bị đầu cuối", "#38BDF8"),
            ("LỚP 3: PHÂN ĐOẠN MẠNG VI MÔ (NETWORK)", "Tường lửa phân đoạn mạng ảo & mã hóa đường truyền mTLS", "#10B981"),
            ("LỚP 4: BẢO VỆ ỨNG DỤNG (APPLICATION)", "Quét lỗ hổng tĩnh/động SAST & Bảo vệ runtime WAF", "#F59E0B"),
            ("LỚP 5: BẢO MẬT DỮ LIỆU CỐT LÕI (DATA)", "Mã hóa AES-256 dữ liệu lưu trữ & Ngăn rò rỉ dữ liệu DLP", "#EF4444")
        ]

        row_h = (height - 24.0) / len(layers)
        for i, (title, desc, color) in enumerate(layers):
            ry = top + i * (row_h + 6.0)
            sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, ry, width, row_h)
            sh.Fill.Solid()
            sh.Fill.ForeColor.RGB = hex_to_bgr(surface)
            sh.Line.Visible = msoTrue
            sh.Line.ForeColor.RGB = hex_to_bgr(color)
            sh.Line.Weight = 2.0
            shapes.append(sh)

            tr = sh.TextFrame.TextRange
            tr.Text = f"{title}: {desc}"
            tr.Font.Size = 14.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignLeft

        return shapes

    # 19. ARCH_DATA_LAKEHOUSE_MEDALLION (Kiến Trúc Hồ Dữ Liệu Medallion 3 Tầng)
    def render_data_lakehouse_medallion(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")

        tiers = spec.get("medallion_tiers") or [
            {
                "tier": "TẦNG 01: BRONZE",
                "sub": "RAW DATA INGESTION",
                "color": "#B45309",
                "bg_tint": "#2A1705" if self.theme == "DARK" else "#FEF3C7",
                "specs": [
                    "• Nguồn: Streaming logs, Kafka, CDC, S3 files",
                    "• Định dạng: JSON/Parquet nguyên bản chưa lọc",
                    "• Lưu trữ: Append-only, cam kết Zero data loss"
                ],
                "chip": "Trạng Thái: Dữ Liệu Thô Sơ"
            },
            {
                "tier": "TẦNG 02: SILVER",
                "sub": "CURATED & CLEANED",
                "color": "#94A3B8",
                "bg_tint": "#1E293B" if self.theme == "DARK" else "#F1F5F9",
                "specs": [
                    "• Tiền xử lý: Khử trùng lặp, lọc schema & null",
                    "• Cấu trúc hóa: Bảng Dimension & Fact chuẩn hóa",
                    "• Bảo toàn: Delta Lake ACID Transactions"
                ],
                "chip": "Trạng Thái: Đã Chuẩn Hóa"
            },
            {
                "tier": "TẦNG 03: GOLD",
                "sub": "BUSINESS AGGREGATED",
                "color": "#EAB308",
                "bg_tint": "#2D2200" if self.theme == "DARK" else "#FEF9C3",
                "specs": [
                    "• Tổng hợp: Star Schema, Data Marts theo ngành",
                    "• Tiêu thụ: BI Dashboards, C-Level KPI & AI/ML",
                    "• SLA: Độ chính xác 100%, truy vấn < 1s"
                ],
                "chip": "Trạng Thái: Sẵn Sàng BI & AI"
            }
        ]

        card_gap = 42.0
        card_w = (width - 2 * card_gap) / 3.0
        card_h = min(height - 40.0, 275.0)
        card_y = top + 10.0

        # Create Bottom Architecture Summary Strip first so it binds with Tier 0
        sum_shapes = []
        sum_y = card_y + card_h + 14.0
        sum_bar = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, sum_y, width, 26)
        sum_bar.Fill.Solid()
        sum_bar.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
        sum_bar.Line.Visible = msoFalse
        sum_shapes.append(sum_bar)

        st = sum_bar.TextFrame.TextRange
        summary_text = spec.get("summary_strip") or spec.get("architecture_summary") or spec.get("summary_text") or spec.get("bottom_note")
        if not summary_text:
            summary_text = "HỆ THỐNG PHÂN CẤP CHỈ ĐẠO & CUNG ỨNG DỊCH VỤ DÂN SỐ LIÊN HOÀN TOÀN TUYẾN"
        st.Text = summary_text
        st.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        st.Font.Size = 14.5
        st.Font.Bold = msoTrue
        st.Font.Color.RGB = hex_to_bgr("#38BDF8")
        sum_bar.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter

        card_coords = []
        for i, item in enumerate(tiers):
            t_shapes = []
            cx = left + i * (card_w + card_gap)
            card_coords.append((cx, card_y))
            color = item["color"]

            # Flow Arrow incoming from previous tier (atoms bound to current tier)
            if i > 0 and len(card_coords) > 1:
                x_start = card_coords[i - 1][0] + card_w
                y_mid = card_y + card_h / 2.0
                x_end = cx
                conn = add_vector_connector(slide, x_start, y_mid, x_end, y_mid, color=color, weight=2.5, arrowhead=True)
                if conn:
                    t_shapes.append(conn)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(item["bg_tint"])
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(color)
            card.Line.Weight = 2.0
            t_shapes.append(card)

            # Top Header Pill
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 12, card_y + 12, card_w - 24, 26)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(color)
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = item["tier"]
            pt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            pt.Font.Size = 15.0
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr("#0F172A" if color == "#EAB308" else "#FFFFFF")
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            t_shapes.append(pill)

            # Subtitle
            tb_sub = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 10, card_y + 42, card_w - 20, 24)
            stf = tb_sub.TextFrame
            stf.WordWrap = msoTrue
            stf.MarginLeft = 0
            stf.MarginRight = 0
            stt = stf.TextRange
            stt.Text = item["sub"]
            stt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            stt.Font.Size = 14.5
            stt.Font.Bold = msoTrue
            stt.Font.Color.RGB = hex_to_bgr(color)
            stt.ParagraphFormat.Alignment = ppAlignCenter
            t_shapes.append(tb_sub)

            # Divider line
            div = slide.Shapes.AddShape(msoShapeRectangle, cx + 16, card_y + 70, card_w - 32, 1.5)
            div.Fill.Solid()
            div.Fill.ForeColor.RGB = hex_to_bgr(color)
            div.Line.Visible = msoFalse
            t_shapes.append(div)

            # Specs Bullets
            tb_spec = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 12, card_y + 78, card_w - 24, card_h - 120)
            btf = tb_spec.TextFrame
            btf.WordWrap = msoTrue
            btf.MarginLeft = 0
            btf.MarginRight = 0
            btt = btf.TextRange
            btt.Text = "\n\n".join(item["specs"])
            btt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            btt.Font.Size = 14.5
            btt.Font.Color.RGB = hex_to_bgr(ink if self.theme == "DARK" else "#334155")
            btt.ParagraphFormat.Alignment = ppAlignLeft
            t_shapes.append(tb_spec)

            # Bottom Status Chip
            chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 14, card_y + card_h - 32, card_w - 28, 22)
            chip.Fill.Solid()
            chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            chip.Line.Visible = msoFalse
            ct = chip.TextFrame.TextRange
            ct.Text = item["chip"]
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 16.0.5
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(color)
            chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            t_shapes.append(chip)

            # Anchor summary bar to Tier 0 so it appears on slide transition without an extra click
            if i == 0:
                t_shapes.append(sum_bar)

            tier_grp = safe_group(slide, t_shapes, f"Medallion_Tier_{i+1}")
            shapes.append(tier_grp)

        return shapes

    # 20. ARCH_CI_CD_AUTOMATION (Quy Trình Tự Động Hóa CI/CD 4 Bước)
    def render_ci_cd_automation(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        stages = [
            ("BƯỚC 1: GIT COMMIT", "Lập trình viên commit mã nguồn lên nhánh main", "#0284C7"),
            ("BƯỚC 2: BUILD & UNIT TEST", "Chạy 48/48 bài kiểm thử tự động pytest trong 2.5s", "#38BDF8"),
            ("BƯỚC 3: MACC QA AUDIT", "Hội đồng 16 tác tử quét lỗi hồi quy và độ chuẩn font", "#10B981"),
            ("BƯỚC 4: DEPLOY PRODUCTION", "Phát hành bản cập nhật an toàn không downtime", "#059669")
        ]

        card_w = (width - 36.0) / 4.0
        for i, (title, desc, color) in enumerate(stages):
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
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 21. ARCH_HUB_SPOKE_ENTERPRISE_NETWORK (Mạng Doanh Nghiệp Hub-Spoke)
    def render_hub_spoke_enterprise_network(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Center Hub (Transit Gateway & Shared Core Services)
        hub_w = width * 0.32
        hub_h = height * 0.65
        hx = left + (width - hub_w) / 2.0
        hy = top + (height - hub_h) / 2.0

        hub = slide.Shapes.AddShape(msoShapeRoundedRectangle, hx, hy, hub_w, hub_h)
        hub.Fill.Solid()
        hub.Fill.ForeColor.RGB = hex_to_bgr("#0C4A6E")
        hub.Line.Visible = msoTrue
        hub.Line.ForeColor.RGB = hex_to_bgr(brand)
        hub.Line.Weight = 2.5
        shapes.append(hub)
        t_hub = hub.TextFrame.TextRange
        t_hub.Text = "TRUNG TÂM ĐIỀU HÀNH (CORE HUB)\n\n• Transit Gateway Router\n• Shared Database Cluster\n• Central Authentication SSO\n• Master Component Registry"
        t_hub.Font.Size = 14.5
        t_hub.Font.Bold = msoTrue
        t_hub.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        t_hub.ParagraphFormat.Alignment = ppAlignCenter

        # Left Spokes (Spoke 1 & Spoke 2)
        spoke_w = width * 0.28
        spoke_h = (height - 16.0) / 2.0
        s1 = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, spoke_w, spoke_h)
        s1.Fill.Solid()
        s1.Fill.ForeColor.RGB = hex_to_bgr(surface)
        s1.Line.Visible = msoTrue
        s1.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        shapes.append(s1)
        s1.TextFrame.TextRange.Text = "SPOKE 1: WEB STUDIO\nFrontend Interactive Editor"
        s1.TextFrame.TextRange.Font.Size = 14.5
        s1.TextFrame.TextRange.Font.Color.RGB = hex_to_bgr(ink)

        s2 = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top + spoke_h + 16.0, spoke_w, spoke_h)
        s2.Fill.Solid()
        s2.Fill.ForeColor.RGB = hex_to_bgr(surface)
        s2.Line.Visible = msoTrue
        s2.Line.ForeColor.RGB = hex_to_bgr("#38BDF8")
        shapes.append(s2)
        s2.TextFrame.TextRange.Text = "SPOKE 2: DESKTOP COM ENGINE\nNative PowerPoint Automation"
        s2.TextFrame.TextRange.Font.Size = 14.5
        s2.TextFrame.TextRange.Font.Color.RGB = hex_to_bgr(ink)

        # Right Spokes (Spoke 3 & Spoke 4)
        rx = left + hub_w + spoke_w + 24.0
        s3 = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top, spoke_w, spoke_h)
        s3.Fill.Solid()
        s3.Fill.ForeColor.RGB = hex_to_bgr(surface)
        s3.Line.Visible = msoTrue
        s3.Line.ForeColor.RGB = hex_to_bgr("#10B981")
        shapes.append(s3)
        s3.TextFrame.TextRange.Text = "SPOKE 3: MACC QA AUDIT\n16 Tác Tử Kiểm Định Đa Chiều"
        s3.TextFrame.TextRange.Font.Size = 14.5
        s3.TextFrame.TextRange.Font.Color.RGB = hex_to_bgr(ink)

        s4 = slide.Shapes.AddShape(msoShapeRoundedRectangle, rx, top + spoke_h + 16.0, spoke_w, spoke_h)
        s4.Fill.Solid()
        s4.Fill.ForeColor.RGB = hex_to_bgr(surface)
        s4.Line.Visible = msoTrue
        s4.Line.ForeColor.RGB = hex_to_bgr("#10B981")
        shapes.append(s4)
        s4.TextFrame.TextRange.Text = "SPOKE 4: APPLE MOTION\nChuyển Động Morph & Reveal"
        s4.TextFrame.TextRange.Font.Size = 14.5
        s4.TextFrame.TextRange.Font.Color.RGB = hex_to_bgr(ink)

        return shapes

    # 22. ARCH_MULTI_TENANT_SAAS (Kiến Trúc Đa Người Thuê SaaS)
    def render_multi_tenant_saas(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Top Shared Tier (API & Application Gateway)
        top_h = height * 0.35
        app_sh = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, top_h)
        app_sh.Fill.Solid()
        app_sh.Fill.ForeColor.RGB = hex_to_bgr("#0C4A6E")
        app_sh.Line.Visible = msoTrue
        app_sh.Line.ForeColor.RGB = hex_to_bgr(brand)
        app_sh.Line.Weight = 2.0
        shapes.append(app_sh)
        t_app = app_sh.TextFrame.TextRange
        t_app.Text = "TẦNG ỨNG DỤNG DÙNG CHUNG (SHARED APPLICATION TIER)\n\n• Load Balancer • Định Tuyến Tenant Router • 165+ Archetype Engine"
        t_app.Font.Size = 15.0
        t_app.Font.Bold = msoTrue
        t_app.Font.Color.RGB = hex_to_bgr("#FFFFFF")
        t_app.ParagraphFormat.Alignment = ppAlignCenter

        # 3 Isolated Tenant Databases Below
        db_w = (width - 24.0) / 3.0
        db_h = height * 0.55
        db_y = top + top_h + 16.0

        tenants = [
            ("TENANT A (ENTERPRISE 1)", "Cơ sở dữ liệu cô lập riêng biệt\nMã hóa dữ liệu với khóa KMS riêng", "#10B981"),
            ("TENANT B (ENTERPRISE 2)", "Cơ sở dữ liệu cô lập riêng biệt\nĐáp ứng chuẩn tuân thủ HIPAA/GDPR", "#38BDF8"),
            ("TENANT C (DOANH NGHIỆP 3)", "Cơ sở dữ liệu cô lập riêng biệt\nToàn quyền xuất file bảo mật cao", "#F59E0B")
        ]

        for i, (t_name, t_desc, color) in enumerate(tenants):
            dx = left + i * (db_w + 12.0)
            tdb = slide.Shapes.AddShape(msoShapeRoundedRectangle, dx, db_y, db_w, db_h)
            tdb.Fill.Solid()
            tdb.Fill.ForeColor.RGB = hex_to_bgr(surface)
            tdb.Line.Visible = msoTrue
            tdb.Line.ForeColor.RGB = hex_to_bgr(color)
            tdb.Line.Weight = 1.8
            shapes.append(tdb)

            tr = tdb.TextFrame.TextRange
            tr.Text = f"{t_name}\n\n{t_desc}"
            tr.Font.Size = 14.5
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 23. ARCH_RAG_LLM_PIPELINE (Đường Ống RAG Cho Mô Hình Ngôn Ngữ Lớn Có Mũi Tên Vector)
    def render_rag_llm_pipeline(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")
        muted = self._get_token("colors", "muted", "#94A3B8")

        steps = [
            {
                "step": "GIAI ĐOẠN 01",
                "title": "Nạp & Tiền Xử Lý",
                "sub": "DOCUMENT INGESTION",
                "color": "#64748B",
                "specs": [
                    "• Phân rã PDF, DOCX, Web, Markdown",
                    "• Recursive Chunking 512 tokens",
                    "• Trích xuất metadata & ngữ cảnh"
                ],
                "chip": "Nguồn Tri Thức Thô"
            },
            {
                "step": "GIAI ĐOẠN 02",
                "title": "Nhúng & Vector DB",
                "sub": "EMBEDDING & INDEX",
                "color": "#0284C7",
                "specs": [
                    "• Mô hình OpenAI text-embedding-3",
                    "• Lưu trữ Milvus / Qdrant HNSW",
                    "• Đánh chỉ mục Dense Vector đa chiều"
                ],
                "chip": "Không Gian Vector"
            },
            {
                "step": "GIAI ĐOẠN 03",
                "title": "Truy Xuất Ngữ Nghĩa",
                "sub": "HYBRID RETRIEVER",
                "color": "#38BDF8",
                "specs": [
                    "• Tìm kiếm kết hợp BM25 + Vector",
                    "• Cross-Encoder Re-ranking Top-5",
                    "• Lọc lọc ngưỡng tin cậy tương đồng"
                ],
                "chip": "Top-K Ngữ Cảnh Chuẩn"
            },
            {
                "step": "GIAI ĐOẠN 04",
                "title": "Tổng Hợp & Sinh Slide",
                "sub": "LLM GENERATOR",
                "color": "#10B981",
                "specs": [
                    "• Ghép nối Prompt & Context đã lọc",
                    "• LLM kiểm chứng nguồn trích dẫn",
                    "• Điều phối xuất 100% Native PPT"
                ],
                "chip": "Slide Chuẩn Xác 100%"
            }
        ]

        card_gap = 26.0
        card_w = (width - 3 * card_gap) / 4.0
        card_h = min(height - 30.0, 275.0)
        card_y = top + 10.0

        card_coords = []
        for i, item in enumerate(steps):
            s_shapes = []
            cx = left + i * (card_w + card_gap)
            card_coords.append((cx, card_y))
            color = item["color"]

            # Flow arrow incoming from previous stage (atoms bound to current stage)
            if i > 0 and len(card_coords) > 1:
                x_start = card_coords[i - 1][0] + card_w
                y_mid = card_y + card_h / 2.0
                x_end = cx
                conn = add_vector_connector(slide, x_start, y_mid, x_end, y_mid, color="#38BDF8", weight=2.2, arrowhead=True)
                if conn:
                    s_shapes.append(conn)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx, card_y, card_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(surface)
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(color)
            card.Line.Weight = 2.0
            s_shapes.append(card)

            # Top Header Pill
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 8, card_y + 10, card_w - 16, 22)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(color)
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = item["step"]
            pt.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
            pt.Font.Size = 16.0.5
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            s_shapes.append(pill)

            # Title
            tb_title = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 6, card_y + 34, card_w - 12, 34)
            ttf = tb_title.TextFrame
            ttf.WordWrap = msoTrue
            ttf.MarginLeft = 0
            ttf.MarginRight = 0
            ttt = ttf.TextRange
            ttt.Text = item["title"]
            ttt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ttt.Font.Size = 15.0
            ttt.Font.Bold = msoTrue
            ttt.Font.Color.RGB = hex_to_bgr(ink)
            ttt.ParagraphFormat.Alignment = ppAlignCenter
            s_shapes.append(tb_title)

            # Divider line
            div = slide.Shapes.AddShape(msoShapeRectangle, cx + 12, card_y + 70, card_w - 24, 1.5)
            div.Fill.Solid()
            div.Fill.ForeColor.RGB = hex_to_bgr(color)
            div.Line.Visible = msoFalse
            s_shapes.append(div)

            # Specs Bullets
            tb_spec = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx + 8, card_y + 78, card_w - 16, card_h - 118)
            btf = tb_spec.TextFrame
            btf.WordWrap = msoTrue
            btf.MarginLeft = 0
            btf.MarginRight = 0
            btt = btf.TextRange
            btt.Text = "\n\n".join(item["specs"])
            btt.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            btt.Font.Size = 16.0.5
            btt.Font.Color.RGB = hex_to_bgr(muted)
            btt.ParagraphFormat.Alignment = ppAlignLeft
            s_shapes.append(tb_spec)

            # Bottom Status Chip
            chip = slide.Shapes.AddShape(msoShapeRoundedRectangle, cx + 10, card_y + card_h - 30, card_w - 20, 20)
            chip.Fill.Solid()
            chip.Fill.ForeColor.RGB = hex_to_bgr("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            chip.Line.Visible = msoFalse
            ct = chip.TextFrame.TextRange
            ct.Text = item["chip"]
            ct.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
            ct.Font.Size = 16.0.5
            ct.Font.Bold = msoTrue
            ct.Font.Color.RGB = hex_to_bgr(color)
            chip.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            s_shapes.append(chip)

            step_grp = safe_group(slide, s_shapes, f"RAG_Step_{i+1}")
            shapes.append(step_grp)

        return shapes

    # 24. ARCH_EDGE_TO_CLOUD_IOT (Kiến Trúc IoT Từ Biên Đến Đám Mây)
    def render_edge_to_cloud_iot(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        tiers = [
            ("1. THIẾT BỊ BIÊN (EDGE SENSORS)", "Cảm biến IoT, Camera thông minh thu thập dữ liệu thời gian thực", "#0284C7"),
            ("2. CỔNG BIÊN (EDGE GATEWAY)", "Xử lý sơ bộ tại chỗ, lọc nhiễu và nén dữ liệu đường truyền", "#38BDF8"),
            ("3. ĐÁM MÂY (CLOUD INGESTION)", "Hấp thụ hàng triệu thông điệp mỗi giây qua giao thức MQTT", "#10B981"),
            ("4. PHÂN TÍCH THỊ GIÁC (AI ANALYTICS)", "Trực quan hóa biểu đồ và tạo slide báo cáo vận hành tự động", "#F59E0B")
        ]

        card_w = (width - 36.0) / 4.0
        for i, (title, desc, color) in enumerate(tiers):
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
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

    # 25. ARCH_MODULAR_MONOLITH (Kiến Trúc Monolith Module Hóa)
    def render_modular_monolith(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        surface = self._get_token("colors", "surface", "#0B132B")
        brand = self._get_token("colors", "brand", "#0284C7")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        # Outer Bounded Context Box
        outer = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, width, height)
        outer.Fill.Solid()
        outer.Fill.ForeColor.RGB = hex_to_bgr("#082F49")
        outer.Line.Visible = msoTrue
        outer.Line.ForeColor.RGB = hex_to_bgr(brand)
        outer.Line.Weight = 2.0
        shapes.append(outer)

        # 4 Internal Independent Modules Inside
        mod_w = (width - 48.0) / 4.0
        mod_h = height * 0.65
        mod_y = top + height * 0.22

        modules = [
            ("MODULE 1\nComponent Library", "165+ Archetypes", "#38BDF8"),
            ("MODULE 2\nNative COM", "Tables & Charts", "#10B981"),
            ("MODULE 3\nMotion Engine", "Apple Keynote", "#F59E0B"),
            ("MODULE 4\nMACC QA Council", "16 Tác Tử Kiểm Định", "#8B5CF6")
        ]

        for i, (title, desc, color) in enumerate(modules):
            mx = left + 12.0 + i * (mod_w + 8.0)
            m = slide.Shapes.AddShape(msoShapeRoundedRectangle, mx, mod_y, mod_w, mod_h)
            m.Fill.Solid()
            m.Fill.ForeColor.RGB = hex_to_bgr(surface)
            m.Line.Visible = msoTrue
            m.Line.ForeColor.RGB = hex_to_bgr(color)
            m.Line.Weight = 1.5
            shapes.append(m)

            tr = m.TextFrame.TextRange
            tr.Text = f"{title}\n\n{desc}"
            tr.Font.Size = 14.5
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr(ink)
            tr.ParagraphFormat.Alignment = ppAlignCenter

        return shapes

