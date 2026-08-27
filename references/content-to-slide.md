# Content To Slide

## Canonicalization

Canonical content là semantic source of truth. Giữ nguyên câu chữ nguồn trong `verbatim`; đặt normalized wording, translation và display copy ở field riêng. Không thay fact bằng interpretation. Giữ qualifier đi kèm: period, unit, denominator, geography, audience, uncertainty, causality, attribution và condition.

## Atom contract

Mỗi atom cần stable `atom_id`, `type`, `source_id`, locator chính xác, verbatim value, normalized meaning, `priority` P0–P3, `confidence`, `must_preserve`, qualifiers, dependencies, destination và allowed transformations.

P0 là nội dung decision-critical, legally/materially sensitive hoặc numerically load-bearing. P1 là context/support quan trọng. P2/P3 chỉ được compress khi meaning còn nguyên.

## Reconciliation logic

Với mỗi metric, so tuple:

```text
(metric_key, period, unit, denominator, actual_or_forecast)
```

Sau đó so value, formula, source authority và locator. Percentage thiếu denominator là incomplete. Target không phải actual. CAGR, total, average hoặc derived ratio phải có formula inputs. Hai verified sources mâu thuẫn phải mang `CONFLICTED` và chặn release đến khi resolve.

## Coverage matrix

Mỗi atom một row:

```text
atom_id | priority | source_locator | canonical_text | destination
slide_ids | visible_copy | notes_copy | appendix_ref | transformation
approval | evidence_status | omission_reason
```

Không atom nào kết thúc ở unallocated state. `INTENTIONALLY_OMITTED` cần explicit approval và reason; P0/P1 omission chặn certification.

## Narrative construction

Tạo ít nhất ba candidate arcs:

1. **Decision-first** — recommendation, why now, evidence, choices, ask.
2. **Journey** — context, tension, insight, strategy, roadmap, operating model.
3. **Value-case** — opportunity, economics, capability gap, investment, return, risks.

Chấm candidate 0–100 theo audience relevance, evidence strength, decision clarity, flow, cognitive load và fidelity. Chọn phương án có score cao nhất có thể bảo vệ, không chọn phương án theatrical nhất. Ghi candidate bị loại và rationale.

Mỗi slide trả lời một câu hỏi. Title nêu answer/assertion, không chỉ nêu topic. Title-only test: chỉ đọc titles vẫn thấy lập luận coherent. Một primary claim và một primary role trên mỗi slide.

## Blueprint recipe

Mỗi slide gồm:

1. slide identity và section;
2. assertion title;
3. primary claim;
4. source atom IDs và primary evidence;
5. implication/decision relevance;
6. role và visual job;
7. một visual anchor;
8. data/chart/table spec nếu có;
9. image/icon IDs và provenance;
10. speaker notes và appendix refs;
11. transition và motion beats;
12. source footer/methodology treatment.

Blueprint validation chạy trước authoring. Slide thiếu source atoms hoặc meaningful visual anchor chưa sẵn sàng. Visual anchor có thể là chart, editable table, photo, product, illustration, diagram, map, screenshot hoặc metric composition; decorative background không được tính.

## Transformation rules

- Translate không đổi entity, tense, modality hoặc numeric meaning.
- Compress bằng bỏ repetition, không bỏ qualifier/caveat.
- Reorder chỉ khi question-answer logic tốt hơn và phải log.
- Derive chỉ khi có formula và source IDs.
- Visualize trend với axes, denominator và labels trung thực.
- Đẩy detail xuống notes/appendix khi density cao.
- Không dùng generated imagery để giả real event, person, product, UI, document, screenshot, chart hoặc market evidence.

## Copy and layout budget

Ưu tiên một sentence headline, một supporting proof, một implication. Body text chỉ giữ phần có evidence hoặc instruction. Nếu text không vừa, đổi hierarchy, wording hoặc layout; không giảm font dưới token minimum để nhét chữ.
