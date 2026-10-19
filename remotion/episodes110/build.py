#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTY-THIRD 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes110/.

Four returning hosts, no new faces: "blonde in cream sweater" / desk+
lamp+plant+notebook room (a, f), "blue-shirt brunette" / THE SMITHS
poster + "ЕГЭ 2026" sticky note room (b, c, g), "mother" / bookshelf+
doorway apartment with small framed picture (d, h, i), "teen boy on
couch" / bookshelf+plant+window room (e).

Sub-themes: a class debate over whether a full practice variant or one
task at a time is better for ЕГЭ prep, resolved by needing both --
stamina from the full variant, precision from the single task; Russian's
irregular plural genitive forms (носков/чулок/килограммов etc) as the
one spot where grammar logic goes quiet and just needs a memorized list;
finding an old exam task already solved a year ago and now solving it
twice as fast -- old tasks as a ruler for measuring growth; a daughter
who stopped confusing the order of tasks in an exam variant once she
realized order is itself a plan; a bike key placed on top of the exam
collection so leaving the house means solving the task first; the
Battle of the Kalka and the Mongol invasion landing in the same
sentence for history ЕГЭ despite fifteen years between them, worth
memorizing as a sequence; being able to pick the right multiple-choice
answer but not explain why the other three are wrong, which turns out
to close real gaps; theory read before vs after a task -- inserted in
exactly the right spot it works as a hint instead of a lecture; and
wanting a daughter to fear command words like "объясните"/"обоснуйте"
less, since the fear fades once she sees a model answer.

