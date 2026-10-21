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
# "расставлять порядке" -- широкий передекод 15.0-16.8с дал чистое "нужно
# расставлять по порядку": токенизатор проглотил отдельное "по" и
# смазал падеж "порядку" в "порядке"; "по" вставлено, падеж исправлен
idx = next(i for i,w in enumerate(w1) if w['w']=='порядке')
w1 = replace_range(w1, idx, idx, [{'w':'по','t':16.044,'end':16.14}])
idx = next(i for i,w in enumerate(w1) if w['w']=='порядке')
w1[idx]['w'] = 'порядку'
w1[idx]['t'] = 16.15
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "почту" -- широкий передекод 3.0-5.5с дал чистое "вот что я делал каждый
# день": узкий VAD-сегмент смазал "вот что" в несуществующее "почту";
# разбито на два реальных слова в границах исходного токена
idx_pt = next(i for i,w in enumerate(w2) if w['w']=='почту')
w2 = replace_range(w2, idx_pt, idx_pt+1, [
    {'w':'вот','t':3.644,'end':3.78},
    {'w':'что','t':3.80,'end':3.984},
])
# "банк пи пи" -- тот же кампанейский паттерн разрыва "ФИПИ" на два токена
# "пи"; широкий передекод 17.3-19.5с подтвердил тот же разрыв ("банк пипи
# по истории в ЕГЭ"), склеено в "банк ФИПИ" по смыслу и прецеденту
idx_pi1 = next(i for i,w in enumerate(w2) if w['w']=='пи' and abs(w['t']-17.996)<0.05)
idx_pi2 = idx_pi1 + 1
assert w2[idx_pi2]['w'] == 'пи'
w2 = replace_range(w2, idx_pi1, idx_pi2+1, [{'w':'ФИПИ','t':w2[idx_pi1]['t'],'end':w2[idx_pi2]['end']}])
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 26.9-28.4с показал отдельный токен ' в' на 26.900, перед "ша" на 27.340)
# -- стандартный для кампании пропуск "в" перед "шапке"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':26.95,'end':27.26}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
