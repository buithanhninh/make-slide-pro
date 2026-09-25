import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('inspect_90_slides.json', 'r', encoding='utf-8') as f:
    slides = json.load(f)

print(f"Loaded {len(slides)} slides.")

# Find duplicate titles
title_map = {}
for s in slides:
    # get assertion
    txts = s.get('texts', [])
    ass = ""
    for t in txts:
        if "•" in t or "/ 90" in t: continue
        ass = t
        break
    s['ass_title'] = ass
    title_map.setdefault(ass, []).append(s['slide_num'])

dup_title_slides = {k: v for k, v in title_map.items() if len(v) > 1}

# Categorize defects per slide
slide_defects = {}
for s in slides:
    num = s['slide_num']
    defects = []
    texts = s.get('texts', [])
    all_text = " ".join(texts)
    
    # Check duplicate title
    ass = s.get('ass_title', '')
    if ass in dup_title_slides:
        defects.append(f"DUPLICATE_TITLE ({len(dup_title_slides[ass])}x: {dup_title_slides[ass]})")
        
    # Check placeholder Yếu tố 2
    if "Yếu Tố 2" in all_text or "Mô tả chi tiết" in all_text:
        defects.append("PLACEHOLDER_YEU_TO_2")
        
    # Check fake filler Khuyen Nghi Ap Dung
    if "Khuyến Nghị Áp Dụng" in all_text or "Vận dụng đồng bộ" in all_text:
        defects.append("FAKE_FILLER_KHUYEN_NGHI")
        
    # Check generic Muc Sinh & Xu Huong
    if "Mức Sinh & Xu Hướng" in all_text:
        defects.append("GENERIC_MUC_SINH_XU_HUONG")
        
    # Check isolated numbering
    import re
    if re.search(r"\b(4\.\d+\.\d+|3\.\d+\.\d+|1\.\d+\.\d+)\.\.\.", all_text) or any(t.strip() in ['3.2.', '4.1.3.', '4.1.5.', '4.1.6.', '4.2.1.', '4.2.2.', '4.2.4.'] for t in texts):
        defects.append("ISOLATED_HEADING_NUMBER")
        
    slide_defects[num] = defects

# Summary statistics
clean_slides = [num for num, d in slide_defects.items() if len(d) == 0]
defective_slides = [num for num, d in slide_defects.items() if len(d) > 0]

print(f"\nTotal slides: {len(slides)}")
print(f"Clean slides: {len(clean_slides)} -> {clean_slides}")
print(f"Defective slides: {len(defective_slides)} -> {defective_slides}")

# Defect frequency
all_d = []
for d in slide_defects.values():
    all_d.extend([x.split(' ')[0] for x in d])
print(f"\nDefect Frequency: {Counter(all_d)}")

# Print detailed per-slide report
print("\n--- DETAILED SLIDE-BY-SLIDE AUDIT REPORT ---")
for num in range(1, len(slides) + 1):
    d = slide_defects.get(num, [])
    ass = slides[num-1].get('ass_title', '')[:40]
    status = "PASS" if not d else f"FAIL: {', '.join(d)}"
    print(f"Slide {num:02d} | [{status}] | {ass}")
