# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

for name in [
    'Bài 3. Dịch vụ DS KHHGĐ.txt',
    'Bài 4. Dịch vụ CSSKSS vị thành niên-thanh niên.txt',
    'BÀI 5. DỊCH VỤ TƯ VẤN-TẦM SOÁT-CHẨN ĐOÁN MỘT SỐ BỆNH-TẬT TRƯỚC SINH VÀ SƠ SINH.txt',
    'BÀI 6. DỊCH VỤ CHĂM SÓC SỨC KHỎE NGƯỜI CAO TUỔI.txt'
]:
    p = Path('scripts/temp_lesson_text') / name
    if p.exists():
        lines = [line.strip() for line in p.read_text(encoding='utf-8').split('\n') if line.strip()]
        print(f"\n{'='*70}\nFILE: {name} ({len(lines)} lines)\n{'='*70}")
        # Print headings
        for l in lines:
            if any(l.startswith(pfx) for pfx in ['BÀI', 'Bài', 'MỤC TIÊU', '1.', '2.', '3.', '4.', '5.', '6.', '5.', 'CÂU HỎI']):
                if len(l) < 90:
                    print('  *', l)
