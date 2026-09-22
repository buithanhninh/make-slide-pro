# -*- coding: utf-8 -*-
"""
scripts/course2_curriculum_builder.py
Master Curriculum Blueprint Dispatcher for Du An/A Tuan Dan So 2 (Make Slide Pro V9.0).
Provides 100% authentic, high-quality, academic slides for all 6 core modules:
- Bai 1: Tổng quan về dịch vụ dân số (48 slides)
- Bai 2: Dịch vụ tư vấn, khám sức khỏe trước khi kết hôn (48 slides)
- Bai 3: Dịch vụ Kế hoạch hóa gia đình (50 slides)
- Bai 4: Dịch vụ chăm sóc SKSS vị thành niên - thanh niên (48 slides)
- Bai 5: Dịch vụ tư vấn, tầm soát, chẩn đoán trước sinh và sơ sinh (48 slides)
- Bai 6: Dịch vụ chăm sóc sức khỏe người cao tuổi tại cộng đồng (48 slides)
"""

from typing import Any, Dict, List, Optional
import unicodedata

try:
    from course2_data_bai1 import get_slides_bai_1
    from course2_data_bai2 import get_slides_bai_2
    from course2_data_bai3 import get_slides_bai_3
    from course2_data_bai4 import get_slides_bai_4
    from course2_data_bai5 import get_slides_bai_5
    from course2_data_bai6 import get_slides_bai_6
except ImportError:
    from scripts.course2_data_bai1 import get_slides_bai_1
    from scripts.course2_data_bai2 import get_slides_bai_2
    from scripts.course2_data_bai3 import get_slides_bai_3
    from scripts.course2_data_bai4 import get_slides_bai_4
    from scripts.course2_data_bai5 import get_slides_bai_5
    from scripts.course2_data_bai6 import get_slides_bai_6


def strip_accents(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def get_course2_blueprints(doc_name: str, target_slides: int = 0) -> Dict[str, Any]:
    """
    Returns authentic, rigorous Master Slide Blueprints for Course 2 (A Tuan Dan So 2).
    """
    clean_name = strip_accents(doc_name)
    
    if any(k in clean_name for k in ["bai 1", "tong quan"]):
        deck_title = "BÀI 1: TỔNG QUAN VỀ DỊCH VỤ DÂN SỐ"
        lesson_index = 1
        slides = get_slides_bai_1()
    elif any(k in clean_name for k in ["bai 2", "ket hon", "kham suc khoe"]):
        deck_title = "BÀI 2: DỊCH VỤ TƯ VẤN, KHÁM SỨC KHỎE TRƯỚC KHI KẾT HÔN"
        lesson_index = 2
        slides = get_slides_bai_2()
    elif any(k in clean_name for k in ["bai 3", "khhgd", "ke hoach hoa gia dinh"]):
        deck_title = "BÀI 3: DỊCH VỤ KẾ HOẠCH HÓA GIA ĐÌNH"
        lesson_index = 3
        slides = get_slides_bai_3()
    elif any(k in clean_name for k in ["bai 4", "vi thanh nien", "thanh nien", "csskss"]):
        deck_title = "BÀI 4: DỊCH VỤ CHĂM SÓC SỨC KHỎE SINH SẢN VỊ THÀNH NIÊN, THANH NIÊN"
        lesson_index = 4
        slides = get_slides_bai_4()
    elif any(k in clean_name for k in ["bai 5", "truoc sinh", "so sinh", "tam soat", "chan doan"]):
        deck_title = "BÀI 5: DỊCH VỤ TƯ VẤN, TẦM SOÁT, CHẨN ĐOÁN BỆNH TẬT TRƯỚC SINH VÀ SƠ SINH"
        lesson_index = 5
        slides = get_slides_bai_5()
    elif any(k in clean_name for k in ["bai 6", "cao tuoi", "nguoi cao tuoi"]):
        deck_title = "BÀI 6: DỊCH VỤ CHĂM SÓC SỨC KHỎE NGƯỜI CAO TUỔI TẠI CỘNG ĐỒNG"
        lesson_index = 6
        slides = get_slides_bai_6()
    else:
        # Fallback to Bài 1 if undetermined
        deck_title = f"CHUYÊN ĐỀ DỊCH VỤ DÂN SỐ: {doc_name}"
        lesson_index = 1
        slides = get_slides_bai_1()

    total_s = len(slides)
    for idx, s in enumerate(slides):
        s["slide_id"] = f"SLIDE_{idx+1:02d}"
        if idx == 0 or idx == total_s - 1:
            s["transition"] = "fade"
            s["transition_duration"] = 0.65
        else:
            s["transition"] = "morph"
            s["transition_duration"] = 0.85
            s["atomic_card"] = True
            s["safe_group"] = True

    return {
        "schema_version": "9.0.0",
        "version": "9.0.0",
        "v9_mode": True,
        "lesson_index": lesson_index,
        "deck_title": deck_title,
        "total_slides": len(slides),
        "visual_system": "MODERN_REFINED",
        "slides": slides
    }
