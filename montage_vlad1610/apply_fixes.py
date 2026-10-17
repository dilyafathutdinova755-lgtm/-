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
# "банк пи пи" -> "банк фипи" (redecode: "есть банк фипи", one word not split)
idx = next(i for i,w in enumerate(w1) if w['w']=='банк')
w1 = replace_range(w1, idx, idx+3, [
    {'w':'банк','t':14.484,'end':14.824},
    {'w':'фипи','t':14.844,'end':15.304},
])
# CTA: "в" genuinely present per redecode but VAD-dropped; "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':21.02,'end':21.18}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
save(2, w2)
print('video2 fixed:', len(w2), 'words (only ЕГЭ case)')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "строго средняя свободна" -> "строго средне свободно" (adverbial triad,
# redecode at two different windows consistently returned -о/-е endings,
# grammatically coherent as "делю на строго/средне/свободно [управляемые]")
idx = next(i for i,w in enumerate(w3) if w['w']=='средняя')
w3[idx]['w'] = 'средне'
idx = next(i for i,w in enumerate(w3) if w['w']=='свободна')
w3[idx]['w'] = 'свободно'
# CTA: "в" genuinely present per redecode but VAD-dropped; "шапки"->"шапке"; "профиль"->"профиля"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':21.10,'end':21.26}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w3) if w['w']=='профиль')
w3[idx]['w'] = 'профиля'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
