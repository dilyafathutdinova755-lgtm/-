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
# "банк пи пи с заданиями" -- широкий передекод 16.3-20.0с подтвердил "банк ФИПИ
# с заданиями по физике открыт без": VAD-сегмент обрезал начальный "ф" у "ФИПИ",
# из-за чего токенизатор разбил слово на два отдельных "пи"; склеено в одно слово
idx_pi1 = next(i for i,w in enumerate(w1) if w['w']=='пи' and abs(w['t']-17.676)<0.05)
idx_pi2 = idx_pi1 + 1
assert w1[idx_pi2]['w'] == 'пи'
w1 = replace_range(w1, idx_pi1, idx_pi2+1, [{'w':'ФИПИ','t':w1[idx_pi1]['t'],'end':w1[idx_pi2]['end']}])
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" действительно присутствует по передекоду (широкий передекод 22.9-24.6с
# показал отдельный токен ' в' на 23.260, перед "ша" на 23.460) -- тот же
# повторяющийся паттерн пропуска "в" перед "шапке" (§ASR-правки campaign-wide)
idx = next(i for i,w in enumerate(w2) if w['w']=='шапке')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':23.28,'end':23.44}])
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" действительно присутствует по передекоду (широкий передекод 20.7-22.3с
# показал отдельный токен ' в' на 21.100, перед "ша" на 21.260) -- тот же
# повторяющийся паттерн пропуска "в" перед "шапке"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапке')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':21.10,'end':21.24}])
save(3, w3)
print('video3 fixed:', len(w3), 'words')
