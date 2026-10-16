#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-EIGHTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes105/.

Three returning hosts, no new faces: "blue-shirt brunette" / THE SMITHS
poster + "ЕГЭ 2026" sticky note room (a, d), "blonde in cream sweater" /
desk+lamp+plant+notebook room (b, e, f), "mother" / bookshelf+doorway
apartment with small framed picture (c).

Sub-themes: sorting norms of law/morality/custom into three boxes for the
social-studies exam, which break on examples where one act fits two boxes
at once; a task breakdown offering three methods at once leaving the
narrator stuck choosing none; a daughter's image of government-as-traffic-
controller that will stick better than the exact list of functions;
finding a step the author skipped in a breakdown and feeling happier about
it than about a good grade; an older sister's empty room becoming a quiet
study zone once she left for the dorm; and childhood chaos of historical
raids turning into a precise schedule once each gets its own year and city.

Card/intro text was authored with per-line pixel-width verification against
the actual Golos Text Black render (see batch 57's overflow fix) -- every
accent line here was checked to fit the 920px available width at its
assigned font size before being written below, instead of relying on the
10-char heuristic alone.
"""
import json

REAL_DURATION = {
    "a": 25.922, "b": 19.372, "c": 20.823,
    "d": 22.240, "e": 19.650, "f": 22.167,
}
SOURCE_FILE = {
    "a": "bfhdrsyehjn.mesjrt", "b": "fghshbnhsetfvs", "c": "fgsgfgfsdfsf",
    "d": "fhdargbh.setrf", "e": "fzghdsh.nsherfv", "f": "sddgbgawefdvdswef",
}
FIXES = {
    "a": {"общесвознанию": "обществознанию", "виде": "где"},
    "b": {},
    "c": {},
    "d": {"етренажере": "тренажере"},
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
    with open(f"../asr_coffee123_58/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (blue-shirt brunette, 25.922s): sorting norms of law, morality
# and custom into three boxes for the social-studies exam -- the boxes
# break on examples where one act fits two of them at once, and the app's
# games sort norms using exactly those ambiguous examples
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ОДИН ПОСТУПОК", "ПОД ДВА ЯЩИКА"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "НОРМЫ ПРАВА МОРАЛИ", "accent": False, "size": "small"}, {"text": "И ОБЫЧАЕВ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.90, "lines": [{"text": "НА ЕГЭ ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "РАСКЛАДЫВАЮ", "accent": True, "size": "small"}]},
    {"start": 4.90, "end": 6.30, "lines": [{"text": "ПО ТРЕМ", "accent": False, "size": "small"}, {"text": "ЯЩИКАМ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.70, "lines": [{"text": "НО ЯЩИКИ У МЕНЯ", "accent": False, "size": "small"}, {"text": "ЛОМАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.70, "end": 9.30, "lines": [{"text": "ЛОМАЮТСЯ ОНИ", "accent": False, "size": "small"}, {"text": "НА ПРИМЕРАХ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.90, "lines": [{"text": "ОДИН И ТОТ ЖЕ", "accent": False, "size": "small"}, {"text": "ПОСТУПОК", "accent": True, "size": "big"}]},
    {"start": 10.90, "end": 12.50, "lines": [{"text": "ПОДХОДИТ СРАЗУ ПОД", "accent": False, "size": "small"}, {"text": "ДВА ЯЩИКА", "accent": True, "size": "big"}]},
    {"start": 12.50, "end": 14.10, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 15.70, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.70, "end": 17.30, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ГДЕ НОРМЫ", "accent": True, "size": "big"}]},
    {"start": 17.30, "end": 18.90, "lines": [{"text": "РАЗБИРАЮТСЯ", "accent": False, "size": "small"}, {"text": "НА ПРИМЕРАХ", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 20.70, "lines": [{"text": "ПРИХОДИТСЯ РАСКЛАДЫВАТЬ", "accent": False, "size": "small"}, {"text": "ПО ЯЩИКАМ", "accent": True, "size": "big"}]},
    {"start": 20.70, "end": 22.30, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.30, "end": 25.922, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 7.92, "end": 9.60}, {"start": 12.72, "end": 14.43}, {"start": 22.02, "end": 23.22}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde in cream sweater, 19.372s): a task breakdown offering
# three methods at once leaves the narrator choosing none -- the app's
# text breakdown highlights the one main method, others kept as backup
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ТРИ СПОСОБА", "И Я ТЕРЯЮСЬ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "КОГДА В РАЗБОРЕ", "accent": False, "size": "small"}, {"text": "ТРИ СПОСОБА", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.60, "lines": [{"text": "Я ТЕРЯЮСЬ И НЕ", "accent": False, "size": "small"}, {"text": "ВЫБИРАЮ", "accent": True, "size": "big"}]},
    {"start": 4.60, "end": 5.80, "lines": [{"text": "НИ", "accent": False, "size": "small"}, {"text": "ОДНОГО", "accent": True, "size": "big"}]},
    {"start": 5.80, "end": 7.20, "lines": [{"text": "МНЕ НУЖЕН ОДИН", "accent": False, "size": "small"}, {"text": "РАБОЧИЙ", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.60, "lines": [{"text": "СПОСОБ И", "accent": False, "size": "small"}, {"text": "ПОМЕТКА", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 10.00, "lines": [{"text": "КОГДА НУЖНЫ", "accent": False, "size": "small"}, {"text": "ОСТАЛЬНЫЕ", "accent": True, "size": "big"}]},
    {"start": 10.00, "end": 11.40, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.80, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.20, "lines": [{"text": "ГДЕ ГЛАВНЫЙ", "accent": False, "size": "small"}, {"text": "СПОСОБ", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 15.80, "lines": [{"text": "ВЫДЕЛЕН А ОСТАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ЗАПАСНЫЕ", "accent": True, "size": "big"}]},
    {"start": 15.80, "end": 17.20, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.20, "end": 19.372, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.60, "end": 8.22}, {"start": 13.62, "end": 14.79}, {"start": 16.41, "end": 16.74}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 20.823s): a daughter's image of government-as-
# traffic-controller for the social-studies exam will stick better than
# the exact list of functions -- the app's games repeat those functions
# in rounds until they stick too
# ---------------------------------------------------------------------------
c_intro = {"lines": ["КАК", "РЕГУЛИРОВЩИК"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "ДОЧЬ СРАВНИЛА", "accent": False, "size": "small"}, {"text": "РОЛЬ", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 5.10, "lines": [{"text": "В ЭКОНОМИКЕ С РОЛЬЮ", "accent": False, "size": "small"}, {"text": "РЕГУЛИРОВЩИКА", "accent": True, "size": "small"}]},
    {"start": 5.10, "end": 6.30, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПЕРЕКРЕСТКЕ", "accent": True, "size": "small"}]},
    {"start": 6.30, "end": 7.70, "lines": [{"text": "ДЛЯ ЕГЭ ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ОБРАЗ", "accent": True, "size": "big"}]},
    {"start": 7.70, "end": 9.10, "lines": [{"text": "МНЕ ПОНРАВИЛСЯ", "accent": False, "size": "small"}, {"text": "ЭТОТ ОБРАЗ", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 10.10, "lines": [{"text": "ОН", "accent": False, "size": "small"}, {"text": "ЗАПОМНИТСЯ", "accent": True, "size": "big"}]},
    {"start": 10.10, "end": 11.50, "lines": [{"text": "А ТОЧНЫЙ СПИСОК", "accent": False, "size": "small"}, {"text": "ФУНКЦИЙ", "accent": True, "size": "big"}]},
    {"start": 11.50, "end": 12.70, "lines": [{"text": "ДОЧЬ ВЫУЧИТ", "accent": False, "size": "small"}, {"text": "ИГРАМИ", "accent": True, "size": "big"}]},
    {"start": 12.70, "end": 14.10, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 15.30, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.70, "lines": [{"text": "ГДЕ ФУНКЦИИ", "accent": False, "size": "small"}, {"text": "ГОСУДАРСТВА", "accent": True, "size": "small"}]},
    {"start": 16.70, "end": 18.30, "lines": [{"text": "В ЭКОНОМИКЕ ПОВТОРЯЮТСЯ", "accent": False, "size": "small"}, {"text": "РАУНДАМИ", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.50, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.50, "end": 20.823, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.27, "end": 4.59}, {"start": 8.46, "end": 9.24}, {"start": 17.55, "end": 18.63}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 22.240s): finding a step the author
# skipped in a breakdown felt better than a good grade -- it means she can
# read breakdowns attentively, and the app's writes every step out fully
# so a skip is always noticeable
# ---------------------------------------------------------------------------
d_intro = {"lines": ["НАШЛА", "ПРОПУЩЕННЫЙ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "ОДНАЖДЫ Я НАШЛА", "accent": False, "size": "small"}, {"text": "ШАГ", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.50, "lines": [{"text": "КОТОРЫЙ АВТОР", "accent": False, "size": "small"}, {"text": "ПРОПУСТИЛ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.70, "lines": [{"text": "И ОБРАДОВАЛАСЬ", "accent": False, "size": "small"}, {"text": "БОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 6.90, "lines": [{"text": "ЧЕМ ХОРОШИМ", "accent": False, "size": "small"}, {"text": "ОЦЕНКАМ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.10, "lines": [{"text": "ЗНАЧИТ Я УЖЕ", "accent": False, "size": "small"}, {"text": "УМЕЮ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.50, "lines": [{"text": "ЧИТАТЬ РАЗБОРЫ", "accent": False, "size": "small"}, {"text": "ВНИМАТЕЛЬНО", "accent": True, "size": "small"}]},
    {"start": 9.50, "end": 10.70, "lines": [{"text": "И ОСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "НАУЧИТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 10.70, "end": 11.90, "lines": [{"text": "ПИСАТЬ", "accent": False, "size": "small"}, {"text": "СОБСТВЕННЫЕ", "accent": True, "size": "small"}]},
    {"start": 11.90, "end": 13.10, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.10, "end": 14.50, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.50, "end": 15.70, "lines": [{"text": "ГДЕ ШАГИ", "accent": False, "size": "small"}, {"text": "ЗАПИСАНЫ", "accent": True, "size": "big"}]},
    {"start": 15.70, "end": 17.10, "lines": [{"text": "ПОЛНОСТЬЮ ПОЭТОМУ ЛЮБОЙ", "accent": False, "size": "small"}, {"text": "ПРОПУСК", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.30, "lines": [{"text": "СРАЗУ", "accent": False, "size": "small"}, {"text": "ЗАМЕТЕН", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.70, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.70, "end": 22.240, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.84, "end": 5.64}, {"start": 10.65, "end": 12.45}, {"start": 18.33, "end": 19.80}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde in cream sweater, 19.650s): an older sister's empty
# room becomes a quiet study zone once she leaves for the dorm -- the
# app's FIPI bank lets a task be opened anywhere, quiet room included
# ---------------------------------------------------------------------------
e_intro = {"lines": ["КОМНАТА", "ОСВОБОДИЛАСЬ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "СТАРШАЯ СЕСТРА", "accent": False, "size": "small"}, {"text": "УЕХАЛА", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ОБЩЕЖИТИЕ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.70, "lines": [{"text": "ЕЕ ПУСТАЯ КОМНАТА", "accent": False, "size": "small"}, {"text": "СТАЛА", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 6.90, "lines": [{"text": "МОЕЙ ТИХОЙ", "accent": False, "size": "small"}, {"text": "ЗОНОЙ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.10, "lines": [{"text": "ДЛЯ ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.30, "lines": [{"text": "ТИШИНА", "accent": False, "size": "small"}, {"text": "ПОМОГАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.50, "lines": [{"text": "НО ГЛАВНОЕ ЧТО У", "accent": False, "size": "small"}, {"text": "ЗАНЯТИЙ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.70, "lines": [{"text": "ПОЯВИЛОСЬ", "accent": False, "size": "small"}, {"text": "СВОЕ МЕСТО", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.90, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.10, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 15.50, "lines": [{"text": "ГДЕ ЗАДАНИЕ МОЖНО", "accent": False, "size": "small"}, {"text": "ОТКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 15.50, "end": 16.90, "lines": [{"text": "В ТОМ ЧИСЛЕ В ТИХОЙ", "accent": False, "size": "small"}, {"text": "КОМНАТЕ", "accent": True, "size": "big"}]},
    {"start": 16.90, "end": 18.30, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.650, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 6.99, "end": 7.74}, {"start": 9.48, "end": 10.50}, {"start": 16.35, "end": 17.01}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde in cream sweater, 22.167s): childhood chaos of
# historical raids on Russian cities turns into a precise schedule once
# each raid gets its own year and city -- the app's history games sort
# raids and cities by year through rounds
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ШУМНО НО", "НЕ СКАЖУ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "НАБЕГИ ОРДЫ", "accent": False, "size": "small"}, {"text": "НА ГОРОДА", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "В ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "Я ПОМНЮ ИХ", "accent": False, "size": "small"}, {"text": "КАК ГРОЗУ", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "ШУМНО НО", "accent": False, "size": "small"}, {"text": "КТО КОГДА", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "И КУДА", "accent": False, "size": "small"}, {"text": "НЕ СКАЖУ", "accent": True, "size": "big"}]},
    {"start": 7.90, "end": 9.30, "lines": [{"text": "ГРОЗА ПРЕВРАЩАЕТСЯ В", "accent": False, "size": "small"}, {"text": "РАСПИСАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.50, "lines": [{"text": "КОГДА КАЖДОМУ", "accent": False, "size": "small"}, {"text": "НАБЕГУ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.70, "lines": [{"text": "НАЗНАЧЕН СВОЙ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.90, "lines": [{"text": "И СВОЙ", "accent": False, "size": "small"}, {"text": "ГОРОД", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.10, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 15.50, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.50, "end": 16.90, "lines": [{"text": "ГДЕ НАБЕГИ", "accent": False, "size": "small"}, {"text": "И ГОРОДА", "accent": True, "size": "big"}]},
    {"start": 16.90, "end": 18.30, "lines": [{"text": "РАССТАВЛЯЮТСЯ", "accent": False, "size": "small"}, {"text": "ПО ГОДАМ", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.70, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.70, "end": 22.167, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 6.09, "end": 7.92}, {"start": 11.82, "end": 13.50}, {"start": 17.76, "end": 19.17}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