Card/intro text was verified against the actual Golos Text Black render
(PIL getbbox at each line's real font size, small lines included) before
being written below -- consistent with the process that caught overflow
bugs in batches 58-59 and 27 overflows in batch 61.

ASR notes: episode f had "батея" for "Батыя" (a proper noun garble with
a clear, well-known correct form), fixed. Episode g had "ответо" for
"ответов" (dropped case ending) and "тренажери" for "тренажере" (garbled
case ending), both fixed. Episode h had "тренажеров" for "тренажер" in
the CTA line (garbled case ending), fixed. All four are unique 1:1 token
substitutions. Episode b's unintelligible "вига" (likely a slurred
"и ЕГЭ") was left unfixed and simply not quoted in card text.
"""
import json

REAL_DURATION = {
    "a": 20.311, "b": 23.788, "c": 19.650,
    "d": 15.810, "e": 15.980, "f": 22.188,
    "g": 21.720, "h": 20.631, "i": 17.303,
}
SOURCE_FILE = {
    "a": "cdgfhhjtsrhgrgh", "b": "gbfdrgdhdfhzsg", "c": "gfjshgfhfdfgdf",
    "d": "gnfnfnfdnn", "e": "hgfdhdhgdfhdhgfd", "f": "mfdgjjdfhfhf",
    "g": "mhfjghdfstajdhj", "h": "mhjgfdhjtd", "i": "nbmvcmfgfhjnfhb",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {},
    "d": {},
    "e": {},
    "f": {"батея": "батыя"},
    "g": {"ответо": "ответов", "тренажери": "тренажере"},
    "h": {"тренажеров": "тренажер"},
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
    with open(f"../asr_coffee123_63/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (blonde in cream sweater, 20.311s): a class debate over full
# practice variant vs one task at a time -- resolved by needing both,
# stamina from the variant and precision from the task, and the app's
# FIPI bank lets you do either
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВАРИАНТ ИЛИ", "ЗАДАНИЕ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 4.17, "lines": [{"text": "ЧТО ЛУЧШЕ ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ ИЛИ ЗАДАНИЕ", "accent": True, "size": "small"}]},
    {"start": 4.71, "end": 6.72, "lines": [{"text": "Я РЕШИЛА ВАРИАНТ", "accent": False, "size": "small"}, {"text": "И УВИДЕЛА ГДЕ ПРОСЕДАЮ", "accent": True, "size": "small"}]},
    {"start": 7.38, "end": 9.42, "lines": [{"text": "ВАРИАНТ ЦЕЛИКОМ", "accent": False, "size": "small"}, {"text": "ВЫНОСЛИВОСТЬ", "accent": True, "size": "small"}]},
    {"start": 9.72, "end": 11.22, "lines": [{"text": "ОДНО ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ТОЧНОСТЬ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 12.55, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "НУЖНЫ ОБА", "accent": True, "size": "big"}]},
    {"start": 13.32, "end": 14.14, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 15.06, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 16.92, "lines": [{"text": "ГДЕ МОЖНО РЕШАТЬ", "accent": False, "size": "small"}, {"text": "ПО ОДНОМУ ЗАДАНИЮ", "accent": True, "size": "small"}]},
    {"start": 17.19, "end": 18.57, "lines": [{"text": "И ЦЕЛЫМ", "accent": False, "size": "small"}, {"text": "ВАРИАНТОМ", "accent": True, "size": "big"}]},
    {"start": 18.57, "end": 19.50, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.50, "end": 20.311, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 1.62, "end": 2.46}, {"start": 7.38, "end": 9.42}, {"start": 16.08, "end": 18.03}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blue-shirt brunette, 23.788s): Russian's irregular plural
# genitive forms are the one spot where grammar logic goes quiet -- just
# needs a memorized list, and the app's memory games repeat those forms
# in quick rounds
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ГДЕ ЛОГИКА", "МОЛЧИТ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "МНОЖЕСТВЕННОЕ", "accent": False, "size": "small"}, {"text": "НОСОК", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 5.25, "lines": [{"text": "ЧУЛОК И", "accent": False, "size": "small"}, {"text": "КИЛОГРАММ ПО РУССКОМУ", "accent": True, "size": "small"}]},
    {"start": 6.36, "end": 8.40, "lines": [{"text": "ЕДИНСТВЕННОЕ МЕСТО", "accent": False, "size": "small"}, {"text": "ГДЕ ЛОГИКА МОЛЧИТ", "accent": True, "size": "small"}]},
    {"start": 9.06, "end": 10.44, "lines": [{"text": "МОЛЧИТ ОНА", "accent": False, "size": "small"}, {"text": "НЕ ТОЛЬКО У МЕНЯ", "accent": True, "size": "small"}]},
    {"start": 10.80, "end": 11.61, "lines": [{"text": "ЗДЕСЬ НУЖНЫ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 12.93, "lines": [{"text": "СПИСОК И", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 14.34, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.37, "end": 15.18, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 16.83, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.31, "end": 18.63, "lines": [{"text": "ГДЕ ФОРМЫ", "accent": False, "size": "small"}, {"text": "МНОЖЕСТВЕННОГО ЧИСЛА", "accent": True, "size": "small"}]},
    {"start": 19.05, "end": 19.86, "lines": [{"text": "ПОВТОРЯЮТСЯ", "accent": False, "size": "small"}, {"text": "СПИСКОМ", "accent": True, "size": "big"}]},
    {"start": 20.37, "end": 21.18, "lines": [{"text": "В БЫСТРЫХ", "accent": False, "size": "small"}, {"text": "РАУНДАХ", "accent": True, "size": "big"}]},
    {"start": 21.72, "end": 22.86, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.86, "end": 23.788, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.36, "end": 8.40}, {"start": 11.82, "end": 12.93}, {"start": 17.31, "end": 19.80}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 19.650s): finding an old exam task
# already solved a year ago and solving it twice as fast now -- old
# tasks as a ruler for growth, and the app's FIPI bank lets you revisit
# solved tasks and compare results
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЗАДАНИЕ ГОД", "НАЗАД"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 4.02, "lines": [{"text": "НАШЛА В СБОРНИКЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 6.57, "lines": [{"text": "ТЕПЕРЬ РЕШАЮ", "accent": False, "size": "small"}, {"text": "ВДВОЕ БЫСТРЕЕ", "accent": True, "size": "small"}]},
    {"start": 7.44, "end": 8.25, "lines": [{"text": "СТАРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 10.32, "lines": [{"text": "ЛИНЕЙКА ПО КОТОРОЙ", "accent": False, "size": "small"}, {"text": "ВИДНО РОСТ", "accent": True, "size": "big"}]},
    {"start": 11.10, "end": 12.93, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "small"}]},
    {"start": 13.47, "end": 14.79, "lines": [{"text": "ГДЕ УЖЕ", "accent": False, "size": "small"}, {"text": "РЕШЕННЫМ ЗАДАНИЯМ", "accent": True, "size": "small"}]},
    {"start": 15.00, "end": 16.89, "lines": [{"text": "МОЖНО ВЕРНУТЬСЯ", "accent": False, "size": "small"}, {"text": "И СРАВНИТЬ РЕЗУЛЬТАТ", "accent": True, "size": "small"}]},
    {"start": 17.52, "end": 18.84, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.84, "end": 19.650, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.50, "end": 6.57}, {"start": 8.70, "end": 10.32}, {"start": 15.00, "end": 16.89}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 15.810s): a daughter who stopped confusing the
# order of tasks in an exam variant once she realized order is itself a
# plan -- the app's FIPI bank lays out tasks in the order of a real
# variant
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПУТАЛА", "ПОРЯДОК"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "ДОЧЬ ПЕРЕСТАЛА", "accent": False, "size": "small"}, {"text": "ПУТАТЬ ПОРЯДОК", "accent": True, "size": "small"}]},
    {"start": 3.45, "end": 4.92, "lines": [{"text": "И ТЕПЕРЬ ЗНАЕТ", "accent": False, "size": "small"}, {"text": "С ЧЕГО НАЧИНАТЬ", "accent": True, "size": "small"}]},
    {"start": 5.61, "end": 6.51, "lines": [{"text": "ПОРЯДОК ЭТО", "accent": False, "size": "small"}, {"text": "ПЛАН", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.95, "lines": [{"text": "А ПЛАН", "accent": False, "size": "small"}, {"text": "СНИЖАЕТ СУЕТУ", "accent": True, "size": "small"}]},
    {"start": 8.70, "end": 10.38, "lines": [{"text": "В ЕГА ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "small"}]},
    {"start": 10.74, "end": 13.11, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "В ПОРЯДКЕ ВАРИАНТА", "accent": True, "size": "small"}]},
    {"start": 13.86, "end": 15.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 15.810, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.45, "end": 4.92}, {"start": 6.90, "end": 7.95}, {"start": 10.74, "end": 13.11}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (teen boy on couch, 15.980s): a bike key placed on top of
# the exam collection so leaving the house means solving the task first
# -- the app's FIPI bank makes one solved task the key to a good evening
# ---------------------------------------------------------------------------
e_intro = {"lines": ["КЛЮЧ ЛЕЖИТ", "У ЗАДАНИЯ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.12, "lines": [{"text": "Я ПОЛОЖИЛ РЯДОМ", "accent": False, "size": "small"}, {"text": "СО СБОРНИКОМ ЕГЭ", "accent": True, "size": "small"}]},
    {"start": 3.30, "end": 4.62, "lines": [{"text": "ЧТОБЫ СНАЧАЛА", "accent": False, "size": "small"}, {"text": "РЕШИТЬ ЗАДАНИЕ", "accent": True, "size": "small"}]},
    {"start": 4.89, "end": 5.70, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "ЕХАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 6.90, "lines": [{"text": "КЛЮЧ ЛЕЖИТ", "accent": False, "size": "small"}, {"text": "У ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.55, "lines": [{"text": "И ОБОЙТИ ЕГО", "accent": False, "size": "small"}, {"text": "НЕ ПОЛУЧАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 8.97, "end": 9.78, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 10.68, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 12.30, "lines": [{"text": "ГДЕ КЛЮЧ К", "accent": False, "size": "small"}, {"text": "ХОРОШЕМУ ВЕЧЕРУ", "accent": True, "size": "small"}]},
    {"start": 12.66, "end": 13.77, "lines": [{"text": "ОДНО", "accent": False, "size": "small"}, {"text": "РЕШЕННОЕ ЗАДАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.07, "end": 15.15, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 15.980, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 0.54, "end": 1.32}, {"start": 5.85, "end": 8.55}, {"start": 10.95, "end": 12.30}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde in cream sweater, 22.188s): the Battle of the Kalka
# and the Mongol invasion land in the same sentence for history ЕГЭ
# despite fifteen years between them -- worth memorizing as a sequence,
# and the app's history games line up 13th-century events in order
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ДВА СОБЫТИЯ", "ОДНА ФРАЗА"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.48, "lines": [{"text": "НАШЕСТВИЕ БАТЫЯ", "accent": False, "size": "small"}, {"text": "В ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 3.90, "end": 5.25, "lines": [{"text": "ИДУТ У МЕНЯ", "accent": False, "size": "small"}, {"text": "В ОДНОМ ПРЕДЛОЖЕНИИ", "accent": True, "size": "small"}]},
    {"start": 5.64, "end": 7.32, "lines": [{"text": "ХОТЯ МЕЖДУ НИМИ", "accent": False, "size": "small"}, {"text": "ПЯТНАДЦАТЬ ЛЕТ", "accent": True, "size": "small"}]},
    {"start": 8.04, "end": 10.35, "lines": [{"text": "ПЯТНАДЦАТЬ ЛЕТ", "accent": False, "size": "small"}, {"text": "ЭТО СОБЫТИЕ ИЛИ ДВА", "accent": True, "size": "small"}]},
    {"start": 10.83, "end": 12.93, "lines": [{"text": "И РАДИ НИХ СТОИТ ВЫУЧИТЬ", "accent": False, "size": "small"}, {"text": "ПОСЛЕДОВАТЕЛЬНОСТЬ", "accent": True, "size": "small"}]},
    {"start": 13.56, "end": 14.82, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 16.20, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.65, "end": 18.03, "lines": [{"text": "ГДЕ СОБЫТИЯ", "accent": False, "size": "small"}, {"text": "ТРИНАДЦАТОГО ВЕКА", "accent": True, "size": "small"}]},
    {"start": 18.21, "end": 19.71, "lines": [{"text": "ВЫСТРАИВАЮТСЯ", "accent": False, "size": "small"}, {"text": "В ПОРЯДКЕ ОЧЕРЕДИ", "accent": True, "size": "small"}]},
    {"start": 20.37, "end": 21.38, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.38, "end": 22.188, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.64, "end": 7.32}, {"start": 9.30, "end": 10.35}, {"start": 18.21, "end": 19.71}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (blue-shirt brunette, 21.720s): can pick the right
# multiple-choice answer but not explain why the other three are wrong
# -- explaining wrong answers closes real gaps, and the app's text
# breakdown explains why each wrong answer doesn't fit
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ОТВЕТ ЗНАЮ", "ПОЧЕМУ НЕТ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "В ТЕСТЕ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.76, "end": 3.66, "lines": [{"text": "Я ВЫБИРАЮ", "accent": False, "size": "small"}, {"text": "ВЕРНЫЙ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.01, "lines": [{"text": "А ПОЧЕМУ ТРИ", "accent": False, "size": "small"}, {"text": "ДРУГИХ", "accent": True, "size": "big"}]},
    {"start": 5.22, "end": 6.12, "lines": [{"text": "НЕВЕРНЫЕ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ НЕ МОГУ", "accent": True, "size": "small"}]},
    {"start": 7.47, "end": 8.85, "lines": [{"text": "ОБЪЯСНЕНИЕ", "accent": False, "size": "small"}, {"text": "НЕВЕРНЫХ ВАРИАНТОВ", "accent": True, "size": "small"}]},
    {"start": 9.00, "end": 9.82, "lines": [{"text": "ЗАКРЫВАЕТ", "accent": False, "size": "small"}, {"text": "ПРОБЕЛ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.02, "lines": [{"text": "В СЛЕДУЮЩЕМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИИ", "accent": True, "size": "big"}]},
    {"start": 11.13, "end": 12.30, "lines": [{"text": "ЛОВУШКИ УЖЕ", "accent": False, "size": "small"}, {"text": "ЗНАКОМЫ", "accent": True, "size": "big"}]},
    {"start": 13.14, "end": 13.96, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 15.60, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 15.99, "end": 18.27, "lines": [{"text": "ГДЕ ОБЪЯСНЕНО", "accent": False, "size": "small"}, {"text": "ПОЧЕМУ ОСТАЛЬНЫЕ", "accent": True, "size": "small"}]},
    {"start": 18.69, "end": 19.71, "lines": [{"text": "ВАРИАНТЫ ОТВЕТА", "accent": False, "size": "small"}, {"text": "НЕ ПОДХОДЯТ", "accent": True, "size": "small"}]},
    {"start": 19.71, "end": 20.82, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.82, "end": 21.720, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 5.22, "end": 6.12}, {"start": 7.47, "end": 8.85}, {"start": 15.99, "end": 18.27}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (mother, 20.631s): theory read before vs after a task --
# inserted in exactly the right spot it works as a hint instead of a
# lecture, same as the app's text breakdown which inserts theory exactly
# where it's needed
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ДО ИЛИ ПОСЛЕ", "НЕ ЗНАЮ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "ДО ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ИЛИ ПОСЛЕ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.65, "lines": [{"text": "Я ПЕРЕПРОБОВАЛА", "accent": False, "size": "small"}, {"text": "ОБА", "accent": True, "size": "big"}]},
    {"start": 4.77, "end": 6.15, "lines": [{"text": "ПОРЯДКА И НЕ", "accent": False, "size": "small"}, {"text": "МОГУ ВЫБРАТЬ", "accent": True, "size": "small"}]},
    {"start": 6.87, "end": 8.64, "lines": [{"text": "ЕСЛИ ТЕОРИЯ В НУЖНОЕ", "accent": False, "size": "small"}, {"text": "МЕСТО", "accent": True, "size": "big"}]},
    {"start": 8.88, "end": 9.69, "lines": [{"text": "ВЫБОР", "accent": False, "size": "small"}, {"text": "ОТПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 12.24, "lines": [{"text": "ОНА РАБОТАЕТ КАК", "accent": False, "size": "small"}, {"text": "ПОДСКАЗКА А НЕ ЛЕКЦИЯ", "accent": True, "size": "small"}]},
    {"start": 12.93, "end": 14.31, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 14.46, "end": 15.27, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 16.74, "lines": [{"text": "В КОТОРОЙ ТЕОРИЯ", "accent": False, "size": "small"}, {"text": "ВСТАВЛЕНА", "accent": True, "size": "big"}]},
    {"start": 16.95, "end": 18.18, "lines": [{"text": "РОВНО ТАМ ГДЕ", "accent": False, "size": "small"}, {"text": "ОНА НУЖНА", "accent": True, "size": "big"}]},
    {"start": 18.96, "end": 19.82, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.82, "end": 20.631, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.63, "end": 4.65}, {"start": 6.87, "end": 8.64}, {"start": 10.05, "end": 12.24}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (mother, 17.303s): wanting a daughter to fear command words
# like "объясните"/"обоснуйте" less -- the fear fades once you see a
# model answer, same as the app's text breakdown which shows a model
# answer for "объясните"
# ---------------------------------------------------------------------------
i_intro = {"lines": ["БОЮСЬ СЛОВА", "ОБЪЯСНИТЕ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "ЧТОБЫ ДОЧЬ МЕНЬШЕ", "accent": False, "size": "small"}, {"text": "БОЯЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 2.85, "end": 4.02, "lines": [{"text": "СЛОВ ОБЪЯСНИТЬ", "accent": False, "size": "small"}, {"text": "И ОБОСНУЙТЕ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 4.98, "lines": [{"text": "В ЗАДАНИЯХ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.49, "end": 7.02, "lines": [{"text": "СТРАХ УХОДИТ", "accent": False, "size": "small"}, {"text": "КОГДА ВИДИШЬ ОБРАЗЕЦ", "accent": True, "size": "small"}]},
    {"start": 7.41, "end": 8.52, "lines": [{"text": "ЧТО ЗНАЧИТ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЕ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.78, "lines": [{"text": "И СКОЛЬКО", "accent": False, "size": "small"}, {"text": "СТРОК НУЖНО", "accent": True, "size": "small"}]},
    {"start": 10.23, "end": 11.37, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 11.49, "end": 12.45, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 14.10, "lines": [{"text": "ГДЕ ПОКАЗАН", "accent": False, "size": "small"}, {"text": "ОБРАЗЕЦ ОТВЕТА", "accent": True, "size": "small"}]},
    {"start": 14.22, "end": 15.15, "lines": [{"text": "НА СЛОВО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЕ", "accent": True, "size": "big"}]},
    {"start": 15.57, "end": 16.49, "lines": [{"text": "ССЫЛКА НА Г", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.49, "end": 17.303, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 5.49, "end": 6.30}, {"start": 7.41, "end": 8.52}, {"start": 12.75, "end": 14.10}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
