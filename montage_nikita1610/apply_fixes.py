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
# CTA: "в" genuinely absent on redecode -> supply per invariant CTA formula
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':17.40,'end':17.52}])
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
# "заданием" -> "заданиям" (redecode confirms dative plural: "к заданиям есть")
idx = next(i for i,w in enumerate(w2) if w['w']=='заданием')
w2[idx]['w'] = 'заданиям'
# CTA: "шапте"/"профир" garbled -> "шапке"/"профиля"
idx = next(i for i,w in enumerate(w2) if w['w']=='шапте')
w2[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w2) if w['w']=='профир')
w2[idx]['w'] = 'профиля'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "пороним" -> "паронимы" (redecode: "порониям различаются в паре")
idx = next(i for i,w in enumerate(w3) if w['w']=='пороним')
w3[idx]['w'] = 'паронимы'
# "запомните" -> "запомнить" (redecode: "один без другого не запомнить")
idx = next(i for i,w in enumerate(w3) if w['w']=='запомните')
w3[idx]['w'] = 'запомнить'
# "паронямы" -> "паронимы"
idx = next(i for i,w in enumerate(w3) if w['w']=='паронямы')
w3[idx]['w'] = 'паронимы'
# "быстрый"+"раун" -> "в"+"быстрых"+"раундах" (wide redecode: "...парами в быстрых раундах ссылка...")
idx = next(i for i,w in enumerate(w3) if w['w']=='быстрый')
w3 = replace_range(w3, idx, idx+2, [
    {'w':'в','t':15.90,'end':16.14},
    {'w':'быстрых','t':16.26,'end':16.68},
    {'w':'раундах','t':16.74,'end':17.22},
])
# CTA: "обтепрофиль" -> "в"+"шапке"+"профиля" (redecode: "...тренажёр в шапке профиля")
idx = next(i for i,w in enumerate(w3) if w['w']=='обтепрофиль')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'в','t':18.84,'end':18.96},
    {'w':'шапке','t':19.00,'end':19.30},
    {'w':'профиля','t':19.32,'end':19.744},
])
save(3, w3)
print('video3 fixed:', len(w3), 'words')
