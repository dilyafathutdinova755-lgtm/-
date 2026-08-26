#!/usr/bin/env python3
import json

with open("words.json", encoding="utf-8") as f:
    words = json.load(f)

SRC_DURATION = 42.12

# (gap_index_after_word_text, trim_target)
cuts = [
    ("автоматически", 0.35),
    ("практика", 0.35),
    ("слух", 0.35),
    ("перечня", 0.35),
    ("егэ", 0.35),  # after "...соответствующему предмету егэ если" -> before "если"
    ("экзамене", 0.35),
    ("олимпиаде", 0.35),
    ("порог", 0.35),  # first "порог" (после "минимальный")... need index-based, see below
    ("задании", 0.40),
    ("источниках", 0.40),
    ("тренажер", 0.35),
]

# Resolve by explicit (start,end) pairs found manually from words.json instead of ambiguous text match.
cut_gaps = [
    (5.94, 6.75, 0.35),
    (8.13, 8.73, 0.35),
    (9.12, 9.84, 0.35),
    (12.96, 13.62, 0.35),
    (16.53, 17.16, 0.35),
    (20.52, 21.18, 0.35),
    (23.07, 23.85, 0.35),
    (25.77, 26.40, 0.35),
    (29.10, 30.00, 0.40),
    (35.61, 36.57, 0.40),
    (40.11, 40.83, 0.35),
]

PAD = 0.10
segments = []  # (old_start, old_end)
cursor = 0.0
for (t1, t2, trim) in cut_gaps:
    end_keep = t1 + PAD
    start_resume = end_keep + trim
    assert start_resume < t2, (t1, t2, trim, start_resume)
    segments.append((cursor, end_keep))
    cursor = start_resume
segments.append((cursor, SRC_DURATION))

zooms = [1.00, 1.10, 1.20, 1.08, 1.22, 1.14, 1.26, 1.10, 1.18, 1.06, 1.24, 1.14]
assert len(zooms) == len(segments)

# Build old->new time remap
new_segments = []
new_cursor = 0.0
for (os_, oe), z in zip(segments, zooms):
    dur = oe - os_
    new_segments.append({"old_start": round(os_, 3), "old_end": round(oe, 3),
                          "new_start": round(new_cursor, 3), "new_end": round(new_cursor + dur, 3),
                          "zoom": z})
    new_cursor += dur

total_new_duration = new_cursor
print(f"Segments: {len(new_segments)}  New total duration: {total_new_duration:.3f}s (was {SRC_DURATION}s)")
for s in new_segments:
    print(s)


def remap(t):
    for s in new_segments:
        if s["old_start"] - 1e-6 <= t <= s["old_end"] + 1e-6:
            return s["new_start"] + (t - s["old_start"])
    # in a cut gap -> clamp to nearest segment edge (shouldn't happen for word timestamps)
    for i, s in enumerate(new_segments):
        if t < s["old_start"]:
            return s["new_start"]
    return new_segments[-1]["new_end"]


new_words = []
for w in words:
    ns, ne = remap(w["start"]), remap(w["end"])
    if ne <= ns:
        ne = ns + 0.06
    new_words.append({"text": w["text"], "start": round(ns, 3), "end": round(ne, 3)})

with open("segments.json", "w", encoding="utf-8") as f:
    json.dump({"segments": new_segments, "total_duration": round(total_new_duration, 3)}, f, ensure_ascii=False, indent=2)

with open("words_remapped.json", "w", encoding="utf-8") as f:
    json.dump(new_words, f, ensure_ascii=False, indent=2)

print("\n--- remapped words ---")
for w in new_words:
    print(f"{w['start']:6.2f} - {w['end']:6.2f}  {w['text']}")
