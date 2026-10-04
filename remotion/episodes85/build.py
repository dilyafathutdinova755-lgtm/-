#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-EIGHTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes85/.

Two returning hosts, no new faces: "blue-shirt brunette" / THE SMITHS
poster room (a, e, f), "blonde in cream sweater" (b, c, d).

Sub-themes: an answer that's technically correct but incomplete or
mis-signed -- a number without its required explanation, a sign
flipped at the final step, a letter-choice habit that falls apart
once options disappear, similar-sounding words/stresses slipping into
the wrong spot despite being distinguishable in isolation, and a
shared class folder that lost material to an accidental deletion.
"""
import json

REAL_DURATION = {
    "a": 27.180, "b": 23.575, "c": 30.295,
    "d": 22.082, "e": 24.087, "f": 27.778,
}
SOURCE_FILE = {
    "a": "fdgdgfdgdfgf", "b": "fvbgdhd", "c": "gdgdgdfggd",
    "d": "gdgfdgfdgdg", "e": "gfdgfdgfdgdfgf", "f": "gvmxfhtehgt",
}
FIXES = {}


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
    with open(f"../asr_coffee123_38/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blue-shirt brunette, 27.180s): a task sometimes asks not just
# for a number but also a short explanation of it; out of habit only the
# number gets written, losing points; the app's breakdown separately
# flags when an explanation is also required
# ---------------------------------------------------------------------------
a_intro = {"lines": ["НАШЛА ЧИСЛО", "НО НЕ ОБЪЯСНИЛА?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.54, "lines": [{"text": "МЕНЯ ИНОГДА ПРОСИТ", "accent": False, "size": "small"}, {"text": "НЕ ТОЛЬКО НАЙТИ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.71, "lines": [{"text": "ЧИСЛО НО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.71, "end": 6.06, "lines": [{"text": "ЕГО", "accent": False, "size": "small"}, {"text": "СМЫСЛ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.11, "lines": [{"text": "А Я ПО ПРИВЫЧКЕ", "accent": False, "size": "small"}, {"text": "ПИШУ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.28, "lines": [{"text": "ТОЛЬКО САМО", "accent": False, "size": "small"}, {"text": "ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 9.12, "end": 9.96, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 11.22, "lines": [{"text": "Я ПОЛУЧИЛА", "accent": False, "size": "small"}, {"text": "ВЕРНОЕ ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.36, "lines": [{"text": "И ПОТЕРЯЛА", "accent": False, "size": "small"}, {"text": "БАЛЛЫ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 14.16, "lines": [{"text": "ПРОСТО ЗА ТО ЧТО НЕ", "accent": False, "size": "small"}, {"text": "НАПИСАЛА", "accent": True, "size": "big"}]},
    {"start": 14.16, "end": 15.99, "lines": [{"text": "КОРОТКОЕ ОБЪЯСНЕНИЕ", "accent": False, "size": "small"}, {"text": "РЯДОМ С НИМ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 17.66, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.66, "end": 19.38, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 19.38, "end": 21.18, "lines": [{"text": "КОТОРЫЙ ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 21.18, "end": 22.74, "lines": [{"text": "КОГДА В ОТВЕТЕ НУЖНО", "accent": False, "size": "small"}, {"text": "НЕ ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 22.74, "end": 24.42, "lines": [{"text": "ЧИСЛО НО И", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 25.17, "end": 26.00, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 26.00, "end": 27.180, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.32, "end": 4.71}, {"start": 11.61, "end": 12.36}, {"start": 22.14, "end": 22.74}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde cream sweater, 23.575s): trained almost only
# multiple-choice tasks and barely touched short-answer tasks without
# options; got lost specifically where there was no letter to pick; the
# app's bank has every format together, not just multiple-choice
# ---------------------------------------------------------------------------
b_intro = {"lines": ["С ВЫБОРОМ ОТВЕТА", "РЕШАЕШЬ ПОЧТИ ВСЕ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 2.79, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "С ВЫБОРОМ", "accent": True, "size": "big"}]},
    {"start": 2.79, "end": 3.96, "lines": [{"text": "ОТВЕТА Я РЕШАЛА", "accent": False, "size": "small"}, {"text": "ПОЧТИ ВСЕ ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 5.82, "lines": [{"text": "А ЗАДАНИЯ С", "accent": False, "size": "small"}, {"text": "КРАТКИМ ОТВЕТОМ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 7.56, "lines": [{"text": "БЕЗ ВАРИАНТОВ ПОЧТИ", "accent": False, "size": "small"}, {"text": "НЕ ТРОГАЛА", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 9.18, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.05, "lines": [{"text": "БЕЗ ВАРИАНТОВ", "accent": False, "size": "small"}, {"text": "ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 11.01, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "РАСТЕРЯЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 11.01, "end": 12.27, "lines": [{"text": "ИМЕННО ТАМ ГДЕ", "accent": False, "size": "small"}, {"text": "РАНЬШЕ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.89, "lines": [{"text": "ПРОСТО ВЫБИРАЛА", "accent": False, "size": "small"}, {"text": "НУЖНУЮ БУКВУ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 15.81, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.81, "end": 16.95, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.95, "end": 18.45, "lines": [{"text": "СО ВСЕМИ", "accent": False, "size": "small"}, {"text": "ФОРМАТАМИ ЗАДАНИЙ", "accent": True, "size": "small"}]},
    {"start": 18.45, "end": 19.59, "lines": [{"text": "СРАЗУ", "accent": False, "size": "small"}, {"text": "А НЕ ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 19.59, "end": 20.97, "lines": [{"text": "С ПРИВЫЧНЫМ", "accent": False, "size": "small"}, {"text": "ВЫБОРОМ ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 21.66, "end": 22.50, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.50, "end": 23.575, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.18, "end": 3.63}, {"start": 10.47, "end": 11.01}, {"start": 12.78, "end": 13.14}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blonde cream sweater, 30.295s): similar-sounding but
# different-meaning Russian words slip into the wrong spot in her own
# sentences, even though she tells them apart flawlessly on a list; the
# app's memory games train exactly such word pairs side by side
# ---------------------------------------------------------------------------
c_intro = {"lines": ["СОЗВУЧНЫЕ НО РАЗНЫЕ", "ПО СМЫСЛУ СЛОВА ПУТАЕШЬ?"], "end": 1.98}
c_cards = [
    {"start": 1.98, "end": 2.81, "lines": [{"text": "ПО СМЫСЛУ", "accent": False, "size": "small"}, {"text": "СЛОВА", "accent": True, "size": "big"}]},
    {"start": 3.21, "end": 4.35, "lines": [{"text": "ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 4.77, "end": 5.73, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ПРОСКАКИВАЮТ", "accent": True, "size": "small"}]},
    {"start": 5.73, "end": 6.72, "lines": [{"text": "В МОЕМ", "accent": False, "size": "small"}, {"text": "ПРЕДЛОЖЕНИИ", "accent": True, "size": "small"}]},
    {"start": 7.08, "end": 7.89, "lines": [{"text": "НЕ НА СВОЕМ", "accent": False, "size": "small"}, {"text": "МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 8.52, "end": 9.60, "lines": [{"text": "ХОТЯ В ОТДЕЛЬНОМ", "accent": False, "size": "small"}, {"text": "СПИСКЕ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.34, "lines": [{"text": "Я ИХ РАЗЛИЧАЮ", "accent": False, "size": "small"}, {"text": "БЕЗОШИБОЧНО", "accent": True, "size": "small"}]},
    {"start": 12.27, "end": 13.06, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 13.06, "end": 14.16, "lines": [{"text": "Я ВСТАВИЛА В", "accent": False, "size": "small"}, {"text": "ПРЕДЛОЖЕНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.52, "end": 16.20, "lines": [{"text": "СОЗВУЧНОЕ НО", "accent": False, "size": "small"}, {"text": "НЕВЕРНОЕ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.03, "lines": [{"text": "ПО СМЫСЛУ", "accent": False, "size": "small"}, {"text": "СЛОВА", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 18.00, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "НУЖНОГО", "accent": True, "size": "big"}]},
    {"start": 19.26, "end": 20.07, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 20.07, "end": 20.88, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 21.27, "end": 22.50, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 22.95, "end": 23.79, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 24.06, "end": 25.38, "lines": [{"text": "ИМЕННО ТАКИЕ", "accent": False, "size": "small"}, {"text": "ПОХОЖИЕ", "accent": True, "size": "big"}]},
    {"start": 25.38, "end": 27.51, "lines": [{"text": "ПО ЗВУЧАНИЮ СЛОВА", "accent": False, "size": "small"}, {"text": "РЯДОМ ДРУГ С ДРУГОМ", "accent": True, "size": "small"}]},
    {"start": 28.41, "end": 29.22, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 29.22, "end": 30.295, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.19, "end": 5.73}, {"start": 10.77, "end": 11.34}, {"start": 14.52, "end": 15.06}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blonde cream sweater, 22.082s): correctly substitutes numbers
# into a formula but doesn't double-check the sign in front of the
# result at the end; the app's breakdown separately checks that sign
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАК ПЕРЕД", "РЕЗУЛЬТАТОМ ПЕРЕПРОВЕРЯЕШЬ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 2.82, "lines": [{"text": "ЗАДАНИЕ ЕГЭ Я ИНОГДА", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНО", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 3.69, "lines": [{"text": "ПОДСТАВЛЯЮ ЧИСЛА В", "accent": False, "size": "small"}, {"text": "ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 4.26, "end": 5.31, "lines": [{"text": "А ЗНАК ПЕРЕД", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТОМ", "accent": True, "size": "small"}]},
    {"start": 5.31, "end": 7.02, "lines": [{"text": "В САМОМ КОНЦЕ НЕ", "accent": False, "size": "small"}, {"text": "ПЕРЕПРОВЕРЯЮ", "accent": True, "size": "small"}]},
    {"start": 7.80, "end": 8.60, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 9.66, "lines": [{"text": "Я ПОЛУЧИЛА", "accent": False, "size": "small"}, {"text": "ВЕРНОЕ ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 10.71, "lines": [{"text": "С НЕВЕРНЫМ", "accent": False, "size": "small"}, {"text": "ЗНАКОМ", "accent": True, "size": "big"}]},
    {"start": 11.28, "end": 12.87, "lines": [{"text": "И ИЗ ЗА ЭТОГО СОВСЕМ", "accent": False, "size": "small"}, {"text": "ДРУГОЙ ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 14.65, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.65, "end": 16.32, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.32, "end": 17.85, "lines": [{"text": "КОТОРЫЙ ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯЕТ", "accent": True, "size": "big"}]},
    {"start": 18.06, "end": 19.47, "lines": [{"text": "ЗНАК РЕЗУЛЬТАТА В", "accent": False, "size": "small"}, {"text": "САМОМ КОНЦЕ", "accent": True, "size": "big"}]},
    {"start": 20.22, "end": 21.05, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.05, "end": 22.082, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 6.51, "end": 7.02}, {"start": 9.99, "end": 10.71}, {"start": 12.30, "end": 12.87}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 24.087s): confuses the stress placement
# in a word with the stress of a similar-but-different word, placing it
# by habit the way she's heard it in conversation; the app's memory games
# train stress in difficult words individually
# ---------------------------------------------------------------------------
e_intro = {"lines": ["МЕСТО УДАРЕНИЯ", "В СЛОВЕ ПУТАЕШЬ?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 2.79, "lines": [{"text": "В ОДНОМ И ТОМ ЖЕ", "accent": False, "size": "small"}, {"text": "СЛОВЕ", "accent": True, "size": "big"}]},
    {"start": 2.79, "end": 3.72, "lines": [{"text": "ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.55, "lines": [{"text": "Я ИНОГДА ПУТАЮ С", "accent": False, "size": "small"}, {"text": "УДАРЕНИЕМ", "accent": True, "size": "small"}]},
    {"start": 5.55, "end": 7.17, "lines": [{"text": "В ПОХОЖЕМ НО", "accent": False, "size": "small"}, {"text": "ДРУГОМ СЛОВЕ", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 8.65, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 8.65, "end": 9.60, "lines": [{"text": "Я ПОСТАВИЛА", "accent": False, "size": "small"}, {"text": "УДАРЕНИЕ", "accent": True, "size": "small"}]},
    {"start": 9.60, "end": 10.89, "lines": [{"text": "ПО ПРИВЫЧКЕ ТАК", "accent": False, "size": "small"}, {"text": "КАК", "accent": True, "size": "big"}]},
    {"start": 10.89, "end": 12.09, "lines": [{"text": "СЛЫШАЛА В", "accent": False, "size": "small"}, {"text": "РАЗГОВОРЕ", "accent": True, "size": "small"}]},
    {"start": 12.51, "end": 13.80, "lines": [{"text": "А НЕ ТАК КАК ТРЕБУЕТ", "accent": False, "size": "small"}, {"text": "НОРМА", "accent": True, "size": "big"}]},
    {"start": 14.42, "end": 15.21, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 16.02, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 16.32, "end": 17.52, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.79, "end": 18.63, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 18.63, "end": 19.71, "lines": [{"text": "УДАРЕНИЕ", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 19.71, "end": 20.64, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "СЛОЖНЫХ СЛОВАХ", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 21.85, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНОСТИ", "accent": True, "size": "small"}]},
    {"start": 22.26, "end": 23.10, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.10, "end": 24.087, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 4.71, "end": 5.55}, {"start": 9.72, "end": 10.20}, {"start": 13.17, "end": 13.80}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blue-shirt brunette, 27.778s): ЕГЭ materials in the class's
# shared folder vanished after someone accidentally deleted part of the
# files; noticed only on a practice test, hitting a topic never reviewed
# because it had been deleted; the app's bank never loses material
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗАДАНИЯ ИЗ ПАПКИ", "КЛАССА ПРОПАЛИ?"], "end": 1.95}
f_cards = [
    {"start": 1.95, "end": 3.15, "lines": [{"text": "ЕГЭ В ОБЩЕЙ", "accent": False, "size": "small"}, {"text": "ПАПКЕ КЛАССА", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.29, "lines": [{"text": "ПОЛОВИНА ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ПРОПАЛО", "accent": True, "size": "big"}]},
    {"start": 4.29, "end": 5.97, "lines": [{"text": "ПОСЛЕ ТОГО КАК КТО ТО", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНО УДАЛИЛ", "accent": True, "size": "small"}]},
    {"start": 5.97, "end": 7.89, "lines": [{"text": "ЧАСТЬ ФАЙЛОВ А Я", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 7.89, "end": 9.00, "lines": [{"text": "ЭТО ТОЛЬКО", "accent": False, "size": "small"}, {"text": "НА ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.92, "lines": [{"text": "Я ТРЕНИРОВАЛАСЬ", "accent": False, "size": "small"}, {"text": "ПОТОМУ ЧТО", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 12.78, "lines": [{"text": "ОСТАЛОСЬ И НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 14.49, "lines": [{"text": "НАТКНУЛАСЬ НА ЦЕЛУЮ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 16.08, "lines": [{"text": "КОТОРУЮ ИЗ ЗА", "accent": False, "size": "small"}, {"text": "УДАЛЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 16.08, "end": 17.40, "lines": [{"text": "ВООБЩЕ НЕ", "accent": False, "size": "small"}, {"text": "РАЗБИРАЛА", "accent": True, "size": "small"}]},
    {"start": 19.15, "end": 19.95, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 19.95, "end": 21.06, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 22.47, "lines": [{"text": "ГДЕ НИЧЕГО НЕ", "accent": False, "size": "small"}, {"text": "УДАЛЯЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 22.47, "end": 23.94, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНОСТИ", "accent": True, "size": "small"}]},
    {"start": 23.94, "end": 25.32, "lines": [{"text": "И ВСЕ ТЕМЫ", "accent": False, "size": "small"}, {"text": "ОСТАЮТСЯ НА МЕСТЕ", "accent": True, "size": "small"}]},
    {"start": 25.80, "end": 26.61, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 26.61, "end": 27.778, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.31, "end": 5.97}, {"start": 13.05, "end": 13.53}, {"start": 16.80, "end": 17.40}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
