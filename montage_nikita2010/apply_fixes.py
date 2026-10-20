import json

def load(i): return json.load(open(f'words{i}.json'))
def save(i, d): json.dump(d, open(f'words{i}.json', 'w'), ensure_ascii=False, indent=1)

def replace_range(words, start_idx, end_idx, new_words):
    return words[:start_idx] + new_words + words[end_idx:]

# ---- video1 ----
w1 = load(1)
# "вегая" (2.148-2.528, in "по генетике ВЕГАЯ по биологии") is a slurred blend of
# "в"+"ЕГЭ" -- redecode (1.3-4.9с) gave clean separate ' в'(2.100)/'е'(2.220)/
# 'га'(2.300)/'я'(2.420) tokens, i.e. "в ЕГЭ" collapsed into one ASR word.
idx = next(i for i,w in enumerate(w1) if w['w']=='вегая')
w1 = replace_range(w1, idx, idx+1, [
    {'w':'в','t':w1[idx]['t'],'end':2.330},
    {'w':'ЕГЭ','t':2.330,'end':w1[idx]['end']},
])
# "бегая" (originally idx43, now +1) in "...сам [в] БЕГАЯ тренажёре" -- ASR fully
# dropped a separate "в" here; redecode (16.3-17.7с) confirmed ' сам'/' в'/' его'
# (same "его"-for-"ЕГЭ" garble as sergey1410/sergey2010 video1), i.e. "в ЕГЭ
# тренажёре" with "в" as its own word this time, not merged.
idx = next(i for i,w in enumerate(w1) if w['w']=='бегая')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':17.100,'end':17.260}])
idx = next(i for i,w in enumerate(w1) if w['w']=='бегая')
w1[idx]['w'] = 'ЕГЭ'
# "теннажёр" (24.62-25.096, in CTA) -- garbled "тренажёр", redecode confirmed
# consistently across two passes; not a real word, fixed by position.
idx = next(i for i,w in enumerate(w1) if w['w']=='теннажёр')
w1[idx]['w'] = 'тренажёр'
# CTA: "шапки" -> "шапке" + "в" inserted. Three independent redecode passes
# (narrow, wide, wider) all show a short blank/near-silent token immediately
# before "ша" rather than a clear letter -- same acoustic signature as the
# genuinely-present-but-reduced "в" found elsewhere in this campaign (maksim2010,
# sergey2010, dmitry2010), so treated the same way rather than left unfixed.
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1 = replace_range(w1, idx, idx, [{'w':'в','t':25.220,'end':25.260}])
idx = next(i for i,w in enumerate(w1) if w['w']=='шапки')
w1[idx]['w'] = 'шапке'
save(1, w1)
print('video1 fixed:', len(w1), 'words')

# ---- video2 ----
w2 = load(2)
# ASR produced an empty-text VAD segment between "химии"(idx10, ends 5.256) and
# "я"(was idx11, starts 7.164) -- redecode (5.0-6.2с) recovered it cleanly as
# "и в ЕГЭ", a whole phrase the original pass dropped entirely (not garbled,
# just missing). Inserted as three words.
idx = next(i for i,w in enumerate(w2) if w['w']=='химии') + 1
w2 = replace_range(w2, idx, idx, [
    {'w':'и','t':5.280,'end':5.480},
    {'w':'в','t':5.480,'end':5.640},
    {'w':'ЕГЭ','t':5.640,'end':5.900},
])
# "ега" (in "в ЕГА тренажёре") -- redecode (23.0-24.8с) gave "в его тренажёре":
# same "его"-for-"ЕГЭ" garble pattern as video1/video3 here and as precedent
# sergey1410/sergey2010; "в" already present and correct, fixed "ега" by position.
idx = next(i for i,w in enumerate(w2) if w['w']=='ега')
w2[idx]['w'] = 'ЕГЭ'
# CTA tail: "обе профиль" -- two wide redecodes (33.0-35.4с and 33.4-35.0с) both
# resolve this region as "шапки"/"шаптик"-ish tokens, not "обе"/"профиль"; no
# clean "в" token recovered in several attempts (same near-silent-token pattern
# as video1's CTA), so "в" inserted the same way. "обе"->"шапке", "профиль"
# (missing final -я) -> "профиля".
idx = next(i for i,w in enumerate(w2) if w['w']=='обе')
w2 = replace_range(w2, idx, idx, [{'w':'в','t':34.440,'end':34.480}])
idx = next(i for i,w in enumerate(w2) if w['w']=='обе')
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
# "бегая" (in "...не открываю [в] БЕГАЯ тренажёре игры...") -- same dropped-"в"
# + "его"-for-ЕГЭ garble as video1; redecode (14.6-16.3с) confirmed ' в' at
# 14.600 followed by the same slurred ЕГЭ continuation.
idx = next(i for i,w in enumerate(w3) if w['w']=='бегая')
w3 = replace_range(w3, idx, idx, [{'w':'в','t':14.900,'end':15.800}])
idx = next(i for i,w in enumerate(w3) if w['w']=='бегая')
w3[idx]['w'] = 'ЕГЭ'
# Last word "профи" (26.412-26.752) -- the source recording itself ends at
# 26.760с (ffprobe), essentially zero padding after this token: the speaker's
# "профиля" is cut off by the raw footage ending mid-word, not an ASR error.
# Completed to the intended word for subtitle/caption text; end clamped to the
# video's own duration since there is no more audio to extend into.
idx = next(i for i,w in enumerate(w3) if w['w']=='профи')
w3[idx]['w'] = 'профиля'
w3[idx]['end'] = 26.760
save(3, w3)
print('video3 fixed:', len(w3), 'words')
