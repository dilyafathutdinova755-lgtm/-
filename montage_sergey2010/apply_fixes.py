import json

def load(i): return json.load(open(f'words{i}.json'))
def save(i, d): json.dump(d, open(f'words{i}.json', 'w'), ensure_ascii=False, indent=1)

def replace_range(words, start_idx, end_idx, new_words):
    return words[:start_idx] + new_words + words[end_idx:]

# ---- video1 ----
w1 = load(1)
for w in w1:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# positional fix: "ега" (19.852-20.272, in "в ега тренажёре") is a garbled/slurred
# ЕГЭ mention, not a real word -- same pattern as sergey1410's "его"->"ЕГЭ" fix.
# Fixed by index, not blanket replace, since "ега" doesn't occur elsewhere.
idx = next(i for i,w in enumerate(w1) if w['w']=='ега')
w1[idx]['w'] = 'ЕГЭ'
# CTA: "в" genuinely present per redecode (wide redecode showed ' в' at 28.120)
# but tokenizer dropped it as separate word; "шапки" -> "шапке". Nudged start to
# 28.140 (vs raw redecode 28.120) to clear "тренажёр"'s own end at 28.136 in this
# pass's alignment -- the two ASR passes don't share identical word boundaries.
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':28.140,'end':28.280}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA already complete ("в шапке профиля" fully recognized) -- no insertion needed
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" genuinely present per redecode (wide redecode showed ' в' at 24.180)
# but tokenizer dropped it; "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':24.180,'end':24.340}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
