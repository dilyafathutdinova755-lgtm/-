# -*- coding: utf-8 -*-
"""Двухпроходный EBU R128 loudnorm (TP=-2.0 на обоих проходах, §4.5.1) + финальная проверка TP на AAC."""
import json, re, subprocess, sys

def measure(infile):
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", infile,
        "-af", "loudnorm=I=-14:TP=-2.0:LRA=11:print_format=json",
        "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\}\s*$", r.stderr, re.S)
    if not m:
        print(r.stderr[-3000:])
        raise RuntimeError("no loudnorm json found (pass1)")
    return json.loads(m.group(0))

def apply(infile, outfile, meas):
    af = (
        f"loudnorm=I=-14:TP=-2.0:LRA=11:"
        f"measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
        f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
        f"offset={meas['target_offset']}:linear=true:print_format=summary"
    )
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", infile,
        "-af", af, "-c:v", "copy", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", outfile,
    ]
    subprocess.run(cmd, check=True)

def verify_tp(outfile):
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", outfile,
        "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json",
        "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\}\s*$", r.stderr, re.S)
    if not m:
        print(r.stderr[-3000:])
        raise RuntimeError("no loudnorm json found (verify)")
    return json.loads(m.group(0))

if __name__ == "__main__":
    i = sys.argv[1]
    raw = f"out{i}_raw.mp4"
    final = f"final{i}.mp4"
    meas1 = measure(raw)
    print(f"[{i}] pass1 measured: I={meas1['input_i']} TP={meas1['input_tp']} LRA={meas1['input_lra']}")
    apply(raw, final, meas1)
    meas2 = verify_tp(final)
    print(f"[{i}] FINAL AAC check: I={meas2['input_i']} LUFS, TP={meas2['input_tp']} dBTP")
    ok = float(meas2['input_tp']) <= -1.0
    print(f"[{i}] TP<=-1.0dBTP: {'OK' if ok else 'FAIL -- NEEDS ATTENTION'}")
