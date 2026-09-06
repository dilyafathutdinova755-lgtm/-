#!/usr/bin/env python3
import json
import subprocess

with open("segments.json", encoding="utf-8") as f:
    plan = json.load(f)

segs = plan["segments"]
src = "/home/user/-/remotion/sources/IMG_3749.mp4"

filter_parts = []
concat_inputs = []
for i, s in enumerate(segs):
    a_label = f"a{i}"
    filter_parts.append(
        f"[0:a]atrim=start={s['old_start']}:end={s['old_end']},asetpts=PTS-STARTPTS[{a_label}]"
    )
    concat_inputs.append(f"[{a_label}]")

filter_complex = ";".join(filter_parts) + ";" + "".join(concat_inputs) + f"concat=n={len(segs)}:v=0:a=1[outa]"

cmd = [
    "ffmpeg", "-y", "-i", src,
    "-filter_complex", filter_complex,
    "-map", "[outa]",
    "/home/user/-/remotion/asr/audio_cut.wav",
]
print(" ".join(cmd))
subprocess.run(cmd, check=True)
