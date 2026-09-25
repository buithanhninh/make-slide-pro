import json
import sys
import os
import glob
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

folders = glob.glob('Du_An_Outputs/*Chuy*')
target_folder = [f for f in folders if os.path.isdir(f)][0]

with open(os.path.join(target_folder, 'canonical-content.json'), 'r', encoding='utf-8') as f:
    content = json.load(f)

with open(os.path.join(target_folder, 'slide-blueprints.json'), 'r', encoding='utf-8') as f:
    blueprint = json.load(f)

print(f"Content sections: {len(content.get('sections', []))}")
total_raw_atoms = sum(len(s.get('atoms', [])) for s in content.get('sections', []))
print(f"Total raw atoms in content: {total_raw_atoms}")
slides = blueprint.get('slides', [])
print(f"Blueprint slides: {len(slides)}")

archetypes = {}
repeated_titles = {}
generic_atoms_count = 0
generic_titles_found = []

for i, slide in enumerate(slides):
    sid = slide.get('slide_id', f'SLIDE_{i+1:02d}')
    role = slide.get('role', '')
    sec = slide.get('section', '')
    title = slide.get('assertion_title', '')
    vjob = slide.get('visual_job', '')
    atoms = slide.get('atoms', [])
    
    archetypes[vjob] = archetypes.get(vjob, 0) + 1
    repeated_titles[title] = repeated_titles.get(title, 0) + 1
    
    atom_summaries = []
    for a in atoms:
        at_title = a.get('title', '')
        at_text = a.get('text', '')
        if at_title in ['Mức Sinh & Xu Hướng', 'Khuyến Nghị Áp Dụng', 'Nội Dung Trọng Tâm', 'Yếu Tố 2', 'Luận Điểm Cốt Lõi', 'Cơ Chế & Quy Chuẩn Thực Thi', 'Ý Nghĩa & Mục Tiêu Đo Lường']:
            generic_atoms_count += 1
            generic_titles_found.append(at_title)
        atom_summaries.append(f"[{at_title}]: {at_text[:35]}...")
        
    print(f"{sid} | {vjob[:25]:<25} | Title: {title[:55]}")
    for a_sum in atom_summaries[:2]:
        print(f"     -> {a_sum}")

print("\n" + "="*80)
print(f"Total generic card titles found: {generic_atoms_count}")
print(f"Generic titles breakdown: {Counter(generic_titles_found)}")

print("\nArchetype Distribution:")
for arch, cnt in sorted(archetypes.items(), key=lambda x: x[1], reverse=True):
    print(f"  {arch:<35}: {cnt}")

print("\nMost Repeated Slide Titles:")
for t, cnt in sorted(repeated_titles.items(), key=lambda x: x[1], reverse=True):
    if cnt > 1:
        print(f"  [{cnt}x] {t}")
