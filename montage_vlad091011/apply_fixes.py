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
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':18.140,'end':18.260}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
w1[-1]['end'] = min(w1[-1]['end'], 19.080)
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'профили':
        w['w'] = 'профиля'
w2[-1]['end'] = min(w2[-1]['end'], 21.804)
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'отечественные':
        w['w'] = 'отечественной'
w3[-1]['end'] = min(w3[-1]['end'], 19.970)
save(3, w3)
print('video3 fixed:', len(w3), 'words')
