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
# CTA ("в шапке профиля") recognized fully and cleanly -- no insertion needed
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "водка" (4.668-5.192) is a garbled "вот как" -- redecode (4.4-7.8с) gave clean
# ' вот'/' как' tokens at this exact position; same transition phrase as video1's
# "вот как" (5.404-5.896). Split into two words within the existing boundary.
idx = next(i for i,w in enumerate(w2) if w['w']=='водка')
w2 = replace_range(w2, idx, idx+1, [
    {'w':'вот','t':w2[idx]['t'],'end':4.900},
    {'w':'как','t':4.920,'end':w2[idx]['end']},
])
# "тотча" (5.692-5.952) is a garbled "дочь" -- not a real word, redecode context
# ("вот как ДОЧЬ сама исправляла слово") confirms; fixed by position.
idx = next(i for i,w in enumerate(w2) if w['w']=='тотча')
w2[idx]['w'] = 'дочь'
# CTA: "в" genuinely present per redecode (wide redecode showed ' в' at 21.380)
# but tokenizer dropped it as separate word; "шапки" -> "шапке". Nudged into the
# 21.384-21.500 gap between "тренажёр"'s end and "шапки"'s start in this pass's
# own alignment (the two ASR passes don't share identical word boundaries).
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':21.390,'end':21.480}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "водка" (5.212-5.608) -- same garbled "вот как" pattern as video2, redecode
# (4.9-6.1с) gave clean ' вот'/' как' tokens at this exact position.
idx = next(i for i,w in enumerate(w3) if w['w']=='водка')
w3 = replace_range(w3, idx, idx+1, [
    {'w':'вот','t':w3[idx]['t'],'end':5.420},
    {'w':'как','t':5.440,'end':w3[idx]['end']},
])
# CTA ("в шапке профиля") recognized fully and cleanly -- no insertion needed
save(3, w3)
print('video3 fixed:', len(w3), 'words')
