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
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 24.6-26.2с показал отдельный токен ' в' на 24.840, перед "ша" на 25.080)
# -- стандартный для кампании пропуск "в" перед "шапке"
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':24.84,'end':25.04}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
    if w['w'] == 'фипи':
        w['w'] = 'ФИПИ'
# "банке пи пи" -- тот же кампанейский паттерн разрыва "ФИПИ" на два токена
# "пи"; широкий передекод 2.8-5.2с подтвердил чистое "в банке ФИПИ по
# одному в день", склеено в одно слово
idx_pi1 = next(i for i,w in enumerate(w2) if w['w']=='пи' and abs(w['t']-3.484)<0.05)
idx_pi2 = idx_pi1 + 1
assert w2[idx_pi2]['w'] == 'пи'
w2 = replace_range(w2, idx_pi1, idx_pi2+1, [{'w':'ФИПИ','t':w2[idx_pi1]['t'],'end':w2[idx_pi2]['end']}])
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 21.1-22.7с показал отдельный токен ' в' на 21.420, перед "ша" на 21.580)
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':21.42,'end':21.54}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "каждую автобус" -- тот же паттерн, что в влад2110/video3: узкий сегмент
# смазал "пока жду" в несуществующее "каждую"; широкий передекод 0.0-1.8с
# дал чистое "пока жду автобус я по..." (продолжение "повторяю правители
# россии"), разбито на два реальных слова в границах исходного токена
idx_kzh = next(i for i,w in enumerate(w3) if w['w']=='каждую')
w3 = replace_range(w3, idx_kzh, idx_kzh+1, [
    {'w':'пока','t':0.412,'end':0.58},
    {'w':'жду','t':0.59,'end':0.712},
])
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 20.6-22.2с показал отдельный токен ' в' на 20.920, перед "ша" на 21.080)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':20.92,'end':21.04}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
