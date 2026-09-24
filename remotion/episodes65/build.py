#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-FIRST 'coffee123'
batch (9 episodes uploaded under the same tag after twenty prior batches
were delivered). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes65/.

Four returning hosts, no new faces: the brunette study-room host (a, b,
i), the wavy-haired living-room boy (c, d), the study-room girl
introduced in the 20th batch (e, f, g), and the mother (parent POV,
h). Three sub-themes repeat across hosts: memorization games that
require active recall instead of passive rereading, a full text
breakdown that shows whether a topic/method is really understood
instead of just having gotten lucky, and an up-to-date FIPI-sourced
task bank instead of stale/contradictory internet collections.
"""
import json

REAL_DURATION = {
    "a": 24.520, "b": 23.127, "c": 15.682,
    "d": 15.212, "e": 19.372, "f": 22.167,
    "g": 21.804, "h": 20.418, "i": 23.255,
}
SOURCE_FILE = {
    "a": "bgdfhbjgfdujfutyjtr", "b": "btdrthdftujnfcrtjuytr", "c": "bthghftgdufurjru",
    "d": "btrhdfhjtrjtrdiukjtrirt", "e": "fdbhgdyhbfhfdgshu", "f": "gfdgdgfdgdgfdgdf",
    "g": "ghdfgdhgfdhg", "h": "rdhgchgfhtrujtjtrsd", "i": "thrdghfcgtfrjfdurdujjutr",
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
    if letter == "a":
        for w in words:
            if abs(w["start"] - 24.03) < 0.02 and w["text"] == "шапти":
                w["text"] = "шапке"
    if letter == "d":
        for w in words:
            if abs(w["start"] - 10.74) < 0.02 and w["text"] == "ипи":
                w["text"] = "фипи"
    if letter == "e":
        for w in words:
            if abs(w["start"] - 7.62) < 0.02 and w["text"] == "такуй":
                w["text"] = "такой"
    if letter == "f":
        for w in words:
            if abs(w["start"] - 4.23) < 0.02 and w["text"] == "спорников":
                w["text"] = "сборников"
        fixed = []
        skip_next = False
        for i, w in enumerate(words):
            if skip_next:
                skip_next = False
                continue
            if (abs(w["start"] - 16.92) < 0.02 and w["text"] == "фи"
                    and i + 1 < len(words) and words[i + 1]["text"] == "пи"):
                w = dict(w)
                w["text"] = "фипи"
                w["end"] = words[i + 1]["end"]
                skip_next = True
            fixed.append(w)
        words = fixed
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_21/{src}_words.json"))
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
# Episode A (brunette study-room host, 24.520s): rules memorized the night
# before still get mixed up because they were never actually applied; the
# app's memorization games require active application, not just repetition
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВЫУЧИЛ ПРАВИЛА", "И ВСЕ РАВНО ПУТАЕШЬ?"], "end": 2.22}
a_cards = [
    {"start": 2.58, "end": 3.72, "lines": [{"text": "МОЖНО ВЫУЧИТЬ ПЕРЕД", "accent": False, "size": "small"}, {"text": "СНОМ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 6.15, "lines": [{"text": "И ВСЕ РАВНО ПЕРЕПУТАТЬ ЕГО НА СЛЕДУЮЩИЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 8.73, "lines": [{"text": "ДЕЛО НЕ В СЛОЖНОСТИ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 12.30, "lines": [{"text": "А В ТОМ ЧТО ОНО НЕ БЫЛО ПО НАСТОЯЩЕМУ ПРОВЕРЕНО НА", "accent": False, "size": "small"}, {"text": "ПРАКТИКЕ", "accent": True, "size": "big"}]},
    {"start": 13.32, "end": 14.64, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.62, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 17.25, "end": 18.54, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.99, "end": 20.73, "lines": [{"text": "ГДЕ ПРАВИЛА ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ПРИМЕНЯТЬ", "accent": True, "size": "big"}]},
    {"start": 21.15, "end": 22.05, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ПОВТОРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 22.59, "end": 24.520, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.58, "end": 2.91}, {"start": 13.32, "end": 13.65}, {"start": 22.59, "end": 22.92}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (brunette study-room host, 23.127s): a topic that suddenly
# stops working again was probably never truly understood, just gotten
# right by luck; the app's breakdown shows whether it's really understood
# ---------------------------------------------------------------------------
b_intro = {"lines": ["КАЖЕТСЯ ЧТО ТЕМА", "ДАВНО ЗАКРЫТА?"], "end": 3.0}
b_cards = [
    {"start": 3.36, "end": 6.42, "lines": [{"text": "А ПОТОМ ОДНО И ТО ЖЕ ЗАДАНИЕ СНОВА НЕ", "accent": False, "size": "small"}, {"text": "ПОДДАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.26, "end": 9.54, "lines": [{"text": "ОБЫЧНАЯ ПРИЧИНА В ТОМ ЧТО РАНЬШЕ ПРОСТО", "accent": False, "size": "small"}, {"text": "ПОВЕЗЛО", "accent": True, "size": "big"}]},
    {"start": 9.72, "end": 11.91, "lines": [{"text": "С ОТВЕТОМ А НЕ ЧТО ТЕМА ПРАВДА", "accent": False, "size": "small"}, {"text": "ПОНЯТА", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 14.10, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ К", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 14.22, "end": 16.44, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.83, "end": 17.67, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 18.12, "end": 20.19, "lines": [{"text": "ПОНЯТА ТЕМА НА САМОМ ДЕЛЕ ИЛИ", "accent": False, "size": "small"}, {"text": "НЕТ", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 23.127, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.36, "end": 3.69}, {"start": 12.66, "end": 12.99}, {"start": 21.06, "end": 21.39}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (wavy-haired living-room boy, 15.682s): landing on the right
# answer by chance on a real exam doesn't mean the method works, and that
# luck won't always repeat; the app's breakdown shows if the method holds
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПОПАЛ В ОТВЕТ", "И ДАЖЕ НЕ ЗАМЕТИЛ?"], "end": 1.74}
c_cards = [
    {"start": 1.74, "end": 4.32, "lines": [{"text": "ПРАВИЛЬНЫЙ ОТВЕТ ЗАДАНИЙ ЕГЭ И ДАЖЕ НЕ ЗАМЕТИТЬ", "accent": False, "size": "small"}, {"text": "ЭТОГО", "accent": True, "size": "big"}]},
    {"start": 4.47, "end": 5.52, "lines": [{"text": "НО НАСТОЯЩЕМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 5.64, "end": 7.38, "lines": [{"text": "УДАЧА ПОВТОРЯЕТСЯ ДАЛЕКО НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ТАКАЯ", "accent": True, "size": "big"}]},
    {"start": 7.74, "end": 8.94, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.92, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.13, "end": 13.59, "lines": [{"text": "КОТОРЫЙ ПОКАЗЫВАЕТ РАБОТАЕТ ЛИ СПОСОБ НА САМОМ", "accent": False, "size": "small"}, {"text": "ДЕЛЕ", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 15.682, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.74, "end": 2.07}, {"start": 7.74, "end": 8.07}, {"start": 13.86, "end": 14.19}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (wavy-haired living-room boy, 15.212s): variants downloaded long
# ago and never rechecked can drift from the current exam format; the app's
# bank is the actual FIPI bank, always matching the real exam
# ---------------------------------------------------------------------------
d_intro = {"lines": ["РЕШАЕШЬ ВАРИАНТЫ", "КОТОРЫЕ СКАЧАЛ ДАВНО?"], "end": 2.01}
d_cards = [
    {"start": 2.10, "end": 3.96, "lines": [{"text": "КОТОРЫЕ СКАЧАЛИ ДАВНО И БОЛЬШЕ НИ", "accent": False, "size": "small"}, {"text": "РАЗУ", "accent": True, "size": "big"}]},
    {"start": 4.14, "end": 5.94, "lines": [{"text": "НЕ ПРОВЕРЯЛИ НА АКТУАЛЬНОСТЬ ЗА ЭТО", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 6.12, "end": 8.37, "lines": [{"text": "ФОРМУЛИРОВКИ ЗАДАНИЙ ВПОЛНЕ МОГЛИ", "accent": False, "size": "small"}, {"text": "ИЗМЕНИТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 10.32, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 10.44, "end": 11.25, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.23, "lines": [{"text": "ВСЕГДА СООТВЕТСТВУЕТ РЕАЛЬНОМУ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНУ", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 15.212, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.10, "end": 2.43}, {"start": 8.73, "end": 9.06}, {"start": 13.44, "end": 13.77}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (study-room girl, 19.372s): the same wrong answer twice usually
# traces back to one misunderstood step, not bad luck; the app's breakdown
# finds exactly that step
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ПОЛУЧАЕШЬ ОДИНАКОВЫЙ", "НЕПРАВИЛЬНЫЙ ОТВЕТ?"], "end": 1.80}
e_cards = [
    {"start": 1.95, "end": 3.42, "lines": [{"text": "ПОДРЯД ПОЛУЧИТЬ", "accent": False, "size": "small"}, {"text": "ОДИНАКОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 3.57, "end": 4.41, "lines": [{"text": "НЕПРАВИЛЬНЫЙ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 6.27, "lines": [{"text": "И РЕШИТЬ ЧТО ПРОСТО НЕ", "accent": False, "size": "small"}, {"text": "ПОВЕЗЛО", "accent": True, "size": "big"}]},
    {"start": 7.02, "end": 8.13, "lines": [{"text": "НА ДЕЛЕ ЗА ТАКОЙ", "accent": False, "size": "small"}, {"text": "ОШИБКОЙ", "accent": True, "size": "big"}]},
    {"start": 8.31, "end": 10.74, "lines": [{"text": "ОБЫЧНО СТОИТ ОДИН И ТОТ ЖЕ НЕПОНЯТЫЙ", "accent": False, "size": "small"}, {"text": "ШАГ", "accent": True, "size": "big"}]},
    {"start": 11.43, "end": 12.66, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 14.73, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЕ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 16.83, "lines": [{"text": "КОТОРЫЙ НАХОДИТ ИМЕННО ЭТОТ", "accent": False, "size": "small"}, {"text": "ШАГ", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 19.372, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.95, "end": 2.28}, {"start": 11.43, "end": 11.76}, {"start": 17.40, "end": 17.73}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (study-room girl, 22.167s): variants pulled from several
# collections often contradict each other in format, which only confuses;
# the app's bank is unified and actual, without discrepancies between
# sources
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СОБИРАЕШЬ ВАРИАНТЫ", "ИЗ РАЗНЫХ СБОРНИКОВ?"], "end": 1.92}
f_cards = [
    {"start": 2.07, "end": 4.68, "lines": [{"text": "ВАРИАНТОВ ИЗ ТРЕХ ЧЕТЫРЕХ РАЗНЫХ", "accent": False, "size": "small"}, {"text": "СБОРНИКОВ", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 8.10, "lines": [{"text": "И НЕ ЗАМЕТИТЬ ЧТО ОНИ ПРОТИВОРЕЧАТ ДРУГ ДРУГУ ПО", "accent": False, "size": "small"}, {"text": "ФОРМАТУ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 10.26, "lines": [{"text": "ТАКАЯ ПУТАНИЦА", "accent": False, "size": "small"}, {"text": "ОБЫЧНО", "accent": True, "size": "big"}]},
    {"start": 10.47, "end": 12.45, "lines": [{"text": "НЕ ПОМОГАЕТ А ТОЛЬКО СБИВАЕТ С", "accent": False, "size": "small"}, {"text": "ТОЛКУ", "accent": True, "size": "big"}]},
    {"start": 13.74, "end": 15.63, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЕДИНЫЙ", "accent": True, "size": "big"}]},
    {"start": 15.84, "end": 17.13, "lines": [{"text": "АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 17.73, "end": 19.50, "lines": [{"text": "РАЗНОЧТЕНИЙ МЕЖДУ ИСТОЧНИКАМИ", "accent": False, "size": "small"}, {"text": "БЕЗ", "accent": True, "size": "big"}]},
    {"start": 20.16, "end": 22.167, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.07, "end": 2.40}, {"start": 13.74, "end": 14.07}, {"start": 20.16, "end": 20.49}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (study-room girl, 21.804s): terms for history stick only until
# the end of the lesson; reading them aloud again barely helps without
# extra training; the app's memorization games give a longer-lasting effect
# ---------------------------------------------------------------------------
g_intro = {"lines": ["УЧИШЬ ТЕРМИНЫ", "И ЗАБЫВАЕШЬ ПОСЛЕ УРОКА?"], "end": 1.89}
g_cards = [
    {"start": 2.16, "end": 3.30, "lines": [{"text": "ИНОГДА ДЕРЖИТСЯ В", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 4.77, "lines": [{"text": "РОВНО ДО КОНЦА", "accent": False, "size": "small"}, {"text": "УРОКА", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.12, "lines": [{"text": "НА КОТОРОМ ИХ", "accent": False, "size": "small"}, {"text": "РАЗБИРАЛИ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.79, "lines": [{"text": "ПРОСТОЕ ПОВТОРЕНИЕ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 8.97, "end": 9.90, "lines": [{"text": "ПОЧТИ НЕ", "accent": False, "size": "small"}, {"text": "ПОМОГАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.34, "lines": [{"text": "БЕЗ ДОПОЛНИТЕЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ТРЕНИРОВКИ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.65, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.69, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 16.41, "end": 17.64, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 17.88, "end": 19.20, "lines": [{"text": "ДЛЯ БОЛЕЕ ДОЛГОГО", "accent": False, "size": "small"}, {"text": "ЭФФЕКТА", "accent": True, "size": "big"}]},
    {"start": 19.95, "end": 21.804, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.16, "end": 2.49}, {"start": 12.33, "end": 12.66}, {"start": 19.95, "end": 20.28}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (mother, 20.418s): a child can sit honestly with the textbook
# and still barely retain anything; the issue is usually the method of
# repetition, not the time spent; the app's memorization games give a
# stronger result
# ---------------------------------------------------------------------------
h_intro = {"lines": ["РЕБЕНОК ЧЕСТНО УЧИТ", "НО НИЧЕГО НЕ ПОМНИТ?"], "end": 2.94}
h_cards = [
    {"start": 3.33, "end": 4.92, "lines": [{"text": "МОЖЕТ ЧЕСТНО СИДЕТЬ ЗА", "accent": False, "size": "small"}, {"text": "УЧЕБНИКОМ", "accent": True, "size": "big"}]},
    {"start": 5.07, "end": 6.96, "lines": [{"text": "И ПОЧТИ НИЧЕГО НЕ ЗАПОМИНАТЬ", "accent": False, "size": "small"}, {"text": "НАДОЛГО", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 8.85, "lines": [{"text": "ДЕЛО ЧАСТО НЕ ВО", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 11.01, "lines": [{"text": "ЗА СТОЛОМ А В САМОМ", "accent": False, "size": "small"}, {"text": "СПОСОБЕ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.96, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 13.11, "end": 14.70, "lines": [{"text": "ЯЗЫКУ ОБЩЕСТВОЗНАНИЯ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 16.32, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 17.91, "lines": [{"text": "ДЛЯ БОЛЕЕ ПРОЧНОГО", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТА", "accent": True, "size": "big"}]},
    {"start": 18.51, "end": 20.418, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.33, "end": 3.66}, {"start": 11.70, "end": 12.03}, {"start": 18.51, "end": 18.84}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (brunette study-room host, 23.255s): hitting an unfamiliar
# task formulation on the real exam is often because the training variants
# were collected from scattered sources without checking relevance; the
# app's actual FIPI bank carries the same formulations as the real exam
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ВСТРЕЧАЕШЬ ЗАДАНИЕ", "КОТОРОГО НИКОГДА НЕ БЫЛО?"], "end": 1.98}
i_cards = [
    {"start": 2.13, "end": 3.06, "lines": [{"text": "ФОРМУЛИРОВКУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 5.01, "lines": [{"text": "КОТОРУЮ ТЫ НИКОГДА РАНЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "ВИДЕЛА", "accent": True, "size": "big"}]},
    {"start": 5.13, "end": 6.69, "lines": [{"text": "В СВОИХ ТРЕНИРОВОЧНЫХ", "accent": False, "size": "small"}, {"text": "ВАРИАНТАХ", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 9.96, "lines": [{"text": "ЧАСТО ДЕЛО В ТОМ ЧТО САМИ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 10.26, "end": 11.82, "lines": [{"text": "СОБРАНЫ ИЗ РАЗНЫХ", "accent": False, "size": "small"}, {"text": "ИСТОЧНИКОВ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.47, "lines": [{"text": "ПРОВЕРКИ АКТУАЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "БЕЗ", "accent": True, "size": "big"}]},
    {"start": 14.43, "end": 16.26, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 16.38, "end": 17.20, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 17.64, "end": 20.43, "lines": [{"text": "ТЕ ЖЕ ФОРМУЛИРОВКИ ЧТО ДЕЙСТВИТЕЛЬНО БУДУТ НА", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 23.255, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.13, "end": 2.46}, {"start": 14.43, "end": 14.76}, {"start": 21.21, "end": 21.54}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
