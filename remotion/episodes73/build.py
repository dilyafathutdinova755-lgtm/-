#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-SIXTH 'coffee123'
batch (6 episodes uploaded under the same tag after twenty-five prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes73/.

Two returning hosts, no new faces: the study-room girl (a, b, c) and the
cream-sweater girl introduced in batch 26's predecessor rooms (d, e, f).
Sub-themes: an up-to-date FIPI bank/formulations vs. stale sborniks
(a, d), a correct answer that isn't real understanding (b, f), and
memorization games for terms/definitions that fade or get confused
(c, e).
"""
import json

REAL_DURATION = {
    "a": 25.410, "b": 24.236, "c": 20.760,
    "d": 18.903, "e": 22.764, "f": 21.612,
}
SOURCE_FILE = {
    "a": "bnfxg.gf", "b": "bvmgcxhmnhcgfv", "c": "nvncvnn.cfg",
    "d": "dfgfcfdhyfhdhdf", "e": "gfdgdgfdgfdgdg", "f": "nbvncfgmgfh",
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
    "d": {"перек": "перед"},
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
    words = json.load(open(f"../asr_coffee123_26/{src}_words.json"))
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
# Episode A (study-room girl, 25.410s): old sborniks for Russian can't keep
# up with how fast task wording changes; the app's FIPI bank stays current
# ---------------------------------------------------------------------------
a_intro = {"lines": ["СТАРЫЕ СБОРНИКИ", "ЕГЭ УСТАРЕЛИ?"], "end": 2.07}
a_cards = [
    {"start": 2.07, "end": 3.12, "lines": [{"text": "ФОРМУЛИРОВКИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 3.12, "end": 4.26, "lines": [{"text": "БЫСТРЕЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "МЕНЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.26, "end": 5.55, "lines": [{"text": "ОБНОВИТЬСЯ", "accent": False, "size": "small"}, {"text": "УСПЕВАЕТ", "accent": True, "size": "big"}]},
    {"start": 5.55, "end": 7.32, "lines": [{"text": "СТАРЫЕ", "accent": False, "size": "small"}, {"text": "СБОРНИКИ", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 8.13, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 8.94, "lines": [{"text": "РЕШАЛА", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 9.84, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "СКАЧАЛА", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 11.19, "lines": [{"text": "ЕЩЕ В ПРОШЛОМ", "accent": False, "size": "small"}, {"text": "ГОДУ", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 12.48, "lines": [{"text": "И НА КОНСУЛЬТАЦИИ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 12.48, "end": 13.50, "lines": [{"text": "ЧТО ЧАСТЬ", "accent": False, "size": "small"}, {"text": "УЗНАЛА", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 17.07, "lines": [{"text": "ТАМ УЖЕ НЕ ВСТРЕЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 18.06, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 18.06, "end": 18.87, "lines": [{"text": "СОБРАН", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 18.87, "end": 20.19, "lines": [{"text": "АКТУАЛЬНЫМИ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 20.19, "end": 21.69, "lines": [{"text": "НА ЭТОТ ЗАДАНИЯМИ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 21.69, "end": 23.25, "lines": [{"text": "УСТАРЕВШИХ ФОРМУЛИРОВОК", "accent": False, "size": "small"}, {"text": "БЕЗ", "accent": True, "size": "big"}]},
    {"start": 23.25, "end": 25.410, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.07, "end": 2.40}, {"start": 17.07, "end": 17.40}, {"start": 23.25, "end": 23.58}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (study-room girl, 24.236s): a correct answer isn't the same as
# understanding why it's correct; the app's text breakdown explains the
# logic of the solution, not just the answer
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПРАВИЛЬНЫЙ ОТВЕТ", "ЭТО НЕ ПОНИМАНИЕ?"], "end": 1.98}
b_cards = [
    {"start": 1.98, "end": 3.39, "lines": [{"text": "МОЖЕТ БЫТЬ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНЫМ", "accent": True, "size": "big"}]},
    {"start": 3.39, "end": 4.71, "lines": [{"text": "А ПОЧЕМУ", "accent": False, "size": "small"}, {"text": "ПОНИМАНИЕ", "accent": True, "size": "big"}]},
    {"start": 4.71, "end": 5.85, "lines": [{"text": "ОН", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 6.90, "lines": [{"text": "НЕТ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.98, "lines": [{"text": "БУКВУ", "accent": False, "size": "small"}, {"text": "УГАДЫВАЛА", "accent": True, "size": "big"}]},
    {"start": 7.98, "end": 9.15, "lines": [{"text": "СЛОВЕ И", "accent": False, "size": "small"}, {"text": "РАДОВАЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.11, "lines": [{"text": "СОВПАДЕНИЮ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.16, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "ВСТРЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 12.15, "lines": [{"text": "ПОХОЖЕЕ", "accent": False, "size": "small"}, {"text": "СЛОВО", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 14.01, "lines": [{"text": "С ДРУГИМ", "accent": False, "size": "small"}, {"text": "ПРАВИЛОМ", "accent": True, "size": "big"}]},
    {"start": 14.01, "end": 15.30, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.38, "lines": [{"text": "К ЗАДАНИЮ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 16.38, "end": 17.31, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 17.31, "end": 18.51, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 18.51, "end": 19.59, "lines": [{"text": "ЛОГИКУ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 19.59, "end": 20.52, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 20.52, "end": 21.42, "lines": [{"text": "ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 21.42, "end": 22.29, "lines": [{"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 22.29, "end": 24.236, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.98, "end": 2.31}, {"start": 14.01, "end": 14.34}, {"start": 22.29, "end": 22.62}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (study-room girl, 20.760s): a history term learned in the
# evening can be forgotten by the next day's lunch; the app's memorization
# games make you recall it yourself instead of picking it from hints
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ВЫУЧИЛ ТЕРМИН ВЕЧЕРОМ", "А УЖЕ ЗАБЫЛ?"], "end": 2.10}
c_cards = [
    {"start": 2.10, "end": 3.33, "lines": [{"text": "МОЖНО ВЕЧЕРОМ", "accent": False, "size": "small"}, {"text": "ВЫУЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 3.33, "end": 4.50, "lines": [{"text": "И УЖЕ ЗАБЫТЬ К", "accent": False, "size": "small"}, {"text": "ОБЕДУ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.73, "lines": [{"text": "ДНЯ", "accent": False, "size": "small"}, {"text": "СЛЕДУЮЩЕГО", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 6.96, "lines": [{"text": "БЫЛО У МЕНЯ", "accent": False, "size": "small"}, {"text": "ТАК", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 8.19, "lines": [{"text": "ОПРЕДЕЛЕНИЕ", "accent": False, "size": "small"}, {"text": "ПРОЧИТАЛА", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.00, "lines": [{"text": "РАЗ", "accent": False, "size": "small"}, {"text": "ПЯТЬ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.17, "lines": [{"text": "НА ВСПОМНИТЬ", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 10.17, "end": 11.70, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.54, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.54, "end": 13.59, "lines": [{"text": "ПО ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 14.79, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 15.72, "lines": [{"text": "ГДЕ НУЖНО", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 15.72, "end": 17.01, "lines": [{"text": "САМОМУ", "accent": False, "size": "small"}, {"text": "ВСПОМНИТЬ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 18.87, "lines": [{"text": "А НЕ УЗНАТЬ СРЕДИ", "accent": False, "size": "small"}, {"text": "ПОДСКАЗОК", "accent": True, "size": "big"}]},
    {"start": 18.87, "end": 20.760, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.10, "end": 2.43}, {"start": 11.70, "end": 12.03}, {"start": 18.87, "end": 19.20}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (cream-sweater girl, 18.903s): having two task collections
# doesn't guarantee up-to-date material if one carries old wording; the
# app's single FIPI bank matches this year's actual wording
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ДВА СБОРНИКА", "ЕГЭ ДОМА?"], "end": 1.98}
d_cards = [
    {"start": 1.98, "end": 2.82, "lines": [{"text": "ЕЩЕ НЕ", "accent": False, "size": "small"}, {"text": "ДОМА", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 3.66, "lines": [{"text": "РАССЛАБИТЬСЯ", "accent": False, "size": "small"}, {"text": "ПОВОД", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 4.62, "lines": [{"text": "АКТУАЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "НАСЧЕТ", "accent": True, "size": "big"}]},
    {"start": 4.62, "end": 5.79, "lines": [{"text": "МАТЕРИАЛА", "accent": True, "size": "big"}]},
    {"start": 5.79, "end": 6.72, "lines": [{"text": "Я ОБА", "accent": False, "size": "small"}, {"text": "ЧЕРЕДОВАЛА", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 8.10, "lines": [{"text": "ПЕРЕД ПРОБНИКОМ", "accent": False, "size": "small"}, {"text": "СБОРНИКА", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 8.91, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 8.91, "end": 9.93, "lines": [{"text": "В ИЗ НИХ", "accent": False, "size": "small"}, {"text": "ОДНОМ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 11.73, "lines": [{"text": "ФОРМУЛИРОВКИ ПРОШЛЫХ", "accent": False, "size": "small"}, {"text": "ЛЕТ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 12.75, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 13.83, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ОДИН", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 15.12, "lines": [{"text": "С АКТУАЛЬНЫМИ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.29, "lines": [{"text": "ФОРМУЛИРОВКАМИ", "accent": False, "size": "small"}, {"text": "ТЕКУЩЕГО", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 17.43, "lines": [{"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 18.903, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.98, "end": 2.31}, {"start": 11.73, "end": 12.06}, {"start": 17.43, "end": 17.76}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (cream-sweater girl, 22.764s): definitions in obshestvoznanie
# are easy to mix up when read one after another; the app's memorization
# games make you tell similar terms apart without ready-made hints
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ПУТАЕШЬ ОПРЕДЕЛЕНИЯ", "ПО ОБЩЕСТВОЗНАНИЮ?"], "end": 2.34}
e_cards = [
    {"start": 2.34, "end": 3.21, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ЛЕГКО", "accent": True, "size": "big"}]},
    {"start": 3.21, "end": 4.08, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.07, "lines": [{"text": "ЕСЛИ", "accent": False, "size": "small"}, {"text": "СОБОЙ", "accent": True, "size": "big"}]},
    {"start": 5.07, "end": 5.94, "lines": [{"text": "ПРОСТО ИХ", "accent": False, "size": "small"}, {"text": "ЧИТАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.94, "end": 7.05, "lines": [{"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 8.10, "lines": [{"text": "Я ПОХОЖИЕ", "accent": False, "size": "small"}, {"text": "ПУТАЛА", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.24, "lines": [{"text": "НА ПРОБНИКИ", "accent": False, "size": "small"}, {"text": "ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 9.24, "end": 10.11, "lines": [{"text": "ХОТЯ", "accent": False, "size": "small"}, {"text": "НАКАНУНЕ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.22, "lines": [{"text": "БЫЛА ЧТО", "accent": False, "size": "small"}, {"text": "УВЕРЕНА", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.90, "lines": [{"text": "ЧТО ВСЕ", "accent": False, "size": "small"}, {"text": "ПОМНЮ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.64, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.64, "end": 16.50, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЯ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.43, "lines": [{"text": "ГДЕ НУЖНО", "accent": False, "size": "small"}, {"text": "ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 19.05, "lines": [{"text": "САМОСТОЯТЕЛЬНО", "accent": False, "size": "small"}, {"text": "РАЗЛИЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 19.05, "end": 20.73, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПОДСКАЗОК", "accent": True, "size": "big"}]},
    {"start": 20.73, "end": 22.764, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.34, "end": 2.67}, {"start": 12.90, "end": 13.23}, {"start": 20.73, "end": 21.06}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (cream-sweater girl, 21.612s): intuition on the math exam can
# get a task right once and fail on a similar one days later; the app's
# text breakdown explains the step-by-step logic, not just the final answer
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ИНТУИЦИЯ НА", "МАТЕМАТИКЕ ПОДВОДИТ?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.82, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ИНТУИЦИЯ", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 4.08, "lines": [{"text": "ПОДСКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ВЕРНО", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.13, "lines": [{"text": "А", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 5.13, "end": 6.36, "lines": [{"text": "СОВСЕМ", "accent": False, "size": "small"}, {"text": "НЕТ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.29, "lines": [{"text": "Я РЕШИЛА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 8.28, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ОЩУЩЕНИЮ", "accent": True, "size": "big"}]},
    {"start": 8.28, "end": 9.21, "lines": [{"text": "ПОЛУЧИЛА", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.02, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 10.02, "end": 10.92, "lines": [{"text": "СМОГЛА", "accent": False, "size": "small"}, {"text": "ПОВТОРИТЬ", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 12.33, "lines": [{"text": "ЭТО НА", "accent": False, "size": "small"}, {"text": "ПОХОЖЕМ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.50, "lines": [{"text": "ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.43, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.43, "end": 15.33, "lines": [{"text": "К ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 15.33, "end": 16.29, "lines": [{"text": "ТЕКСТОВЫЙ С", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 17.34, "lines": [{"text": "ЛОГИКОЙ", "accent": False, "size": "small"}, {"text": "ПОШАГОВОЙ", "accent": True, "size": "big"}]},
    {"start": 17.34, "end": 18.21, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.05, "lines": [{"text": "ТОЛЬКО", "accent": False, "size": "small"}, {"text": "КОНЕЧНЫЙ", "accent": True, "size": "big"}]},
    {"start": 19.05, "end": 20.07, "lines": [{"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 20.07, "end": 21.612, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.86, "end": 2.19}, {"start": 13.50, "end": 13.83}, {"start": 20.07, "end": 20.40}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
