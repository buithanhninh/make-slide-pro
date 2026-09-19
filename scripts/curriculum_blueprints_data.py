"""
curriculum_blueprints_data.py
Exhaustive Deep-Curriculum Slide Blueprints for Make Slide Pro V8.3.0.
Contains full academic coverage (106 slides total across 5 core modules):
- Bai 1 (Nhap Mon DSH): 14 slides
- Bai 2 (Quy Mo, Co Cau, Chat Luong DS): 28 slides
- Bai 3 (Bien Dong Tu Nhien DS): 22 slides
- Bai 4 (Phan Bo DS va Di Dan - Do Thi Hoa): 22 slides
- Bai 5 (Du Bao Dan So): 20 slides
Enhanced with 21 Pure AI Illustrations (20%), 24 Publication Demographic Charts (22.6%),
18 Mathematical Formula Cards (17%), and 5 Native Data Tables (4.7%).
"""

from typing import Any, Dict, List

def get_lesson_blueprints_bai_1() -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "lesson_index": 1,
        "deck_title": "Nhập Môn Dân Số Học",
        "total_slides": 14,
        "visual_system": "MODERN_REFINED",
        "slides": [
            {
                "slide_id": "SLIDE_01",
                "role": "COVER",
                "section": "TỔNG QUAN CHUYÊN ĐỀ",
                "assertion_title": "BÀI 1: NHẬP MÔN DÂN SỐ HỌC",
                "primary_claim": "Khung lý thuyết nền tảng về quy mô, cơ cấu, chất lượng và phương pháp luận nghiên cứu Dân số học hiện đại.",
                "visual_job": "HERO_TITLE",
                "visual_anchor": "BRAND_COVER",
                "speaker_notes": "Kính chào quý học viên, hôm nay chúng ta bắt đầu chuyên đề Nhập môn Dân số học nhằm nắm vững các khái niệm và nguyên lý vận động của dân số.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia",
                "illustration": "illustration_bai_1.jpg"
            },
            {
                "slide_id": "SLIDE_02",
                "role": "CONTENT",
                "section": "MỤC TIÊU BÀI HỌC",
                "assertion_title": "Nắm Vững Khái Niệm Cốt Lõi Và Phương Pháp Luận Nghiên Cứu Dân Số Học",
                "primary_claim": "Chuẩn đầu ra yêu cầu học viên làm chủ hệ thống khái niệm nhân khẩu học và vận dụng vào phân tích chính sách phát triển.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_OBJECTIVES",
                "atoms": [
                    {
                        "title": "Hệ Thống Khái Niệm Cốt Lõi",
                        "text": "Làm chủ các khái niệm dân số, dân cư, tái sản xuất dân số và các trạng thái động - tĩnh nhân khẩu học.",
                        "icon": "book-open"
                    },
                    {
                        "title": "Phương Pháp Luận Nghiên Cứu",
                        "text": "Nắm vững kỹ thuật thu thập dữ liệu tổng điều tra, thống kê hộ tịch và các mô hình toán học dự báo dân số.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Ứng Dụng Thực Tiễn Hoạch Định",
                        "text": "Phân tích mối quan hệ hữu cơ giữa dân số với tăng trưởng kinh tế, an sinh xã hội và tài nguyên môi trường.",
                        "icon": "target"
                    }
                ],
                "speaker_notes": "Chuẩn đầu ra được thiết kế theo 3 tầng năng lực: nhận biết khái niệm, phương pháp tính toán và ứng dụng hoạch định.",
                "source_footer": "Khung chuẩn đầu ra chuyên đề"
            },
            {
                "slide_id": "SLIDE_03",
                "role": "CONTENT",
                "section": "BẢN CHẤT DÂN SỐ",
                "assertion_title": "Bản Chất Kép Của Dân Số: Sự Thống Nhất Giữa Thuộc Tính Sinh Học Và Xã Hội",
                "primary_claim": "Dân số vừa mang bản chất sinh học tự nhiên vừa chịu sự chi phối quyết định của các quy luật phát triển xã hội.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Thuộc Tính Tự Nhiên Sinh Học",
                        "text": "Biểu hiện qua các quy luật sinh học như sinh đẻ, lão hóa, giới tính và tử vong tự nhiên của cơ thể con người.",
                        "icon": "activity"
                    },
                    {
                        "title": "Thuộc Tính Kinh Tế Xã Hội",
                        "text": "Chịu sự quy định trực tiếp bởi trình độ phát triển kinh tế, phong tục tập quán, y tế, giáo dục và chính sách an sinh.",
                        "icon": "users"
                    }
                ],
                "speaker_notes": "Cần nhấn mạnh tính chất xã hội là mặt quyết định, biến các hiện tượng sinh học thành đối tượng nghiên cứu khoa học xã hội.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "illustration": "ai_bai_1_community.jpg"
            },
            {
                "slide_id": "SLIDE_04",
                "role": "CONTENT",
                "section": "CẶP KHÁI NIỆM KINH ĐIỂN",
                "assertion_title": "Phân Biệt Bản Chất Giữa Hai Khái Niệm Dân Cư Và Dân Số",
                "primary_claim": "Dân cư là thực thể văn hóa xã hội rộng lớn trong khi dân số là tập hợp được đo lường định lượng thống kê chính xác.",
                "visual_job": "DATA_TABLE",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Khái Niệm Dân Cư (Population Group)",
                        "text": "Toàn bộ con người cùng cư trú trên một vùng lãnh thổ, gắn liền với các mối quan hệ lịch sử, văn hóa, phong tục và cộng đồng.",
                        "icon": "globe"
                    },
                    {
                        "title": "Khái Niệm Dân Số (Demographic Population)",
                        "text": "Tập hợp người được xác định tại một thời điểm cụ thể, được đo đạc định lượng qua quy mô, cơ cấu tuổi, giới tính và biến động sinh tử di cư.",
                        "icon": "bar-chart-2"
                    }
                ],
                "speaker_notes": "Sự nhầm lẫn giữa dân cư và dân số rất phổ biến; dân số học tập trung vào khía cạnh định lượng và các biến động của tập hợp người.",
                "source_footer": "Hội đồng Thẩm định Học thuật Dân số học",
                "table_data": {
                    "headers": [
                        "Tiêu Chí So Sánh",
                        "Dân Cư (Geography)",
                        "Dân Số (Demography)",
                        "Ý Nghĩa Quản Trị"
                    ],
                    "rows": [
                        [
                            "Bản Chất Khái Niệm",
                            "Tập hợp người sinh sống trên một lãnh thổ địa lý",
                            "Tập hợp người gắn liền tái sản xuất, sinh tử và cơ cấu",
                            "Xác định rõ đối tượng"
                        ],
                        [
                            "Góc Độ Tiếp Cận",
                            "Không gian địa lý, phân bố cư trú và cảnh quan",
                            "Quy luật sinh học, kinh tế và biến động nhân khẩu",
                            "Đo lường tỷ suất chuẩn"
                        ],
                        [
                            "Thuộc Tính Thống Kê",
                            "Phản ánh dung lượng cư trú và mật độ lãnh thổ",
                            "Phân rã chi tiết theo tuổi, giới tính, học vấn",
                            "Cơ sở phân bổ ngân sách"
                        ],
                        [
                            "Phạm Vi Ứng Dụng",
                            "Địa lý kinh tế, quy hoạch giao thông, tài nguyên",
                            "Chính sách dân số, an sinh xã hội và thị trường",
                            "Hoạch định chiến lược dài hạn"
                        ]
                    ],
                    "col_widths": [
                        0.2,
                        0.28,
                        0.28,
                        0.24
                    ]
                }
            },
            {
                "slide_id": "SLIDE_05",
                "role": "CONTENT",
                "section": "TRẠNG THÁI DÂN SỐ",
                "assertion_title": "Hai Trạng Thái Tồn Tại Của Dân Số: Trạng Thái Tĩnh Và Trạng Thái Động",
                "primary_claim": "Nghiên cứu dân số đòi hỏi kết hợp đồng thời việc chụp cắt lớp tại một thời điểm và theo dõi dòng chảy vận động qua thời gian.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Trạng Thái Tĩnh (Static Demography)",
                        "text": "Phản ánh quy mô tổng thể và cơ cấu dân số theo độ tuổi, giới tính tại một thời điểm cố định như thời điểm tổng điều tra.",
                        "icon": "clock"
                    },
                    {
                        "title": "Trạng Thái Động (Dynamic Demography)",
                        "text": "Sự vận động liên tục của dân số theo thời gian thông qua hai kênh: biến động tự nhiên (sinh, chết) và biến động cơ học (di cư).",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Trạng thái tĩnh cho biết bức tranh hiện tại, còn trạng thái động phản ánh quy luật chuyển dịch và xu hướng tương lai.",
                "source_footer": "Giáo trình Dân số học đại cương"
            },
            {
                "slide_id": "SLIDE_06",
                "role": "CONTENT",
                "section": "QUÁ TRÌNH DÂN SỐ",
                "assertion_title": "Ba Quá Trình Dân Số Cơ Bản Quyết Định Quy Mô Và Cấu Trúc Nhân Khẩu",
                "primary_claim": "Sinh đẻ, tử vong và di cư là ba biến số nền tảng chi phối toàn bộ sự phát triển và cân bằng của hệ thống dân số.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "THREE_PILLARS",
                "atoms": [
                    {
                        "title": "Mức Sinh (Fertility)",
                        "text": "Biến số bù đắp số lượng, chịu sự chi phối của độ tuổi kết hôn, chi phí nuôi dạy con và chính sách kế hoạch hóa gia đình.",
                        "icon": "activity"
                    },
                    {
                        "title": "Mức Chết (Mortality)",
                        "text": "Biến số suy giảm tự nhiên, phản ánh điều kiện vệ sinh phòng bệnh, mức sống và chất lượng mạng lưới y tế điều trị.",
                        "icon": "shield"
                    },
                    {
                        "title": "Di Cư (Migration)",
                        "text": "Biến số phân bổ lại không gian, tạo ra sự chuyển dịch lao động và tái cấu trúc mạng lưới đô thị - nông thôn.",
                        "icon": "shuffle"
                    }
                ],
                "speaker_notes": "Ba quá trình này luôn tác động tương hỗ; sự thay đổi của một yếu tố sẽ kéo theo sự điều chỉnh của toàn bộ hệ thống.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia",
                "chart_type": "CENSUS_DATA_COLLECTION_FLOW"
            },
            {
                "slide_id": "SLIDE_07",
                "role": "CONTENT",
                "section": "TÁI SẢN XUẤT DÂN SỐ",
                "assertion_title": "Quá Trình Tái Sản Xuất Dân Số Xét Theo Nghĩa Hẹp Và Nghĩa Rộng",
                "primary_claim": "Tái sản xuất dân số không chỉ đơn thuần là sinh sôi thế hệ mà còn là sự tái sản xuất toàn bộ năng lực thể chất và trí tuệ xã hội.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Tái Sản Xuất Nghĩa Hẹp (Natural Replacement)",
                        "text": "Quá trình thay thế liên tục các thế hệ thông qua quan hệ sinh - chết, duy trì sự tồn tại sinh học liên tục của quần thể người.",
                        "icon": "refresh-cw"
                    },
                    {
                        "title": "Tái Sản Xuất Nghĩa Rộng (Social Reproduction)",
                        "text": "Bao gồm việc tái tạo sức lao động, nâng cao trình độ văn hóa, chuyên môn nghề nghiệp và chuyển dịch cơ cấu vị thế xã hội.",
                        "icon": "briefcase"
                    }
                ],
                "speaker_notes": "Ở các quốc gia hiện đại, tái sản xuất nghĩa rộng ngày càng đóng vai trò trọng yếu trong việc nâng cao năng suất quốc gia.",
                "source_footer": "Giáo trình Dân số học đại cương"
            },
            {
                "slide_id": "SLIDE_08",
                "role": "CONTENT",
                "section": "PHẠM VI NGHIÊN CỨU",
                "assertion_title": "Phạm Vi Nghiên Cứu Đa Chiều Và Tính Liên Ngành Của Dân Số Học",
                "primary_claim": "Dân số học nằm ở giao lộ của nhiều ngành khoa học từ toán học thống kê, y học xã hội đến kinh tế học và xã hội học.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Dân Số Học Hình Thức (Formal Demography)",
                        "text": "Nghiên cứu định lượng thuần túy về quy mô, cấu trúc và các mô hình toán học biểu diễn biến động nhân khẩu.",
                        "icon": "compass"
                    },
                    {
                        "title": "Kinh Tế Học Dân Số (Economic Demography)",
                        "text": "Phân tích tác động của cơ cấu tuổi đến tích lũy vốn, quỹ lương, thị trường lao động và tăng trưởng GDP.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "Xã Hội Học Dân Số (Social Demography)",
                        "text": "Nghiên cứu mối quan hệ giữa biến động dân số với gia đình, tôn giáo, bất bình đẳng xã hội và đô thị hóa.",
                        "icon": "users"
                    }
                ],
                "speaker_notes": "Tính liên ngành giúp dân số học cung cấp bức tranh toàn cảnh cho các nhà hoạch định chiến lược kinh tế xã hội.",
                "source_footer": "Khung chương trình đào tạo Dân số học",
                "illustration": "cinematic_bai_1_system.jpg"
            },
            {
                "slide_id": "SLIDE_09",
                "role": "CONTENT",
                "section": "PHƯƠNG PHÁP NGHIÊN CỨU",
                "assertion_title": "Bốn Bước Phương Pháp Luận Chuẩn Mực Trong Nghiên Cứu Dân Số Học",
                "primary_claim": "Từ thu thập dữ liệu nguồn đến mô hình hóa dự báo, quy trình nghiên cứu dân số bảo đảm tính khoa học thực chứng cao nhất.",
                "visual_job": "PROCESS",
                "visual_anchor": "FOUR_STEPS",
                "atoms": [
                    {
                        "title": "1. Thu Thập Dữ Liệu Nguồn",
                        "text": "Tiến hành Tổng điều tra dân số định kỳ 10 năm, điều tra biến động dân số hàng năm và thu thập số liệu đăng ký hộ tịch.",
                        "icon": "database"
                    },
                    {
                        "title": "2. Đo Lường Thống Kê Chuẩn",
                        "text": "Tính toán các tỷ suất thô, tỷ suất đặc trưng theo tuổi, tỷ số phụ thuộc và xây dựng tháp tuổi - giới tính.",
                        "icon": "pie-chart"
                    },
                    {
                        "title": "3. Phân Tích Cơ Chế Nhân Quả",
                        "text": "Khảo sát các yếu tố kinh tế, văn hóa, chính sách y tế chi phối đến hành vi sinh sản, tử vong và di cư.",
                        "icon": "search"
                    },
                    {
                        "title": "4. Mô Hình Hóa & Dự Báo",
                        "text": "Ứng dụng phương pháp thành phần nhân khẩu (Cohort Component) để xây dựng các kịch bản dự báo dân số tương lai.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Bốn bước này cấu thành chu trình nghiên cứu khép kín, làm cơ sở tin cậy cho việc lập kế hoạch ngân sách quốc gia.",
                "source_footer": "Giáo trình Phương pháp nghiên cứu Dân số"
            },
            {
                "slide_id": "SLIDE_10",
                "role": "CONTENT",
                "section": "Ý NGHĨA HOẠCH ĐỊNH",
                "assertion_title": "Mối Quan Hệ Biện Chứng Giữa Dân Số Và Chiến Lược Phát Triển Đất Nước",
                "primary_claim": "Dân số vừa là mục tiêu tối thượng vừa là nguồn lực quyết định tốc độ và chất lượng phát triển bền vững quốc gia.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "BENTO_POLICY",
                "atoms": [
                    {
                        "title": "Dân Số Là Nguồn Lực Lao Động",
                        "text": "Quy mô và chất lượng nguồn nhân lực quyết định trực tiếp tiềm năng tăng trưởng kinh tế và năng lực hấp thụ vốn đầu tư FDI.",
                        "icon": "users"
                    },
                    {
                        "title": "Cơ Sở Hoạch Định Dịch Vụ Công",
                        "text": "Cơ cấu lứa tuổi định hình chính xác nhu cầu xây dựng trường học, mạng lưới bệnh viện và hệ thống bảo hiểm hưu trí.",
                        "icon": "home"
                    },
                    {
                        "title": "Dân Số Là Mục Tiêu Phục Vụ",
                        "text": "Mọi thành quả phát triển kinh tế cuối cùng đều hướng tới mục tiêu nâng cao chất lượng cuộc sống và tuổi thọ người dân.",
                        "icon": "heart"
                    }
                ],
                "speaker_notes": "Chính sách kinh tế nếu tách rời quy luật nhân khẩu học sẽ luôn đối mặt rủi ro mất cân đối cơ cấu và quá tải hạ tầng.",
                "source_footer": "Nghị quyết 21-NQ/TW về công tác dân số",
                "illustration": "ai_bai_1_policy.jpg"
            },
            {
                "slide_id": "SLIDE_11",
                "role": "CONTENT",
                "section": "BỐI CẢNH VIỆT NAM",
                "assertion_title": "Bối Cảnh Dân Số Việt Nam: Cột Mốc 100 Triệu Dân Và Thời Kỳ Dân Số Vàng",
                "primary_claim": "Việt Nam chính thức gia nhập nhóm các quốc gia trên 100 triệu dân với tỷ lệ người trong độ tuổi lao động đạt đỉnh lịch sử.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "POPULATION_METRICS",
                "atoms": [
                    {
                        "title": "100.3 Triệu Người (2024)",
                        "text": "Việt Nam xếp thứ 3 khu vực Đông Nam Á và đứng thứ 15 trên thế giới về quy mô dân số, tạo thị trường tiêu dùng nội địa rộng lớn.",
                        "icon": "users"
                    },
                    {
                        "title": "68.0% Độ Tuổi Lao Động",
                        "text": "Thời kỳ cơ cấu dân số vàng với tỷ số phụ thuộc chung dưới 50%, mang lại lợi thế cạnh tranh lớn về lực lượng lao động dồi dào.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Thách Thức Năng Suất",
                        "text": "Tỷ lệ lao động qua đào tạo có chứng chỉ mới đạt khoảng 28%, đòi hỏi cấp thiết phải nâng cao chất lượng kỹ năng nghề.",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "Quy mô dân số tròn 100 triệu người là dấu mốc tự hào, nhưng thách thức nâng cao giá trị gia tăng lao động là nhiệm vụ sống còn.",
                "source_footer": "Tổng cục Thống kê - Kết quả Tổng điều tra dân số"
            },
            {
                "slide_id": "SLIDE_12",
                "role": "CONTENT",
                "section": "THÁCH THỨC CẤP BÁCH",
                "assertion_title": "Ba Thách Thức Nhân Khẩu Học Cấp Bách Cần Giải Pháp Căn Cơ",
                "primary_claim": "Mức sinh giảm thấp, già hóa dân số với tốc độ nhanh và mất cân bằng giới tính khi sinh đang đe dọa cơ cấu bền vững tương lai.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "THREE_CHALLENGES",
                "atoms": [
                    {
                        "title": "Mức Sinh Giảm Sâu Đô Thị",
                        "text": "Tổng tỷ suất sinh tại TP.HCM và vùng Đông Nam Bộ xuống dưới 1.5 con/phụ nữ, đối mặt nguy cơ suy giảm dân số dài hạn.",
                        "icon": "trending-down"
                    },
                    {
                        "title": "Già Hóa Trước Khi Giàu",
                        "text": "Thời gian chuyển từ già hóa (7%) sang dân số già (14%) chưa đầy 20 năm, tạo sức ép khổng lồ lên quỹ bảo hiểm và hệ thống y tế.",
                        "icon": "shield-alert"
                    },
                    {
                        "title": "Mất Cân Bằng Giới Tính (SRB)",
                        "text": "Tỷ số giới tính khi sinh duy trì mức cao 112 bé trai / 100 bé gái, tiềm ẩn nguy cơ dư thừa 1.5 triệu nam giới vào năm 2034.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Đây là ba vấn đề được Nghị quyết 21 chỉ rõ cần sự vào cuộc đồng bộ của cả hệ thống chính trị và toàn xã hội.",
                "source_footer": "Báo cáo thực trạng dân số Việt Nam 2024",
                "illustration": "cinematic_bai_1_hero.jpg"
            },
            {
                "slide_id": "SLIDE_13",
                "role": "CONTENT",
                "section": "LỘ TRÌNH HÀNH ĐỘNG",
                "assertion_title": "Khung Lộ Trình Hành Động Chiến Lược Cho Nhà Hoạch Định Đến Năm 2045",
                "primary_claim": "Chuyển hướng trọng tâm chính sách từ kế hoạch hóa gia đình sang dân số và phát triển toàn diện mọi phương diện.",
                "visual_job": "DATA_TABLE",
                "visual_anchor": "THREE_HORIZONS",
                "atoms": [
                    {
                        "title": "2024 - 2030: Bứt Phá Cơ Cấu Vàng",
                        "text": "Tối đa hóa việc làm chất lượng cao, đào tạo kỹ năng số cho 70% lao động, nâng cao năng suất trước khi già hóa dân số ập đến.",
                        "icon": "zap"
                    },
                    {
                        "title": "2030 - 2040: Thích Ứng Già Hóa",
                        "text": "Cải cách bảo hiểm xã hội đa tầng, hoàn thiện mạng lưới y tế lão khoa và phát triển thị trường kinh tế bạc (Silver Economy).",
                        "icon": "shield"
                    },
                    {
                        "title": "Tầm Nhìn 2045: Nâng Tầm Vóc Việt",
                        "text": "Đưa chỉ số phát triển con người HDI vào nhóm rất cao (>0.800), bảo đảm an sinh bền vững cho mọi thế hệ công dân.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Lộ trình 3 giai đoạn giúp phân kỳ nguồn lực đầu tư ngân sách công và huy động sự tham gia của khu vực tư nhân.",
                "source_footer": "Chiến lược Dân số Việt Nam đến năm 2030"
            },
            {
                "slide_id": "SLIDE_14",
                "role": "CONTENT",
                "section": "TỔNG KẾT BÀI HỌC",
                "assertion_title": "Tổng Kết Kiến Thức Trọng Tâm Chuyên Đề Nhập Môn Dân Số Học",
                "primary_claim": "Nắm vững lý luận và phương pháp luận nhân khẩu học là chìa khóa để phân tích khoa học các biến động dân số và phát triển.",
                "visual_job": "CARDS",
                "visual_anchor": "SUMMARY_QUESTIONS",
                "atoms": [
                    {
                        "title": "Câu Hỏi Lý Thuyết 1",
                        "text": "Phân tích sự khác biệt bản chất giữa hai khái niệm Dân cư và Dân số. Lấy ví dụ minh chứng trong thực tế quản lý nhà nước.",
                        "icon": "help-circle"
                    },
                    {
                        "title": "Câu Hỏi Phân Tích 2",
                        "text": "Tại sao nói dân số vừa mang thuộc tính sinh học vừa mang thuộc tính xã hội? Mặt nào đóng vai trò quyết định và vì sao?",
                        "icon": "help-circle"
                    },
                    {
                        "title": "Tình Huống Thực Tiễn 3",
                        "text": "Đánh giá các cơ hội và thách thức của thời kỳ dân số vàng với 68% lao động tại địa phương công tác. Đề xuất giải pháp phát huy.",
                        "icon": "message-square"
                    }
                ],
                "speaker_notes": "Học viên chuẩn bị thảo luận nhóm theo 3 câu hỏi trên. Xin cảm ơn quý vị đã chú ý theo dõi.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
            }
        ]
    }


def get_lesson_blueprints_bai_2() -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "lesson_index": 2,
        "deck_title": "Quy Mô, Cơ Cấu Và Chất Lượng Dân Số",
        "total_slides": 28,
        "visual_system": "MODERN_REFINED",
        "slides": [
            {
                "slide_id": "SLIDE_01",
                "role": "COVER",
                "section": "TỔNG QUAN CHUYÊN ĐỀ",
                "assertion_title": "BÀI 2: QUY MÔ, CƠ CẤU VÀ CHẤT LƯỢNG DÂN SỐ",
                "primary_claim": "Hệ thống chỉ báo đo lường động lực học dân số, các mô hình tháp tuổi - giới tính và nâng cao chất lượng dân số Việt Nam.",
                "visual_job": "HERO_TITLE",
                "visual_anchor": "BRAND_COVER",
                "speaker_notes": "Chào các bạn, Bài 2 cung cấp toàn bộ công cụ định lượng cốt lõi để đo lường quy mô, cơ cấu tuổi - giới tính và chất lượng dân số.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia",
                "illustration": "illustration_bai_2.jpg"
            },
            {
                "slide_id": "SLIDE_02",
                "role": "CONTENT",
                "section": "MỤC TIÊU BÀI HỌC",
                "assertion_title": "Năng Lực Tính Toán Chỉ Số Đo Lường Và Đánh Giá Biến Động Sinh Tử Di Cư",
                "primary_claim": "Học viên làm chủ các công thức cân bằng dân số, phân tích tháp dân số và nhận diện các vấn đề chất lượng dân số tại Việt Nam.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_OBJECTIVES",
                "atoms": [
                    {
                        "title": "Năng Lực Đo Lường Định Lượng",
                        "text": "Làm chủ phương trình cân bằng dân số, các công thức tính dân số trung bình, tỷ số giới tính và tỷ số phụ thuộc.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Nhận Diện Dân Số Vàng & Già Hóa",
                        "text": "Đánh giá cơ hội lịch sử từ cơ cấu dân số vàng với 68% lao động và nhận diện thách thức già hóa dân số diễn ra với tốc độ rất nhanh.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Nâng Cao Chất Lượng Toàn Diện",
                        "text": "Nắm vững chỉ số phát triển con người HDI, các chỉ báo sức khỏe thể chất, giáo dục và chính sách nâng cao thể trạng dân số.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Chuẩn đầu ra nhấn mạnh khả năng tính toán định lượng các chỉ số quy mô và hiểu sâu cơ cấu dân số vàng.",
                "source_footer": "Khung chuẩn đầu ra chuyên đề"
            },
            {
                "slide_id": "SLIDE_03",
                "role": "CONTENT",
                "section": "QUY MÔ DÂN SỐ",
                "assertion_title": "Khái Niệm Quy Mô Dân Số Và Thời Điểm Thống Kê Xác Định",
                "primary_claim": "Quy mô dân số là tổng số người sống trong một lãnh thổ tại một thời điểm xác định, là chỉ báo quy mô cơ bản nhất.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Khái Niệm Quy Mô Dân Số",
                        "text": "Tổng số dân sinh sống thường trú trên một đơn vị hành chính lãnh thổ nhất định, đo lường sức chứa và tầm vóc quốc gia.",
                        "icon": "users"
                    },
                    {
                        "title": "Thời Điểm Thống Kê (Census Time)",
                        "text": "Quy ước thời điểm đo đạc chuẩn mực (ví dụ 0 giờ ngày 1 tháng 4 trong các kỳ Tổng điều tra dân số tại Việt Nam).",
                        "icon": "calendar"
                    }
                ],
                "speaker_notes": "Quy mô dân số luôn gắn chặt với thời điểm xác định vì dân số liên tục biến động từng giây từng phút.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "illustration": "illustration_bai_2_structure.jpg"
            },
            {
                "slide_id": "SLIDE_04",
                "role": "CONTENT",
                "section": "ĐO LƯỜNG QUY MÔ",
                "assertion_title": "Chỉ Số Dân Số Trung Bình Và Ứng Dụng Làm Mẫu Số Cho Mọi Tỷ Suất",
                "primary_claim": "Dân số trung bình phản ánh quy mô bình quân trong thời kỳ nghiên cứu, loại trừ sai số do tăng giảm dân số giữa kỳ.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Công Thức Số Học Đơn Giản",
                        "text": "P_tb = (P_0 + P_t) / 2. Áp dụng khi quy mô dân số gia tăng đều đặn qua các tháng trong năm dương lịch.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Công Thức Thời Điểm Có Trọng Số",
                        "text": "P_tb = [0.5*P_1 + P_2 + P_3 + 0.5*P_n] / (n - 1). Áp dụng khi có số liệu thống kê tại nhiều mốc thời điểm trong năm.",
                        "icon": "layers"
                    },
                    {
                        "title": "Ý Nghĩa Thực Tiễn Mẫu Số",
                        "text": "Là mẫu số bắt buộc để tính toán các tỷ suất sinh thô (CBR), tỷ suất chết thô (CDR) và thu nhập bình quân đầu người.",
                        "icon": "check-circle"
                    }
                ],
                "speaker_notes": "Trong phân tích dân số học, không bao giờ dùng dân số đầu kỳ hay cuối kỳ làm mẫu số tính tỷ suất mà phải dùng dân số trung bình.",
                "source_footer": "Nguyên lý thống kê dân số",
                "formula": "P_tb = (P_0 + P_t) / 2 = [0.5*P_1 + P_2 + P_3 + 0.5*P_n] / (n - 1)"
            },
            {
                "slide_id": "SLIDE_05",
                "role": "CONTENT",
                "section": "PHƯƠNG TRÌNH CÂN BẰNG",
                "assertion_title": "Phương Trình Cân Bằng Dân Số Cơ Bản Xác Định Biến Động Qua Thời Gian",
                "primary_claim": "Dân số thời điểm t bằng dân số thời điểm gốc cộng gia tăng tự nhiên và gia tăng cơ học trong kỳ nghiên cứu.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "FOUR_COMPONENTS",
                "atoms": [
                    {
                        "title": "Dân Số Thời Điểm Gốc (P_0)",
                        "text": "Quy mô dân số ban đầu tại thời điểm xuất phát điểm được kiểm kê hoặc ước lượng chính xác.",
                        "icon": "database"
                    },
                    {
                        "title": "Số Sinh Sống (Births - B)",
                        "text": "Tổng số trẻ em sinh ra còn sống trong suốt khoảng thời gian từ thời điểm 0 đến thời điểm t.",
                        "icon": "plus-circle"
                    },
                    {
                        "title": "Số Người Tử Vong (Deaths - D)",
                        "text": "Tổng số ca tử vong xảy ra trong quần thể dân số trong khoảng thời gian nghiên cứu.",
                        "icon": "minus-circle"
                    },
                    {
                        "title": "Di Cư Thuần (Net Migration: I - O)",
                        "text": "Chênh lệch giữa số người nhập cư (In-migrants) và số người xuất cư (Out-migrants) của địa phương.",
                        "icon": "shuffle"
                    }
                ],
                "speaker_notes": "Phương trình cân bằng Pt = P0 + (B - D) + (I - O) là định luật bảo toàn cơ bản nhất trong khoa học dân số học.",
                "source_footer": "Phương trình cân bằng dân số quốc tế",
                "formula": "P_t = P_0 + (B - D) + (I - O) = P_0 + N_i + N_m"
            },
            {
                "slide_id": "SLIDE_06",
                "role": "CONTENT",
                "section": "TĂNG TRƯỞNG DÂN SỐ",
                "assertion_title": "Ba Thước Đo Tăng Trưởng Dân Số: Tự Nhiên, Cơ Học Và Tăng Tổng Số",
                "primary_claim": "Tỷ lệ gia tăng dân số tổng số là tổng hòa của biến động sinh tử tự nhiên và dòng di chuyển cư trú cơ học.",
                "visual_job": "COMPARISON",
                "visual_anchor": "THREE_RATES",
                "atoms": [
                    {
                        "title": "Tỷ Lệ Tăng Tự Nhiên (r)",
                        "text": "r = CBR - CDR. Tỷ lệ phần trăm chênh lệch giữa tỷ suất sinh thô và tỷ suất chết thô của dân số trong năm.",
                        "icon": "activity"
                    },
                    {
                        "title": "Tỷ Lệ Tăng Cơ Học (m)",
                        "text": "m = IR - OR. Chênh lệch giữa tỷ suất nhập cư và xuất cư trên một nghìn dân trung bình.",
                        "icon": "navigation"
                    },
                    {
                        "title": "Tỷ Lệ Tăng Tổng Số (r_g)",
                        "text": "r_g = r + m = ((P_t - P_0) / P_tb) * 100%. Phản ánh tốc độ mở rộng thực tế của quy mô dân số địa phương.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Ở cấp độ toàn cầu di cư bằng 0 nên tăng tổng số bằng tăng tự nhiên; nhưng ở cấp tỉnh/thành phố, tăng cơ học có thể chiếm ưu thế.",
                "source_footer": "Hệ thống chỉ tiêu thống kê quốc gia"
            },
            {
                "slide_id": "SLIDE_07",
                "role": "CONTENT",
                "section": "MÔ HÌNH HÀM MŨ",
                "assertion_title": "Tốc Độ Gia Tăng Dân Số Và Mô Hình Tăng Trưởng Hàm Số Mũ Liên Tục",
                "primary_claim": "Sự sinh sôi dân số diễn ra liên tục theo thời gian được mô hình hóa chính xác nhất bằng hàm số mũ tự nhiên.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Mô Hình Tăng Trưởng Hàm Mũ",
                        "text": "P_t = P_0 * e^(r*t). Với r là tỷ lệ tăng trưởng liên tục hàng năm, e là cơ số logarit tự nhiên (xấp xỉ 2.71828).",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Xác Định Tỷ Lệ Tăng Trưởng (r)",
                        "text": "r = [ln(P_t / P_0)] / t. Cho phép tính toán chính xác tốc độ tăng trưởng bình quân giữa hai kỳ điều tra dân số.",
                        "icon": "calculator"
                    }
                ],
                "speaker_notes": "Mô hình hàm số mũ phản ánh bản chất lãi kép sinh học của quá trình gia tăng dân số.",
                "source_footer": "Mô hình toán học dân số",
                "formula": "P_t = P_0 * e^(r*t)  ==>  r = [ln(P_t / P_0)] / t",
                "chart_type": "SEX_RATIO_BIRTH_HEATMAP"
            },
            {
                "slide_id": "SLIDE_08",
                "role": "CONTENT",
                "section": "THỜI GIAN NHÂN ĐÔI",
                "assertion_title": "Quy Tắc 70 Và Thời Gian Nhân Đôi Quy Mô Dân Số (Doubling Time)",
                "primary_claim": "Thời gian cần thiết để quy mô dân số tăng gấp đôi là chỉ báo trực quan về áp lực gia tăng dân số lên hạ tầng.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "BENTO_DOUBLING",
                "atoms": [
                    {
                        "title": "Công Thức Thời Gian Nhân Đôi (T_2)",
                        "text": "T_2 = ln(2) / r ≈ 70 / r(%). Nếu dân số tăng 1.0%/năm thì sau đúng 70 năm quy mô dân số sẽ tăng gấp đôi.",
                        "icon": "clock"
                    },
                    {
                        "title": "Áp Lực Lên Hệ Thống Hạ Tầng",
                        "text": "Thời gian nhân đôi càng ngắn đòi hỏi quốc gia phải tăng gấp đôi trường học, bệnh viện, nhà ở và năng lượng trong cùng thời gian.",
                        "icon": "alert-triangle"
                    },
                    {
                        "title": "Ứng Dụng Trong Cảnh Báo Sớm",
                        "text": "Là công cụ trực quan giúp các nhà hoạch định chính sách hình dung tốc độ cạn kiệt tài nguyên nếu không kiểm soát mức sinh.",
                        "icon": "shield"
                    }
                ],
                "speaker_notes": "Quy tắc 70 là công cụ ước tính kinh điển giúp giải thích áp lực dân số cho công chúng và các nhà quản lý.",
                "source_footer": "Sổ tay nhân khẩu học ứng dụng",
                "formula": "T_2 = ln(2) / r ≈ 70 / r(%)  (Quy tắc 70 nhân đôi dân số)"
            },
            {
                "slide_id": "SLIDE_09",
                "role": "CONTENT",
                "section": "QUY MÔ DÂN SỐ VN",
                "assertion_title": "Tiến Trình Gia Tăng Quy Mô Dân Số Việt Nam Qua Các Kỳ Tổng Điều Tra",
                "primary_claim": "Dân số Việt Nam tăng gấp đôi từ 52.7 triệu người (1979) lên hơn 100 triệu người (2024), nhưng tốc độ tăng đã chậm lại rõ rệt.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "AGE_STRUCTURE_RADAR",
                "atoms": [
                    {
                        "title": "1979: 52.7 Triệu Dân",
                        "text": "Tốc độ gia tăng dân số thời kỳ sau chiến tranh rất cao, vượt ngưỡng 2.1%/năm do mức sinh còn cao.",
                        "icon": "users"
                    },
                    {
                        "title": "2019: 96.2 Triệu Dân",
                        "text": "Tốc độ tăng dân số bình quân giai đoạn 2009-2019 giảm xuống còn 1.14%/năm nhờ chính sách kế hoạch hóa gia đình.",
                        "icon": "bar-chart-2"
                    },
                    {
                        "title": "2024: Vượt 100.3 Triệu Dân",
                        "text": "Quy mô đạt mốc lịch sử nhưng tỷ lệ gia tăng dân số hiện chỉ còn dưới 0.9%/năm và đang tiếp tục xu hướng giảm.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Số liệu các kỳ Tổng điều tra cho thấy Việt Nam đã thành công trong kiểm soát quy mô nhưng đang đứng trước bài toán già hóa.",
                "source_footer": "Tổng cục Thống kê - Dữ liệu chuỗi thời gian 1979-2024"
            },
            {
                "slide_id": "SLIDE_10",
                "role": "CONTENT",
                "section": "CƠ CẤU DÂN SỐ",
                "assertion_title": "Khái Niệm Cơ Cấu Dân Số Và Ý Nghĩa Chi Phí Xã Hội Trong Hoạch Định",
                "primary_claim": "Cơ cấu dân số phân chia tổng thể dân số thành các bộ phận hợp thành theo các tiêu thức sinh học và xã hội xác định.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Cơ Cấu Tự Nhiên Sinh Học",
                        "text": "Phân chia theo độ tuổi và giới tính. Đây là cơ cấu khách quan, ít biến đổi đột ngột và mang tính quy luật sinh học cao.",
                        "icon": "activity"
                    },
                    {
                        "title": "Cơ Cấu Xã Hội - Kinh Tế",
                        "text": "Phân chia theo học vấn, nghề nghiệp, dân tộc, tôn giáo và tình trạng hôn nhân, phản ánh trình độ tiến hóa xã hội.",
                        "icon": "briefcase"
                    }
                ],
                "speaker_notes": "Phân tích cơ cấu dân số có ý nghĩa thực tiễn cao hơn quy mô đơn thuần vì nó quyết định loại nhu cầu xã hội cần phục vụ.",
                "source_footer": "Giáo trình Dân số học đại cương"
            },
            {
                "slide_id": "SLIDE_11",
                "role": "CONTENT",
                "section": "CƠ CẤU THEO TUỔI",
                "assertion_title": "Ba Khoảng Tuổi Sinh Học Cơ Bản Trong Phân Tích Cơ Cấu Lực Lượng Lao Động",
                "primary_claim": "Tương quan tỷ lệ giữa 3 nhóm tuổi định hình trực tiếp mô hình tiêu dùng, gánh nặng phụ thuộc và tiềm năng sản xuất quốc gia.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "THREE_AGE_GROUPS",
                "atoms": [
                    {
                        "title": "Nhóm Trẻ Em (0 - 14 Tuổi)",
                        "text": "Nhóm dân số dưới độ tuổi lao động, tiêu dùng nhiều dịch vụ nhi khoa, dinh dưỡng và hệ thống giáo dục phổ thông.",
                        "icon": "smile"
                    },
                    {
                        "title": "Nhóm Lao Động (15 - 64 Tuổi)",
                        "text": "Lực lượng trực tiếp tạo ra của cải vật chất, đóng góp thuế, tiết kiệm và đóng bảo hiểm xã hội nuôi sống các nhóm phụ thuộc.",
                        "icon": "user-check"
                    },
                    {
                        "title": "Nhóm Người Cao Tuổi (65+ Tuổi)",
                        "text": "Nhóm hết tuổi lao động, có nhu cầu lớn về dịch vụ an sinh hưu trí, chăm sóc y tế lão khoa và hỗ trợ sinh hoạt dài hạn.",
                        "icon": "heart"
                    }
                ],
                "speaker_notes": "Phân loại 3 nhóm tuổi theo chuẩn quốc tế của Liên Hợp Quốc là cơ sở tính toán các tỷ số phụ thuộc nhân khẩu học.",
                "source_footer": "Chuẩn phân loại Liên Hợp Quốc (UN DESA)",
                "illustration": "ai_bai_2_golden.jpg"
            },
            {
                "slide_id": "SLIDE_12",
                "role": "CONTENT",
                "section": "TỶ SỐ PHỤ THUỘC",
                "assertion_title": "Hệ Thống Ba Tỷ Số Phụ Thuộc: Trẻ Em, Người Già Và Phụ Thuộc Chung",
                "primary_claim": "Tỷ số phụ thuộc đo lường số lượng người không trong độ tuổi lao động mà 100 người trong độ tuổi lao động phải gánh vác.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "DEPENDENCY_RATIOS",
                "atoms": [
                    {
                        "title": "Tỷ Số Phụ Thuộc Trẻ Em (YDR)",
                        "text": "YDR = (Dân số 0-14 / Dân số 15-64) * 100. Đo lường gánh nặng nuôi dạy thế hệ tương lai.",
                        "icon": "pie-chart"
                    },
                    {
                        "title": "Tỷ Số Phụ Thuộc Người Già (ADR)",
                        "text": "ADR = (Dân số 65+ / Dân số 15-64) * 100. Đo lường gánh nặng an sinh và chăm sóc người cao tuổi.",
                        "icon": "shield"
                    },
                    {
                        "title": "Tỷ Số Phụ Thuộc Chung (CDR)",
                        "text": "CDR = YDR + ADR. Khi CDR < 50, quốc gia chính thức bước vào thời kỳ cơ cấu dân số vàng quý giá.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "CDR càng thấp thì gánh nặng nuôi người ăn theo càng nhẹ, xã hội có điều kiện tích lũy vốn đầu tư phát triển.",
                "source_footer": "Phương pháp tính toán nhân khẩu học",
                "formula": "TDR = [(P_0-14 + P_65+) / P_15-64] * 100 = YDR + ADR",
                "chart_type": "DEMOGRAPHIC_DIVIDEND_STACKED_AREA"
            },
            {
                "slide_id": "SLIDE_13",
                "role": "CONTENT",
                "section": "CƠ CẤU GIỚI TÍNH",
                "assertion_title": "Cơ Cấu Dân Số Theo Giới Tính Và Tỷ Số Giới Tính (Sex Ratio)",
                "primary_claim": "Tỷ số giới tính thay đổi liên tục theo từng nấc thang tuổi tác do sự khác biệt về mức độ tử vong giữa hai giới.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Tỷ Số Giới Tính (Sex Ratio - SR)",
                        "text": "SR = (Số nam / Số nữ) * 100. Tại Việt Nam tỷ số giới tính toàn bộ dân số hiện đạt xấp xỉ 99.5 nam trên 100 nữ.",
                        "icon": "users"
                    },
                    {
                        "title": "Quy Luật Biến Động Theo Tuổi",
                        "text": "Nam giới chiếm ưu thế ở nhóm tuổi trẻ (do số sinh nam cao hơn), cân bằng ở tuổi thanh niên và nữ giới vượt trội ở tuổi già.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Tỷ số giới tính có tính quy luật tự nhiên rất cao; sự lệch lạc bất thường phản ánh sự can thiệp nhân tạo vào quá trình sinh sản.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "formula": "SR = (Số Nam / Số Nữ) * 100  |  SRB = (Bé Trai / Bé Gái) * 100"
            },
            {
                "slide_id": "SLIDE_14",
                "role": "CONTENT",
                "section": "MẤT CÂN BẰNG GIỚI TÍNH",
                "assertion_title": "Thực Trạng Mất Cân Bằng Tỷ Số Giới Tính Khi Sinh (SRB) Tại Việt Nam",
                "primary_claim": "Tỷ số giới tính khi sinh tại Việt Nam lệch chuẩn sinh học nghiêm trọng do tâm lý chuộng con trai và lạm dụng công nghệ chọn giới tính.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "BENTO_SRB",
                "atoms": [
                    {
                        "title": "Ngưỡng Sinh Học Bình Thường",
                        "text": "Mức chuẩn tự nhiên trên thế giới là 104 - 106 bé trai / 100 bé gái sinh sống, bảo đảm bù đắp tử vong nam ở tuổi trưởng thành.",
                        "icon": "check"
                    },
                    {
                        "title": "Thực Trạng Việt Nam (112 - 115)",
                        "text": "SRB tại nhiều tỉnh Đồng bằng sông Hồng vượt ngưỡng 115 bé trai / 100 bé gái, đặc biệt nghiêm trọng ở lần sinh thứ ba trở lên.",
                        "icon": "alert-triangle"
                    },
                    {
                        "title": "Hệ Lụy Xã Hội Nghiêm Trọng",
                        "text": "Dự báo đến năm 2034 Việt Nam sẽ dư thừa từ 1.5 đến 2.5 triệu nam giới trong độ tuổi kết hôn, gây mất ổn định trật tự xã hội.",
                        "icon": "shield-alert"
                    }
                ],
                "speaker_notes": "Mất cân bằng SRB đòi hỏi giải pháp thay đổi định kiến giới và siết chặt quy định cấm chẩn đoán giới tính thai nhi.",
                "source_footer": "Báo cáo thực trạng mất cân bằng giới tính khi sinh - UNFPA & GSO",
                "chart_type": "DEPENDENCY_COMPONENTS_GROUPED"
            },
            {
                "slide_id": "SLIDE_15",
                "role": "CONTENT",
                "section": "DÂN SỐ VÀNG",
                "assertion_title": "Thời Kỳ Cơ Cấu Dân Số Vàng: Cơ Hội Bứt Phá Năng Suất Lao Động Lịch Sử",
                "primary_claim": "Việt Nam đang trong giai đoạn cơ cấu vàng quý giá với 68% dân số trong độ tuổi lao động, tạo cơ hội vàng thúc đẩy tích lũy.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "DEPENDENCY_COMPONENTS_GROUPED",
                "atoms": [
                    {
                        "title": "Cơ Hội Dân Số Vàng (2007 - 2039)",
                        "text": "Việt Nam có hơn 2 người trong độ tuổi lao động phụ thuộc 1 người ăn theo, tạo dư địa lớn để chuyển dịch cơ cấu kinh tế.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Nguy Cơ Bẫy Thu Nhập Trung Bình",
                        "text": "Nếu không kịp thời đào tạo kỹ năng số và nâng cao năng suất, thời kỳ dân số vàng sẽ trôi qua mà đất nước chưa kịp giàu.",
                        "icon": "alert-circle"
                    },
                    {
                        "title": "Hành Động Khẩn Trương",
                        "text": "Đẩy mạnh công nghiệp công nghệ cao, khuyến khích đổi mới sáng tạo và tạo việc làm thỏa đáng cho thanh niên.",
                        "icon": "zap"
                    }
                ],
                "speaker_notes": "Cơ hội dân số vàng chỉ xuất hiện một lần trong lịch sử mỗi quốc gia và kéo dài khoảng 30-40 năm.",
                "source_footer": "Nghiên cứu cơ cấu dân số vàng tại Việt Nam",
                "formula": "TDR = [(P_0-14 + P_65+) / P_15-64] * 100 = YDR + ADR"
            },
            {
                "slide_id": "SLIDE_16",
                "role": "CONTENT",
                "section": "GIÀ HÓA DÂN SỐ",
                "assertion_title": "Tiến Trình Già Hóa Dân Số Và Tốc Độ Chuyển Tiếp Thuộc Hàng Nhanh Nhất Thế Giới",
                "primary_claim": "Việt Nam chính thức bước vào quá trình già hóa dân số từ năm 2011 và sẽ trở thành quốc gia dân số già trước năm 2036.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "BENTO_AGING",
                "atoms": [
                    {
                        "title": "Hai Ngưỡng Già Hóa Quốc Tế",
                        "text": "Xã hội già hóa (Aging Phase) khi tỷ lệ người 65+ đạt 7%; Xã hội già (Aged Phase) khi tỷ lệ này chạm ngưỡng 14%.",
                        "icon": "clock"
                    },
                    {
                        "title": "Tốc Độ Nhanh Kỷ Lục",
                        "text": "Pháp mất 115 năm, Thụy Điển mất 85 năm, Nhật Bản mất 26 năm, trong khi Việt Nam chỉ mất chưa đầy 20 năm để chuyển tiếp.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Áp Lực Kép Lên Hệ Thống",
                        "text": "Quá tải quỹ hưu trí bảo hiểm xã hội, mô hình bệnh tật kép (bệnh mạn tính không lây) và thiếu hụt mạng lưới điều dưỡng lão khoa.",
                        "icon": "shield-alert"
                    }
                ],
                "speaker_notes": "Già hóa dân số đòi hỏi phải chuyển từ trợ cấp nhân đạo sang chủ động phát triển thị trường kinh tế bạc.",
                "source_footer": "Tổng cục Dân số - Kế hoạch hóa gia đình",
                "chart_type": "DEPENDENCY_RATIO_TRENDS",
                "illustration": "ai_bai_2_aging.jpg"
            },
            {
                "slide_id": "SLIDE_17",
                "role": "CONTENT",
                "section": "THÁP DÂN SỐ",
                "assertion_title": "Tháp Dân Số: Cấu Trúc Trực Quan Và Giá Trị Nhận Thức Lịch Sử",
                "primary_claim": "Tháp dân số là biểu đồ thanh ngang đối xứng biểu thị phân bố tuổi và giới tính, lưu giữ vết tích các biến cố lịch sử quốc gia.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Cấu Trúc Trục Biểu Đồ Tháp",
                        "text": "Trục tung chia theo các độ tuổi (thường là nhóm 5 tuổi), trục hoành biểu thị tỷ lệ hoặc số lượng: bên trái là Nam, bên phải là Nữ.",
                        "icon": "bar-chart-2"
                    },
                    {
                        "title": "Giá Trị Nhận Thức Nhân Khẩu",
                        "text": "Các vết lõm phản ánh chiến tranh, dịch bệnh hoặc giảm sinh; các phần phình to phản ánh làn sóng bùng nổ trẻ em (Baby Boom).",
                        "icon": "eye"
                    }
                ],
                "speaker_notes": "Tháp dân số giống như 'hồ sơ sức khỏe' trực quan của một dân tộc qua các biến thiên thời gian.",
                "source_footer": "Kỹ thuật phân tích tháp dân số",
                "chart_type": "POPULATION_PYRAMID"
            },
            {
                "slide_id": "SLIDE_18",
                "role": "CONTENT",
                "section": "DẠNG THÁP DÂN SỐ",
                "assertion_title": "Ba Dạng Tháp Dân Số Kinh Điển: Mở Rộng, Ổn Định Và Thu Hẹp",
                "primary_claim": "Hình thái tháp dân số phản ánh trực tiếp giai đoạn quá độ nhân khẩu học và mức độ sinh - tử của quốc gia.",
                "visual_job": "DATA_TABLE",
                "visual_anchor": "THREE_PYRAMIDS",
                "atoms": [
                    {
                        "title": "Tháp Mở Rộng (Expansive - Trẻ)",
                        "text": "Đáy tháp rất rộng, thu hẹp nhanh về đỉnh. Biểu thị mức sinh cao, tử vong giảm, tỷ lệ trẻ em lớn (phổ biến ở nước nghèo).",
                        "icon": "triangle"
                    },
                    {
                        "title": "Tháp Ổn Định (Stationary - Dừng)",
                        "text": "Đáy tháp và thân tháp có chiều rộng tương đương nhau, thu hẹp ở ngọn. Mức sinh ổn định ở mức thay thế, tuổi thọ cao.",
                        "icon": "square"
                    },
                    {
                        "title": "Tháp Thu Hẹp (Constrictive - Già)",
                        "text": "Đáy tháp hẹp hơn thân tháp, thân phình to. Mức sinh rất thấp, dân số già hóa nhanh chóng (phổ biến ở Nhật, Đức, Hàn Quốc).",
                        "icon": "hexagon"
                    }
                ],
                "speaker_notes": "Hiểu 3 dạng tháp giúp xác định chính xác giai đoạn nhân khẩu học hiện tại của bất kỳ quốc gia nào.",
                "source_footer": "Phân loại tháp dân số của Liên Hợp Quốc",
                "table_data": {
                    "headers": [
                        "Dạng Tháp Dân Số",
                        "Đáy Tháp",
                        "Thân Tháp",
                        "Đỉnh Tháp",
                        "Đặc Trưng Dân Số & Điển Hình"
                    ],
                    "rows": [
                        [
                            "Tháp Mở Rộng (Expansive)",
                            "Rất rộng, đáy mở to",
                            "Thu hẹp nhanh dần",
                            "Đỉnh tháp nhọn hẹp",
                            "Dân số trẻ, sinh cao, tử giảm (Các nước đang phát triển)"
                        ],
                        [
                            "Tháp Ổn Định (Stationary)",
                            "Tương đương thân",
                            "Thẳng đứng, đều đặn",
                            "Đỉnh tháp mở rộng",
                            "Dân số dừng, TFR ≈ 2.1 con, sống thọ (Bắc Âu, Thụy Điển)"
                        ],
                        [
                            "Tháp Thu Hẹp (Constrictive)",
                            "Co thắt, hẹp hơn thân",
                            "Phình to ở giữa",
                            "Đỉnh tháp rất rộng",
                            "Dân số già, sinh thấp kéo dài (Nhật Bản, Đức, Ý)"
                        ]
                    ],
                    "col_widths": [
                        0.22,
                        0.18,
                        0.18,
                        0.18,
                        0.24
                    ]
                }
            },
            {
                "slide_id": "SLIDE_19",
                "role": "CONTENT",
                "section": "THÁP DÂN SỐ VN",
                "assertion_title": "Biến Đổi Hình Thái Tháp Dân Số Việt Nam Từ Dạng Đáy Rộng Sang Con Thoi",
                "primary_claim": "Trong 4 thập kỷ qua, tháp dân số Việt Nam đã chuyển dịch ngoạn mục từ dạng mở rộng trẻ sang dạng phình ở giữa và đang co hẹp đáy.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "LABOR_FORCE_DONUT",
                "atoms": [
                    {
                        "title": "Năm 1989: Tháp Đáy Rộng Tam Giác",
                        "text": "Nhóm tuổi 0-14 chiếm trên 40% dân số, gánh nặng phụ thuộc trẻ em rất lớn, mức sinh bình quân còn trên 3.8 con/phụ nữ.",
                        "icon": "triangle"
                    },
                    {
                        "title": "Năm 2019: Tháp Dạng Con Thoi",
                        "text": "Thân tháp phình to ở nhóm tuổi 20-39 với 68.0% người trong độ tuổi lao động (dân số vàng), đáy tháp co hẹp lại do mức sinh ổn định.",
                        "icon": "circle"
                    },
                    {
                        "title": "Xu Hướng Đến Năm 2040",
                        "text": "Đỉnh tháp phình to mạnh mẽ do số người cao tuổi tăng nhanh, đòi hỏi chuẩn bị ngay hệ sinh thái dịch vụ dưỡng lão chuyên nghiệp.",
                        "icon": "shield"
                    }
                ],
                "speaker_notes": "Sự chuyển dịch của tháp dân số Việt Nam minh chứng rõ nét cho thành công của công tác dân số và áp lực già hóa cận kề.",
                "source_footer": "Dữ liệu Tổng điều tra dân số 1989 - 2019"
            },
            {
                "slide_id": "SLIDE_20",
                "role": "CONTENT",
                "section": "CƠ CẤU XÃ HỘI",
                "assertion_title": "Cơ Cấu Xã Hội Của Dân Số: Hôn Nhân, Dân Tộc Và Học Vấn",
                "primary_claim": "Các đặc trưng xã hội của dân số phản ánh trực tiếp cơ hội tiếp cận nguồn lực, chất lượng sống và sự hòa hợp xã hội.",
                "visual_job": "COMPARISON",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Tình Trạng Hôn Nhân",
                        "text": "Tỷ lệ độc thân tăng, tuổi kết hôn lần đầu trung bình tăng lên 27.2 tuổi (nam 29.8, nữ 24.6), mức sinh có xu hướng giảm.",
                        "icon": "heart"
                    },
                    {
                        "title": "Cơ Cấu Dân Tộc (54 Dân Tộc)",
                        "text": "Dân tộc Kinh chiếm khoảng 85.3%, 53 dân tộc thiểu số chiếm 14.7%, đòi hỏi chính sách hỗ trợ phát triển vùng đồng bào thiểu số.",
                        "icon": "globe"
                    },
                    {
                        "title": "Trình Độ Học Vấn & Tay Nghề",
                        "text": "Tỷ lệ biết chữ đạt trên 95%, nhưng tỷ lệ lao động có chứng chỉ kỹ năng nghề vẫn là điểm nghẽn cần tháo gỡ cấp bách.",
                        "icon": "book-open"
                    }
                ],
                "speaker_notes": "Chính sách xã hội cần tính đến sự đa dạng văn hóa và phong tục tập quán của các nhóm dân cư khác nhau.",
                "source_footer": "Kết quả khảo sát dân tộc thiểu số và mức sống dân cư",
                "chart_type": "LABOR_FORCE_DONUT"
            },
            {
                "slide_id": "SLIDE_21",
                "role": "CONTENT",
                "section": "CHẤT LƯỢNG DÂN SỐ",
                "assertion_title": "Khái Niệm Toàn Diện Về Chất Lượng Dân Số: Thể Chất, Trí Tuệ Và Tinh Thần",
                "primary_claim": "Chất lượng dân số phản ánh năng lực thể chất, trình độ học vấn trí tuệ và sự an lạc tinh thần của toàn bộ cộng đồng.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "THREE_DIMENSIONS",
                "atoms": [
                    {
                        "title": "Chất Lượng Thể Chất (Physical)",
                        "text": "Đo lường bằng tuổi thọ bình quân, kỳ vọng sống khỏe mạnh, chiều cao, cân nặng, sức bền và tỷ lệ suy dinh dưỡng trẻ em.",
                        "icon": "activity"
                    },
                    {
                        "title": "Chất Lượng Trí Tuệ (Intellectual)",
                        "text": "Biểu hiện qua tỷ lệ biết chữ, số năm đi học bình quân, tỷ lệ lao động có chuyên môn kỹ thuật và năng lực sáng tạo công nghệ.",
                        "icon": "cpu"
                    },
                    {
                        "title": "Chất Lượng Tinh Thần (Mental)",
                        "text": "Phản ánh qua mức độ hài lòng cuộc sống, sức khỏe tâm thần, môi trường gia đình ấm no và các chuẩn mực đạo đức xã hội.",
                        "icon": "smile"
                    }
                ],
                "speaker_notes": "Chất lượng dân số là mục tiêu cuối cùng của mọi chiến lược phát triển con người bền vững.",
                "source_footer": "Pháp lệnh Dân số Việt Nam",
                "illustration": "ai_bai_2_quality.jpg"
            },
            {
                "slide_id": "SLIDE_22",
                "role": "CONTENT",
                "section": "CHỈ SỐ HDI",
                "assertion_title": "Chỉ Số Phát Triển Con Người (HDI) Và Ba Trụ Cột Thành Phần Đo Lường",
                "primary_claim": "HDI là thước đo tổng hợp quốc tế về sự tiến bộ con người, kết hợp hài hòa giữa sức khỏe, giáo dục và mức sống kinh tế.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "THREE_HDI_PILLARS",
                "atoms": [
                    {
                        "title": "1. Trụ Cột Sức Khỏe (LEI)",
                        "text": "Đo bằng tuổi thọ kỳ vọng khi sinh (Life Expectancy Index). Chuẩn hóa trong khoảng từ 20 năm đến 85 năm.",
                        "icon": "heart"
                    },
                    {
                        "title": "2. Trụ Cột Giáo Dục (EI)",
                        "text": "Kết hợp giữa số năm đi học kỳ vọng của trẻ em (EYS) và số năm đi học bình quân của người từ 25 tuổi trở lên (MYS).",
                        "icon": "book-open"
                    },
                    {
                        "title": "3. Trụ Cột Thu Nhập (II)",
                        "text": "Đo bằng Tổng thu nhập quốc dân (GNI) bình quân đầu người tính theo sức mua tương đương (PPP tính bằng USD).",
                        "icon": "dollar-sign"
                    }
                ],
                "speaker_notes": "Chỉ số HDI = căn bậc 3 của tích (LEI * EI * II). Điểm số dao động từ 0 đến 1.",
                "source_footer": "Chương trình Phát triển Liên Hợp Quốc (UNDP HDR)",
                "formula": "HDI = [I_Health * I_Education * I_Income]^(1/3) = (LEI * EI * II)^(1/3)"
            },
            {
                "slide_id": "SLIDE_23",
                "role": "CONTENT",
                "section": "HDI VIỆT NAM",
                "assertion_title": "Vị Thế Và Tiến Trình Cải Thiện Chỉ Số HDI Của Việt Nam Trên Bản Đồ Thế Giới",
                "primary_claim": "Việt Nam chính thức gia nhập nhóm các quốc gia có mức phát triển con người cao với chỉ số HDI vượt ngưỡng 0.700.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "HDI_DIMENSIONS",
                "atoms": [
                    {
                        "title": "HDI Đạt 0.726 (2023)",
                        "text": "Việt Nam xếp thứ 107 trên 193 quốc gia, thuộc nhóm phát triển con người cao nhờ cải thiện liên tục suốt 3 thập kỷ.",
                        "icon": "award"
                    },
                    {
                        "title": "Điểm Mạnh Tuổi Thọ (73.7 Tuổi)",
                        "text": "Chỉ số sức khỏe của Việt Nam vượt trội so với các quốc gia có cùng mức thu nhập bình quân đầu người.",
                        "icon": "heart"
                    },
                    {
                        "title": "Dư Địa Cải Thiện Thu Nhập & Giáo Dục",
                        "text": "Cần thúc đẩy đào tạo sau phổ thông và chuyển đổi mô hình kinh tế để nâng cao thực chất GNI bình quân đầu người.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Thành tựu HDI của Việt Nam được quốc tế đánh giá cao, đặc biệt trong việc phổ cập giáo dục cơ sở và chăm sóc y tế ban đầu.",
                "source_footer": "Báo cáo Phát triển Con người Toàn cầu - UNDP"
            },
            {
                "slide_id": "SLIDE_24",
                "role": "CONTENT",
                "section": "SỨC KHỎE DÂN SỐ",
                "assertion_title": "Hệ Thống Chỉ Báo Đo Lường Sức Khỏe Thể Lực Và Tình Trạng Dinh Dưỡng",
                "primary_claim": "Tử vong trẻ sơ sinh giảm sâu và thể lực người Việt được cải thiện, nhưng gánh nặng bệnh tật mạn tính đang gia tăng.",
                "visual_job": "CARDS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Tử Vong Trẻ Em (IMR & U5MR)",
                        "text": "Tỷ suất tử vong trẻ sơ sinh (IMR) giảm xuống dưới 12‰; tử vong dưới 5 tuổi (U5MR) giảm mạnh về mức 18.9‰.",
                        "icon": "shield"
                    },
                    {
                        "title": "Chiều Cao Thanh Niên Cải Thiện",
                        "text": "Chiều cao trung bình của nam thanh niên đạt 168.1 cm, nữ đạt 156.2 cm, tăng hơn 3 cm sau 10 năm can thiệp dinh dưỡng học đường.",
                        "icon": "user-check"
                    },
                    {
                        "title": "Mô Hình Bệnh Tật Kép",
                        "text": "Bệnh không lây nhiễm (tim mạch, ung thư, tiểu đường) chiếm hơn 70% gánh nặng bệnh tật và nguyên nhân tử vong.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Chiến lược nâng cao thể lực tầm vóc người Việt Nam cần kết hợp dinh dưỡng, thể dục thể thao và tầm soát sơ sinh.",
                "source_footer": "Bộ Y tế - Khảo sát Dinh dưỡng Quốc gia"
            },
            {
                "slide_id": "SLIDE_25",
                "role": "CONTENT",
                "section": "YẾU TỐ ẢNH HƯỞNG",
                "assertion_title": "Bốn Nhóm Yếu Tố Quyết Định Nâng Cao Chất Lượng Dân Số Bền Vững",
                "primary_claim": "Nâng cao chất lượng dân số đòi hỏi can thiệp đồng bộ từ kinh tế, y tế gia đình, giáo dục đào tạo đến môi trường sinh thái.",
                "visual_job": "CARDS",
                "visual_anchor": "FOUR_FACTORS",
                "atoms": [
                    {
                        "title": "Kinh Tế & An Sinh Xã Hội",
                        "text": "Tăng trưởng thu nhập, giảm nghèo bền vững và mở rộng bao phủ bảo hiểm y tế toàn dân tạo nền tảng vật chất vững chắc.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "Y Tế & Chăm Sóc Đầu Đời",
                        "text": "Khám sức khỏe tiền hôn nhân, tầm soát trước sinh và sơ sinh giúp giảm thiểu tối đa dị tật bẩm sinh di truyền.",
                        "icon": "heart"
                    },
                    {
                        "title": "Hệ Thống Giáo Dục & Kỹ Năng",
                        "text": "Đổi mới căn bản giáo dục phổ thông, phát triển trường nghề chất lượng cao và xây dựng xã hội học tập suốt đời.",
                        "icon": "book-open"
                    }
                ],
                "speaker_notes": "Đầu tư cho chất lượng dân số giai đoạn đầu đời mang lại tỷ suất hoàn vốn xã hội cao nhất trong mọi khoản đầu tư công.",
                "source_footer": "Chiến lược Dân số và Sức khỏe sinh sản"
            },
            {
                "slide_id": "SLIDE_26",
                "role": "CONTENT",
                "section": "MỐI QUAN HỆ BIỆN CHỨNG",
                "assertion_title": "Mối Quan Hệ Biện Chứng Giữa Quy Mô, Cơ Cấu Và Chất Lượng Dân Số",
                "primary_claim": "Quy mô, cơ cấu và chất lượng là ba đỉnh của tam giác nhân khẩu học tác động qua lại mật thiết trong phát triển kinh tế.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Cơ Cấu Vàng Là Thời Cơ Nâng Cao Chất Lượng",
                        "text": "Tỷ lệ người phụ thuộc thấp cho phép gia đình và nhà nước dồn nguồn lực đầu tư giáo dục, dinh dưỡng chất lượng cao cho con em.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Chất Lượng Cao Bù Đắp Suy Giảm Số Lượng",
                        "text": "Khi quy mô bước vào giai đoạn chững lại và cơ cấu già hóa, năng suất lao động vượt trội sẽ bù đắp hoàn toàn sự thiếu hụt số lượng.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Chiến lược dân số hiện đại không theo đuổi số lượng thuần túy mà tập trung chuyển hóa số lượng thành chất lượng nguồn nhân lực.",
                "source_footer": "Nghị quyết 21-NQ/TW"
            },
            {
                "slide_id": "SLIDE_27",
                "role": "CONTENT",
                "section": "ĐỊNH HƯỚNG CHIẾN LƯỢC",
                "assertion_title": "Định Hướng Chiến Lược Nâng Cao Toàn Diện Chất Lượng Dân Số Đến 2030",
                "primary_claim": "Chuyển mạnh trọng tâm chính sách từ Kế hoạch hóa gia đình sang Dân số và Phát triển theo tinh thần Nghị quyết 21-NQ/TW.",
                "visual_job": "PROCESS",
                "visual_anchor": "STRATEGIC_PILLARS",
                "atoms": [
                    {
                        "title": "1. Duy Trì Mức Sinh Thay Thế",
                        "text": "Vận động mỗi cặp vợ chồng sinh đủ 2 con, kiểm soát không để mức sinh giảm quá sâu tại các đô thị phát triển.",
                        "icon": "target"
                    },
                    {
                        "title": "2. Đưa SRB Về Mức Tự Nhiên",
                        "text": "Phấn đấu đưa tỷ số giới tính khi sinh về dưới 109 bé trai / 100 bé gái vào năm 2030 qua kiểm soát nghiêm ngặt y tế.",
                        "icon": "balance"
                    },
                    {
                        "title": "3. Tận Dụng Vàng & Thích Ứng Già",
                        "text": "Phát triển công nghiệp giá trị gia tăng cao và chuẩn bị cơ sở hạ tầng, y tế lão khoa thích ứng xã hội dân số già.",
                        "icon": "zap"
                    },
                    {
                        "title": "4. Tầm Soát Sức Khỏe Đầu Đời",
                        "text": "70% phụ nữ mang thai được sàng lọc trước sinh; 90% trẻ sơ sinh được sàng lọc 5 bệnh tật bẩm sinh phổ biến nhất.",
                        "icon": "shield"
                    }
                ],
                "speaker_notes": "Bốn trụ cột chiến lược này định hình toàn bộ chính sách đầu tư nguồn lực dân số của Việt Nam trong thập kỷ tới.",
                "source_footer": "Chiến lược Dân số Việt Nam đến năm 2030"
            },
            {
                "slide_id": "SLIDE_28",
                "role": "CONTENT",
                "section": "TỔNG KẾT BÀI HỌC",
                "assertion_title": "Tổng Kết Chuyên Đề Và Bài Tập Thực Hành Tính Toán Dân Số Học",
                "primary_claim": "Vận dụng thành thạo các công thức tính dân số trung bình, tỷ số phụ thuộc và phân tích ý nghĩa chính sách phát triển.",
                "visual_job": "CARDS",
                "visual_anchor": "SUMMARY_PRACTICE",
                "atoms": [
                    {
                        "title": "Bài Tập 1: Cân Bằng Dân Số",
                        "text": "Cho P_0 = 1,000,000 người; B = 16,000; D = 6,000; I = 8,000; O = 3,000. Hãy tính quy mô dân số P_t và tỷ lệ tăng tổng số r_g.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Bài Tập 2: Tỷ Số Phụ Thuộc",
                        "text": "Dân số 0-14 chiếm 23%, dân số 65+ chiếm 9%, dân số 15-64 chiếm 68%. Tính YDR, ADR, CDR và xác định có thuộc cơ cấu vàng không?",
                        "icon": "pie-chart"
                    },
                    {
                        "title": "Thảo Luận Chính Sách 3",
                        "text": "Đề xuất 3 giải pháp chính sách an sinh xã hội khả thi để Việt Nam chủ động ứng phó với tốc độ già hóa dân số nhanh hiện nay.",
                        "icon": "message-square"
                    }
                ],
                "speaker_notes": "Học viên hoàn thành bài tập thực hành vào phiếu làm việc và nộp lại cho giảng viên chấm điểm chuẩn đầu ra.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
            }
        ]
    }


def get_lesson_blueprints_bai_3() -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "lesson_index": 3,
        "deck_title": "Biến Động Tự Nhiên Dân Số",
        "total_slides": 22,
        "visual_system": "MODERN_REFINED",
        "slides": [
            {
                "slide_id": "SLIDE_01",
                "role": "COVER",
                "section": "TỔNG QUAN CHUYÊN ĐỀ",
                "assertion_title": "BÀI 3: BIẾN ĐỘNG TỰ NHIÊN DÂN SỐ",
                "primary_claim": "Khung lý thuyết và phương pháp đo lường mức sinh, mức chết, bảng sống và mô hình chuyển tiếp dân số.",
                "visual_job": "HERO_TITLE",
                "visual_anchor": "BRAND_COVER",
                "speaker_notes": "Kính chào quý học viên, Bài 3 đi sâu vào bản chất sinh - tử của con người và các quy luật biến động tự nhiên dân số.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia",
                "illustration": "illustration_bai_3.jpg"
            },
            {
                "slide_id": "SLIDE_02",
                "role": "CONTENT",
                "section": "MỤC TIÊU BÀI HỌC",
                "assertion_title": "Năng Lực Làm Chủ Các Chỉ Báo Đo Lường Mức Sinh Và Mức Chết",
                "primary_claim": "Trang bị phương pháp tính toán chuyên sâu từ CBR, ASFR, TFR đến CDR, IMR, bảng sống và mô hình chuyển tiếp nhân khẩu.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_OBJECTIVES",
                "atoms": [
                    {
                        "title": "Hệ Thống Thước Đo Mức Sinh",
                        "text": "Tính toán và phân tích chuyên sâu tỷ suất sinh thô (CBR), tỷ suất sinh chung (GFR), ASFR và tổng tỷ suất sinh (TFR).",
                        "icon": "activity"
                    },
                    {
                        "title": "Hệ Thống Thước Đo Mức Chết",
                        "text": "Làm chủ tỷ suất chết thô (CDR), tử vong trẻ sơ sinh (IMR), tử vong mẹ (MMR) và nguyên lý lập bảng sống (Life Table).",
                        "icon": "shield"
                    },
                    {
                        "title": "Mô Hình Chuyển Tiếp Dân Số",
                        "text": "Hiểu rõ 4 giai đoạn chuyển tiếp nhân khẩu học và vận dụng vào phân tích chính sách duy trì mức sinh thay thế ở Việt Nam.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Chuẩn đầu ra yêu cầu học viên phân biệt được ưu nhược điểm của từng thước đo thô và thước đo chuẩn hóa.",
                "source_footer": "Khung chuẩn đầu ra chuyên đề"
            },
            {
                "slide_id": "SLIDE_03",
                "role": "CONTENT",
                "section": "KHÁI NIỆM MỨC SINH",
                "assertion_title": "Quá Trình Sinh Đẻ Và Bản Chất Khái Niệm Mức Sinh (Fertility)",
                "primary_claim": "Mức sinh phản ánh kết quả thực tế của quá trình sinh đẻ của quần thể dân số trong một khoảng thời gian xác định.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Khả Năng Sinh Sản (Fecundity)",
                        "text": "Khả năng sinh lý tiềm tàng về mặt sinh học của người phụ nữ có thể thụ thai và sinh con trong độ tuổi sinh sản (15-49 tuổi).",
                        "icon": "heart"
                    },
                    {
                        "title": "Mức Sinh Thực Tế (Fertility)",
                        "text": "Số lượng trẻ sinh sống thực tế được sinh ra, là sự kết hợp giữa khả năng sinh học và các rào cản hành vi kinh tế - xã hội.",
                        "icon": "users"
                    }
                ],
                "speaker_notes": "Sự phân biệt giữa khả năng sinh học và mức sinh thực tế là nền tảng của lý thuyết chuyển tiếp mức sinh.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "illustration": "ai_bai_3_fertility.jpg"
            },
            {
                "slide_id": "SLIDE_04",
                "role": "CONTENT",
                "section": "THƯỚC ĐO MỨC SINH",
                "assertion_title": "Tỷ Suất Sinh Thô (CBR) Và Giới Hạn Của Thước Đo Ban Đầu",
                "primary_claim": "Tỷ suất sinh thô đo lường số trẻ sinh sống trên 1.000 dân trung bình trong năm, dễ tính nhưng bị nhiễu bởi cơ cấu tuổi.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Công Thức Tính CBR",
                        "text": "CBR = (B / P_tb) * 1,000 (đơn vị ‰). Với B là tổng số trẻ sinh sống trong năm, P_tb là dân số trung bình trong năm.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Ưu Điểm Của Chỉ Số",
                        "text": "Đơn giản, dễ thu thập số liệu qua đăng ký hộ tịch và cho phép so sánh khái quát nhanh giữa các quốc gia.",
                        "icon": "check-circle"
                    },
                    {
                        "title": "Nhược Điểm Cốt Tử",
                        "text": "Mẫu số chứa cả nam giới, người già và trẻ em - những đối tượng không có khả năng sinh sản, làm méo mó bản chất mức sinh.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Khi hai địa phương có cùng mức sinh nhưng cơ cấu tuổi khác nhau thì CBR sẽ cho ra con số rất khác biệt.",
                "source_footer": "Phương pháp đo lường nhân khẩu học",
                "formula": "CBR = (B / P_tb) * 1,000  (Đơn vị: ‰ - Trên 1.000 dân trung bình)"
            },
            {
                "slide_id": "SLIDE_05",
                "role": "CONTENT",
                "section": "TỶ SUẤT GFR",
                "assertion_title": "Tỷ Suất Sinh Chung (GFR) Xác Định Trên Quần Thể Phụ Nữ Sinh Đẻ",
                "primary_claim": "GFR thu hẹp mẫu số vào nhóm phụ nữ trong độ tuổi sinh sản (15-49 tuổi), nâng cao độ chính xác đo lường mức sinh.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Công Thức Tính GFR",
                        "text": "GFR = (B / W_15-49) * 1,000 (đơn vị ‰). Với W_15-49 là số phụ nữ trong độ tuổi 15-49 tuổi bình quân trong năm.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Mức Độ Chuẩn Hóa Cao Hơn",
                        "text": "GFR thường có giá trị cao gấp 4 đến 5 lần so với CBR vì đã loại bỏ nam giới và các lứa tuổi không tham gia sinh đẻ.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Hạn Chế Còn Tồn Tại",
                        "text": "Vẫn chưa tính đến sự khác biệt lớn về cường độ sinh con giữa các lứa tuổi trong khoảng 15-49 (tuổi 25-29 sinh nhiều hơn 40-44).",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "GFR là bước tiến lớn so với CBR nhưng vẫn cần bóc tách sâu hơn theo từng nhóm tuổi.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "formula": "GFR = [B / W_(15-49)] * 1,000  (Đơn vị: ‰ - Phụ nữ 15-49 tuổi)",
                "chart_type": "FERTILITY_TRENDS"
            },
            {
                "slide_id": "SLIDE_06",
                "role": "CONTENT",
                "section": "TỶ SUẤT ASFR",
                "assertion_title": "Tỷ Suất Sinh Đặc Trưng Theo Tuổi (ASFR) Và Đồ Thị Phân Bố Sinh",
                "primary_claim": "ASFR bóc tách mức sinh theo từng nhóm tuổi 5 năm, cho thấy rõ mô hình sinh đẻ sớm hay muộn của phụ nữ.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Công Thức ASFR_x",
                        "text": "ASFR_x = (B_x / W_x) * 1,000 (đơn vị ‰). Với B_x là số con do phụ nữ nhóm tuổi x sinh ra, W_x là số phụ nữ nhóm tuổi x.",
                        "icon": "bar-chart-2"
                    },
                    {
                        "title": "Hình Thái Đồ Thị Hình Chuông",
                        "text": "Đồ thị ASFR luôn có dạng hình chuông: bắt đầu thấp ở 15-19, đạt đỉnh cao ở 25-29 tuổi và giảm dần về 45-49 tuổi.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Xu Hướng Dịch Chuyển Đỉnh",
                        "text": "Ở các đô thị hiện đại, đỉnh sinh đẻ đang dịch chuyển từ nhóm 20-24 sang nhóm 25-29 và thậm chí 30-34 tuổi.",
                        "icon": "calendar"
                    }
                ],
                "speaker_notes": "ASFR là nền tảng để tính toán Tổng tỷ suất sinh (TFR) - thước đo chuẩn mực nhất thế giới.",
                "source_footer": "Phương pháp thống kê nhân khẩu học",
                "formula": "ASFR_x = (B_x / W_x) * 1,000  (Đơn vị: ‰ - Cho từng nhóm tuổi x)"
            },
            {
                "slide_id": "SLIDE_07",
                "role": "CONTENT",
                "section": "TỔNG TỶ SUẤT SINH",
                "assertion_title": "Tổng Tỷ Suất Sinh (TFR) Và Ngưỡng Mức Sinh Thay Thế Chuẩn 2.1 Con",
                "primary_claim": "TFR là số con trung bình mà một phụ nữ sinh ra trong suốt cuộc đời nếu tuân theo tỷ suất sinh đặc trưng theo tuổi của năm đó.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "BENTO_TFR",
                "atoms": [
                    {
                        "title": "Công Thức Tính TFR",
                        "text": "TFR = 5 * Σ(ASFR_x) / 1,000. Đo lường độc lập hoàn toàn với cơ cấu tuổi của dân số, cho phép so sánh quốc tế chuẩn xác.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Ngưỡng Mức Sinh Thay Thế (2.1 Con)",
                        "text": "Mức sinh bảo đảm một thế hệ con gái thay thế đúng số lượng thế hệ người mẹ. Cần 2.1 con để bù đắp rủi ro tử vong trước tuổi sinh sản.",
                        "icon": "check-circle"
                    },
                    {
                        "title": "Ý Nghĩa Chiến Lược Quốc Gia",
                        "text": "Duy trì TFR quanh mức 2.1 con giúp ổn định quy mô dân số và làm chậm quá trình già hóa trong dài hạn.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "TFR là chỉ tiêu quan trọng số 1 trong các nghị quyết và chiến lược dân số của mọi quốc gia.",
                "source_footer": "Khái niệm mức sinh thay thế - Liên Hợp Quốc",
                "formula": "TFR = 5 * Σ(ASFR_x) / 1,000  (Mức sinh thay thế chuẩn = 2.10 con)"
            },
            {
                "slide_id": "SLIDE_08",
                "role": "CONTENT",
                "section": "TÁI SINH DÂN SỐ",
                "assertion_title": "Thước Đo Tái Sinh Dân Số: Tỷ Suất Tái Sinh Thô (GRR) Và Thuần (NRR)",
                "primary_claim": "Đo lường sự thay thế dân số qua thế hệ con gái là thước đo thực chất về tương lai tăng trưởng nhân khẩu học.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Tỷ Suất Tái Sinh Thô (GRR)",
                        "text": "Số con gái trung bình một phụ nữ sinh ra nếu không tính đến rủi ro tử vong của người mẹ và con gái trước khi hết tuổi sinh sản.",
                        "icon": "users"
                    },
                    {
                        "title": "Tỷ Suất Tái Sinh Thuần (NRR)",
                        "text": "Có tính đến xác suất sống sót của con gái từ khi sinh đến độ tuổi của mẹ. Nếu NRR = 1.0, dân số bảo đảm thay thế hoàn hảo.",
                        "icon": "shield-check"
                    }
                ],
                "speaker_notes": "Khi NRR < 1.0 kéo dài, quy mô dân số chắc chắn sẽ bước vào giai đoạn suy giảm trong tương lai.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "chart_type": "FERTILITY_BY_REGION_BAR"
            },
            {
                "slide_id": "SLIDE_09",
                "role": "CONTENT",
                "section": "YẾU TỐ SINH HỌC",
                "assertion_title": "Nhóm Yếu Tố Tự Nhiên Và Sinh Học Chi Phối Khả Năng Sinh Sản",
                "primary_claim": "Khả năng sinh sản sinh học chịu tác động của độ tuổi dậy thì, mãn kinh, khoảng cách giữa các lần sinh và tình trạng sức khỏe.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Khoảng Thời Gian Sinh Sản",
                        "text": "Thời kỳ từ khi có kinh nguyệt đầu tiên đến khi mãn kinh. Tuổi kết hôn càng muộn thì khoảng thời gian sinh sản thực tế càng bị rút ngắn.",
                        "icon": "clock"
                    },
                    {
                        "title": "Thời Gian Vô Sinh Tạm Thời Sau Sinh",
                        "text": "Tác dụng ức chế rụng trứng tự nhiên khi nuôi con hoàn toàn bằng sữa mẹ kéo dài khoảng cách giữa các lần sinh.",
                        "icon": "heart"
                    },
                    {
                        "title": "Tình Trạng Vô Sinh & Hiếm Muộn",
                        "text": "Ô nhiễm môi trường, lối sống và bệnh lý khiến tỷ lệ vô sinh thứ phát gia tăng, cần sự can thiệp của y học hỗ trợ sinh sản.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Mặc dù là yếu tố sinh học tự nhiên, các yếu tố này ngày càng chịu ảnh hưởng sâu sắc của lối sống hiện đại.",
                "source_footer": "Y học sinh sản và nhân khẩu học",
                "illustration": "cinematic_bai_3_health.jpg"
            },
            {
                "slide_id": "SLIDE_10",
                "role": "CONTENT",
                "section": "YẾU TỐ VĂN HÓA",
                "assertion_title": "Nhóm Yếu Tố Phong Tục Tập Quán Và Tâm Lý Xã Hội Ảnh Hưởng Mức Sinh",
                "primary_claim": "Quan niệm truyền thống về quy mô gia đình, nối dõi tông đường và thờ cúng tổ tiên định hình mạnh mẽ hành vi sinh con.",
                "visual_job": "CARDS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Tâm Lý Chuộng Con Trai",
                        "text": "Quan niệm Nho giáo 'nhất nam viết hữu' thúc đẩy các cặp vợ chồng cố sinh cho được con trai, làm gia tăng số con và mất cân bằng SRB.",
                        "icon": "users"
                    },
                    {
                        "title": "Quan Niệm Gia Đình Trẻ Hiện Đại",
                        "text": "Thế hệ trẻ chuyển dịch sang lối sống đề cao tự do cá nhân, ưu tiên thăng tiến nghề nghiệp và giảm số con mong muốn xuống 1-2 con.",
                        "icon": "smile"
                    },
                    {
                        "title": "Tôn Giáo Và Niềm Tin Tâm Linh",
                        "text": "Các tín điều tôn giáo về hôn nhân, cấm đoán phá thai hoặc quan niệm năm sinh tốt/xấu tạo ra các làn sóng sinh biến động.",
                        "icon": "sun"
                    }
                ],
                "speaker_notes": "Thay đổi định kiến văn hóa là quá trình lâu dài đòi hỏi kiên trì truyền thông vận động.",
                "source_footer": "Xã hội học gia đình và mức sinh"
            },
            {
                "slide_id": "SLIDE_11",
                "role": "CONTENT",
                "section": "YẾU TỐ KINH TẾ",
                "assertion_title": "Chi Phí Nuôi Dạy Con Cái Và Xu Hướng Giảm Mức Sinh Tại Các Đô Thị",
                "primary_claim": "Lý thuyết kinh tế vi mô về hành vi sinh đẻ của Gary Becker: Con cái chuyển từ nguồn lao động thành hàng hóa tiêu dùng chất lượng cao.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Chi Phí Cơ Hội Và Đầu Tư Giáo Dục",
                        "text": "Giá nhà ở đắt đỏ, chi phí học hành tăng cao cùng chi phí cơ hội việc làm của phụ nữ khiến các gia đình đô thị trì hoãn sinh con.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "Đánh Đổi Số Lượng - Chất Lượng",
                        "text": "Cha mẹ hiện đại chọn sinh ít con (1-2 con) để tập trung toàn bộ nguồn lực tài chính chăm lo điều kiện phát triển tốt nhất.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Đây là nguyên nhân kinh tế căn bản giải thích tại sao kinh tế càng phát triển thì mức sinh càng có xu hướng giảm sâu.",
                "source_footer": "Kinh tế học nhân khẩu học (Gary Becker Model)",
                "chart_type": "FERTILITY_TRENDS"
            },
            {
                "slide_id": "SLIDE_12",
                "role": "CONTENT",
                "section": "MỨC SINH VIỆT NAM",
                "assertion_title": "Thực Trạng Mức Sinh Việt Nam: Đạt Thay Thế Toàn Quốc Nhưng Phân Hóa Vùng Miền",
                "primary_claim": "Việt Nam duy trì mức sinh thay thế suốt gần 2 thập kỷ (TFR ~ 2.0 - 2.1), nhưng đang xuất hiện sự phân hóa sâu sắc giữa hai miền.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_VN_FERTILITY",
                "atoms": [
                    {
                        "title": "Vùng Đông Nam Bộ Sinh Rất Thấp",
                        "text": "TFR TP.HCM xuống mức kỷ lục 1.39 con/phụ nữ; Đồng bằng sông Cửu Long chỉ đạt 1.8 con. Nguy cơ thiếu hụt lao động tương lai.",
                        "icon": "trending-down"
                    },
                    {
                        "title": "Vùng Trung Du Miền Núi Sinh Cao",
                        "text": "Khu vực Trung du miền núi phía Bắc và Tây Nguyên có mức sinh trên 2.4 con/phụ nữ, gánh nặng nghèo đói và giáo dục còn lớn.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Chính Sách Điều Chỉnh Mức Sinh",
                        "text": "Chuyển từ khẩu hiệu 'mỗi cặp vợ chồng sinh 1-2 con' sang khuyến khích: Nơi sinh cao vận động sinh ít; nơi sinh thấp khuyến khích sinh đủ 2 con.",
                        "icon": "flag"
                    }
                ],
                "speaker_notes": "Quyết định 588/QĐ-TTg của Thủ tướng Chính phủ là bước chuyển hướng lịch sử trong chính sách mức sinh Việt Nam.",
                "source_footer": "Quyết định 588/QĐ-TTg phê duyệt Chương trình điều chỉnh mức sinh"
            },
            {
                "slide_id": "SLIDE_13",
                "role": "CONTENT",
                "section": "MỨC CHẾT",
                "assertion_title": "Khái Niệm Mức Chết (Mortality) Và Tỷ Suất Chết Thô (CDR)",
                "primary_claim": "Tử vong là sự mất đi vĩnh viễn mọi biểu hiện của sự sống; tỷ suất chết thô đo lường cường độ chết chung của quần thể dân số.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Công Thức Tỷ Suất Chết Thô (CDR)",
                        "text": "CDR = (D / P_tb) * 1,000 (đơn vị ‰). Với D là tổng số ca tử vong trong năm, P_tb là dân số trung bình. CDR Việt Nam hiện khoảng 6.1‰.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Nghịch Lý Cơ Cấu Dân Số Già",
                        "text": "Các nước phát triển có y tế cực tốt nhưng CDR lại cao hơn nước đang phát triển vì tỷ lệ người già trong dân số quá cao.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Cũng giống như CBR, CDR là thước đo thô và chịu ảnh hưởng chi phối rất lớn của cơ cấu tuổi.",
                "source_footer": "Phương pháp thống kê mức chết",
                "formula": "CDR = (D / P_tb) * 1,000  (Đơn vị: ‰ - Trên 1.000 dân trung bình)"
            },
            {
                "slide_id": "SLIDE_14",
                "role": "CONTENT",
                "section": "TỶ SUẤT ASDR",
                "assertion_title": "Tỷ Suất Chết Đặc Trưng Theo Tuổi (ASDR) Và Đồ Thị Hình Chữ U",
                "primary_claim": "ASDR phản ánh chính xác quy luật sinh học của tử vong: cao ở giai đoạn sơ sinh, chạm đáy ở tuổi thiếu niên và tăng vọt ở tuổi già.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Công Thức ASDR_x",
                        "text": "ASDR_x = (D_x / P_x) * 1,000 (đơn vị ‰). Với D_x là số người chết ở nhóm tuổi x, P_x là dân số nhóm tuổi x.",
                        "icon": "bar-chart-2"
                    },
                    {
                        "title": "Đồ Thị Dạng Chữ U (U-Shaped Curve)",
                        "text": "Đường cong ASDR cao ở nhóm 0 tuổi, giảm xuống cực tiểu ở nhóm 10-14 tuổi, sau đó tăng cấp số nhân từ tuổi 50 trở đi.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Khoảng Cách Tử Vong Giới Tính",
                        "text": "Ở hầu hết mọi lứa tuổi, tỷ suất chết của nam giới luôn cao hơn nữ giới do tai nạn lao động, lối sống và bệnh tim mạch.",
                        "icon": "activity"
                    }
                ],
                "speaker_notes": "ASFR là đầu vào trực tiếp để xây dựng Bảng sống nhân khẩu học.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "formula": "ASDR_x = (D_x / P_(x,tb)) * 1,000  (Đồ thị tử vong dạng chữ U kinh điển)"
            },
            {
                "slide_id": "SLIDE_15",
                "role": "CONTENT",
                "section": "TỬ VONG TRẺ EM",
                "assertion_title": "Đo Lường Tử Vong Trẻ Em: Tỷ Suất IMR Và U5MR Phản Ánh Trình Độ Y Tế",
                "primary_claim": "Tỷ suất tử vong trẻ sơ sinh (IMR) là thước đo nhạy cảm nhất phản ánh mức sống, dinh dưỡng và chất lượng y tế của một quốc gia.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Tử Vong Trẻ Dưới 1 Tuổi (IMR)",
                        "text": "IMR = (D_0 / B) * 1,000. Đo số trẻ chết trước sinh nhật 1 tuổi trên 1,000 trẻ sinh sống. Việt Nam giảm ấn tượng xuống 11.6‰ (2023).",
                        "icon": "heart"
                    },
                    {
                        "title": "Tử Vong Trẻ Dưới 5 Tuổi (U5MR)",
                        "text": "U5MR đo lường xác suất một đứa trẻ chết trước khi tròn 5 tuổi. Việt Nam hiện đạt mức khoảng 18.2‰.",
                        "icon": "shield"
                    },
                    {
                        "title": "Mục Tiêu Phát Triển Bền Vững (SDG)",
                        "text": "Chấm dứt các ca tử vong có thể phòng ngừa được ở trẻ sơ sinh và trẻ nhỏ thông qua tiêm chủng mở rộng và chăm sóc sơ sinh.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Giảm IMR là một trong những thành tựu nổi bật nhất của ngành y tế Việt Nam được Liên Hợp Quốc vinh danh.",
                "source_footer": "Báo cáo Mục tiêu Phát triển Bền vững (SDGs) Việt Nam",
                "formula": "IMR = (D_0 / B) * 1,000  |  U5MR = (D_0-4 / B) * 1,000  (‰)"
            },
            {
                "slide_id": "SLIDE_16",
                "role": "CONTENT",
                "section": "TỬ VONG BÀ MẸ",
                "assertion_title": "Tỷ Số Tử Vong Mẹ (MMR) Và Chăm Sóc Sức Khỏe Sinh Sản Phụ Nữ",
                "primary_claim": "Tỷ số tử vong mẹ đo lường số ca tử vong liên quan đến thai sản trên 100.000 trẻ sinh sống, phản ánh năng lực sản khoa.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_MMR",
                "atoms": [
                    {
                        "title": "Công Thức Đo Lường MMR",
                        "text": "MMR = (Số ca tử vong mẹ do thai sản / Số trẻ sinh sống) * 100,000. Việt Nam giảm xuống khoảng 44 ca / 100,000 ca sinh.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Các Nguyên Nhân Sản Khoa Chính",
                        "text": "Băng huyết sau sinh, tiền sản giật, nhiễm trùng hậu sản và tai biến sản khoa tại các vùng sâu vùng xa giao thông chia cắt.",
                        "icon": "alert-triangle"
                    },
                    {
                        "title": "Giải Pháp Mạng Lưới Sản Nhi",
                        "text": "Đào tạo cô đỡ thôn bản, nâng cấp trang thiết bị y tế tuyến huyện và triển khai hỗ trợ cấp cứu sản khoa từ xa (Telemedicine).",
                        "icon": "plus-circle"
                    }
                ],
                "speaker_notes": "Chênh lệch MMR giữa miền núi và đồng bằng vẫn còn lớn, đòi hỏi đầu tư mạnh cho mạng lưới y tế cơ sở.",
                "source_footer": "Bộ Y tế - Báo cáo Sức khỏe Sinh sản"
            },
            {
                "slide_id": "SLIDE_17",
                "role": "CONTENT",
                "section": "BẢNG SỐNG",
                "assertion_title": "Bảng Sống (Life Table) Và Kỳ Vọng Sống Khi Sinh (Life Expectancy)",
                "primary_claim": "Bảng sống là mô hình toán học nhân khẩu mô tả quá trình chết và sống sót của một thế hệ giả định từ khi sinh đến khi chết.",
                "visual_job": "DATA_TABLE",
                "visual_anchor": "LIFE_TABLE_STEPS",
                "atoms": [
                    {
                        "title": "Thế Hệ Giả Định (Radix: l_0)",
                        "text": "Xuất phát từ 100,000 trẻ sơ sinh cùng sinh ra tại thời điểm t = 0 và chịu tác động của tỷ suất chết ASDR hiện hành.",
                        "icon": "users"
                    },
                    {
                        "title": "Xác Suất Tử Vong (q_x)",
                        "text": "Tính toán xác suất một người ở độ tuổi x sẽ qua đời trước khi đạt độ tuổi x+n (n_q_x).",
                        "icon": "trending-down"
                    },
                    {
                        "title": "Số Người Còn Sống (l_x)",
                        "text": "Hàm số lượng người sống sót đến chính xác độ tuổi x. Cho thấy tốc độ hao mòn sinh học của thế hệ.",
                        "icon": "heart"
                    },
                    {
                        "title": "Kỳ Vọng Sống Khi Sinh (e_0)",
                        "text": "Số năm bình quân một đứa trẻ mới sinh có thể kỳ vọng sống được. Thước đo tổng hợp tối thượng về mức chết.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Bảng sống là công cụ nền tảng trong định phí bảo hiểm nhân thọ và tính toán quỹ hưu trí quốc gia.",
                "source_footer": "Nguyên lý lập Bảng sống nhân khẩu học",
                "table_data": {
                    "headers": [
                        "Độ Tuổi (x)",
                        "Số Sống Sót (lx)",
                        "Số Ca Tử Vong (dx)",
                        "Xác Suất Chết (qx)",
                        "Kỳ Vọng Sống (ex)"
                    ],
                    "rows": [
                        [
                            "0 (Sơ sinh)",
                            "100,000",
                            "1,160",
                            "0.0116",
                            "73.7 năm"
                        ],
                        [
                            "1 - 4 tuổi",
                            "98,840",
                            "660",
                            "0.0067",
                            "73.6 năm"
                        ],
                        [
                            "5 - 14 tuổi",
                            "98,180",
                            "390",
                            "0.0040",
                            "69.8 năm"
                        ],
                        [
                            "15 - 59 tuổi",
                            "97,790",
                            "12,450",
                            "0.1273",
                            "60.1 năm"
                        ],
                        [
                            "60 - 79 tuổi",
                            "85,340",
                            "42,800",
                            "0.5015",
                            "20.4 năm"
                        ],
                        [
                            "80 tuổi trở lên",
                            "42,540",
                            "42,540",
                            "1.0000",
                            "7.8 năm"
                        ]
                    ],
                    "col_widths": [
                        0.2,
                        0.2,
                        0.2,
                        0.2,
                        0.2
                    ]
                }
            },
            {
                "slide_id": "SLIDE_18",
                "role": "CONTENT",
                "section": "YẾU TỐ ẢNH HƯỞNG CHẾT",
                "assertion_title": "Bốn Nhóm Yếu Tố Tác Động Đến Xu Hướng Giảm Mức Chết Toàn Cầu",
                "primary_claim": "Tiến bộ y học, cải thiện nước sạch vệ sinh, nâng cao dinh dưỡng và phát triển an sinh xã hội đã kéo giảm mức chết ngoạn mục.",
                "visual_job": "CARDS",
                "visual_anchor": "FOUR_MORTALITY_FACTORS",
                "atoms": [
                    {
                        "title": "Tiến Bộ Y Học & Vắc-xin",
                        "text": "Phát minh kháng sinh, chương trình tiêm chủng mở rộng và kỹ thuật phẫu thuật hiện đại xóa bỏ đại dịch truyền nhiễm.",
                        "icon": "shield"
                    },
                    {
                        "title": "Nước Sạch & Môi Trường Vệ Sinh",
                        "text": "Xử lý nước thải, cung cấp nước sạch sinh hoạt và vệ sinh an toàn thực phẩm ngăn ngừa các bệnh tiêu chảy chết người.",
                        "icon": "droplet"
                    },
                    {
                        "title": "Nâng Cao Thu Nhập & Dinh Dưỡng",
                        "text": "Xóa đói giảm nghèo bảo đảm chế độ calo và vi chất dinh dưỡng đầy đủ, gia tăng sức đề kháng tự nhiên của cơ thể.",
                        "icon": "dollar-sign"
                    }
                ],
                "speaker_notes": "Sự suy giảm mức chết là thành tựu vĩ đại nhất của nền văn minh nhân loại trong 150 năm qua.",
                "source_footer": "Lịch sử dịch tễ học và y tế công cộng"
            },
            {
                "slide_id": "SLIDE_19",
                "role": "CONTENT",
                "section": "TUỔI THỌ VIỆT NAM",
                "assertion_title": "Thành Tựu Tăng Tuổi Thọ Bình Quân Của Dân Số Việt Nam Đạt 73.7 Tuổi",
                "primary_claim": "Tuổi thọ bình quân của người Việt Nam tăng ấn tượng từ 40 tuổi (1960) lên 73.7 tuổi (2023), nữ giới thọ hơn nam 5.4 tuổi.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "LIFE_EXPECTANCY_WATERFALL",
                "atoms": [
                    {
                        "title": "Tuổi Thọ Bình Quân: 73.7 Tuổi",
                        "text": "Nam giới đạt 71.1 tuổi, Nữ giới đạt 76.5 tuổi. Việt Nam có tuổi thọ cao hơn mức trung bình của các nước có cùng thu nhập.",
                        "icon": "heart"
                    },
                    {
                        "title": "Chênh Lệch Giới Tính 5.4 Năm",
                        "text": "Nữ giới sống thọ hơn nam phản ánh ưu thế sinh học và tỷ lệ tử vong do tai nạn, rượu bia thuốc lá ở nam giới cao hơn.",
                        "icon": "users"
                    },
                    {
                        "title": "Khoảng Trống Tuổi Thọ Khỏe Mạnh",
                        "text": "Kỳ vọng sống khỏe mạnh chỉ đạt khoảng 64 tuổi; người cao tuổi Việt Nam gánh chịu trung bình 8-9 năm ốm đau bệnh tật.",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "Mục tiêu hiện nay không chỉ là sống thọ mà là nâng cao số năm sống khỏe mạnh không tàn tật (HALE).",
                "source_footer": "Tổng cục Thống kê - Báo cáo Tình hình Dân số"
            },
            {
                "slide_id": "SLIDE_20",
                "role": "CONTENT",
                "section": "GIA TĂNG TỰ NHIÊN",
                "assertion_title": "Tỷ Suất Tăng Tự Nhiên (NIR) Và Phương Trình Cân Bằng Sinh - Tử",
                "primary_claim": "Tỷ suất gia tăng tự nhiên phản ánh hiệu số giữa mức sinh và mức chết, quyết định tốc độ tăng trưởng cơ bản của quốc gia.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Công Thức Tính NIR",
                        "text": "NIR = CBR - CDR (tính theo đơn vị ‰) hoặc NIR(%) = (CBR - CDR) / 10. Ở Việt Nam hiện nay CBR ~14.5‰, CDR ~6.1‰ -> NIR ~0.84%/năm.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Quy Luật Thu Hẹp Khoảng Cách",
                        "text": "Khi mức sinh giảm dần về mức thay thế trong khi mức chết chạm đáy và hơi tăng do già hóa, NIR sẽ dần tiến về 0%.",
                        "icon": "trending-down"
                    }
                ],
                "speaker_notes": "NIR tiệm cận 0% là dấu hiệu cho thấy quy mô dân số chuẩn bị đạt đỉnh cực đại.",
                "source_footer": "Giáo trình Dân số học đại cương",
                "chart_type": "MORTALITY_CURVE_GOMPERTZ"
            },
            {
                "slide_id": "SLIDE_21",
                "role": "CONTENT",
                "section": "QUÁ ĐỘ DÂN SỐ",
                "assertion_title": "Mô Hình Chuyển Tiếp Dân Số Bốn Giai Đoạn (Demographic Transition)",
                "primary_claim": "Mô hình kinh điển giải thích quy luật chuyển dịch từ trạng thái sinh cao - chết cao sang trạng thái sinh thấp - chết thấp.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "FOUR_STAGES",
                "atoms": [
                    {
                        "title": "Giai Đoạn 1: Tiền Chuyển Tiếp",
                        "text": "Sinh cao và chết cao. Quy mô dân số tăng trưởng rất chậm chạp, thường xuyên gặp dịch bệnh và nạn đói.",
                        "icon": "circle"
                    },
                    {
                        "title": "Giai Đoạn 2: Bùng Nổ Dân Số",
                        "text": "Mức chết giảm mạnh nhờ tiến bộ y tế trong khi mức sinh vẫn giữ ở mức cao. Dân số tăng vọt đột biến.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Giai Đoạn 3: Suy Giảm Mức Sinh",
                        "text": "Đô thị hóa và chi phí nuôi dạy con khiến mức sinh giảm nhanh. Tốc độ tăng trưởng dân số chậm dần.",
                        "icon": "trending-down"
                    },
                    {
                        "title": "Giai Đoạn 4: Hậu Chuyển Tiếp",
                        "text": "Cả sinh và chết đều ở mức thấp. Quy mô dân số ổn định hoặc suy giảm, già hóa dân số diễn ra sâu rộng.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Việt Nam hiện đang ở cuối Giai đoạn 3 và chuẩn bị bước hẳn sang Giai đoạn 4 của mô hình quá độ.",
                "source_footer": "Lý thuyết chuyển tiếp dân số (Frank Notestein Model)",
                "chart_type": "DEMO_TRANSITION_STAGES"
            },
            {
                "slide_id": "SLIDE_22",
                "role": "CONTENT",
                "section": "TỔNG KẾT BÀI HỌC",
                "assertion_title": "Tổng Kết Chuyên Đề Và Bài Tập Phân Tích Mức Sinh - Mức Chết",
                "primary_claim": "Làm chủ phương pháp tính TFR, phân tích bảng sống và đề xuất giải pháp chính sách duy trì mức sinh thay thế.",
                "visual_job": "CARDS",
                "visual_anchor": "SUMMARY_QUESTIONS",
                "atoms": [
                    {
                        "title": "Bài Tập Tính TFR",
                        "text": "Cho chuỗi tỷ suất sinh đặc trưng theo tuổi ASFR (nhóm 15-49). Hãy tính Tổng tỷ suất sinh TFR và rút ra kết luận mức sinh.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Bài Tập Phân Tích Bảng Sống",
                        "text": "Dựa vào bảng sống rút gọn, tính toán kỳ vọng sống còn lại ở độ tuổi 60 (e_60) để phục vụ tính toán quỹ bảo hiểm xã hội.",
                        "icon": "file-text"
                    },
                    {
                        "title": "Câu Hỏi Thảo Luận Chính Sách",
                        "text": "Tại sao các chính sách khuyến sinh ở Hàn Quốc, Singapore ít hiệu quả? Bài học nào cho các đô thị lớn tại Việt Nam?",
                        "icon": "message-square"
                    }
                ],
                "speaker_notes": "Học viên chuẩn bị thảo luận nhóm theo bài tập tính toán trên lớp. Xin cảm ơn quý học viên.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
            }
        ]
    }


def get_lesson_blueprints_bai_4() -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "lesson_index": 4,
        "deck_title": "Phân Bố Dân Số, Di Dân Và Đô Thị Hóa",
        "total_slides": 22,
        "visual_system": "MODERN_REFINED",
        "slides": [
            {
                "slide_id": "SLIDE_01",
                "role": "COVER",
                "section": "TỔNG QUAN CHUYÊN ĐỀ",
                "assertion_title": "BÀI 4: PHÂN BỐ DÂN SỐ, DI DÂN VÀ ĐÔ THỊ HÓA",
                "primary_claim": "Không gian phân bố dân cư, các luồng di chuyển cơ học và tiến trình đô thị hóa trong phát triển kinh tế - xã hội.",
                "visual_job": "HERO_TITLE",
                "visual_anchor": "BRAND_COVER",
                "speaker_notes": "Kính chào quý học viên, Bài 4 phân tích chiều kích không gian của dân số: phân bố lãnh thổ, di dân và đô thị hóa.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia",
                "illustration": "illustration_bai_4.jpg"
            },
            {
                "slide_id": "SLIDE_02",
                "role": "CONTENT",
                "section": "MỤC TIÊU BÀI HỌC",
                "assertion_title": "Năng Lực Khảo Sát Không Gian Dân Cư Và Luồng Dịch Chuyển Nhân Khẩu",
                "primary_claim": "Làm chủ các thước đo mật độ, đường cong Lorenz, lý thuyết di dân lực đẩy - lực kéo và quy hoạch đô thị vệ tinh.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_OBJECTIVES",
                "atoms": [
                    {
                        "title": "Đo Lường Phân Bố Dân Số",
                        "text": "Tính toán mật độ dân số số học, mật độ kinh tế và vẽ đường cong Lorenz đánh giá độ tập trung không gian dân cư.",
                        "icon": "map-pin"
                    },
                    {
                        "title": "Phân Tích Động Lực Di Dân",
                        "text": "Nhận diện 4 luồng di dân nội địa chủ yếu và vận dụng mô hình lực đẩy - lực kéo giải thích làn sóng dịch chuyển lao động.",
                        "icon": "shuffle"
                    },
                    {
                        "title": "Đô Thị Hóa & Quy Hoạch Không Gian",
                        "text": "Đánh giá tốc độ đô thị hóa, áp lực lên siêu đô thị và đề xuất giải pháp phát triển chuỗi đô thị vệ tinh sinh thái bền vững.",
                        "icon": "home"
                    }
                ],
                "speaker_notes": "Chuẩn đầu ra gắn chặt với kỹ năng phân tích không gian địa lý nhân khẩu và hoạch định quy hoạch vùng.",
                "source_footer": "Khung chuẩn đầu ra chuyên đề"
            },
            {
                "slide_id": "SLIDE_03",
                "role": "CONTENT",
                "section": "PHÂN BỐ DÂN SỐ",
                "assertion_title": "Khái Niệm Phân Bố Dân Số Và Tính Không Gian Của Hiện Tượng Nhân Khẩu",
                "primary_claim": "Phân bố dân số là sự sắp xếp, phân bổ tập hợp người trên bề mặt lãnh thổ tại một thời điểm xác định.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Tính Lịch Sử Và Địa Lý Tự Nhiên",
                        "text": "Dân cư tập trung đông đúc ở các vùng đồng bằng châu thổ phì nhiêu, nguồn nước thuận tiện và mạng lưới giao thông thủy bộ.",
                        "icon": "globe"
                    },
                    {
                        "title": "Tính Quy Định Bởi Kinh Tế",
                        "text": "Nơi nào có mật độ khu công nghiệp, dịch vụ và cơ hội việc làm thu nhập cao thì nơi đó hút dân cư tập trung sinh sống.",
                        "icon": "briefcase"
                    }
                ],
                "speaker_notes": "Phân bố dân số không bao giờ bất biến mà liên tục tái sắp xếp theo chiến lược phát triển kinh tế vùng.",
                "source_footer": "Giáo trình Địa lý nhân khẩu học",
                "illustration": "ai_bai_4_distribution.jpg"
            },
            {
                "slide_id": "SLIDE_04",
                "role": "CONTENT",
                "section": "MẬT ĐỘ DÂN SỐ",
                "assertion_title": "Mật Độ Dân Số Số Học Và Mật Độ Dân Số Kinh Tế",
                "primary_claim": "Mật độ dân số phản ánh tương quan giữa quy mô số dân và diện tích không gian lãnh thổ cư trú.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Mật Độ Số Học (Crude Density)",
                        "text": "D = P / S (người/km²). Với P là tổng dân số, S là tổng diện tích tự nhiên. Việt Nam đạt gần 300 người/km² (thuộc nhóm cao).",
                        "icon": "calculator"
                    },
                    {
                        "title": "Mật Độ Kinh Tế Nông Nghiệp",
                        "text": "Số dân nông nghiệp trên một đơn vị diện tích đất canh tác nông nghiệp, phản ánh chính xác sức ép dân số lên tư liệu sản xuất.",
                        "icon": "pie-chart"
                    },
                    {
                        "title": "Mật Độ Đô Thị Thực Tế",
                        "text": "Mật độ dân cư trên diện tích đất xây dựng đô thị, phản ánh trực tiếp nguy cơ quá tải hạ tầng giao thông và thoát nước.",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "Mật độ số học chỉ cho biết con số bình quân; mật độ kinh tế mới phản ánh chính xác áp lực sống của người dân.",
                "source_footer": "Phương pháp đo lường không gian dân số",
                "formula": "D_sohoc = P / S (người/km²)  |  D_kinhte = P / S_nongnghiep (người/ha)"
            },
            {
                "slide_id": "SLIDE_05",
                "role": "CONTENT",
                "section": "ĐƯỜNG CONG LORENZ",
                "assertion_title": "Đường Cong Lorenz Và Đánh Giá Độ Tập Trung Không Gian Dân Cư",
                "primary_claim": "Đường cong Lorenz và hệ số bất bình đẳng không gian phản ánh mức độ phân bố đồng đều hay tập trung cục bộ của dân số.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "BENTO_LORENZ",
                "atoms": [
                    {
                        "title": "Nguyên Lý Đường Cong Lorenz",
                        "text": "Đồ thị biểu diễn phần trăm tích lũy dân số so với phần trăm tích lũy diện tích các đơn vị hành chính thành phần.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Đường Bình Đẳng Tuyệt Đối",
                        "text": "Đường chéo 45 độ: nếu đường cong càng phình xa đường chéo, mức độ tập trung dân số vào một vài vùng càng cực đoan.",
                        "icon": "maximize"
                    },
                    {
                        "title": "Ứng Dụng Trong Quy Hoạch Vùng",
                        "text": "Nhận diện tình trạng mất cân đối không gian để xây dựng chính sách phân bố lại lực lượng sản xuất và dịch cư có tổ chức.",
                        "icon": "map"
                    }
                ],
                "speaker_notes": "Đường cong Lorenz là công cụ định lượng chuẩn mực giúp đo độ méo mó của không gian nhân khẩu học.",
                "source_footer": "Kỹ thuật phân tích không gian kinh tế - xã hội",
                "chart_type": "URBAN_RURAL_DIVERGENCE_BUBBLE"
            },
            {
                "slide_id": "SLIDE_06",
                "role": "CONTENT",
                "section": "PHÂN BỐ DÂN CƯ VN",
                "assertion_title": "Đặc Điểm Phân Bố Dân Cư Trên Sáu Vùng Kinh Tế - Xã Hội Việt Nam",
                "primary_claim": "Dân cư Việt Nam phân bố rất chênh lệch: tập trung đậm đặc ở hai vùng đồng bằng châu thổ và thưa thớt ở vùng miền núi.",
                "visual_job": "DATA_TABLE",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "REGIONAL_DENSITY",
                "atoms": [
                    {
                        "title": "Đồng Bằng Sông Hồng (>1,000 người/km²)",
                        "text": "Vùng có mật độ dân số cao nhất cả nước, gấp 3.5 lần mức trung bình toàn quốc, áp lực nhà ở và môi trường cực lớn.",
                        "icon": "map-pin"
                    },
                    {
                        "title": "Đông Nam Bộ (>750 người/km²)",
                        "text": "Vùng kinh tế năng động nhất, hút dòng di cư lao động khổng lồ, tạo nên siêu vùng đô thị TP.HCM - Bình Dương - Đồng Nai.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Tây Bắc & Tây Nguyên (<150 người/km²)",
                        "text": "Địa bàn chiến lược về quốc phòng và sinh thái nhưng mật độ dân cư thưa thớt, khó khăn trong tổ chức mạng lưới dịch vụ công.",
                        "icon": "compass"
                    }
                ],
                "speaker_notes": "Chênh lệch mật độ giữa Đồng bằng sông Hồng và Tây Bắc lên tới hơn 10 lần, tạo ra thách thức lớn cho phát triển đồng đều.",
                "source_footer": "Niên giám Thống kê Việt Nam",
                "table_data": {
                    "headers": [
                        "Vùng Kinh Tế - Xã Hội",
                        "Dân Số (Triệu)",
                        "Tỷ Trọng (%)",
                        "Mật Độ (ng/km²)",
                        "Di Cư Thuần (‰)"
                    ],
                    "rows": [
                        [
                            "Đồng Bằng Sông Hồng",
                            "23.4 Triệu",
                            "23.4%",
                            "1,090 ng/km²",
                            "+2.1 ‰ (Hút di dân)"
                        ],
                        [
                            "Trung Du & MN Phía Bắc",
                            "13.0 Triệu",
                            "13.0%",
                            "136 ng/km²",
                            "-2.8 ‰ (Xuất cư)"
                        ],
                        [
                            "Bắc Trung Bộ & Duyên Hải MT",
                            "20.7 Triệu",
                            "20.7%",
                            "216 ng/km²",
                            "-3.5 ‰ (Xuất cư)"
                        ],
                        [
                            "Tây Nguyên",
                            "6.1 Triệu",
                            "6.1%",
                            "111 ng/km²",
                            "-0.8 ‰ (Cân bằng)"
                        ],
                        [
                            "Đông Nam Bộ",
                            "18.8 Triệu",
                            "18.8%",
                            "795 ng/km²",
                            "+11.2 ‰ (Đô thị hóa cao)"
                        ],
                        [
                            "Đồng Bằng Sông Cửu Long",
                            "17.5 Triệu",
                            "17.5%",
                            "426 ng/km²",
                            "-4.6 ‰ (Xuất cư lớn)"
                        ]
                    ],
                    "col_widths": [
                        0.28,
                        0.18,
                        0.16,
                        0.18,
                        0.2
                    ]
                }
            },
            {
                "slide_id": "SLIDE_07",
                "role": "CONTENT",
                "section": "CHÊNH LỆCH ĐỊA BÀN",
                "assertion_title": "Sự Chênh Lệch Phân Bố Giữa Nông Thôn - Thành Thị Và Đồng Bằng - Miền Núi",
                "primary_claim": "Hơn 58% dân số vẫn sinh sống ở nông thôn nhưng dòng chuyển dịch sang đô thị đang diễn ra với tốc độ tăng dần.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Khu Vực Nông Thôn (58%)",
                        "text": "Lực lượng lao động già hóa do thanh niên di cư ra thành phố; kinh tế nông nghiệp đòi hỏi cơ giới hóa để giải quyết thiếu lao động.",
                        "icon": "home"
                    },
                    {
                        "title": "Khu Vực Đô Thị (42%)",
                        "text": "Tập trung lực lượng lao động trẻ, đóng góp hơn 70% GDP cả nước nhưng đối mặt bài toán ách tắc giao thông và ô nhiễm không khí.",
                        "icon": "briefcase"
                    }
                ],
                "speaker_notes": "Sự chênh lệch này thúc đẩy các dòng di chuyển cư trú cơ học nhằm tìm kiếm sinh kế và điều kiện sống tốt hơn.",
                "source_footer": "Báo cáo Tổng điều tra dân số và nhà ở"
            },
            {
                "slide_id": "SLIDE_08",
                "role": "CONTENT",
                "section": "KHÁI NIỆM DI DÂN",
                "assertion_title": "Khái Niệm Di Dân (Migration) Và Các Tiêu Chí Xác Định Dòng Cư Trú",
                "primary_claim": "Di dân là sự di chuyển không gian của con người gắn liền với sự thay đổi nơi cư trú thường xuyên trong một khoảng thời gian xác định.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Ba Thành Tố Cơ Bản Của Di Dân",
                        "text": "Nơi xuất phát (Nơi đi), Nơi tiếp nhận (Nơi đến), và Khoảng cách ranh giới hành chính vượt qua (xã, huyện, tỉnh hoặc quốc gia).",
                        "icon": "navigation"
                    },
                    {
                        "title": "Tiêu Chí Thời Gian Cư Trú (6 Tháng)",
                        "text": "Quy ước thống kê chuẩn mực: thời gian cư trú thực tế tại nơi đến từ 6 tháng trở lên mới được tính là di dân thường trú.",
                        "icon": "calendar"
                    }
                ],
                "speaker_notes": "Cần phân biệt rõ di dân với các hình thức di chuyển tạm thời như du lịch, công tác, du học ngắn hạn hoặc đi lại hàng ngày.",
                "source_footer": "Giáo trình Dân số học đại cương"
            },
            {
                "slide_id": "SLIDE_09",
                "role": "CONTENT",
                "section": "PHÂN LOẠI DI DÂN",
                "assertion_title": "Phân Loại Di Dân Theo Không Gian Lãnh Thổ, Tính Chất Và Mục Đích",
                "primary_claim": "Phân loại chính xác các hình thái di cư giúp xây dựng chính sách quản lý cư trú và phân bổ ngân sách hạ tầng hiệu quả.",
                "visual_job": "CARDS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Di Dân Nội Địa vs Quốc Tế",
                        "text": "Di cư giữa các vùng, các tỉnh trong nước (nội địa) đối lập với di cư vượt qua biên giới quốc gia (xuất cư, nhập cư quốc tế).",
                        "icon": "globe"
                    },
                    {
                        "title": "Di Dân Có Tổ Chức vs Tự Do",
                        "text": "Di dân theo kế hoạch khai hoang, xây dựng vùng kinh tế mới của nhà nước đối lập với dòng di dân tự do theo quy luật thị trường.",
                        "icon": "file-text"
                    },
                    {
                        "title": "Di Dân Lao Động vs Cưỡng Bức",
                        "text": "Di cư tự nguyện tìm kiếm việc làm, học tập đối lập với tị nạn do thiên tai, biến đổi khí hậu hoặc xung đột vũ trang.",
                        "icon": "shield"
                    }
                ],
                "speaker_notes": "Tại Việt Nam hiện nay, di cư tự do vì mục đích kinh tế việc làm chiếm tỷ trọng áp đảo tuyệt đối.",
                "source_footer": "Sổ tay nghiên cứu di cư"
            },
            {
                "slide_id": "SLIDE_10",
                "role": "CONTENT",
                "section": "THƯỚC ĐO DI DÂN",
                "assertion_title": "Hệ Thống Các Thước Đo Đo Lường Cường Độ Di Dân: IR, OR, NMR",
                "primary_claim": "Các tỷ suất di cư phản ánh cường độ dịch chuyển nhân khẩu đến và đi của một địa phương trên 1.000 dân.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "MIGRATION_METRICS",
                "atoms": [
                    {
                        "title": "Tỷ Suất Nhập Cư (In-Migration: IR)",
                        "text": "IR = (I / P_tb) * 1,000 (‰). Đo lường sức hút lao động của các vùng công nghiệp như Bình Dương, Bắc Ninh.",
                        "icon": "log-in"
                    },
                    {
                        "title": "Tỷ Suất Xuất Cư (Out-Migration: OR)",
                        "text": "OR = (O / P_tb) * 1,000 (‰). Đo lường mức độ ly hương của các vùng nông nghiệp có thu nhập thấp.",
                        "icon": "log-out"
                    },
                    {
                        "title": "Tỷ Suất Di Cư Thuần (Net: NMR)",
                        "text": "NMR = IR - OR = ((I - O) / P_tb) * 1,000. Nếu NMR dương: vùng hút dân; nếu NMR âm: vùng xuất cư ròng.",
                        "icon": "shuffle"
                    }
                ],
                "speaker_notes": "NMR là chỉ báo tốt nhất phản ánh cán cân dịch chuyển nhân khẩu giữa các tỉnh thành.",
                "source_footer": "Phương pháp thống kê di cư - Tổng cục Thống kê",
                "formula": "NMR = [(I - O) / P_tb] * 1,000  |  MER = [(I - O) / (I + O)] * 100"
            },
            {
                "slide_id": "SLIDE_11",
                "role": "CONTENT",
                "section": "LÝ THUYẾT DI DÂN",
                "assertion_title": "Lý Thuyết Lực Đẩy - Lực Kéo (Push-Pull Factors) Của Everett Lee",
                "primary_claim": "Quyết định di cư là kết quả tương tác giữa các yếu tố đẩy tiêu cực tại nơi đi và các yếu tố kéo hấp dẫn tại nơi đến.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_PUSHPULL",
                "atoms": [
                    {
                        "title": "Lực Đẩy Tại Nơi Đi (Push Factors)",
                        "text": "Thiếu đất canh tác, việc làm bấp bênh, thu nhập thấp, thiên tai hạn hán bão lũ và thiếu hụt dịch vụ vui chơi giải trí.",
                        "icon": "arrow-up-right"
                    },
                    {
                        "title": "Lực Kéo Tại Nơi Đến (Pull Factors)",
                        "text": "Cơ hội việc làm lương cao, hệ thống giáo dục đại học tiên tiến, mạng lưới bệnh viện hiện đại và môi trường sống sôi động.",
                        "icon": "arrow-down-left"
                    },
                    {
                        "title": "Rào Cản Trung Gian & Yếu Tố Cá Nhân",
                        "text": "Khoảng cách địa lý, chi phí dịch chuyển, rào cản đăng ký cư trú hộ khẩu và tính cách sẵn sàng chấp nhận rủi ro.",
                        "icon": "sliders"
                    }
                ],
                "speaker_notes": "Mô hình Everett Lee là khung lý thuyết kinh điển giúp giải thích toàn bộ động cơ dịch chuyển của người lao động.",
                "source_footer": "Lý thuyết di cư Everett Lee (A Theory of Migration)"
            },
            {
                "slide_id": "SLIDE_12",
                "role": "CONTENT",
                "section": "LUỒNG DI DÂN VN",
                "assertion_title": "Bốn Luồng Di Dân Nội Địa Chủ Yếu Định Hình Bản Đồ Lao Động Việt Nam",
                "primary_claim": "Phân hóa 4 dòng di cư phản ánh quá trình công nghiệp hóa và chuyển dịch cơ cấu việc làm của đất nước.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "FOUR_STREAMS",
                "atoms": [
                    {
                        "title": "Nông Thôn - Đô Thị (Chiếm Ưu Thế)",
                        "text": "Luồng di cư lớn nhất: thanh niên nông thôn đổ về các đại đô thị tìm việc làm trong ngành may mặc, xây dựng và dịch vụ.",
                        "icon": "arrow-right"
                    },
                    {
                        "title": "Nông Thôn - Nông Thôn (Kinh Tế Mới)",
                        "text": "Dòng di dân lịch sử từ đồng bằng lên Tây Nguyên, Tây Bắc phát triển cây công nghiệp (cà phê, cao su, hồ tiêu).",
                        "icon": "arrow-right"
                    },
                    {
                        "title": "Đô Thị - Đô Thị (Chuyển Dịch Bậc Cao)",
                        "text": "Dịch chuyển của lao động có chuyên môn kỹ thuật cao giữa các thành phố lớn hoặc từ đô thị nhỏ sang siêu đô thị.",
                        "icon": "arrow-right"
                    },
                    {
                        "title": "Đô Thị - Nông Thôn (Xu Hướng Mới)",
                        "text": "Xu hướng người cao tuổi hồi hương dưỡng già hoặc lao động trẻ về quê lập nghiệp (khởi nghiệp nông nghiệp công nghệ cao).",
                        "icon": "arrow-left"
                    }
                ],
                "speaker_notes": "Luồng Nông thôn - Đô thị tạo động lực tăng trưởng kinh tế nhưng đặt gánh nặng khổng lồ lên vai các thành phố lớn.",
                "source_footer": "Điều tra Di cư nội địa Việt Nam",
                "chart_type": "REGIONAL_DENSITY"
            },
            {
                "slide_id": "SLIDE_13",
                "role": "CONTENT",
                "section": "DI DÂN ĐÔ THỊ",
                "assertion_title": "Luồng Di Dân Nông Thôn - Đô Thị: Động Lực Tăng Trưởng Và Sức Ép Hạ Tầng",
                "primary_claim": "Di cư đóng góp to lớn vào năng suất quốc gia nhưng tạo áp lực gay gắt về nhà ở, trường học và bảo hiểm xã hội.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Lợi Ích Kinh Tế Đột Phá",
                        "text": "Cung cấp nguồn lao động dồi dào, giá hợp lý cho các khu chế xuất; chuyển kiều hối nội địa về xây dựng nông thôn mới.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "Thách Thức Tích Hợp Xã Hội",
                        "text": "Người di cư đối mặt điều kiện nhà trọ chật chội, khó khăn trong tiếp cận trường học công lập cho con em và bảo hiểm y tế.",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "Chính sách quản lý hiện đại cần xóa bỏ rào cản phân biệt cư trú, tạo điều kiện hòa nhập cho người nhập cư.",
                "source_footer": "Viện Nghiên cứu Quản lý Kinh tế Trung ương (CIEM)",
                "illustration": "ai_bai_4_industrial.jpg"
            },
            {
                "slide_id": "SLIDE_14",
                "role": "CONTENT",
                "section": "DI DÂN QUỐC TẾ",
                "assertion_title": "Di Dân Lao Động Quốc Tế Và Dòng Kiều Hối Đóng Góp Phát Triển Quốc Gia",
                "primary_claim": "Hàng trăm nghìn lao động xuất khẩu mỗi năm gửi về lượng kiều hối khổng lồ nhưng đòi hỏi chính sách bảo hộ công dân.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Xuất Khẩu Lao Động (>150,000 người/năm)",
                        "text": "Thị trường chủ yếu: Nhật Bản, Đài Loan, Hàn Quốc. Giúp thanh niên học hỏi tác phong công nghiệp và ngoại ngữ.",
                        "icon": "plane"
                    },
                    {
                        "title": "Nguồn Kiều Hối Dồi Dào (>18 Tỷ USD)",
                        "text": "Việt Nam nằm trong top 10 quốc gia nhận kiều hối lớn nhất thế giới, củng cố nguồn dự trữ ngoại hối và đầu tư tư nhân.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "Thách Thức Chảy Máu Chất Xám",
                        "text": "Tình trạng nhiều chuyên gia, du học sinh giỏi không quay về nước, đòi hỏi chính sách đãi ngộ nhân tài hấp dẫn hơn.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Kiều hối là nguồn lực quý giá, nhưng mục tiêu lâu dài là phát triển việc làm chất lượng cao ngay tại trong nước.",
                "source_footer": "Ngân hàng Thế giới (World Bank Migration and Development Brief)",
                "chart_type": "MIGRATION_FLOWS_MATRIX"
            },
            {
                "slide_id": "SLIDE_15",
                "role": "CONTENT",
                "section": "TÁC ĐỘNG DI DÂN",
                "assertion_title": "Tác Động Hai Mặt Của Di Dân Đến Sự Phát Triển Của Vùng Đi Và Vùng Đến",
                "primary_claim": "Di dân là con dao hai lưỡi: giải tỏa áp lực đất đai cho vùng đi và cấp lao động cho vùng đến, nhưng làm xáo trộn cấu trúc xã hội.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_SIDES",
                "atoms": [
                    {
                        "title": "Tác Động Đến Nơi Đi (Xuất Cư)",
                        "text": "Giảm áp lực thiếu đất, nhận nguồn kiều hối nhưng mất đi lực lượng lao động trẻ khỏe, phụ nữ và người già phải gánh việc đồng áng.",
                        "icon": "log-out"
                    },
                    {
                        "title": "Tác Động Đến Nơi Đến (Nhập Cư)",
                        "text": "Bổ sung lao động năng động, kích thích tiêu dùng nhưng gây áp lực lên bệnh viện, trường học, nước sạch và an ninh trật tự.",
                        "icon": "log-in"
                    },
                    {
                        "title": "Giải Pháp Điều Hòa Lợi Ích",
                        "text": "Phát triển công nghiệp vệ tinh và dịch vụ tại các tỉnh xuất cư để người lao động 'ly nông bất ly hương'.",
                        "icon": "refresh-cw"
                    }
                ],
                "speaker_notes": "Chính sách quy hoạch cần hướng tới cân bằng lợi ích giữa vùng xuất cư và vùng nhập cư.",
                "source_footer": "Giáo trình Kinh tế phát triển",
                "illustration": "cinematic_bai_4_megacity.jpg"
            },
            {
                "slide_id": "SLIDE_16",
                "role": "CONTENT",
                "section": "ĐÔ THỊ HÓA",
                "assertion_title": "Khái Niệm Đô Thị Hóa Và Các Tiêu Chí Định Danh Khu Vực Đô Thị",
                "primary_claim": "Đô thị hóa là quá trình kinh tế - xã hội làm tăng tỷ trọng dân cư đô thị và lan tỏa lối sống văn minh đô thị về nông thôn.",
                "visual_job": "COMPARISON",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Phương Diện Nhân Khẩu & Lãnh Thổ",
                        "text": "Sự tập trung dân cư với mật độ cao, mở rộng diện tích đất phi nông nghiệp và hình thành hệ thống hạ tầng đồng bộ.",
                        "icon": "home"
                    },
                    {
                        "title": "Phương Diện Văn Hóa & Lối Sống",
                        "text": "Chuyển biến cơ cấu nghề nghiệp sang công nghiệp - dịch vụ, thay đổi lối sống từ cộng đồng khép kín sang năng động, chuyên nghiệp.",
                        "icon": "coffee"
                    }
                ],
                "speaker_notes": "Đô thị hóa không chỉ là xây nhà cao tầng mà cốt lõi là sự chuyển hóa lối sống và cơ cấu kinh tế.",
                "source_footer": "Luật Quy hoạch Đô thị Việt Nam"
            },
            {
                "slide_id": "SLIDE_17",
                "role": "CONTENT",
                "section": "THƯỚC ĐO ĐÔ THỊ HÓA",
                "assertion_title": "Các Chỉ Số Đo Lường Đô Thị Hóa: Tỷ Lệ Đô Thị Hóa (PU) Và Tốc Độ Tăng",
                "primary_claim": "Tỷ lệ đô thị hóa là thước đo chuẩn mực phản ánh mức độ hiện đại hóa và chuyển dịch kinh tế của một quốc gia.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "URBAN_METRICS",
                "atoms": [
                    {
                        "title": "Tỷ Lệ Đô Thị Hóa (PU)",
                        "text": "PU = (Dân số đô thị / Tổng dân số) * 100 (%). Việt Nam tăng từ 30.5% (2009) lên 38.1% (2019) và đạt ~42% vào năm 2024.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Tốc Độ Đô Thị Hóa (UR)",
                        "text": "Đo lường tốc độ tăng trưởng của tỷ lệ đô thị hóa qua các năm, phản ánh nhịp độ chuyển dịch cơ cấu kinh tế.",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Tỷ Lệ Lao Động Phi Nông Nghiệp",
                        "text": "Tỷ trọng lao động làm việc trong khu vực công nghiệp và dịch vụ, thường đạt trên 75% tại các đô thị tiêu chuẩn.",
                        "icon": "briefcase"
                    }
                ],
                "speaker_notes": "Nghị quyết 06-NQ/TW đặt mục tiêu tỷ lệ đô thị hóa của Việt Nam đạt trên 45% vào năm 2025 và trên 50% vào năm 2030.",
                "source_footer": "Nghị quyết 06-NQ/TW của Bộ Chính trị về phát triển đô thị",
                "formula": "PU(%) = (P_u / P_total) * 100  |  UR = [(P_u,t - P_u,0) / t] * 100"
            },
            {
                "slide_id": "SLIDE_18",
                "role": "CONTENT",
                "section": "ĐÔ THỊ HÓA VN",
                "assertion_title": "Tiến Trình Đô Thị Hóa Tại Việt Nam: Động Lực Chủ Lực Của Tăng Trưởng GDP",
                "primary_claim": "Khu vực đô thị đóng góp hơn 70% tổng GDP cả nước, là trung tâm đổi mới sáng tạo, khoa học công nghệ và hội nhập quốc tế.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "URBANIZATION_SCURVE",
                "atoms": [
                    {
                        "title": "Mạng Lưới Đô Thị Phát Triển Rộng Khắp",
                        "text": "Cả nước có gần 900 đô thị các loại từ đô thị đặc biệt, loại I đến loại V, tạo thành bộ khung kết nối vùng vững chắc.",
                        "icon": "map"
                    },
                    {
                        "title": "Đầu Tàu Tăng Trưởng Kinh Tế",
                        "text": "Năng suất lao động tại đô thị cao gấp gần 2 lần so với mức bình quân nông thôn nhờ tập trung vốn và công nghệ cao.",
                        "icon": "zap"
                    },
                    {
                        "title": "Chất Lượng Đô Thị Chưa Đồng Đều",
                        "text": "Đô thị hóa nhanh về mặt diện tích và dân số nhưng hạ tầng kỹ thuật và hạ tầng xã hội chưa theo kịp tương xứng.",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "Đô thị hóa là động lực không thể đảo ngược, nhưng cần chuyển từ đô thị hóa mở rộng sang nâng cao chất lượng sống đô thị.",
                "source_footer": "Bộ Xây dựng - Báo cáo Phát triển Đô thị Việt Nam"
            },
            {
                "slide_id": "SLIDE_19",
                "role": "CONTENT",
                "section": "SIÊU ĐÔ THỊ",
                "assertion_title": "Sự Phát Triển Của Hai Siêu Đô Thị: Hà Nội Và Thành Phố Hồ Chí Minh",
                "primary_claim": "Hai đại đô thị đặc biệt là cực tăng trưởng kinh tế quốc gia nhưng đang đối mặt thách thức nghiêm trọng của hiện tượng siêu tập trung.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "BENTO_MEGACITIES",
                "atoms": [
                    {
                        "title": "Quy Mô Dân Số Cực Lớn",
                        "text": "Dân số thực tế (tính cả người cư trú tạm thời) tại Hà Nội và TP.HCM đều vượt ngưỡng 9-10 triệu người.",
                        "icon": "users"
                    },
                    {
                        "title": "Đóng Góp Ngân Sách Vượt Trội",
                        "text": "Hai thành phố đóng góp gần 45% tổng thu ngân sách quốc gia và là trung tâm tài chính, thương mại, đại học hàng đầu.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "Ách Tắc Và Ngập Úng Đô Thị",
                        "text": "Kẹt xe, ngập úng mùa mưa, ô nhiễm bụi mịn PM2.5 và thiếu hụt không gian cây xanh công cộng làm suy giảm chất lượng sống.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Giải pháp căn cơ cho hai siêu đô thị là phát triển đường sắt đô thị (Metro) và giãn dân sang các đô thị vệ tinh.",
                "source_footer": "Quy hoạch Tổng thể Phát triển Hà Nội và TP.HCM",
                "illustration": "cinematic_bai_4_urban.jpg"
            },
            {
                "slide_id": "SLIDE_20",
                "role": "CONTENT",
                "section": "THÁCH THỨC ĐÔ THỊ",
                "assertion_title": "Các Thách Thức Đô Thị Hóa: Áp Lực Nhà Ở, Giao Thông Và Môi Trường Sống",
                "primary_claim": "Sự gia tăng cơ học quá nhanh khiến hạ tầng dịch vụ xã hội luôn ở trong tình trạng rượt đuổi nhu cầu thực tế của người dân.",
                "visual_job": "CARDS",
                "visual_anchor": "THREE_URBAN_CHALLENGES",
                "atoms": [
                    {
                        "title": "Thiếu Hụt Nhà Ở Xã Hội",
                        "text": "Giá nhà ở thương mại vượt xa thu nhập thực tế của người lao động di cư; khan hiếm phân khúc nhà ở xã hội giá rẻ.",
                        "icon": "home"
                    },
                    {
                        "title": "Quá Tải Mạng Lưới Giao Thông",
                        "text": "Phương tiện cá nhân tăng nhanh chóng mặt trong khi tỷ lệ đất dành cho giao thông chỉ đạt dưới 15% (chuẩn là 20-25%).",
                        "icon": "navigation"
                    },
                    {
                        "title": "Ô Nhiễm Nước & Rác Thải Sinh Hoạt",
                        "text": "Hàng chục nghìn tấn rác thải mỗi ngày gây áp lực lên các bãi chôn lấp; nước thải sinh hoạt chưa qua xử lý làm ô nhiễm kênh rạch.",
                        "icon": "trash-2"
                    }
                ],
                "speaker_notes": "Phát triển đô thị bền vững đòi hỏi phải đặt môi trường sống và sức khỏe người dân làm trung tâm của mọi đồ án quy hoạch.",
                "source_footer": "Báo cáo Môi trường Quốc gia - Bộ Tài nguyên và Môi trường"
            },
            {
                "slide_id": "SLIDE_21",
                "role": "CONTENT",
                "section": "QUY HOẠCH ĐÔ THỊ VỆ TINH",
                "assertion_title": "Định Hướng Phát Triển Hệ Thống Đô Thị Xanh, Thông Minh Và Vệ Tinh",
                "primary_claim": "Xây dựng các đô thị vệ tinh độc lập có đầy đủ dịch vụ việc làm, trường học, bệnh viện để giảm tải cho vùng lõi trung tâm.",
                "visual_job": "PROCESS",
                "visual_anchor": "URBAN_SOLUTIONS",
                "atoms": [
                    {
                        "title": "1. Mô Hình Phát Triển TOD",
                        "text": "Phát triển đô thị định hướng giao thông công cộng (Transit-Oriented Development) quanh các nhà ga đường sắt đô thị.",
                        "icon": "navigation"
                    },
                    {
                        "title": "2. Chuỗi Đô Thị Vệ Tinh Sinh Thái",
                        "text": "Phát triển các chùm đô thị vệ tinh như Hòa Lạc, Sơn Tây (Hà Nội), Thủ Đức, Cần Giờ (TP.HCM) với môi trường xanh.",
                        "icon": "sun"
                    },
                    {
                        "title": "3. Chuyển Đổi Số Đô Thị Thông Minh",
                        "text": "Ứng dụng trí tuệ nhân tạo và IoT trong quản lý giao thông thông minh, điều hành chiếu sáng và quan trắc môi trường số.",
                        "icon": "cpu"
                    },
                    {
                        "title": "4. Phát Triển Nhà Ở Xã Hội Đạt Chuẩn",
                        "text": "Thực hiện đề án 1 triệu căn hộ nhà ở xã hội nhằm an cư lạc nghiệp cho công nhân khu công nghiệp và người có thu nhập thấp.",
                        "icon": "home"
                    }
                ],
                "speaker_notes": "Mô hình TOD và đô thị vệ tinh là kinh nghiệm thành công của Tokyo, Seoul mà Việt Nam đang tích cực triển khai.",
                "source_footer": "Chiến lược Phát triển Đô thị Quốc gia đến 2030"
            },
            {
                "slide_id": "SLIDE_22",
                "role": "CONTENT",
                "section": "TỔNG KẾT BÀI HỌC",
                "assertion_title": "Tổng Kết Chuyên Đề Và Câu Hỏi Thảo Luận Quy Hoạch Không Gian Dân Cư",
                "primary_claim": "Nắm vững lý luận phân bố dân số, động lực di dân và đề xuất giải pháp phát triển đô thị bền vững cho địa phương.",
                "visual_job": "CARDS",
                "visual_anchor": "SUMMARY_PRACTICE",
                "atoms": [
                    {
                        "title": "Câu Hỏi 1: Đo Lường Phân Bố",
                        "text": "Phân tích ý nghĩa của đường cong Lorenz trong đánh giá bất bình đẳng phân bố dân cư giữa các vùng kinh tế.",
                        "icon": "help-circle"
                    },
                    {
                        "title": "Câu Hỏi 2: Lực Đẩy - Lực Kéo",
                        "text": "Vận dụng lý thuyết lực đẩy - lực kéo của Everett Lee để giải thích làn sóng di dân lao động vào vùng Đông Nam Bộ.",
                        "icon": "help-circle"
                    },
                    {
                        "title": "Tình Huống 3: Quy Hoạch Đô Thị",
                        "text": "Để giải quyết ách tắc giao thông tại Hà Nội hoặc TP.HCM, anh/chị ưu tiên mở rộng đường xá hay phát triển đô thị vệ tinh? Vì sao?",
                        "icon": "message-square"
                    }
                ],
                "speaker_notes": "Học viên hoàn thành thảo luận nhóm theo các chủ đề trên. Xin cảm ơn quý học viên đã theo dõi chuyên đề.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
            }
        ]
    }


def get_lesson_blueprints_bai_5() -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "lesson_index": 5,
        "deck_title": "Dự Báo Dân Số: Phương Pháp Luận Và Ứng Dụng",
        "total_slides": 20,
        "visual_system": "MODERN_REFINED",
        "slides": [
            {
                "slide_id": "SLIDE_01",
                "role": "COVER",
                "section": "TỔNG QUAN CHUYÊN ĐỀ",
                "assertion_title": "BÀI 5: DỰ BÁO DÂN SỐ: PHƯƠNG PHÁP LUẬN VÀ ỨNG DỤNG",
                "primary_claim": "Phương pháp luận khoa học, kỹ thuật mô hình hóa thành phần nhân khẩu và ứng dụng dự báo dân số trong hoạch định tương lai.",
                "visual_job": "HERO_TITLE",
                "visual_anchor": "BRAND_COVER",
                "speaker_notes": "Kính chào quý học viên, Bài 5 là chuyên đề tổng hợp quan trọng: làm chủ kỹ thuật dự báo dân số tương lai phục vụ hoạch định chính sách.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia",
                "illustration": "illustration_bai_5.jpg"
            },
            {
                "slide_id": "SLIDE_02",
                "role": "CONTENT",
                "section": "MỤC TIÊU BÀI HỌC",
                "assertion_title": "Năng Lực Xây Dựng Giả Thiết Và Mô Hình Dự Báo Dân Số Khoa Học",
                "primary_claim": "Trang bị phương pháp ngoại suy toán học, phương pháp thành phần nhân khẩu và phân tích các kịch bản dân số Việt Nam.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_OBJECTIVES",
                "atoms": [
                    {
                        "title": "Làm Chủ Các Phương Pháp Dự Báo",
                        "text": "Nắm vững kỹ thuật ngoại suy hàm số toán học và phương pháp thành phần nhân khẩu (Cohort Component Method).",
                        "icon": "calculator"
                    },
                    {
                        "title": "Kỹ Năng Xây Dựng Giả Thiết",
                        "text": "Xây dựng các giả thiết khoa học về mức sinh, mức chết và di cư cho các kịch bản dự báo thấp, trung bình và cao.",
                        "icon": "sliders"
                    },
                    {
                        "title": "Ứng Dụng Hoạch Định Chính Sách",
                        "text": "Vận dụng kết quả dự báo dân số để tính toán nhu cầu trường học, bệnh viện, quỹ hưu trí và định hướng chiến lược đến 2045.",
                        "icon": "target"
                    }
                ],
                "speaker_notes": "Chuẩn đầu ra yêu cầu học viên hiểu sâu bản chất các giả thiết nhân khẩu để không coi dự báo là phép bói toán số học.",
                "source_footer": "Khung chuẩn đầu ra chuyên đề"
            },
            {
                "slide_id": "SLIDE_03",
                "role": "CONTENT",
                "section": "Ý NGHĨA DỰ BÁO",
                "assertion_title": "Khái Niệm, Mục Đích Và Ý Nghĩa Sống Còn Của Dự Báo Dân Số",
                "primary_claim": "Dự báo dân số là cơ sở khoa học đầu tiên để lập quy hoạch phát triển kinh tế - xã hội, bảo đảm cung cấp dịch vụ công.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Khái Niệm Dự Báo Dân Số",
                        "text": "Tính toán quy mô và cơ cấu dân số trong tương lai dựa trên dữ liệu hiện tại và các giả thiết khoa học về sinh, tử, di cư.",
                        "icon": "search"
                    },
                    {
                        "title": "Mục Tiêu Quy Hoạch Xã Hội",
                        "text": "Xác định trước nhu cầu về số lượng giáo viên, số giường bệnh, diện tích nhà ở và cân đối quỹ bảo hiểm xã hội tương lai.",
                        "icon": "check-circle"
                    }
                ],
                "speaker_notes": "Một kế hoạch phát triển kinh tế nếu không dựa trên số liệu dự báo dân số chắc chắn sẽ bị phá sản trong thực tế.",
                "source_footer": "Giáo trình Dự báo nhân khẩu học",
                "illustration": "cinematic_bai_5_forecast.jpg"
            },
            {
                "slide_id": "SLIDE_04",
                "role": "CONTENT",
                "section": "PHÂN LOẠI DỰ BÁO",
                "assertion_title": "Phân Loại Dự Báo Dân Số Theo Tầm Thời Gian Và Phạm Vi Lãnh Thổ",
                "primary_claim": "Thời gian dự báo càng dài thì độ bất định càng lớn, đòi hỏi phải thường xuyên hiệu chỉnh giả thiết định kỳ.",
                "visual_job": "CARDS",
                "visual_anchor": "FORECAST_HORIZONS",
                "atoms": [
                    {
                        "title": "Dự Báo Ngắn Hạn (< 5 Năm)",
                        "text": "Độ chính xác rất cao vì cơ cấu tuổi đã định hình sẵn; phục vụ lập kế hoạch ngân sách và phân bổ chỉ tiêu hàng năm.",
                        "icon": "clock"
                    },
                    {
                        "title": "Dự Báo Trung Hạn (5 - 15 Năm)",
                        "text": "Phục vụ các kế hoạch phát triển kinh tế - xã hội 5 năm, 10 năm của quốc gia và các quy hoạch phát triển ngành.",
                        "icon": "calendar"
                    },
                    {
                        "title": "Dự Báo Dài Hạn (15 - 50 Năm)",
                        "text": "Định hướng chiến lược an ninh lương thực, ứng phó già hóa, quỹ bảo hiểm hưu trí và tầm nhìn phát triển thế kỷ.",
                        "icon": "compass"
                    }
                ],
                "speaker_notes": "Dự báo dài hạn thường đưa ra dưới dạng dải kịch bản (Thấp - Trung bình - Cao) thay vì một con số duy nhất.",
                "source_footer": "Phương pháp luận dự báo kinh tế xã hội"
            },
            {
                "slide_id": "SLIDE_05",
                "role": "CONTENT",
                "section": "NGOẠI SUY TOÁN HỌC",
                "assertion_title": "Các Phương Pháp Ngoại Suy Toán Học Tuyến Tính Và Đa Thức",
                "primary_claim": "Sử dụng các hàm số toán học theo chuỗi thời gian để ngoại suy quy mô tổng thể nhanh chóng cho các địa bàn nhỏ.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Mô Hình Tuyến Tính (Linear Model)",
                        "text": "P_t = P_0 + b*t. Giả định dân số gia tăng một lượng tuyệt đối không đổi hàng năm. Chỉ phù hợp trong thời gian rất ngắn.",
                        "icon": "activity"
                    },
                    {
                        "title": "Mô Hình Hình Học (Geometric Model)",
                        "text": "P_t = P_0 * (1 + r)^t. Giả định dân số tăng theo tỷ lệ phần trăm cố định mỗi năm (lãi kép gián đoạn).",
                        "icon": "trending-up"
                    },
                    {
                        "title": "Ưu Nhược Điểm Cơ Bản",
                        "text": "Dễ tính toán chỉ cần số liệu 2 kỳ; nhưng nhược điểm lớn là không thể bóc tách cơ cấu tuổi và giới tính.",
                        "icon": "alert-circle"
                    }
                ],
                "speaker_notes": "Ngoại suy toán học đơn giản thường được cấp huyện/xã dùng để ước tính nhanh quy mô tổng số.",
                "source_footer": "Giáo trình Toán nhân khẩu học",
                "formula": "P_t = P_0 * (1 + r*t)  |  P_t = P_0 * (1 + r)^t  (Ngoại suy ngắn hạn)"
            },
            {
                "slide_id": "SLIDE_06",
                "role": "CONTENT",
                "section": "HÀM SỐ LOGISTIC",
                "assertion_title": "Mô Hình Tăng Trưởng Hàm Số Mũ Và Hàm Số Logistic Giới Hạn Dung Nạp",
                "primary_claim": "Dân số không thể tăng trưởng hàm mũ vô tận mà sẽ tiệm cận ngưỡng sức chịu tải cực đại của môi trường sinh thái.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Hàm Mũ Không Giới Hạn (Malthus)",
                        "text": "P_t = P_0 * e^(rt). Quy mô bùng nổ theo cấp số nhân; bỏ qua giới hạn về tài nguyên đất đai, nguồn nước và lương thực.",
                        "icon": "maximize"
                    },
                    {
                        "title": "Mô Hình Logistic (Verhulst Model)",
                        "text": "P_t = K / [1 + a*e^(-rt)]. Với K là ngưỡng dung nạp tối đa (Carrying Capacity). Đồ thị dạng chữ S uốn lượn ổn định ở mức K.",
                        "icon": "shield"
                    }
                ],
                "speaker_notes": "Mô hình Logistic phản ánh đúng quy luật sinh học khi quần thể đạt đến ngưỡng giới hạn tài nguyên môi trường.",
                "source_footer": "Mô hình sinh thái nhân học Verhulst",
                "chart_type": "POPULATION_FORECAST_SCENARIOS"
            },
            {
                "slide_id": "SLIDE_07",
                "role": "CONTENT",
                "section": "PHƯƠNG PHÁP THÀNH PHẦN",
                "assertion_title": "Phương Pháp Thành Phần Nhân Khẩu (Cohort-Component Method) Chuẩn Mực",
                "primary_claim": "Phương pháp dự báo chuẩn mực quốc tế của Liên Hợp Quốc mô phỏng chi tiết sự chuyển dịch từng thế hệ theo từng năm.",
                "visual_job": "FORMULA_CARD",
                "visual_anchor": "BENTO_COHORT",
                "atoms": [
                    {
                        "title": "Nguyên Lý Lõi Của Phương Pháp",
                        "text": "Dự báo độc lập từng thành phần nhân khẩu: tính số sống sót theo bảng sống, tính số sinh qua ASFR và tính di cư ròng theo tuổi.",
                        "icon": "layers"
                    },
                    {
                        "title": "Cung Cấp Chi Tiết Tuổi & Giới Tính",
                        "text": "Cho ra kết quả tháp dân số chi tiết từng độ tuổi cho từng năm tương lai, phục vụ trực tiếp cho quy hoạch chuyên ngành.",
                        "icon": "users"
                    },
                    {
                        "title": "Tiêu Chuẩn Của Liên Hợp Quốc",
                        "text": "Được tất cả các cơ quan thống kê quốc gia và tổ chức quốc tế sử dụng để dự báo dân số toàn cầu.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Phương pháp thành phần là 'tiêu chuẩn vàng' trong mọi nghiên cứu dự báo dân số hiện đại.",
                "source_footer": "Cẩm nang Dự báo Dân số của Liên Hợp Quốc (Manual X)",
                "formula": "P_(x+n, t+n) = P_(x,t) * S_(x,x+n) + NetMig_(x,x+n)  (Tiêu chuẩn UN)"
            },
            {
                "slide_id": "SLIDE_08",
                "role": "CONTENT",
                "section": "BỐN BƯỚC MÔ HÌNH",
                "assertion_title": "Bốn Bước Vận Hành Mô Hình Thành Phần: Dịch Chuyển Từng Nhóm Tuổi",
                "primary_claim": "Chu trình tính toán tuần tự từ dân số gốc, nhân xác suất sống sót, cộng số trẻ sinh mới và điều chỉnh di cư thuần.",
                "visual_job": "PROCESS",
                "visual_anchor": "FOUR_COHORT_STEPS",
                "atoms": [
                    {
                        "title": "1. Dịch Chuyển Tuổi & Tử Vong",
                        "text": "Dân số tuổi x năm nay sẽ sống sót lên tuổi x+1 vào năm sau bằng cách nhân với tỷ lệ sống sót từ bảng sống: P_(x+1, t+1) = P_(x,t) * S_x.",
                        "icon": "arrow-up"
                    },
                    {
                        "title": "2. Dự Báo Số Trẻ Sinh Mới",
                        "text": "Nhân số phụ nữ từng độ tuổi sinh sản với tỷ suất sinh đặc trưng tương ứng: B = Σ(W_x * ASFR_x). Tách bé trai và bé gái theo SRB.",
                        "icon": "plus"
                    },
                    {
                        "title": "3. Đưa Trẻ Mới Sinh Vào Đáy Tháp",
                        "text": "Nhân tổng số sinh với xác suất sống sót từ 0 đến 1 tuổi (S_0) để tạo thành nhóm 0 tuổi trong năm kế tiếp: P_(0, t+1) = B * S_0.",
                        "icon": "database"
                    },
                    {
                        "title": "4. Hiệu Chỉnh Di Cư Thuần",
                        "text": "Cộng hoặc trừ số di cư thuần theo từng độ tuổi và giới tính vào quy mô từng nhóm tuổi tương ứng.",
                        "icon": "shuffle"
                    }
                ],
                "speaker_notes": "Chu trình 4 bước này lặp lại liên tục cho từng năm dự báo trong suốt thời kỳ nghiên cứu.",
                "source_footer": "Quy trình tính toán Cohort Component"
            },
            {
                "slide_id": "SLIDE_09",
                "role": "CONTENT",
                "section": "DÂN SỐ GỐC",
                "assertion_title": "Xây Dựng Bộ Dữ Liệu Dân Số Gốc (Base Population) Và Hiệu Chỉnh Sai Số",
                "primary_claim": "Chất lượng bộ dữ liệu dân số ban đầu quyết định trực tiếp độ chính xác của toàn bộ chuỗi số liệu dự báo tương lai.",
                "visual_job": "CARDS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Nguồn Số Liệu Tổng Điều Tra",
                        "text": "Lấy từ kết quả Tổng điều tra dân số mới nhất. Cần hiệu chỉnh tỷ lệ sót dân và sai số khai báo tuổi (hiện tượng làm tròn tuổi).",
                        "icon": "database"
                    },
                    {
                        "title": "Chuyển Đổi Về Thời Điểm Chuẩn",
                        "text": "Đưa thời điểm kiểm kê (ngày 1/4) về thời điểm giữa năm (1/7) để thuận tiện cho việc ghép nối với số liệu thống kê kinh tế.",
                        "icon": "calendar"
                    },
                    {
                        "title": "San Bằng Đường Cong Tuổi",
                        "text": "Áp dụng các thuật toán Sprague hoặc Beers để làm mịn đường cong cơ cấu tuổi, loại trừ các đỉnh nhọn nhân tạo.",
                        "icon": "sliders"
                    }
                ],
                "speaker_notes": "Nguyên tắc 'rác vào thì rác ra' (GIGO) đặc biệt đúng với kỹ thuật dự báo dân số; chuẩn hóa dữ liệu gốc là khâu quyết định.",
                "source_footer": "Kỹ thuật hiệu chỉnh số liệu điều tra dân số"
            },
            {
                "slide_id": "SLIDE_10",
                "role": "CONTENT",
                "section": "GIẢ THIẾT MỨC SINH",
                "assertion_title": "Thiết Lập Các Giả Thiết Về Mức Sinh Cho Các Kịch Bản Dự Báo",
                "primary_claim": "Mức sinh là biến số nhạy cảm và khó dự đoán nhất, đòi hỏi xây dựng 3 kịch bản: Thấp, Trung bình và Cao.",
                "visual_job": "COMPARISON",
                "visual_anchor": "FERTILITY_SCENARIOS",
                "atoms": [
                    {
                        "title": "Kịch Bản Mức Sinh Thấp",
                        "text": "Giả định mức sinh tiếp tục giảm sâu theo xu hướng của Đông Á, TFR giảm về mức 1.5 con/phụ nữ vào năm 2035.",
                        "icon": "trending-down"
                    },
                    {
                        "title": "Kịch Bản Trung Bình (Khả Dĩ Nhất)",
                        "text": "Giả định chính sách hỗ trợ phát huy hiệu quả, Việt Nam giữ vững mức sinh thay thế TFR quanh ngưỡng 2.0 - 2.1 con.",
                        "icon": "minus"
                    },
                    {
                        "title": "Kịch Bản Mức Sinh Cao",
                        "text": "Giả định kinh tế tăng trưởng vượt bậc, an sinh xã hội hoàn thiện thúc đẩy TFR tăng nhẹ lên mức 2.2 con.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Kịch bản trung bình luôn được chọn làm phương án cơ sở để các bộ ngành xây dựng quy hoạch phát triển.",
                "source_footer": "Báo cáo Giả thiết Dự báo Dân số Việt Nam 2019-2069"
            },
            {
                "slide_id": "SLIDE_11",
                "role": "CONTENT",
                "section": "GIẢ THIẾT MỨC CHẾT",
                "assertion_title": "Thiết Lập Các Giả Thiết Về Mức Chết Và Xu Hướng Tăng Kỳ Vọng Sống",
                "primary_claim": "Mức chết biến động theo xu hướng tương đối ổn định với kỳ vọng sống khi sinh tiếp tục tăng dần đều.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Mô Hình Giảm Tử Vong Lee-Carter",
                        "text": "Ứng dụng mô hình toán Lee-Carter để ngoại suy xu hướng giảm tỷ suất chết theo tuổi dựa trên chuỗi số liệu lịch sử.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Tăng Kỳ Vọng Sống Của Việt Nam",
                        "text": "Dự báo tuổi thọ bình quân của Việt Nam tăng từ 73.7 tuổi hiện nay lên mức 76.5 tuổi vào năm 2039 và 78.5 tuổi vào 2069.",
                        "icon": "heart"
                    },
                    {
                        "title": "Thu Hẹp Khoảng Cách Giới",
                        "text": "Khoảng cách tuổi thọ giữa nữ và nam thu hẹp nhẹ từ 5.4 năm xuống khoảng 4.5 năm nhờ y tế nam khoa và giảm tai nạn.",
                        "icon": "users"
                    }
                ],
                "speaker_notes": "Xu hướng tăng tuổi thọ là chắc chắn, đặt ra yêu cầu cấp thiết về tái thiết kế hệ thống lương hưu.",
                "source_footer": "Mô hình Lee-Carter trong dự báo mức chết",
                "chart_type": "MATH_MODELS"
            },
            {
                "slide_id": "SLIDE_12",
                "role": "CONTENT",
                "section": "GIẢ THIẾT DI CƯ",
                "assertion_title": "Thiết Lập Các Giả Thiết Về Xu Hướng Di Cư Thuần Nội Địa Và Quốc Tế",
                "primary_claim": "Di cư chịu chi phối mạnh mẽ của tốc độ đầu tư công nghiệp và các hiệp định thương mại tự do.",
                "visual_job": "CARDS",
                "visual_anchor": "SECTION_CARDS",
                "atoms": [
                    {
                        "title": "Di Cư Thuần Quốc Tế",
                        "text": "Quy ước mức di cư thuần quốc tế âm nhẹ (khoảng -50,000 người/năm) do số lượng đi lao động và định cư ở nước ngoài.",
                        "icon": "plane"
                    },
                    {
                        "title": "Di Cư Nội Địa Giữa Các Tỉnh",
                        "text": "Xu hướng dòng di cư tiếp tục đổ về Đông Nam Bộ và Đồng bằng sông Hồng nhưng tốc độ có xu hướng chậm lại do lan tỏa khu công nghiệp.",
                        "icon": "shuffle"
                    },
                    {
                        "title": "Tác Động Của Biến Đổi Khí Hậu",
                        "text": "Tình trạng xâm nhập mặn và sạt lở tại Đồng bằng sông Cửu Long có thể tạo ra làn sóng di cư khí hậu mới về các đô thị lớn.",
                        "icon": "alert-triangle"
                    }
                ],
                "speaker_notes": "Dự báo di cư ở cấp tỉnh phức tạp hơn nhiều so với cấp quốc gia vì phụ thuộc trực tiếp vào các dự án FDI.",
                "source_footer": "Dự báo di cư trong quy hoạch tổng thể quốc gia"
            },
            {
                "slide_id": "SLIDE_13",
                "role": "CONTENT",
                "section": "ỨNG DỤNG TĐT 2019",
                "assertion_title": "Ứng Dụng Phương Pháp Thành Phần Trong Dự Báo Dân Số Việt Nam 2019 - 2069",
                "primary_claim": "Tổng cục Thống kê phối hợp với Quỹ Dân số Liên Hợp Quốc (UNFPA) xây dựng bộ dự báo chuẩn quốc gia cho 50 năm.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_CENSUS_PROJECTION",
                "atoms": [
                    {
                        "title": "Dân Số Gốc Chuẩn Hóa 2019",
                        "text": "Tổng số 96,208,984 người tại thời điểm 0h ngày 1/4/2019, được chia chi tiết theo 63 tỉnh thành và từng nhóm tuổi đơn lẻ.",
                        "icon": "database"
                    },
                    {
                        "title": "Công Cụ Phần Mềm Quốc Tế",
                        "text": "Sử dụng bộ phần mềm Spectrum (DemProj) và R chuyên dụng để tính toán chuyển dịch nhân khẩu học đồng bộ.",
                        "icon": "cpu"
                    },
                    {
                        "title": "Bàn Giao Cho Các Bộ Ngành",
                        "text": "Bộ số liệu được chuyển giao chính thức cho Bộ Kế hoạch & Đầu tư, Bộ GD&ĐT, Bộ Y tế để làm cơ sở quy hoạch ngành.",
                        "icon": "award"
                    }
                ],
                "speaker_notes": "Đây là ấn phẩm dự báo có quy mô lớn nhất và phương pháp luận chặt chẽ nhất trong lịch sử thống kê Việt Nam.",
                "source_footer": "Ấn phẩm Dự báo Dân số Việt Nam giai đoạn 2019-2069 (GSO & UNFPA)"
            },
            {
                "slide_id": "SLIDE_14",
                "role": "CONTENT",
                "section": "BA KỊCH BẢN QUY MÔ",
                "assertion_title": "Ba Kịch Bản Dự Báo Quy Mô Dân Số Việt Nam: Thấp, Trung Bình Và Cao",
                "primary_claim": "Dân số Việt Nam được dự báo sẽ vượt ngưỡng 105 triệu vào năm 2030 và đạt đỉnh trong khoảng thời gian từ 2045 đến 2055.",
                "visual_job": "DATA_TABLE",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "MATH_MODELS",
                "atoms": [
                    {
                        "title": "Kịch Bản Thấp: Đạt Đỉnh 107 Triệu",
                        "text": "Nếu mức sinh giảm sâu như Hàn Quốc, dân số sẽ đạt đỉnh vào năm 2044 với 107 triệu dân rồi giảm nhanh xuống 95 triệu vào 2069.",
                        "icon": "trending-down"
                    },
                    {
                        "title": "Kịch Bản Trung Bình: Đỉnh 117 Triệu",
                        "text": "Kịch bản chuẩn: dân số đạt đỉnh vào năm 2054 với 117.7 triệu dân, sau đó giảm nhẹ và duy trì ổn định quanh 110 triệu.",
                        "icon": "check"
                    },
                    {
                        "title": "Kịch Bản Cao: Tăng Đến 125 Triệu",
                        "text": "Nếu mức sinh hồi phục trên mức thay thế, quy mô dân số sẽ duy trì đà tăng trưởng và đạt 125 triệu người vào năm 2069.",
                        "icon": "trending-up"
                    }
                ],
                "speaker_notes": "Cả 3 kịch bản đều thống nhất một điểm mốc: Dân số Việt Nam chắc chắn sẽ đạt đỉnh trong thế kỷ 21 này.",
                "source_footer": "Dự báo Dân số Việt Nam 2019-2069 - Tổng cục Thống kê",
                "table_data": {
                    "headers": [
                        "Kịch Bản Dự Báo",
                        "Giả Thiết Mức Sinh (TFR)",
                        "Dân Số Năm 2030",
                        "Quy Mô Đỉnh Dân Số",
                        "Thời Điểm Đạt Đỉnh"
                    ],
                    "rows": [
                        [
                            "Kịch Bản Thấp",
                            "TFR giảm nhanh về 1.60 con/phụ nữ",
                            "102.5 Triệu",
                            "104.2 Triệu",
                            "Năm 2044 (Đạt đỉnh sớm)"
                        ],
                        [
                            "Kịch Bản Trung Bình",
                            "Duy trì ổn định TFR ≈ 2.05 con/phụ nữ",
                            "104.5 Triệu",
                            "107.0 Triệu",
                            "Năm 2055 (Khả dĩ nhất)"
                        ],
                        [
                            "Kịch Bản Cao",
                            "TFR phục hồi đạt 2.25 con/phụ nữ",
                            "106.8 Triệu",
                            "112.5 Triệu",
                            "Sau năm 2065 (Tăng dài)"
                        ]
                    ],
                    "col_widths": [
                        0.22,
                        0.28,
                        0.16,
                        0.16,
                        0.18
                    ]
                }
            },
            {
                "slide_id": "SLIDE_15",
                "role": "CONTENT",
                "section": "THỜI ĐIỂM ĐẠT ĐỈNH",
                "assertion_title": "Thời Điểm Dân Số Đạt Đỉnh (Peak Population) Và Giai Đoạn Thu Hẹp Quy Mô",
                "primary_claim": "Sau khi chạm đỉnh cực đại vào khoảng năm 2054, Việt Nam sẽ bước vào giai đoạn giảm dân số tự nhiên lịch sử.",
                "visual_job": "BENTO_GRID",
                "visual_anchor": "BENTO_PEAK",
                "atoms": [
                    {
                        "title": "Hiện Tượng Số Chết Vượt Số Sinh",
                        "text": "Từ sau năm 2054, số người cao tuổi tử vong mỗi năm sẽ vượt quá số trẻ sơ sinh chào đời, dẫn tới mức tăng tự nhiên âm (NIR < 0).",
                        "icon": "alert-triangle"
                    },
                    {
                        "title": "Thay Đổi Căn Bản Mô Hình Tăng Trưởng",
                        "text": "Kinh tế không thể tiếp tục dựa vào việc mở rộng thâm dụng lao động mà bắt buộc phải chuyển sang tăng trưởng dựa vào đổi mới sáng tạo.",
                        "icon": "zap"
                    },
                    {
                        "title": "Chuẩn Bị Sớm Từ Hôm Nay",
                        "text": "Khoảng đệm 30 năm (từ 2024 đến 2054) là cơ hội vàng duy nhất để đất nước tích lũy của cải trước khi dân số bắt đầu suy giảm.",
                        "icon": "clock"
                    }
                ],
                "speaker_notes": "Hiểu rõ thời điểm đạt đỉnh giúp hoạch định chính xác chu kỳ đầu tư công cho các công trình hạ tầng dài hạn.",
                "source_footer": "Nghiên cứu quá trình chuyển tiếp dân số Việt Nam"
            },
            {
                "slide_id": "SLIDE_16",
                "role": "CONTENT",
                "section": "DỰ BÁO CƠ CẤU TUỔI",
                "assertion_title": "Dự Báo Xu Hướng Biến Đổi Cơ Cấu Tuổi Và Tốc Độ Già Hóa Đến 2045",
                "primary_claim": "Tỷ lệ người cao tuổi từ 65 tuổi trở lên sẽ tăng gấp đôi từ 8.3% (2019) lên gần 18% vào năm 2045, biến Việt Nam thành xã hội rất già.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "CHART_INSIGHTS",
                "chart_type": "POPULATION_PYRAMID",
                "atoms": [
                    {
                        "title": "2019: 8.3% Người Cao Tuổi",
                        "text": "Toàn quốc có khoảng 8 triệu người từ 65 tuổi trở lên. Tỷ số phụ thuộc người già ADR mới ở mức xấp xỉ 12.2%.",
                        "icon": "circle"
                    },
                    {
                        "title": "2036: Chạm Ngưỡng Xã Hội Già (14%)",
                        "text": "Việt Nam chính thức trở thành quốc gia 'dân số già' theo phân loại của Liên Hợp Quốc với hơn 15 triệu người già.",
                        "icon": "alert-circle"
                    },
                    {
                        "title": "2045: 18.0% Người Cao Tuổi",
                        "text": "Cứ 5 người dân sẽ có 1 người cao tuổi; tỷ số phụ thuộc chung tăng vọt trở lại, chấm dứt cơ cấu dân số vàng khi quy mô lao động suy giảm.",
                        "icon": "shield-alert"
                    }
                ],
                "speaker_notes": "Sự thay đổi cơ cấu tuổi diễn ra với tốc độ rất nhanh, đòi hỏi tái cấu trúc toàn diện hệ thống an sinh xã hội.",
                "source_footer": "Báo cáo Già hóa Dân số Việt Nam - GSO & UNFPA"
            },
            {
                "slide_id": "SLIDE_17",
                "role": "CONTENT",
                "section": "KẾT THÚC DÂN SỐ VÀNG",
                "assertion_title": "Dự Báo Thu Hẹp Lực Lượng Lao Động Và Sự Kết Thúc Của Cơ Cấu Vàng",
                "primary_claim": "Thời kỳ cơ cấu dân số vàng dự kiến sẽ chính thức khép lại vào khoảng năm 2039 khi tỷ số phụ thuộc chung vượt ngưỡng 50%.",
                "visual_job": "CHART_AND_INSIGHTS",
                "visual_anchor": "TWO_PILLARS",
                "atoms": [
                    {
                        "title": "Quy Mô Lao Động Đạt Đỉnh (2035)",
                        "text": "Số người trong độ tuổi 15-64 sẽ đạt đỉnh khoảng 67.5 triệu người vào năm 2035, sau đó giảm dần đều cả về số lượng và tỷ trọng.",
                        "icon": "users"
                    },
                    {
                        "title": "Thiếu Hụt Lao Động Trẻ Tuổi",
                        "text": "Lực lượng lao động mới gia nhập (nhóm 15-24) suy giảm rõ rệt, buộc doanh nghiệp phải tự động hóa và tăng cường ứng dụng AI.",
                        "icon": "cpu"
                    }
                ],
                "speaker_notes": "Chúng ta chỉ còn khoảng 15 năm cơ cấu vàng nữa; từng năm trôi qua đều là thời gian vô giá không thể lãng phí.",
                "source_footer": "Dự báo Lực lượng Lao động Việt Nam - Bộ Lao động - Thương binh & Xã hội",
                "chart_type": "DEMOGRAPHIC_DIVIDEND_STACKED_AREA"
            },
            {
                "slide_id": "SLIDE_18",
                "role": "CONTENT",
                "section": "ỨNG DỤNG QUY HOẠCH",
                "assertion_title": "Ứng Dụng Kết Quả Dự Báo Trong Quy Hoạch Giáo Dục, Y Tế Và Quỹ Hưu Trí",
                "primary_claim": "Dự báo dân số là kim chỉ nam để phân bổ hàng triệu tỷ đồng vốn đầu tư công vào đúng các địa bàn và đối tượng thụ hưởng.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "POLICY_APPLICATIONS",
                "atoms": [
                    {
                        "title": "1. Tái Cấu Trúc Ngành Giáo Dục",
                        "text": "Quy mô học sinh tiểu học giảm dần do mức sinh giảm, chuyển nguồn lực từ xây thêm trường sang nâng cao chất lượng phòng học số.",
                        "icon": "book-open"
                    },
                    {
                        "title": "2. Chuyển Đổi Trọng Tâm Y Tế",
                        "text": "Mở rộng chuyên khoa lão khoa tại tất cả bệnh viện tỉnh, đào tạo bác sĩ gia đình và thành lập mạng lưới viện dưỡng lão.",
                        "icon": "heart"
                    },
                    {
                        "title": "3. Cân Đối Quỹ Bảo Hiểm Xã Hội",
                        "text": "Điều chỉnh tuổi nghỉ hưu theo lộ trình và đa dạng hóa danh mục đầu tư quỹ hưu trí để bảo đảm an toàn chi trả dài hạn.",
                        "icon": "dollar-sign"
                    },
                    {
                        "title": "4. Quy Hoạch Phát Triển Đô Thị",
                        "text": "Thiết kế không gian đô thị thân thiện với người cao tuổi: vỉa hè không bậc, giao thông công cộng dễ tiếp cận xe lăn.",
                        "icon": "home"
                    }
                ],
                "speaker_notes": "Dự báo dân số giúp nhà quản lý không bị bất ngờ trước các thay đổi nhu cầu xã hội trong tương lai.",
                "source_footer": "Quy hoạch phát triển kinh tế xã hội quốc gia",
                "illustration": "ai_bai_5_sustainability.jpg"
            },
            {
                "slide_id": "SLIDE_19",
                "role": "CONTENT",
                "section": "KHUYẾN NGHỊ 2045",
                "assertion_title": "Khuyến Nghị Chiến Lược Chủ Động Thích Ứng Cho Nhà Hoạch Định Đến 2045",
                "primary_claim": "Chủ động thích ứng với quá trình chuyển tiếp nhân khẩu học là chìa khóa để hiện thực hóa khát vọng Việt Nam thịnh vượng năm 2045.",
                "visual_job": "PROCESS",
                "visual_anchor": "STRATEGIC_RECOMMENDATIONS",
                "atoms": [
                    {
                        "title": "Nâng Cao Năng Suất Vượt Trội",
                        "text": "Lấy năng suất lao động và đổi mới sáng tạo làm động lực cốt lõi để bù đắp sự suy giảm số lượng lực lượng lao động tương lai.",
                        "icon": "zap"
                    },
                    {
                        "title": "Kích Hoạt Kinh Tế Bạc (Silver Economy)",
                        "text": "Biến già hóa từ gánh nặng thành cơ hội phát triển các ngành sản xuất thiết bị chăm sóc sức khỏe, bảo hiểm và du lịch nghỉ dưỡng.",
                        "icon": "award"
                    },
                    {
                        "title": "Duy Trì Mức Sinh Bền Vững",
                        "text": "Thực hiện đồng bộ các chính sách hỗ trợ tài chính, nhà ở và thai sản để các gia đình trẻ yên tâm sinh đủ hai con.",
                        "icon": "heart"
                    }
                ],
                "speaker_notes": "Tầm nhìn 2045 đòi hỏi sự chủ động ngay từ bây giờ, không chờ đến khi dân số già mới bắt đầu xây dựng chính sách.",
                "source_footer": "Tầm nhìn Phát triển Quốc gia đến năm 2045"
            },
            {
                "slide_id": "SLIDE_20",
                "role": "CONTENT",
                "section": "TỔNG KẾT BÀI HỌC",
                "assertion_title": "Tổng Kết Toàn Khóa Học Và Bài Tập Tình Huống Xây Dựng Kịch Bản Dự Báo",
                "primary_claim": "Làm chủ phương pháp dự báo thành phần nhân khẩu và hoàn thành bài tập lớn xây dựng kịch bản dân số địa phương.",
                "visual_job": "CARDS",
                "visual_anchor": "SUMMARY_PRACTICE",
                "atoms": [
                    {
                        "title": "Bài Tập 1: Ngoại Suy Hàm Số",
                        "text": "Dùng số liệu dân số tỉnh X năm 2014 (1.2 tr) và 2024 (1.4 tr), áp dụng mô hình hàm mũ để dự báo dân số năm 2034.",
                        "icon": "calculator"
                    },
                    {
                        "title": "Bài Tập 2: Xây Dựng Giả Thiết",
                        "text": "Hãy xây dựng 3 kịch bản mức sinh (TFR) cho địa phương anh/chị đến năm 2035 dựa trên các yếu tố kinh tế xã hội thực tế.",
                        "icon": "sliders"
                    },
                    {
                        "title": "Thảo Luận Cuối Khóa 3",
                        "text": "Đánh giá tác động của xu hướng già hóa dân số đến cân đối ngân sách chi trả an sinh xã hội tại địa phương đến năm 2045.",
                        "icon": "message-square"
                    }
                ],
                "speaker_notes": "Chúc mừng quý học viên đã hoàn thành toàn bộ chương trình đào tạo Dân số học chuyên sâu.",
                "source_footer": "Tài liệu đào tạo Dân số học chuẩn quốc gia"
            }
        ]
    }

