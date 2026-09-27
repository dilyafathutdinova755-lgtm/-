#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-EIGHTH 'coffee123'
batch (6 episodes uploaded under the same tag after twenty-seven prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes75/.

Two brand-new hosts this batch (first appearance in the series): a boy
in a gray t-shirt in a sunlit apartment with a bookshelf and window
plants (a, b, c), and an adult woman in a different apartment entirely
(wood floors, wood bookshelf/desk) who speaks about her daughter (d, e, f).

Sub-themes: a memorized answer/method that doesn't survive a short gap
without review (a, e), memorization that resists a slightly different
context -- a new date interval, a different word, a changed format
(b, d, g/c), and stale study material inherited or kept too long vs.
the app's up-to-date FIPI bank (c, f).
"""
import json

REAL_DURATION = {
    "a": 18.040, "b": 18.263, "c": 17.730,
    "d": 21.960, "e": 19.820, "f": 17.520,
}
SOURCE_FILE = {
    "a": "gfgfdgfdg", "b": "gfhjytertyj", "c": "gjkhgjhzetrw",
    "d": "gfjhdtdrs", "e": "jfghdsthnd", "f": "mjghfgtretyghj",
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


def build_running_caption(words, total_duration):
    groups = [{"text": w["text"].upper(), "start": w["start"]} for w in words]
    for idx in range(len(groups)):
        groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
    groups[0]["start"] = 0.0
    return groups


FIXES = {
    "a": {"тренажери": "тренажере"},
    "c": {"фипис": "фипи"},
}


def fix_words(letter, words):
    """Repair known sherpa-onnx ASR mis-transcriptions before captioning."""
    fixes = FIXES.get(letter, {})
    for w in words:
        if w["text"] in fixes:
            w["text"] = fixes[w["text"]]
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_28/{src}_words.json"))
    words = fix_words(letter, words)
    for w in words:
        w["start"] = min(w["start"], total_duration)
        w["end"] = min(w["end"], total_duration)

    check_intro_vs_cards(letter, intro["end"], cards)
    check_cards(letter, cards, total_duration)
    check_emphasis(letter, emphasis, total_duration)

    running_caption = build_running_caption(words, total_duration)

    json.dump(words, open(f"ep_{letter}_words.json", "w"), ensure_ascii=False, indent=2)
    json.dump(cards, open(f"ep_{letter}_cards.json", "w"), ensure_ascii=False, indent=2)
    json.dump(running_caption, open(f"ep_{letter}_running_caption.json", "w"), ensure_ascii=False, indent=2)
    json.dump({"total_duration": total_duration}, open(f"ep_{letter}_duration.json", "w"), indent=2)
    json.dump(intro, open(f"ep_{letter}_intro.json", "w"), ensure_ascii=False, indent=2)
    json.dump(emphasis, open(f"ep_{letter}_emphasis.json", "w"), ensure_ascii=False, indent=2)
    json.dump([], open(f"ep_{letter}_stock_cutaways.json", "w"))
    print(f"ep{letter}: OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode A (new host: gray-shirt boy, 18.040s): closing a task with the
# right answer can mean forgetting the solution method within a day; the
# app's text breakdown stays on hand for reviewing the method
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗАКРЫЛ ЗАДАНИЕ", "НО ЗАБЫЛ СПОСОБ?"], "end": 1.68}
a_cards = [
    {"start": 1.68, "end": 2.52, "lines": [{"text": "МОЖНО ПРАВИЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ЗАКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 2.52, "end": 3.54, "lines": [{"text": "И ЗАБЫТЬ", "accent": False, "size": "small"}, {"text": "ОТВЕТОМ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.41, "lines": [{"text": "СПОСОБ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 5.34, "lines": [{"text": "УЖЕ ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 5.34, "end": 6.60, "lines": [{"text": "Я ТАК ТЕСТЫ", "accent": False, "size": "small"}, {"text": "ПРОХОДИЛ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 7.77, "lines": [{"text": "ПАЧКАМИ", "accent": False, "size": "small"}, {"text": "ПОХОЖЕЕ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 8.79, "lines": [{"text": "ЗАДАНИЯ ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 8.79, "end": 9.66, "lines": [{"text": "НЕ МЕНЯ В", "accent": False, "size": "small"}, {"text": "ПОСТАВИЛО", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 10.83, "lines": [{"text": "СНОВА", "accent": False, "size": "small"}, {"text": "ТУПИК", "accent": True, "size": "big"}]},
    {"start": 10.83, "end": 11.64, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.64, "end": 12.51, "lines": [{"text": "К ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.65, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.52, "lines": [{"text": "КОТОРЫЙ ПОД", "accent": False, "size": "small"}, {"text": "РУКОЙ", "accent": True, "size": "big"}]},
    {"start": 14.52, "end": 16.26, "lines": [{"text": "ДЛЯ СПОСОБА", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 18.040, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 1.68, "end": 2.01}, {"start": 10.83, "end": 11.16}, {"start": 16.26, "end": 16.59}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (gray-shirt boy, 18.263s): a history date perfectly learned
# the night before can vanish right before the mock exam; the app's
# memorization games lock a date in over several days, not one night
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ИДЕАЛЬНО ВЫУЧЕННАЯ", "НАКАНУНЕ ДАТА?"], "end": 1.95}
b_cards = [
    {"start": 1.95, "end": 2.76, "lines": [{"text": "ДАТА ПО", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 2.76, "end": 3.96, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "СТЕРЕТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 4.83, "lines": [{"text": "ИЗ ПРЯМО", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 5.73, "lines": [{"text": "ПЕРЕД", "accent": False, "size": "small"}, {"text": "ПРОБНИКОМ", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 6.57, "lines": [{"text": "Я ПО", "accent": False, "size": "small"}, {"text": "ГОТОВИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 6.57, "end": 7.38, "lines": [{"text": "ДАТАМ ВСЮ", "accent": False, "size": "small"}, {"text": "НОЧЬ", "accent": True, "size": "big"}]},
    {"start": 7.38, "end": 8.55, "lines": [{"text": "ПЕРЕД ПРОБНЫМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНОМ", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.69, "lines": [{"text": "И ПОЛОВИНУ", "accent": False, "size": "small"}, {"text": "ЗАБЫЛ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 10.65, "lines": [{"text": "УЖЕ ЗА", "accent": False, "size": "small"}, {"text": "ЗАВТРАКОМ", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 11.46, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.46, "end": 12.30, "lines": [{"text": "ПО ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.30, "end": 13.29, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.29, "end": 14.31, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "big"}]},
    {"start": 14.31, "end": 15.15, "lines": [{"text": "ЗА НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "ДАТУ", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 16.56, "lines": [{"text": "ДНЕЙ А НЕ ЗА ОДНУ", "accent": False, "size": "small"}, {"text": "НОЧЬ", "accent": True, "size": "big"}]},
    {"start": 16.56, "end": 18.263, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.95, "end": 2.28}, {"start": 10.65, "end": 10.98}, {"start": 16.56, "end": 16.89}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (gray-shirt boy, 17.730s): a task collection inherited from an
# older sibling doesn't always get checked for staleness in time; the
# app's FIPI bank updates under the current year
# ---------------------------------------------------------------------------
c_intro = {"lines": ["СБОРНИК ОТ БРАТА", "ДО СИХ ПОР АКТУАЛЕН?"], "end": 2.01}
c_cards = [
    {"start": 2.01, "end": 2.94, "lines": [{"text": "СБОРНИК", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 2.94, "end": 3.87, "lines": [{"text": "НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 5.22, "lines": [{"text": "СТОИТ НА АКТУАЛЬНОСТЬ", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 5.22, "end": 6.06, "lines": [{"text": "ВОВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.14, "lines": [{"text": "Я ТАКОЙ РЕШАЛ", "accent": False, "size": "small"}, {"text": "СБОРНИК", "accent": True, "size": "big"}]},
    {"start": 7.14, "end": 7.95, "lines": [{"text": "ПОЛОВИНУ", "accent": False, "size": "small"}, {"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.21, "lines": [{"text": "ПОКА НЕ УЧИТЕЛЬ", "accent": False, "size": "small"}, {"text": "ПОКАЗАЛ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.14, "lines": [{"text": "ФОРМАТ", "accent": False, "size": "small"}, {"text": "ИЗМЕНИВШИЙСЯ", "accent": True, "size": "small"}]},
    {"start": 10.14, "end": 11.31, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "КОНСУЛЬТАЦИИ", "accent": True, "size": "small"}]},
    {"start": 11.31, "end": 12.21, "lines": [{"text": "В ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.21, "end": 13.20, "lines": [{"text": "ФИПИ", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.34, "lines": [{"text": "С КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 14.34, "end": 15.57, "lines": [{"text": "ОБНОВЛЯЮТСЯ ПОД", "accent": False, "size": "small"}, {"text": "ТЕКУЩИЙ", "accent": True, "size": "big"}]},
    {"start": 15.57, "end": 16.38, "lines": [{"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 16.38, "end": 17.730, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.01, "end": 2.34}, {"start": 11.31, "end": 11.64}, {"start": 16.38, "end": 16.71}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (new host: mother, 21.960s): a daughter can know grammar rules
# by heart and still make mistakes in specific words; the app's
# memorization games reinforce rules on concrete words, not just theory
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАЕТ ПРАВИЛА", "НО ОШИБАЕТСЯ?"], "end": 2.04}
d_cards = [
    {"start": 2.04, "end": 3.06, "lines": [{"text": "ЕГЭ МОЖЕТ", "accent": False, "size": "small"}, {"text": "ДОЧЬ", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 3.96, "lines": [{"text": "ЗНАТЬ", "accent": False, "size": "small"}, {"text": "НАИЗУСТЬ", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 5.10, "lines": [{"text": "И ВСЕ", "accent": False, "size": "small"}, {"text": "ОШИБАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 6.75, "lines": [{"text": "В КОНКРЕТНЫХ", "accent": False, "size": "small"}, {"text": "СЛОВАХ", "accent": True, "size": "big"}]},
    {"start": 6.75, "end": 7.77, "lines": [{"text": "Я КАК ОНА", "accent": False, "size": "small"}, {"text": "СЛУШАЛА", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 8.97, "lines": [{"text": "ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "БЕЗУПРЕЧНО", "accent": True, "size": "big"}]},
    {"start": 8.97, "end": 10.05, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 10.89, "lines": [{"text": "ВИДЕЛА", "accent": False, "size": "small"}, {"text": "ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 10.89, "end": 12.72, "lines": [{"text": "ТОМ ЖЕ В ТЕТРАДИ", "accent": False, "size": "small"}, {"text": "СЛОВЕ", "accent": True, "size": "big"}]},
    {"start": 12.72, "end": 13.56, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.56, "end": 14.76, "lines": [{"text": "ПО ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 14.76, "end": 16.08, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.08, "end": 17.07, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 18.12, "lines": [{"text": "ПРАВИЛА НА", "accent": False, "size": "small"}, {"text": "КОНКРЕТНЫХ", "accent": True, "size": "big"}]},
    {"start": 18.12, "end": 19.20, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "СЛОВАХ", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.19, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТЕОРИИ", "accent": True, "size": "big"}]},
    {"start": 20.19, "end": 21.960, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.04, "end": 2.37}, {"start": 12.72, "end": 13.05}, {"start": 20.19, "end": 20.52}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (mother, 19.820s): a daughter can pass a mock exam with a good
# score and not be able to retell a single solution; the app's text
# breakdown stays on hand right after solving, not just before
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ДОЧЬ СДАЛА ПРОБНИК", "НО НЕ СМОГЛА ПЕРЕСКАЗАТЬ?"], "end": 1.83}
e_cards = [
    {"start": 1.83, "end": 3.18, "lines": [{"text": "ПО ХОРОШИМ", "accent": False, "size": "small"}, {"text": "БАЛЛОМ", "accent": True, "size": "big"}]},
    {"start": 3.18, "end": 4.29, "lines": [{"text": "И НЕ ПЕРЕСКАЗАТЬ", "accent": False, "size": "small"}, {"text": "СУМЕТЬ", "accent": True, "size": "big"}]},
    {"start": 4.29, "end": 6.24, "lines": [{"text": "НИ ОДНО", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.24, "end": 7.14, "lines": [{"text": "Я ЗА", "accent": False, "size": "small"}, {"text": "ПОРАДОВАЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 7.14, "end": 7.95, "lines": [{"text": "А ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "БАЛЫ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 8.76, "lines": [{"text": "НЕДЕЛЮ НЕ", "accent": False, "size": "small"}, {"text": "ДОЧЬ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.84, "lines": [{"text": "ВСПОМНИЛА КАК", "accent": False, "size": "small"}, {"text": "РЕШАЛА", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 11.73, "lines": [{"text": "ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ПОЛОВИНУ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 12.63, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 13.62, "lines": [{"text": "К ЗАДАНИЮ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 14.91, "lines": [{"text": "ЕСТЬ РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 15.75, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОСТАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 15.75, "end": 16.86, "lines": [{"text": "ПОД УЖЕ ПОСЛЕ", "accent": False, "size": "small"}, {"text": "РУКОЙ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 17.82, "lines": [{"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 17.82, "end": 19.820, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.83, "end": 2.16}, {"start": 11.73, "end": 12.06}, {"start": 17.82, "end": 18.15}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (mother, 17.520s): preparing from a five-year-old study guide
# can take a long time in the wrong direction; the app's FIPI bank is
# updated to the current year's requirements
# ---------------------------------------------------------------------------
f_intro = {"lines": ["МЕТОДИЧКА", "ПЯТИЛЕТНЕЙ ДАВНОСТИ?"], "end": 1.56}
f_cards = [
    {"start": 1.56, "end": 3.03, "lines": [{"text": "МЕТОДИЧКЕ ПЯТИЛЕТНЕЙ", "accent": False, "size": "small"}, {"text": "ДАВНОСТИ", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 3.84, "lines": [{"text": "МОЖНО И", "accent": False, "size": "small"}, {"text": "ДОЛГО", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 5.43, "lines": [{"text": "НЕ ТУДА", "accent": False, "size": "small"}, {"text": "СОВЕРШЕННО", "accent": True, "size": "big"}]},
    {"start": 5.43, "end": 6.30, "lines": [{"text": "Я У ДОЧЕРИ", "accent": False, "size": "small"}, {"text": "НАШЛА", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.62, "lines": [{"text": "ИМЕННО ТАКУЮ", "accent": False, "size": "small"}, {"text": "МЕТОДИЧКУ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.85, "lines": [{"text": "И ТОЛЬКО ТОГДА", "accent": False, "size": "small"}, {"text": "ПОНЯЛА", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 9.72, "lines": [{"text": "ОТКУДА", "accent": False, "size": "small"}, {"text": "СТРАННЫЕ", "accent": True, "size": "big"}]},
    {"start": 9.72, "end": 11.25, "lines": [{"text": "РЕЗУЛЬТАТЫ НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКАХ", "accent": True, "size": "big"}]},
    {"start": 11.25, "end": 12.12, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 13.20, "lines": [{"text": "СОБРАН", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.46, "lines": [{"text": "ПО ТРЕБОВАНИЯ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЕННЫЙ", "accent": True, "size": "small"}]},
    {"start": 14.46, "end": 15.66, "lines": [{"text": "ТЕКУЩЕГО", "accent": False, "size": "small"}, {"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 17.520, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.56, "end": 1.89}, {"start": 11.25, "end": 11.58}, {"start": 15.66, "end": 15.99}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
