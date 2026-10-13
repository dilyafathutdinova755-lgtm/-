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
    elif w['w'] == 'фипи':
        w['w'] = 'ФИПИ'
idx = next(i for i,w in enumerate(w1) if w['w']=='тренажёр' and w1[i]['t'] > 19)
w1[idx]['end'] = min(w1[idx]['end'], 20.780)
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':20.800,'end':20.880}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w1) if w['w']=='профи')
w1[idx]['w'] = 'профиля'
w1[-1]['end'] = min(w1[-1]['end'], 21.570)
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'здания':
        w['w'] = 'задания'
    elif w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'двига':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'заданием':
        w['w'] = 'заданиям'
    elif w['w'] == 'шапки':
        w['w'] = 'шапке'
idx = next(i for i,w in enumerate(w2) if w['w']=='ступень')
w2[idx]['w'] = 'ступени'
idx = next(i for i,w in enumerate(w2) if w['w']=='что' and w2[i-1]['w']=='ступени')
w2 = replace_range(w2, idx, idx+1, [])
w2[-1]['end'] = min(w2[-1]['end'], 20.780)
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
idx = next(i for i,w in enumerate(w3) if w['w']=='по-русскому')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'по','t':2.492,'end':2.600},
    {'w':'русскому','t':2.640,'end':3.032},
])
for w in w3:
    if w['w'] == 'игра':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'ега':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'нимало':
        w['w'] = 'немало'
    elif w['w'] == 'запоминаниях':
        w['w'] = 'запоминание'
    elif w['w'] == 'шапки':
        w['w'] = 'шапке'
w3[-1]['end'] = min(w3[-1]['end'], 18.455)
save(3, w3)
print('video3 fixed:', len(w3), 'words')
