#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-SEVENTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes104/.

Three returning hosts, no new faces: "Рома" / black Under Armour hoodie
(a, e, i), "blue-shirt brunette" / THE SMITHS poster + "ЕГЭ 2026" sticky
note room (b), "mother" / bookshelf+doorway apartment with small framed
picture (c, h), "teen boy on couch" / bookshelf+plant+window room (d, f, g).

Sub-themes: a friend who solves ЕГЭ dreading failure versus solving with
the opposite mindset, the real difference being how often the next task
gets opened; swapping open-ended revision sessions for a fixed
twenty-five-minute timer so stopping isn't a willpower decision; a
daughter coming back from a consultation in a good mood because
progress is visible in numbers, not just a feeling; a little sister's
drawings turned into a built-in reward after every task; eighteenth-
century treaties remembered only by city name, with the actual terms
forgotten; the word "note that" in a task breakdown working like a
highlighter for the one nonstandard step; embarrassment over declining
"five hundred" out loud fading only through repetition; a mother's
school-era explanation landing wrong because the language has moved on,
not the method; and a task breakdown that explains why each step
exists, not just how to do it.
"""
import json

REAL_DURATION = {
    "a": 15.60, "b": 19.82, "c": 17.154,
    "d": 18.12, "e": 17.218, "f": 18.20,
    "g": 20.631, "h": 20.162, "i": 17.73,
}
SOURCE_FILE = {
    "a": "bcgfhjbhcgcghh", "b": "chgkk.cdkytru", "c": "gdsfghhfjhghd",
    "d": "gkdjjdmfdjhhg", "e": "hcjgfmfxdngh", "f": "hjytmrmrjrjfjn",
    "g": "hmfjtjmhydrjyj", "h": "mhgmgjngngn", "i": "mnbvcghfjjhmcf",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {},
    "d": {},
    "e": {"о": "а"},
    "f": {"тренажери": "тренажере"},
    "g": {"егтренажере": "тренажере"},
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
    with open(f"../asr_coffee123_57/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (Рома, 15.60s): a friend solves ЕГЭ dreading "what if it
# doesn't work out" -- the real difference is just opening the next
# task more often, and the app's FIPI bank opens it right after the last
# ---------------------------------------------------------------------------
a_intro = {"lines": ["А ВДРУГ", "НЕ ПОЛУЧИТСЯ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДРУГ БОИТСЯ ЧТО НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИТСЯ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "А Я", "accent": False, "size": "small"}, {"text": "ПОЛУЧИТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "РАЗНИЦА В ТОМ", "accent": False, "size": "small"}, {"text": "ЧТО Я ЧАЩЕ", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.50, "lines": [{"text": "ОТКРЫВАЮ СЛЕДУЮЩЕЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.60, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.20, "lines": [{"text": "СЛЕДУЮЩЕЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЕТСЯ СРАЗУ", "accent": True, "size": "small"}]},
    {"start": 12.20, "end": 13.60, "lines": [{"text": "ПОСЛЕ", "accent": False, "size": "small"}, {"text": "ПРЕДЫДУЩЕГО", "accent": True, "size": "small"}]},
    {"start": 13.60, "end": 14.80, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 15.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.25, "end": 3.18}, {"start": 4.53, "end": 5.31}, {"start": 12.27, "end": 13.41}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blue-shirt brunette, 19.82s): open-ended revision until
# exhaustion gets swapped for a fixed twenty-five-minute timer -- the
# app's FIPI bank picks a task for that exact window, sorted by topic
# ---------------------------------------------------------------------------
b_intro = {"lines": ["НЕ ЗНАЮ", "КОГДА ХВАТИТ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "РАНЬШЕ РЕШАЛА ПОКА НЕ", "accent": False, "size": "small"}, {"text": "УСТАНУ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ТЕПЕРЬ СТАВЛЮ", "accent": False, "size": "small"}, {"text": "БУДИЛЬНИК", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НА ДВАДЦАТЬ ПЯТЬ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "БУДИЛЬНИК ЗВЕНИТ", "accent": False, "size": "small"}, {"text": "И ВСЕ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ОСТАНОВИТЬСЯ ПРОЩЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "РЕШАТЬ", "accent": True, "size": "big"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "КОГДА", "accent": False, "size": "small"}, {"text": "ХВАТИТ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 15.00, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.60, "lines": [{"text": "ЗАДАНИЕ НА ДВАДЦАТЬ ПЯТЬ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 17.80, "lines": [{"text": "ВЫБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПО ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 19.00, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.00, "end": 19.82, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.25, "end": 6.09}, {"start": 7.35, "end": 8.43}, {"start": 10.05, "end": 10.71}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 17.154s): a daughter comes back from a consultation
# in a good mood because progress is visible in numbers, not a feeling
# -- the app's FIPI bank shows weekly results broken down by topic
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЕСТЬ ЛИ", "ПРОГРЕСС"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДОЧЬ ВЕРНУЛАСЬ", "accent": False, "size": "small"}, {"text": "С КОНСУЛЬТАЦИИ", "accent": True, "size": "small"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "ПО ЕГЭ В ХОРОШЕМ", "accent": False, "size": "small"}, {"text": "НАСТРОЕНИИ", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "УЧИТЕЛЬ СКАЗАЛ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ПРОГРЕСС", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.50, "lines": [{"text": "ПРОГРЕСС ВИДЕН", "accent": False, "size": "small"}, {"text": "ПО ЦИФРАМ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.30, "lines": [{"text": "Я ПРЕДЛОЖИЛА ИХ", "accent": False, "size": "small"}, {"text": "ЗАПИСЫВАТЬ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.70, "lines": [{"text": "В КОНЦЕ", "accent": False, "size": "small"}, {"text": "НЕДЕЛИ", "accent": True, "size": "big"}]},
    {"start": 10.70, "end": 12.10, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.10, "end": 13.50, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 15.00, "lines": [{"text": "РЕЗУЛЬТАТЫ НЕДЕЛИ ВИДНЫ ПО", "accent": False, "size": "small"}, {"text": "ТЕМАМ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.30, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.30, "end": 17.154, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 6.39, "end": 6.99}, {"start": 8.19, "end": 9.09}, {"start": 12.99, "end": 13.77}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (teen boy on couch, 18.12s): a little sister's drawings
# become a built-in reward after every task -- the app's FIPI bank makes
# one task take about as long as one drawing
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СЕСТРА", "ОТВЛЕКАЕТ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "СЕСТРА СЕЛА РЯДОМ", "accent": False, "size": "small"}, {"text": "РИСОВАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "ПОКА Я", "accent": False, "size": "small"}, {"text": "РЕШАЮ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "ПОКАЗЫВАЕТ КАЖДЫЕ ПЯТЬ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.50, "lines": [{"text": "МЫ ДОГОВОРИЛИСЬ", "accent": False, "size": "small"}, {"text": "РИСУНОК", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.00, "lines": [{"text": "ПОСЛЕ КАЖДОГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.60, "lines": [{"text": "И ОБА СТАЛИ", "accent": False, "size": "small"}, {"text": "УСИДЧИВЕЕ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.60, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 15.00, "lines": [{"text": "ЗАДАНИЕ ЗАНИМАЕТ", "accent": False, "size": "small"}, {"text": "СТОЛЬКО ЖЕ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.20, "lines": [{"text": "СКОЛЬКО ОДИН", "accent": False, "size": "small"}, {"text": "РИСУНОК", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.30, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.30, "end": 18.12, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.92, "end": 5.70}, {"start": 10.32, "end": 10.80}, {"start": 15.45, "end": 15.99}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 17.218s): eighteenth-century treaties remembered
# only by city name, the actual terms forgotten -- the app's history
# games link treaties to cities and their conditions together
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ПОМНЮ ТОЛЬКО", "ГОРОДА"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДОГОВОРЫ ДВАДЦАТОГО", "accent": False, "size": "small"}, {"text": "ВЕКА", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "НА ЕГЭ ПО ИСТОРИИ ЗНАЮ ПО", "accent": False, "size": "small"}, {"text": "ГОРОДАМ", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "А ЧТО БЫЛО ПОМНЮ", "accent": False, "size": "small"}, {"text": "ПЛОХО", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.50, "lines": [{"text": "ГОРОД ЭТО", "accent": False, "size": "small"}, {"text": "АДРЕС", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.00, "lines": [{"text": "А СОДЕРЖАНИЕ НУЖНО", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.60, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.20, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.80, "lines": [{"text": "ДОГОВОРЫ СВЯЗЫВАЮТСЯ", "accent": False, "size": "small"}, {"text": "С ГОРОДАМИ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 17.218, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 7.62, "end": 8.73}, {"start": 10.23, "end": 10.80}, {"start": 13.38, "end": 14.28}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 18.20s): the word "note that" in a task
# breakdown works like a highlighter for the one nonstandard step -- the
# app's text breakdown highlights exactly those key spots separately
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ПРОПУСКАЮ", "СЛОВО ЗАМЕТИМ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "СЛОВО ЗАМЕТИМ", "accent": False, "size": "small"}, {"text": "В РАЗБОРЕ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "РАБОТАЕТ КАК ЖЕЛТЫЙ", "accent": False, "size": "small"}, {"text": "МАРКЕР", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "ПОСЛЕ НЕГО САМОЕ", "accent": False, "size": "small"}, {"text": "ВАЖНОЕ", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.50, "lines": [{"text": "ЭТО", "accent": False, "size": "small"}, {"text": "СИГНАЛ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.00, "lines": [{"text": "РАЗ ЗАМЕТИМ", "accent": False, "size": "small"}, {"text": "ЗНАЧИТ ШАГ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.60, "lines": [{"text": "НЕСТАНДАРТНЫЙ", "accent": False, "size": "small"}, {"text": "И ВАЖНЫЙ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.80, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.60, "lines": [{"text": "КЛЮЧЕВЫЕ МЕСТА ВЫДЕЛЕНЫ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 17.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.00, "end": 18.20, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 3.81, "end": 4.38}, {"start": 6.57, "end": 7.02}, {"start": 14.25, "end": 14.85}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (teen boy on couch, 20.631s): embarrassment over declining
# "five hundred" out loud fades only through repetition -- the app's
# Russian-language games repeat numeral declension round after round
# ---------------------------------------------------------------------------
g_intro = {"lines": ["СТЕСНЯЮСЬ", "ОТВЕЧАТЬ ВСЛУХ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "СКЛОНЕНИЕ", "accent": False, "size": "small"}, {"text": "ЧИСЛИТЕЛЬНЫХ", "accent": True, "size": "small"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "НА ЕГЭ ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЕДИНСТВЕННАЯ ТЕМА", "accent": True, "size": "small"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "ГДЕ Я", "accent": False, "size": "small"}, {"text": "СТЕСНЯЮСЬ", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.60, "lines": [{"text": "ПЯТИСТАМИ ИЛИ", "accent": False, "size": "small"}, {"text": "ПЯТЬЮСТАМИ", "accent": True, "size": "big"}]},
    {"start": 7.60, "end": 9.00, "lines": [{"text": "СТЕСНЕНИЕ ПРОХОДИТ", "accent": False, "size": "small"}, {"text": "КОГДА", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.60, "lines": [{"text": "ВЫБИРАЕШЬ ДЕСЯТЬ РАЗ", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.20, "lines": [{"text": "И ОН СТАНОВИТСЯ", "accent": False, "size": "small"}, {"text": "ПРИВЫЧНЫМ", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.80, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.40, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 17.20, "lines": [{"text": "СКЛОНЯЮТСЯ РАУНД ЗА", "accent": False, "size": "small"}, {"text": "РАУНДОМ", "accent": True, "size": "big"}]},
    {"start": 17.20, "end": 18.60, "lines": [{"text": "ПОКА ФОРМА НЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПИТСЯ", "accent": True, "size": "big"}]},
    {"start": 18.60, "end": 19.80, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.80, "end": 20.631, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 5.31, "end": 7.23}, {"start": 9.66, "end": 10.38}, {"start": 16.41, "end": 17.10}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (mother, 20.162s): a school-era explanation lands wrong
# because the language has moved on, not the method -- the app's text
# breakdown is written in today's language, no old-school formulas
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ОБЪЯСНЯЮ", "КАК УЧИЛИ МЕНЯ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ПОПРОБОВАЛА ОБЪЯСНИТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "КАК МЕНЯ УЧИЛИ В", "accent": False, "size": "small"}, {"text": "ШКОЛЕ", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.20, "lines": [{"text": "А ОНА СКАЗАЛА ОБЪЯСНЯЮТ", "accent": False, "size": "small"}, {"text": "ИНАЧЕ", "accent": True, "size": "big"}]},
    {"start": 6.20, "end": 7.70, "lines": [{"text": "СТАРЫЕ МЕТОДЫ", "accent": False, "size": "small"}, {"text": "НЕ ХУЖЕ", "accent": True, "size": "big"}]},
    {"start": 7.70, "end": 9.20, "lines": [{"text": "НО ЯЗЫК", "accent": False, "size": "small"}, {"text": "РАЗНЫЙ", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 10.90, "lines": [{"text": "НУЖЕН РАЗБОР", "accent": False, "size": "small"}, {"text": "СЕГОДНЯШНИМ ЯЗЫКОМ", "accent": True, "size": "small"}]},
    {"start": 10.90, "end": 12.50, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.50, "end": 14.00, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.00, "end": 15.60, "lines": [{"text": "НАПИСАННЫЙ", "accent": False, "size": "small"}, {"text": "СОВРЕМЕННЫМ ЯЗЫКОМ", "accent": True, "size": "small"}]},
    {"start": 15.60, "end": 17.60, "lines": [{"text": "БЕЗ ФОРМУЛ ИЗ ШКОЛЬНОГО", "accent": False, "size": "small"}, {"text": "ПРОШЛОГО", "accent": True, "size": "big"}]},
    {"start": 17.60, "end": 19.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.00, "end": 20.162, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 7.35, "end": 8.01}, {"start": 9.72, "end": 10.86}, {"start": 16.20, "end": 16.59}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (Рома, 17.73s): a task breakdown that answers "how" but
# also "why" for each step -- the app's text breakdown states why every
# step is needed, which sticks better than steps alone
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ЗНАЮ КАК", "НЕ ЗНАЮ ЗАЧЕМ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "РАЗБОР ОТВЕЧАЕТ НА", "accent": False, "size": "small"}, {"text": "КАК", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.70, "lines": [{"text": "А ОН ЕЩЕ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "ЗАЧЕМ", "accent": True, "size": "big"}]},
    {"start": 4.70, "end": 6.10, "lines": [{"text": "КАК", "accent": False, "size": "small"}, {"text": "ДАЕТ ШАГИ", "accent": True, "size": "big"}]},
    {"start": 6.10, "end": 7.50, "lines": [{"text": "ЗАЧЕМ", "accent": False, "size": "small"}, {"text": "ДАЕТ ИДЕЮ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.00, "lines": [{"text": "ВМЕСТЕ ОНИ", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЮТСЯ НАДЕЖНЕЕ", "accent": True, "size": "small"}]},
    {"start": 9.00, "end": 10.60, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.20, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.80, "lines": [{"text": "У КАЖДОГО ШАГА УКАЗАНО", "accent": False, "size": "small"}, {"text": "ЗАЧЕМ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.40, "lines": [{"text": "ОН", "accent": False, "size": "small"}, {"text": "НУЖЕН", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 16.80, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 17.73, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 4.38, "end": 5.31}, {"start": 9.66, "end": 10.65}, {"start": 14.46, "end": 15.09}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
