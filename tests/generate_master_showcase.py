"""
generate_master_showcase.py
Generates a comprehensive demonstration PowerPoint deck showcasing
the 30 elite presentation archetypes of Make Slide Pro V8.4.0.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from author_native_com import NativeDeckAuthor

def create_showcase_deck():
    output_dir = ROOT / "output" / "master_showcase"
    output_dir.mkdir(parents=True, exist_ok=True)
    blueprints_file = output_dir / "master_showcase_blueprints.json"
    output_pptx = output_dir / "make_slide_pro_master_showcase.pptx"

    slides = [
        # Slide 1: Cover
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "assertion_title": "MAKE SLIDE PRO V8.4.0: KHO THƯ VIỆN 30 ARCHETYPES TOÀN CẦU",
            "primary_claim": "Chuẩn hóa dựa trên phân tích 1,000 template slide hàng đầu thế giới (McKinsey, BCG, Apple Keynote, YC Pitch Decks).",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Kính chào quý vị, đây là bản trình diễn kho thư viện 30 thành phần thị giác cao cấp hoàn toàn có thể chỉnh sửa trực tiếp trong PowerPoint."
        },
        # Slide 2: TABLE_COMPARISON
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "THƯ VIỆN BẢNG BIỂU NATIVE",
            "assertion_title": "So Sánh Tính Năng & Năng Lực Giải Pháp: Nổi Bật Lợi Thế Đề Xuất",
            "primary_claim": "Bảng Native PowerPoint cho phép chỉnh sửa từng ô, thêm dòng cột và đổi màu tự do.",
            "visual_job": "TABLE_COMPARISON",
            "table_data": {
                "headers": ["Tiêu Chí Đánh Giá", "Giải Pháp Hiện Hữu", "Make Slide Pro V8.4 (Đề Xuất)", "Giải Pháp Mở Rộng"],
                "highlight_col": 3,
                "rows": [
                    ["Khả năng chỉnh sửa trên PPT", "Ảnh tĩnh không sửa được", "100% Native Editable Object", "Chỉnh sửa bán phần"],
                    ["Tốc độ xuất file toàn khóa", "12 - 15 phút", "< 25 giây (Thời gian thực)", "3 - 5 phút"],
                    ["Kiểm định chất lượng", "Thủ công 1 bước", "16 Tác Tử Hội Đồng MACC", "Quy tắc tĩnh cơ bản"],
                    ["Độ phong phú thị giác", "5 bố cục cơ bản", "30 Archetypes Chuẩn Quốc Tế", "10 - 12 mẫu cố định"]
                ]
            }
        },
        # Slide 3: TABLE_SCORECARD
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "THƯ VIỆN BẢNG BIỂU NATIVE",
            "assertion_title": "Thẻ Điểm Rủi Ro & Đánh Giá Tiến Độ Dự Án: Trực Quan Hóa Heatmap",
            "primary_claim": "Phân tầng màu sắc trạng thái giúp lãnh đạo nhận diện ngay điểm nghẽn.",
            "visual_job": "TABLE_SCORECARD",
            "table_data": {
                "headers": ["Hạng Mục Chiến Lược", "Mục Tiêu Q3", "Thực Tế", "Mức Rủi Ro", "Trạng Thái"],
                "rows": [
                    ["Tự động hóa báo cáo số liệu", "90% quy trình", "94.2% hoàn thành", "Thấp", "ĐẠT CHUẨN"],
                    ["Tích hợp Native Chart Excel", "8 loại biểu đồ", "8/8 loại (100%)", "Rất thấp", "XUẤT SẮC"],
                    ["Triển khai đào tạo nội bộ", "100% nhân sự", "65.0% hoàn thành", "Trung bình", "CẦN TĂNG TỐC"],
                    ["Kiểm thử tải đồng thời", "500 phiên/giây", "320 phiên/giây", "Cao", "CẢNH BÁO"]
                ]
            }
        },
        # Slide 4: FRAMEWORK_MATRIX_2X2
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Ma Trận Chiến Lược 2x2: Phân Bổ Nguồn Lực & Ưu Tiên Hành Động",
            "primary_claim": "Gartner Magic Quadrant & BCG Matrix giúp định vị rõ ràng các sáng kiến đột phá.",
            "visual_job": "FRAMEWORK_MATRIX_2X2",
            "matrix_data": {
                "axis_x": "Mức Độ Khả Thi Kỹ Thuật →",
                "axis_y": "Giá Trị Tác Động Chiến Lược →",
                "quadrants": [
                    {"title": "ĐỔI MỚI ĐỘT PHÁ (STRATEGIC BETS)", "desc": "Tác động rất lớn, cần đầu tư R&D sâu về thuật toán AI.", "highlight": False},
                    {"title": "ƯU TIÊN HÀNG ĐẦU (QUICK WINS)", "desc": "Khả thi cao, tác động tức thì. Tập trung toàn lực thực thi.", "highlight": True},
                    {"title": "CÂN NHẮC LOẠI BỎ (TIME SINKS)", "desc": "Khả thi thấp, giá trị thấp. Cắt giảm để tối ưu ngân sách.", "highlight": False},
                    {"title": "DUY TRÌ NỀN TẢNG (FILL-INS)", "desc": "Khả thi cao, tác động trung bình. Thực hiện theo tiến độ chuẩn.", "highlight": False}
                ]
            }
        },
        # Slide 5: FRAMEWORK_STRATEGY_HOUSE
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Ngôi Nhà Chiến Lược: Tầm Nhìn, Cột Trụ Và Nền Móng Vững Chắc",
            "primary_claim": "Kiến trúc Strategy House thể hiện trọn vẹn bức tranh phát triển toàn diện của tổ chức.",
            "visual_job": "FRAMEWORK_STRATEGY_HOUSE",
            "house_data": {
                "roof": "TẦM NHÌN 2030: HỆ SINH THÁI TỰ ĐỘNG HÓA THUYẾT TRÌNH THÔNG MINH SỐ 1 VIỆT NAM",
                "pillars": [
                    {"title": "Trụ Cột 1: Công Nghệ Lõi", "desc": "Kiến trúc 16 tác tử MACC & Native COM Automation trực tiếp."},
                    {"title": "Trụ Cột 2: Trải Nghiệm Đỉnh Cao", "desc": "30 Archetypes chuẩn quốc tế, hiệu ứng chuyển động mượt mà."},
                    {"title": "Trụ Cột 3: Khả Năng Tùy Biến", "desc": "Tất cả thành phần đều là Native Object, sửa được 100% trong Excel."}
                ],
                "foundation": "NỀN MÓNG CỐT LÕI: DỮ LIỆU ĐÁNG TIN CẬY - BẢO MẬT ZERO-TRUST - SỰ CHỈN CHU TUYỆT ĐỐI"
            }
        },
        # Slide 6: FRAMEWORK_FUNNEL
        {
            "slide_id": "SLIDE_06",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Mô Hình Phễu Chuyển Đổi: Tối Ưu Hóa Từng Khâu Trong Hành Trình",
            "primary_claim": "Mỗi nấc thang chuyển đổi đều đo lường tỷ lệ giữ chân và giá trị tạo ra.",
            "visual_job": "FRAMEWORK_FUNNEL",
            "funnel_data": [
                {"stage": "TIẾP CẬN TÀI LIỆU", "metric": "500,000+", "rate": "100%", "desc": "Nguồn tài liệu học tập và báo cáo nghiên cứu nhập môn"},
                {"stage": "BÓC TÁCH NỘI DUNG", "metric": "120,000", "rate": "24.0%", "desc": "Trích xuất cấu trúc ngữ nghĩa và bảng số liệu thực chứng"},
                {"stage": "TẠO BLUEPRINT BÀI HỌC", "metric": "24,000", "rate": "4.8%", "desc": "Tự động phân bổ archetype và bố cục thị giác tối ưu"},
                {"stage": "XUẤT BẢN SLIDE NATIVE", "metric": "5,000", "rate": "1.0%", "desc": "Sinh file PPTX hoàn chỉnh chất lượng giám đốc điều hành"}
            ]
        },
        # Slide 7: FRAMEWORK_ROADMAP_GANTT
        {
            "slide_id": "SLIDE_07",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Lộ Trình 3 Chân Trời Tăng Trưởng: Định Hướng Tương Lai Bền Vững",
            "primary_claim": "Quy hoạch các giai đoạn phát triển rõ ràng từ cốt lõi đến mở rộng và đột phá.",
            "visual_job": "FRAMEWORK_ROADMAP_GANTT",
            "horizons": [
                {"phase": "CHÂN TRỜI 1: TỐI ƯU CỐT LÕI (2024)", "tag": "HOÀN THÀNH 100%", "items": ["Xây dựng kho 30 Archetypes quốc tế", "Hỗ trợ 100% Native Table & Chart", "Vận hành 16 tác tử MACC tự sửa lỗi"]},
                {"phase": "CHÂN TRỜI 2: MỞ RỘNG ĐA NỀN TẢNG (2025)", "tag": "ĐANG THỰC HIỆN", "items": ["Phát hành Web SaaS Studio thời gian thực", "Tích hợp Generative AI đa ngôn ngữ", "Hợp tác mạng lưới giáo dục quốc gia"]},
                {"phase": "CHÂN TRỜI 3: HỆ SINH THÁI THÔNG MINH (2026)", "tag": "ĐỊNH HƯỚNG", "items": ["Autonomous AI Presentation Agent", "Liên thông hệ thống báo cáo chính phủ", "Mở rộng thị trường Đông Nam Á"]}
            ]
        },
        # Slide 8: CHART_DONUT_KPI
        {
            "slide_id": "SLIDE_08",
            "role": "CONTENT",
            "section": "BIỂU ĐỒ OFFICE GỐC (NATIVE CHARTS)",
            "assertion_title": "Cơ Cấu Dân Số Theo 6 Vùng Kinh Tế: Biểu Đồ Vành Khuyên Native",
            "primary_claim": "Click đúp vào biểu đồ để mở Excel sửa số liệu trực tiếp trong PowerPoint.",
            "visual_job": "CHART_DONUT_KPI",
            "chart_data": {
                "categories": ["Đồng Bằng Sông Hồng", "Đông Nam Bộ", "ĐBSCL", "Bắc Trung Bộ & DHMT", "Trung Du & Miền Núi", "Tây Nguyên"],
                "series": [{"name": "Dân Số (Triệu Người)", "values": [23.4, 18.8, 17.5, 20.6, 13.9, 6.1]}],
                "center_metric": "100.3 Tr",
                "center_label": "Tổng Dân Số VN"
            }
        },
        # Slide 9: CONTAINER_KPI_STAT_DELTA
        {
            "slide_id": "SLIDE_09",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA CAO CẤP",
            "assertion_title": "Chỉ Số Trọng Yếu Đạt Được: Thẻ Số Liệu Kèm Chip Tăng Trưởng",
            "primary_claim": "Thiết kế hiện đại phong cách Apple Keynote tôn vinh những thành tựu vượt bậc.",
            "visual_job": "CONTAINER_KPI_STAT_DELTA",
            "kpi_stats": [
                {"metric": "100.3 Tr", "delta": "+0.84% YoY", "is_positive": True, "label": "Quy Mô Dân Số", "desc": "Cột mốc lịch sử đạt 100 triệu người"},
                {"metric": "1.96", "delta": "-7.1% vs Chuẩn", "is_positive": False, "label": "Mức Sinh (TFR)", "desc": "Dưới mức sinh thay thế 2.10 con"},
                {"metric": "42.5%", "delta": "+1.8% YoY", "is_positive": True, "label": "Tỷ Lệ Đô Thị Hóa", "desc": "Động lực phát triển kinh tế vùng"}
            ]
        },
        # Slide 10: CONTAINER_BEFORE_AFTER
        {
            "slide_id": "SLIDE_10",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA CAO CẤP",
            "assertion_title": "So Sánh Tương Phản Trước & Sau Khi Nâng Cấp Kho Thư Viện",
            "primary_claim": "Sự chuyển dịch từ các khối hình đơn điệu sang hệ sinh thái thị giác chuyên nghiệp.",
            "visual_job": "CONTAINER_BEFORE_AFTER",
            "contrast_data": {
                "before_title": "PHIÊN BẢN CŨ (TRƯỚC NÂNG CẤP)",
                "before_items": [
                    "Chỉ có 5 layout cơ bản (Card, Bento 3 ô, So sánh, Quy trình, Lưới)",
                    "Biểu đồ xuất ra dạng ảnh raster PNG, không thể sửa số liệu",
                    "Bảng biểu đôi khi bị dispatch nhầm thành layout ảnh tĩnh",
                    "Hình khối đơn điệu, lặp đi lặp lại giữa các bài giảng"
                ],
                "after_title": "PHIÊN BẢN V8.4.0 (HIỆN TẠI)",
                "after_items": [
                    "Kho thư viện 30 Archetypes chuẩn quốc tế (McKinsey, BCG, Apple)",
                    "100% Native Office Charts với bảng tính Excel nhúng có thể sửa trực tiếp",
                    "Toàn bộ bảng biểu là Native PowerPoint Table chỉnh sửa tự do từng ô",
                    "Hỗ trợ 10 mô hình chiến lược (2x2 Matrix, Funnel, Value Chain, House, Flywheel)"
                ]
            }
        },
        # Slide 11: CONTAINER_EXECUTIVE_QUOTE
        {
            "slide_id": "SLIDE_11",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA CAO CẤP",
            "assertion_title": "Thông Điệp Lãnh Đạo: Tuyên Ngôn Về Đổi Mới Sáng Tạo & Tinh Thần Chỉn Chu",
            "primary_claim": "Khối trích dẫn phong cách báo chí New York Times mang lại cảm xúc lắng đọng.",
            "visual_job": "CONTAINER_EXECUTIVE_QUOTE",
            "quote_data": {
                "quote": "Sự hoàn hảo không đến từ những điều phức tạp, mà đến từ sự chỉn chu tuyệt đối trong từng đường nét, từng bảng số liệu và từng mô hình thị giác trao đến tay người dùng.",
                "author": "ĐỘI NGŨ PHÁT TRIỂN MAKE SLIDE PRO",
                "title": "Kiến Trúc Sư Trưởng Hệ Thống"
            }
        },
        # Slide 12: PROCESS_CHEVRON_LINEAR
        {
            "slide_id": "SLIDE_12",
            "role": "CONTENT",
            "section": "SƠ ĐỒ QUY TRÌNH & DÒNG CHẢY",
            "assertion_title": "Quy Trình 5 Bước Mũi Tên Vát Chevron: Liền Mạch & Rõ Ràng",
            "primary_claim": "Mỗi bước thể hiện rõ thứ tự thời gian và nhiệm vụ hành động trọng tâm.",
            "visual_job": "PROCESS_CHEVRON_LINEAR",
            "process_data": {
                "steps": [
                    {"step": "01", "title": "Khảo Sát Hiện Trạng", "desc": "Thu thập dữ liệu thực địa, phỏng vấn chuyên sâu các phòng ban."},
                    {"step": "02", "title": "Phân Tích Khoảng Trống", "desc": "Xác định điểm nghẽn quy trình và định lượng tổn thất."},
                    {"step": "03", "title": "Thiết Kế Kiến Trúc", "desc": "Mô hình hóa giải pháp số hóa thế hệ mới chuẩn quốc tế."},
                    {"step": "04", "title": "Triển Khai & Kiểm Thử", "desc": "Thiết lập Sandbox, chạy thử nghiệm pilot 30 ngày."},
                    {"step": "05", "title": "Bàn Giao & Mở Rộng", "desc": "Đào tạo nhân sự toàn diện và bàn giao tài liệu kỹ thuật."}
                ]
            }
        },
        # Slide 13: PROCESS_FISHBONE_ISHIKAWA
        {
            "slide_id": "SLIDE_13",
            "role": "CONTENT",
            "section": "SƠ ĐỒ QUY TRÌNH & DÒNG CHẢY",
            "assertion_title": "Biểu Đồ Xương Cá Ishikawa: Truy Cứu Căn Nguyên & Giải Pháp",
            "primary_claim": "Phân nhóm 4 chiều: Con người, Quy trình, Công nghệ và Chính sách.",
            "visual_job": "PROCESS_FISHBONE_ISHIKAWA",
            "process_data": {
                "effect": "TỶ LỆ RỚT HỌC VIÊN\nCAO HƠN MỤC TIÊU",
                "causes": [
                    {"cat": "CON NGƯỜI (PEOPLE)", "items": "• Thiếu tương tác giảng viên\n• Học viên chưa có nền tảng"},
                    {"cat": "QUY TRÌNH (PROCESS)", "items": "• Lịch học quá dày đặc\n• Thiếu bài tập thực hành"},
                    {"cat": "CÔNG NGHỆ (TECH)", "items": "• Nền tảng LMS bị giật lag\n• Slide bài giảng đơn điệu"},
                    {"cat": "CHÍNH SÁCH (POLICY)", "items": "• Thiếu chứng chỉ hoàn thành\n• Chưa có học bổng động viên"}
                ]
            }
        },
        # Slide 14: ARCH_SYSTEM_LAYERED_STACK
        {
            "slide_id": "SLIDE_14",
            "role": "CONTENT",
            "section": "KIẾN TRÚC HỆ THỐNG & PHÂN TẦNG",
            "assertion_title": "Kiến Trúc Phân Tầng Hệ Thống Make Slide Pro: Tách Biệt & Bền Vững",
            "primary_claim": "4 tầng độc lập bảo đảm khả năng mở rộng hàng triệu người dùng đồng thời.",
            "visual_job": "ARCH_SYSTEM_LAYERED_STACK",
            "arch_data": {
                "layers": [
                    {"tier": "TẦNG 1: TRÌNH DIỄN (CLIENT)", "tech": "React, Next.js, Desktop COM UI", "desc": "Giao diện mượt mà, phản hồi tức thời."},
                    {"tier": "TẦNG 2: CỔNG ĐIỀU HƯỚNG (API GATEWAY)", "tech": "FastAPI, Envoy, OAuth2", "desc": "Xác thực bảo mật, cân bằng tải thông minh."},
                    {"tier": "TẦNG 3: ĐIỀU PHỐI AI (MICROSERVICES)", "tech": "16 MACC Agents, Gemini 2.5 Pro", "desc": "Phân tích ngữ nghĩa, tự sửa lỗi đa tác tử."},
                    {"tier": "TẦNG 4: HẠ TẦNG DỮ LIỆU (DATA LAKE)", "tech": "BigQuery, SQLite, Office COM Engine", "desc": "Lưu trữ bền vững, xuất bản PPTX siêu tốc."}
                ]
            }
        },
        # Slide 15: ARCH_MICROSERVICES_MESH
        {
            "slide_id": "SLIDE_15",
            "role": "CONTENT",
            "section": "KIẾN TRÚC HỆ THỐNG & PHÂN TẦNG",
            "assertion_title": "Mạng Lưới Dịch Vụ Microservices: Tự Chủ & Tương Hỗ Chặt Chẽ",
            "primary_claim": "Các cụm dịch vụ giao tiếp qua gRPC tốc độ cao, độc lập triển khai.",
            "visual_job": "ARCH_MICROSERVICES_MESH",
            "arch_data": {
                "services": [
                    {"name": "Auth & SaaS Service", "proto": "OAuth2 / JWT", "scale": "Autoscale 3-10 Pods"},
                    {"name": "AI Reasoning Agent", "proto": "Gemini 2.5 Pro", "scale": "High GPU Quota"},
                    {"name": "PowerPoint COM Worker", "proto": "Win32 Direct", "scale": "Dedicated Windows"},
                    {"name": "Billing Webhook", "proto": "Stripe Hook", "scale": "Zero-Downtime"},
                    {"name": "Telemetry Engine", "proto": "OpenTelemetry", "scale": "Elastic Logs"},
                    {"name": "Asset CDN Storage", "proto": "Cloud Storage", "scale": "Global Edge"}
                ]
            }
        },
        # Slide 16: CHART_COLUMN_100_STACKED
        {
            "slide_id": "SLIDE_16",
            "role": "CONTENT",
            "section": "BIỂU ĐỒ OFFICE GỐC (NATIVE CHARTS)",
            "assertion_title": "Cơ Cấu Tỷ Trọng Doanh Thu 100%: Biểu Đồ Cột Chồng Native",
            "primary_claim": "Phân tích chuyển dịch mô hình kinh doanh từ dịch vụ sang SaaS định kỳ.",
            "visual_job": "CHART_COLUMN_100_STACKED",
            "chart_data": {
                "categories": ["2021", "2022", "2023", "2024", "2025 (F)"],
                "series": [
                    {"name": "Doanh Thu SaaS ARR (%)", "values": [35, 48, 62, 74, 85]},
                    {"name": "Dịch Vụ Tư Vấn Chuyên Sâu (%)", "values": [45, 38, 26, 18, 10]},
                    {"name": "Bản Quyền Triển Khai (%)", "values": [20, 14, 12, 8, 5]}
                ]
            }
        },
        # Slide 17: CHART_RADAR
        {
            "slide_id": "SLIDE_17",
            "role": "CONTENT",
            "section": "BIỂU ĐỒ OFFICE GỐC (NATIVE CHARTS)",
            "assertion_title": "Đánh Giá Năng Lực Cạnh Tranh: Biểu Đồ Mạng Nhện Native Radar",
            "primary_claim": "So sánh 6 chiều năng lực cốt lõi giữa hiện trạng thực tế và mục tiêu chuẩn.",
            "visual_job": "CHART_RADAR",
            "chart_data": {
                "categories": ["Hạ Tầng Số", "Năng Lực AI", "An Ninh Mạng", "Văn Hóa Đổi Mới", "Tối Ưu Quy Trình", "Khai Thác Dữ Liệu"],
                "series": [
                    {"name": "Hiện Trạng Thực Tế", "values": [65, 45, 80, 55, 70, 60]},
                    {"name": "Mục Tiêu Năm 2025", "values": [90, 85, 95, 85, 90, 95]}
                ]
            }
        },
        # Slide 18: CONTAINER_BENTO_GRID_3X3
        {
            "slide_id": "SLIDE_18",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA CAO CẤP",
            "assertion_title": "Hệ Tính Năng Toàn Diện: Lưới Bento Modular 9 Ô Phong Cách Apple",
            "primary_claim": "Phân bổ 9 giá trị then chốt trong bố cục ô vuông cân đối và tinh tế.",
            "visual_job": "CONTAINER_BENTO_GRID_3X3"
        },
        # Slide 19: CONTAINER_EXECUTIVE_DASHBOARD
        {
            "slide_id": "SLIDE_19",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA CAO CẤP",
            "assertion_title": "Bảng Điều Khiển Giám Đốc Điều Hành: Khẳng Định Then Chốt & KPI Lớn",
            "primary_claim": "Tích hợp tiêu đề hành động to bản cùng 3 chỉ số đo lường tăng trưởng vượt trội.",
            "visual_job": "CONTAINER_EXECUTIVE_DASHBOARD"
        },
        # Slide 20: Closing
        {
            "slide_id": "SLIDE_20",
            "role": "COVER",
            "assertion_title": "HOÀN TẤT TRÌNH DIỄN KHO THƯ VIỆN MEGA 110+ ARCHETYPES V8.5.0",
            "primary_claim": "Hệ sinh thái thị giác đỉnh cao: 100% Native Tables, Charts, Frameworks & Containers.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Xin trân trọng cảm ơn quý vị đã theo dõi buổi trình diễn kho thư viện Mega 110+ Archetypes."
        }
    ]

    blueprints_data = {
        "schema_version": "1.0",
        "lesson_index": 1,
        "deck_title": "Make Slide Pro Master Showcase",
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }

    with open(blueprints_file, "w", encoding="utf-8") as f:
        json.dump(blueprints_data, f, ensure_ascii=False, indent=2)

    print(f"Blueprints saved to {blueprints_file}")

    author = NativeDeckAuthor(visible=True, theme="DARK", motion_mode="presenter_click")
    try:
        author.create_deck(blueprints_file, output_pptx)
        print(f"MASTER SHOWCASE DECK CREATED SUCCESSFULLY: {output_pptx}")
    finally:
        author.close()

if __name__ == "__main__":
    create_showcase_deck()
