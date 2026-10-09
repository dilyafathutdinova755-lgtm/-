import json

def load(i): return json.load(open(f'words{i}.json'))
def save(i, d): json.dump(d, open(f'words{i}.json', 'w'), ensure_ascii=False, indent=1)

def replace_range(words, start_idx, end_idx, new_words):
    return words[:start_idx] + new_words + words[end_idx:]

# ---- video1 ----
w1 = load(1)
for w in w1:
    if w['w'] in ('егэ', 'ега'):
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'фипи':
        w['w'] = 'ФИПИ'
idx = next(i for i,w in enumerate(w1) if w['w']=='тренажёр' and w1[i]['t'] > 17)
w1[idx]['end'] = min(w1[idx]['end'], 18.680)
idx = next(i for i,w in enumerate(w1) if w['w']=='капки')
w1 = replace_range(w1, idx, idx+1, [
    {'w':'в','t':18.700,'end':18.830},
    {'w':'шапке','t':18.844,'end':19.064},
])
idx = next(i for i,w in enumerate(w1) if w['w']=='профи')
w1[idx]['w'] = 'профиля'
w1[-1]['end'] = min(w1[-1]['end'], 19.415)
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] in ('егэ', 'его'):
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'шапки':
        w['w'] = 'шапке'
    elif w['w'] == 'профиль':
        w['w'] = 'профиля'
w2[-1]['end'] = min(w2[-1]['end'], 18.135)
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
idx = next(i for i,w in enumerate(w3) if w['w']=='лига')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'для','t':1.884,'end':2.060},
    {'w':'ЕГЭ','t':2.080,'end':2.344},
])
idx = next(i for i,w in enumerate(w3) if w['w']=='по-русскому')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'по','t':2.364,'end':2.520},
    {'w':'русскому','t':2.560,'end':2.952},
])
idx = next(i for i,w in enumerate(w3) if w['w']=='экзамене')
w3 = replace_range(w3, idx+1, idx+1, [{'w':'нет','t':13.880,'end':14.150}])
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='тренажёр' and w3[i]['t'] > 22)
w3[idx]['end'] = min(w3[idx]['end'], 23.620)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':23.640,'end':23.760}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w3) if w['w']=='профиль')
w3[idx]['w'] = 'профиля'
w3[-1]['end'] = min(w3[-1]['end'], 24.535)
save(3, w3)
print('video3 fixed:', len(w3), 'words')
