#!/usr/bin/env python3
import json
import sys

ep = sys.argv[1]
total_duration = float(sys.argv[2])

with open(f"ep{ep}_words.json", encoding="utf-8") as f:
    words = json.load(f)

# One word per group (CLAUDE.md §1.4): the running caption must stay short/
# compact on screen, not stretch wide with two-word merges.
groups = [{"text": w["text"].upper(), "start": w["start"]} for w in words]

for idx in range(len(groups)):
    groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
groups[0]["start"] = 0.0

with open(f"ep{ep}_running_caption.json", "w", encoding="utf-8") as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)

with open(f"ep{ep}_duration.json", "w", encoding="utf-8") as f:
    json.dump({"total_duration": total_duration}, f, indent=2)

print(f"EP{ep}: {len(groups)} caption groups, duration {total_duration}")
