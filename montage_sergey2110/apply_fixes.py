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
# "банка пи пи" -- тот же паттерн кампании, что и в этой же комнате в
# сергей1710/video1: "ФИПИ" разбивается VAD/токенизатором на два отдельных
# "пи"; широкий передекод 20.8-22.3с подтвердил тот же разрыв ("банка пипи"),
# но по смыслу (банк заданий для подготовки) и прецеденту в этой комнате
# однозначно "банк ФИПИ" -- склеено в одно слово
idx_pi1 = next(i for i,w in enumerate(w1) if w['w']=='пи' and abs(w['t']-21.46)<0.05)
idx_pi2 = idx_pi1 + 1
assert w1[idx_pi2]['w'] == 'пи'
w1 = replace_range(w1, idx_pi1, idx_pi2+1, [{'w':'ФИПИ','t':w1[idx_pi1]['t'],'end':w1[idx_pi2]['end']}])
# CTA: "в" действительно присутствует по передекоду (25.0-26.8с показал
# отдельный токен ' в' на 25.520, перед "ша" на 25.720) -- стандартный для
# кампании пропуск "в" перед "шапке"
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':25.52,'end':25.68}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    if w['w'] == 'тренажоре':
        w['w'] = 'тренажёре'
# CTA: "тапки" -- широкий передекод 22.5-24.1с дал чистое "в шапке профиля":
# "т" вместо "ш" -- акустическая ошибка модели на этом конкретном дубле, не
# реальное слово; "в" тоже отдельно присутствует (токен на 22.900, перед
# "ша" на 23.100), тот же стандартный пропуск
idx = next(i for i,w in enumerate(w2) if w['w']=='тапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':22.90,'end':23.06}])
idx = next(i for i,w in enumerate(w2) if w['w']=='тапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" действительно присутствует по передекоду (21.0-22.5с показал
# отдельный токен ' в' на 21.320, перед "ша" на 21.480)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':21.32,'end':21.44}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
