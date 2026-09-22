# -*- coding: utf-8 -*-
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from make_slide_pro import process_single_document

input_file = PROJECT_ROOT / "Du An" / "A Tuan Dan So 2" / "BÀI 1. Tổng quan về dịch vụ dân số.docx"
output_dir = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2"

print(f"Starting test for: {input_file.name}")
t0 = time.time()
res = process_single_document(
    input_file=input_file,
    output_dir=output_dir,
    theme="DARK",
    motion_mode="presenter_click",
    run_qa=False,
    open_pptx=False,
    target_slides=50
)
elapsed = time.time() - t0
print(f"DONE in {elapsed:.1f}s: {res['document']} - Total slides: {res['total_slides']}")
