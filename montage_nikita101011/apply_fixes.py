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
    elif w['w'] == 'дига':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'фипи':
        w['w'] = 'ФИПИ'
    elif w['w'] == 'профит':
        w['w'] = 'профиля'
w1[-1]['end'] = min(w1[-1]['end'], 20.204)
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'их':
        w['w'] = 'к'
    elif w['w'] == 'заданием':
        w['w'] = 'заданиям'
idx = next(i for i,w in enumerate(w2) if w['w']=='вокругление')
w2 = replace_range(w2, idx, idx+1, [
    {'w':'в','t':8.860,'end':8.920},
    {'w':'округлении','t':8.940,'end':9.512},
])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
w2[-1]['end'] = min(w2[-1]['end'], 21.100)
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
idx = next(i for i,w in enumerate(w3) if w['w']=='они')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'а','t':8.124,'end':8.164},
    {'w':'не','t':8.184,'end':8.224},
])
idx = next(i for i,w in enumerate(w3) if w['w']=='дефакторы')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'где','t':14.684,'end':14.860},
    {'w':'факторы','t':14.880,'end':15.144},
])
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='тренажёр' and w3[i]['t'] > 18)
w3[idx]['end'] = min(w3[idx]['end'], 19.220)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':19.240,'end':19.360}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w3) if w['w']=='профиль')
w3[idx]['w'] = 'профиля'
w3[-1]['end'] = min(w3[-1]['end'], 20.120)
save(3, w3)
print('video3 fixed:', len(w3), 'words')
