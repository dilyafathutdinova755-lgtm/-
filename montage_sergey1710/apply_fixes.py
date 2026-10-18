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
# "банк пи пи" -> "банк фипи" (redecode: "банк фипи", clean)
idx = next(i for i,w in enumerate(w1) if w['w']=='банк')
w1 = replace_range(w1, idx, idx+3, [
    {'w':'банк','t':10.66,'end':11.16},
    {'w':'фипи','t':11.18,'end':11.72},
])
# CTA: "в" present per redecode; "шапки"->"шапке"; "профиль"->"профиля" (invariant CTA formula)
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':16.90,'end':16.98}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w1) if w['w']=='профиль')
w1[idx]['w'] = 'профиля'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "после плохого телефону" -> "...к телефону" (redecode: "а после плохого к телефону", "к" dropped by VAD)
idx = next(i for i,w in enumerate(w2) if w['w']=='телефону')
w2 = replace_range(w2, idx, idx, [{'w':'к','t':5.40,'end':5.52}])
# CTA: "в" entirely dropped by VAD (invariant CTA formula); "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':16.52,'end':16.60}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "игры на запоминания" -> "...запоминание" (redecode confirms nominative, matches series terminology)
idx = next(i for i,w in enumerate(w3) if w['w']=='запоминания')
w3[idx]['w'] = 'запоминание'
# "ещё не задание задание" -- repeat confirmed genuine on redecode (deliberate rhetorical
# repeat before explaining the term, same pattern as vlad1710's "признаки признаки") -- left as spoken
# CTA: "в" entirely dropped by VAD; "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':19.60,'end':19.68}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
