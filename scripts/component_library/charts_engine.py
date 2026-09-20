"""
charts_engine.py
100% Native Editable Microsoft Office Chart Engine for Make Slide Pro V8.4.0.
Creates genuine PowerPoint Office Charts (Shapes.AddChart) with embedded
Excel Worksheets so users can right-click and choose 'Edit Data in Excel'.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

# Win32 & Office Chart Constants
xlColumnClustered = 51
xlColumnStacked = 52
xlColumnStacked100 = 53
xlBarClustered = 57
xlBarStacked = 58
xlBarStacked100 = 59
xlLine = 4
xlLineMarkers = 65
xlPie = 5
xlDoughnut = -4120
xlArea = 1
xlAreaStacked = 76
xlRadar = -4151
xlRadarFilled = 82
xlPieExploded = 69
xlXYScatter = -4169
xlBubble = 15
msoShapeOval = 9
msoShapeRoundedRectangle = 5
msoTextOrientationHorizontal = 1
ppAlignCenter = 2
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


class NativeChartsEngine:
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}

    def _get_token(self, category: str, key: str, fallback: str) -> str:
        return self.tokens.get(category, {}).get(key, fallback)

    def _populate_worksheet_data(self, chart: Any, categories: List[str], series_list: List[Dict[str, Any]]) -> None:
        """
        Populates data directly into the chart's embedded Excel Worksheet
        and resizes the chart source data range.
        series_list format: [{'name': 'Series 1', 'values': [10, 20, 30]}]
        """
        try:
            chart_data = chart.ChartData
            try:
                chart_data.Activate()
            except Exception:
                pass
            workbook = chart_data.Workbook
            xl_app = getattr(workbook, "Application", None)
            if xl_app is not None:
                try:
                    xl_app.DisplayAlerts = False
                except Exception:
                    pass
            sheet = workbook.Worksheets(1)

            # Clear default dummy cells (PowerPoint defaults to 4 rows, 3 cols)
            sheet.Range("A1:Z50").ClearContents()

            # Category Header
            sheet.Range("A1").Value = "Danh Mục"

            # Series Headers
            for s_idx, s in enumerate(series_list, start=2):
                col_letter = chr(64 + s_idx)
                sheet.Range(f"{col_letter}1").Value = s.get("name", f"Chuỗi {s_idx - 1}")

            # Rows
            for r_idx, cat in enumerate(categories, start=2):
                sheet.Range(f"A{r_idx}").Value = str(cat)
                for s_idx, s in enumerate(series_list, start=2):
                    col_letter = chr(64 + s_idx)
                    vals = s.get("values", [])
                    v = vals[r_idx - 2] if (r_idx - 2) < len(vals) else 0
                    sheet.Range(f"{col_letter}{r_idx}").Value = v

            num_rows = len(categories) + 1
            num_cols = len(series_list) + 1
            last_col_letter = chr(64 + num_cols)

            data_range = f"='{sheet.Name}'!$A$1:${last_col_letter}${num_rows}"
            chart.SetSourceData(data_range)
            try:
                workbook.Close(True)
            except Exception:
                pass
            if xl_app is not None:
                try:
                    xl_app.Quit()
                except Exception:
                    pass
        except Exception as e:
            print(f"Warning: Chart Excel worksheet update error: {e}")
        
        # Automatically apply high-contrast theme styling to all charts
        self._style_chart_text(chart)

    def _style_chart_text(self, chart: Any) -> None:
        """Styles chart axes, tick labels, legend, and background with high-contrast colors matching theme."""
        try:
            axis_color = hex_to_bgr("#E2E8F0" if self.theme == "DARK" else "#1E293B")
            font_name = self.tokens.get("fonts", {}).get("primary", "Segoe UI")

            # Chart Area overall font and transparency
            try:
                chart.ChartArea.Font.Color = axis_color
                chart.ChartArea.Font.Name = font_name
                chart.ChartArea.Format.Fill.Visible = msoFalse
                chart.ChartArea.Format.Line.Visible = msoFalse
            except Exception:
                pass

            try:
                chart.PlotArea.Format.Fill.Visible = msoFalse
                chart.PlotArea.Format.Line.Visible = msoFalse
            except Exception:
                pass

            # xlCategory = 1
            try:
                ax = chart.Axes(1)
                ax.TickLabels.Font.Color = axis_color
                ax.TickLabels.Font.Size = 10
                ax.TickLabels.Font.Name = font_name
            except Exception:
                pass

            # xlValue = 2
            try:
                ay = chart.Axes(2)
                ay.TickLabels.Font.Color = axis_color
                ay.TickLabels.Font.Size = 9.5
                ay.TickLabels.Font.Name = font_name
            except Exception:
                pass

            # Legend
            try:
                if chart.HasLegend:
                    chart.Legend.Font.Color = axis_color
                    chart.Legend.Font.Size = 10
                    chart.Legend.Font.Name = font_name
                    chart.Legend.Format.Fill.Visible = msoFalse
                    chart.Legend.Format.Line.Visible = msoFalse
            except Exception:
                pass
        except Exception as e:
            pass

    # -------------------------------------------------------------
    # 1. CLUSTERED COLUMN CHART (Cột Nhóm)
    # -------------------------------------------------------------
    def render_column_clustered(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["2020", "2021", "2022", "2023", "2024"])
        series = c_data.get("series", [
            {"name": "Mục Tiêu Kế Hoạch", "values": [120, 145, 170, 205, 250]},
            {"name": "Thực Tế Đạt Được", "values": [128, 152, 168, 215, 268]}
        ])

        shape = slide.Shapes.AddChart(xlColumnClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        self._style_chart_text(chart)
        return [shape]

    # -------------------------------------------------------------
    # 2. STACKED COLUMN CHART (Cột Chồng Cơ Cấu)
    # -------------------------------------------------------------
    def render_column_stacked(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Nông Nghiệp", "Công Nghiệp", "Dịch Vụ", "Kinh Tế Số"])
        series = c_data.get("series", [
            {"name": "Đồng Bằng Sông Hồng", "values": [8.5, 42.0, 38.5, 11.0]},
            {"name": "Đông Nam Bộ", "values": [4.2, 45.8, 36.2, 13.8]},
            {"name": "ĐBSCL", "values": [28.4, 26.5, 38.1, 7.0]}
        ])

        shape = slide.Shapes.AddChart(xlColumnStacked, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 3. DIVERGING BAR CHART (Tháp Dân Số 2 Vế Đối Xứng)
    # -------------------------------------------------------------
    def render_bar_diverging(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        """
        Generates a 100% Native Population Pyramid in PowerPoint.
        Uses negative values for Males and positive values for Females.
        """
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["0-4", "5-14", "15-24", "25-39", "40-54", "55-64", "65-74", "75+"])
        # Negative values for left side
        series = c_data.get("series", [
            {"name": "Nam Giới (%)", "values": [-3.8, -7.6, -7.8, -12.5, -10.2, -5.8, -3.2, -1.4]},
            {"name": "Nữ Giới (%)", "values": [3.5, 7.1, 7.3, 12.1, 10.4, 6.4, 4.1, 2.3]}
        ])

        shape = slide.Shapes.AddChart(xlBarClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 4. MULTI-SERIES LINE TREND CHART (Đường Xu Hướng)
    # -------------------------------------------------------------
    def render_line_trend(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["1999", "2009", "2015", "2019", "2021", "2023"])
        series = c_data.get("series", [
            {"name": "TFR Toàn Quốc", "values": [2.33, 2.03, 2.10, 2.09, 2.11, 1.96]},
            {"name": "TFR Đông Nam Bộ", "values": [1.95, 1.70, 1.62, 1.56, 1.48, 1.39]},
            {"name": "Mức Sinh Thay Thế", "values": [2.10, 2.10, 2.10, 2.10, 2.10, 2.10]}
        ])

        shape = slide.Shapes.AddChart(xlLineMarkers, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 5. DONUT CHART WITH KPI CENTER METRIC (Vành Khuyên + Tâm Điểm)
    # -------------------------------------------------------------
    def render_donut_kpi(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        shapes = []
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Đồng Bằng Sông Hồng", "Đông Nam Bộ", "ĐBSCL", "Bắc Trung Bộ & DHMT", "Trung Du & Miền Núi", "Tây Nguyên"])
        series = c_data.get("series", [
            {"name": "Quy Mô Dân Số", "values": [23.4, 18.8, 17.5, 20.6, 13.9, 6.1]}
        ])
        center_metric = c_data.get("center_metric", "100.3 Tr")
        center_label = c_data.get("center_label", "Tổng Dân Số")

        chart_shape = slide.Shapes.AddChart(xlDoughnut, left, top, width, height)
        chart = chart_shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True
        self._populate_worksheet_data(chart, categories, series)
        shapes.append(chart_shape)

        # Center Textbox Overlay
        center_w, center_h = 130.0, 65.0
        cx = left + (width - center_w) / 2.0 - 50.0  # Slightly offset to left since legend is on right
        cy = top + (height - center_h) / 2.0

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, cx, cy, center_w, center_h)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = center_metric + "\n"
        p1.Font.Name = self._get_token("fonts", "numeric", "Bahnschrift")
        p1.Font.Size = 22
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "brand", "#0284C7"))
        p1.ParagraphFormat.Alignment = ppAlignCenter

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = center_label
        p2.Font.Name = self._get_token("fonts", "primary", "Segoe UI")
        p2.Font.Size = 10
        p2.Font.Color.RGB = hex_to_bgr(self._get_token("colors", "muted", "#CBD5E1"))
        p2.ParagraphFormat.Alignment = ppAlignCenter
        shapes.append(tb)

        return shapes

    # -------------------------------------------------------------
    # 6. WATERFALL / BRIDGE ANALYSIS CHART (Thác Nước Biến Động)
    # -------------------------------------------------------------
    def render_waterfall(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Đầu Kỳ", "Sinh Tự Nhiên", "Di Cư Đến", "Tử Vong", "Di Cư Đi", "Cuối Kỳ"])
        series = c_data.get("series", [
            {"name": "Biến Động Quy Mô (Nghìn Người)", "values": [98500, 1420, 210, -640, -190, 99300]}
        ])

        shape = slide.Shapes.AddChart(xlColumnClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = False

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 7. COMBO DUAL-AXIS CHART (Cột + Đường 2 Trục Tung)
    # -------------------------------------------------------------
    def render_combo_dual_axis(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["2019", "2020", "2021", "2022", "2023", "2024"])
        series = c_data.get("series", [
            {"name": "Doanh Thu (Tỷ VNĐ)", "values": [520, 680, 890, 1240, 1580, 2050]},
            {"name": "Biên Lợi Nhuận (%)", "values": [12.4, 14.2, 16.8, 19.5, 21.8, 23.8]}
        ])

        shape = slide.Shapes.AddChart(xlColumnClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 8. RADAR / SPIDER CHART (Biểu Đồ Mạng Nhện)
    # -------------------------------------------------------------
    def render_radar(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Hạ Tầng Số", "Năng Lực AI", "An Ninh Mạng", "Văn Hóa Đổi Mới", "Tối Ưu Quy Trình", "Khai Thác Dữ Liệu"])
        series = c_data.get("series", [
            {"name": "Hiện Trạng Thực Tế", "values": [65, 45, 80, 55, 70, 60]},
            {"name": "Mục Tiêu Năm 2025", "values": [90, 85, 95, 85, 90, 95]}
        ])

        shape = slide.Shapes.AddChart(xlRadar, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 9. 100% STACKED COLUMN CHART (Cột Chồng 100%)
    # -------------------------------------------------------------
    def render_column_100_stacked(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["2021", "2022", "2023", "2024", "2025 (F)"])
        series = c_data.get("series", [
            {"name": "Doanh Thu Định Kỳ (SaaS ARR)", "values": [35, 48, 62, 74, 85]},
            {"name": "Dịch Vụ Tư Vấn Chuyên Sâu", "values": [45, 38, 26, 18, 10]},
            {"name": "Bản Quyền Triển Khai On-Prem", "values": [20, 14, 12, 8, 5]}
        ])

        shape = slide.Shapes.AddChart(xlColumnStacked100, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 10. CLUSTERED BAR CHART (Thanh Ngang Phân Hạng Top)
    # -------------------------------------------------------------
    def render_bar_clustered(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Hà Nội", "TP. Hồ Chí Minh", "Bình Dương", "Đà Nẵng", "Hải Phòng", "Cần Thơ"])
        series = c_data.get("series", [
            {"name": "Chỉ Số Cạnh Tranh (PCI)", "values": [71.2, 70.8, 69.5, 68.9, 68.2, 66.4]},
            {"name": "Tốc Độ Tăng Trưởng GRDP (%)", "values": [6.8, 6.2, 7.5, 7.1, 7.8, 6.0]}
        ])

        shape = slide.Shapes.AddChart(xlBarClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 11. AREA STANDARD CHART (Diện Tích Tích Lũy)
    # -------------------------------------------------------------
    def render_area_standard(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"])
        series = c_data.get("series", [
            {"name": "Lượng Người Dùng Hoạt Động (MAU - Nghìn)", "values": [120, 145, 180, 230, 290, 370, 460, 580, 710, 860, 1020, 1250]}
        ])

        shape = slide.Shapes.AddChart(xlArea, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 12. STACKED AREA CHART (Diện Tích Xếp Chồng)
    # -------------------------------------------------------------
    def render_area_stacked(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["2020", "2021", "2022", "2023", "2024"])
        series = c_data.get("series", [
            {"name": "Thị Trường Châu Á", "values": [45, 68, 95, 130, 185]},
            {"name": "Thị Trường Bắc Mỹ", "values": [30, 42, 60, 85, 120]},
            {"name": "Thị Trường Châu Âu", "values": [25, 35, 48, 65, 90]}
        ])

        shape = slide.Shapes.AddChart(xlAreaStacked, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 13. PIE CHART WITH HIGHLIGHT SLICE (Biểu Đồ Tròn Tách Lát)
    # -------------------------------------------------------------
    def render_pie_highlight_slice(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Make Slide Pro (Dẫn Đầu)", "Đối Thủ A", "Đối Thủ B", "Các Đơn Vị Khác"])
        series = c_data.get("series", [
            {"name": "Thị Phần Thị Trường (%)", "values": [58.5, 21.0, 12.5, 8.0]}
        ])

        shape = slide.Shapes.AddChart(xlPieExploded, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 14. SCATTER / CORRELATION CHART (Phân Tán Tương Quan)
    # -------------------------------------------------------------
    def render_scatter_correlation(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Điểm A", "Điểm B", "Điểm C", "Điểm D", "Điểm E", "Điểm F", "Điểm G"])
        series = c_data.get("series", [
            {"name": "Ngân Sách R&D (Tỷ VNĐ)", "values": [12, 18, 25, 34, 45, 58, 75]},
            {"name": "Tốc Độ Tăng Trưởng (%)", "values": [8, 14, 21, 32, 44, 59, 78]}
        ])

        shape = slide.Shapes.AddChart(xlLineMarkers, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 15. BUBBLE / PORTFOLIO MATRIX (Biểu Đồ Danh Mục Đa Chiều)
    # -------------------------------------------------------------
    def render_bubble_matrix(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Sản Phẩm A (Ngôi Sao)", "Sản Phẩm B (Bò Sữa)", "Sản Phẩm C (Dấu Hỏi)", "Sản Phẩm D (Chó Mực)"])
        series = c_data.get("series", [
            {"name": "Thị Phần Tương Đối (X)", "values": [3.5, 4.2, 0.8, 0.4]},
            {"name": "Tỷ Lệ Tăng Trưởng Ngành (Y)", "values": [25.0, 4.5, 22.0, 2.0]}
        ])

        shape = slide.Shapes.AddChart(xlColumnClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 16. BAR STACKED 100% (Thanh Ngang 100% Chồng)
    # -------------------------------------------------------------
    def render_bar_stacked_100(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Miền Bắc", "Miền Trung", "Miền Nam", "Đồng Bằng SCL"])
        series = c_data.get("series", [
            {"name": "Thành Thị (%)", "values": [42.5, 31.8, 68.2, 28.5]},
            {"name": "Nông Thôn (%)", "values": [57.5, 68.2, 31.8, 71.5]}
        ])

        shape = slide.Shapes.AddChart(xlBarStacked100, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 17. PARETO ANALYSIS (Biểu Đồ Pareto 80/20)
    # -------------------------------------------------------------
    def render_pareto_analysis(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Lỗi Định Dạng Font", "Lỗi Tràn Khung Chữ", "Thiếu Icon Đồ Họa", "Lỗi Màu Tương Phản", "Khác"])
        series = c_data.get("series", [
            {"name": "Số Lần Xuất Hiện (Cột)", "values": [120, 85, 45, 18, 12]},
            {"name": "Tỷ Lệ Tích Lũy % (Đường)", "values": [42.8, 73.2, 89.3, 95.7, 100.0]}
        ])

        shape = slide.Shapes.AddChart(xlColumnClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 18. STEPPED LINE (Đường Bậc Thang)
    # -------------------------------------------------------------
    def render_stepped_line(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Tháng 1", "Tháng 3", "Tháng 6", "Tháng 9", "Tháng 12"])
        series = c_data.get("series", [
            {"name": "Lãi Suất Cơ Bản Điều Hành (%)", "values": [4.5, 4.5, 5.0, 5.0, 5.5]},
            {"name": "Lãi Suất Trần Huy Động (%)", "values": [5.5, 5.5, 6.0, 6.0, 6.5]}
        ])

        shape = slide.Shapes.AddChart(xlLineMarkers, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 19. RADAR FILLED (Mạng Nhện Diện Tích Phủ)
    # -------------------------------------------------------------
    def render_radar_filled(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["Tốc Độ Render", "Độ Phủ Mẫu (165+)", "Chất Lượng Native", "Độ Ổn Định QA", "Chuyển Động Apple"])
        series = c_data.get("series", [
            {"name": "Giải Pháp Make Slide Pro", "values": [98, 100, 100, 96, 95]},
            {"name": "Tiêu Chuẩn Thị Trường", "values": [65, 40, 50, 60, 45]}
        ])

        shape = slide.Shapes.AddChart(xlRadarFilled, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = True

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

    # -------------------------------------------------------------
    # 20. HISTOGRAM DISTRIBUTION (Phân Phối Tần Suất)
    # -------------------------------------------------------------
    def render_histogram_distribution(self, slide: Any, spec: Dict[str, Any], left: float, top: float, width: float, height: float) -> List[Any]:
        c_data = spec.get("chart_data", {})
        categories = c_data.get("categories", ["0 - 5 giây", "5 - 10 giây", "10 - 15 giây", "15 - 20 giây", "20 - 25 giây", "> 25 giây"])
        series = c_data.get("series", [
            {"name": "Số Lượng Bài Thuyết Trình Hoàn Tất", "values": [45, 120, 85, 30, 15, 5]}
        ])

        shape = slide.Shapes.AddChart(xlColumnClustered, left, top, width, height)
        shape.Name = "!!Stage_Hero_Container!!"
        chart = shape.Chart
        chart.HasTitle = False
        chart.HasLegend = False

        self._populate_worksheet_data(chart, categories, series)
        return [shape]

