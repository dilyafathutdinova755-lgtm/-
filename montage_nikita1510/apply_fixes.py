import json

def load(i): return json.load(open(f'words{i}.json'))
def save(i, d): json.dump(d, open(f'words{i}.json', 'w'), ensure_ascii=False, indent=1)

def replace_range(words, start_idx, end_idx, new_words):
    return words[:start_idx] + new_words + words[end_idx:]

# ---- video1 ----
w1 = load(1)
idx = next(i for i,w in enumerate(w1) if w['w']=='игр')
w1[idx]['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w1) if w['w']=='мышек')
w1[idx]['w'] = 'мышке'
idx = next(i for i,w in enumerate(w1) if w['w']=='вига')
w1[idx]['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w1) if w['w']=='фипи')
w1[idx]['w'] = 'ФИПИ'
# irresolvable acoustic artifact ("свайфак") between "тренажёр" and "в шапке" —
# redecoded multiple times with different windows, consistently non-words;
# dropped, previous word's caption holds through the gap (run_events behavior)
idx = next(i for i,w in enumerate(w1) if w['w']=='с' and w['t'] > 20)
end_idx = next(i for i,w in enumerate(w1) if w['w']=='шапке')
w1 = replace_range(w1, idx, end_idx, [])
idx = next(i for i,w in enumerate(w1) if w['w']=='профиль')
w1[idx]['w'] = 'профиля'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'ега':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'заданием':
        w['w'] = 'заданиям'
idx = next(i for i,w in enumerate(w2) if w['w']=='заданиям')
w2 = replace_range(w2, idx, idx, [{'w':'к','t':12.94,'end':13.28}])
idx = next(i for i,w in enumerate(w2) if w['w']=='сука')
w2[idx]['w'] = 'ссылка'
idx = next(i for i,w in enumerate(w2) if w['w']=='мы')
w2[idx]['w'] = 'на'
idx = next(i for i,w in enumerate(w2) if w['w']=='тапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':18.60,'end':18.70}])
idx = next(i for i,w in enumerate(w2) if w['w']=='тапки')
w2[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w2) if w['w']=='профи')
w2[idx]['w'] = 'профиля'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
idx = next(i for i,w in enumerate(w3) if w['w']=='отца')
w3[idx]['w'] = '-ться'
idx = next(i for i,w in enumerate(w3) if w['w']=='ца')
w3[idx]['w'] = '-тся'
idx = next(i for i,w in enumerate(w3) if w['w']=='вига')
w3[idx]['w'] = 'ЕГЭ'
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
