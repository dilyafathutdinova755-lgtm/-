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
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
for w in w2:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# CTA: "в" genuinely present per redecode (wide redecode showed ' в' at 26.400,
# distinct token before "ша" at 26.600) but VAD/tokenizer dropped it as a
# separate word; "шапки" -> "шапке" (same recurring issue as maksim1710)
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':26.400,'end':26.560}])
idx = next(i for i,w in enumerate(w2) if w['w']=='шапки')
w2[idx]['w'] = 'шапке'
save(2, w2)
print('video2 fixed:', len(w2), 'words')

# ---- video3 ----
w3 = load(3)
for w in w3:
    if w['w'] == 'егэ':
        w['w'] = 'ЕГЭ'
# "да"+"ты" (9.02-9.12 / 9.14-9.28, gap 0.02s -- identical to normal intra-word
# token spacing in this model) -> merge to "даты": "да ты там надо ставить по
# порядку" is not grammatical, but "даты там надо ставить по порядку" matches
# the invariant topic phrase ("даты смуты" at 1.116, "где даты смуты надо
# расставить по порядку" at 20.892) -- same construction, reconstructed per §ASR
# convention (acoustically ambiguous split reconstructed from invariant phrase).
idx_da = next(i for i,w in enumerate(w3) if w['w']=='да' and abs(w['t']-9.02)<0.05)
idx_ty = idx_da + 1
assert w3[idx_ty]['w'] == 'ты'
w3 = replace_range(w3, idx_da, idx_ty+1, [{'w':'даты','t':w3[idx_da]['t'],'end':w3[idx_ty]['end']}])
# CTA: "в" genuinely present per redecode (wide redecode showed ' в' at 27.280)
# but tokenizer dropped it; "шапки" -> "шапке"
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':27.280,'end':27.440}])
idx = next(i for i,w in enumerate(w3) if w['w']=='шапки')
w3[idx]['w'] = 'шапке'
save(3, w3)
print('video3 fixed:', len(w3), 'words')
