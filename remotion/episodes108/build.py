#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTY-FIRST 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes108/.

Four returning hosts, no new faces: "teen boy on couch" / bookshelf+plant+
window room (a, g), "blonde in cream sweater" / desk+lamp+plant+notebook
room (b, c, e, h), "blue-shirt brunette" / THE SMITHS poster + "ЕГЭ 2026"
sticky note room (d, i), "mother" / bookshelf+doorway apartment with small
framed picture (f).

Sub-themes: switching from solving ЕГЭ only on "even days" (too few of
them) to one task every day, no parity tracking needed; "-ить"/"-еть"
exception verbs no longer apply here -- this batch's abbreviation theme
is for essay breakdowns, where abbreviations save the author's space but
cost the reader their train of thought; a school project crowding out
ЕГЭ prep for a week, solved by keeping one task a day going regardless;
solving a task in two lines only to find the official breakdown needed
six, because an unnamed assumption is a risk; remembering Yaroslav the
Wise by one nickname and one document, which is too little for a real
answer; a personal study schedule a classmate's parents ask to copy,
held together by one simple rule -- one task a day; conflict types for
social studies needing one example each, not just one example overall;
a six-ruler, thirty-seven-year blank spot after Peter I nicknamed "the
era of palace coups"; and a spare phone charger always in the backpack
but no spare plan for low-motivation days, fixed by defaulting to the
single shortest task.

