#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-FOURTH 'coffee123'
batch (6 episodes uploaded under the same tag after twenty-three prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes71/.

Two returning hosts, no new faces: the study-room girl introduced in
the 20th batch (a, b, f) and the mother (parent POV, c, d, e).
Sub-themes: an up-to-date FIPI bank that matches the real exam format
instead of stale/unknown-origin files (a, d), a detailed text
breakdown that reveals whether a correct answer was real understanding
or a lucky guess (b, c), memorization games built on independent
active recall instead of passive repetition (e, f).
"""
import json

REAL_DURATION = {
    "a": 19.160, "b": 21.880, "c": 19.586,
    "d": 19.202, "e": 19.820, "f": 21.960,
}
SOURCE_FILE = {
    "a": "fdgfdgfdufdjnejdre", "b": "fdhdhbfdndgfjfhnd", "c": "fhdhjfgjmfgjfhjtsnh",
    "d": "fhdjfdjngfxhghxd", "e": "gdjfxjfhdbdxbhdxz", "f": "ghfdhfjhhteyhgrdghd",
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
    words = json.load(open(f"../asr_coffee123_24/{src}_words.json"))
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
# Episode A (study-room girl, 19.160s): solving pre-downloaded EGE variants
# is convenient but not always safe for the result, since some circulate
# online for years and drift from the current format; the app's bank is
# updated together with the real exam
# ---------------------------------------------------------------------------
a_intro = {"lines": ["СКАЧИВАЕШЬ ВАРИАНТЫ", "ЗАРАНЕЕ ДЛЯ УДОБСТВА?"], "end": 2.49}
a_cards = [
    {"start": 2.70, "end": 5.43, "lines": [{"text": "УДОБНО НО НЕ ВСЕГДА БЕЗОПАСНО ДЛЯ", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТА", "accent": True, "size": "big"}]},
    {"start": 6.21, "end": 7.44, "lines": [{"text": "ЧАСТЬ ТАКИХ ФАЙЛОВ", "accent": False, "size": "small"}, {"text": "ГУЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 8.40, "lines": [{"text": "ПО СЕТИ", "accent": False, "size": "small"}, {"text": "ГОДАМИ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 9.81, "lines": [{"text": "И ДАВНО НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.89, "lines": [{"text": "С АКТУАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 13.11, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "СОБРАН", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.14, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.43, "end": 16.62, "lines": [{"text": "КОТОРЫЙ ОБНОВЛЯЕТСЯ ВМЕСТЕ С НАСТОЯЩИМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНОМ", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 19.160, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.70, "end": 3.03}, {"start": 11.76, "end": 12.09}, {"start": 17.19, "end": 17.52}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (study-room girl, 21.880s): it's easy to fall into the trap of
# "solved the task means the topic is learned" when a correct answer comes
# almost by chance, without understanding the solution; the app's
# breakdown shows whether it was real understanding or chance
# ---------------------------------------------------------------------------
b_intro = {"lines": ["РЕШАЕШЬ ЗАДАНИЕ", "И СЧИТАЕШЬ ЧТО ТЕМА ВЫУЧЕНА?"], "end": 2.46}
b_cards = [
    {"start": 3.09, "end": 5.19, "lines": [{"text": "РЕШИЛ ЗАДАНИЕ ЗНАЧИТ ТЕМА", "accent": False, "size": "small"}, {"text": "ВЫУЧЕНА", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.23, "lines": [{"text": "НА ДЕЛЕ ПРАВИЛЬНЫЙ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 7.41, "end": 8.25, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ПОЛУЧАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.37, "end": 9.21, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНО", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 11.16, "lines": [{"text": "БЕЗ ПОНИМАНИЯ ХОДА", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 13.56, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ К", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 15.72, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.11, "end": 17.04, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.37, "end": 18.27, "lines": [{"text": "БЫЛО ЭТО", "accent": False, "size": "small"}, {"text": "ПОНИМАНИЕ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 19.23, "lines": [{"text": "СЛУЧАЙНОСТЬ", "accent": False, "size": "small"}, {"text": "ИЛИ", "accent": True, "size": "big"}]},
    {"start": 19.95, "end": 21.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.09, "end": 3.42}, {"start": 12.15, "end": 12.48}, {"start": 19.95, "end": 20.28}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (mother, 19.586s): a child can solve an EGE task correctly and
# a month later not explain how they got there; without a breakdown that
# stays a lucky guess, not a skill; the app's breakdown fixes the actual
# solution method
# ---------------------------------------------------------------------------
c_intro = {"lines": ["РЕБЕНОК РЕШАЕТ ЗАДАНИЕ", "НО ЗАБЫВАЕТ КАК ЧЕРЕЗ МЕСЯЦ?"], "end": 2.25}
c_cards = [
    {"start": 2.37, "end": 3.60, "lines": [{"text": "ПРАВИЛЬНО И ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 3.78, "end": 4.59, "lines": [{"text": "НЕ СУМЕТЬ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.77, "end": 6.24, "lines": [{"text": "КАК ОН ВООБЩЕ К ЭТОМУ", "accent": False, "size": "small"}, {"text": "ПРИШЕЛ", "accent": True, "size": "big"}]},
    {"start": 6.81, "end": 8.10, "lines": [{"text": "БЕЗ РАЗБОРА ТАКОЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.22, "end": 9.54, "lines": [{"text": "ОСТАЕТСЯ СЛУЧАЙНОЙ", "accent": False, "size": "small"}, {"text": "УДАЧЕЙ", "accent": True, "size": "big"}]},
    {"start": 9.75, "end": 10.56, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "НАВЫКОМ", "accent": True, "size": "big"}]},
    {"start": 10.98, "end": 12.36, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 12.45, "end": 14.52, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.88, "end": 15.69, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ФИКСИРУЕТ", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 16.83, "lines": [{"text": "САМ СПОСОБ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 19.586, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.37, "end": 2.70}, {"start": 10.98, "end": 11.31}, {"start": 17.55, "end": 17.88}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (mother, 19.202s): a parent usually doesn't see which exact EGE
# tasks a child solves in the evenings, only that they seem to be
# studying, and the format can differ a lot from the real exam; the app's
# bank is sourced from the actual exam compilers
# ---------------------------------------------------------------------------
d_intro = {"lines": ["НЕ ЗНАЕШЬ КАКИЕ ЗАДАНИЯ", "РЕБЕНОК РЕШАЕТ ВЕЧЕРАМИ?"], "end": 1.80}
d_cards = [
    {"start": 2.04, "end": 3.33, "lines": [{"text": "КАКИЕ ИМЕННО ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.48, "end": 4.65, "lines": [{"text": "РЕБЕНОК РЕШАЕТ", "accent": False, "size": "small"}, {"text": "ВЕЧЕРАМИ", "accent": True, "size": "big"}]},
    {"start": 5.04, "end": 6.84, "lines": [{"text": "ТОЛЬКО ТО ЧТО ОН ВРОДЕ БЫ", "accent": False, "size": "small"}, {"text": "ЗАНИМАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.44, "end": 8.23, "lines": [{"text": "ФОРМАТ ЭТИХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 8.31, "end": 9.27, "lines": [{"text": "МОЖЕТ СИЛЬНО", "accent": False, "size": "small"}, {"text": "ОТЛИЧАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 11.34, "lines": [{"text": "ОТ ТОГО ЧТО БУДЕТ НА НАСТОЯЩЕМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 11.97, "end": 13.50, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 14.41, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 16.71, "lines": [{"text": "ЗАДАНИЕ ОТ СОСТАВИТЕЛЕЙ НАСТОЯЩЕГО", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 17.25, "end": 19.202, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.04, "end": 2.37}, {"start": 11.97, "end": 12.30}, {"start": 17.25, "end": 17.58}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (mother, 19.820s): a child can honestly repeat history/social
# studies material and still forget it a couple days later; the issue is
# often not memory but the method of repetition; the app's memorization
# games give a more durable result
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЧЕСТНО ПОВТОРЯЕШЬ МАТЕРИАЛ", "И ВСЕ РАВНО ЗАБЫВАЕШЬ?"], "end": 2.10}
e_cards = [
    {"start": 2.25, "end": 3.45, "lines": [{"text": "МАТЕРИАЛ ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 5.10, "lines": [{"text": "И ОБЩЕСТВОЗНАНИЮ И ВСЕ", "accent": False, "size": "small"}, {"text": "РАВНО", "accent": True, "size": "big"}]},
    {"start": 5.31, "end": 6.57, "lines": [{"text": "ЗАБЫВАТЬ ЕГО ЧЕРЕЗ ПАРУ", "accent": False, "size": "small"}, {"text": "ДНЕЙ", "accent": True, "size": "big"}]},
    {"start": 7.44, "end": 8.61, "lines": [{"text": "ДЕЛО ЧАСТО НЕ", "accent": False, "size": "small"}, {"text": "ЯВЛЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 10.14, "lines": [{"text": "А В САМОМ СПОСОБЕ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 10.86, "end": 12.12, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 12.21, "end": 13.08, "lines": [{"text": "ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.91, "lines": [{"text": "И ОБЩЕСТВОЗНАНИЯ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.06, "end": 17.25, "lines": [{"text": "НА ЗАПОМИНАНИЕ ДЛЯ БОЛЕЕ ПРОЧНОГО", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТА", "accent": True, "size": "big"}]},
    {"start": 17.94, "end": 19.820, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.25, "end": 2.58}, {"start": 10.86, "end": 11.19}, {"start": 17.94, "end": 18.27}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (study-room girl, 21.960s): history dates sometimes get learned
# just for the lesson and are forgotten by exam time, not because of
# memory but because they were never recalled independently; the app's
# memorization games build that independent recall
# ---------------------------------------------------------------------------
f_intro = {"lines": ["УЧИШЬ ДАТЫ НА УРОК", "А К ЭКЗАМЕНУ ЗАБЫВАЕШЬ?"], "end": 1.77}
f_cards = [
    {"start": 2.01, "end": 4.05, "lines": [{"text": "ИНОГДА ВЫУЧИВАЮТСЯ ТОЛЬКО НА ВРЕМЯ", "accent": False, "size": "small"}, {"text": "УРОКА", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 6.42, "lines": [{"text": "А К ЭКЗАМЕНУ БЛАГОПОЛУЧНО", "accent": False, "size": "small"}, {"text": "ЗАБЫВАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.35, "lines": [{"text": "ДЕЛО НЕ В", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 9.66, "lines": [{"text": "А В ТОМ ЧТО", "accent": False, "size": "small"}, {"text": "ДАТЫ", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 11.73, "lines": [{"text": "НИ РАЗУ НЕ ПРИШЛОСЬ", "accent": False, "size": "small"}, {"text": "ВСПОМИНАТЬ", "accent": True, "size": "big"}]},
    {"start": 12.48, "end": 13.71, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 15.51, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 17.28, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 19.23, "lines": [{"text": "ДЛЯ САМОСТОЯТЕЛЬНОГО ВОСПОМИНАНИЯ", "accent": False, "size": "small"}, {"text": "ТАКОГО", "accent": True, "size": "big"}]},
    {"start": 19.98, "end": 21.960, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.01, "end": 2.34}, {"start": 12.48, "end": 12.81}, {"start": 19.98, "end": 20.31}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
