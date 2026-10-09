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
idx = next(i for i,w in enumerate(w1) if w['w']=='пи' and w1[i+1]['w']=='пи')
w1 = replace_range(w1, idx, idx+2, [{'w':'ФИПИ','t':w1[idx]['t'],'end':w1[idx+1]['end']}])
idx = next(i for i,w in enumerate(w1) if w['w']=='пипи')
w1[idx]['w'] = 'ФИПИ'
w1[-1]['end'] = min(w1[-1]['end'], 20.631)
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
w2[-1]['end'] = min(w2[-1]['end'], 21.911)
save(2, w2)
print('video2 fixed:', len(w2), 'words')
