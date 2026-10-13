#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-FIRST 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes98/.

Three returning hosts, no new faces: "Рома" / black Under Armour hoodie
(a, b, h), "mother" / bookshelf+doorway apartment with small framed
picture (c, g), "blonde in cream sweater" (d), "teen boy on couch"
(e, f, i).

Sub-themes: practice runs that stop exactly where the hard part starts,
copying a solved method and plugging in new numbers without
understanding why each step exists, a new method from a teacher that
dissolves by evening because there was no time to write it down, one
dictation word rewritten three times before it stuck, an answer format
mismatch with no way to tell if it counts, staying silent on a museum
excursion question that an exam won't forgive, a parent-teacher meeting
revealing which spelling words actually trip up a kid, a sister's
vocabulary dictation exposing a word that resists any rule, and a
school project collision that forces exam prep into ten-minute blocks.
"""
import json

REAL_DURATION = {
    "a": 16.172, "b": 16.620, "c": 18.263,
    "d": 24.663, "e": 16.556, "f": 17.602,
    "g": 18.903, "h": 17.880, "i": 15.682,
}
SOURCE_FILE = {
    "a": "cbvcvcvsvsdvsdvs", "b": "cvvsvsdvsvsdv", "c": "dshsdbsgsgdsgsf",
    "d": "dssggdffdsfdf", "e": "fbsdhggvsdfdsfdsf", "f": "fdbdghfgvvgsdfdf",
    "g": "fshfbgsvgsfgsdfsd", "h": "sdbsbsdbsvvs", "i": "xbhxhhwgweffefd",
}
FIXES = {
    "a": {"сложная": "сложное"},
    "b": {},
    "c": {"он": "она", "опомнила": "вспомнила"},
    "d": {"дектанте": "диктанте"},
    "e": {"текстовые": "текстовый"},
    "f": {},
    "g": {"ея": "я"},
    "h": {},
    "i": {},
}


def check_cards(ep, cards, total_duration):
    prev_end = 0.0
    for i, c in enumerate(cards):
        assert c["start"] < c["end"], f"ep{ep} card{i}: start>=end"
        assert c["start"] >= prev_end - 1e-6, f"ep{ep} card{i}: overlaps previous (start {c['start']} < prev_end {prev_end})"
        dur = c["end"] - c["start"]
        assert dur <= 4.0 + 1e-6, f"ep{ep} card{i}: duration {dur:.2f}s > 4s"
        assert dur >= 0.79, f"ep{ep} card{i}: duration {dur:.2f}s < 0.8s (too short)"
        n_accent = sum(1 for l in c["lines"] for l in [l] if l.get("accent"))
        assert n_accent >= 1, f"ep{ep} card{i}: no accent line"
        for l in c["lines"]:
            assert "?" not in l["text"] or l["text"].endswith("?"), f"ep{ep} card{i}: bad '?' placement"
            assert "," not in l["text"] and "." not in l["text"] and "-" not in l["text"], f"ep{ep} card{i}: punctuation not allowed: {l['text']}"
            if l.get("accent") and l["size"] == "big":
                longest = max((len(w) for w in l["text"].split()), default=0)
                assert longest <= 10, f"ep{ep} card{i}: accent word too long ({longest} chars): {l['text']!r}"
        prev_end = c["end"]
    assert prev_end <= total_duration + 0.5, f"ep{ep}: last card end {prev_end} exceeds total_duration {total_duration}"


def check_intro_vs_cards(ep, intro_end, cards):
    assert cards[0]["start"] >= intro_end, f"ep{ep}: card1 start {cards[0]['start']} < intro end {intro_end}"
    assert 1.5 <= intro_end <= 3.0, f"ep{ep}: intro end {intro_end} out of 1.5-3.0s range"


def check_emphasis(ep, emphasis, total_duration):
    prev_end = -10
    for w in emphasis:
        assert w["start"] < w["end"]
        assert w["start"] >= prev_end + 1.0, f"ep{ep}: emphasis windows too close ({prev_end} -> {w['start']})"
        assert w["end"] <= total_duration
        prev_end = w["end"]
    assert 2 <= len(emphasis) <= 4, f"ep{ep}: {len(emphasis)} emphasis windows (need 2-4)"


def fix_words(letter, words):
    fixes = FIXES.get(letter, {})
    out = []
    for w in words:
        t = w["text"]
        if t in fixes:
            t = fixes[t]
        out.append({"text": t, "start": w["start"], "end": w["end"]})
    return out


def build_running_caption(words):
    return [{"text": w["text"].upper(), "start": w["start"], "end": w["end"]} for w in words]


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    stem = SOURCE_FILE[letter]
    with open(f"../asr_coffee123_51/{stem}_words.json", encoding="utf-8") as f:
        words = json.load(f)
    words = fix_words(letter, words)

    check_cards(letter, cards, total_duration)
    check_intro_vs_cards(letter, intro["end"], cards)
    check_emphasis(letter, emphasis, total_duration)

    running_caption = build_running_caption(words)

    with open(f"ep_{letter}_cards.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_intro.json", "w", encoding="utf-8") as f:
        json.dump(intro, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_emphasis.json", "w", encoding="utf-8") as f:
        json.dump(emphasis, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_running_caption.json", "w", encoding="utf-8") as f:
        json.dump(running_caption, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_stock_cutaways.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_duration.json", "w", encoding="utf-8") as f:
        json.dump({"total_duration": total_duration}, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print(f"ep{letter}: OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode A (Рома, 16.172s): practice always stops exactly where the
# hard part starts -- hard tasks get pushed to tomorrow, and tomorrow
# they get pushed again while the unsolved list grows; the app's FIPI
# bank lets hard tasks be returned to one at a time
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ТРЕНИРОВКА ЗАКАНЧИВАЕТСЯ", "ГДЕ НАЧИНАЕТСЯ СЛОЖНОЕ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ТРЕНИРОВКА ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "ЗАКАНЧИВАЕТСЯ ТАМ", "accent": True, "size": "small"}]},
    {"start": 3.30, "end": 4.95, "lines": [{"text": "ГДЕ НАЧИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "СЛОЖНОЕ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.75, "lines": [{"text": "СЛОЖНОЕ Я", "accent": False, "size": "small"}, {"text": "ОТКЛАДЫВАЮ НА ЗАВТРА", "accent": True, "size": "small"}]},
    {"start": 6.75, "end": 8.70, "lines": [{"text": "А ЗАВТРА", "accent": False, "size": "small"}, {"text": "СНОВА ОТКЛАДЫВАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 8.70, "end": 10.35, "lines": [{"text": "И СПИСОК", "accent": False, "size": "small"}, {"text": "НЕРЕШЕННОГО РАСТЕТ", "accent": True, "size": "small"}]},
    {"start": 10.35, "end": 11.25, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.25, "end": 12.15, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 13.60, "lines": [{"text": "ГДЕ МОЖНО", "accent": False, "size": "small"}, {"text": "ВОЗВРАЩАТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 13.60, "end": 14.40, "lines": [{"text": "К ТРУДНЫМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ ПО ОДНОМУ", "accent": True, "size": "small"}]},
    {"start": 14.40, "end": 15.35, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.35, "end": 16.172, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.42, "end": 3.75}, {"start": 8.91, "end": 9.78}, {"start": 12.54, "end": 13.47}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 16.620s): copying a solved method and plugging in
# new numbers doesn't work when the answer doesn't match -- mechanical
# substitution isn't enough, each step needs to be understood; the
# app's text breakdown explains why each step is there
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПОДСТАВИЛ ЧИСЛА", "НО ОТВЕТ НЕ СОШЕЛСЯ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ПЕРЕПИСАЛ РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "ИЗ РАЗБОРА И", "accent": False, "size": "small"}, {"text": "ПОДСТАВИЛ СВОИ ЧИСЛА", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.70, "lines": [{"text": "НО ОТВЕТ", "accent": False, "size": "small"}, {"text": "НЕ СОШЕЛСЯ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.50, "lines": [{"text": "ЗНАЧИТ", "accent": False, "size": "small"}, {"text": "МЕХАНИЧЕСКИ ПОДСТАВЛЯТЬ", "accent": True, "size": "small"}]},
    {"start": 7.50, "end": 8.70, "lines": [{"text": "НЕЛЬЗЯ", "accent": False, "size": "small"}, {"text": "НУЖНО ВИДЕТЬ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.90, "lines": [{"text": "ЗАЧЕМ СДЕЛАН", "accent": False, "size": "small"}, {"text": "КАЖДЫЙ ШАГ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.80, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.80, "end": 11.90, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.90, "end": 13.30, "lines": [{"text": "ГДЕ У КАЖДОГО", "accent": False, "size": "small"}, {"text": "ШАГА ЕСТЬ ОБЪЯСНЕНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.30, "end": 14.90, "lines": [{"text": "ЗАЧЕМ ОН", "accent": False, "size": "small"}, {"text": "НУЖЕН", "accent": True, "size": "big"}]},
    {"start": 14.90, "end": 15.80, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.80, "end": 16.620, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.41, "end": 5.46}, {"start": 7.71, "end": 8.22}, {"start": 14.10, "end": 14.76}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 18.263s): a teacher gives a new method but there's
# no time to write it down -- by evening only the name is remembered,
# the method itself dissolved; the app's text breakdown is written
# down and can be reread
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НОВЫЙ СПОСОБ", "А ЗАПИСАТЬ НЕ УСПЕЛА"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ДОЧЬ ВЕРНУЛАСЬ", "accent": False, "size": "small"}, {"text": "С УРОКА ПО ЕГ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.35, "lines": [{"text": "УЧИТЕЛЬ ДАЛ", "accent": False, "size": "small"}, {"text": "НОВЫЙ СПОСОБ", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 5.70, "lines": [{"text": "НО ЗАПИСАТЬ", "accent": False, "size": "small"}, {"text": "ОНА НЕ УСПЕЛА", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.65, "lines": [{"text": "К ВЕЧЕРУ ОНА", "accent": False, "size": "small"}, {"text": "ВСПОМНИЛА", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 8.70, "lines": [{"text": "ТОЛЬКО", "accent": False, "size": "small"}, {"text": "НАЗВАНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 10.20, "lines": [{"text": "А САМ СПОСОБ", "accent": False, "size": "small"}, {"text": "РАСТВОРИЛСЯ", "accent": True, "size": "small"}]},
    {"start": 10.30, "end": 11.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.00, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.00, "end": 14.00, "lines": [{"text": "ГДЕ СПОСОБ", "accent": False, "size": "small"}, {"text": "ОПИСАН ПИСЬМЕННО", "accent": True, "size": "big"}]},
    {"start": 14.50, "end": 16.00, "lines": [{"text": "И ЕГО МОЖНО", "accent": False, "size": "small"}, {"text": "ПЕРЕЧИТАТЬ", "accent": True, "size": "small"}]},
    {"start": 16.15, "end": 17.10, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.263, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.60, "end": 4.17}, {"start": 7.05, "end": 7.35}, {"start": 9.15, "end": 9.72}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blonde in cream sweater, 24.663s): one dictation word gets
# rewritten three different ways before it sticks -- rare words aren't
# derived by rule, they need repeated exposure; the app's memory games
# repeat such rare words in pairs
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ТРИ РАЗА ПЕРЕПИСАЛА", "ОДНО СЛОВО"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "СЛОВО ЧЕРЕСЧУР", "accent": False, "size": "small"}, {"text": "В ДИКТАНТЕ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.35, "lines": [{"text": "ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ НАПИСАЛА", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 5.40, "lines": [{"text": "В ТРИ", "accent": False, "size": "small"}, {"text": "ПРИЕМА", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 7.80, "lines": [{"text": "СНАЧАЛА ТАК", "accent": False, "size": "small"}, {"text": "ПОТОМ ИНАЧЕ", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.30, "lines": [{"text": "ПОТОМ", "accent": False, "size": "small"}, {"text": "ЗАЧЕРКНУЛА", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.50, "lines": [{"text": "РЕДКИЕ СЛОВА", "accent": False, "size": "small"}, {"text": "НЕ ВЫВОДЯТСЯ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.90, "lines": [{"text": "ПРАВИЛОМ", "accent": False, "size": "small"}, {"text": "ИХ НУЖНО ВИДЕТЬ", "accent": True, "size": "big"}]},
    {"start": 11.90, "end": 13.60, "lines": [{"text": "МНОГО РАЗ", "accent": False, "size": "small"}, {"text": "ПОКА НАПИСАНИЕ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 16.10, "lines": [{"text": "НЕ СТАНЕТ", "accent": False, "size": "small"}, {"text": "ПРИВЫЧНЫМ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.10, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.10, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 18.10, "end": 19.60, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.80, "end": 21.80, "lines": [{"text": "ГДЕ ТАКИЕ", "accent": False, "size": "small"}, {"text": "РЕДКИЕ СЛОВА", "accent": True, "size": "big"}]},
    {"start": 21.80, "end": 22.80, "lines": [{"text": "ПОВТОРЯЮТСЯ", "accent": False, "size": "small"}, {"text": "ПАРАМИ", "accent": True, "size": "big"}]},
    {"start": 22.90, "end": 23.85, "lines": [{"text": "ССЫЛКА НА Г", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.85, "end": 24.663, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.08, "end": 1.47}, {"start": 7.83, "end": 8.37}, {"start": 14.52, "end": 15.36}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (teen boy on couch, 16.556s): a book answer is given as a
# fraction but a decimal comes out instead, with no way to know if the
# format counts; the app's text breakdown shows exactly what format to
# write the answer in
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОТВЕТ ДРОБЬЮ", "А У МЕНЯ ДЕСЯТИЧНАЯ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "В СБОРНИКЕ ОТВЕТ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЮ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "ЗАПИСАН", "accent": False, "size": "small"}, {"text": "ДРОБЬЮ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.70, "lines": [{"text": "А У МЕНЯ ВЫШЛО", "accent": False, "size": "small"}, {"text": "ДЕСЯТИЧНАЯ ЗАПИСЬ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 6.60, "lines": [{"text": "И Я НЕ ЗНАЮ", "accent": False, "size": "small"}, {"text": "ЗАСЧИТАЮТ ЛИ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 7.80, "lines": [{"text": "ФОРМА ОТВЕТА", "accent": False, "size": "small"}, {"text": "ВАЖНА", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.60, "lines": [{"text": "ОБ ЭТОМ", "accent": False, "size": "small"}, {"text": "НЕ ВСЕГДА УКАЗАНО", "accent": True, "size": "big"}]},
    {"start": 9.70, "end": 10.50, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.30, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.30, "end": 13.00, "lines": [{"text": "ГДЕ УКАЗАНО", "accent": False, "size": "small"}, {"text": "В КАКОЙ ФОРМЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.40, "lines": [{"text": "ЗАПИСЫВАТЬ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 15.50, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.50, "end": 16.556, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.88, "end": 3.15}, {"start": 7.35, "end": 7.56}, {"start": 13.02, "end": 13.44}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 17.602s): a museum guide's question
# about how a war ended gets met with silence because only part of the
# answer is known -- but an exam won't forgive staying silent; the
# app's memory games make war outcomes get named in full
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ГИД СПРОСИЛ", "А Я ПРОМОЛЧАЛ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "НА ЭКСКУРСИИ", "accent": False, "size": "small"}, {"text": "В МУЗЕЕ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.50, "lines": [{"text": "ГИД СПРОСИЛ", "accent": False, "size": "small"}, {"text": "ЧЕМ ЗАКОНЧИЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 4.50, "end": 5.70, "lines": [{"text": "СЕВЕРНАЯ", "accent": False, "size": "small"}, {"text": "ВОЙНА", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.50, "lines": [{"text": "И Я ДЛЯ ЕГ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ ПРОМОЛЧАЛ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.40, "lines": [{"text": "ЗНАЛ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "КУСОК ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.30, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "РЕШИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.65, "lines": [{"text": "А НА ЭКЗАМЕНЕ", "accent": False, "size": "small"}, {"text": "ПРОМОЛЧАТЬ НЕЛЬЗЯ", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 11.55, "lines": [{"text": "В ЕГА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.55, "end": 12.60, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.50, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.50, "end": 15.65, "lines": [{"text": "ГДЕ ИТОГИ ВОЙН", "accent": False, "size": "small"}, {"text": "НУЖНО НАЗЫВАТЬ ПОЛНОСТЬЮ", "accent": True, "size": "big"}]},
    {"start": 15.65, "end": 16.60, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 17.602, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 3.75, "end": 4.35}, {"start": 9.30, "end": 10.08}, {"start": 14.97, "end": 15.33}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (mother, 18.903s): a parent-teacher meeting reveals most
# points are lost on spelling, and asking a daughter directly turns up
# five confused words at once; the app's memory games repeat such
# words briefly
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ТЕРЯЮТ БАЛЛЫ", "НА ОРФОГРАФИИ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "УЧИТЕЛЬНИЦА СКАЗАЛА", "accent": False, "size": "small"}, {"text": "НА СОБРАНИИ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.50, "lines": [{"text": "ЧТО НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.85, "lines": [{"text": "ЧАЩЕ ВСЕГО", "accent": False, "size": "small"}, {"text": "ТЕРЯЮТ БАЛЛЫ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 6.90, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ОРФОГРАФИИ", "accent": True, "size": "small"}]},
    {"start": 6.90, "end": 7.95, "lines": [{"text": "ДОМА Я", "accent": False, "size": "small"}, {"text": "СПРОСИЛА ДОЧЬ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 8.75, "lines": [{"text": "КАКИЕ СЛОВА", "accent": False, "size": "small"}, {"text": "ОНА ПУТАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.75, "end": 9.60, "lines": [{"text": "ЧАЩЕ", "accent": False, "size": "small"}, {"text": "ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "И ОНА НАЗВАЛА", "accent": False, "size": "small"}, {"text": "СРАЗУ ПЯТЬ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.60, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.60, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 14.80, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.90, "end": 16.60, "lines": [{"text": "ГДЕ ТАКИЕ СЛОВА", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ КОРОТКО", "accent": True, "size": "small"}]},
    {"start": 17.10, "end": 18.05, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.05, "end": 18.903, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 4.59, "end": 5.13}, {"start": 8.46, "end": 8.67}, {"start": 10.59, "end": 11.01}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (Рома, 17.880s): a sister's vocabulary dictation exposes a
# word that resists any rule -- vocabulary words have to be repeated
# until the hand remembers; the app's memory games repeat vocabulary
# words in short series
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ОШИБЛАСЬ В СЛОВЕ", "ВИНЕГРЕТ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "СЕСТРА ДИКТОВАЛА", "accent": False, "size": "small"}, {"text": "СЛОВАРНЫЕ СЛОВА", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.40, "lines": [{"text": "И В СЛОВЕ", "accent": False, "size": "small"}, {"text": "ВИНЕГРЕТ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.30, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "ОШИБСЯ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.50, "lines": [{"text": "СЛОВАРНЫЕ СЛОВА", "accent": False, "size": "small"}, {"text": "НЕ ВЫВЕДЕШЬ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.70, "lines": [{"text": "ПРАВИЛАМ", "accent": False, "size": "small"}, {"text": "ИХ ПРИХОДИТСЯ", "accent": True, "size": "small"}]},
    {"start": 8.70, "end": 9.90, "lines": [{"text": "ПОВТОРЯТЬ", "accent": False, "size": "small"}, {"text": "ПОКА РУКА", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.80, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ЗАПОМНИТ", "accent": True, "size": "big"}]},
    {"start": 10.80, "end": 11.70, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.70, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 12.70, "end": 13.80, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.80, "end": 14.70, "lines": [{"text": "ГДЕ СЛОВАРНЫЕ", "accent": False, "size": "small"}, {"text": "СЛОВА ПОВТОРЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 14.70, "end": 15.80, "lines": [{"text": "КОРОТКИМИ", "accent": False, "size": "small"}, {"text": "СЕРИЯМИ", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 16.85, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.85, "end": 17.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 4.20, "end": 4.65}, {"start": 6.54, "end": 6.90}, {"start": 9.42, "end": 9.72}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (teen boy on couch, 15.682s): a school project collides
# with exam-prep week and evenings run out -- prep gets split into
# ten-minute blocks between other tasks; the app's FIPI bank has short
# tasks, so ten minutes is enough for one or two
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ВЕЧЕРА ЗАКОНЧИЛИСЬ", "РАЗБИЛ НА БЛОКИ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ШКОЛЬНЫЙ ПРОЕКТ", "accent": False, "size": "small"}, {"text": "СОВПАЛ С ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "И ВЕЧЕРА", "accent": False, "size": "small"}, {"text": "ЗАКОНЧИЛИСЬ", "accent": True, "size": "small"}]},
    {"start": 4.20, "end": 5.70, "lines": [{"text": "Я РАЗБИЛ", "accent": False, "size": "small"}, {"text": "ПОДГОТОВКУ НА БЛОКИ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.20, "lines": [{"text": "ПО ДЕСЯТЬ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.40, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "ДЕЛАМИ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.30, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.20, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.60, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "КОРОТКИЕ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 12.90, "lines": [{"text": "И ДЕСЯТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "ХВАТАЕТ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 13.70, "lines": [{"text": "НА ОДНО", "accent": False, "size": "small"}, {"text": "ДВА", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 14.70, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.682, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 3.99, "end": 4.50}, {"start": 11.07, "end": 11.46}, {"start": 12.90, "end": 13.47}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
