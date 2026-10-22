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
    if w['w'] == 'фипи':
        w['w'] = 'ФИПИ'
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 24.6-26.2с показал отдельный токен ' в' на 24.960, перед "ша" на 25.120)
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':24.96,'end':25.08}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "тапки" -- широкий передекод 24.3-25.9с дал чистое "в шапке
# профиля": "т" вместо "ш" -- та же акустическая ошибка модели, что
# в video2 вчерашнего батча сергей2110 этой же комнаты; "в" тоже
# отдельно присутствует (токен на 24.540, перед "ша" на 24.700)
idx = next(i for i,w in enumerate(w2) if w['w']=='тапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':24.54,'end':24.66}])
idx = next(i for i,w in enumerate(w2) if w['w']=='тапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "игры на запоминания" -- широкий передекод 16.0-17.6с подтвердил тот
# же результат (не узкий сегмент), значит это действительно сказанное
# слово (разговорная форма), не ошибка ASR -- оставлено как есть
# CTA: "в" действительно присутствует по передекоду (широкий передекод
# 21.6-23.3с показал отдельный токен ' в' на 22.000, перед "ша" на 22.200)
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':22.00,'end':22.16}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
