#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTY-FOURTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes111/.

Three returning hosts, no new faces: "mother" / bookshelf+doorway
apartment with small framed picture (a), "Рома" / tight curls, black
Under Armour hoodie, desk+mouse+monitor room (b, c, d), "teen boy on
couch" / bookshelf+plant+window room (e, f).

Sub-themes: a daughter who mixes up internal vs external state functions
in social-studies ЕГЭ despite explaining each one fine on its own --
turns out it's one list that just needs splitting in half, and the
app's memory games drill that exact split; a friend grading a task
explanation like a school report card -- a 4 for clarity, a 3 for being
boring, with clarity mattering more than entertainment; giving up on
waiting for motivation and treating ЕГЭ prep like brushing teeth --
scheduled, no deliberation, motivation shows up later as a side effect
of the habit; a daughter who instantly recalls a textbook city but
blanks on the appanage principality it belongs to, since geography only
sticks once it's tied to history; and knowing the famous names from the
Crimean War (Sevastopol, Nakhimov) but not the causes and outcome the
exam actually asks for, which collapse into three short paragraphs once
structured as causes-course-outcome.

Card/intro text was verified against the actual Golos Text Black render
(PIL getbbox at each line's real font size, small lines included) before
being written below -- consistent with the process that caught overflow
bugs across batches 58-63.

ASR notes: episode e had "тренажери" for "тренажере" (garbled case
ending in the CTA line), fixed as a 1:1 token substitution. Episode d's
CTA used "яга" for "ЕГЭ" -- the familiar tolerated ЕГЭ mishearing
(same family as ег/иг/его/иго/эг/ега/игэ/г/яг), left unfixed per policy.
"""
import json

REAL_DURATION = {
    "a": 18.732, "b": 14.060, "c": 13.463,
    "d": 15.920, "e": 14.978, "f": 16.343,
}
SOURCE_FILE = {
    "a": "bgwgesgffweffw", "b": "bxcxgsfff", "c": "cvnbzsfggsf",
    "d": "fchgsgfsfef", "e": "gdfssdfdsfs", "f": "vsdgdsfdssdv",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {},
    "d": {},
    "e": {"тренажери": "тренажере"},
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
    with open(f"../asr_coffee123_64/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (mother, 18.732s): a daughter mixes up internal vs external
# state functions in social-studies ЕГЭ despite explaining each one fine
# alone -- it's one list that needs splitting in half, and the app's
# memory games drill exactly that split
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗНАЕТ ОБЕ", "НО ПУТАЕТ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.84, "lines": [{"text": "ВНУТРЕННИЕ И ВНЕШНИЕ", "accent": False, "size": "small"}, {"text": "ФУНКЦИИ ГОСУДАРСТВА", "accent": True, "size": "small"}]},
    {"start": 4.02, "end": 5.52, "lines": [{"text": "ДОЧЬ СМЕШИВАЕТ", "accent": False, "size": "small"}, {"text": "ХОТЯ ЗНАЕТ ОБЕ", "accent": True, "size": "small"}]},
    {"start": 5.67, "end": 6.93, "lines": [{"text": "ПО ОТДЕЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ ЛЕГКО", "accent": True, "size": "small"}]},
    {"start": 7.56, "end": 8.79, "lines": [{"text": "ДЕЛО В ТОМ ЧТО", "accent": False, "size": "small"}, {"text": "СПИСОК ОДИН", "accent": True, "size": "small"}]},
    {"start": 9.09, "end": 10.23, "lines": [{"text": "ОТДЕЛИТЬ ЕГО", "accent": False, "size": "small"}, {"text": "НУЖНО ПОПОЛАМ", "accent": True, "size": "small"}]},
    {"start": 10.86, "end": 11.70, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 13.56, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.89, "end": 14.94, "lines": [{"text": "ГДЕ ФУНКЦИИ", "accent": False, "size": "small"}, {"text": "ГОСУДАРСТВА", "accent": True, "size": "small"}]},
    {"start": 15.06, "end": 16.62, "lines": [{"text": "ДЕЛЯТСЯ НА", "accent": False, "size": "small"}, {"text": "ВНУТРЕННИЕ И ВНЕШНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.98, "end": 17.90, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.90, "end": 18.732, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.02, "end": 5.52}, {"start": 9.09, "end": 10.23}, {"start": 15.06, "end": 16.62}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 14.060s): a friend grades a task explanation like a
# school report card -- a 4 for clarity, a 3 for being boring, and
# clarity matters more than entertainment, which is what the app's text
# breakdown optimizes for
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ДРУГ ОЦЕНИЛ", "КАК В ШКОЛЕ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 2.88, "lines": [{"text": "ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ПЯТИБАЛЛЬНОЙ ШКАЛЕ", "accent": True, "size": "small"}]},
    {"start": 3.09, "end": 4.11, "lines": [{"text": "ЧЕТВЕРКА ЗА", "accent": False, "size": "small"}, {"text": "ПОНЯТНОСТЬ", "accent": True, "size": "big"}]},
    {"start": 4.26, "end": 5.13, "lines": [{"text": "И ТРОЙКА ЗА", "accent": False, "size": "small"}, {"text": "СКУКУ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.25, "lines": [{"text": "ПОНЯТНОСТЬ", "accent": False, "size": "small"}, {"text": "НУЖНЕЕ", "accent": True, "size": "big"}]},
    {"start": 6.48, "end": 7.53, "lines": [{"text": "СКУКУ МОЖНО", "accent": False, "size": "small"}, {"text": "ПОТЕРПЕТЬ", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 8.68, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.75, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 9.84, "end": 11.37, "lines": [{"text": "ГДЕ ГЛАВНАЯ", "accent": False, "size": "small"}, {"text": "ПОНЯТНОСТЬ", "accent": True, "size": "big"}]},
    {"start": 11.52, "end": 12.35, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "УКРАШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 12.39, "end": 13.20, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.060, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.09, "end": 4.11}, {"start": 5.40, "end": 7.53}, {"start": 9.84, "end": 11.37}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 13.463s): giving up on waiting for motivation and
# treating ЕГЭ prep like brushing teeth -- scheduled, no deliberation,
# motivation shows up later as a side effect of the habit, same as the
# app's FIPI bank that opens a task without a moment of hesitation
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НЕТ МОТИВАЦИИ", "И НЕ БУДЕТ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.33, "lines": [{"text": "РЕШАЮ ЕГЭ", "accent": False, "size": "small"}, {"text": "КАК ЧИЩУ ЗУБЫ", "accent": True, "size": "small"}]},
    {"start": 3.54, "end": 5.16, "lines": [{"text": "ПО РАСПИСАНИЮ", "accent": False, "size": "small"}, {"text": "БЕЗ РАЗМЫШЛЕНИЙ", "accent": True, "size": "small"}]},
    {"start": 5.40, "end": 6.51, "lines": [{"text": "МОТИВАЦИЯ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТ ПОЗЖЕ", "accent": True, "size": "small"}]},
    {"start": 6.66, "end": 7.80, "lines": [{"text": "КАК ПРИЛОЖЕНИЕ", "accent": False, "size": "small"}, {"text": "К ПРИВЫЧКЕ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.33, "lines": [{"text": "В ЕГ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "small"}]},
    {"start": 9.87, "end": 11.52, "lines": [{"text": "ГДЕ ЗАДАНИЕ ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "БЕЗ РАЗДУМИЙ", "accent": True, "size": "small"}]},
    {"start": 11.73, "end": 12.65, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 12.65, "end": 13.463, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.86, "end": 3.33}, {"start": 5.40, "end": 6.51}, {"start": 11.04, "end": 11.52}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (Рома, 15.920s): a daughter instantly recalls a textbook
# city but blanks on the appanage principality it belongs to -- geography
# only sticks once tied to history, which is what the app's history
# memory games pair up
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПОМНЮ ГОРОД", "НЕ КНЯЖЕСТВО"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 2.70, "lines": [{"text": "В ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 4.56, "lines": [{"text": "НАЗВАНИЕ КНЯЖЕСТВА", "accent": False, "size": "small"}, {"text": "Я НЕ ВСПОМНЮ", "accent": True, "size": "small"}]},
    {"start": 4.71, "end": 5.70, "lines": [{"text": "А ГОРОД ИЗ УЧЕБНИКА", "accent": False, "size": "small"}, {"text": "ВСПОМНЮ СРАЗУ", "accent": True, "size": "small"}]},
    {"start": 5.85, "end": 6.93, "lines": [{"text": "ГОРОД НУЖНО", "accent": False, "size": "small"}, {"text": "СВЯЗАТЬ С КНЯЖЕСТВОМ", "accent": True, "size": "small"}]},
    {"start": 7.11, "end": 8.79, "lines": [{"text": "ИНАЧЕ ГЕОГРАФИЯ", "accent": False, "size": "small"}, {"text": "ОСТАЕТСЯ КАРТИНКОЙ", "accent": True, "size": "small"}]},
    {"start": 9.06, "end": 10.20, "lines": [{"text": "В ЕГ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 10.41, "end": 11.37, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 11.55, "end": 13.83, "lines": [{"text": "ГОРОДА СВЯЗАНЫ", "accent": False, "size": "small"}, {"text": "С КНЯЖЕСТВАМИ", "accent": True, "size": "small"}]},
    {"start": 14.07, "end": 15.09, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 15.920, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.71, "end": 5.70}, {"start": 7.11, "end": 8.79}, {"start": 11.55, "end": 12.48}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (teen boy on couch, 14.978s): paper exam booklets print
# answers upside down so peeking is always one flip away -- this tool
# keeps the reasoning and the answer together, so there's nowhere to
# peek without reading the path to it, same as the app's text breakdown
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ХОЧЕТСЯ", "ПОДГЛЯДЕТЬ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ОТВЕТЫ ЕГЭ", "accent": False, "size": "small"}, {"text": "ВВЕРХ НОГАМИ", "accent": True, "size": "small"}]},
    {"start": 3.51, "end": 5.34, "lines": [{"text": "Я СМЕЮСЬ", "accent": False, "size": "small"}, {"text": "НО ПОДГЛЯДЫВАЮ", "accent": True, "size": "small"}]},
    {"start": 5.70, "end": 6.84, "lines": [{"text": "ЗДЕСЬ", "accent": False, "size": "small"}, {"text": "ПОДГЛЯДЫВАТЬ НЕКУДА", "accent": True, "size": "small"}]},
    {"start": 7.08, "end": 8.40, "lines": [{"text": "ПУТЬ И ОТВЕТ", "accent": False, "size": "small"}, {"text": "ИДУТ ПОДРЯД", "accent": True, "size": "small"}]},
    {"start": 8.70, "end": 9.87, "lines": [{"text": "В ЕГ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "small"}]},
    {"start": 10.02, "end": 10.86, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "small"}]},
    {"start": 11.01, "end": 12.15, "lines": [{"text": "ГДЕ ОТВЕТ НЕЛЬЗЯ", "accent": False, "size": "small"}, {"text": "ПОДГЛЯДЕТЬ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.19, "lines": [{"text": "БЕЗ ПУТИ", "accent": False, "size": "small"}, {"text": "К НЕМУ", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.15, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.15, "end": 14.978, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.86, "end": 3.30}, {"start": 5.70, "end": 8.40}, {"start": 11.01, "end": 12.15}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 16.343s): knowing the famous names from
# the Crimean War but not the causes and outcome the exam actually asks
# for -- causes, course and outcome collapse into three short paragraphs,
# and the app's history memory games line them up in order
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗНАЮ ИМЕНА", "НЕ ЗНАЮ ПРИЧИН"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.94, "lines": [{"text": "ЗНАЮ", "accent": False, "size": "small"}, {"text": "СЕВАСТОПОЛЬ И НАХИМОВА", "accent": True, "size": "small"}]},
    {"start": 3.09, "end": 3.96, "lines": [{"text": "А ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.58, "lines": [{"text": "НУЖНЫ ЕЩЕ", "accent": False, "size": "small"}, {"text": "ПРИЧИНЫ И ИТОГ", "accent": True, "size": "small"}]},
    {"start": 5.79, "end": 7.35, "lines": [{"text": "ПРИЧИНЫ ХОД И ИТОГ", "accent": False, "size": "small"}, {"text": "СКЛАДЫВАЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 7.50, "end": 8.70, "lines": [{"text": "КАК ТРИ КОРОТКИХ", "accent": False, "size": "small"}, {"text": "ПАРАГРАФА", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 10.11, "lines": [{"text": "В ЕГ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 10.29, "end": 11.34, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 11.49, "end": 13.50, "lines": [{"text": "ГДЕ ПРИЧИНЫ ХОД", "accent": False, "size": "small"}, {"text": "И ИТОГИ ВОЙНЫ", "accent": True, "size": "small"}]},
    {"start": 13.65, "end": 14.49, "lines": [{"text": "РАЗЛОЖЕНЫ", "accent": False, "size": "small"}, {"text": "ПО ПОРЯДКУ", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 15.50, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.50, "end": 16.343, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.86, "end": 2.94}, {"start": 5.79, "end": 8.70}, {"start": 13.65, "end": 14.49}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
