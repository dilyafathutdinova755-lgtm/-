#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTY-SECOND 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes109/.

Two returning hosts, no new faces: "mother" / bookshelf+doorway apartment
with small framed picture (a, e), "Рома" (tight curls, black Under Armour
hoodie) in two different rooms -- a desk room (c) and a sunset-window
balcony room (d, f) -- first appearance in this session's window but
already on the established host roster from earlier batches, "teen boy
on couch" / bookshelf+plant+window room (b).

Sub-themes: wishing a task breakdown felt like a conversation instead of
a lecture the daughter just reads at, since a "living" Q&A breakdown is
more memorable; not being able to choose between a picture (memorable)
or a formula (fast to check) breakdown and realizing both are needed --
a picture for the idea, a formula for the check; a breakdown that calls
a mistake an "imprecision" instead of naming it plainly, which breeds
suspicion something's being hidden, versus a direct one: here's the
mistake, here's the cause, here's the fix; recognizing Russian homonyms
by picture but struggling to name them by meaning, when meaning is what
actually gets tested; a daughter who understands how a bank account
works from the example of one real card, but social studies ЕГЭ asks
for bank functions as a full list, not one example; and a friend who
buys a thousand-task collection and shelves it to avoid flipping through
it, while the narrator's own "shelf" is a screen where any task opens
with one tap.

