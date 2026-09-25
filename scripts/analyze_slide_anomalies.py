import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('inspect_90_slides.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

img_slides = [s['slide_num'] for s in data if s['has_image']]
tbl_slides = [s['slide_num'] for s in data if s['has_table']]
chrt_slides = [s['slide_num'] for s in data if s['has_chart']]

print(f'Total slides: {len(data)}')
print(f'Slides with images ({len(img_slides)}): {img_slides}')
print(f'Slides with tables ({len(tbl_slides)}): {tbl_slides}')
print(f'Slides with charts ({len(chrt_slides)}): {chrt_slides}')

# Let's inspect each slide's exact kicker, assertion, and cards
for s in data:
    txts = s['texts']
    kicker = ""
    assertion = ""
    cards = []
    for t in txts:
        if "•" in t and ("TRỌNG TÂM" in t or "TỔNG QUAN" in t or "KẾT LUẬN" in t or "THỰC TRẠNG" in t):
            kicker = t
        elif "/ 90" in t:
            pass
        elif not assertion:
            assertion = t
        else:
            cards.append(t)
    s['kicker'] = kicker
    s['assertion'] = assertion
    s['card_texts'] = cards

print("\n--- DETAILED SLIDE INSPECTION ---")
for s in data:
    num = s['slide_num']
    k = s.get('kicker', '')[:30]
    a = s.get('assertion', '')[:50]
    cards = s.get('card_texts', [])
    c_summary = " // ".join([c.replace('\n', ' ')[:30] for c in cards[:4]])
    print(f"Slide {num:02d} | Kicker: {k} | Title: {a} | Cards({len(cards)}): {c_summary[:90]}")

# Repeated assertion titles
assertions = [s.get('assertion', '') for s in data]
c = Counter(assertions)
print("\n--- REPEATED TITLES ---")
for title, count in c.most_common(15):
    if count > 1:
        print(f"[{count} times] {title}")
