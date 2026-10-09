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
assert w1[idx+1]['w'] == 'пи'
w1 = replace_range(w1, idx, idx+2, [{'w':'ФИПИ','t':w1[idx]['t'],'end':w1[idx+1]['end']}])
idx = next(i for i,w in enumerate(w1) if w['w']=='тренажёр' and w['t'] > 19)
w1[idx]['end'] = min(w1[idx]['end'], 20.420)
idx = next(i for i,w in enumerate(w1) if w['w']=='шапке')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':20.440,'end':20.600}])
w1[-1]['end'] = min(w1[-1]['end'], 21.400)
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
w2[-1]['end'] = min(w2[-1]['end'], 22.920)
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='тренажёр' and w['t'] > 21)
w3[idx]['end'] = min(w3[idx]['end'], 22.220)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапке')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':22.240,'end':22.400}])
w3[-1]['end'] = min(w3[-1]['end'], 23.255)
save(3, w3)
print('video3 fixed:', len(w3), 'words')
