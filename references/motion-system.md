# Motion System

## Principle

Motion reveals structure and pacing. Static deck is source of truth; motion adds sequence without changing final meaning. Final deck remains click-controlled unless user explicitly requests timed playback and accepts a different release policy.

Motion input must carry a `STATIC_READY_FOR_MOTION` certificate whose `visual_assets_verified` summary metadata passes native visual coverage validation. `apply-motion.ps1` revalidates both certificate-summary metadata and raw receipt metadata against the exact static deck hash and rejects any mismatch. Sau PowerPoint save, script đọc lại certificate và chạy lại complete static validation trước khi giữ output; receipt/report/source drift trong cửa sổ COM làm output bị xóa.

## Grammar

| Intent | Native motion | Use |
|---|---|---|
| establish context | Fade | title, background, section marker |
| reveal flow | Wipe | process, roadmap, directional sequence |
| preserve continuity | Morph | same object truly moves/resizes between states |
| compare values | Grow/Wipe | bars, lines, bridge components |
| emphasize decision | Fade + subtle scale | one recommendation or ask |

Dùng 3–7 narrative beats mỗi slide. Group object chỉ khi cùng semantic timing. Duration thường 0.35–0.65 s; delay 0–0.25 s. Easing mượt. Effect count không phải quality metric; effect thừa là defect.

## Storyboard contract

Storyboard dùng `schema_version=1.0`, `replace_existing=true` và không có property ngoài schema. Mỗi beat nêu exact shape names, effect, trigger, explicit duration, explicit delay và non-empty narrative purpose. Không dùng timing default. Transition thuộc `none`, `fade_smoothly`, `morph`. `click_controlled=true`, `auto_advance_allowed=false` là invariant.

## Order of operations

1. certify static content/layout/data/visual/render;
2. apply storyboard lên versioned copy;
3. inspect native timeline và transitions;
4. render final deck;
5. compare static frame với motion end-frame;
6. fresh-open và release-certify.

Không animate quanh static defect. Không dùng hidden animation che caveat, source, label hoặc material data. Không để transition imply causality không có trong nguồn.

## Morph safety

Dùng Morph chỉ khi object identity stable và continuity thật. Không dựa vào accidental name matching. Tránh Morph giữa unrelated charts, changed data hoặc missing objects. Nếu native result không chắc, dùng Fade/Wipe và ghi limitation.

## Click and timing safety

Set `AdvanceOnClick=true` và `AdvanceOnTime=false` trên mọi final slide. Audit `AdvanceTime`, trigger type, sequence order và shape existence. Auto-advance là P0 vì có thể skip material content.

## Preview review

Review first frame, từng click state và final frame ở full size. Montage chỉ dùng cho pacing. Test keyboard click progression và fresh PowerPoint open. End-frame pixel comparison phải đạt threshold khai báo; không thì `BLOCKED` hoặc `UNVERIFIED`.
