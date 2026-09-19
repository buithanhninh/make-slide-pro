"""
export_showcase_png.py
Exports slides of the master showcase presentation to 1080p PNG images.
"""
import sys
from pathlib import Path
import win32com.client

def export_pngs():
    deck_path = Path(r"D:\Make Slide PPT\output\master_showcase\make_slide_pro_master_showcase.pptx").resolve()
    png_dir = Path(r"D:\Make Slide PPT\output\master_showcase\slides_png").resolve()
    png_dir.mkdir(parents=True, exist_ok=True)

    app = win32com.client.DispatchEx("PowerPoint.Application")
    app.Visible = True
    pres = None
    try:
        pres = app.Presentations.Open(str(deck_path), False, False, False)
        for i in range(1, pres.Slides.Count + 1):
            out_file = png_dir / f"slide_{i:02d}.png"
            pres.Slides(i).Export(str(out_file), "PNG", 1920, 1080)
            print(f"Exported slide_{i:02d}.png")
    finally:
        if pres:
            pres.Close()
        app.Quit()

if __name__ == "__main__":
    export_pngs()
