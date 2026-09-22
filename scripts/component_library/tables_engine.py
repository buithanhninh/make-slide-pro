"""
tables_engine.py
Exhaustive Native PowerPoint Table Engine for Make Slide Pro V8.5.0.
Generates 15 elite management consulting and decision tables using PowerPoint COM (Shapes.AddTable).
All tables are 100% editable Microsoft Office objects.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

# Win32 Constants
msoShapeRoundedRectangle = 5
msoShapeRectangle = 1
msoShapeOval = 9
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


class NativeTablesEngine:
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}

    def _get_token(self, category: str, key: str, fallback: str) -> str:
        return self.tokens.get(category, {}).get(key, fallback)

    def _apply_header_cell(self, cell: Any, text: str, bg_color: str, fg_color: str = "#FFFFFF", align: int = ppAlignCenter) -> None:
        cell.Shape.Fill.Solid()
        cell.Shape.Fill.ForeColor.RGB = hex_to_bgr(bg_color)
        try:
            cell.Shape.TextFrame.VerticalAnchor = 3
            cell.Shape.TextFrame.MarginTop = 6
            cell.Shape.TextFrame.MarginBottom = 6
        except Exception:
            pass
        tr = cell.Shape.TextFrame.TextRange
        tr.Text = str(text).upper()
        tr.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        tr.Font.Size = 11.5
        tr.Font.Bold = msoTrue
        tr.Font.Color.RGB = hex_to_bgr(fg_color)
        tr.ParagraphFormat.Alignment = align

    def _apply_body_cell(self, cell: Any, text: str, bg_color: str, fg_color: str, bold: int = msoFalse, align: int = ppAlignLeft, is_numeric: bool = False, font_size: float = 11.5) -> None:
        cell.Shape.Fill.Solid()
        cell.Shape.Fill.ForeColor.RGB = hex_to_bgr(bg_color)
        try:
            cell.Shape.TextFrame.VerticalAnchor = 3
            cell.Shape.TextFrame.MarginTop = 5
            cell.Shape.TextFrame.MarginBottom = 5
        except Exception:
            pass
        tr = cell.Shape.TextFrame.TextRange
        tr.Text = str(text)
        tr.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift") if is_numeric else self._get_token("fonts", "primary", "Segoe UI")
        tr.Font.Size = font_size
        tr.Font.Bold = bold
        tr.Font.Color.RGB = hex_to_bgr(fg_color)
        tr.ParagraphFormat.Alignment = align

    # 1. TABLE_COMPARISON_PRO (So Sánh Tính Năng Pro)
    def render_comparison_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Tiêu Chí Đánh Giá", "Giải Pháp Tiêu Chuẩn", "Make Slide Pro V8.5 (Đề Xuất)", "Giải Pháp Mở Rộng"])
        rows = table_data.get("rows", [
            ["Khả năng chỉnh sửa trên PPT", "Ảnh tĩnh không sửa được", "100% Native Editable Object", "Chỉnh sửa bán phần"],
            ["Tốc độ xuất file toàn khóa", "12 - 15 phút", "< 25 giây (Thời gian thực)", "3 - 5 phút"],
            ["Kiểm định chất lượng", "Thủ công 1 bước", "16 Tác Tử Hội Đồng MACC", "Quy tắc tĩnh cơ bản"],
            ["Độ phong phú thị giác", "5 bố cục cơ bản", "110+ Archetypes Chuẩn Quốc Tế", "10 - 12 mẫu cố định"]
        ])
        highlight_col_idx = table_data.get("highlight_col", 3)

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        col_w = width / num_cols
        for c in range(1, num_cols + 1):
            tbl.Columns(c).Width = col_w * 1.35 if c == 1 else col_w * 0.88

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h_text in enumerate(headers, start=1):
            is_hl = (c_idx == highlight_col_idx)
            bg = brand if is_hl else ("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            self._apply_header_cell(tbl.Cell(1, c_idx), h_text, bg, "#FFFFFF" if (is_hl or self.theme == "DARK") else "#0F172A", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        for r_idx, row_items in enumerate(rows, start=2):
            is_odd = (r_idx % 2 == 1)
            row_bg = surface if is_odd else (self._get_token("colors", "card_navy", "#0B132B") if self.theme == "DARK" else "#F1F5F9")
            for c_idx, val in enumerate(row_items, start=1):
                is_hl = (c_idx == highlight_col_idx)
                cell_bg = ("#0369A1" if self.theme == "DARK" else "#E0F2FE") if is_hl else row_bg
                fg = (brand if self.theme == "LIGHT" else "#FFFFFF") if is_hl else ink
                bold = msoTrue if (c_idx == 1 or is_hl) else msoFalse
                align = ppAlignCenter if (c_idx > 1 and len(str(val)) <= 18) else ppAlignLeft
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, fg, bold, align)

        return table_shape

    # 2. TABLE_SCORECARD_HEATMAP (Thẻ Điểm Rủi Ro Heatmap)
    def render_scorecard_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Hạng Mục Đánh Giá", "Mục Tiêu", "Hiện Trạng", "Mức Rủi Ro", "Trạng Thái"])
        rows = table_data.get("rows", [
            ["Tiến độ chuyển đổi số", "95% quy trình", "94.2% hoàn thành", "Thấp", "ĐẠT CHUẨN"],
            ["Tích hợp Native Chart Excel", "15 loại biểu đồ", "15/15 loại (100%)", "Rất thấp", "XUẤT SẮC"],
            ["Đào tạo nguồn nhân lực", "100% cán bộ", "65.0% hoàn thành", "Trung bình", "CẦN TĂNG TỐC"],
            ["Kiểm soát tải đồng thời", "500 phiên/giây", "320 phiên/giây", "Cao", "CẢNH BÁO"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        col_w = width / num_cols
        for c in range(1, num_cols + 1):
            tbl.Columns(c).Width = col_w * 1.3 if c == 1 else col_w * 0.925

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        STATUS_COLORS = {
            "đạt chuẩn": ("#064E3B", "#10B981") if self.theme == "DARK" else ("#DCFCE7", "#15803D"),
            "xuất sắc": ("#064E3B", "#10B981") if self.theme == "DARK" else ("#DCFCE7", "#15803D"),
            "cần tăng tốc": ("#78350F", "#F59E0B") if self.theme == "DARK" else ("#FEF3C7", "#B45309"),
            "cảnh báo": ("#7F1D1D", "#EF4444") if self.theme == "DARK" else ("#FEE2E2", "#B91C1C"),
        }

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            is_odd = (r_idx % 2 == 1)
            row_bg = surface if is_odd else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                cell = tbl.Cell(r_idx, c_idx)
                val_lower = str(val).lower().strip()
                if c_idx == num_cols and val_lower in STATUS_COLORS:
                    bg_c, fg_c = STATUS_COLORS[val_lower]
                    self._apply_body_cell(cell, val, bg_c, fg_c, msoTrue, ppAlignCenter)
                else:
                    bold = msoTrue if c_idx == 1 else msoFalse
                    align = ppAlignCenter if c_idx > 1 else ppAlignLeft
                    self._apply_body_cell(cell, val, row_bg, ink, bold, align)

        return table_shape

    # 3. TABLE_FINANCIAL_PL (Báo Cáo Tài Chính P&L)
    def render_financial_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Khoản Mục Tài Chính (Tỷ VNĐ)", "Năm 2022", "Năm 2023", "Năm 2024 (KH)", "Tăng Trưởng YoY"])
        rows = table_data.get("rows", [
            ["Doanh Thu Thuần", "1,240.5", "1,580.2", "2,050.0", "+29.7%"],
            ["  - Giá vốn hàng bán (COGS)", "(720.0)", "(890.5)", "(1,120.0)", "+25.8%"],
            ["Lợi Nhuận Gộp", "520.5", "689.7", "930.0", "+34.8%"],
            ["  - Chi phí bán hàng & quản lý", "(210.0)", "(260.4)", "(320.0)", "+22.9%"],
            ["Lợi Nhuận Trước Thuế (EBT)", "310.5", "429.3", "610.0", "+42.1%"],
            ["Lợi Nhuận Sau Thuế (Ròng)", "248.4", "343.4", "488.0", "+42.1%"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.38
        rem_w = (width * 0.62) / (num_cols - 1)
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = rem_w

        for c_idx, h in enumerate(headers, start=1):
            bg = "#0F172A" if self.theme == "DARK" else "#334155"
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF", ppAlignRight if c_idx > 1 else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            is_total = "lợi nhuận" in row_items[0].lower() or "tổng" in row_items[0].lower()
            cell_bg = ("#1E293B" if self.theme == "DARK" else "#E2E8F0") if is_total else (surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#FFFFFF"))

            for c_idx, val in enumerate(row_items, start=1):
                fg = ink
                if "+" in str(val):
                    fg = "#10B981" if self.theme == "DARK" else "#059669"
                elif "(" in str(val):
                    fg = "#EF4444" if self.theme == "DARK" else "#DC2626"
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, fg, msoTrue if is_total else msoFalse, ppAlignRight if c_idx > 1 else ppAlignLeft, is_numeric=(c_idx > 1))

        return table_shape

    # 4. TABLE_RACI_GOVERNANCE (Ma Trận Phân Quyền RACI)
    def render_raci_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Giai Đoạn / Nhiệm Vụ", "Hội Đồng Quản Trị", "CEO / Ban Giám Đốc", "Trưởng Nhóm Kỹ Thuật", "Đội Vận Hành", "Khách Hàng"])
        rows = table_data.get("rows", [
            ["Phê duyệt Chiến lược & Ngân sách", "A", "R", "C", "I", "I"],
            ["Thiết kế Kiến trúc Hệ thống", "I", "A", "R", "C", "I"],
            ["Kiểm thử Nghiệm thu & QA", "I", "I", "R", "A", "C"],
            ["Bàn giao & Đưa vào Vận hành", "I", "A", "C", "R", "A"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.35
        rem_w = (width * 0.65) / (num_cols - 1)
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = rem_w

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        RACI_COLORS = {
            "R": ("#0369A1", "#FFFFFF") if self.theme == "DARK" else ("#BAE6FD", "#0369A1"),
            "A": ("#065F46", "#FFFFFF") if self.theme == "DARK" else ("#A7F3D0", "#065F46"),
            "C": ("#92400E", "#FFFFFF") if self.theme == "DARK" else ("#FDE68A", "#92400E"),
            "I": ("#334155", "#CBD5E1") if self.theme == "DARK" else ("#E2E8F0", "#475569"),
        }

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            cell_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                v_clean = str(val).strip().upper()
                if c_idx > 1 and v_clean in RACI_COLORS:
                    bg_c, fg_c = RACI_COLORS[v_clean]
                    self._apply_body_cell(tbl.Cell(r_idx, c_idx), v_clean, bg_c, fg_c, msoTrue, ppAlignCenter)
                else:
                    self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, ink, msoTrue if c_idx == 1 else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 5. TABLE_METRIC_MATRIX (Tổng Hợp Chỉ Số Đa Chiều)
    def render_metric_matrix_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Khu Vực Kinh Tế", "Quy Mô Dân Số (Tr)", "Tỷ Lệ Đô Thị Hóa", "Thu Nhập Bình Quân", "Chỉ Số HDI"])
        rows = table_data.get("rows", [
            ["Đồng Bằng Sông Hồng", "23.4", "45.2%", "8.2 Tr/Tháng", "0.768"],
            ["Đông Nam Bộ", "18.8", "67.8%", "10.5 Tr/Tháng", "0.802"],
            ["Đồng Bằng Sông Cửu Long", "17.5", "25.6%", "5.9 Tr/Tháng", "0.714"],
            ["Bắc Trung Bộ & Duyên Hải Miền Trung", "20.6", "31.2%", "5.6 Tr/Tháng", "0.722"],
            ["Tây Nguyên", "6.1", "29.4%", "5.2 Tr/Tháng", "0.701"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        col_w = width / num_cols
        for c in range(1, num_cols + 1):
            tbl.Columns(c).Width = col_w * 1.25 if c == 1 else col_w * 0.9375

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            is_odd = (r_idx % 2 == 1)
            cell_bg = surface if is_odd else ("#111C3A" if self.theme == "DARK" else "#F1F5F9")
            for c_idx, val in enumerate(row_items, start=1):
                bold = msoTrue if c_idx == 1 else msoFalse
                align = ppAlignCenter if c_idx > 1 else ppAlignLeft
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, ink, bold, align, is_numeric=(c_idx > 1))

        return table_shape

    # 6. TABLE_COMPETITOR_BENCHMARK (So Sánh Đối Thủ Cạnh Tranh)
    def render_competitor_benchmark(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Hạng Mục Năng Lực", "Make Slide Pro", "Đối Thủ Toàn Cầu A", "Đối Thủ Bán Tự Động B", "Phần Mềm Truyền Thống C"])
        rows = table_data.get("rows", [
            ["Tự Động Xuất Native PPT", "★★★★★ (Tuyệt đối)", "★★☆☆☆ (Xuất PDF)", "★★★☆☆ (Xuất ảnh)", "★☆☆☆☆ (Thủ công)"],
            ["Tích Hợp 16 Tác Tử QA", "✓ Có sẵn tự phục hồi", "✕ Không hỗ trợ", "✕ Không hỗ trợ", "✕ Không hỗ trợ"],
            ["Kho 110+ Archetypes", "✓ Đa dạng phong phú", "✓ Hạn chế 15 mẫu", "✓ 20 mẫu tĩnh", "✕ Mẫu trống"],
            ["Khả năng sửa số liệu Excel", "✓ 100% Native Object", "✕ Khóa ảnh tĩnh", "✕ Khóa vector", "✓ Sửa thủ công"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.28
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = (width * 0.72) / (num_cols - 1)

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            is_our = (c_idx == 2)
            bg = brand if is_our else ("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF" if (is_our or self.theme == "DARK") else "#0F172A", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                is_our = (c_idx == 2)
                cell_bg = ("#0369A1" if self.theme == "DARK" else "#E0F2FE") if is_our else row_bg
                fg = ("#F59E0B" if "★" in str(val) else ink) if not is_our else ("#FFFFFF" if self.theme == "DARK" else brand)
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, fg, msoTrue if is_our else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 7. TABLE_CAPABILITY_GAP (Ma Trận Khoảng Trống Năng Lực)
    def render_capability_gap(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Năng Lực Cốt Lõi", "Mức Độ Hiện Tại", "Mục Tiêu Năm 2025", "Độ Lệch (Gap)", "Mức Ưu Tiên"])
        rows = table_data.get("rows", [
            ["Tự động hóa báo cáo AI", "Mức 2 (Bán tự động)", "Mức 5 (Autonomous)", "-3 Bậc", "CẤP THIẾT"],
            ["Kiến trúc dữ liệu Lakehouse", "Mức 3 (Đã chuẩn hóa)", "Mức 4 (Thời gian thực)", "-1 Bậc", "TRUNG BÌNH"],
            ["An ninh mạng Zero-Trust", "Mức 4 (Tiên tiến)", "Mức 5 (Tuyệt đối)", "-1 Bậc", "CAO"],
            ["Văn hóa dữ liệu nhân sự", "Mức 2 (Thủ công)", "Mức 4 (Tự phục vụ)", "-2 Bậc", "CAO"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        col_w = width / num_cols
        for c in range(1, num_cols + 1):
            tbl.Columns(c).Width = col_w * 1.3 if c == 1 else col_w * 0.925

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        PRIO_COLORS = {
            "cấp thiết": ("#7F1D1D", "#EF4444") if self.theme == "DARK" else ("#FEE2E2", "#DC2626"),
            "cao": ("#78350F", "#F59E0B") if self.theme == "DARK" else ("#FEF3C7", "#D97706"),
            "trung bình": ("#064E3B", "#10B981") if self.theme == "DARK" else ("#DCFCE7", "#16A34A")
        }

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                val_clean = str(val).lower().strip()
                if c_idx == num_cols and val_clean in PRIO_COLORS:
                    bg_c, fg_c = PRIO_COLORS[val_clean]
                    self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, bg_c, fg_c, msoTrue, ppAlignCenter)
                else:
                    fg = ("#EF4444" if "-" in str(val) and c_idx == 4 else ink)
                    self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx == 1 else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 8. TABLE_PRICING_TIERS (Bảng Báo Giá Gói Dịch Vụ)
    def render_pricing_tiers(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Hạng Mục Đánh Giá", "Cấp Cơ Sở", "Cấp Chuyên Sâu", "Cấp Toàn Diện"])
        rows = table_data.get("rows", [
            ["Phạm Vi Hoạt Động", "Tại hộ gia đình và trạm y tế", "Trung tâm y tế huyện", "Bệnh viện chuyên khoa tỉnh"],
            ["Tần Suất Thực Hiện", "Định kỳ hàng tháng", "Định kỳ hàng quý", "Thường xuyên liên tục"],
            ["Quy Chuẩn Chuyên Môn", "Quy trình cơ bản", "Quy trình nâng cao", "Tiêu chuẩn quốc gia"],
            ["Nguồn Lực Đảm Bảo", "Cán bộ chuyên trách", "Bác sĩ chuyên khoa", "Hội đồng chuyên môn"],
            ["Hiệu Quả Dự Kiến", "Bao phủ 85% đối tượng", "Đạt chuẩn 95% mục tiêu", "100% đối tượng đích"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.31
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = (width * 0.69) / (num_cols - 1)

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            is_pro = (c_idx == 3)
            bg = brand if is_pro else ("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF" if (is_pro or self.theme == "DARK") else "#0F172A", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                is_pro = (c_idx == 3)
                cell_bg = ("#0369A1" if self.theme == "DARK" else "#E0F2FE") if is_pro else row_bg
                fg = ("#FFFFFF" if self.theme == "DARK" else brand) if is_pro else ink
                bold = msoTrue if (r_idx == 2 or is_pro or c_idx == 1) else msoFalse
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, fg, bold, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 9. TABLE_RISK_REGISTER (Sổ Đăng Ký Rủi Ro Dự Án)
    def render_risk_register(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Mã & Tên Rủi Ro", "Xác Suất", "Tác Động", "Biện Pháp Giảm Thiểu", "Người Phụ Trách"])
        rows = table_data.get("rows", [
            ["R01: Gián đoạn kết nối thông tin", "Thấp (15%)", "Nghiêm trọng", "Dự phòng kết nối song song và báo cáo trực tiếp", "Cán bộ phụ trách"],
            ["R02: Sai lệch dữ liệu thống kê", "Trung bình (25%)", "Trung bình", "Quy trình đối soát chéo và phúc tra định kỳ", "Hội đồng chuyên môn"],
            ["R03: Quá tải cơ sở cung ứng dịch vụ", "Thấp (20%)", "Cao", "Điều phối nhân lực tăng cường từ tuyến trên", "Lãnh đạo đơn vị"],
            ["R04: Vi phạm bảo mật thông tin cá nhân", "Rất thấp (5%)", "Nghiêm trọng", "Tuân thủ nghiêm ngặt quy định bảo mật hồ sơ", "Cán bộ quản lý"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.28
        tbl.Columns(2).Width = width * 0.14
        tbl.Columns(3).Width = width * 0.14
        tbl.Columns(4).Width = width * 0.30
        tbl.Columns(5).Width = width * 0.14

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {2, 3, 5} else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                align = ppAlignCenter if c_idx in {2, 3, 5} else ppAlignLeft
                bold = msoTrue if c_idx == 1 else msoFalse
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, ink, bold, align)

        return table_shape

    # 10. TABLE_AUDIT_COMPLIANCE (Kiểm Toán Tuân Thủ Chuẩn Mực)
    def render_audit_compliance(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Tiêu Chuẩn & Quy Định", "Phạm Vi Áp Dụng", "Kết Quả Kiểm Toán", "Kế Hoạch Khắc Phục", "Thời Hạn"])
        rows = table_data.get("rows", [
            ["ISO/IEC 27001:2022", "Toàn bộ hạ tầng đám mây", "TUÂN THỦ 100%", "Duy trì giám sát định kỳ", "Hàng Quý"],
            ["Nghị Định 13/2023/NĐ-CP", "Bảo vệ dữ liệu cá nhân", "TUÂN THỦ 100%", "Đã ban hành quy chế nội bộ", "Hoàn thành"],
            ["SOC 2 Type II", "Quy trình vận hành SaaS", "ĐANG ĐÁNH GIÁ", "Bổ sung bằng chứng truy vết", "Tháng 11/2024"],
            ["GDPR / Quốc Tế", "Người dùng xuyên biên giới", "TUÂN THỦ", "Cập nhật chính sách Cookie", "Hoàn thành"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.26
        tbl.Columns(2).Width = width * 0.24
        tbl.Columns(3).Width = width * 0.18
        tbl.Columns(4).Width = width * 0.20
        tbl.Columns(5).Width = width * 0.12

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {3, 5} else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                align = ppAlignCenter if c_idx in {3, 5} else ppAlignLeft
                bold = msoTrue if (c_idx == 1 or c_idx == 3) else msoFalse
                fg = ("#10B981" if "TUÂN THỦ" in str(val) else ("#F59E0B" if "ĐANG" in str(val) else ink)) if c_idx == 3 else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, bold, align)

        return table_shape

    # 11. TABLE_PROS_CONS (So Sánh Ưu - Nhược Điểm)
    def render_pros_cons(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Lĩnh Vực Đánh Giá", "Ưu Điểm Vượt Trội (+)", "Nhược Điểm & Thách Thức (-)"])
        rows = table_data.get("rows", [
            ["Chi Phí & Ngân Sách", "Tiết kiệm 45% chi phí thiết kế và sản xuất slide", "Cần vốn đầu tư ban đầu cho hạ tầng AI chuyên sâu"],
            ["Thời Gian & Năng Suất", "Rút ngắn thời gian từ 3 ngày xuống dưới 30 giây", "Đòi hỏi nhân sự làm quen với quy trình prompt chuẩn"],
            ["Chất Lượng Thẩm Mỹ", "Chuẩn hóa theo 110+ Archetypes toàn cầu", "Cần duyệt lại các thuật ngữ mang tính địa phương hẹp"],
            ["Khả Năng Tùy Biến", "100% Native Object sửa trực tiếp trong PowerPoint", "Yêu cầu máy tính cài đặt bộ Microsoft Office tương thích"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.24
        tbl.Columns(2).Width = width * 0.38
        tbl.Columns(3).Width = width * 0.38

        self._apply_header_cell(tbl.Cell(1, 1), headers[0], "#1E293B" if self.theme == "DARK" else "#334155", "#FFFFFF", ppAlignLeft)
        self._apply_header_cell(tbl.Cell(1, 2), headers[1], "#065F46" if self.theme == "DARK" else "#059669", "#FFFFFF", ppAlignLeft)
        self._apply_header_cell(tbl.Cell(1, 3), headers[2], "#7F1D1D" if self.theme == "DARK" else "#DC2626", "#FFFFFF", ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                fg = ink
                if c_idx == 2:
                    fg = "#34D399" if self.theme == "DARK" else "#047857"
                elif c_idx == 3:
                    fg = "#F87171" if self.theme == "DARK" else "#B91C1C"
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx == 1 else msoFalse, ppAlignLeft)

        return table_shape

    # 12. TABLE_ROADMAP_SCHEDULE (Bảng Lịch Trình Phát Hành)
    def render_roadmap_schedule(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Giai Đoạn (Sprint)", "Tính Năng Bàn Giao", "Ngày Hoàn Thành", "Độ Sẵn Sàng", "Trạng Thái"])
        rows = table_data.get("rows", [
            ["Sprint 01: Nền Tảng", "Kho 110+ Archetypes & Native COM Dispatcher", "15/09/2024", "100% Production", "HOÀN TẤT"],
            ["Sprint 02: Tự Động Hóa", "Semantic Pattern Recognizer & Tự phục hồi MACC", "25/09/2024", "100% Production", "HOÀN TẤT"],
            ["Sprint 03: Web Studio", "Giao diện Web SaaS kéo thả thời gian thực", "10/10/2024", "90% Staging", "ĐANG THỬ NGHIỆM"],
            ["Sprint 04: Cloud Hub", "Liên thông hệ thống báo cáo dữ liệu chính phủ", "15/11/2024", "50% Planning", "CHUẨN BỊ"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        col_w = width / num_cols
        for c in range(1, num_cols + 1):
            tbl.Columns(c).Width = col_w * 1.2 if c == 2 else col_w * 0.95

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {3, 4, 5} else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                bold = msoTrue if (c_idx == 1 or c_idx == 5) else msoFalse
                align = ppAlignCenter if c_idx in {3, 4, 5} else ppAlignLeft
                fg = ink
                if c_idx == 5:
                    fg = "#10B981" if "HOÀN TẤT" in str(val) else ("#F59E0B" if "ĐANG" in str(val) else "#94A3B8")
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, bold, align)

        return table_shape

    # 13. TABLE_SALES_TERRITORY (Bảng Chỉ Tiêu Kinh Doanh Khu Vực)
    def render_sales_territory(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Vùng Kinh Tế", "Doanh Thu Thực Hiện", "Chỉ Tiêu Năm 2024", "Tỷ Lệ Đạt (%)", "Xếp Hạng"])
        rows = table_data.get("rows", [
            ["Đông Nam Bộ", "450.5 Tỷ VNĐ", "420.0 Tỷ VNĐ", "107.3%", "Hạng 1 (Dẫn Đầu)"],
            ["Đồng Bằng Sông Hồng", "380.2 Tỷ VNĐ", "370.0 Tỷ VNĐ", "102.8%", "Hạng 2 (Xuất Sắc)"],
            ["Đồng Bằng Sông Cửu Long", "195.0 Tỷ VNĐ", "210.0 Tỷ VNĐ", "92.9%", "Hạng 3 (Khá)"],
            ["Bắc Trung Bộ & DHMT", "180.4 Tỷ VNĐ", "200.0 Tỷ VNĐ", "90.2%", "Hạng 4 (Cần Nỗ Lực)"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        col_w = width / num_cols
        for c in range(1, num_cols + 1):
            tbl.Columns(c).Width = col_w * 1.25 if c == 1 else col_w * 0.9375

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {4, 5} else (ppAlignRight if c_idx in {2, 3} else ppAlignLeft))

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                align = ppAlignCenter if c_idx in {4, 5} else (ppAlignRight if c_idx in {2, 3} else ppAlignLeft)
                bold = msoTrue if (c_idx == 1 or c_idx == 5) else msoFalse
                fg = ("#10B981" if ">=" in str(val) or "10" in str(val) and c_idx == 4 else ink)
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, bold, align, is_numeric=(c_idx in {2, 3, 4}))

        return table_shape

    # 14. TABLE_WEIGHTED_DECISION (Ma Trận Quyết Định Đa Tiêu Chí)
    def render_weighted_decision(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Tiêu Chí Chiến Lược", "Trọng Số (%)", "Phương Án A (Cloud)", "Phương Án B (On-Prem)", "Phương Án C (Hybrid)"])
        rows = table_data.get("rows", [
            ["Chi phí đầu tư ban đầu (CAPEX)", "25%", "8.5 / 10", "4.0 / 10", "6.5 / 10"],
            ["Khả năng mở rộng & co giãn", "30%", "9.5 / 10", "5.0 / 10", "8.5 / 10"],
            ["Bảo mật & Chủ quyền dữ liệu", "25%", "7.5 / 10", "9.5 / 10", "9.0 / 10"],
            ["Tốc độ triển khai ra thị trường", "20%", "9.0 / 10", "4.5 / 10", "7.5 / 10"],
            ["ĐIỂM TỔNG KẾT CÓ TRỌNG SỐ", "100%", "8.65 / 10 (Hạng 1)", "5.65 / 10 (Hạng 3)", "7.95 / 10 (Hạng 2)"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.32
        tbl.Columns(2).Width = width * 0.14
        for c in range(3, num_cols + 1):
            tbl.Columns(c).Width = (width * 0.54) / (num_cols - 2)

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            is_best = (c_idx == 3)
            bg = brand if is_best else ("#1E293B" if self.theme == "DARK" else "#E2E8F0")
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF" if (is_best or self.theme == "DARK") else "#0F172A", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            is_total = (r_idx == num_rows)
            cell_bg = ("#1E293B" if self.theme == "DARK" else "#E2E8F0") if is_total else (surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC"))
            for c_idx, val in enumerate(row_items, start=1):
                is_best = (c_idx == 3)
                fg = ("#10B981" if is_best and is_total else (brand if is_best else ink))
                bold = msoTrue if (is_total or is_best or c_idx == 1) else msoFalse
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, cell_bg, fg, bold, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 15. TABLE_EXECUTIVE_SUMMARY (Bảng Điều Hành Cấp Cao)
    def render_executive_summary_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Lĩnh Vực Điều Hành", "Chỉ Số Cốt Lõi", "Tiến Độ Năm 2024", "Đánh Giá Của Ban Điều Hành"])
        rows = table_data.get("rows", [
            ["1. Tăng Trưởng Quy Mô Dân Số", "100.3 Triệu Người", "Đạt 100.2% Kế Hoạch", "Duy trì vị thế thị trường lao động dồi dào"],
            ["2. Tỷ Suất Sinh Toàn Quốc", "1.96 Con / Phụ Nữ", "Cảnh báo mức thấp", "Cần chính sách hỗ trợ sinh đẻ tại các vùng kinh tế trọng điểm"],
            ["3. Tốc Độ Già Hóa Dân Số", "13.4% Dân Số > 60 Tuổi", "Đang già hóa nhanh", "Khẩn trương mở rộng quỹ hưu trí và y tế dưỡng lão"],
            ["4. Đô Thị Hóa & Di Cư", "42.5% Tỷ Lệ Đô Thị", "Tăng 1.8% YoY", "Tập trung đầu tư hạ tầng giao thông và nhà ở xã hội"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.28
        tbl.Columns(2).Width = width * 0.20
        tbl.Columns(3).Width = width * 0.20
        tbl.Columns(4).Width = width * 0.32

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {2, 3} else ppAlignLeft)

        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                bold = msoTrue if c_idx == 1 else msoFalse
                align = ppAlignCenter if c_idx in {2, 3} else ppAlignLeft
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, ink, bold, align)

        return table_shape

    # 16. TABLE_PRICING_FEATURE_MATRIX (Ma Trận Tính Năng 4 Gói)
    def render_pricing_feature_matrix(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Tiêu Chí Chuyên Môn", "Giai Đoạn 1", "Giai Đoạn 2", "Giai Đoạn 3", "Giai Đoạn 4"])
        rows = table_data.get("rows", [
            ["Tiếp Cận Đối Tượng", "Diện hẹp (Thí điểm)", "Mở rộng 50%", "Bao phủ 85%", "Toàn diện 100%"],
            ["Đội Ngũ Nhân Sự", "Tập huấn cơ bản", "Đào tạo thực địa", "Chứng chỉ chuyên sâu", "Chuyên gia đầu ngành"],
            ["Quy Trình Kỹ Thuật", "Khảo sát ban đầu", "Thực hiện định kỳ", "Giám sát độc lập", "Tiêu chuẩn hóa quốc gia"],
            ["Kiểm Định Chất Lượng", "Tự đánh giá", "Đánh giá chéo", "Kiểm định định kỳ", "Hội đồng nghiệm thu"],
            ["Mức Độ Đạt Chuẩn", "Đạt yêu cầu", "Khá", "Tốt", "Xuất sắc"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.32
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = (width * 0.68) / (num_cols - 1)

        brand = self._get_token("colors", "brand", "#0284C7")
        accent = self._get_token("colors", "accent", "#38BDF8")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            bg = accent if c_idx == 4 else brand
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF", ppAlignLeft if c_idx == 1 else ppAlignCenter)

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                fg = "#10B981" if "✓" in str(val) else ("#EF4444" if "✕" in str(val) else ink)
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx == 1 else msoFalse, ppAlignLeft if c_idx == 1 else ppAlignCenter)

        return table_shape

    # 17. TABLE_MILESTONE_DELIVERABLES (Bảng Phân Công Bàn Giao Mốc Dự Án)
    def render_milestone_deliverables(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Cột Mốc / Giai Đoạn", "Nội Dung Bàn Giao", "Đơn Vị Chủ Trì", "Tiến Độ", "Trạng Thái"])
        rows = table_data.get("rows", [
            ["Giai Đoạn 1: Khảo Sát Ban Đầu", "Báo cáo điều tra thực địa cơ sở", "Ban Quản Lý", "Tháng 01", "HOÀN TẤT 100%"],
            ["Giai Đoạn 2: Xây Dựng Kế Hoạch", "Kế hoạch hành động và phân bổ ngân sách", "Tổ Chuyên Môn", "Tháng 03", "HOÀN TẤT 100%"],
            ["Giai Đoạn 3: Triển Khai Thực Địa", "Tập huấn và cung ứng dịch vụ tại cộng đồng", "Đội Ngũ Thực Hiện", "Tháng 06", "ĐANG THỰC HIỆN"],
            ["Giai Đoạn 4: Giám Sát & Đánh Giá", "Báo cáo giám sát định kỳ độc lập", "Hội Đồng Thẩm Định", "Tháng 09", "CHUẨN BỊ"],
            ["Giai Đoạn 5: Tổng Kết & Nhân Rộng", "Hội nghị tổng kết và đề xuất giải pháp", "Ban Chỉ Đạo", "Tháng 12", "THEO KẾ HOẠCH"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.25
        tbl.Columns(2).Width = width * 0.30
        tbl.Columns(3).Width = width * 0.18
        tbl.Columns(4).Width = width * 0.12
        tbl.Columns(5).Width = width * 0.15

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {3, 4, 5} else ppAlignLeft)

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                status_color = "#10B981" if "HOÀN TẤT" in str(val) else ("#F59E0B" if "ĐANG" in str(val) else ink)
                fg = status_color if c_idx == 5 else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx in {1, 5} else msoFalse, ppAlignCenter if c_idx in {3, 4, 5} else ppAlignLeft)

        return table_shape

    # 18. TABLE_SWOT_DETAILED (Bảng Phân Tích SWOT Chi Tiết)
    def render_swot_detailed_table(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Góc Nhìn Chiến Lược", "Nội Dung Phân Tích Thực Tế", "Tác Động Đến Tổ Chức", "Hành Động Đề Xuất"])
        rows = table_data.get("rows", [
            ["Điểm Mạnh (Strengths)", "Kho 165+ Archetypes, 100% Native Tables/Charts nhúng Excel", "Lợi thế dẫn đầu công nghệ vượt trội", "Truyền thông quảng bá tính năng độc quyền"],
            ["Điểm Yếu (Weaknesses)", "Cần tối ưu thời gian render cho các bài giảng trên 100 slides", "Ảnh hưởng trải nghiệm người dùng lớn", "Nâng cấp cơ chế batch render song song"],
            ["Cơ Hội (Opportunities)", "Nhu cầu chuẩn hóa báo cáo chuyên nghiệp của các tập đoàn", "Thị trường B2B tiềm năng tăng trưởng 35%", "Thiết kế gói Enterprise dành riêng cho DN"],
            ["Thách Thức (Threats)", "Sự xuất hiện của các công cụ sinh slide AI giá rẻ", "Cạnh tranh về giá trên thị trường", "Tập trung vào chất lượng Native & Motion Apple"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.22
        tbl.Columns(2).Width = width * 0.38
        tbl.Columns(3).Width = width * 0.20
        tbl.Columns(4).Width = width * 0.20

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignLeft)

        swot_colors = ["#10B981", "#EF4444", "#3B82F6", "#F59E0B"]
        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            corner_color = swot_colors[(r_idx - 2) % len(swot_colors)]
            for c_idx, val in enumerate(row_items, start=1):
                fg = corner_color if c_idx == 1 else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx == 1 else msoFalse, ppAlignLeft)

        return table_shape

    # 19. TABLE_RISK_HEATMAP_5X5 (Ma Trận Nhiệt Rủi Ro 5x5)
    def render_risk_heatmap_5x5(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Khả Năng / Tác Động", "1 - Rất Thấp", "2 - Thấp", "3 - Trung Bình", "4 - Cao", "5 - Nghiêm Trọng"])
        rows = table_data.get("rows", [
            ["5 - Chắc Chắn Xảy Ra", "Trung Bình (5)", "Cao (10)", "Nghiêm Trọng (15)", "Nguy Hiểm (20)", "Cực Kỳ Nguy Hiểm (25)"],
            ["4 - Khả Năng Cao", "Thấp (4)", "Trung Bình (8)", "Cao (12)", "Nghiêm Trọng (16)", "Nguy Hiểm (20)"],
            ["3 - Có Thể Xảy Ra", "Thấp (3)", "Thấp (6)", "Trung Bình (9)", "Cao (12)", "Nghiêm Trọng (15)"],
            ["2 - Ít Khả Năng", "Rất Thấp (2)", "Thấp (4)", "Thấp (6)", "Trung Bình (8)", "Cao (10)"],
            ["1 - Hiếm Khi", "Rất Thấp (1)", "Rất Thấp (2)", "Thấp (3)", "Thấp (4)", "Trung Bình (5)"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.25
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = (width * 0.75) / (num_cols - 1)

        brand = self._get_token("colors", "brand", "#0284C7")
        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        # Risk level heatmap colors
        def get_heat_color(val_str: str) -> str:
            if "Nguy Hiểm" in val_str or "25" in val_str or "20" in val_str:
                return "#7F1D1D"  # Deep Red
            elif "Nghiêm Trọng" in val_str or "16" in val_str or "15" in val_str:
                return "#991B1B"  # Dark Red
            elif "Cao" in val_str or "12" in val_str or "10" in val_str:
                return "#B45309"  # Amber Orange
            elif "Trung Bình" in val_str or "8" in val_str or "9" in val_str:
                return "#854D0E"  # Yellow Amber
            else:
                return "#064E3B"  # Deep Emerald Green

        surface = self._get_token("colors", "surface", "#0B132B")
        for r_idx, row_items in enumerate(rows, start=2):
            for c_idx, val in enumerate(row_items, start=1):
                bg = surface if c_idx == 1 else get_heat_color(str(val))
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, bg, "#FFFFFF", msoTrue if c_idx == 1 else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft, font_size=10.5)

        return table_shape

    # 20. TABLE_BUDGET_ALLOCATION (Bảng Phân Bổ Ngân Sách Capex/Opex)
    def render_budget_allocation(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Khoản Mục Ngân Sách", "Loại Chi Phí", "Dự Toán Kế Hoạch", "Thực Tế Đã Chi", "Đánh Giá"])
        rows = table_data.get("rows", [
            ["1. Đào Tạo & Tập Huấn Chuyên Môn", "Chi thường xuyên", "150.000.000 đ", "145.000.000 đ", "Đạt chuẩn"],
            ["2. Truyền Thông & Giáo Dục Cộng Đồng", "Chi nghiệp vụ", "200.000.000 đ", "198.500.000 đ", "Đạt chuẩn"],
            ["3. Trang Thiết Bị & Vật Tư Y Tế", "Đầu tư cơ sở", "350.000.000 đ", "342.000.000 đ", "Tiết kiệm 2.3%"],
            ["4. Giám Sát Đánh Giá & Hỗ Trợ Kỹ Thuật", "Chi thường xuyên", "100.000.000 đ", "96.500.000 đ", "Đạt chuẩn"],
            ["TỔNG CỘNG KINH PHÍ HOẠT ĐỘNG", "TOÀN DỰ ÁN", "800.000.000 đ", "782.000.000 đ", "Trong hạn mức"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.35
        tbl.Columns(2).Width = width * 0.15
        tbl.Columns(3).Width = width * 0.16
        tbl.Columns(4).Width = width * 0.16
        tbl.Columns(5).Width = width * 0.18

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignRight if c_idx in {3, 4, 5} else (ppAlignCenter if c_idx == 2 else ppAlignLeft))

        for r_idx, row_items in enumerate(rows, start=2):
            is_total = (r_idx == num_rows)
            row_bg = "#1E293B" if is_total else (surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC"))
            for c_idx, val in enumerate(row_items, start=1):
                fg = "#10B981" if "-" in str(val) and "%" in str(val) else ("#EF4444" if "+" in str(val) and "%" in str(val) else ink)
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if is_total or c_idx == 1 else msoFalse, ppAlignRight if c_idx in {3, 4, 5} else (ppAlignCenter if c_idx == 2 else ppAlignLeft), is_numeric=(c_idx in {3, 4}))

        return table_shape

    # 21. TABLE_VENDOR_EVALUATION (Bảng Chấm Điểm Nhà Cung Cấp Đa Tiêu Chí)
    def render_vendor_evaluation(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Tiêu Chí Thẩm Định", "Trọng Số (%)", "Nhà Thầu Alpha", "Nhà Thầu Beta (Make Slide)", "Nhà Thầu Gamma"])
        rows = table_data.get("rows", [
            ["Năng Lực Kỹ Thuật & Kiến Trúc", "30%", "78 / 100", "98 / 100", "82 / 100"],
            ["Bảo Mật & Tuân Thủ (ISO/SOC2)", "25%", "85 / 100", "95 / 100", "88 / 100"],
            ["Tốc Độ Triển Khai & Hiệu Năng", "20%", "70 / 100", "96 / 100", "75 / 100"],
            ["Chi Phí Sở Hữu Toàn Vòng Đời", "15%", "88 / 100", "90 / 100", "80 / 100"],
            ["Chất Lượng Hỗ Trợ Kỹ Thuật SLA", "10%", "75 / 100", "94 / 100", "82 / 100"],
            ["ĐIỂM TỔNG HỢP CÓ TRỌNG SỐ", "100%", "79.1 / 100", "95.5 / 100 (TRÚNG THẦU)", "81.9 / 100"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.32
        tbl.Columns(2).Width = width * 0.14
        tbl.Columns(3).Width = width * 0.18
        tbl.Columns(4).Width = width * 0.20
        tbl.Columns(5).Width = width * 0.16

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            bg = "#0369A1" if c_idx == 4 else brand
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF", ppAlignLeft if c_idx == 1 else ppAlignCenter)

        for r_idx, row_items in enumerate(rows, start=2):
            is_total = (r_idx == num_rows)
            row_bg = "#1E293B" if is_total else (surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC"))
            for c_idx, val in enumerate(row_items, start=1):
                col_bg = "#0C4A6E" if (c_idx == 4 and not is_total) else ("#0284C7" if (c_idx == 4 and is_total) else row_bg)
                fg = "#38BDF8" if (c_idx == 4 and not is_total) else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, col_bg, fg, msoTrue if is_total or c_idx in {1, 4} else msoFalse, ppAlignLeft if c_idx == 1 else ppAlignCenter)

        return table_shape

    # 22. TABLE_OKRS_TRACKER (Bảng Theo Dõi Mục Tiêu & Kết Quả Then Chốt)
    def render_okrs_tracker(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Mục Tiêu Trọng Tâm", "Chỉ Số Đo Lường Then Chốt", "Chỉ Tiêu Đề Ra", "Kết Quả Đạt Được", "Đánh Giá"])
        rows = table_data.get("rows", [
            ["Mục Tiêu 1: Tăng Cường Bao Phủ Dịch Vụ", "Tỷ lệ tiếp cận tư vấn tiền hôn nhân", "80% đối tượng", "82% đạt chuẩn", "VƯỢT CHỈ TIÊU"],
            ["Mục Tiêu 1: Tăng Cường Bao Phủ Dịch Vụ", "Tỷ lệ sàng lọc trước sinh và sơ sinh", "70% trẻ sinh ra", "74% đạt chuẩn", "VƯỢT CHỈ TIÊU"],
            ["Mục Tiêu 2: Nâng Cao Năng Lực Cán Bộ", "Tập huấn chuyên sâu cho cán bộ cơ sở", "100% trạm y tế", "100% hoàn thành", "HOÀN THÀNH"],
            ["Mục Tiêu 2: Nâng Cao Năng Lực Cán Bộ", "Đạt chuẩn kỹ thuật chăm sóc người cao tuổi", "90% địa bàn", "92% đạt chuẩn", "HOÀN THÀNH"],
            ["Mục Tiêu 3: Đảm Bảo Chất Lượng Toàn Diện", "Chỉ số hài lòng của người thụ hưởng dịch vụ", "≥ 90% hài lòng", "94.5% hài lòng", "XUẤT SẮC"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.28
        tbl.Columns(2).Width = width * 0.36
        tbl.Columns(3).Width = width * 0.12
        tbl.Columns(4).Width = width * 0.12
        tbl.Columns(5).Width = width * 0.12

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx in {3, 4, 5} else ppAlignLeft)

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                fg = "#10B981" if c_idx == 5 else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx in {1, 5} else msoFalse, ppAlignCenter if c_idx in {3, 4, 5} else ppAlignLeft)

        return table_shape

    # 23. TABLE_EMPLOYEE_SKILLS_MATRIX (Ma Trận Năng Lực Nhân Sự)
    def render_skills_matrix(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Thành Viên / Vai Trò", "Python / COM API", "Kiến Trúc Đồ Họa", "Motion & Transition", "Kiểm Định Tác Tử QA", "Đánh Giá Chung"])
        rows = table_data.get("rows", [
            ["Nguyễn Văn A (Lead Architect)", "Level 5 (Chuyên Gia)", "Level 5 (Chuyên Gia)", "Level 4 (Nâng Cao)", "Level 5 (Chuyên Gia)", "XUẤT SẮC"],
            ["Trần Thị B (Graphic Designer)", "Level 3 (Thành Thạo)", "Level 5 (Chuyên Gia)", "Level 5 (Chuyên Gia)", "Level 4 (Nâng Cao)", "XUẤT SẮC"],
            ["Lê Hoàng C (Motion Engineer)", "Level 4 (Nâng Cao)", "Level 4 (Nâng Cao)", "Level 5 (Chuyên Gia)", "Level 4 (Nâng Cao)", "XUẤT SẮC"],
            ["Phạm Minh D (QA Automation)", "Level 4 (Nâng Cao)", "Level 3 (Thành Thạo)", "Level 4 (Nâng Cao)", "Level 5 (Chuyên Gia)", "XUẤT SẮC"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.26
        for c in range(2, num_cols + 1):
            tbl.Columns(c).Width = (width * 0.74) / (num_cols - 1)

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            self._apply_header_cell(tbl.Cell(1, c_idx), h, brand, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                fg = "#38BDF8" if "Level 5" in str(val) else ("#10B981" if c_idx == 6 else ink)
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, row_bg, fg, msoTrue if c_idx in {1, 6} else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 24. TABLE_PRODUCT_SPECS (Bảng So Sánh Thông Số Kỹ Thuật Sản Phẩm)
    def render_product_specs(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Tiêu Chuẩn Đánh Giá", "Mức Cơ Bản", "Mức Nâng Cao", "Mức Đạt Chuẩn Quốc Gia"])
        rows = table_data.get("rows", [
            ["Phạm Vi Tiếp Cận Đối Tượng", "Tối thiểu 60%", "Đạt 85%", "Bao phủ 100% đối tượng đích"],
            ["Chất Lượng Cung Ứng Kỹ Thuật", "Đạt chuẩn cơ sở", "Đạt chuẩn tuyến huyện", "Đạt chuẩn bệnh viện chuyên khoa"],
            ["Đội Ngũ Nhân Lực Chuyên Môn", "Tập huấn định kỳ", "Có chứng chỉ thực hành", "Đào tạo liên tục chuyên sâu"],
            ["Kiểm Định Chất Lượng Độc Lập", "Kiểm tra 6 tháng/lần", "Kiểm tra hàng quý", "Giám sát thời gian thực"],
            ["Mức Độ Hài Lòng Của Người Dân", "≥ 75% hài lòng", "≥ 85% hài lòng", "≥ 95% rất hài lòng"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.31
        tbl.Columns(2).Width = width * 0.23
        tbl.Columns(3).Width = width * 0.23
        tbl.Columns(4).Width = width * 0.23

        brand = self._get_token("colors", "brand", "#0284C7")
        accent = self._get_token("colors", "accent", "#38BDF8")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            bg = accent if c_idx == 4 else brand
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                col_bg = "#0C4A6E" if c_idx == 4 else row_bg
                fg = "#38BDF8" if c_idx == 4 else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, col_bg, fg, msoTrue if c_idx in {1, 4} else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

    # 25. TABLE_SLA_TIERS (Bảng Cam Kết Chất Lượng Dịch Vụ SLA)
    def render_sla_tiers(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> Any:
        table_data = spec.get("table_data", {})
        headers = table_data.get("headers", ["Hạng Mục Cam Kết", "Bronze SLA", "Silver SLA", "Gold SLA (Doanh Nghiệp)"])
        rows = table_data.get("rows", [
            ["Thời Gian Uptime Khả Dụng Hệ Thống", "99.0% Uptime / Tháng", "99.9% Uptime / Tháng", "99.99% Uptime (Zero-Downtime)"],
            ["Thời Gian Phản Hồi Sự Cố P0 (Khẩn Cấp)", "< 4 Giờ Làm Việc", "< 1 Giờ Làm Việc", "< 15 Phút Phản Hồi 24/7"],
            ["Tần Suất Sao Lưu & Phục Hồi Dữ Liệu", "Hàng Tuần (Weekly)", "Hàng Ngày (Daily)", "Thời Gian Thực (Continuous RPO=0)"],
            ["Kênh Tiếp Nhận Hỗ Trợ Kỹ Thuật", "Web Ticket", "Email + Chat Trực Tuyến", "Kênh Thoại Riêng + Dedicated Engineer"],
            ["Bồi Thường Vi Phạm Cam Kết Dịch Vụ", "10% Giá Trị Hợp Đồng", "25% Giá Trị Hợp Đồng", "50% - 100% Giá Trị Gói Dịch Vụ"]
        ])

        num_rows = len(rows) + 1
        num_cols = len(headers)
        table_shape = slide.Shapes.AddTable(num_rows, num_cols, left, top, width, height)
        table_shape.Name = "!!Stage_Hero_Container!!"
        tbl = table_shape.Table

        tbl.Columns(1).Width = width * 0.34
        tbl.Columns(2).Width = width * 0.22
        tbl.Columns(3).Width = width * 0.22
        tbl.Columns(4).Width = width * 0.22

        brand = self._get_token("colors", "brand", "#0284C7")
        surface = self._get_token("colors", "surface", "#0B132B")
        ink = self._get_token("colors", "ink", "#FFFFFF")

        for c_idx, h in enumerate(headers, start=1):
            bg = "#D97706" if c_idx == 2 else ("#64748B" if c_idx == 3 else "#0284C7")
            self._apply_header_cell(tbl.Cell(1, c_idx), h, bg, "#FFFFFF", ppAlignCenter if c_idx > 1 else ppAlignLeft)

        for r_idx, row_items in enumerate(rows, start=2):
            row_bg = surface if (r_idx % 2 == 1) else ("#111C3A" if self.theme == "DARK" else "#F8FAFC")
            for c_idx, val in enumerate(row_items, start=1):
                col_bg = "#0C4A6E" if c_idx == 4 else row_bg
                fg = "#38BDF8" if c_idx == 4 else ink
                self._apply_body_cell(tbl.Cell(r_idx, c_idx), val, col_bg, fg, msoTrue if c_idx in {1, 4} else msoFalse, ppAlignCenter if c_idx > 1 else ppAlignLeft)

        return table_shape

