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
# 26.4-28.0с показал отдельный токен ' в' на 26.640, перед "ша" на 26.800)
# -- стандартный для кампании пропуск "в" перед "шапке"
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':26.64,'end':26.76}])
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
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 24.5-26.1с показал отдельный токен ' в' на 24.780, перед "ша" на 24.980)
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':24.78,'end':24.94}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "каждую автобус или лифт" -- широкий передекод 2.8-5.5с дал чистое "учу
# пока жду автобус или лифт": несуществующее "каждую" не согласуется
# грамматически ("учу каждую автобус" -- разнородный род), тогда как "пока
# жду автобус или лифт" (жду -- в автобусной очереди/лифте) грамматически
# и по смыслу совпадает с остальным текстом про игру в паузах между делами;
# разбито на два реальных слова в границах исходного токена
idx_kzh = next(i for i,w in enumerate(w3) if w['w']=='каждую')
w3 = replace_range(w3, idx_kzh, idx_kzh+1, [
    {'w':'пока','t':3.452,'end':3.64},
    {'w':'жду','t':3.65,'end':3.832},
])
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 22.5-24.1с показал отдельный токен ' в' на 22.740, перед "ша" на 22.940)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':22.74,'end':22.90}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
