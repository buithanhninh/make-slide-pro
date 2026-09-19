"""
blueprint_generator.py
Synthesizes canonical content into certified slide blueprints with assertion titles,
vector icon assignments, high-resolution demographic charts, editorial AI illustrations,
and bento grid structures.
Supports all 5 demographic course modules and dynamic generic documents.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from content_multi_agent_council import ContentMultiAgentCouncil
except ImportError:
    try:
        from scripts.content_multi_agent_council import ContentMultiAgentCouncil
    except ImportError:
        ContentMultiAgentCouncil = None


def extract_pedagogical_sentence(text: str, max_words: int = 32) -> str:
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return ""
    # Strip leading numbering like '1. ', '2.3 ', 'a) '
    cleaned = re.sub(r"^(\d+[\.\:\)\-]?|[a-zA-Z][\.\)\-])\s*", "", cleaned).strip()
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    valid_sentences = [s.strip() for s in sentences if s.strip()]
    if valid_sentences:
        res = valid_sentences[0]
        for next_s in valid_sentences[1:]:
            cand = res + " " + next_s
            if len(cand.split()) <= max_words:
                res = cand
            else:
                break
        if len(res.split()) >= 4:
            if not res.endswith((".", "!", "?")):
                res += "."
            return res
    words = cleaned.split()[:max_words]
    res = " ".join(words).strip()
    if not res.endswith((".", "!", "?")):
        res += "."
    return res


def clean_summary(text: str, max_words: int = 25) -> str:
    return extract_pedagogical_sentence(text, max_words)


def clean_title(text: str, max_words: int = 16) -> str:
    cleaned = re.sub(r"^(\d+[\.\:\)\-]?|[a-zA-Z][\.\)\-])\s*", "", text.strip())
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return ""
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned.rstrip(".!?:; -–—").strip()
    truncated = " ".join(words[:max_words]).rstrip(",.!?:; -–—").strip()
    return truncated


def get_lesson_blueprints_bai_1() -> Dict[str, Any]:
    slides = [
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "section": "TỔNG QUAN CHUYÊN ĐỀ",
            "assertion_title": "BÀI I: NHẬP MÔN DÂN SỐ HỌC",
            "primary_claim": "Khung lý thuyết nền tảng về quy mô, cơ cấu, chất lượng và phương pháp luận nghiên cứu Dân số học hiện đại.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Kính chào quý học viên, hôm nay chúng ta bắt đầu chuyên đề Nhập môn Dân số học nhằm nắm vững các khái niệm và nguyên lý vận động của dân số.",
            "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
        },
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "MỤC TIÊU BÀI HỌC",
            "assertion_title": "Nắm Vững Khái Niệm Cốt Lõi Và Phương Pháp Luận Nghiên Cứu Dân Số Học",
            "primary_claim": "MỤC TIÊU: Sau khi học xong bài này học viên có khả năng nắm vững 2 năng lực cốt lõi: Nhận diện cấu trúc dân số và vận dụng phương pháp phân tích nhân quả.",
            "visual_job": "BENTO_GRID",
            "visual_anchor": "BENTO_OBJECTIVES",
            "atoms": [
                {
                    "title": "Chuẩn Đầu Ra & Năng Lực Cốt Lõi",
                    "text": "Trang bị hệ thống phương pháp luận nghiên cứu dân số học hiện đại phục vụ phân tích nhân quả, đánh giá quy luật hình thành, biến động và dự báo chính sách KT-XH bền vững.",
                    "icon": "target"
                },
                {
                    "title": "1. Năng Lực Khái Niệm",
                    "text": "Hiểu rõ và phân biệt rành mạch giữa Dân cư và Dân số; nắm vững trạng thái tĩnh và trạng thái động trong nghiên cứu nhân khẩu học.",
                    "icon": "book-open"
                },
                {
                    "title": "2. Năng Lực Phương Pháp",
                    "text": "Trình bày chính xác đối tượng, phạm vi và phương pháp luận nghiên cứu dân số học phục vụ dự báo và hoạch định chính sách quốc gia.",
                    "icon": "calculator"
                }
            ],
            "speaker_notes": "Mục tiêu bài giảng yêu cầu người học phân biệt rành mạch giữa dân cư và dân số, từ đó vận dụng phương pháp nghiên cứu chính xác.",
            "source_footer": "Khung chuẩn đầu ra chuyên đề"
        },
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "KHÁI NIỆM NỀN TẢNG",
            "assertion_title": "Khái Niệm Dân Cư Mang Tính Toàn Diện Hơn Nội Hàm Dân Số",
            "primary_claim": "Đối với Dân số thì thông tin được tìm hiểu đầu tiên là quy mô của dân cư; Dân cư bao trùm văn hóa, kinh tế, xã hội.",
            "visual_job": "EDITORIAL_HERO",
            "visual_anchor": "EDITORIAL_POPULATION_CONCEPT",
            "atoms": [
                {
                    "title": "Dân Cư (Khái Niệm Toàn Diện)",
                    "text": "Gồm toàn bộ con người cùng cư trú trên một lãnh thổ; xem xét dưới đa góc độ: Văn hóa, lịch sử, kinh tế, ẩm thực, tập quán và lối sống.",
                    "icon": "globe"
                },
                {
                    "title": "Dân Số (Nội Hàm Định Lượng)",
                    "text": "Đối với Dân số thì thông tin được tìm hiểu đầu tiên là quy mô, cơ cấu giới tính - độ tuổi, chất lượng và các thành tố sinh, chết, di cư.",
                    "icon": "users"
                },
                {
                    "title": "Ý Nghĩa Trong Hoạch Định",
                    "text": "Cung cấp bằng chứng định lượng chính xác phục vụ xây dựng kế hoạch phân bổ nguồn lực và chính sách an sinh xã hội bền vững.",
                    "icon": "file-check"
                }
            ],
            "speaker_notes": "Đối với Dân số thì thông tin được tìm hiểu đầu tiên là quy mô của dân cư. Cần lưu ý dân cư là khái niệm rộng hơn rất nhiều so với dân số.",
            "source_footer": "Giáo trình Dân số học đại cương"
        },
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "HỆ THỐNG TƯƠNG TÁC",
            "assertion_title": "Dân Số Vận Động Trong Mối Quan Hệ Tương Tác Đa Chiều Với Phát Triển",
            "primary_claim": "Dân số vừa là mục tiêu, vừa là động lực của sự phát triển; tương tác hữu cơ với kinh tế, xã hội, tài nguyên và chính sách quốc gia.",
            "visual_job": "CHART_AND_INSIGHTS",
            "visual_anchor": "SYSTEM_INTERACTION_CHART",
            "chart_type": "SYSTEM_INTERACTION",
            "atoms": [
                {
                    "title": "Trạng Thái Tĩnh & Động",
                    "text": "Điều tra tĩnh chụp lại quy mô, phân bố tại thời điểm; theo dõi động nắm bắt dòng chảy sinh, chết và di cư liên tục.",
                    "icon": "activity"
                },
                {
                    "title": "Động Lực Phát Triển Kinh Tế",
                    "text": "Cung cấp lực lượng lao động sản xuất, đồng thời là đối tượng thụ hưởng toàn bộ thành quả tăng trưởng quốc gia.",
                    "icon": "trending-up"
                },
                {
                    "title": "Cân Bằng Môi Trường Sống",
                    "text": "Mật độ và tốc độ tăng dân số quyết định trực tiếp áp lực lên tài nguyên đất đai, nguồn nước và hạ tầng xã hội.",
                    "icon": "layers"
                }
            ],
            "speaker_notes": "Sơ đồ ma trận tương tác làm rõ vị trí trung tâm của con người trong mối quan hệ với 4 trụ cột phát triển bền vững.",
            "source_footer": "Liên Hợp Quốc (UN 1958) & Dân số học Việt Nam"
        },
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "BẢN CHẤT KHOA HỌC",
            "assertion_title": "Dân Số Học Không Chỉ Mô Tả Hiện Tượng Mà Tìm Mối Quan Hệ Nhân Quả",
            "primary_claim": "Như vậy, có thể khái quát rằng Dân số học là một môn khoa học nghiên cứu quy mô, cơ cấu, phân bố, chất lượng và tìm mối quan hệ nhân quả.",
            "visual_job": "CARDS",
            "visual_anchor": "THREE_PILLARS",
            "atoms": [
                {
                    "title": "1. Bản Chất Khoa Học",
                    "text": "Như vậy, có thể khái quát rằng Dân số học là một môn khoa học nghiên cứu quy luật hình thành, biến động và tìm mối quan hệ nhân quả kinh tế - xã hội.",
                    "icon": "lightbulb"
                },
                {
                    "title": "2. Dự Báo Xu Hướng",
                    "text": "Xây dựng các kịch bản dân số nhằm chuẩn bị cơ sở hạ tầng, trường học, bệnh viện và hệ thống an sinh xã hội vững chắc.",
                    "icon": "chart-line"
                },
                {
                    "title": "3. Luận Cứ Chính Sách",
                    "text": "Cung cấp bằng chứng khoa học phục vụ chiến lược dân số, tận dụng cơ hội dân số vàng và thích ứng già hóa dân số.",
                    "icon": "file-check"
                }
            ],
            "speaker_notes": "Như vậy, có thể khái quát rằng Dân số học là một môn khoa học giữ vai trò then chốt trong việc hoạch định chính sách phát triển quốc gia dựa trên bằng chứng định lượng vững chắc.",
            "source_footer": "Liên Hợp Quốc (UN 1958) & Chiến lược Dân số Việt Nam"
        },
        {
            "slide_id": "SLIDE_06",
            "role": "COVER",
            "section": "TỔNG KẾT BÀI HỌC",
            "assertion_title": "Dân Số Là Trung Tâm Của Mọi Chiến Lược Phát Triển Kinh Tế - Xã Hội",
            "primary_claim": "Nắm vững quy luật dân số là điều kiện tiên quyết để xây dựng chính sách an sinh, lao động và tăng trưởng bền vững.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Cảm ơn quý học viên đã lắng nghe. Xin mời thảo luận và đặt câu hỏi cho chuyên đề Nhập môn Dân số học.",
            "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
        }
    ]
    return {
        "schema_version": "1.0",
        "lesson_index": 1,
        "deck_title": "Nhập Môn Dân Số Học",
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }


def get_lesson_blueprints_bai_2() -> Dict[str, Any]:
    slides = [
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "section": "TỔNG QUAN CHUYÊN ĐỀ",
            "assertion_title": "BÀI 2: QUY MÔ, CƠ CẤU VÀ CHẤT LƯỢNG DÂN SỐ",
            "primary_claim": "Hệ thống chỉ báo đo lường động lực học dân số, các mô hình tháp tuổi - giới tính và bài toán già hóa dân số tại Việt Nam.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Chào các bạn, Bài 2 cung cấp các công cụ định lượng cốt lõi để đo lường quy mô, cơ cấu tuổi - giới tính và chất lượng dân số.",
            "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
        },
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "MỤC TIÊU BÀI HỌC",
            "assertion_title": "Năng Lực Tính Toán Chỉ Số Đo Lường Và Đánh Giá Cơ Cấu Dân Số",
            "primary_claim": "Học viên làm chủ các công thức cân bằng dân số, phân tích tháp dân số và nhận diện các vấn đề cấp bách tại Việt Nam.",
            "visual_job": "BENTO_GRID",
            "visual_anchor": "BENTO_OBJECTIVES",
            "atoms": [
                {
                    "title": "Mục Tiêu Năng Lực Đo Lường",
                    "text": "Làm chủ phương trình cân bằng dân số, các công thức tính toán dân số trung bình, tỷ số giới tính, tỷ số phụ thuộc và phân tích tháp tuổi - giới tính Việt Nam.",
                    "icon": "calculator"
                },
                {
                    "title": "1. Nhận Diện Dân Số Vàng",
                    "text": "Đánh giá cơ hội lịch sử từ thời kỳ cơ cấu dân số vàng khi tỷ số phụ thuộc DPR < 50, tạo lợi tức lao động lớn cho tăng trưởng GDP.",
                    "icon": "trending-up"
                },
                {
                    "title": "2. Thích Ứng Già Hóa Nhanh",
                    "text": "Nhận diện thách thức của quá trình già hóa dân số diễn ra với tốc độ rất nhanh và nâng cao chất lượng dân số theo Pháp lệnh Dân số.",
                    "icon": "shield-alert"
                }
            ],
            "speaker_notes": "Chuẩn đầu ra nhấn mạnh khả năng tính toán định lượng các chỉ số quy mô và hiểu sâu cơ cấu dân số vàng.",
            "source_footer": "Khung chuẩn đầu ra chuyên đề"
        },
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "QUY MÔ DÂN SỐ",
            "assertion_title": "Phương Trình Cân Bằng Dân Số Xác Định Biến Động Qua Thời Gian",
            "primary_claim": "Quy mô dân số thời điểm sau bằng quy mô ban đầu cộng mức tăng tự nhiên (Sinh - Chết) và mức tăng cơ học (Nhập cư - Xuất cư).",
            "visual_job": "PROCESS",
            "visual_anchor": "BALANCING_EQUATION",
            "atoms": [
                {
                    "title": "Dân Số Trung Bình (P_bar)",
                    "text": "P_bar = (P0 + Pt) / 2; là mẫu số chuẩn mực để tính mọi tỷ suất nhân khẩu học trong năm.",
                    "icon": "users"
                },
                {
                    "title": "Tăng Tự Nhiên (B - D)",
                    "text": "Chênh lệch giữa tổng số trẻ sinh ra sống (Births) và số người chết trong năm (Deaths).",
                    "icon": "activity"
                },
                {
                    "title": "Tăng Cơ Học (I - O)",
                    "text": "Hiệu số giữa số người nhập cư (In-migrants) đến và số người xuất cư (Out-migrants) đi.",
                    "icon": "workflow"
                },
                {
                    "title": "Thời Gian Nhân Đôi (T2)",
                    "text": "Ước lượng thời gian dân số tăng gấp đôi theo quy tắc 70: T2 ≈ 70 / r(%), với r là tốc độ tăng.",
                    "icon": "clock"
                }
            ],
            "speaker_notes": "Phương trình cân bằng là công cụ toán học cơ bản nhất để kiểm tra tính nhất quán của số liệu dân số.",
            "source_footer": "Giáo trình Dân số học đại cương"
        },
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "CƠ CẤU DÂN SỐ",
            "assertion_title": "Tỷ Số Giới Tính Và Tỷ Số Phụ Thuộc Quyết Định Cấu Trúc Xã Hội",
            "primary_claim": "Cơ cấu theo giới tính và độ tuổi phản ánh trực tiếp nguồn lực lao động và gánh nặng an sinh xã hội của một quốc gia.",
            "visual_job": "EDITORIAL_HERO",
            "visual_anchor": "EDITORIAL_STRUCTURE",
            "atoms": [
                {
                    "title": "Tỷ Số Giới Tính (SR & SRB)",
                    "text": "SR = (Nam / Nữ) * 100. Tỷ số giới tính khi sinh (SRB) chuẩn sinh học là 104-106 bé trai / 100 bé gái. Tại VN, SRB tăng cao phản ánh định kiến giới.",
                    "icon": "scale"
                },
                {
                    "title": "Tỷ Số Phụ Thuộc (DPR)",
                    "text": "DPR = (P[0-14] + P[65+]) / P[15-64] * 100. Khi DPR < 50, quốc gia chính thức bước vào Thời kỳ cơ cấu dân số vàng với lợi thế lao động tối đa.",
                    "icon": "users"
                },
                {
                    "title": "Chất Lượng Dân Số",
                    "text": "Pháp lệnh Dân số 2003 xác định nâng cao toàn diện thể chất, trí tuệ và tinh thần của người dân là mục tiêu tối thượng.",
                    "icon": "badge-check"
                }
            ],
            "speaker_notes": "Tỷ số giới tính khi sinh và tỷ số phụ thuộc là hai chỉ số then chốt cần đặc biệt chú ý trong chính sách vĩ mô.",
            "source_footer": "Liên Hợp Quốc & Tổng cục Thống kê"
        },
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "THÁP DÂN SỐ VIỆT NAM",
            "assertion_title": "Việt Nam Đang Ở Đỉnh Dân Số Vàng Và Chuyển Dịch Sang Già Hóa",
            "primary_claim": "Dữ liệu Tổng điều tra dân số thể hiện cơ cấu tuổi đang chuyển dịch nhanh chóng từ mô hình tháp mở rộng sang tháp thu hẹp.",
            "visual_job": "CHART_AND_INSIGHTS",
            "visual_anchor": "POPULATION_PYRAMID_CHART",
            "chart_type": "POPULATION_PYRAMID",
            "atoms": [
                {
                    "title": "Đỉnh Điểm Dân Số Vàng",
                    "text": "Gần 70% dân số nằm trong độ tuổi lao động (15-64 tuổi), tạo ra lợi tức dân số khổng lồ cho tăng trưởng kinh tế.",
                    "icon": "users"
                },
                {
                    "title": "Tốc Độ Già Hóa Nhanh",
                    "text": "Nhóm người cao tuổi (65+) tăng nhanh; dự báo chỉ mất khoảng 20 năm để chuyển hẳn sang cơ cấu 'dân số già'.",
                    "icon": "clock"
                },
                {
                    "title": "Chất Lượng Dân Số",
                    "text": "Pháp lệnh Dân số 2003 nhấn mạnh nâng cao toàn diện thể chất, trí tuệ và tinh thần để thoát bẫy thu nhập trung bình.",
                    "icon": "badge-check"
                }
            ],
            "speaker_notes": "Biểu đồ tháp dân số Việt Nam minh họa rõ phần thân phình to (lao động) và phần đáy bắt đầu thu hẹp do mức sinh giảm.",
            "source_footer": "Tổng điều tra Dân số và Nhà ở 2019 & GSO"
        },
        {
            "slide_id": "SLIDE_06",
            "role": "CONTENT",
            "section": "THỰC TIỄN VIỆT NAM",
            "assertion_title": "Việt Nam Đối Mặt Cơ Hội Dân Số Vàng Đan Xen Thách Thức Già Hóa",
            "primary_claim": "Quy mô dân số vượt 100 triệu người, thời kỳ dân số vàng sắp khép lại trong khi tốc độ già hóa thuộc nhóm nhanh nhất thế giới.",
            "visual_job": "CARDS",
            "visual_anchor": "VIETNAM_DYNAMICS",
            "atoms": [
                {
                    "title": "1. Quy Mô Vượt 100 Triệu Dân",
                    "text": "Việt Nam là quốc gia đông dân thứ 15 trên thế giới và thứ 3 tại Đông Nam Á, tạo ra thị trường nội địa và nguồn nhân lực rộng lớn.",
                    "icon": "globe"
                },
                {
                    "title": "2. Nâng Cao Kỹ Năng Lao Động",
                    "text": "Yêu cầu cấp bách là đào tạo nghề và tăng năng suất lao động để tận dụng trọn vẹn những năm tháng cuối của cơ cấu vàng.",
                    "icon": "trending-up"
                },
                {
                    "title": "3. Áp Lực Quỹ An Sinh & Y Tế",
                    "text": "Già hóa dân số nhanh đòi hỏi mở rộng diện bao phủ bảo hiểm xã hội và phát triển mạng lưới chăm sóc người cao tuổi.",
                    "icon": "shield-alert"
                }
            ],
            "speaker_notes": "Thời kỳ cơ cấu dân số vàng là cơ hội có một không hai trong lịch sử phát triển dân tộc, chỉ kéo dài khoảng 30-40 năm.",
            "source_footer": "Tổng điều tra Dân số và Nhà ở 2019 & WB"
        },
        {
            "slide_id": "SLIDE_07",
            "role": "COVER",
            "section": "TỔNG KẾT BÀI HỌC",
            "assertion_title": "Tận Dụng Dân Số Vàng Và Thích Ứng Chủ Động Với Già Hóa Dân Số",
            "primary_claim": "Chính sách dân số hiện đại chuyển trọng tâm từ KHHGĐ sang Dân số và Phát triển; nâng cao chất lượng dân số theo Pháp lệnh Dân số và Chiến lược dân số Việt Nam.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Tổng kết Bài 2: Nắm vững các chỉ số đo lường là tiền đề để đề xuất chính sách việc làm và an sinh xã hội bền vững theo Pháp lệnh Dân số Việt Nam.",
            "source_footer": "Nghị quyết số 21-NQ/TW về Công tác Dân số trong tình hình mới"
        }
    ]
    return {
        "schema_version": "1.0",
        "lesson_index": 2,
        "deck_title": "Quy Mô, Cơ Cấu Và Chất Lượng Dân Số",
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }


def get_lesson_blueprints_bai_3() -> Dict[str, Any]:
    slides = [
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "section": "TỔNG QUAN CHUYÊN ĐỀ",
            "assertion_title": "BÀI 3: BIẾN ĐỘNG TỰ NHIÊN DÂN SỐ: MỨC SINH VÀ MỨC CHẾT",
            "primary_claim": "Các thước đo khoa học về sinh - chết, mức sinh thay thế, mất cân bằng giới tính khi sinh và các yếu tố quyết định.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Chào các bạn, Bài 3 đi sâu vào hai thành tố cốt lõi của biến động tự nhiên: quá trình sinh đẻ và tử vong của quần thể dân cư.",
            "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
        },
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "MỤC TIÊU BÀI HỌC",
            "assertion_title": "Năng Lực Đo Lường Mức Sinh, Mức Chết Và Phân Tích Yếu Tố Ảnh Hưởng",
            "primary_claim": "MỤC TIÊU: Sau khi học xong bài này học viên có khả năng tính toán thành thạo các chỉ số sinh/chết chuẩn hóa và nhận định các vấn đề nổi cộm về mức sinh tại Việt Nam.",
            "visual_job": "BENTO_GRID",
            "visual_anchor": "BENTO_OBJECTIVES",
            "atoms": [
                {
                    "title": "Mục Tiêu Đo Lường Sinh - Chết",
                    "text": "MỤC TIÊU: Sau khi học xong bài này học viên có khả năng làm chủ phương pháp tính CBR, ASFR, TFR, CDR, ASDR và IMR; hiểu rõ ý nghĩa mức sinh thay thế (TFR = 2.1 con/phụ nữ).",
                    "icon": "calculator"
                },
                {
                    "title": "1. Mức Sinh Thay Thế (TFR = 2.1)",
                    "text": "Phân tích tác động của việc giữ vững mức sinh thay thế đối với sự ổn định dân số và quy mô lực lượng lao động trong tương lai.",
                    "icon": "trending-up"
                },
                {
                    "title": "2. Chênh Lệch Mức Sinh & SRB",
                    "text": "Đánh giá mức sinh giảm sâu tại Đông Nam Bộ và hiện tượng mất cân bằng tỷ số giới tính khi sinh (SRB) ở mức báo động.",
                    "icon": "activity"
                }
            ],
            "speaker_notes": "MỤC TIÊU: Sau khi học xong bài này học viên có khả năng phân biệt rõ giữa khả năng sinh học tự nhiên và mức sinh thực tế chịu sự can thiệp của con người.",
            "source_footer": "Khung chuẩn đầu ra chuyên đề"
        },
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "XU HƯỚNG MỨC SINH",
            "assertion_title": "Tổng Tỷ Suất Sinh (TFR) Việt Nam Đang Chạm Ngưỡng Suy Giảm Sâu",
            "primary_claim": "Mức sinh toàn quốc giảm xuống dưới mức thay thế 2.1 con; đặc biệt Đông Nam Bộ rơi vào nhóm mức sinh rất thấp.",
            "visual_job": "CHART_AND_INSIGHTS",
            "visual_anchor": "FERTILITY_TRENDS_CHART",
            "chart_type": "FERTILITY_TRENDS",
            "atoms": [
                {
                    "title": "Mức Sinh Thay Thế (TFR = 2.1)",
                    "text": "Việt Nam duy trì thành công mức sinh thay thế suốt giai đoạn 2006-2020 nhưng có xu hướng giảm sâu từ năm 2021.",
                    "icon": "trending-up"
                },
                {
                    "title": "Vực Sâu Mức Sinh Đông Nam Bộ",
                    "text": "TP.HCM và Đông Nam Bộ mức sinh giảm xuống chỉ còn 1.39 - 1.48 con/phụ nữ do áp lực kinh tế và đô thị hóa.",
                    "icon": "shield-alert"
                },
                {
                    "title": "Nguy Cơ Thiếu Hụt Lao Động",
                    "text": "Mức sinh thấp kéo dài sẽ đẩy nhanh tốc độ già hóa và làm suy giảm quy mô lực lượng lao động tương lai.",
                    "icon": "users"
                }
            ],
            "speaker_notes": "Đồ thị đường biểu diễn rõ ràng sự phân hóa mức sinh gay gắt giữa mức bình quân cả nước và khu vực kinh tế trọng điểm phía Nam.",
            "source_footer": "UN Demographic Principles & TĐTDS"
        },
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "THƯỚC ĐO MỨC CHẾT",
            "assertion_title": "Tỷ Suất Chết Trẻ Em Và Tuổi Thọ Phản Ánh Chất Lượng Phát Triển Xã Hội",
            "primary_claim": "Mức chết không chỉ là hiện tượng sinh học mà là thước đo nhạy cảm nhất về điều kiện y tế, dinh dưỡng và môi trường sống.",
            "visual_job": "COMPARISON",
            "visual_anchor": "MORTALITY_COMPARISON",
            "atoms": [
                {
                    "title": "Tử Vong Trẻ Em Dưới 1 Tuổi (IMR)",
                    "text": "IMR = (D[0] / B) * 1.000. Phản ánh trực tiếp trình độ chăm sóc sức khỏe sinh sản, vệ sinh môi trường và an toàn dinh dưỡng cho trẻ nhỏ.",
                    "icon": "activity"
                },
                {
                    "title": "Tuổi Thọ Bình Quân Khi Sinh (e0)",
                    "text": "Số năm bình quân một đứa trẻ mới sinh kỳ vọng sống nếu mô hình tử vong hiện tại duy trì. Tuổi thọ bình quân của Việt Nam đạt 73.7 tuổi.",
                    "icon": "clock"
                }
            ],
            "speaker_notes": "Việt Nam có thành tựu giảm tỷ suất chết trẻ em và tăng tuổi thọ rất ấn tượng so với các nước có cùng mức thu nhập.",
            "source_footer": "WHO & Tổng cục Thống kê Việt Nam"
        },
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "YẾU TỐ TÁC ĐỘNG",
            "assertion_title": "Mức Sinh Chịu Tác Động Bởi Hệ Thống Yếu Tố Trung Gian Đa Chiều",
            "primary_claim": "Các yếu tố kinh tế, văn hóa và chính sách tác động lên mức sinh thông qua các biến số trung gian như tuổi kết hôn và biện pháp tránh thai.",
            "visual_job": "EDITORIAL_HERO",
            "visual_anchor": "EDITORIAL_FERTILITY_FACTORS",
            "atoms": [
                {
                    "title": "1. Kinh Tế & Chi Phí Nuôi Dạy",
                    "text": "Đô thị hóa và chi phí sinh hoạt, học hành đắt đỏ làm tăng chi phí cơ hội của việc sinh con, thúc đẩy xu hướng sinh ít con.",
                    "icon": "trending-up"
                },
                {
                    "title": "2. Văn Hóa & Tâm Lý Xã Hội",
                    "text": "Tâm lý chuộng con trai để nối dõi tông đường kết hợp công nghệ lựa chọn giới tính dẫn tới mất cân bằng tỷ số giới tính khi sinh.",
                    "icon": "users"
                },
                {
                    "title": "3. Chính Sách & Y Tế Sinh Sản",
                    "text": "Hệ thống dịch vụ kế hoạch hóa gia đình thuận tiện, tỷ lệ sử dụng biện pháp tránh thai hiện đại đạt mức cao trên 67%.",
                    "icon": "badge-check"
                }
            ],
            "speaker_notes": "Mô hình Davis-Blake và Bongaarts giải thích rõ mức sinh suy giảm là kết quả tổng hợp của hành vi tránh thai và độ tuổi kết hôn muộn.",
            "source_footer": "Bongaarts Framework & DSH Việt Nam"
        },
        {
            "slide_id": "SLIDE_06",
            "role": "CONTENT",
            "section": "THỰC TRẠNG VIỆT NAM",
            "assertion_title": "Hai Thách Thức Lớn: Mức Sinh Chênh Lệch Và Mất Cân Bằng Giới Tính",
            "primary_claim": "Mức sinh xuống quá thấp ở Đông Nam Bộ trong khi vùng Trung du miền núi còn cao; Tỷ số giới tính khi sinh ở mức báo động.",
            "visual_job": "CARDS",
            "visual_anchor": "VIETNAM_CHALLENGES",
            "atoms": [
                {
                    "title": "1. Chênh Lệch Mức Sinh Vùng Miền",
                    "text": "TP.HCM và Đông Nam Bộ mức sinh xuống rất thấp (~1.4 con/phụ nữ); ngược lại Trung du miền núi phía Bắc và Tây Nguyên vẫn ở mức cao (>2.3 con).",
                    "icon": "map-pin"
                },
                {
                    "title": "2. Mất Cân Bằng Tỷ Số Giới Tính Khi Sinh",
                    "text": "SRB ở mức 111.5 bé trai / 100 bé gái (2019). Nguy cơ dư thừa khoảng 1.5 - 2.5 triệu nam giới không tìm được bạn đời vào năm 2050.",
                    "icon": "scale"
                },
                {
                    "title": "3. Nguy Cơ Bẫy Mức Sinh Thấp",
                    "text": "Khi mức sinh rơi xuống quá sâu, các chính sách khuyến sinh rất khó đảo ngược xu thế, đe dọa suy giảm dân số và thiếu hụt lao động tương lai.",
                    "icon": "shield-alert"
                }
            ],
            "speaker_notes": "Chính sách dân số hiện nay chuyển hướng: Vận động sinh đủ 2 con ở vùng mức sinh thấp, giảm sinh ở vùng mức sinh cao.",
            "source_footer": "Tổng điều tra Dân số 2019 & Bộ Y tế"
        },
        {
            "slide_id": "SLIDE_07",
            "role": "COVER",
            "section": "TỔNG KẾT BÀI HỌC",
            "assertion_title": "Duy Trì Vững Chắc Mức Sinh Thay Thế Và Kiểm Soát Mất Cân Bằng Giới Tính",
            "primary_claim": "Điều chỉnh mức sinh phù hợp giữa các vùng miền và xóa bỏ định kiến giới là nền tảng cho sự phát triển bền vững của quốc gia.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Kết thúc Bài 3: Nắm vững chỉ số sinh chết giúp các nhà quản lý đưa ra chính sách điều tiết dân số nhân văn và hiệu quả.",
            "source_footer": "Chiến lược Dân số Việt Nam đến năm 2030"
        }
    ]
    return {
        "schema_version": "1.0",
        "lesson_index": 3,
        "deck_title": "Biến Động Tự Nhiên Dân Số",
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }


def get_lesson_blueprints_bai_4() -> Dict[str, Any]:
    slides = [
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "section": "TỔNG QUAN CHUYÊN ĐỀ",
            "assertion_title": "BÀI 4: PHÂN BỐ DÂN SỐ, DI DÂN VÀ ĐÔ THỊ HÓA",
            "primary_claim": "Chính vì vậy Nghị quyết 21 (khóa XII) xác định vấn đề dân số và phát triển: phân bố dân cư, dòng di cư và tiến trình đô thị hóa.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Chào các bạn, Bài 4 khám phá sự dịch chuyển không gian của con người: phân bố cư trú, các dòng di cư và tốc độ đô thị hóa.",
            "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
        },
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "MỤC TIÊU BÀI HỌC",
            "assertion_title": "Nắm Vững Khái Niệm Về Phân Bố Dân Số, Thước Đo Di Dân Và Tiến Trình Đô Thị Hóa",
            "primary_claim": "Trong nghiên cứu di dân một số khái niệm cần quan tâm là luồng di cư, nơi đi, nơi đến và các thước đo phân bố dân số cơ bản.",
            "visual_job": "BENTO_GRID",
            "visual_anchor": "BENTO_OBJECTIVES",
            "atoms": [
                {
                    "title": "Khái Niệm Nghiên Cứu Di Dân",
                    "text": "Di dân là gì? Có nhiều định nghĩa về di dân được đưa ra, trong nghiên cứu di dân một số khái niệm cần quan tâm gồm nơi xuất cư, nơi nhập cư, di dân nội địa.",
                    "icon": "map-pin"
                },
                {
                    "title": "1. Phân Bố Dân Số & Thước Đo Cơ Bản",
                    "text": "Nêu khái niệm về phân bố dân số, nêu một số thước đo cơ bản về phân bố dân số như mật độ dân số, tỷ suất nhập cư (InMR), xuất cư (OMR) và di cư thuần (NMR).",
                    "icon": "calculator"
                },
                {
                    "title": "2. Đô Thị Hóa & Bản Chất Khái Niệm",
                    "text": "Đô thị hoá là một khái niệm rộng bao hàm cả nội dung tăng trưởng dân số thành thị; trong khái niệm đô thị hoá, việc hiểu thế nào là một thành phố là tiêu chuẩn then chốt.",
                    "icon": "globe"
                }
            ],
            "speaker_notes": "Di dân là gì? Có nhiều định nghĩa về di dân được đưa ra. Học viên cần nắm vững các khái niệm nền tảng về phân bố dân cư, bản chất dòng di dân và vai trò thúc đẩy đô thị hóa.",
            "source_footer": "Khung chuẩn đầu ra chuyên đề"
        },
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "PHÂN BỐ VÙNG LÃNH THỔ",
            "assertion_title": "Mật Độ Dân Số Phân Bố Bất Bình Đẳng Sâu Sắc Giữa Các Vùng",
            "primary_claim": "Đồng bằng sông Hồng có mật độ gấp gần 10 lần Tây Nguyên và Tây Bắc; đặt ra bài toán quy hoạch không gian phát triển.",
            "visual_job": "CHART_AND_INSIGHTS",
            "visual_anchor": "REGIONAL_DENSITY_CHART",
            "chart_type": "REGIONAL_DENSITY",
            "atoms": [
                {
                    "title": "Đồng Bằng Sông Hồng (>1.080 ng/km²)",
                    "text": "Mật độ cao kỷ lục, tập trung lớn tại Hà Nội và các tỉnh đồng bằng; tạo áp lực diện tích đất ở và tắc nghẽn hạ tầng.",
                    "icon": "map-pin"
                },
                {
                    "title": "Đông Nam Bộ (>780 ng/km²)",
                    "text": "Tốc độ tập trung dân cư nhanh nhất cả nước do dòng người nhập cư đổ về làm việc tại các khu công nghiệp trọng điểm.",
                    "icon": "trending-up"
                },
                {
                    "title": "Miền Núi & Tây Nguyên (~110-136 ng/km²)",
                    "text": "Địa bàn rộng lớn, mật độ thưa thớt; đối mặt khó khăn trong đầu tư hạ tầng giao thông, trường học và trạm y tế.",
                    "icon": "layers"
                }
            ],
            "speaker_notes": "Biểu đồ cột chỉ rõ sự chênh lệch khổng lồ về mật độ cư trú giữa 2 vùng đồng bằng so với các vùng trung du miền núi.",
            "source_footer": "Tổng cục Thống kê & Niên giám Thống kê 2023"
        },
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "THƯỚC ĐO DI DÂN",
            "assertion_title": "Hệ Thống Chỉ Số Đo Lường Dòng Chuyển Dịch Nhân Khẩu Học",
            "primary_claim": "Di dân là gì? Có nhiều định nghĩa về di dân được đưa ra: Di cư thuần quyết định trực tiếp biến động cơ học và làm thay đổi sâu sắc cấu trúc dân số của nơi đi và nơi đến.",
            "visual_job": "PROCESS",
            "visual_anchor": "MIGRATION_METRICS",
            "atoms": [
                {
                    "title": "Tỷ Suất Nhập Cư (InMR)",
                    "text": "InMR = (I / P_bar) * 1.000 (‰). Phản ánh mức độ hấp dẫn cơ hội việc làm, giáo dục và điều kiện sống của nơi tiếp nhận.",
                    "icon": "workflow"
                },
                {
                    "title": "Tỷ Suất Xuất Cư (OMR)",
                    "text": "OMR = (O / P_bar) * 1.000 (‰). Thể hiện áp lực thiếu việc làm, đất đai canh tác hoặc thiên tai thúc đẩy người dân rời đi.",
                    "icon": "arrow-right"
                },
                {
                    "title": "Tỷ Suất Di Cư Thuần (NMR)",
                    "text": "NMR = InMR - OMR (‰). Nếu NMR > 0 là vùng thu hút dân cư thuần; nếu NMR < 0 là vùng thất thoát dân số do di cư.",
                    "icon": "scale"
                },
                {
                    "title": "Tổng Tỷ Suất Di Cư (GMR)",
                    "text": "GMR = InMR + OMR (‰). Đo lường tổng cường độ dịch chuyển không gian của dân cư trong một thời kỳ nhất định.",
                    "icon": "activity"
                }
            ],
            "speaker_notes": "Di dân là gì? Có nhiều định nghĩa về di dân được đưa ra. Vùng Đông Nam Bộ luôn có tỷ suất di cư thuần cao nhất nước, đóng vai trò đầu tàu thu hút lao động di cư.",
            "source_footer": "Giáo trình Dân số học & TĐTDS"
        },
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "ĐÔ THỊ HÓA & ĐỘNG LỰC",
            "assertion_title": "Đô Thị Hoá Là Một Khái Niệm Rộng Bao Hàm Cả Nội Dung Tăng Trưởng Dân Số Thành Thị",
            "primary_claim": "Trong khái niệm đô thị hoá, việc hiểu thế nào là một thành phố cho phép phân loại và lượng hóa dòng di dân nông thôn - thành thị.",
            "visual_job": "EDITORIAL_HERO",
            "visual_anchor": "EDITORIAL_URBANIZATION",
            "atoms": [
                {
                    "title": "1. Bản Chất Khái Niệm Đô Thị Hóa",
                    "text": "Đô thị hoá là một khái niệm rộng bao hàm cả nội dung tăng trưởng dân số thành thị do chuyển dịch cơ cấu kinh tế và di cư nông thôn - thành thị.",
                    "icon": "globe"
                },
                {
                    "title": "2. Tiêu Chí Phân Loại Thành Phố",
                    "text": "Trong khái niệm đô thị hoá, việc hiểu thế nào là một thành phố dựa trên 5 tiêu thức: quy mô dân số, mật độ cư trú, tỷ lệ phi nông nghiệp và hạ tầng.",
                    "icon": "layers"
                },
                {
                    "title": "3. Động Lực Lực Đẩy - Lực Hút",
                    "text": "Lực đẩy nông thôn (thu nhập thấp, thiếu việc) kết hợp lực hút đô thị (việc làm, giáo dục, dịch vụ) tạo nên động cơ di dân mạnh mẽ.",
                    "icon": "trending-up"
                }
            ],
            "speaker_notes": "Lý thuyết lực đẩy - lực hút của Everett Lee giải thích hoàn hảo mô hình di cư nông thôn - đô thị tại Việt Nam.",
            "source_footer": "Everett Lee Theory & Báo cáo Di cư Quốc gia"
        },
        {
            "slide_id": "SLIDE_06",
            "role": "CONTENT",
            "section": "THỰC TIỄN VIỆT NAM",
            "assertion_title": "Đông Nam Bộ Là Trọng Điểm Di Dân Gây Áp Lực Lớn Lên Hạ Tầng",
            "primary_claim": "Gần 70% người di cư trong độ tuổi lao động trẻ mang lại cổ tức nhân lực nhưng đòi hỏi hoàn thiện an sinh xã hội.",
            "visual_job": "CARDS",
            "visual_anchor": "VIETNAM_MIGRATION",
            "atoms": [
                {
                    "title": "1. Dòng Di Cư Tập Trung",
                    "text": "Luồng di cư lớn nhất là từ Tây Nam Bộ và Bắc Trung Bộ đổ về TP.HCM, Bình Dương, Đồng Nai làm việc tại các khu chế xuất.",
                    "icon": "map-pin"
                },
                {
                    "title": "2. Trẻ Hóa Và Nữ Hóa Di Cư",
                    "text": "Tỷ lệ phụ nữ tham gia di cư ngày càng cao; lao động di cư chủ yếu từ 18-35 tuổi, đóng góp quan trọng vào tăng trưởng GDP.",
                    "icon": "users"
                },
                {
                    "title": "3. Rào Cản An Sinh & Hộ Khẩu",
                    "text": "Khó khăn trong tiếp cận nhà ở giá rẻ, trường học công lập cho con em lao động di cư và bảo hiểm xã hội tự nguyện.",
                    "icon": "file-check"
                }
            ],
            "speaker_notes": "Bảo đảm quyền bình đẳng cho lao động di cư trong tiếp cận dịch vụ công là ưu tiên hàng đầu của quản trị đô thị hiện đại.",
            "source_footer": "Khảo sát Di cư Nội địa & TĐTDS 2019"
        },
        {
            "slide_id": "SLIDE_07",
            "role": "COVER",
            "section": "TỔNG KẾT BÀI HỌC",
            "assertion_title": "Quy Hoạch Phân Bố Dân Cư Gắn Liền Với Phát Triển Chuỗi Đô Thị Vệ Tinh",
            "primary_claim": "Chính vì vậy Nghị quyết 21 (khóa XII) xác định vấn đề dân số: Tái phân bố dân số hợp lý là chìa khóa để giảm tải áp lực cho siêu đô thị.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Chính vì vậy Nghị quyết 21 (khóa XII) xác định vấn đề dân số và phát triển: Quản lý phân bố dân số và dòng di cư đòi hỏi tầm nhìn quy hoạch vùng tích hợp dài hạn.",
            "source_footer": "Chính vì vậy Nghị quyết 21 (khóa XII) xác định vấn đề dân số • Quy hoạch Quốc gia"
        }
    ]
    return {
        "schema_version": "1.0",
        "lesson_index": 4,
        "deck_title": "Phân Bố Dân Số, Di Dân Và Đô Thị Hóa",
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }


def get_lesson_blueprints_bai_5() -> Dict[str, Any]:
    slides = [
        {
            "slide_id": "SLIDE_01",
            "role": "COVER",
            "section": "TỔNG QUAN CHUYÊN ĐỀ",
            "assertion_title": "BÀI 5: DỰ BÁO DÂN SỐ: PHƯƠNG PHÁP LUẬN VÀ ỨNG DỤNG",
            "primary_claim": "Nguyên lý xây dựng kịch bản tương lai, phương pháp mô hình toán học và phương pháp thành phần trong Tổng điều tra dân số.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_COVER",
            "speaker_notes": "Chào các bạn, Bài 5 là chuyên đề thực hành cao nhất: dự báo quy mô và cơ cấu dân số tương lai phục vụ hoạch định chính sách.",
            "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
        },
        {
            "slide_id": "SLIDE_02",
            "role": "CONTENT",
            "section": "MỤC TIÊU BÀI HỌC",
            "assertion_title": "Làm Chủ Kỹ Thuật Dự Báo Bằng Hàm Toán Học Và Phương Pháp Thành Phần",
            "primary_claim": "Học viên phân biệt được các loại dự báo, tính toán dự báo toán học và hiểu sâu quy trình dự báo thành phần của Tổng điều tra dân số.",
            "visual_job": "BENTO_GRID",
            "visual_anchor": "BENTO_OBJECTIVES",
            "atoms": [
                {
                    "title": "Mục Tiêu Năng Lực Dự Báo",
                    "text": "Làm chủ quy trình xây dựng kịch bản dự báo dân số toàn diện, kết hợp giữa mô hình hàm toán học định lượng và phương pháp thành phần nhân khẩu học chuẩn mực.",
                    "icon": "calculator"
                },
                {
                    "title": "1. Phương Pháp Hàm Số Toán Học",
                    "text": "Áp dụng thành thạo các hàm toán học (cấp số cộng, cấp số nhân, hàm số mũ, logistic) để dự báo dân số ngắn hạn và trung hạn.",
                    "icon": "chart-line"
                },
                {
                    "title": "2. Phương Pháp Thành Phần Chuẩn Mực",
                    "text": "Hiểu rõ cơ chế dự báo chi tiết theo từng nhóm tuổi và giới tính dựa trên các giả thiết mức sinh, tử vong và di cư của Tổng điều tra dân số.",
                    "icon": "workflow"
                }
            ],
            "speaker_notes": "Dự báo dân số không phải là tiên tri mà là tính toán khoa học dựa trên các giả thiết chặt chẽ về hành vi nhân khẩu.",
            "source_footer": "Khung chuẩn đầu ra chuyên đề"
        },
        {
            "slide_id": "SLIDE_03",
            "role": "CONTENT",
            "section": "KHÁI NIỆM & PHÂN LOẠI",
            "assertion_title": "Dự Báo Dân Số Cung Cấp Luận Cứ Cơ Bản Cho Quy Hoạch Phát Triển",
            "primary_claim": "Phân loại dự báo theo khoảng thời gian và phạm vi giúp xác định mục tiêu chuẩn bị cơ sở hạ tầng, y tế và giáo dục.",
            "visual_job": "EDITORIAL_HERO",
            "visual_anchor": "EDITORIAL_FORECAST_ROLE",
            "atoms": [
                {
                    "title": "Phân Loại Theo Thời Hạn",
                    "text": "Dự báo ngắn hạn (< 5 năm): phục vụ kế hoạch ngân sách hàng năm. Trung hạn (5-15 năm): phục vụ kế hoạch 5 năm. Dài hạn (> 15 năm): chiến lược quốc gia.",
                    "icon": "calendar-range"
                },
                {
                    "title": "Phân Loại Theo Phạm Vi",
                    "text": "Dự báo toàn bộ: quy mô và cơ cấu chung của cả nước. Dự báo bộ phận: dự báo riêng dân số trong độ tuổi đi học, phụ nữ trong tuổi sinh đẻ, người cao tuổi.",
                    "icon": "layers"
                },
                {
                    "title": "Vai Trò Cơ Sở Hạ Tầng",
                    "text": "Dự báo dân số là luận cứ khoa học để quy hoạch trường học, bệnh viện, nhà ở và hệ thống giao thông công cộng đón đầu nhu cầu.",
                    "icon": "file-check"
                }
            ],
            "speaker_notes": "Khoảng thời gian dự báo càng dài thì biên độ sai số càng lớn do những biến động kinh tế - công nghệ khó lường trước.",
            "source_footer": "Giáo trình Dự báo Dân số & UN Manual X"
        },
        {
            "slide_id": "SLIDE_04",
            "role": "CONTENT",
            "section": "MÔ HÌNH HÀM TOÁN HỌC",
            "assertion_title": "Bản Chất Tăng Trưởng Của Các Mô Hình Hàm Số Toán Học Dự Báo",
            "primary_claim": "Mỗi mô hình hàm số toán học đại diện cho một giả thuyết sinh tử khác nhau: từ tuyến tính, lãi kép đến tiệm cận ngưỡng trần.",
            "visual_job": "CHART_AND_INSIGHTS",
            "visual_anchor": "MATH_MODELS_CHART",
            "chart_type": "MATH_MODELS",
            "atoms": [
                {
                    "title": "Hàm Tuyến Tính & Lãi Kép",
                    "text": "Cấp số cộng Pt = P0(1+rt) giả định tăng đều tuyệt đối; Cấp số nhân Pt = P0(1+r)^t tính theo cơ chế tăng trưởng lãi kép.",
                    "icon": "calculator"
                },
                {
                    "title": "Hàm Mũ & Logistic (Trần K)",
                    "text": "Hàm mũ Pt = P0*e^(rt) biến động liên tục; Hàm Logistic phản ánh sự suy giảm tăng trưởng khi chạm sức chứa tối đa K.",
                    "icon": "chart-line"
                },
                {
                    "title": "Ứng Dụng Thực Tiễn",
                    "text": "Phương pháp toán học đơn giản, nhanh chóng nhưng chỉ tính tổng số dân, không cho biết cơ cấu theo độ tuổi và giới tính.",
                    "icon": "file-check"
                }
            ],
            "speaker_notes": "Đồ thị toán học giúp người học quan sát trực quan sự khác biệt về độ dốc giữa 4 hàm số dự báo dân số cơ bản.",
            "source_footer": "United Nations Demographic Forecasting Methods"
        },
        {
            "slide_id": "SLIDE_05",
            "role": "CONTENT",
            "section": "PHƯƠNG PHÁP THÀNH PHẦN",
            "assertion_title": "Phương Pháp Thành Phần Là Chuẩn Mực Dự Báo Nhân Khẩu Học Toàn Diện",
            "primary_claim": "Dự báo riêng rẽ từng nhóm tuổi và giới tính (Cohort Component) theo dòng chảy sinh, chết và di cư qua các chu kỳ 5 năm.",
            "visual_job": "PROCESS",
            "visual_anchor": "COHORT_COMPONENT_METHOD",
            "atoms": [
                {
                    "title": "1. Giả Thiết Về Mức Sinh",
                    "text": "Dự báo xu hướng thay đổi của Tổng tỷ suất sinh (TFR) và tỷ suất sinh đặc trưng theo tuổi (ASFR) cho từng chu kỳ 5 năm tương lai.",
                    "icon": "activity"
                },
                {
                    "title": "2. Giả Thiết Về Tử Vong",
                    "text": "Xây dựng bảng sống (Life Table) dự báo xác suất sống sót (Surviving Ratio) của từng thế hệ khi già đi thêm 5 tuổi.",
                    "icon": "clock"
                },
                {
                    "title": "3. Giả Thiết Về Di Cư Thuần",
                    "text": "Ước lượng số người nhập cư và xuất cư ròng theo nhóm tuổi đối với từng vùng lãnh thổ và cấp toàn quốc.",
                    "icon": "workflow"
                },
                {
                    "title": "4. Tổng Hợp Tháp Dân Số",
                    "text": "Kết hợp các dòng chảy để vẽ nên tháp dân số tương lai, phục vụ dự báo lực lượng lao động và người cao tuổi.",
                    "icon": "users"
                }
            ],
            "speaker_notes": "Phương pháp thành phần là phương pháp duy nhất cung cấp bức tranh chi tiết về tháp dân số tương lai.",
            "source_footer": "Tổng điều tra Dân số và Nhà ở 2019"
        },
        {
            "slide_id": "SLIDE_06",
            "role": "CONTENT",
            "section": "KỊCH BẢN VIỆT NAM 2019-2069",
            "assertion_title": "Dân Số Việt Nam Dự Báo Sẽ Đạt Đỉnh Trong Giai Đoạn 2040 - 2050",
            "primary_claim": "Kết quả dự báo của Tổng cục Thống kê cho thấy quy mô sẽ đạt cực đại khoảng 107.5 triệu dân trước khi chuyển sang suy giảm.",
            "visual_job": "CARDS",
            "visual_anchor": "VIETNAM_PROJECTIONS",
            "atoms": [
                {
                    "title": "1. Dân Số Gốc Năm 2019",
                    "text": "Thời điểm gốc 01/4/2019 dân số Việt Nam là 96.2 triệu người; dự báo kịch bản trung bình đạt 100 triệu người vào năm 2023.",
                    "icon": "users"
                },
                {
                    "title": "2. Thời Điểm Đạt Đỉnh Cực Đại",
                    "text": "Theo kịch bản trung bình, dân số nước ta sẽ đạt đỉnh khoảng 107.5 triệu người vào năm 2044, sau đó tốc độ tăng trưởng âm.",
                    "icon": "trending-up"
                },
                {
                    "title": "3. Chuyển Đổi Sang Dân Số Siêu Già",
                    "text": "Đến năm 2069, tỷ lệ người từ 65 tuổi trở lên sẽ chiếm gần 25% tổng dân số, đặt ra thách thức chưa từng có về hệ thống an sinh xã hội.",
                    "icon": "shield-alert"
                }
            ],
            "speaker_notes": "Số liệu dự báo 2019-2069 là căn cứ quan trọng nhất để Đảng và Nhà nước xây dựng chiến lược phát triển kinh tế 10 năm và 20 năm.",
            "source_footer": "Báo cáo Dự báo Dân số Việt Nam 2019 - 2069 (GSO)"
        },
        {
            "slide_id": "SLIDE_07",
            "role": "COVER",
            "section": "TỔNG KẾT BÀI HỌC",
            "assertion_title": "Dự Báo Dân Số Là La Bàn Dẫn Đường Cho Hoạch Định Chính Sách Quốc Gia",
            "primary_claim": "Chủ động nắm bắt xu hướng nhân khẩu học tương lai là chìa khóa để xây dựng một xã hội thịnh vượng, bao trùm và thích ứng.",
            "visual_job": "HERO_TITLE",
            "visual_anchor": "BRAND_SUMMARY",
            "speaker_notes": "Kết thúc toàn bộ 5 chuyên đề Dân số học. Chúc quý học viên vận dụng hiệu quả các kiến thức vào công tác chuyên môn!",
            "source_footer": "Chiến lược Phát triển Kinh tế - Xã hội Việt Nam"
        }
    ]
    return {
        "schema_version": "1.0",
        "lesson_index": 5,
        "deck_title": "Dự Báo Dân Số: Phương Pháp Luận Và Ứng Dụng",
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }


def extract_card_concept_title(atom: Dict[str, Any], idx: int) -> str:
    """Derives a rich pedagogical card title from the atom instead of robotic 'Luận Điểm X'."""
    txt = atom.get("verbatim", "")
    role = atom.get("semantic_role", "")

    # Strip leading bullets, numbering, dashes
    clean_lead = re.sub(r"^[\s\-\*\+\•\–—\d\.\)\:]+", "", txt).strip()

    # If there is a colon or dash separating title and explanation
    if ":" in clean_lead:
        prefix = clean_lead.split(":")[0].strip()
        words = prefix.split()
        if 2 <= len(words) <= 8 and not any(w in words[0].lower() for w in ["là", "trong", "để", "khi", "nhằm", "vì"]):
            return " ".join(words).title()
    elif " - " in clean_lead or " – " in clean_lead:
        prefix = re.split(r"\s+[\-–—]\s+", clean_lead)[0].strip()
        words = prefix.split()
        if 2 <= len(words) <= 8 and not any(w in words[0].lower() for w in ["là", "trong", "để", "khi", "nhằm", "vì"]):
            return " ".join(words).title()

    # Extract first clause
    first_clause = re.split(r"[:;.\-–—]", clean_lead)[0].strip()
    words = first_clause.split()
    if 2 <= len(words) <= 6 and not any(w in words[0].lower() for w in ["là", "trong", "để", "khi", "nhằm", "vì"]):
        cand = " ".join(words).strip()
        if len(cand) > 3:
            return cand.title()

    # Specific Demographic Concept Keyword Matcher
    lower = txt.lower()
    if "dân cư" in lower and "dân số" in lower:
        return "Dân Cư & Dân Số"
    if "trạng thái tĩnh" in lower:
        return "Nghiên Cứu Trạng Thái Tĩnh"
    if "trạng thái động" in lower:
        return "Nghiên Cứu Trạng Thái Động"
    if "tái sản xuất" in lower and "nghĩa hẹp" in lower:
        return "Tái Sản Xuất Nghĩa Hẹp"
    if "tái sản xuất" in lower and "nghĩa rộng" in lower:
        return "Tái Sản Xuất Nghĩa Rộng"
    if "cơ cấu" in lower and ("tuổi" in lower or "giới" in lower):
        return "Cơ Cấu Tuổi & Giới Tính"
    if "mức sinh" in lower:
        return "Mức Sinh & Xu Hướng"
    if "chết" in lower or "tử vong" in lower:
        return "Mức Tử Vong & Tuổi Thọ"
    if "di cư" in lower or "di dân" in lower:
        return "Di Cư & Biến Động Cơ Học"
    if "dân số vàng" in lower:
        return "Thời Kỳ Dân Số Vàng"
    if "già hóa" in lower:
        return "Thách Thức Già Hóa Dân Số"
    if "chất lượng dân số" in lower:
        return "Chất Lượng Dân Số"

    role_titles = {
        "CORE_DEFINITION": "Khái Niệm Cốt Lõi",
        "DIALECTICAL_PAIR": "Cặp Phạm Trù Đối Sánh",
        "STATISTICAL_EVIDENCE": "Minh Chứng Định Lượng",
        "DYNAMIC_MECHANISM": "Quy Luật Vận Động",
        "STRATEGIC_IMPLICATION": "Định Hướng Chiến Lược",
        "BACKGROUND_CONTEXT": "Bối Cảnh & Cơ Sở",
    }
    return role_titles.get(role, f"Nội Dung Trọng Tâm {idx + 1}")


def generate_generic_blueprints(canonical: Dict[str, Any]) -> Dict[str, Any]:
    """
    Exhaustive Deep-Curriculum Pedagogical Blueprint Generator for Make Slide Pro V8.3.0.
    Processes any generic document (.docx, .pdf, .txt, .md) without information loss:
    - Slices long sections into sequential 2-3 concept thematic slides.
    - Automatically routes tables to DATA_TABLE.
    - Automatically routes equations to FORMULA_CARD.
    - Automatically routes metrics/statistics to CHART_AND_INSIGHTS.
    - Injects pure 16:9 AI illustrations as EDITORIAL_HERO every 5-6 slides.
    - Dynamically assigns BENTO_GRID, COMPARISON, PROCESS, and CARDS.
    """
    sections = canonical.get("sections", [])
    source_path = Path(canonical.get("source_path", "Tài Liệu Chuyên Đề"))
    title_text = canonical.get("deck_title", "")
    if not title_text or title_text == "CHUYÊN ĐỀ DÂN SỐ HỌC":
        first_sec = sections[0]["title"] if sections else source_path.stem
        title_text = re.sub(r"^(bài\s*\d+[\.\:\-]?\s*)", "", first_sec, flags=re.IGNORECASE).strip()
        if not title_text or len(title_text) < 3:
            title_text = source_path.stem.replace("_", " ").title()

    all_atoms = [a for s in sections for a in s.get("atoms", [])]
    core_claims = [a["verbatim"] for a in all_atoms if a.get("priority") == "P0" or a.get("semantic_role") == "CORE_DEFINITION"]
    if core_claims:
        primary_cover_claim = extract_pedagogical_sentence(core_claims[0], 28)
    elif all_atoms:
        primary_cover_claim = extract_pedagogical_sentence(all_atoms[0]["verbatim"], 28)
    else:
        primary_cover_claim = f"Hệ thống hóa cơ sở lý luận, phương pháp luận nghiên cứu và phân tích chuyên sâu của {title_text}."

    # Asset Pools for Generic Documents
    AI_ILLUSTRATIONS = [
        "illustration_bai_1.jpg", "ai_bai_1_community.jpg", "ai_bai_1_policy.jpg",
        "cinematic_bai_1_hero.jpg", "illustration_bai_2_structure.jpg", "ai_bai_2_golden.jpg",
        "ai_bai_2_aging.jpg", "ai_bai_2_quality.jpg", "ai_bai_3_fertility.jpg",
        "cinematic_bai_3_health.jpg", "ai_bai_4_distribution.jpg", "ai_bai_4_industrial.jpg",
        "cinematic_bai_4_megacity.jpg", "cinematic_bai_4_urban.jpg", "cinematic_bai_5_forecast.jpg",
        "ai_bai_5_sustainability.jpg"
    ]
    DEMO_CHARTS = [
        "POPULATION_PYRAMID", "AGE_STRUCTURE_RADAR", "SEX_RATIO_BIRTH_HEATMAP",
        "FERTILITY_TRENDS", "MORTALITY_CURVE_GOMPERTZ", "LIFE_EXPECTANCY_WATERFALL",
        "POPULATION_FORECAST_SCENARIOS", "URBANIZATION_SCURVE", "REGIONAL_DENSITY",
        "DEMOGRAPHIC_DIVIDEND_STACKED_AREA", "LABOR_FORCE_DONUT", "HDI_DIMENSIONS",
        "MATH_MODELS"
    ]
    ICONS_PALETTE = ["activity", "target", "trending-up", "book-open", "shield", "users", "award", "zap", "calculator", "sliders"]

    slides = []
    # 1. Cover Slide
    slides.append({
        "slide_id": "SLIDE_01",
        "role": "COVER",
        "section": "TỔNG QUAN CHUYÊN ĐỀ",
        "assertion_title": title_text.upper(),
        "primary_claim": primary_cover_claim,
        "visual_job": "HERO_TITLE",
        "visual_anchor": "BRAND_COVER",
        "illustration": "illustration_bai_1.jpg",
        "speaker_notes": f"Kính chào quý học viên, hôm nay chúng ta nghiên cứu chuyên đề {title_text}.",
        "source_footer": f"Tài liệu đào tạo chuẩn hóa: {source_path.name}"
    })

    slide_counter = 1
    ill_idx = 1
    chart_idx = 0

    for sec in sections:
        sec_title = sec.get("title", "Nội Dung Trọng Tâm").strip()
        sec_clean = re.sub(r"^\d+[\.\:\-]?\s*", "", sec_title).strip() or sec_title
        atoms = sec.get("atoms", [])
        if not atoms:
            continue

        # Separate tables, formulas, and general narrative atoms
        table_atoms = [a for a in atoms if a.get("is_table") or a.get("table_data")]
        formula_atoms = [a for a in atoms if a.get("is_formula") or a.get("semantic_role") == "MATHEMATICAL_FORMULA"]
        narrative_atoms = [a for a in atoms if not (a.get("is_table") or a.get("is_formula"))]

        # 2.1 Render Table Slides
        for t_atom in table_atoms:
            slide_counter += 1
            t_data = t_atom.get("table_data", {})
            slides.append({
                "slide_id": f"SLIDE_{slide_counter:02d}",
                "role": "CONTENT",
                "section": sec_title.upper()[:30],
                "assertion_title": clean_title(f"Bảng Dữ Liệu Thực Chứng: {sec_clean}", 14),
                "primary_claim": clean_summary(t_atom.get("verbatim", "Số liệu thống kê thực chứng phân bổ chi tiết."), 22),
                "visual_job": "DATA_TABLE",
                "visual_anchor": "DATA_TABLE_MATRIX",
                "table_data": t_data,
                "speaker_notes": f"Phân tích bảng số liệu tổng hợp của phần {sec_clean}.",
                "source_footer": f"Nguồn trích dẫn: {source_path.name}"
            })

        # 2.2 Render Formula Slides
        for f_atom in formula_atoms:
            slide_counter += 1
            formula_text = f_atom.get("verbatim", "")
            # Clean formula string: stop before comma, semicolon, period, or 'trong đó'
            f_match = re.search(r"([A-Za-z0-9_]{1,10}\s*=\s*[^,;.\n]+(?:\s*[\*\/\+\-]\s*[^,;.\n]+)*)", formula_text)
            clean_formula = f_match.group(1).strip() if f_match else formula_text[:50]
            if "trong đó" in clean_formula.lower():
                clean_formula = re.split(r"trong đó", clean_formula, flags=re.IGNORECASE)[0].strip()
            
            slides.append({
                "slide_id": f"SLIDE_{slide_counter:02d}",
                "role": "CONTENT",
                "section": sec_title.upper()[:30],
                "assertion_title": clean_title(f"Mô Hình Định Lượng: {sec_clean}", 14),
                "primary_claim": clean_summary(formula_text, 22),
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "TWO_PILLARS",
                "formula": clean_formula,
                "atoms": [
                    {
                        "title": "Công Thức Định Lượng",
                        "text": clean_summary(formula_text, 25),
                        "icon": "calculator"
                    },
                    {
                        "title": "Ý Nghĩa Đo Lường",
                        "text": f"Đo lường chính xác các biến số then chốt phục vụ công tác phân tích và dự báo {sec_clean.lower()}.",
                        "icon": "target"
                    }
                ],
                "speaker_notes": f"Trọng tâm công thức toán học và phương pháp tính của {sec_clean}.",
                "source_footer": f"Phương pháp luận: {source_path.name}"
            })

        # 2.3 Deep Pedagogical Chunking for Narrative Atoms (2-3 atoms per slide)
        chunk_size = 3
        for chunk_idx in range(0, len(narrative_atoms), chunk_size):
            chunk = narrative_atoms[chunk_idx:chunk_idx + chunk_size]
            if not chunk:
                continue

            slide_counter += 1
            has_metric = any(a.get("contains_metric") or a.get("semantic_role") == "STATISTICAL_EVIDENCE" for a in chunk)
            has_contrast = any(a.get("semantic_role") == "DIALECTICAL_PAIR" for a in chunk)
            has_mechanism = any(a.get("semantic_role") == "DYNAMIC_MECHANISM" for a in chunk)

            # Assign Visual Job
            if slide_counter % 5 == 3:
                vjob = "EDITORIAL_HERO"
                current_ill = AI_ILLUSTRATIONS[ill_idx % len(AI_ILLUSTRATIONS)]
                ill_idx += 1
            elif has_metric and DEMO_CHARTS:
                vjob = "CHART_AND_INSIGHTS"
                current_chart = DEMO_CHARTS[chart_idx % len(DEMO_CHARTS)]
                chart_idx += 1
            elif has_contrast:
                vjob = "COMPARISON"
            elif has_mechanism or len(chunk) >= 3:
                vjob = "PROCESS" if chunk_idx > 0 else "BENTO_GRID"
            else:
                vjob = "CARDS"

            # Build card atoms
            card_atoms = []
            for a_idx, atom in enumerate(chunk):
                raw_text = atom.get("verbatim", "")
                card_title = extract_card_concept_title(atom, a_idx)
                card_text = clean_summary(raw_text, 25)
                card_icon = ICONS_PALETTE[(slide_counter + a_idx) % len(ICONS_PALETTE)]
                card_atoms.append({
                    "title": card_title,
                    "text": card_text,
                    "icon": card_icon
                })

            primary_claim = clean_summary(chunk[0].get("verbatim", sec_title), 22)
            
            # Assertion title
            if len(narrative_atoms) > chunk_size:
                part_num = (chunk_idx // chunk_size) + 1
                total_parts = (len(narrative_atoms) + chunk_size - 1) // chunk_size
                assertion_title = clean_title(f"{sec_clean}: {card_atoms[0]['title']} (Phần {part_num}/{total_parts})", 16)
            else:
                assertion_title = clean_title(f"{sec_clean}: {card_atoms[0]['title']}", 16)

            slide_spec = {
                "slide_id": f"SLIDE_{slide_counter:02d}",
                "role": "CONTENT",
                "section": sec_title.upper()[:30],
                "assertion_title": assertion_title,
                "primary_claim": primary_claim,
                "visual_job": vjob,
                "visual_anchor": "SECTION_CARDS",
                "atoms": card_atoms,
                "speaker_notes": f"Nội dung trọng tâm của chuyên đề {sec_title}.",
                "source_footer": f"Tài liệu chuẩn hóa: {source_path.name}"
            }

            if vjob == "EDITORIAL_HERO":
                slide_spec["illustration"] = current_ill
            elif vjob == "CHART_AND_INSIGHTS":
                slide_spec["chart_type"] = current_chart

            slides.append(slide_spec)

    # 3. Summary & Conclusion Slide
    slide_counter += 1
    slides.append({
        "slide_id": f"SLIDE_{slide_counter:02d}",
        "role": "COVER",
        "section": "TỔNG KẾT BÀI HỌC",
        "assertion_title": f"TỔNG KẾT & ĐỊNH HƯỚNG: {title_text.upper()}",
        "primary_claim": "Nắm vững lý thuyết, phương pháp luận và dữ liệu thực chứng là nền tảng cốt lõi cho mọi hành động thực tiễn hiệu quả.",
        "visual_job": "HERO_TITLE",
        "visual_anchor": "BRAND_SUMMARY",
        "speaker_notes": "Cảm ơn quý học viên đã theo dõi. Xin mời thảo luận và đóng góp ý kiến.",
        "source_footer": f"Hoàn thành chuyên đề đào tạo: {source_path.name}"
    })

    return {
        "schema_version": "1.0",
        "lesson_index": 1,
        "deck_title": title_text,
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }


def generate_blueprints_from_canonical(canonical: Dict[str, Any], doc_name: str = "") -> Dict[str, Any]:
    header_str = canonical.get("source_path", "") + " " + (canonical.get("sections", [{}])[0].get("title", ""))
    check_str = (doc_name + " " + header_str).lower()
    
    # Import exhaustive deep curriculum blueprints (106 slides total across 5 core lessons)
    try:
        import curriculum_blueprints_data as cbd
    except ImportError:
        from scripts import curriculum_blueprints_data as cbd

    if any(k in check_str for k in ["bai 1", "bài 1", "bài i", "nhap mon", "nhập môn"]):
        raw_bp = cbd.get_lesson_blueprints_bai_1()
    elif any(k in check_str for k in ["bai 2", "bài 2", "bài ii", "quy mo-co cau", "qui mô", "chất lượng ds", "chat luong ds"]):
        raw_bp = cbd.get_lesson_blueprints_bai_2()
    elif any(k in check_str for k in ["bai 3", "bài 3", "bài iii", "bien dong", "biến động", "mức sinh"]):
        raw_bp = cbd.get_lesson_blueprints_bai_3()
    elif any(k in check_str for k in ["bai 4", "bài 4", "bài iv", "phan bo", "phân bố", "di dan", "đô thị hóa", "do thi hoa"]):
        raw_bp = cbd.get_lesson_blueprints_bai_4()
    elif any(k in check_str for k in ["bai 5", "bài 5", "bài v", "du bao", "dự báo"]):
        raw_bp = cbd.get_lesson_blueprints_bai_5()
    else:
        raw_bp = generate_generic_blueprints(canonical)

    # Route through MACC-QA V7.0 Multi-Agent Content Council for Forensic Review & Refinement
    if ContentMultiAgentCouncil:
        council = ContentMultiAgentCouncil(max_rounds=3)
        all_text = " ".join(
            a.get("verbatim", "") for sec in canonical.get("sections", []) for a in sec.get("atoms", [])
        )
        return council.review_and_refine_blueprints(raw_bp, canonical_text=all_text)
    return raw_bp


def main():
    parser = argparse.ArgumentParser(description="Generate Certified Slide Blueprints")
    parser.add_argument("--canonical", required=True, type=Path, help="Path to canonical-content.json")
    parser.add_argument("--output", required=True, type=Path, help="Path to output slide-blueprints.json")
    parser.add_argument("--name", default="", type=str, help="Optional document name hint")
    args = parser.parse_args()

    with open(args.canonical, "r", encoding="utf-8") as f:
        canonical = json.load(f)

    blueprints = generate_blueprints_from_canonical(canonical, doc_name=args.name or args.canonical.name)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(blueprints, f, ensure_ascii=False, indent=2)

    print(f"Blueprints generated: {blueprints['total_slides']} slides created at {args.output}")


if __name__ == "__main__":
    main()
