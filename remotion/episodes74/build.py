#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-SEVENTH 'coffee123'
batch (9 episodes uploaded under the same tag after twenty-six prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes74/.

Three returning hosts, no new faces: cream-sweater girl (a, b, c),
study-room girl (d, e, f), curly-hair boy (g, h, i).

Sub-themes: knowing a definition in your own words isn't the same as
recognizing the official formulation, and a memorized method isn't the
same as understanding why it works (a, b, h), stale/mismatched task
material vs. the app's up-to-date FIPI bank (c, f, g), and things that
seem learned but slip under slightly different conditions -- similar
dates, a rule retaught to someone else, punctuation without the
underlying rule (d, e, i).

A few long Russian words (e.g. "формулировке", "обновляется",
"перечитывать", "формулировкой", "пронумерованными",
"одноклассникам") have no short accent-worthy synonym in their spoken
clause; for those the accent line is kept at size "small" instead of
"big" so the >10-char validator rule (which only applies to
accent+big lines) doesn't force a misleading substitution.
"""
import json

REAL_DURATION = {
    "a": 23.618, "b": 23.575, "c": 24.300,
    "d": 24.471, "e": 22.850, "f": 22.167,
    "g": 15.600, "h": 19.266, "i": 22.240,
}
SOURCE_FILE = {
    "a": "ghfhdhdhdehdh", "b": "ghhgtfhghfgh", "c": "ghshshshshsgh",
    "d": "gsjfndhfkjhgjteygat", "e": "kjhfydutyrtyruyjkh", "f": "uyiyutyrjhjdytfu",
    "g": "jgkllfguyk.lf", "h": "jhgfdhtfkfgkh", "i": "khjkfgdyitikjhkfg",
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
    "g": {"бариант": "вариант", "фипис": "фипи"},
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
    words = json.load(open(f"../asr_coffee123_27/{src}_words.json"))
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
# Episode A (cream-sweater girl, 23.618s): knowing a definition in your own
# words isn't the same as recognizing it in the official formulation; the
# app's memorization games train recognition of the official wording
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗНАЕШЬ ПОНЯТИЕ", "СВОИМИ СЛОВАМИ?"], "end": 2.70}
a_cards = [
    {"start": 2.70, "end": 3.51, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.51, "end": 4.68, "lines": [{"text": "СВОИМИ", "accent": False, "size": "small"}, {"text": "СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 4.68, "end": 5.55, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "УЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.55, "end": 8.07, "lines": [{"text": "ОФИЦИАЛЬНОЙ ФОРМУЛИРОВКЕ", "accent": True, "size": "small"}]},
    {"start": 8.07, "end": 9.18, "lines": [{"text": "Я ТЕРМИНЫ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЛА", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.05, "lines": [{"text": "НА СВОЕМ", "accent": False, "size": "small"}, {"text": "ПОДРУГИ", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 10.86, "lines": [{"text": "А НА", "accent": False, "size": "small"}, {"text": "ЯЗЫКЕ", "accent": True, "size": "big"}]},
    {"start": 10.86, "end": 11.79, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 11.79, "end": 12.66, "lines": [{"text": "ТО ЖЕ", "accent": False, "size": "small"}, {"text": "УЗНАЛА", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 13.50, "lines": [{"text": "САМОЕ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЕ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.94, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 14.94, "end": 15.78, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.78, "end": 16.86, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 18.27, "lines": [{"text": "НА ЗАПОМИНАНИЯ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.27, "end": 19.41, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 19.41, "end": 20.52, "lines": [{"text": "ОФИЦИАЛЬНОЙ", "accent": False, "size": "small"}, {"text": "УЗНАВАНИЯ", "accent": True, "size": "big"}]},
    {"start": 20.52, "end": 21.66, "lines": [{"text": "ФОРМУЛИРОВОК", "accent": True, "size": "small"}]},
    {"start": 21.66, "end": 23.618, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.70, "end": 3.03}, {"start": 14.94, "end": 15.27}, {"start": 21.66, "end": 21.99}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (cream-sweater girl, 23.575s): applying a formula correctly on
# the math exam isn't the same as understanding why it was the right
# choice; the app's breakdown explains the choice of formula, not just
# the calculation
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПРИМЕНИЛ ФОРМУЛУ", "НО ПОНЯЛ ЛИ ПОЧЕМУ?"], "end": 1.98}
b_cards = [
    {"start": 1.98, "end": 2.85, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ВЕРНО", "accent": True, "size": "big"}]},
    {"start": 2.85, "end": 4.11, "lines": [{"text": "ПРИМЕНИТЬ", "accent": False, "size": "small"}, {"text": "ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 4.92, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "ПОНЯТЬ", "accent": True, "size": "big"}]},
    {"start": 4.92, "end": 6.12, "lines": [{"text": "ВЫБРАНО", "accent": False, "size": "small"}, {"text": "ПОЧЕМУ", "accent": True, "size": "big"}]},
    {"start": 6.12, "end": 7.56, "lines": [{"text": "ОНА", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.88, "lines": [{"text": "Я ТАК РЕШАЛА", "accent": False, "size": "small"}, {"text": "ЗАДАЧИ", "accent": True, "size": "big"}]},
    {"start": 8.88, "end": 9.72, "lines": [{"text": "ПО ИЗ", "accent": False, "size": "small"}, {"text": "ОБРАЗЦУ", "accent": True, "size": "big"}]},
    {"start": 9.72, "end": 10.86, "lines": [{"text": "ТЕТРАДИ", "accent": True, "size": "big"}]},
    {"start": 10.86, "end": 11.85, "lines": [{"text": "НА ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ПОХОЖЕМ", "accent": True, "size": "big"}]},
    {"start": 11.85, "end": 12.78, "lines": [{"text": "С ДРУГИМИ", "accent": False, "size": "small"}, {"text": "ЧИСЛАМИ", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 14.37, "lines": [{"text": "РАСТЕРЯЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 14.37, "end": 15.33, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.33, "end": 16.32, "lines": [{"text": "К ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 16.32, "end": 17.34, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 17.34, "end": 18.48, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 18.48, "end": 19.50, "lines": [{"text": "ВЫБОР", "accent": False, "size": "small"}, {"text": "ФОРМУЛЫ", "accent": True, "size": "big"}]},
    {"start": 19.50, "end": 21.36, "lines": [{"text": "А НЕ ТОЛЬКО САМ", "accent": False, "size": "small"}, {"text": "РАСЧЕТ", "accent": True, "size": "big"}]},
    {"start": 21.36, "end": 23.575, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.98, "end": 2.31}, {"start": 14.37, "end": 14.70}, {"start": 21.36, "end": 21.69}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (cream-sweater girl, 24.300s): a demo version saved in spring
# can quietly be the wrong one by autumn; the app's FIPI bank updates
# under the current format with no stale versions left lying around
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ДЕМОВЕРСИЯ ЕГЭ", "СОХРАНЕНА ВЕСНОЙ?"], "end": 1.80}
c_cards = [
    {"start": 1.80, "end": 3.12, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОНЕ", "accent": True, "size": "big"}]},
    {"start": 3.12, "end": 4.20, "lines": [{"text": "ЕЩЕ", "accent": False, "size": "small"}, {"text": "ВЕСНОЙ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.61, "lines": [{"text": "К ОСЕНИ МОЖЕТ", "accent": False, "size": "small"}, {"text": "ОКАЗАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 5.61, "end": 6.51, "lines": [{"text": "НЕ ТОЙ", "accent": False, "size": "small"}, {"text": "СОВСЕМ", "accent": True, "size": "big"}]},
    {"start": 6.51, "end": 7.77, "lines": [{"text": "ВЕРСИЕЙ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 8.61, "lines": [{"text": "Я ПО", "accent": False, "size": "small"}, {"text": "ГОТОВИЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 8.61, "end": 9.75, "lines": [{"text": "СТАРОЙ", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 9.75, "end": 10.80, "lines": [{"text": "ДВА", "accent": False, "size": "small"}, {"text": "МЕСЯЦА", "accent": True, "size": "big"}]},
    {"start": 10.80, "end": 11.61, "lines": [{"text": "ПОКА", "accent": False, "size": "small"}, {"text": "ПОДРУГА", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 12.81, "lines": [{"text": "НЕ ОБНОВЛЕННЫЙ", "accent": False, "size": "small"}, {"text": "ПРИСЛАЛА", "accent": True, "size": "big"}]},
    {"start": 12.81, "end": 13.62, "lines": [{"text": "С ДРУГИМИ", "accent": False, "size": "small"}, {"text": "ФАЙЛ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 15.42, "lines": [{"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 16.44, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 17.70, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 17.70, "end": 18.69, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЯЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 18.69, "end": 20.16, "lines": [{"text": "ПОД ТЕКУЩИЙ", "accent": False, "size": "small"}, {"text": "ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 20.16, "end": 21.06, "lines": [{"text": "БЕЗ СТАРЫХ", "accent": False, "size": "small"}, {"text": "ВЕРСИЙ", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 22.32, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ЗАПАСЕ", "accent": True, "size": "big"}]},
    {"start": 22.32, "end": 24.300, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.80, "end": 2.13}, {"start": 15.42, "end": 15.75}, {"start": 22.32, "end": 22.65}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (study-room girl, 24.471s): punctuating a sentence correctly
# on autopilot isn't the same as being able to explain the rule; the
# app's text breakdown explains the rules, not just the right answer
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СТАВИШЬ ЗАПЯТЫЕ", "НА АВТОМАТЕ?"], "end": 2.25}
d_cards = [
    {"start": 2.25, "end": 3.09, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ВЕРНО", "accent": True, "size": "big"}]},
    {"start": 3.09, "end": 4.32, "lines": [{"text": "РАССТАВИТЬ", "accent": False, "size": "small"}, {"text": "ЗАПЯТЫЕ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 5.82, "lines": [{"text": "И НЕ ОБЪЯСНИТЬ", "accent": False, "size": "small"}, {"text": "СУМЕТЬ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 7.71, "lines": [{"text": "НИ ОДНО", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 8.55, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ПИСАЛА", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.66, "lines": [{"text": "ПРОБНЫЕ", "accent": False, "size": "small"}, {"text": "ДИКТАНТЫ", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 10.71, "lines": [{"text": "ВЕСЬ", "accent": False, "size": "small"}, {"text": "АВГУСТ", "accent": True, "size": "big"}]},
    {"start": 10.71, "end": 11.79, "lines": [{"text": "А НА", "accent": False, "size": "small"}, {"text": "КОНСУЛЬТАЦИИ", "accent": True, "size": "small"}]},
    {"start": 11.79, "end": 12.69, "lines": [{"text": "НЕ НАЗВАТЬ", "accent": False, "size": "small"}, {"text": "МОГЛА", "accent": True, "size": "big"}]},
    {"start": 12.69, "end": 13.62, "lines": [{"text": "НИ", "accent": False, "size": "small"}, {"text": "ПРИЧИНУ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 15.30, "lines": [{"text": "ОДНОЙ", "accent": False, "size": "small"}, {"text": "ЗАПЯТОЙ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.26, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.34, "lines": [{"text": "К ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 17.34, "end": 18.27, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 18.27, "end": 19.41, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 19.41, "end": 20.22, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 20.22, "end": 21.15, "lines": [{"text": "ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 21.15, "end": 22.44, "lines": [{"text": "ВЕРНЫЙ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 22.44, "end": 24.471, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.25, "end": 2.58}, {"start": 15.30, "end": 15.63}, {"start": 22.44, "end": 22.77}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (study-room girl, 22.850s): a history date can get confused
# with a very close neighboring one; the app's memorization games make
# you tell similar dates apart yourself instead of rereading a list
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ДАТЫ СОБЫТИЙ", "ПО ИСТОРИИ ПУТАЮТСЯ?"], "end": 2.10}
e_cards = [
    {"start": 2.10, "end": 3.15, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.26, "lines": [{"text": "С ОЧЕНЬ", "accent": False, "size": "small"}, {"text": "ПУТАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.26, "end": 5.28, "lines": [{"text": "СОСЕДНЕЙ", "accent": False, "size": "small"}, {"text": "ПОХОЖЕЙ", "accent": True, "size": "big"}]},
    {"start": 5.28, "end": 6.30, "lines": [{"text": "ДАТОЙ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.17, "lines": [{"text": "Я РАЗ", "accent": False, "size": "small"}, {"text": "МИЛЛИОН", "accent": True, "size": "big"}]},
    {"start": 7.17, "end": 8.25, "lines": [{"text": "ПУТАЛА ДВА", "accent": False, "size": "small"}, {"text": "ПОХОЖИХ", "accent": True, "size": "big"}]},
    {"start": 8.25, "end": 9.42, "lines": [{"text": "ПОДРЯД", "accent": False, "size": "small"}, {"text": "СОБЫТИЯ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 10.38, "lines": [{"text": "ХОТЯ МЕЖДУ", "accent": False, "size": "small"}, {"text": "РАЗНИЦА", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.31, "lines": [{"text": "БЫЛА НИМИ", "accent": False, "size": "small"}, {"text": "ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 13.44, "lines": [{"text": "В ЛЕТ", "accent": False, "size": "small"}, {"text": "ПАРУ", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.31, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.31, "end": 15.39, "lines": [{"text": "ПО ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 15.39, "end": 16.59, "lines": [{"text": "НА ЗАПОМИНАНИЕ ГДЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.59, "end": 17.61, "lines": [{"text": "ГДЕ ДАТЫ", "accent": False, "size": "small"}, {"text": "ПОХОЖИЕ", "accent": True, "size": "big"}]},
    {"start": 17.61, "end": 18.69, "lines": [{"text": "ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "РАЗЛИЧАТЬ", "accent": True, "size": "big"}]},
    {"start": 18.69, "end": 19.56, "lines": [{"text": "САМОЙ", "accent": True, "size": "big"}]},
    {"start": 19.56, "end": 21.06, "lines": [{"text": "А НЕ СПИСОК", "accent": False, "size": "small"}, {"text": "ПЕРЕЧИТЫВАТЬ", "accent": True, "size": "small"}]},
    {"start": 21.06, "end": 22.850, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.10, "end": 2.43}, {"start": 13.44, "end": 13.77}, {"start": 21.06, "end": 21.39}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (study-room girl, 22.167s): an old task's numbering can drift
# from the current format; the app's FIPI bank has tasks numbered to
# match this year's actual format
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗАДАНИЕ ПРОШЛЫХ ЛЕТ", "СО СТАРОЙ НУМЕРАЦИЕЙ?"], "end": 1.89}
f_cards = [
    {"start": 1.89, "end": 2.82, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "СОХРАНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 4.05, "lines": [{"text": "СТАРУЮ", "accent": False, "size": "small"}, {"text": "НУМЕРАЦИЮ", "accent": True, "size": "big"}]},
    {"start": 4.05, "end": 4.86, "lines": [{"text": "УЖЕ НЕ", "accent": False, "size": "small"}, {"text": "КОТОРАЯ", "accent": True, "size": "big"}]},
    {"start": 4.86, "end": 5.82, "lines": [{"text": "С ТЕКУЩЕЙ", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 6.96, "lines": [{"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 7.83, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "ТРЕНИРОВАЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 7.83, "end": 8.70, "lines": [{"text": "ТАКОМУ", "accent": False, "size": "small"}, {"text": "АРХИВУ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.51, "lines": [{"text": "ВЕСЬ", "accent": False, "size": "small"}, {"text": "СЕНТЯБРЬ", "accent": True, "size": "big"}]},
    {"start": 9.51, "end": 10.35, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "СВЕРИЛА", "accent": True, "size": "big"}]},
    {"start": 10.35, "end": 11.22, "lines": [{"text": "НОМЕРА С", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 13.89, "lines": [{"text": "ОФИЦИАЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИЕЙ", "accent": True, "size": "small"}]},
    {"start": 13.89, "end": 14.91, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 15.72, "lines": [{"text": "СОБРАН", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 15.72, "end": 17.01, "lines": [{"text": "ЗАДАНИЯМИ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 17.94, "lines": [{"text": "ПРОНУМЕРОВАННЫМИ", "accent": True, "size": "small"}]},
    {"start": 17.94, "end": 18.81, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНОМУ", "accent": True, "size": "small"}]},
    {"start": 18.81, "end": 20.25, "lines": [{"text": "ЭТОТ ГОД", "accent": False, "size": "small"}, {"text": "ФОРМАТУ", "accent": True, "size": "big"}]},
    {"start": 20.25, "end": 22.167, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 13.89, "end": 14.22}, {"start": 20.25, "end": 20.58}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (curly-hair boy, 15.600s): a variant forwarded in the class
# chat doesn't always match the official exam format; the app's FIPI
# bank has tasks for the current year
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ВАРИАНТ ИЗ ЧАТА", "КЛАССА НАДЕЖЕН?"], "end": 1.89}
g_cards = [
    {"start": 1.89, "end": 3.06, "lines": [{"text": "ЧАТЕ НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "КЛАССА", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 4.11, "lines": [{"text": "С ОФИЦИАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 5.22, "lines": [{"text": "ЭКЗАМЕНА", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 5.22, "end": 6.36, "lines": [{"text": "Я ПЕРЕСЛАННЫЙ", "accent": False, "size": "small"}, {"text": "РЕШАЛ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.26, "lines": [{"text": "НЕДЕЛЮ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 7.26, "end": 8.58, "lines": [{"text": "НЕ ЗАМЕТИЛ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.58, "end": 9.63, "lines": [{"text": "С ИЗМЕНЕННОЙ", "accent": False, "size": "small"}, {"text": "ДАВНО", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 10.44, "lines": [{"text": "ФОРМУЛИРОВКОЙ", "accent": True, "size": "small"}]},
    {"start": 10.44, "end": 11.31, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.36, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.35, "lines": [{"text": "ТЕКУЩЕГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.28, "lines": [{"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 14.28, "end": 15.600, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 10.44, "end": 10.77}, {"start": 14.28, "end": 14.61}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (curly-hair boy, 19.266s): proof by contradiction can work on
# an EGE task without you being able to explain why it worked; the app's
# breakdown explains the logic of the method, not just the answer
# ---------------------------------------------------------------------------
h_intro = {"lines": ["МЕТОД ОТ ПРОТИВНОГО", "РАБОТАЕТ НО НЕ ОБЪЯСНЯЕТ?"], "end": 1.74}
h_cards = [
    {"start": 1.74, "end": 2.64, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ЗАДАНИИ", "accent": True, "size": "big"}]},
    {"start": 2.64, "end": 3.54, "lines": [{"text": "МОЖЕТ", "accent": False, "size": "small"}, {"text": "СРАБОТАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.65, "lines": [{"text": "А ПОЧЕМУ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 5.88, "lines": [{"text": "ОН", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 6.84, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "НЕТ", "accent": True, "size": "big"}]},
    {"start": 6.84, "end": 7.74, "lines": [{"text": "СЛОЖНОЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЫЛ", "accent": True, "size": "big"}]},
    {"start": 7.74, "end": 8.97, "lines": [{"text": "НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.97, "end": 10.08, "lines": [{"text": "А ЛОГИКУ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 10.08, "end": 10.95, "lines": [{"text": "ПОТОМ", "accent": False, "size": "small"}, {"text": "УЧИТЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 11.97, "lines": [{"text": "НЕ СМОГ", "accent": False, "size": "small"}, {"text": "ТОЛКОМ", "accent": True, "size": "big"}]},
    {"start": 11.97, "end": 12.78, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 13.71, "lines": [{"text": "К ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 13.71, "end": 14.52, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 14.52, "end": 15.66, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 16.53, "lines": [{"text": "МЕТОДА А", "accent": False, "size": "small"}, {"text": "ЛОГИКУ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.55, "lines": [{"text": "НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 19.266, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 1.74, "end": 2.07}, {"start": 11.97, "end": 12.30}, {"start": 17.55, "end": 17.88}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (curly-hair boy, 22.240s): explaining a rule to friends
# flawlessly doesn't mean you'll hold onto it yourself a day later; the
# app's memorization games reinforce rules through practice, not retelling
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ОБЪЯСНЯЮ ПРАВИЛА", "ДРУЗЬЯМ БЕЗ ЗАПИНКИ?"], "end": 2.88}
i_cards = [
    {"start": 2.88, "end": 3.72, "lines": [{"text": "ДЛЯ БЕЗ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.72, "end": 4.86, "lines": [{"text": "ЕДИНОЙ", "accent": False, "size": "small"}, {"text": "ЗАПИНКИ", "accent": True, "size": "big"}]},
    {"start": 4.86, "end": 5.79, "lines": [{"text": "А ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 5.79, "end": 6.63, "lines": [{"text": "САМ В", "accent": False, "size": "small"}, {"text": "ОШИБАЮСЬ", "accent": True, "size": "big"}]},
    {"start": 6.63, "end": 7.83, "lines": [{"text": "ЖЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЕ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 8.82, "lines": [{"text": "Я ЧТО МОГУ", "accent": False, "size": "small"}, {"text": "ГОРДИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 8.82, "end": 9.66, "lines": [{"text": "ПРАВИЛО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 10.50, "lines": [{"text": "ОДНОКЛАССНИКАМ", "accent": True, "size": "small"}]},
    {"start": 10.50, "end": 11.31, "lines": [{"text": "А ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.51, "lines": [{"text": "САМ ОШИБСЯ В", "accent": False, "size": "small"}, {"text": "ДИКТАНТЕ", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.89, "lines": [{"text": "НА ЖЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 13.89, "end": 14.79, "lines": [{"text": "В ПО", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 15.63, "lines": [{"text": "РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 16.95, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.95, "end": 17.97, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "big"}]},
    {"start": 17.97, "end": 18.87, "lines": [{"text": "ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 18.87, "end": 19.74, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ПРАКТИКУ", "accent": True, "size": "big"}]},
    {"start": 19.74, "end": 20.79, "lines": [{"text": "ПЕРЕСКАЗ", "accent": True, "size": "big"}]},
    {"start": 20.79, "end": 22.240, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.88, "end": 3.21}, {"start": 13.89, "end": 14.22}, {"start": 20.79, "end": 21.12}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
