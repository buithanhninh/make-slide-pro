import win32com.client
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ppt_path = os.path.abspath('Du_An_Outputs/Chuyên đề. Điều chỉnh mức sinh - Dark.pptx')
out_dir = os.path.abspath('C:/Users/HP/.gemini/antigravity/brain/a1c6c6ec-eb4c-4dbc-b9d2-b0f5fb78a606')

app = win32com.client.Dispatch('PowerPoint.Application')
pres = app.Presentations.Open(ppt_path, WithWindow=False)

sample_slides = [1, 10, 24, 52, 54, 57, 66, 70, 76, 80, 90]
for s_num in sample_slides:
    if 1 <= s_num <= pres.Slides.Count:
        slide = pres.Slides(s_num)
        out_png = os.path.join(out_dir, f'muc_sinh_v94_slide_{s_num:02d}.png')
        slide.Export(out_png, 'PNG', 1920, 1080)
        print(f'Exported slide {s_num} -> {out_png}')

pres.Close()
print('All verification slides exported successfully.')