Card/intro text was verified against the actual Golos Text Black render
(PIL getbbox at each line's real font size, small lines included) before
being written below -- consistent with the process that caught overflow
bugs in batches 58-59 and found 27 overflows in batch 61.

ASR notes: episode d had three fixable garbles -- "монимы" (dropped
leading "о" from "омонимы"), "егтренажере" (merged "ег"+"тренажере",
fixed by dropping the "ег" half per the established drop-the-extra-part
precedent), and "аммонимов" (extra "м" in "омонимов") -- all unique
1:1 token substitutions. Episode f's "где а тысячи заданий" (a stray
filler "а") and episode d's minor subject-verb agreement wobble
("значение... повторяются" instead of "повторяется") are natural-speech
imperfections, not ASR garble, and are left alone in FIXES; the card
text routes around them with a clean paraphrase as usual.
"""
import json

REAL_DURATION = {
    "a": 18.480, "b": 17.360, "c": 17.964,
    "d": 15.746, "e": 18.967, "f": 14.560,
}
SOURCE_FILE = {
    "a": "gfdhhjnfhhgfh", "b": "gfhdndxfh", "c": "gfjhfdjhndfhhb",
    "d": "hfdshgnhdhg", "e": "hfghdghfdgd", "f": "hjgfjfdrhgf",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {},
    "d": {"монимы": "омонимы", "егтренажере": "тренажере", "аммонимов": "омонимов"},
    "e": {},
    "f": {},
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
    with open(f"../asr_coffee123_62/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (mother, 18.480s): wishing a task breakdown felt like a
# conversation instead of a lecture the daughter just reads -- a living
# Q&A breakdown sticks better, and the app's text breakdown is written
# as a conversation with questions and answers
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЧИТАЕТ РАЗБОР", "КАК ЛЕКЦИЮ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.09, "lines": [{"text": "ХОЧУ ЧТОБЫ РАЗБОР", "accent": False, "size": "small"}, {"text": "РАЗГОВОР", "accent": True, "size": "big"}]},
    {"start": 4.14, "end": 5.52, "lines": [{"text": "А ДОЧЬ ЧИТАЕТ", "accent": False, "size": "small"}, {"text": "КАК ЛЕКЦИЮ", "accent": True, "size": "big"}]},
    {"start": 6.57, "end": 8.07, "lines": [{"text": "ЖИВОЙ РАЗБОР", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 8.19, "end": 10.11, "lines": [{"text": "ПОТОМУ ЧТО В НЕМ", "accent": False, "size": "small"}, {"text": "ВОПРОСЫ И ОТВЕТЫ", "accent": True, "size": "small"}]},
    {"start": 10.83, "end": 11.65, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.23, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 13.62, "end": 16.02, "lines": [{"text": "НАПИСАННЫЙ КАК РАЗГОВОР", "accent": False, "size": "small"}, {"text": "С ВОПРОСАМИ", "accent": True, "size": "small"}]},
    {"start": 16.59, "end": 17.68, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.68, "end": 18.480, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.49, "end": 3.69}, {"start": 6.57, "end": 8.07}, {"start": 13.62, "end": 16.02}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (teen boy on couch, 17.360s): can't choose between a picture
# breakdown (memorable) and a formula breakdown (fast to check) -- better
# to have both, and the app's text breakdown attaches a picture to the
# idea and a formula to the check
# ---------------------------------------------------------------------------
b_intro = {"lines": ["КАРТИНКА ИЛИ", "ФОРМУЛА"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "РАЗБОР С КАРТИНКОЙ", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 3.12, "end": 3.93, "lines": [{"text": "А С ФОРМУЛОЙ", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 4.14, "end": 5.97, "lines": [{"text": "Я НЕ МОГУ ВЫБРАТЬ", "accent": False, "size": "small"}, {"text": "ЧТО ВАЖНЕЕ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.62, "lines": [{"text": "ЛУЧШЕ ИМЕТЬ", "accent": False, "size": "small"}, {"text": "И ТО И ДРУГОЕ", "accent": True, "size": "small"}]},
    {"start": 7.86, "end": 8.76, "lines": [{"text": "КАРТИНКУ ДЛЯ", "accent": False, "size": "small"}, {"text": "ИДЕИ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 9.90, "lines": [{"text": "ФОРМУЛУ ДЛЯ", "accent": False, "size": "small"}, {"text": "ПРОВЕРКИ", "accent": True, "size": "big"}]},
    {"start": 10.26, "end": 11.06, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.06, "end": 12.57, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 12.72, "end": 14.10, "lines": [{"text": "ГДЕ К ИДЕЕ", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНА КАРТИНКА", "accent": True, "size": "small"}]},
    {"start": 14.37, "end": 15.36, "lines": [{"text": "А К ПРОВЕРКЕ", "accent": False, "size": "small"}, {"text": "ФОРМУЛА", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.56, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.56, "end": 17.360, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.12, "end": 3.93}, {"start": 6.30, "end": 7.62}, {"start": 12.72, "end": 14.10}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 17.964s): a breakdown that calls a mistake an
# "imprecision" breeds suspicion something's being hidden -- a good
# breakdown is direct: here's the mistake, the cause, the fix, same as
# the app's text breakdown
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЧТО ТО ОТ МЕНЯ", "СКРЫВАЮТ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.63, "lines": [{"text": "ОШИБКУ НАЗЫВАЮТ", "accent": False, "size": "small"}, {"text": "НЕТОЧНОСТЬЮ", "accent": True, "size": "small"}]},
    {"start": 3.84, "end": 6.36, "lines": [{"text": "ЗНАЧИТ ОТ МЕНЯ", "accent": False, "size": "small"}, {"text": "ЧТО ТО СКРЫВАЮТ", "accent": True, "size": "small"}]},
    {"start": 6.69, "end": 7.65, "lines": [{"text": "ХОРОШИЙ РАЗБОР", "accent": False, "size": "small"}, {"text": "ПРЯМОЙ", "accent": True, "size": "big"}]},
    {"start": 8.04, "end": 10.35, "lines": [{"text": "ВОТ ОШИБКА ВОТ", "accent": False, "size": "small"}, {"text": "ПРИЧИНА И ИСПРАВЛЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 10.74, "end": 11.56, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.58, "end": 13.02, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 13.23, "end": 14.40, "lines": [{"text": "ГДЕ ОШИБКА", "accent": False, "size": "small"}, {"text": "ПРИЧИНА", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.81, "lines": [{"text": "И ИСПРАВЛЕНИЯ", "accent": False, "size": "small"}, {"text": "НАЗВАНЫ ПРЯМО", "accent": True, "size": "small"}]},
    {"start": 16.11, "end": 17.16, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.16, "end": 17.964, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.59, "end": 6.36}, {"start": 8.04, "end": 10.35}, {"start": 13.23, "end": 15.81}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (Рома, 15.746s): recognizing Russian homonyms by picture but
# struggling to name them by meaning -- meaning is what's actually
# needed, and the app's memory games repeat homonym meanings in pairs
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАЮ КАРТИНКУ", "НЕ ЗНАЧЕНИЕ"], "end": 1.83}
d_cards = [
    {"start": 1.83, "end": 3.42, "lines": [{"text": "ОМОНИМЫ В ЕГЭ", "accent": False, "size": "small"}, {"text": "ЛУК КОСА КЛЮЧ", "accent": True, "size": "small"}]},
    {"start": 3.63, "end": 4.50, "lines": [{"text": "Я УЗНАЮ", "accent": False, "size": "small"}, {"text": "ПО КАРТИНКЕ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 5.82, "lines": [{"text": "НО НАЗЫВАЮ", "accent": False, "size": "small"}, {"text": "ПО ЗНАЧЕНИЮ", "accent": True, "size": "small"}]},
    {"start": 6.00, "end": 8.10, "lines": [{"text": "С ТРУДОМ НУЖНЫ", "accent": False, "size": "small"}, {"text": "ЗНАЧЕНИЯ А НЕ КАРТИНКИ", "accent": True, "size": "small"}]},
    {"start": 8.46, "end": 9.96, "lines": [{"text": "В ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ ЯЗЫКУ", "accent": True, "size": "small"}]},
    {"start": 10.20, "end": 11.28, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 11.46, "end": 13.65, "lines": [{"text": "ГДЕ ЗНАЧЕНИЯ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ ПАРАМИ", "accent": True, "size": "small"}]},
    {"start": 13.92, "end": 14.94, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.94, "end": 15.746, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.63, "end": 8.10}, {"start": 11.46, "end": 13.65}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (mother, 18.967s): a daughter understands how a bank account
# works from one real card example, but social studies ЕГЭ asks for bank
# functions as a full list -- the app's memory games reinforce bank
# functions through games, not just one example
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОДИН ПРИМЕР", "ЭТО НЕ СПИСОК"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.48, "lines": [{"text": "ДОЧЬ ПОНИМАЕТ", "accent": False, "size": "small"}, {"text": "КАК РАБОТАЕТ БАНК", "accent": True, "size": "small"}]},
    {"start": 4.17, "end": 5.34, "lines": [{"text": "А В ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 5.49, "end": 7.02, "lines": [{"text": "СПРАШИВАЮТ ПРО", "accent": False, "size": "small"}, {"text": "ФУНКЦИИ БАНКОВ", "accent": True, "size": "small"}]},
    {"start": 7.62, "end": 8.67, "lines": [{"text": "ПРИМЕР С КАРТОЙ", "accent": False, "size": "small"}, {"text": "ХОРОШ", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 10.44, "lines": [{"text": "НО ФУНКЦИИ НУЖНО", "accent": False, "size": "small"}, {"text": "ЗНАТЬ СПИСКОМ", "accent": True, "size": "small"}]},
    {"start": 11.07, "end": 12.66, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 12.87, "end": 14.16, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.37, "end": 16.44, "lines": [{"text": "ГДЕ ФУНКЦИИ", "accent": False, "size": "small"}, {"text": "БАНКОВ ЗАКРЕПЛЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 17.01, "end": 17.85, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.85, "end": 18.967, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.49, "end": 7.02}, {"start": 8.85, "end": 10.44}, {"start": 14.37, "end": 16.44}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 14.560s): a friend buys a thousand-task collection
# and shelves it to avoid flipping through it -- the narrator's own
# "shelf" is a screen where any task opens with one tap, same as the
# app's FIPI bank
# ---------------------------------------------------------------------------
f_intro = {"lines": ["КУПИЛ И НЕ", "ОТКРЫЛ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "НА ТЫСЯЧУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.88, "end": 4.17, "lines": [{"text": "И КРАСИВО", "accent": False, "size": "small"}, {"text": "ПОСТАВИЛ НА ПОЛКУ", "accent": True, "size": "small"}]},
    {"start": 4.29, "end": 5.31, "lines": [{"text": "ЧТОБЫ НЕ", "accent": False, "size": "small"}, {"text": "ЛИСТАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.31, "end": 6.51, "lines": [{"text": "МОЯ ПОЛКА", "accent": False, "size": "small"}, {"text": "ЭТО ЭКРАН", "accent": True, "size": "big"}]},
    {"start": 6.63, "end": 7.59, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 7.74, "end": 8.55, "lines": [{"text": "ОДНИМ", "accent": False, "size": "small"}, {"text": "КАСАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 9.55, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.55, "end": 10.37, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.44, "end": 11.79, "lines": [{"text": "ГДЕ ТЫСЯЧИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ ОТКРЫВАЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 11.97, "end": 12.78, "lines": [{"text": "ОДНИМ", "accent": False, "size": "small"}, {"text": "КАСАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 12.93, "end": 13.76, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 13.76, "end": 14.560, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.53, "end": 2.67}, {"start": 5.31, "end": 6.51}, {"start": 10.44, "end": 11.79}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
