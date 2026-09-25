# -*- coding: utf-8 -*-
import json, importlib
import pipeline as P

for i in ['1', '2', '3']:
    data = importlib.import_module(f"data{i}")
    importlib.reload(data)
    words = json.load(open(f"words{i}.json"))
    n = P.build_ass(f"subs_n2509_{i}.ass", data.CARDS, data.HOOK, words, data.DURATION)
    print(f"subs_n2509_{i}.ass: {n} card events")
