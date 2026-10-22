# -*- coding: utf-8 -*-
import importlib

for i in ["1", "2", "3"]:
    d = importlib.import_module(f"data{i}")
    importlib.reload(d)
    errs = []
    # hook closes before/at first card start
    if d.HOOK["end"] > d.CARDS[0][0] + 1e-6:
        errs.append(f"hook end {d.HOOK['end']} > first card start {d.CARDS[0][0]}")
    # cards sequential, no overlap, duration <=4.01
    for k, (st, en, lines) in enumerate(d.CARDS):
        if en - st > 4.01:
            errs.append(f"card {k} too long: {en-st:.2f}s")
        if en <= st:
            errs.append(f"card {k} non-positive duration")
        if k > 0 and st < d.CARDS[k-1][1] - 1e-6:
            errs.append(f"card {k} overlaps card {k-1}")
    # last card ends exactly at DURATION
    if abs(d.CARDS[-1][1] - d.DURATION) > 1e-6:
        errs.append(f"last card ends {d.CARDS[-1][1]} != DURATION {d.DURATION}")
    # emphasis windows: no overlap (need return to 1.0 between), within duration
    ems = sorted(d.EMPHASIS)
    for k in range(len(ems)-1):
        if ems[k][1] >= ems[k+1][0]:
            errs.append(f"emphasis {k} overlaps emphasis {k+1}")
    for k, (a, b) in enumerate(ems):
        if b > d.DURATION:
            errs.append(f"emphasis {k} end {b} > DURATION {d.DURATION}")
        if b <= a:
            errs.append(f"emphasis {k} non-positive duration")
    status = "OK" if not errs else "FAIL"
    print(f"video{i}: {status}  ({len(d.CARDS)} cards, {len(d.EMPHASIS)} zoom windows)")
    for e in errs:
        print("  -", e)
