"""
generate_master_showcase.py
Generates a comprehensive demonstration PowerPoint deck showcasing
the elite presentation archetypes of Make Slide Pro V8.6.0 with Apple Motion Engine.
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
        # Slide 1: Cover (Cinematic Smooth Fade)
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "assertion_title": "MAKE SLIDE PRO V8.6.0: KHO THƯ VIỆN MEGA 165+ ARCHETYPES & APPLE MOTION",
            "primary_claim": "Chuẩn hóa dựa trên phân tích 1,000 template slide hàng đầu thế giới (McKinsey, BCG, Apple Keynote, YC Pitch Decks).",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Kính chào quý vị, đây là bản trình diễn kho thư viện 165+ thành phần thị giác cao cấp hoàn toàn có thể chỉnh sửa trực tiếp trong PowerPoint."
        },
        # Slide 2: TABLE_PRICING_FEATURE_MATRIX (Native Office Table)
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "THƯ VIỆN BẢNG BIỂU NATIVE",
            "assertion_title": "Ma Trận Tính Năng 4 Gói Dịch Vụ SaaS: Minh Bạch & Tối Ưu Tỷ Lệ Chuyển Đổi",
            "primary_claim": "Bảng Native PowerPoint cho phép chỉnh sửa từng ô, thêm dòng cột và đổi màu tự do.",
            "visual_job": "TABLE_PRICING_FEATURE_MATRIX"
        },
        # Slide 3: TABLE_RISK_HEATMAP_5X5 (Native Heatmap Matrix Table)
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "THƯ VIỆN BẢNG BIỂU NATIVE",
            "assertion_title": "Ma Trận Nhiệt Rủi Ro 5x5 Chuẩn Quốc Tế: Định Lượng Mức Độ Tác Động",
            "primary_claim": "Phân tầng trực quan xác suất và mức độ thiệt hại giúp ban điều hành ứng phó kịp thời.",
            "visual_job": "TABLE_RISK_HEATMAP_5X5"
        },
        # Slide 4: FRAMEWORK_STEEPLE (Strategic Framework)
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Mô Hình STEEPLE: Phân Tích Toàn Diện 7 Yếu Tố Môi Trường Vĩ Mô",
            "primary_claim": "Đánh giá đa chiều Xã hội, Công nghệ, Kinh tế, Môi trường, Chính trị, Pháp lý và Đạo đức.",
            "visual_job": "FRAMEWORK_STEEPLE"
        },
        # Slide 5: FRAMEWORK_VALUE_PROPOSITION_CANVAS
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Khung Đề Xuất Giá Trị Osterwalder: Đồng Bộ Nỗi Đau & Giải Pháp Đột Phá",
            "primary_claim": "Kết nối chính xác hồ sơ khách hàng với bản đồ giá trị sản phẩm để tạo lợi thế vượt trội.",
            "visual_job": "FRAMEWORK_VALUE_PROPOSITION_CANVAS"
        },
        # Slide 6: FRAMEWORK_STRATEGY_HOUSE
        {
            "slide_id": "SLIDE_06",
            "role": "CONTENT",
            "section": "MÔ HÌNH CHIẾN LƯỢC KINH ĐIỂN",
            "assertion_title": "Ngôi Nhà Chiến Lược 2030: Tầm Nhìn, Cột Trụ Và Nền Móng Vững Chắc",
            "primary_claim": "Kiến trúc Strategy House thể hiện trọn vẹn bức tranh phát triển toàn diện của tổ chức.",
            "visual_job": "FRAMEWORK_STRATEGY_HOUSE",
            "house_data": {
                "roof": "TẦM NHÌN 2030: HỆ SINH THÁI TỰ ĐỘNG HÓA THUYẾT TRÌNH THÔNG MINH SỐ 1 VIỆT NAM",
                "pillars": [
                    {"title": "Trụ Cột 1: Công Nghệ Lõi", "desc": "Kiến trúc 16 tác tử MACC & Native COM Automation trực tiếp."},
                    {"title": "Trụ Cột 2: Thư Viện Mega", "desc": "165+ Archetypes chuẩn thế giới, 100% Native Editable."},
                    {"title": "Trụ Cột 3: Apple Motion", "desc": "Chuyển động Magic Morph và Staggered Entrance mượt mà."},
                    {"title": "Trụ Cột 4: Trải Nghiệm Khách Hàng", "desc": "Giao diện Web Studio SaaS hiện đại, phản hồi tức thì."}
                ],
                "foundation": "NỀN TẢNG VỮNG CHẮC: CƠ SỞ DỮ LIỆU ĐỒNG BỘ • AN NINH ZERO TRUST • VĂN HÓA ĐỔI MỚI"
            }
        },
        # Slide 7: PROCESS_DEVSECOPS_INFINITY_LOOP
        {
            "slide_id": "SLIDE_07",
            "role": "CONTENT",
            "section": "QUY TRÌNH & TIẾN ĐỘ THỜI GIAN",
            "assertion_title": "Chu Trình Vòng Lặp Vô Cực DevSecOps: Bảo Mật Xuyên Suốt Mọi Giai Đoạn",
            "primary_claim": "Tích hợp kiểm thử an ninh tự động từ phát triển, kiểm thử tới vận hành sản xuất.",
            "visual_job": "PROCESS_DEVSECOPS_INFINITY_LOOP"
        },
        # Slide 8: PROCESS_CRITICAL_PATH_CPM
        {
            "slide_id": "SLIDE_08",
            "role": "CONTENT",
            "section": "QUY TRÌNH & TIẾN ĐỘ THỜI GIAN",
            "assertion_title": "Phương Pháp Đường Găng (Critical Path CPM): Quản Trị Chuỗi Nhiệm Vụ",
            "primary_claim": "Xác định chính xác thời gian tối thiểu hoàn thành dự án và các điểm chốt trọng yếu.",
            "visual_job": "PROCESS_CRITICAL_PATH_CPM"
        },
        # Slide 9: ARCH_DATA_LAKEHOUSE_MEDALLION
        {
            "slide_id": "SLIDE_09",
            "role": "CONTENT",
            "section": "SƠ ĐỒ HỆ THỐNG & KIẾN TRÚC",
            "assertion_title": "Kiến Trúc Hồ Dữ Liệu Lakehouse Medallion: Bronze - Silver - Gold",
            "primary_claim": "Tinh chế dữ liệu từ dạng thô sơ cấp đến mô hình tổng hợp kinh doanh chuẩn xác.",
            "visual_job": "ARCH_DATA_LAKEHOUSE_MEDALLION"
        },
        # Slide 10: ARCH_RAG_LLM_PIPELINE
        {
            "slide_id": "SLIDE_10",
            "role": "CONTENT",
            "section": "SƠ ĐỒ HỆ THỐNG & KIẾN TRÚC",
            "assertion_title": "Đường Ống Truy Xuất Thông Tin RAG AI: Nâng Cao Độ Chuẩn Xác Tri Thức",
            "primary_claim": "Kết hợp Vector Database, Hybrid Search và LLM Sinh Câu Trả Lời có kiểm chứng nguồn.",
            "visual_job": "ARCH_RAG_LLM_PIPELINE"
        },
        # Slide 11: CHART_PARETO_ANALYSIS (Office Chart)
        {
            "slide_id": "SLIDE_11",
            "role": "CONTENT",
            "section": "BIỂU ĐỒ MICROSOFT OFFICE NATIVE",
            "assertion_title": "Biểu Đồ Phân Tích Pareto 80/20: Tập Trung Giải Quyết Các Nguyên Nhân Gốc Rễ",
            "primary_claim": "Biểu đồ Native PowerPoint kết nối Excel Worksheet cho phép người dùng click sửa số liệu.",
            "visual_job": "CHART_PARETO_ANALYSIS"
        },
        # Slide 12: CHART_RADAR_FILLED (Office Chart)
        {
            "slide_id": "SLIDE_12",
            "role": "CONTENT",
            "section": "BIỂU ĐỒ MICROSOFT OFFICE NATIVE",
            "assertion_title": "Biểu Đồ Radar Đa Trục Lấp Đầy: Đánh Giá Năng Lực Cạnh Tranh Toàn Diện",
            "primary_claim": "So sánh trực quan hiện trạng với mục tiêu trên 6 trục tiêu chí cốt lõi.",
            "visual_job": "CHART_RADAR_FILLED"
        },
        # Slide 13: CHART_HISTOGRAM_DISTRIBUTION (Office Chart)
        {
            "slide_id": "SLIDE_13",
            "role": "CONTENT",
            "section": "BIỂU ĐỒ MICROSOFT OFFICE NATIVE",
            "assertion_title": "Biểu Đồ Phân Phối Tần Suất Histogram: Nhận Diện Quy Luật Dữ Liệu Lớn",
            "primary_claim": "Trực quan hóa sự phân bổ tần suất để đưa ra các quyết định định lượng chính xác.",
            "visual_job": "CHART_HISTOGRAM_DISTRIBUTION"
        },
        # Slide 14: CONTAINER_DEVICE_MOCKUP_FRAME
        {
            "slide_id": "SLIDE_14",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA APPLE KEYNOTE",
            "assertion_title": "Khung Thiết Bị Mockup Tinh Tế: Tôn Vinh Giao Diện Ứng Dụng Đỉnh Cao",
            "primary_claim": "Mô phỏng màn hình thiết bị hiện đại phong cách Apple với điểm nhấn kỹ thuật sắc nét.",
            "visual_job": "CONTAINER_DEVICE_MOCKUP_FRAME"
        },
        # Slide 15: CONTAINER_METRIC_MARQUEE_BANNER
        {
            "slide_id": "SLIDE_15",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA APPLE KEYNOTE",
            "assertion_title": "Dải Marquee Banner 4 Chỉ Số: Tạo Tác Động Thị Giác Mạnh Mẽ Tức Thì",
            "primary_claim": "4 thẻ chỉ số nổi bật với huy hiệu tăng trưởng YoY mang phong cách thuyết trình quốc tế.",
            "visual_job": "CONTAINER_METRIC_MARQUEE_BANNER"
        },
        # Slide 16: CONTAINER_THREE_PILLARS_CARDS
        {
            "slide_id": "SLIDE_16",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA APPLE KEYNOTE",
            "assertion_title": "3 Trụ Cột Kính Mờ: Bố Cục Thẻ Hiện Đại Đẳng Cấp Thẩm Mỹ Tối Đa",
            "primary_claim": "Chia đều không gian 3 cột chuẩn mực, viền tương phản cao và nhịp độ thị giác rõ ràng.",
            "visual_job": "CONTAINER_THREE_PILLARS_CARDS"
        },
        # Slide 17: CONTAINER_PROBLEM_SOLUTION_IMPACT
        {
            "slide_id": "SLIDE_17",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA APPLE KEYNOTE",
            "assertion_title": "Chuỗi Vấn Đề - Giải Pháp Đột Phá - Tác Động: Mạch Dẫn Dắt Thuyết Phục",
            "primary_claim": "Khắc họa sâu sắc nỗi đau khách hàng, đề xuất giải pháp vượt trội và đo lường thành quả.",
            "visual_job": "CONTAINER_PROBLEM_SOLUTION_IMPACT"
        },
        # Slide 18: CONTAINER_MINIMALIST_APPLE_QUOTE
        {
            "slide_id": "SLIDE_18",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA APPLE KEYNOTE",
            "assertion_title": "Châm Ngôn Tối Giản Apple Keynote: Lắng Đọng Cảm Xúc & Định Hình Tư Duy",
            "primary_claim": "Không gian thở rộng lớn, kiểu chữ thanh thoát và điểm nhấn thương hiệu sang trọng.",
            "visual_job": "CONTAINER_MINIMALIST_APPLE_QUOTE"
        },
        # Slide 19: CONTAINER_EXECUTIVE_DASHBOARD
        {
            "slide_id": "SLIDE_19",
            "role": "CONTENT",
            "section": "KHỐI ĐỒ HỌA APPLE KEYNOTE",
            "assertion_title": "Bảng Điều Khiển Giám Đốc Điều Hành: Khẳng Định Then Chốt & KPI Lớn",
            "primary_claim": "Tích hợp tiêu đề hành động to bản cùng 3 chỉ số đo lường tăng trưởng vượt trội.",
            "visual_job": "CONTAINER_EXECUTIVE_DASHBOARD"
        },
        # Slide 20: Closing
        {
            "slide_id": "SLIDE_20",
            "role": "COVER",
            "assertion_title": "HOÀN TẤT TRÌNH DIỄN KHO THƯ VIỆN MEGA 165+ ARCHETYPES & APPLE MOTION V8.6.0",
            "primary_claim": "Hệ sinh thái thị giác đỉnh cao: 100% Native Tables, Charts, Frameworks & Containers.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Xin trân trọng cảm ơn quý vị đã theo dõi buổi trình diễn kho thư viện Mega 165+ Archetypes."
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
