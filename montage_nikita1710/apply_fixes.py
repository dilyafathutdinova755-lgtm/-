import json

def load(i): return json.load(open(f'words{i}.json'))
def save(i, d): json.dump(d, open(f'words{i}.json', 'w'), ensure_ascii=False, indent=1)

def replace_range(words, start_idx, end_idx, new_words):
    return words[:start_idx] + new_words + words[end_idx:]

# ---- video1 ----
w1 = load(1)
for w in w1:
    if w['w'] == 'ега':
        w['w'] = 'ЕГЭ'
    elif w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "мотивация оказывается двойне" -> "...в дедлайне" (redecode: "мотивация оказывается в дедлайне")
idx = next(i for i,w in enumerate(w1) if w['w']=='двойне')
w1 = replace_range(w1, idx, idx+1, [
    {'w':'в','t':6.360,'end':6.520},
    {'w':'дедлайне','t':6.560,'end':7.176},
])
# "перед дедлайн ставлю сам" -> "теперь дедлайн ставлю сам" (redecode consistently: "теперь")
idx = next(i for i,w in enumerate(w1) if w['w']=='перед')
w1[idx]['w'] = 'теперь'
# "банк пи пипи" -> "банк фипи" (redecode narrow window: "банк(а) фипи", product name established across series)
idx = next(i for i,w in enumerate(w1) if w['w']=='банк')
w1 = replace_range(w1, idx, idx+3, [
    {'w':'банк','t':15.452,'end':15.752},
    {'w':'фипи','t':15.772,'end':16.232},
])
# CTA: "гриба" garbled filler with no resolvable lexical content on two independent
# redecodes ("перебата"/"перебатавший") -- dropped, not part of the invariant CTA phrase
idx = next(i for i,w in enumerate(w1) if w['w']=='гриба')
w1 = replace_range(w1, idx, idx+1, [])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапте')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "задания г" -> "задания ЕГЭ" (redecode: "...зада́ни[я е]гэ и нашёл", "г" was a truncated
# fragment of "ЕГЭ" merged with "задания", same garbled-letter pattern as vlad1510/video3)
idx = next(i for i,w in enumerate(w2) if w['w']=='г')
w2[idx]['w'] = 'ЕГЭ'
# "его тренажёре" -> "в ЕГЭ тренажёре" (redecode: "в ЕГЭ тренажёре", clean)
idx = next(i for i,w in enumerate(w2) if w['w']=='его')
w2 = replace_range(w2, idx, idx+1, [
    {'w':'в','t':13.900,'end':14.300},
    {'w':'ЕГЭ','t':14.300,'end':14.580},
])
# "соглавлением" -> "с" + "оглавлением" (redecode confirms "в разбор с оглавлением";
# ASR merged the short preposition into the following word, common pattern)
idx = next(i for i,w in enumerate(w2) if w['w']=='соглавлением')
w2 = replace_range(w2, idx, idx+1, [
    {'w':'с','t':17.500,'end':17.620},
    {'w':'оглавлением','t':17.640,'end':18.248},
])
# CTA: "в" genuinely present per redecode but VAD-dropped; "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':21.600,'end':21.720}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "тьего" -> "третьего" (truncated by VAD; wide redecode 14.4-18.0 confirms clean
# "...правления ивана третьего собираются в тройку", no extra words)
idx = next(i for i,w in enumerate(w3) if w['w']=='тьего')
w3[idx]['w'] = 'третьего'
# CTA: "в шапке" entirely missing between "тренажёр" and "профиль" (VAD gap) --
# redecode confirms full clean "ссылка на тренажёр в шапке профиля"
idx = next(i for i,w in enumerate(w3) if w['w']=='профиль')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'в','t':19.78,'end':19.90},
    {'w':'шапке','t':19.94,'end':20.26},
    {'w':'профиля','t':20.26,'end':20.704},
])
save(3, w3)
print('video3 fixed:', len(w3), 'words')
