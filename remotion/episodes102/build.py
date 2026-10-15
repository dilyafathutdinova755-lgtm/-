#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-FIFTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes102/.

Four returning hosts, no new faces: "teen boy on couch" / bookshelf+
plant+window room (a, f), "blonde in cream sweater" / desk+lamp+plant+
notebook room (b, g, i), "blue-shirt brunette" / THE SMITHS poster +
"ЕГЭ 2026" sticky note room (c, d, e), "mother" / bookshelf+doorway
apartment with small framed picture (h).

Sub-themes: a formula that looked like it had to be guessed until the
breakdown showed it derived in two lines, breakdowns being for everyone
not just weak students, beating a hundred-level phone game in a month
while a year of exam vocabulary went nowhere, a seven-minute voice
message explaining a task that can't be skimmed or rewound to one line,
an "I solved hundreds of problems" classmate who can't say which ones,
an upstairs neighbor's 9am renovation turning study time into noise,
remembering every release date of a favorite show but not a single
reign date for history, a daughter who spends longer choosing a task
than solving it, and the first snow of the year pulling attention out
the window for half an hour.
"""
import json

REAL_DURATION = {
    "a": 16.98, "b": 18.06, "c": 26.25,
    "d": 23.16, "e": 20.91, "f": 15.24,
    "g": 20.94, "h": 16.98, "i": 19.41,
}
SOURCE_FILE = {
    "a": "gbncbbgbbdzbdxf", "b": "gfndznfhgfdg", "c": "ghdfhdgdgsfgdsg",
    "d": "gmfdmnmfnbhf", "e": "gvmndjfhrxhndghhg", "f": "jgxfhdrsfnbvchg",
    "g": "mgxfn.djfb", "h": "mxcngbgvn.xdfg", "i": "vdhfshrdhdrgg",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {"уровне": "уровней"},
    "d": {},
    "e": {},
    "f": {},
    "g": {"держится": "держатся"},
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
    with open(f"../asr_coffee123_55/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy on couch, 16.98s): a formula that looked like it
# had to be guessed turns out to derive in two lines in the breakdown --
# the derivation sticks better than the formula itself
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ФОРМУЛУ НУЖНО УГАДАТЬ", "А МОЖНО ВЫВЕСТИ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "ФОРМУЛУ ЕГЭ", "accent": False, "size": "small"}, {"text": "НУЖНО УГАДАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "А В РАЗБОРЕ", "accent": False, "size": "small"}, {"text": "ОНА ВЫВОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.20, "lines": [{"text": "ЗА ДВЕ", "accent": False, "size": "small"}, {"text": "СТРОКИ", "accent": True, "size": "big"}]},
    {"start": 6.20, "end": 7.80, "lines": [{"text": "ВЫВОД", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЕТСЯ ЛУЧШЕ", "accent": True, "size": "small"}]},
    {"start": 7.80, "end": 9.40, "lines": [{"text": "ТЕПЕРЬ СМОТРЮ", "accent": False, "size": "small"}, {"text": "ОТКУДА ОНА", "accent": True, "size": "big"}]},
    {"start": 9.40, "end": 11.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 12.60, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 14.20, "lines": [{"text": "ФОРМУЛЫ НЕ ПАДАЮТ", "accent": False, "size": "small"}, {"text": "С НЕБА", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 15.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 16.98, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 6.24, "end": 7.11}, {"start": 8.97, "end": 9.84}, {"start": 13.35, "end": 14.88}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde cream sweater, 18.06s): breakdowns aren't only for
# weak students -- strong students read them too, because they know
# knowing where to look for a mistake is the actual skill
# ---------------------------------------------------------------------------
b_intro = {"lines": ["РАЗБОРЫ ДЛЯ СЛАБЫХ", "А Я ЧИТАЮ ИХ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ПОДРУГА СЧИТАЕТ", "accent": False, "size": "small"}, {"text": "РАЗБОРЫ ДЛЯ СЛАБЫХ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "А Я ЧИТАЮ", "accent": False, "size": "small"}, {"text": "ИХ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ЧТОБЫ СТАТЬ", "accent": False, "size": "small"}, {"text": "СИЛЬНЕЕ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "СИЛЬНЫЕ ТОЖЕ", "accent": False, "size": "small"}, {"text": "ОШИБАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "ПРОСТО ЗНАЮТ", "accent": False, "size": "small"}, {"text": "ГДЕ ИСКАТЬ", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "ПРИЧИНУ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "ПРИЧИНА ОШИБКИ", "accent": False, "size": "small"}, {"text": "НАЗВАНА ПРЯМО", "accent": True, "size": "small"}]},
    {"start": 16.20, "end": 17.00, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.00, "end": 18.06, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.73, "end": 3.39}, {"start": 5.58, "end": 8.49}, {"start": 14.91, "end": 15.57}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 26.25s): beating a hundred-level phone
# game in a month while a year of exam vocabulary goes nowhere isn't
# laziness -- the game is built to keep you playing, the textbook isn't
# ---------------------------------------------------------------------------
c_intro = {"lines": ["СТО УРОВНЕЙ ИГРЫ", "ЗА МЕСЯЦ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ИГРУ НА СТО", "accent": False, "size": "small"}, {"text": "УРОВНЕЙ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ПРОШЛА", "accent": False, "size": "small"}, {"text": "ЗА МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "А СЛОВА ЕГЭ", "accent": False, "size": "small"}, {"text": "НЕ ЗА ГОД", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.80, "lines": [{"text": "ЗНАЧИТ ДЕЛО", "accent": False, "size": "small"}, {"text": "НЕ В ЛЕНИ", "accent": True, "size": "big"}]},
    {"start": 8.80, "end": 11.00, "lines": [{"text": "ИГРА ПРИДУМАНА", "accent": False, "size": "small"}, {"text": "ТАК ЧТО ХОЧЕТСЯ ИГРАТЬ", "accent": True, "size": "small"}]},
    {"start": 11.00, "end": 13.20, "lines": [{"text": "А УЧЕБНИК", "accent": False, "size": "small"}, {"text": "ТАК НЕ УМЕЕТ", "accent": True, "size": "small"}]},
    {"start": 13.20, "end": 15.00, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.80, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.60, "lines": [{"text": "УРОВНИ", "accent": False, "size": "small"}, {"text": "УСТРОЕНЫ ТАКЖЕ", "accent": True, "size": "small"}]},
    {"start": 18.60, "end": 20.40, "lines": [{"text": "А СЛОВА", "accent": False, "size": "small"}, {"text": "ОСТАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 20.40, "end": 22.00, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 22.00, "end": 24.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 24.40, "end": 26.25, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.37, "end": 3.15}, {"start": 5.94, "end": 6.84}, {"start": 21.93, "end": 23.25}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 23.16s): a seven-minute voice message
# explaining a task can't be skimmed or rewound to one line -- by the
# end the beginning is already gone; the app's text breakdown can be both
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ГОЛОСОВОЕ НА СЕМЬ МИНУТ", "ЗАБЫЛА НАЧАЛО"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ПОДРУГА ПРИСЛАЛА", "accent": False, "size": "small"}, {"text": "ГОЛОСОВОЕ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "НА СЕМЬ МИНУТ", "accent": False, "size": "small"}, {"text": "ПРО ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "К КОНЦУ Я", "accent": False, "size": "small"}, {"text": "ЗАБЫЛА НАЧАЛО", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.80, "lines": [{"text": "ЕГО НЕЛЬЗЯ", "accent": False, "size": "small"}, {"text": "ПРОБЕЖАТЬ ГЛАЗАМИ", "accent": True, "size": "small"}]},
    {"start": 8.80, "end": 10.60, "lines": [{"text": "МНЕ НЕ", "accent": False, "size": "small"}, {"text": "ПОДХОДИТ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.40, "lines": [{"text": "ХОЧУ ВЕРНУТЬСЯ", "accent": False, "size": "small"}, {"text": "К СТРОКЕ", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 14.60, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 18.00, "lines": [{"text": "МОЖНО ПРОБЕЖАТЬ", "accent": False, "size": "small"}, {"text": "ГЛАЗАМИ", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 20.00, "lines": [{"text": "И ВЕРНУТЬСЯ", "accent": False, "size": "small"}, {"text": "К ЛЮБОЙ СТРОКЕ", "accent": True, "size": "small"}]},
    {"start": 20.00, "end": 22.00, "lines": [{"text": "ССЫЛКА НА Г", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.00, "end": 23.16, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.19, "end": 6.57}, {"start": 8.07, "end": 9.69}, {"start": 19.23, "end": 20.34}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 20.91s): "I solved hundreds of
# problems" means nothing if you can't say which ones -- random practice
# doesn't close gaps, picking by number and topic does
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ХВАСТАЕТСЯ СОТНЯМИ ЗАДАНИЙ", "НО КАКИХ НЕ ЗНАЕТ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ОДНОКЛАССНИК", "accent": False, "size": "small"}, {"text": "ХВАСТАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "РЕШИЛ ЗА ЛЕТО", "accent": False, "size": "small"}, {"text": "СОТНИ ЗАДАНИЙ", "accent": True, "size": "small"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НО КАКИХ", "accent": False, "size": "small"}, {"text": "ОТВЕЧАЕТ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "РАЗНЫХ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНЫХ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ЭТО НЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЕТ ПРОБЕЛЫ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.80, "lines": [{"text": "МНЕ НУЖНЫ", "accent": False, "size": "small"}, {"text": "ИМЕННО ТЕ", "accent": True, "size": "big"}]},
    {"start": 11.80, "end": 13.60, "lines": [{"text": "ГДЕ Я", "accent": False, "size": "small"}, {"text": "ОШИБАЮСЬ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 15.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.20, "end": 16.80, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.40, "lines": [{"text": "ЗАДАНИЕ ВЫБИРАЕШЬ", "accent": False, "size": "small"}, {"text": "ПО НОМЕРУ И ТЕМЕ", "accent": True, "size": "small"}]},
    {"start": 18.40, "end": 19.60, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.60, "end": 20.91, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.32, "end": 1.77}, {"start": 8.43, "end": 10.02}, {"start": 12.21, "end": 13.08}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 15.24s): an upstairs neighbor's 9am
# renovation turns study time into noise -- solving before the drill
# starts fits three or four tasks from the app's FIPI bank into that window
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СОСЕД НАЧИНАЕТ РЕМОНТ", "РОВНО В ДЕВЯТЬ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "СОСЕД СВЕРХУ", "accent": False, "size": "small"}, {"text": "РЕМОНТ", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "РОВНО В", "accent": False, "size": "small"}, {"text": "ДЕВЯТЬ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "ВРЕМЯ ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПРЕВРАЩАЕТСЯ В ШУМ", "accent": True, "size": "small"}]},
    {"start": 6.40, "end": 8.00, "lines": [{"text": "РЕШАЮ", "accent": False, "size": "small"}, {"text": "ДО ДЕВЯТИ", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "ПОКА", "accent": False, "size": "small"}, {"text": "ДРЕЛЬ МОЛЧИТ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 12.40, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 13.60, "lines": [{"text": "ТРИ ЧЕТЫРЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 14.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 15.24, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.31, "end": 2.85}, {"start": 4.56, "end": 5.64}, {"start": 12.21, "end": 13.08}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (blonde cream sweater, 20.94s): remembering every release
# date of a favorite show but not a single reign date for history isn't
# a memory problem -- it's missing a hook, and a game can be the hook
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ПОМНЮ ДАТЫ СЕРИАЛА", "НЕ ДАТЫ КНЯЗЕЙ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ПОМНЮ ДАТЫ", "accent": False, "size": "small"}, {"text": "ВСЕХ СЕРИЙ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ЛЮБИМОГО", "accent": False, "size": "small"}, {"text": "СЕРИАЛА", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.80, "lines": [{"text": "А ДАТЫ ПРАВЛЕНИЯ", "accent": False, "size": "small"}, {"text": "КНЯЗЕЙ ДЛЯ ЕГЭ", "accent": True, "size": "small"}]},
    {"start": 6.80, "end": 8.60, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ДЕРЖАТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 10.40, "lines": [{"text": "ПАМЯТЬ", "accent": False, "size": "small"}, {"text": "НОРМАЛЬНАЯ", "accent": True, "size": "big"}]},
    {"start": 10.40, "end": 12.00, "lines": [{"text": "НЕ ХВАТАЕТ", "accent": False, "size": "small"}, {"text": "ПОВОДА", "accent": True, "size": "big"}]},
    {"start": 12.00, "end": 13.20, "lines": [{"text": "А ПОВОД", "accent": False, "size": "small"}, {"text": "МОЖЕТ ДАТЬ ИГРА", "accent": True, "size": "small"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.40, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.40, "lines": [{"text": "ДАТЫ КНЯЗЕЙ", "accent": False, "size": "small"}, {"text": "ИДУТ КАК СЕРИИ", "accent": True, "size": "small"}]},
    {"start": 18.40, "end": 19.60, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.60, "end": 20.94, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 6.84, "end": 7.32}, {"start": 9.75, "end": 10.65}, {"start": 18.18, "end": 18.66}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (mother, 16.98s): a daughter who spends longer choosing
# which task to do than actually solving it starts picking by topic
# instead -- the app lets a task be picked by topic directly
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ВЫБИРАЕТ ЗАДАНИЕ ДОЛЬШЕ", "ЧЕМ РЕШАЕТ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ДОЧЬ ТРАТИТ", "accent": False, "size": "small"}, {"text": "НА ВЫБОР ЗАДАНИЯ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "БОЛЬШЕ ВРЕМЕНИ", "accent": False, "size": "small"}, {"text": "ЧЕМ НА РЕШЕНИЕ", "accent": True, "size": "small"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "Я ПРЕДЛОЖИЛА", "accent": False, "size": "small"}, {"text": "ВЫБИРАТЬ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "БЕРЕТ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "С ТОЙ ТЕМЫ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.80, "lines": [{"text": "ЧТО ИДЕТ", "accent": False, "size": "small"}, {"text": "ХУЖЕ ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 11.80, "end": 13.40, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.40, "end": 15.00, "lines": [{"text": "ЗАДАНИЕ ВЫБИРАЕШЬ", "accent": False, "size": "small"}, {"text": "ПО ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 15.80, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.80, "end": 16.98, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 2.70, "end": 3.27}, {"start": 5.22, "end": 6.57}, {"start": 8.64, "end": 10.08}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (blonde cream sweater, 19.41s): the first snow of the year
# pulls attention out the window for half an hour -- the window isn't
# going anywhere, but ten minutes on a task is doable even on that day
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ПЕРВЫЙ СНЕГ", "ПОЛЧАСА СМОТРЕЛА В ОКНО"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ПЕРВЫЙ СНЕГ", "accent": False, "size": "small"}, {"text": "В ОКТЯБРЕ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ВМЕСТО ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОЛЧАСА", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "СМОТРЕЛА", "accent": False, "size": "small"}, {"text": "В ОКНО", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.00, "lines": [{"text": "ОКНО НИКУДА", "accent": False, "size": "small"}, {"text": "НЕ ДЕНЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "А ДЕСЯТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "НАД ЗАДАНИЕМ", "accent": True, "size": "small"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "МОЖНО НАЙТИ", "accent": False, "size": "small"}, {"text": "ДАЖЕ В ТАКОЙ ДЕНЬ", "accent": True, "size": "small"}]},
    {"start": 11.20, "end": 13.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.60, "lines": [{"text": "ДЕСЯТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "СКЛАДЫВАЮТСЯ В НЕДЕЛЮ", "accent": True, "size": "small"}]},
    {"start": 16.60, "end": 17.80, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 19.41, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.22, "end": 4.14}, {"start": 5.64, "end": 8.28}, {"start": 15.18, "end": 16.65}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
