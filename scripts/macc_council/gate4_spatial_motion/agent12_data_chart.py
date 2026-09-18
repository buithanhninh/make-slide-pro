"""
scripts/macc_council/gate4_spatial_motion/agent12_data_chart.py
Agent 12: DataChartCartographer (Chart & Quantitative Visualization Auditor).
Audits chart archetype specifications across 22 chart types, validating axis units,
series data integrity, and 100% component summation.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class DataChartCartographer(BaseCouncilAgent):
    """
    Agent 12: Data Chart Cartographer.
    Audits 22 specialized chart archetypes (grouped bar, line, waterfall, radar, donut, etc.).
    Guarantees that chart data is never empty, axes are explicitly labeled with units,
    and proportional charts sum accurately to 100%.
    """

    SUPPORTED_CHARTS = {
        "bar_vertical", "bar_horizontal", "grouped_bar", "stacked_bar", "stacked_bar_100",
        "line", "area_stacked", "waterfall", "radar", "treemap", "scatter", "bubble",
        "donut", "pie", "funnel", "bullet", "gauge", "sankey", "heatmap", "pareto",
        "mekko", "dumbbell"
    }

    def __init__(self):
        super().__init__(name="DataChartCartographer", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            chart = s.get("chart") or s.get("chart_spec")

            if chart and isinstance(chart, dict):
                chart_type = chart.get("type", "bar_vertical")

                # 1. Missing Data Check (P0 Blocker)
                series = chart.get("series", [])
                data = chart.get("data", [])
                if not series and not data:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P0,
                            issue="Biểu đồ thiếu dữ liệu (Empty Chart Data)",
                            rationale=f"Biểu đồ loại '{chart_type}' được khai báo nhưng không có trường series hoặc data số liệu.",
                            suggestion="Bổ sung cấu trúc dữ liệu chuỗi series cho biểu đồ.",
                            evidence=f"chart_type='{chart_type}', series={series}"
                        )
                    )
                    continue

                # 2. Missing Units / Measurement Labels (P1)
                unit = chart.get("unit") or chart.get("y_unit") or chart.get("value_label")
                if not unit:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Biểu đồ '{chart_type}' thiếu đơn vị đo lường trục (Missing Measurement Unit)",
                            rationale="Số liệu biểu đồ không có đơn vị đo lường (ví dụ: %, tỷ VNĐ, triệu người) khiến người xem không thể lượng hóa quy mô.",
                            suggestion="Khai báo tường minh trường unit trong biểu đồ (ví dụ: unit='Tỷ VNĐ' hoặc unit='%').",
                            evidence=f"chart keys: {list(chart.keys())}",
                            original_value=None,
                            suggested_value="Tỷ VNĐ"
                        )
                    )

                # 3. Pie / Donut / 100% Stacked Summation Check (P0)
                if chart_type in ["pie", "donut", "stacked_bar_100"]:
                    values = []
                    if data and isinstance(data, list):
                        if isinstance(data[0], (int, float)):
                            values = data
                        elif isinstance(data[0], dict):
                            values = [d.get("value", 0) for d in data if "value" in d]

                    if values and all(isinstance(v, (int, float)) for v in values):
                        total = sum(values)
                        # Expect sum to be approximately 100
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

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for s in slides:
            chart = s.get("chart") or s.get("chart_spec")
            if chart and isinstance(chart, dict):
                # If missing unit, inject default unit
                if not chart.get("unit") and not chart.get("y_unit"):
                    chart["unit"] = "%"

                # If pie/donut doesn't sum to 100, normalize
                chart_type = chart.get("type")
                if chart_type in ["pie", "donut", "stacked_bar_100"]:
                    data = chart.get("data", [])
                    if data and isinstance(data, list) and isinstance(data[0], (int, float)):
                        total = sum(data)
                        if total > 0 and abs(total - 100.0) > 1.0:
                            chart["data"] = [round((v / total) * 100.0, 1) for v in data]

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides
