#!/usr/bin/env python3
import json
import sys

ep = sys.argv[1]
total_duration = float(sys.argv[2])

with open(f"ep{ep}_words.json", encoding="utf-8") as f:
    words = json.load(f)

GAP_THRESHOLD = 0.15
groups = []
i = 0
while i < len(words):
    chunk = [words[i]]
    if i + 1 < len(words) and words[i + 1]["start"] - words[i]["end"] < GAP_THRESHOLD:
        chunk.append(words[i + 1])
        i += 2
    else:
        i += 1
    groups.append({"text": " ".join(w["text"] for w in chunk).upper(), "start": chunk[0]["start"]})

for idx in range(len(groups)):
    groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
groups[0]["start"] = 0.0

with open(f"ep{ep}_running_caption.json", "w", encoding="utf-8") as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)

with open(f"ep{ep}_duration.json", "w", encoding="utf-8") as f:
    json.dump({"total_duration": total_duration}, f, indent=2)

print(f"EP{ep}: {len(groups)} caption groups, duration {total_duration}")
