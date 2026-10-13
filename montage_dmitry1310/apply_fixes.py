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
    elif w['w'] == 'ега':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w1) if w['w']=='пи')
w1 = replace_range(w1, idx, idx+2, [{'w':'ФИПИ','t':w1[idx]['t'],'end':w1[idx+1]['end']}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапке')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':18.940,'end':19.020}])
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w2) if w['w']=='тренажёр' and w2[i]['t'] > 20)
w2[idx]['end'] = min(w2[idx]['end'], 21.950)
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':21.960,'end':22.080}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='по' and w3[i-1]['w']=='выбирать')
w3[idx]['end'] = min(w3[idx]['end'], 17.020)
w3 = replace_range(w3, idx+1, idx+1, [{'w':'признакам','t':17.040,'end':17.520}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':18.960,'end':19.080}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w3) if w['w']=='профиль')
w3[idx]['w'] = 'профиля'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
