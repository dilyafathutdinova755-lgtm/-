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
idx = next(i for i,w in enumerate(w1) if w['w']=='дождь')
w1[idx]['w'] = 'дольше'
idx = next(i for i,w in enumerate(w1) if w['w']=='решай')
w1[idx]['w'] = 'решаю'
idx = next(i for i,w in enumerate(w1) if w['w']=='то' and w1[i]['t'] > 10)
w1[idx]['w'] = 'что'
idx = next(i for i,w in enumerate(w1) if w['w']=='пи')
w1 = replace_range(w1, idx, idx+2, [{'w':'ФИПИ','t':w1[idx]['t'],'end':w1[idx+1]['end']}])
idx = next(i for i,w in enumerate(w1) if w['w']=='виде')
w1[idx]['w'] = 'где'
idx = next(i for i,w in enumerate(w1) if w['w']=='тренажёр' and w1[i]['t'] > 18)
w1[idx]['end'] = min(w1[idx]['end'], 19.120)
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':19.120,'end':19.132}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w1) if w['w']=='пофиля')
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
    elif w['w'] == 'шапте':
        w['w'] = 'шапке'
idx = next(i for i,w in enumerate(w2) if w['w']=='вкольном')
w2 = replace_range(w2, idx, idx+1, [
    {'w':'в','t':0.316,'end':0.396},
    {'w':'школьном','t':0.396,'end':0.616},
])
idx = next(i for i,w in enumerate(w2) if w['w']=='анис')
w2 = replace_range(w2, idx, idx+1, [
    {'w':'а','t':14.028,'end':14.200},
    {'w':'не','t':14.200,'end':14.360},
    {'w':'с','t':14.360,'end':14.568},
])
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='общесознанию')
w3[idx]['w'] = 'обществознанию'
idx = next(i for i,w in enumerate(w3) if w['w']=='г')
w3[idx]['w'] = 'ЕГЭ'
idx = next(i for i,w in enumerate(w3) if w['w']=='тренажори')
w3[idx]['w'] = 'тренажёре'
idx = next(i for i,w in enumerate(w3) if w['w']=='обе')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'в','t':22.420,'end':22.540},
    {'w':'шапке','t':22.580,'end':22.900},
    {'w':'профиля','t':22.940,'end':23.340},
])
save(3, w3)
print('video3 fixed:', len(w3), 'words')
