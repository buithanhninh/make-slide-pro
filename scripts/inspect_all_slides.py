import win32com.client
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
ppt_path = os.path.abspath('Du_An_Outputs/Chuyên đề. Điều chỉnh mức sinh - Dark.pptx')
app = win32com.client.Dispatch('PowerPoint.Application')
pres = app.Presentations.Open(ppt_path, WithWindow=False)

print(f'Total slides: {pres.Slides.Count}')
slide_data = []

for i in range(1, pres.Slides.Count + 1):
    slide = pres.Slides(i)
    texts = []
    shape_names = []
    has_image = False
    has_table = False
    has_chart = False
    for s in slide.Shapes:
        shape_names.append(s.Name)
        if s.Type == 13: # msoPicture
            has_image = True
        elif s.HasTable:
            has_table = True
        elif s.HasChart:
            has_chart = True
        elif s.Type == 6: # group
            for sub in s.GroupItems:
                if sub.Type == 13:
                    has_image = True
                if sub.HasTextFrame and sub.TextFrame.HasText:
                    t = sub.TextFrame.TextRange.Text.strip()
                    if t: texts.append(t)
        if s.HasTextFrame and s.TextFrame.HasText:
            t = s.TextFrame.TextRange.Text.strip()
            if t: texts.append(t)
    
    slide_data.append({
        'slide_num': i,
        'shape_count': len(slide.Shapes),
        'shape_names': shape_names,
        'has_image': has_image,
        'has_table': has_table,
        'has_chart': has_chart,
        'texts': texts
    })

pres.Close()

with open('inspect_90_slides.json', 'w', encoding='utf-8') as f:
    json.dump(slide_data, f, ensure_ascii=False, indent=2)

print('Dumped inspect_90_slides.json successfully.')
for s in slide_data:
    first_few = " | ".join([t.replace('\n', ' ')[:40] for t in s['texts'][:3]])
    print(f"Slide {s['slide_num']:02d}: Shapes={s['shape_count']:2d}, Img={s['has_image']}, Tbl={s['has_table']}, Chrt={s['has_chart']} | {first_few[:100]}")
