# -*- coding: utf-8 -*-
"""Строит render{N}.sh: сегментированный эмфасис-зум + split-цепочка иконки + ass."""
import json, importlib
import pipeline as P

ICON = "/home/user/-/IMG_0884.png"

VIDEOS = {
    "1": "Untitled.Video.12.09.1_2160p.mp4",
    "2": "Untitled.Video.12.09.2_2160p.mp4",
    "3": "Untitled.Video.12.09.3_2160p.mp4",
}

for i, vfile in VIDEOS.items():
    data = importlib.import_module(f"data{i}")
    importlib.reload(data)
    words = json.load(open(f"words{i}.json"))
    dur = data.DURATION

    zoom_filter = P.zoom_segments_filter(data.EMPHASIS, dur)

    icon_windows = P.find_icon_windows(words, dur, hold=3.0, fade=0.32)
    icon_parts = []
    n = len(icon_windows)
    if n:
        icon_parts.append(
            "[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];"
        )
        icon_parts.append(f"[icraw]split={n}" + "".join(f"[ic{j}]" for j in range(n)) + ";")
        for j, (a, b) in enumerate(icon_windows):
            fin = f"fade=t=in:st={a}:d=0.32:alpha=1"
            if b < dur - 0.01:
                icon_parts.append(f"[ic{j}]{fin},fade=t=out:st={round(b-0.32,3)}:d=0.32:alpha=1[icf{j}];")
            else:
                icon_parts.append(f"[ic{j}]{fin}[icf{j}];")

    lines = [zoom_filter + ";"]
    lines += icon_parts
    lines.append(f"[base]ass=subs_s{i}.ass[subbed];")

    cur = "subbed"
    for j, (a, b) in enumerate(icon_windows):
        nxt = f"ovi{j}" if j < n - 1 else "ov"
        lines.append(f"[{cur}][icf{j}]overlay=x=746:y=430:enable='between(t,{a},{b})':shortest=1[{nxt}];")
        cur = nxt
    if not icon_windows:
        lines.append("[subbed]null[ov];")

    filter_complex = "\n".join(lines).rstrip(";\n")
    if filter_complex.endswith(";"):
        filter_complex = filter_complex[:-1]

    script = f"""set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "{vfile}" -i a{i}.m4a -i {ICON} -filter_complex "
{filter_complex}
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y
"""
    open(f"render{i}.sh", "w").write(script)
    print(f"render{i}.sh: {len(data.EMPHASIS)} zoom windows, {n} icon windows -> {icon_windows}")
