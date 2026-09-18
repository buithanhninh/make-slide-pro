# upgrade_blueprints.py
# Deeply enriches curriculum_blueprints_data.py with Formula Hero Cards, Native Data Tables, and Publication Charts.

import json
import sys
from pathlib import Path

# Ensure scripts dir is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import curriculum_blueprints_data as cbd

def upgrade_all_blueprints():
    b1 = cbd.get_lesson_blueprints_bai_1()
    b2 = cbd.get_lesson_blueprints_bai_2()
    b3 = cbd.get_lesson_blueprints_bai_3()
    b4 = cbd.get_lesson_blueprints_bai_4()
    b5 = cbd.get_lesson_blueprints_bai_5()

    # === BAI 1 UPGRADES ===
    for s in b1["slides"]:
        if s.get("slide_id") == "SLIDE_04":
            s["visual_job"] = "DATA_TABLE"
            s["table_data"] = {
                "headers": ["Tiêu Chí So Sánh", "Dân Cư (Geography)", "Dân Số (Demography)", "Ý Nghĩa Quản Trị"],
                "rows": [
                    ["Bản Chất Khái Niệm", "Tập hợp người sinh sống trên một lãnh thổ địa lý", "Tập hợp người gắn liền tái sản xuất, sinh tử và cơ cấu", "Xác định rõ đối tượng"],
                    ["Góc Độ Tiếp Cận", "Không gian địa lý, phân bố cư trú và cảnh quan", "Quy luật sinh học, kinh tế và biến động nhân khẩu", "Đo lường tỷ suất chuẩn"],
                    ["Thuộc Tính Thống Kê", "Phản ánh dung lượng cư trú và mật độ lãnh thổ", "Phân rã chi tiết theo tuổi, giới tính, học vấn", "Cơ sở phân bổ ngân sách"],
                    ["Phạm Vi Ứng Dụng", "Địa lý kinh tế, quy hoạch giao thông, tài nguyên", "Chính sách dân số, an sinh xã hội và thị trường", "Hoạch định chiến lược dài hạn"]
                ],
                "col_widths": [0.20, 0.28, 0.28, 0.24]
            }

    # === BAI 2 UPGRADES ===
    for s in b2["slides"]:
        sid = s.get("slide_id")
        if sid == "SLIDE_04":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "P_tb = (P_0 + P_t) / 2 = [0.5*P_1 + P_2 + P_3 + 0.5*P_n] / (n - 1)"
        elif sid == "SLIDE_05":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "P_t = P_0 + (B - D) + (I - O) = P_0 + N_i + N_m"
        elif sid == "SLIDE_07":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "P_t = P_0 * e^(r*t)  ==>  r = [ln(P_t / P_0)] / t"
        elif sid == "SLIDE_08":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "T_2 = ln(2) / r ≈ 70 / r(%)  (Quy tắc 70 nhân đôi dân số)"
        elif sid == "SLIDE_12":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "TDR = [(P_0-14 + P_65+) / P_15-64] * 100 = YDR + ADR"
        elif sid == "SLIDE_13":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "SR = (Số Nam / Số Nữ) * 100  |  SRB = (Bé Trai / Bé Gái) * 100"
        elif sid == "SLIDE_16":
            s["visual_job"] = "CHART_AND_INSIGHTS"
            s["chart_type"] = "DEPENDENCY_RATIO_TRENDS"
        elif sid == "SLIDE_18":
            s["visual_job"] = "DATA_TABLE"
            s["table_data"] = {
                "headers": ["Dạng Tháp Dân Số", "Đáy Tháp", "Thân Tháp", "Đỉnh Tháp", "Đặc Trưng Dân Số & Điển Hình"],
                "rows": [
                    ["Tháp Mở Rộng (Expansive)", "Rất rộng, đáy mở to", "Thu hẹp nhanh dần", "Đỉnh tháp nhọn hẹp", "Dân số trẻ, sinh cao, tử giảm (Các nước đang phát triển)"],
                    ["Tháp Ổn Định (Stationary)", "Tương đương thân", "Thẳng đứng, đều đặn", "Đỉnh tháp mở rộng", "Dân số dừng, TFR ≈ 2.1 con, sống thọ (Bắc Âu, Thụy Điển)"],
                    ["Tháp Thu Hẹp (Constrictive)", "Co thắt, hẹp hơn thân", "Phình to ở giữa", "Đỉnh tháp rất rộng", "Dân số già, sinh thấp kéo dài (Nhật Bản, Đức, Ý)"]
                ],
                "col_widths": [0.22, 0.18, 0.18, 0.18, 0.24]
            }
        elif sid == "SLIDE_22":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "HDI = [I_Health * I_Education * I_Income]^(1/3) = (LEI * EI * II)^(1/3)"
        elif sid == "SLIDE_23":
            s["visual_job"] = "CHART_AND_INSIGHTS"
            s["chart_type"] = "HDI_DIMENSIONS"

    # === BAI 3 UPGRADES ===
    for s in b3["slides"]:
        sid = s.get("slide_id")
        if sid == "SLIDE_04":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "CBR = (B / P_tb) * 1,000  (Đơn vị: ‰ - Trên 1.000 dân trung bình)"
        elif sid == "SLIDE_05":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "GFR = [B / W_(15-49)] * 1,000  (Đơn vị: ‰ - Phụ nữ 15-49 tuổi)"
        elif sid == "SLIDE_06":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "ASFR_x = (B_x / W_x) * 1,000  (Đơn vị: ‰ - Cho từng nhóm tuổi x)"
        elif sid == "SLIDE_07":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "TFR = 5 * Σ(ASFR_x) / 1,000  (Mức sinh thay thế chuẩn = 2.10 con)"
        elif sid == "SLIDE_14":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "ASDR_x = (D_x / P_(x,tb)) * 1,000  (Đồ thị tử vong dạng chữ U kinh điển)"
        elif sid == "SLIDE_15":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "IMR = (D_0 / B) * 1,000  |  U5MR = (D_0-4 / B) * 1,000  (‰)"
        elif sid == "SLIDE_17":
            s["visual_job"] = "DATA_TABLE"
            s["table_data"] = {
                "headers": ["Độ Tuổi (x)", "Số Sống Sót (lx)", "Số Ca Tử Vong (dx)", "Xác Suất Chết (qx)", "Kỳ Vọng Sống (ex)"],
                "rows": [
                    ["0 (Sơ sinh)", "100,000", "1,160", "0.0116", "73.7 năm"],
                    ["1 - 4 tuổi", "98,840", "660", "0.0067", "73.6 năm"],
                    ["5 - 14 tuổi", "98,180", "390", "0.0040", "69.8 năm"],
                    ["15 - 59 tuổi", "97,790", "12,450", "0.1273", "60.1 năm"],
                    ["60 - 79 tuổi", "85,340", "42,800", "0.5015", "20.4 năm"],
                    ["80 tuổi trở lên", "42,540", "42,540", "1.0000", "7.8 năm"]
                ],
                "col_widths": [0.20, 0.20, 0.20, 0.20, 0.20]
            }
        elif sid == "SLIDE_21":
            s["visual_job"] = "CHART_AND_INSIGHTS"
            s["chart_type"] = "DEMO_TRANSITION_STAGES"

    # === BAI 4 UPGRADES ===
    for s in b4["slides"]:
        sid = s.get("slide_id")
        if sid == "SLIDE_04":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "D_sohoc = P / S (người/km²)  |  D_kinhte = P / S_nongnghiep (người/ha)"
        elif sid == "SLIDE_06":
            s["visual_job"] = "DATA_TABLE"
            s["table_data"] = {
                "headers": ["Vùng Kinh Tế - Xã Hội", "Dân Số (Triệu)", "Tỷ Trọng (%)", "Mật Độ (ng/km²)", "Di Cư Thuần (‰)"],
                "rows": [
                    ["Đồng Bằng Sông Hồng", "23.4 Triệu", "23.4%", "1,090 ng/km²", "+2.1 ‰ (Hút di dân)"],
                    ["Trung Du & MN Phía Bắc", "13.0 Triệu", "13.0%", "136 ng/km²", "-2.8 ‰ (Xuất cư)"],
                    ["Bắc Trung Bộ & Duyên Hải MT", "20.7 Triệu", "20.7%", "216 ng/km²", "-3.5 ‰ (Xuất cư)"],
                    ["Tây Nguyên", "6.1 Triệu", "6.1%", "111 ng/km²", "-0.8 ‰ (Cân bằng)"],
                    ["Đông Nam Bộ", "18.8 Triệu", "18.8%", "795 ng/km²", "+11.2 ‰ (Đô thị hóa cao)"],
                    ["Đồng Bằng Sông Cửu Long", "17.5 Triệu", "17.5%", "426 ng/km²", "-4.6 ‰ (Xuất cư lớn)"]
                ],
                "col_widths": [0.28, 0.18, 0.16, 0.18, 0.20]
            }
        elif sid == "SLIDE_10":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "NMR = [(I - O) / P_tb] * 1,000  |  MER = [(I - O) / (I + O)] * 100"
        elif sid == "SLIDE_17":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "PU(%) = (P_u / P_total) * 100  |  UR = [(P_u,t - P_u,0) / t] * 100"
        elif sid == "SLIDE_18":
            s["visual_job"] = "CHART_AND_INSIGHTS"
            s["chart_type"] = "URBANIZATION_SCURVE"

    # === BAI 5 UPGRADES ===
    for s in b5["slides"]:
        sid = s.get("slide_id")
        if sid == "SLIDE_05":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "P_t = P_0 * (1 + r*t)  |  P_t = P_0 * (1 + r)^t  (Ngoại suy ngắn hạn)"
        elif sid == "SLIDE_06":
            s["visual_job"] = "CHART_AND_INSIGHTS"
            s["chart_type"] = "MATH_MODELS"
        elif sid == "SLIDE_07":
            s["visual_job"] = "FORMULA_CARD"
            s["formula"] = "P_(x+n, t+n) = P_(x,t) * S_(x,x+n) + NetMig_(x,x+n)  (Tiêu chuẩn UN)"
        elif sid == "SLIDE_14":
            s["visual_job"] = "DATA_TABLE"
            s["table_data"] = {
                "headers": ["Kịch Bản Dự Báo", "Giả Thiết Mức Sinh (TFR)", "Dân Số Năm 2030", "Quy Mô Đỉnh Dân Số", "Thời Điểm Đạt Đỉnh"],
                "rows": [
                    ["Kịch Bản Thấp", "TFR giảm nhanh về 1.60 con/phụ nữ", "102.5 Triệu", "104.2 Triệu", "Năm 2044 (Đạt đỉnh sớm)"],
                    ["Kịch Bản Trung Bình", "Duy trì ổn định TFR ≈ 2.05 con/phụ nữ", "104.5 Triệu", "107.0 Triệu", "Năm 2055 (Khả dĩ nhất)"],
                    ["Kịch Bản Cao", "TFR phục hồi đạt 2.25 con/phụ nữ", "106.8 Triệu", "112.5 Triệu", "Sau năm 2065 (Tăng dài)"]
                ],
                "col_widths": [0.22, 0.28, 0.16, 0.16, 0.18]
            }

    # Generate output Python file
    out_lines = [
        '"""',
        'curriculum_blueprints_data.py',
        'Exhaustive Deep-Curriculum Slide Blueprints for Make Slide Pro V7.2.',
        'Contains full academic coverage (106 slides total across 5 core modules):',
        '- Bai 1 (Nhap Mon DSH): 14 slides',
        '- Bai 2 (Quy Mo, Co Cau, Chat Luong DS): 28 slides',
        '- Bai 3 (Bien Dong Tu Nhien DS): 22 slides',
        '- Bai 4 (Phan Bo DS va Di Dan - Do Thi Hoa): 22 slides',
        '- Bai 5 (Du Bao Dan So): 20 slides',
        'Enhanced with Formula Hero Cards, Native Data Tables, and 220 DPI Publication Charts.',
        '"""',
        '',
        'from typing import Any, Dict, List',
        '',
    ]

    for idx, (fn_name, data) in enumerate([
        ("get_lesson_blueprints_bai_1", b1),
        ("get_lesson_blueprints_bai_2", b2),
        ("get_lesson_blueprints_bai_3", b3),
        ("get_lesson_blueprints_bai_4", b4),
        ("get_lesson_blueprints_bai_5", b5)
    ], 1):
        out_lines.append(f"def {fn_name}() -> Dict[str, Any]:")
        formatted_json = json.dumps(data, ensure_ascii=False, indent=4)
        # Indent each line by 4 spaces
        indented = "\n".join("    " + line for line in formatted_json.splitlines())
        out_lines.append(f"    return {indented.strip()}")
        out_lines.append("")
        out_lines.append("")

    target_file = SCRIPT_DIR / "curriculum_blueprints_data.py"
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"Successfully upgraded {target_file} with Formula Cards, Native Data Tables, and Charts!")

if __name__ == "__main__":
    upgrade_all_blueprints()