Card/intro text was verified against the actual Golos Text Black render
(PIL getbbox at each line's real font size, small lines included) before
being written below -- consistent with the process that caught overflow
bugs in batches 58-59.

ASR notes: episode f had two merge artifacts ("правере" for "правиле",
and "гдеодно" merging "где"+"одно") fixed via FIXES (the second by
dropping "одно", keeping the clause's connector -- FIXES is 1:1
substitution only, can't split a merged token in two). Episode g had two
merge/garble artifacts ("эгео" for ЕГЭ, "пообществознанию" merging
"по"+"обществознанию") left unfixed per policy -- phonetic ЕГЭ variants
and un-splittable merges are routed around via clean hand-authored card
text rather than forced through FIXES. Episode i had "здание" (building)
for "задание" (task), a clear one-word grammar/meaning fix.
"""
import json

REAL_DURATION = {
    "a": 15.084, "b": 21.676, "c": 19.820,
    "d": 22.764, "e": 20.802, "f": 19.202,
    "g": 23.426, "h": 17.880, "i": 20.226,
}
SOURCE_FILE = {
    "a": "dggnshjngafg", "b": "fdhegb.dhrfg", "c": "fdzgbzhrdgtsgg",
    "d": "fgzsgggfrgf", "e": "gfdsgbgfdxgvgvf", "f": "gfggdgdgfd",
    "g": "gfzdhghnjeagzrz", "h": "gjahdfdsgdfg", "i": "nfdhbhdggd",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {},
    "d": {},
    "e": {},
    "f": {"правере": "правиле", "гдеодно": "где"},
    "g": {},
    "h": {},
    "i": {"здание": "задание"},
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
    with open(f"../asr_coffee123_61/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy on couch, 15.084s): switching from solving ЕГЭ only
# on "even days" (too few of them) to one task every day -- no parity
# tracking needed, and the app's FIPI bank gives exactly one task a day
# with no calendar required either
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЧЕТНЫХ ДНЕЙ", "НЕ ХВАТАЕТ"], "end": 1.74}
a_cards = [
    {"start": 1.74, "end": 3.15, "lines": [{"text": "ЕГЭ ТОЛЬКО ПО", "accent": False, "size": "small"}, {"text": "ЧЕТНЫМ ДНЯМ", "accent": True, "size": "small"}]},
    {"start": 3.15, "end": 4.17, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "ПОНЯЛ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 5.34, "lines": [{"text": "ЧЕТНЫХ ДНЕЙ", "accent": False, "size": "small"}, {"text": "МАЛО", "accent": True, "size": "big"}]},
    {"start": 5.34, "end": 6.48, "lines": [{"text": "ТЕПЕРЬ РЕШАЮ", "accent": False, "size": "small"}, {"text": "ПО ОДНОМУ", "accent": True, "size": "big"}]},
    {"start": 6.48, "end": 7.50, "lines": [{"text": "ЗАДАНИЮ КАЖДЫЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.61, "lines": [{"text": "И ЧЕТНОСТЬ", "accent": False, "size": "small"}, {"text": "НЕ НУЖНА", "accent": True, "size": "big"}]},
    {"start": 8.61, "end": 9.57, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.57, "end": 10.59, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.59, "end": 11.70, "lines": [{"text": "ГДЕ ОДНО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ В ДЕНЬ", "accent": True, "size": "small"}]},
    {"start": 11.70, "end": 13.05, "lines": [{"text": "НАБИРАЕТСЯ БЕЗ", "accent": False, "size": "small"}, {"text": "КАЛЕНДАРЯ", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.25, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 15.084, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.44, "end": 5.34}, {"start": 7.92, "end": 8.61}, {"start": 12.51, "end": 13.05}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde in cream sweater, 21.676s): abbreviations in task
# breakdowns save the author's space, but cost the reader their train of
# thought -- the app's text breakdown writes words out in full instead
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СОКРАЩЕНИЯ", "ПУТАЮТ МЫСЛИ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.03, "lines": [{"text": "У РАЗБОРОВ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ВРАГ", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 4.44, "lines": [{"text": "ЭТОТ ВРАГ", "accent": False, "size": "small"}, {"text": "СОКРАЩЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 4.44, "end": 5.85, "lines": [{"text": "ТО ЕСТЬ", "accent": False, "size": "small"}, {"text": "СМОТРИ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 7.62, "lines": [{"text": "СМОТРИ ЗА", "accent": False, "size": "small"}, {"text": "КОТОРЫМИ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.85, "lines": [{"text": "Я ТЕРЯЮ", "accent": False, "size": "small"}, {"text": "ХОД МЫСЛИ", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 10.65, "lines": [{"text": "СОКРАЩЕНИЕ", "accent": False, "size": "small"}, {"text": "ЭКОНОМИТ", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 11.52, "lines": [{"text": "МЕСТО", "accent": False, "size": "small"}, {"text": "АВТОРУ", "accent": True, "size": "big"}]},
    {"start": 11.52, "end": 12.84, "lines": [{"text": "А НЕ ВРЕМЯ", "accent": False, "size": "small"}, {"text": "ЧИТАТЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 12.84, "end": 14.40, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 16.35, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.35, "end": 17.73, "lines": [{"text": "ГДЕ СЛОВА", "accent": False, "size": "small"}, {"text": "НАПИСАНЫ", "accent": True, "size": "big"}]},
    {"start": 17.73, "end": 19.14, "lines": [{"text": "ПОЛНОСТЬЮ БЕЗ", "accent": False, "size": "small"}, {"text": "СОКРАЩЕНИЙ", "accent": True, "size": "big"}]},
    {"start": 19.14, "end": 20.85, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.85, "end": 21.676, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 7.17, "end": 8.85}, {"start": 16.59, "end": 19.14}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blonde in cream sweater, 19.820s): a week-long school
# project crowds out ЕГЭ prep, solved by keeping one task a day going
# regardless -- the app's FIPI bank makes that one task not get in the
# project's way
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПРОЕКТ ПРОТИВ", "ЕГЭ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 2.88, "lines": [{"text": "НАМ ЗАДАЛИ", "accent": False, "size": "small"}, {"text": "ПРОЕКТ", "accent": True, "size": "big"}]},
    {"start": 2.88, "end": 4.14, "lines": [{"text": "НА НЕДЕЛЮ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.14, "end": 5.67, "lines": [{"text": "ОТОДВИНУЛСЯ НА", "accent": False, "size": "small"}, {"text": "ВТОРОЙ ПЛАН", "accent": True, "size": "big"}]},
    {"start": 5.67, "end": 7.08, "lines": [{"text": "ХОТЯ ВАЖНЕЕ", "accent": False, "size": "small"}, {"text": "ИМЕННО ОН", "accent": True, "size": "big"}]},
    {"start": 7.08, "end": 8.31, "lines": [{"text": "ПРОЕКТ", "accent": False, "size": "small"}, {"text": "ЗАКОНЧИТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.31, "end": 9.57, "lines": [{"text": "В ПЯТНИЦУ А", "accent": False, "size": "small"}, {"text": "ЕГЭ ОСТАНЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 9.57, "end": 10.77, "lines": [{"text": "ПОЭТОМУ НА", "accent": False, "size": "small"}, {"text": "НЕГО", "accent": True, "size": "big"}]},
    {"start": 10.77, "end": 12.48, "lines": [{"text": "Я ОСТАВЛЯЮ ПО", "accent": False, "size": "small"}, {"text": "ОДНОМУ В ДЕНЬ", "accent": True, "size": "small"}]},
    {"start": 13.23, "end": 14.67, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 16.29, "lines": [{"text": "ФИПИ ГДЕ", "accent": False, "size": "small"}, {"text": "ОДНО ЗАДАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.29, "end": 17.40, "lines": [{"text": "НЕ МЕШАЕТ", "accent": False, "size": "small"}, {"text": "ПРОЕКТУ", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.90, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 19.820, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.35, "end": 5.67}, {"start": 8.73, "end": 9.57}, {"start": 16.47, "end": 17.40}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 22.764s): a task solved in two lines
# turns out to need six in the official breakdown -- an unnamed
# assumption is a risk, and the app's text breakdown names assumptions
# directly
# ---------------------------------------------------------------------------
d_intro = {"lines": ["НЕНАЗВАННОЕ", "ЭТО РИСК"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 2.76, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ДВЕ СТРОКИ", "accent": True, "size": "big"}]},
    {"start": 3.18, "end": 5.16, "lines": [{"text": "А В РАЗБОРЕ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦА ИЗ ШЕСТИ", "accent": True, "size": "small"}]},
    {"start": 5.91, "end": 7.95, "lines": [{"text": "И ПОНЯЛА ЧТО", "accent": False, "size": "small"}, {"text": "МОИ ДВЕ СТРОКИ", "accent": True, "size": "small"}]},
    {"start": 8.22, "end": 9.48, "lines": [{"text": "ДЕРЖАЛИСЬ НА", "accent": False, "size": "small"}, {"text": "ДОПУЩЕНИИ", "accent": True, "size": "big"}]},
    {"start": 10.23, "end": 11.43, "lines": [{"text": "ДОПУЩЕНИЕ", "accent": False, "size": "small"}, {"text": "ДОПУСТИМО", "accent": True, "size": "big"}]},
    {"start": 11.64, "end": 12.45, "lines": [{"text": "ПОКА ЕГО", "accent": False, "size": "small"}, {"text": "НАЗВАЛИ", "accent": True, "size": "big"}]},
    {"start": 12.93, "end": 15.06, "lines": [{"text": "А БЕЗ НАЗВАНИЯ", "accent": False, "size": "small"}, {"text": "ПРЕВРАЩАЕТСЯ В РИСК", "accent": True, "size": "small"}]},
    {"start": 15.84, "end": 16.65, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.74, "end": 18.36, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 18.72, "end": 20.22, "lines": [{"text": "ГДЕ ДОПУЩЕНИЯ", "accent": False, "size": "small"}, {"text": "НАЗВАНЫ ПРЯМО", "accent": True, "size": "small"}]},
    {"start": 20.82, "end": 21.90, "lines": [{"text": "ССЫЛКА НА Г", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.90, "end": 22.764, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.18, "end": 5.16}, {"start": 8.22, "end": 9.48}, {"start": 12.93, "end": 15.06}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde in cream sweater, 20.802s): Yaroslav the Wise reduced
# to one nickname and one document is too little for a real history ЕГЭ
# answer -- the app's memory games spread his reign across events and
# documents instead
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОДНО ПРОЗВИЩЕ", "ЭТО НЕ ОТВЕТ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 2.76, "lines": [{"text": "ПРО ЯРОСЛАВА", "accent": False, "size": "small"}, {"text": "МУДРОГО", "accent": True, "size": "big"}]},
    {"start": 2.76, "end": 3.63, "lines": [{"text": "В ИСТОРИИ Я", "accent": False, "size": "small"}, {"text": "ПОМНЮ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.65, "lines": [{"text": "ПРОЗВИЩЕ И", "accent": False, "size": "small"}, {"text": "РУССКУЮ ПРАВДУ", "accent": True, "size": "small"}]},
    {"start": 5.16, "end": 6.21, "lines": [{"text": "А ОСТАЛЬНОЕ", "accent": False, "size": "small"}, {"text": "ТЕРЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.58, "lines": [{"text": "ПРОЗВИЩЕ И", "accent": False, "size": "small"}, {"text": "ОДИН ДОКУМЕНТ", "accent": True, "size": "small"}]},
    {"start": 8.97, "end": 10.14, "lines": [{"text": "СЛИШКОМ МАЛО", "accent": False, "size": "small"}, {"text": "ДЛЯ ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 10.98, "end": 12.36, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.92, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.34, "end": 15.99, "lines": [{"text": "ГДЕ ПРАВЛЕНИЕ", "accent": False, "size": "small"}, {"text": "ЯРОСЛАВА МУДРОГО", "accent": True, "size": "small"}]},
    {"start": 16.20, "end": 17.58, "lines": [{"text": "РАСКЛАДЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПО СОБЫТИЯМ", "accent": True, "size": "small"}]},
    {"start": 17.79, "end": 18.60, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ДОКУМЕНТАМ", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 19.82, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.82, "end": 20.802, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.16, "end": 6.21}, {"start": 8.97, "end": 10.14}, {"start": 14.34, "end": 15.99}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 19.202s): a daughter's personal ЕГЭ study schedule
# that a classmate's parents ask to copy, held together by one simple
# rule -- one task a day, same as the app's bank, which logs each day's
# task automatically
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЛИЧНЫЙ ГРАФИК", "СТАЛ ОБЩИМ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "СОБСТВЕННЫЙ ГРАФИК", "accent": False, "size": "small"}, {"text": "ПОДГОТОВКИ К ЕГЭ", "accent": True, "size": "small"}]},
    {"start": 3.66, "end": 5.94, "lines": [{"text": "КЛАССНЫЙ РУКОВОДИТЕЛЬ", "accent": False, "size": "small"}, {"text": "ПОПРОСИЛ КОПИЮ", "accent": True, "size": "small"}]},
    {"start": 6.51, "end": 8.55, "lines": [{"text": "НЕ ДУМАЛА ЧТО", "accent": False, "size": "small"}, {"text": "ВЫЗОВЕТ ИНТЕРЕС", "accent": True, "size": "small"}]},
    {"start": 8.94, "end": 10.56, "lines": [{"text": "НО ДЕРЖИТСЯ НА", "accent": False, "size": "small"}, {"text": "ПРОСТОМ ПРАВИЛЕ", "accent": True, "size": "small"}]},
    {"start": 10.89, "end": 11.82, "lines": [{"text": "ОДНО ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "В ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 12.45, "end": 13.26, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.32, "end": 14.13, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.39, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "В ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 15.57, "end": 16.83, "lines": [{"text": "ЗАПИСЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "АВТОМАТИЧЕСКИ", "accent": True, "size": "small"}]},
    {"start": 17.40, "end": 18.40, "lines": [{"text": "ССЫЛКА НА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.40, "end": 19.202, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 6.51, "end": 7.86}, {"start": 8.94, "end": 10.56}, {"start": 15.57, "end": 16.83}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (teen boy on couch, 23.426s): one example of a conflict type
# for social studies ЕГЭ isn't enough -- each type needs its own, and the
# app's memory games match a fresh example to every conflict type
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ОДИН ПРИМЕР", "ЭТО МАЛО"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 2.70, "lines": [{"text": "Я ЗНАЮ ЧТО", "accent": False, "size": "small"}, {"text": "КОНФЛИКТЫ", "accent": True, "size": "big"}]},
    {"start": 2.70, "end": 3.57, "lines": [{"text": "БЫВАЮТ РАЗНЫХ", "accent": False, "size": "small"}, {"text": "ТИПОВ", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 4.50, "lines": [{"text": "НО ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 4.71, "end": 5.67, "lines": [{"text": "У МЕНЯ ОДИН", "accent": False, "size": "small"}, {"text": "ПРИМЕР", "accent": True, "size": "big"}]},
    {"start": 6.51, "end": 8.40, "lines": [{"text": "СПОР ЗА", "accent": False, "size": "small"}, {"text": "ПОСЛЕДНЕЕ МЕСТО", "accent": True, "size": "small"}]},
    {"start": 10.38, "end": 11.40, "lines": [{"text": "ОДНОГО ПРИМЕРА", "accent": False, "size": "small"}, {"text": "МАЛО", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 12.48, "lines": [{"text": "НУЖЕН СВОЙ", "accent": False, "size": "small"}, {"text": "ПРИМЕР", "accent": True, "size": "big"}]},
    {"start": 12.72, "end": 13.53, "lines": [{"text": "К КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ТИПУ", "accent": True, "size": "big"}]},
    {"start": 14.28, "end": 15.87, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 16.14, "end": 17.40, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 18.03, "end": 18.90, "lines": [{"text": "ГДЕ КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ТИПУ", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 20.73, "lines": [{"text": "КОНФЛИКТА ПОДБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "СВОЙ ПРИМЕР", "accent": True, "size": "big"}]},
    {"start": 21.48, "end": 22.59, "lines": [{"text": "ССЫЛКА НА Г", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.59, "end": 23.426, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 6.51, "end": 8.40}, {"start": 10.38, "end": 12.48}, {"start": 19.02, "end": 20.73}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blonde in cream sweater, 17.880s): a six-ruler, thirty-
# seven-year blank spot after Peter I nicknamed "the era of palace
# coups" -- the app's history memory games line the rulers of that era
# back up in order
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ШЕСТЬ ИМЕН", "ОДИН ПРОВАЛ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.27, "lines": [{"text": "В ЕГЭ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "У МЕНЯ ПРОВАЛ", "accent": True, "size": "small"}]},
    {"start": 3.48, "end": 4.98, "lines": [{"text": "ШЕСТЬ ПРАВИТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "ЗА ТРИДЦАТЬ СЕМЬ ЛЕТ", "accent": True, "size": "small"}]},
    {"start": 5.19, "end": 6.18, "lines": [{"text": "И Я НАЗОВУ", "accent": False, "size": "small"}, {"text": "ДВОИХ", "accent": True, "size": "big"}]},
    {"start": 6.69, "end": 8.04, "lines": [{"text": "ЭТА ЭПОХА", "accent": False, "size": "small"}, {"text": "ДВОРЦОВЫХ ПЕРЕВОРОТОВ", "accent": True, "size": "small"}]},
    {"start": 8.22, "end": 9.87, "lines": [{"text": "И ПРАВИТЕЛЕЙ НУЖНО", "accent": False, "size": "small"}, {"text": "РАССТАВИТЬ ПО ПОРЯДКУ", "accent": True, "size": "small"}]},
    {"start": 10.20, "end": 11.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 12.60, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 12.75, "end": 14.55, "lines": [{"text": "ГДЕ ПРАВИТЕЛИ", "accent": False, "size": "small"}, {"text": "ЭПОХИ ДВОРЦОВЫХ", "accent": True, "size": "small"}]},
    {"start": 14.70, "end": 15.72, "lines": [{"text": "ПЕРЕВОРОТОВ ПО ПОРЯДКУ", "accent": False, "size": "small"}, {"text": "РАССТАВЛЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 16.02, "end": 17.05, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.05, "end": 17.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.48, "end": 4.98}, {"start": 6.69, "end": 8.04}, {"start": 14.70, "end": 15.72}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (blue-shirt brunette, 20.226s): always a spare phone charger
# in the backpack, but no spare plan for low-motivation ЕГЭ days -- fixed
# by defaulting to the single shortest task, same as the app's FIPI bank
# entries findable in under a minute
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ЗАРЯДКА ЕСТЬ", "ПЛАНА НЕТ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 2.88, "lines": [{"text": "У МЕНЯ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ЗАПАСНАЯ ЗАРЯДКА", "accent": True, "size": "small"}]},
    {"start": 3.33, "end": 4.35, "lines": [{"text": "А ЗАПАСНОГО", "accent": False, "size": "small"}, {"text": "ПЛАНА", "accent": True, "size": "big"}]},
    {"start": 4.68, "end": 6.78, "lines": [{"text": "КОГДА НЕ ХОЧЕТСЯ", "accent": False, "size": "small"}, {"text": "ПЛАНА НЕ БЫЛО", "accent": True, "size": "small"}]},
    {"start": 7.59, "end": 8.46, "lines": [{"text": "ТЕПЕРЬ ПЛАН", "accent": False, "size": "small"}, {"text": "ТАКОЙ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.05, "lines": [{"text": "ЕСЛИ НЕ", "accent": False, "size": "small"}, {"text": "ХОЧЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 10.32, "end": 12.60, "lines": [{"text": "РЕШАЮ ОДНО", "accent": False, "size": "small"}, {"text": "САМОЕ КОРОТКОЕ", "accent": True, "size": "small"}]},
    {"start": 13.38, "end": 14.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 15.27, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.57, "end": 16.50, "lines": [{"text": "ГДЕ КОРОТКОЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 17.52, "lines": [{"text": "НАХОДИТСЯ ЗА", "accent": False, "size": "small"}, {"text": "МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.35, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.35, "end": 20.226, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 5.07, "end": 6.03}, {"start": 10.32, "end": 12.60}, {"start": 16.65, "end": 17.52}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
