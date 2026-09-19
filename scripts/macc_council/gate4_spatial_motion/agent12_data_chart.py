"""
scripts/macc_council/gate4_spatial_motion/agent12_data_chart.py
Agent 12: DataChartCartographer (Chart & Quantitative Visualization Auditor).
Audits chart archetype specifications across 22 chart types, validating axis units,
deep series data integrity, 100% component summation, slice clutter limits, and time-series appropriateness.
Hardened with comprehensive deep data checks, time-series guards, and universal dict/array auto-normalization.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class DataChartCartographer(BaseCouncilAgent):
    """
    Agent 12: Data Chart Cartographer.
    Audits 22 specialized chart archetypes (grouped bar, line, waterfall, radar, donut, etc.).
    Guarantees that chart data is never empty, axes are explicitly labeled with units,
    proportional charts sum accurately to 100%, and time-series data is not abused in pie charts.
    """

    SUPPORTED_CHARTS = {
        "bar_vertical", "bar_horizontal", "grouped_bar", "stacked_bar", "stacked_bar_100",
        "line", "area_stacked", "waterfall", "radar", "treemap", "scatter", "bubble",
        "donut", "pie", "funnel", "bullet", "gauge", "sankey", "heatmap", "pareto",
        "mekko", "dumbbell"
    }

    NATIVE_CHART_TYPES = {
        "POPULATION_PYRAMID", "FERTILITY_TRENDS", "FERTILITY_BY_REGION_BAR",
        "LIFE_EXPECTANCY_WATERFALL", "MORTALITY_CURVE_GOMPERTZ", "DEMO_TRANSITION_STAGES",
        "AGE_STRUCTURE_RADAR", "DEPENDENCY_RATIO_TRENDS", "DEMOGRAPHIC_DIVIDEND_STACKED_AREA",
        "DEPENDENCY_COMPONENTS_GROUPED", "LABOR_FORCE_DONUT", "HDI_DIMENSIONS",
        "URBAN_RURAL_DIVERGENCE_BUBBLE", "REGIONAL_DENSITY", "MIGRATION_FLOWS_MATRIX",
        "URBANIZATION_SCURVE", "POPULATION_FORECAST_SCENARIOS", "MATH_MODELS",
        "SEX_RATIO_BIRTH_HEATMAP", "CENSUS_DATA_COLLECTION_FLOW", "POPULATION_METRICS",
        "SYSTEM_INTERACTION"
    }

    TIME_INDICATORS = re.compile(
        r"\b(năm\s*20\d{2}|20\d{2}|quý\s*[1-4]|tháng\s*\d{1,2}|q[1-4]|year|quarter|month)\b",
        re.IGNORECASE
    )

    def __init__(self):
        super().__init__(name="DataChartCartographer", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _has_valid_data(self, chart: Dict[str, Any]) -> bool:
        """Deep check to ensure chart has at least one valid non-empty series or data array."""
        data = chart.get("data")
        if data and isinstance(data, list) and len(data) > 0:
            return True

        series = chart.get("series")
        if series and isinstance(series, list) and len(series) > 0:
            for s in series:
                if isinstance(s, dict):
                    s_data = s.get("data")
                    if s_data and isinstance(s_data, list) and len(s_data) > 0:
                        return True
                elif isinstance(s, (int, float)):
                    return True
        return False

    def _extract_proportional_values(self, chart: Dict[str, Any]) -> List[float]:
        """Extracts numeric values from either array of numbers or array of dicts."""
        data = chart.get("data", [])
        values: List[float] = []
        if data and isinstance(data, list):
            for d in data:
                if isinstance(d, (int, float)):
                    values.append(float(d))
                elif isinstance(d, dict) and "value" in d and isinstance(d["value"], (int, float)):
                    values.append(float(d["value"]))
        return values

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            chart = s.get("chart") or s.get("chart_spec")

            # Native demographic chart check
            native_ct = s.get("chart_type")
            if native_ct and isinstance(native_ct, str):
                native_ct_upper = native_ct.upper()
                if native_ct_upper not in self.NATIVE_CHART_TYPES:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Loại biểu đồ nhân khẩu học không chuẩn hóa: '{native_ct}'",
                            rationale="Hệ thống chỉ hỗ trợ danh mục biểu đồ nhân khẩu học và đồ thị chuyên sâu chuẩn hóa.",
                            suggestion="Chuyển sang loại biểu đồ hợp lệ như 'POPULATION_PYRAMID', 'FERTILITY_TRENDS', hoặc 'REGIONAL_DENSITY'.",
                            evidence=f"chart_type='{native_ct}'",
                            original_value=native_ct,
                            suggested_value="POPULATION_PYRAMID"
                        )
                    )

                atoms = s.get("atoms", [])
                cards = s.get("cards", [])
                if not atoms and not cards:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue="Biểu đồ trực quan thiếu phân tích định tính (Missing Chart Insights)",
                            rationale="Theo nguyên lý Chart & Insights, biểu đồ số liệu phải luôn đi kèm ít nhất 1-3 thẻ insight phân tích ý nghĩa số liệu.",
                            suggestion="Bổ sung các thẻ atoms diễn giải ý nghĩa phát hiện từ biểu đồ.",
                            evidence=f"chart_type='{native_ct}', atoms count={len(atoms)}"
                        )
                    )

            if chart and isinstance(chart, dict):
                chart_type = chart.get("type", "bar_vertical")

                # 1. Deep Missing Data Check (P0 Blocker)
                if not self._has_valid_data(chart):
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P0,
                            issue="Biểu đồ thiếu dữ liệu (Empty Chart Data)",
                            rationale=f"Biểu đồ loại '{chart_type}' được khai báo nhưng không có dữ liệu chuỗi series hoặc mảng data chứa điểm số liệu hợp lệ.",
                            suggestion="Bổ sung cấu trúc dữ liệu chuỗi series hoặc mảng data cho biểu đồ.",
                            evidence=f"chart_type='{chart_type}', chart_keys={list(chart.keys())}"
                        )
                    )
                    continue

                # 2. Missing Units / Measurement Labels (P1)
                unit = (
                    chart.get("unit") or
                    chart.get("y_unit") or
                    chart.get("value_label") or
                    chart.get("value_unit") or
                    (isinstance(chart.get("y_axis"), dict) and chart["y_axis"].get("unit"))
                )
                if not unit:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Biểu đồ '{chart_type}' thiếu đơn vị đo lường trục (Missing Measurement Unit)",
                            rationale="Số liệu biểu đồ không có đơn vị đo lường (ví dụ: %, Tỷ VNĐ, triệu người) khiến người xem không thể lượng hóa quy mô.",
                            suggestion="Khai báo tường minh trường unit trong biểu đồ (ví dụ: unit='Tỷ VNĐ' hoặc unit='%').",
                            evidence=f"chart keys: {list(chart.keys())}",
                            original_value=None,
                            suggested_value="%" if chart_type in ["pie", "donut", "stacked_bar_100"] else "Tỷ VNĐ"
                        )
                    )

                # 3. Pie / Donut Specialized Validations
                if chart_type in ["pie", "donut", "stacked_bar_100"]:
                    values = self._extract_proportional_values(chart)
                    data = chart.get("data", [])

                    # 3a. Summation Check (P0)
                    if values:
                        total = sum(values)
                        if abs(total - 100.0) > 1.0:
                            findings.append(
                                AgentFinding(
                                    agent=self.name,
                                    gate=self.gate,
                                    slide_id=slide_id,
                                    severity=Severity.P0,
                                    issue=f"Tổng tỷ lệ phần trăm biểu đồ {chart_type} không bằng 100% (Tổng = {total:.1f}%)",
                                    rationale="Biểu đồ cơ cấu thành phần bắt buộc tổng các phần phải bằng 100%. Sai lệch thể hiện tính toán số liệu bất nhất.",
                                    suggestion="Chuẩn hóa lại các giá trị thành phần để tổng chính xác là 100.0%.",
                                    evidence=f"Values: {values} -> Sum = {total:.1f}%",
                                    original_value=str(values),
                                    suggested_value="Normalized to 100%"
                                )
                            )

                    # 3b. Slice Clutter Guard (> 7 slices) (P1)
                    if len(values) > 7:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue=f"Biểu đồ {chart_type} có quá nhiều lát cắt ({len(values)} lát cắt > 7)",
                                rationale="Biểu đồ tròn/donut có trên 7 lát cắt gây rối loạn thị giác và khó đọc nhãn số liệu.",
                                suggestion="Chuyển sang biểu đồ thanh ngang (bar_horizontal) hoặc gom các phần nhỏ thành mục 'Khác'.",
                                evidence=f"Slice count: {len(values)}",
                                original_value=chart_type,
                                suggested_value="bar_horizontal"
                            )
                        )

                    # 3c. Time-Series Misuse in Pie Chart (P1)
                    if data and isinstance(data, list):
                        time_matches = 0
                        for item in data:
                            if isinstance(item, dict):
                                label = str(item.get("label", ""))
                                if self.TIME_INDICATORS.search(label):
                                    time_matches += 1
                        if time_matches >= 3:
                            findings.append(
                                AgentFinding(
                                    agent=self.name,
                                    gate=self.gate,
                                    slide_id=slide_id,
                                    severity=Severity.P1,
                                    issue=f"Biểu đồ {chart_type} bị lạm dụng cho dữ liệu chuỗi thời gian",
                                    rationale="Biểu đồ tròn chỉ dùng để thể hiện cơ cấu tĩnh tại một thời điểm, không dùng cho xu hướng chuỗi thời gian.",
                                    suggestion="Chuyển sang biểu đồ đường (line) hoặc biểu đồ cột (bar_vertical) để thể hiện chuỗi thời gian.",
                                    evidence=f"Time labels detected: {time_matches}",
                                    original_value=chart_type,
                                    suggested_value="line"
                                )
                            )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for s in slides:
            # 1. Remediate native demographic charts
            native_ct = s.get("chart_type")
            if native_ct and isinstance(native_ct, str):
                if native_ct.upper() not in self.NATIVE_CHART_TYPES:
                    s["chart_type"] = "POPULATION_PYRAMID"
                atoms = s.get("atoms", [])
                cards = s.get("cards", [])
                if not atoms and not cards:
                    s["atoms"] = [
                        {
                            "kicker": "PHÂN TÍCH TRỌNG TÂM",
                            "title": "Xu hướng biến động chỉ số then chốt",
                            "text": "Số liệu phản ánh xu thế chuyển dịch rõ nét và tạo tiền đề cho các quyết sách chiến lược."
                        }
                    ]

            chart = s.get("chart") or s.get("chart_spec")
            if chart and isinstance(chart, dict):
                chart_type = chart.get("type", "bar_vertical")

                # 1. Inject missing unit
                unit = chart.get("unit") or chart.get("y_unit")
                if not unit:
                    chart["unit"] = "%" if chart_type in ["pie", "donut", "stacked_bar_100"] else "Tỷ VNĐ"

                # 2. Normalize 100% proportional charts
                if chart_type in ["pie", "donut", "stacked_bar_100"]:
                    data = chart.get("data", [])
                    if data and isinstance(data, list):
                        # Case A: list of numbers
                        if all(isinstance(v, (int, float)) for v in data):
                            total = sum(data)
                            if total > 0 and abs(total - 100.0) > 1.0:
                                chart["data"] = [round((v / total) * 100.0, 1) for v in data]
                        # Case B: list of dicts
                        elif all(isinstance(v, dict) and "value" in v and isinstance(v["value"], (int, float)) for v in data):
                            total = sum(v["value"] for v in data)
                            if total > 0 and abs(total - 100.0) > 1.0:
                                for v in data:
                                    v["value"] = round((v["value"] / total) * 100.0, 1)

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides
