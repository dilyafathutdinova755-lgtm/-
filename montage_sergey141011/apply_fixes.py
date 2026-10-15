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
idx = next(i for i,w in enumerate(w1) if w['w']=='пи')
w1 = replace_range(w1, idx, idx+2, [{'w':'ФИПИ','t':w1[idx]['t'],'end':w1[idx+1]['end']}])
idx = next(i for i,w in enumerate(w1) if w['w']=='тренажёр' and w1[i]['t'] > 20)
w1[idx]['end'] = min(w1[idx]['end'], 20.940)
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':20.940,'end':21.060}])
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
    elif w['w'] == 'отмечен':
        w['w'] = 'отмечены'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='его' and i+1 < len(w3) and w3[i+1]['w']=='тренажёре')
w3[idx]['w'] = 'ЕГЭ'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
