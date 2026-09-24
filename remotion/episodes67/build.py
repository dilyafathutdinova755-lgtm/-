#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-SECOND 'coffee123'
batch (6 episodes uploaded under the same tag after twenty-one prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes67/.

Three returning hosts, no new faces: the mother (parent POV, a, b),
the curly-haired boy (c, d, f), and the wavy-haired living-room boy
(e). Sub-themes: a detailed text breakdown that reveals a recurring or
systemic mistake instead of a one-off (a, d), an up-to-date FIPI bank
sourced from real exam compilers instead of variants of unknown/random
origin (b, c), memorization games for active recall/application
instead of passive rereading (e, f).
"""
import json

REAL_DURATION = {
    "a": 19.052, "b": 17.154, "c": 16.108,
    "d": 17.440, "e": 19.160, "f": 18.200,
}
SOURCE_FILE = {
    "a": "sssssssssssssssssssssssssssss", "b": "ssssssssssssssssssssssssssssssssssssssss",
    "c": "tutrujrytjtgjfgjtj", "d": "tuuutrututu",
    "e": "ytujtjyhgfjytjytj", "f": "ytuuytutuytutu",
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


def fix_words(letter, words):
    """Repair known sherpa-onnx ASR mis-transcriptions before captioning."""
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_22/{src}_words.json"))
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
# Episode A (mother, 19.052s): it's hard for a parent to notice from
# outside that a child keeps making the same type of mistake, since a good
# overall score on other tasks masks it; the app's breakdown shows the
# recurring mistakes
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ТРУДНО ЗАМЕТИТЬ", "ЧТО РЕБЕНОК ПОВТОРЯЕТ ОШИБКУ?"], "end": 1.77}
a_cards = [
    {"start": 1.89, "end": 2.82, "lines": [{"text": "СО СТОРОНЫ ЧТО", "accent": False, "size": "small"}, {"text": "РЕБЕНОК", "accent": True, "size": "big"}]},
    {"start": 3.09, "end": 4.08, "lines": [{"text": "РАЗ ЗА РАЗОМ", "accent": False, "size": "small"}, {"text": "ОШИБАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 5.07, "lines": [{"text": "В ОДНОМ И ТОМ ЖЕ", "accent": False, "size": "small"}, {"text": "ТИПЕ", "accent": True, "size": "big"}]},
    {"start": 5.22, "end": 6.01, "lines": [{"text": "ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 7.23, "lines": [{"text": "ОБЫЧНЫЙ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 8.25, "lines": [{"text": "ОТВЕТ В ДРУГИХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯХ", "accent": True, "size": "big"}]},
    {"start": 8.46, "end": 9.75, "lines": [{"text": "ЭТУ ПРОБЛЕМУ ЛЕГКО", "accent": False, "size": "small"}, {"text": "СКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.58, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ К", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 11.67, "end": 13.71, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.95, "end": 14.76, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 16.47, "lines": [{"text": "ТАКИЕ ПОВТОРЯЮЩИЕСЯ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 19.052, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 10.38, "end": 10.71}, {"start": 17.19, "end": 17.52}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (mother, 17.154s): parents rarely think about where the
# variants their child trains on actually come from, and much of the free
# material online is stale; the app's bank is sourced from the actual exam
# compilers
# ---------------------------------------------------------------------------
b_intro = {"lines": ["НЕ ЗНАЕШЬ ОТКУДА", "ВЗЯТЫ ВАРИАНТЫ ЕГЭ?"], "end": 1.83}
b_cards = [
    {"start": 1.92, "end": 4.02, "lines": [{"text": "ЗАДУМЫВАЮТСЯ ОТКУДА ВЗЯТЫ ВАРИАНТЫ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.14, "end": 5.34, "lines": [{"text": "ПО КОТОРЫМ ГОТОВИТСЯ", "accent": False, "size": "small"}, {"text": "РЕБЕНОК", "accent": True, "size": "big"}]},
    {"start": 5.58, "end": 8.19, "lines": [{"text": "ДОМА ЧАСТЬ ТАКИХ МАТЕРИАЛОВ В СВОБОДНОМ", "accent": False, "size": "small"}, {"text": "ДОСТУПЕ", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 9.27, "lines": [{"text": "НЕ ОБНОВЛЯЛАСЬ", "accent": False, "size": "small"}, {"text": "ДАВНО", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 11.01, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "СОБРАН", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 12.15, "lines": [{"text": "АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.48, "end": 14.64, "lines": [{"text": "ЗАДАНИЯ ОТ СОСТАВИТЕЛЕЙ НАСТОЯЩЕГО", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 15.24, "end": 17.154, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.92, "end": 2.25}, {"start": 9.87, "end": 10.20}, {"start": 15.24, "end": 15.57}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (curly-haired boy, 16.108s): an unfamiliar task format on the
# real exam often traces back to training variants collected at random,
# and checking each one's source yourself is nearly impossible; the app's
# bank is the actual FIPI bank, same format as the real exam
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ВСТРЕЧАЕШЬ НЕЗНАКОМЫЙ", "ФОРМАТ ЗАДАНИЯ?"], "end": 1.65}
c_cards = [
    {"start": 1.80, "end": 2.85, "lines": [{"text": "НА ЕГЭ ВСТРЕЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.80, "lines": [{"text": "ТОЛЬКО ПОТОМУ ЧТО ТРЕНИРОВОЧНЫЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 5.97, "lines": [{"text": "БЫЛИ СОБРАНЫ", "accent": False, "size": "small"}, {"text": "НАУГАД", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 7.53, "lines": [{"text": "ПРОВЕРИТЬ ИСТОЧНИК КАЖДОГО", "accent": False, "size": "small"}, {"text": "ВАРИАНТА", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 9.15, "lines": [{"text": "САМОСТОЯТЕЛЬНО ПОЧТИ", "accent": False, "size": "small"}, {"text": "НЕРЕАЛЬНО", "accent": True, "size": "big"}]},
    {"start": 9.54, "end": 11.13, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 11.25, "end": 12.51, "lines": [{"text": "БАНК ФИПИ ТОТ ЖЕ", "accent": False, "size": "small"}, {"text": "ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 14.10, "lines": [{"text": "ЧТО БУДЕТ НА НАСТОЯЩЕМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 14.34, "end": 16.108, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.80, "end": 2.13}, {"start": 9.54, "end": 9.87}, {"start": 14.34, "end": 14.67}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (curly-haired boy, 17.440s): after a mistake it's easiest to
# call it chance and move on, but chance rarely repeats twice in a row on
# the same task type; the app's breakdown shows whether it's chance or a
# systemic error
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПОСЛЕ ОШИБКИ РЕШАЕШЬ", "ЧТО ЭТО СЛУЧАЙНОСТЬ?"], "end": 1.77}
d_cards = [
    {"start": 1.95, "end": 3.75, "lines": [{"text": "ВСЕГО РЕШИТЬ ЧТО ЭТО СЛУЧАЙНОСТЬ", "accent": False, "size": "small"}, {"text": "ПРОЩЕ", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 4.75, "lines": [{"text": "И ПОЙТИ", "accent": False, "size": "small"}, {"text": "ДАЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 4.92, "end": 6.24, "lines": [{"text": "СЛУЧАЙНОСТЬ ПОВТОРЯЕТСЯ", "accent": False, "size": "small"}, {"text": "РЕДКО", "accent": True, "size": "big"}]},
    {"start": 6.48, "end": 8.70, "lines": [{"text": "ДВАЖДЫ ПОДРЯД НА ОДНОМ И ТОМ ЖЕ ТИПЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 10.29, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 10.41, "end": 12.21, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.15, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 13.38, "end": 15.27, "lines": [{"text": "СЛУЧАЙНОСТЬ ЭТО ИЛИ СИСТЕМНАЯ", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 15.54, "end": 17.440, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.95, "end": 2.28}, {"start": 9.03, "end": 9.36}, {"start": 15.54, "end": 15.87}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (wavy-haired living-room boy, 19.160s): formally memorizing a
# rule for Russian isn't hard, but applying it in a task is a separate
# skill that plain reading doesn't give; the app's memorization games
# require applying the material in practice
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЗНАЕШЬ ПРАВИЛА", "НО НЕ МОЖЕШЬ ПРИМЕНИТЬ?"], "end": 1.80}
e_cards = [
    {"start": 1.92, "end": 2.97, "lines": [{"text": "ДЛЯ ЕГЭ ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 3.36, "end": 4.62, "lines": [{"text": "НЕ СЛОЖНО А ВОТ", "accent": False, "size": "small"}, {"text": "ПРИМЕНИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 7.02, "lines": [{"text": "ЕГО В ЗАДАНИИ УЖЕ ОТДЕЛЬНАЯ", "accent": False, "size": "small"}, {"text": "ЗАДАЧА", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 8.58, "lines": [{"text": "ОБЫЧНОЕ ЧТЕНИЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 10.05, "lines": [{"text": "НЕ ВСЕГДА ДАЕТ ТАКОЙ", "accent": False, "size": "small"}, {"text": "НАВЫК", "accent": True, "size": "big"}]},
    {"start": 10.29, "end": 11.49, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 11.64, "end": 13.35, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.79, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 15.90, "lines": [{"text": "ГДЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ПРИМЕНЯТЬ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 16.92, "lines": [{"text": "МАТЕРИАЛ НА", "accent": False, "size": "small"}, {"text": "ПРАКТИКЕ", "accent": True, "size": "big"}]},
    {"start": 17.25, "end": 19.160, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.92, "end": 2.25}, {"start": 10.29, "end": 10.62}, {"start": 17.25, "end": 17.58}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-haired boy, 18.200s): dates and terms for history/social
# studies crammed in one long evening before the exam barely stick; the
# app's memorization games give an earlier and more durable result
# ---------------------------------------------------------------------------
f_intro = {"lines": ["УЧИШЬ ДАТЫ И ТЕРМИНЫ", "ЗА ОДИН ВЕЧЕР?"], "end": 1.65}
f_cards = [
    {"start": 1.89, "end": 3.15, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ И", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 3.33, "end": 4.41, "lines": [{"text": "ИНОГДА ПЫТАЮТСЯ", "accent": False, "size": "small"}, {"text": "ВЫУЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 5.67, "lines": [{"text": "ЗА ОДИН ДЛИННЫЙ", "accent": False, "size": "small"}, {"text": "ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 5.79, "end": 7.02, "lines": [{"text": "ПЕРЕД ЭКЗАМЕНОМ", "accent": False, "size": "small"}, {"text": "ТАКОЙ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.13, "lines": [{"text": "СПОСОБ ОБЫЧНО", "accent": False, "size": "small"}, {"text": "ДЕРЖИТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.22, "end": 9.33, "lines": [{"text": "В ПАМЯТИ СОВСЕМ", "accent": False, "size": "small"}, {"text": "НЕДОЛГО", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 10.77, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 10.89, "end": 12.48, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 13.83, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 15.93, "lines": [{"text": "ДЛЯ БОЛЕЕ РАННЕГО И ПРОЧНОГО", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТА", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 18.200, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 9.63, "end": 9.96}, {"start": 16.29, "end": 16.62}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
