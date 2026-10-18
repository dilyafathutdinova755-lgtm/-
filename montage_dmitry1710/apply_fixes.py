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
# CTA already recognized correctly by ASR first pass -- no fix needed
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" genuinely present per redecode but VAD-dropped; "шапки"->"шапке"; "профиль"->"профиля"
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':19.900,'end':20.020}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
idx = next(i for i,w in enumerate(w2) if w['w']=='профиль')
w2[idx]['w'] = 'профиля'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "повторяется раун" -> "повторяются раунды" (redecode confirms plural verb matching
# plural subject "принципы", and "раунды" not truncated "раун" -- two independent passes agree)
idx = next(i for i,w in enumerate(w3) if w['w']=='повторяется')
w3 = replace_range(w3, idx, idx+2, [
    {'w':'повторяются','t':19.06,'end':19.68},
    {'w':'раунды','t':19.70,'end':20.04},
])
# CTA: "в" inserted per invariant CTA formula (not resolved on redecode even at wider window,
# but the phrase is brand-locked per CLAUDE.md §1.7); "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':21.68,'end':21.76}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
