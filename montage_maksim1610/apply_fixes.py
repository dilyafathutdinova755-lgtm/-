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
# "бан"+"фипи" -> "банк"+"ФИПИ" (redecode confirms: "в ЕГЭ тренажёре есть банк ФИПИ")
idx = next(i for i,w in enumerate(w1) if w['w']=='бан')
w1 = replace_range(w1, idx, idx+2, [
    {'w':'банк','t':w1[idx]['t'],'end':w1[idx]['end']},
    {'w':'ФИПИ','t':w1[idx+1]['t'],'end':w1[idx+1]['end']},
])
# CTA: "в" genuinely absent even on wide redecode -> supply per invariant CTA formula
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':20.45,'end':20.57}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: redecode confirms "в" present at ~23.28-23.44 (VAD-dropped short word, recovered)
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':23.28,'end':23.44}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: redecode confirms "в" present at ~22.98-23.14 (VAD-dropped short word, recovered)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':22.98,'end':23.14}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
