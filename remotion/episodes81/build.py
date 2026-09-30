#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-FOURTH 'coffee123'
batch (6 episodes uploaded under the same tag after thirty-three prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes81/.

Two returning hosts, no new faces: "mother" HeyGen avatar (a, c, f),
"Рома" HeyGen avatar (b, d, e).

Sub-themes: a collection with gaps vs. the app's complete FIPI bank
(d, f); knowing something "in general terms" without surviving a
precise/different-context test -- explaining a choice, exact words,
out-of-order dates, an end-of-hour check, avoiding a weak type (a, b,
c, e).
"""
import json

REAL_DURATION = {
    "a": 21.804, "b": 21.280, "c": 21.058,
    "d": 19.202, "e": 19.052, "f": 21.122,
}
SOURCE_FILE = {
    "a": "ffhfdghgfhfh", "b": "gfhgfhghfh", "c": "hbjghtghgfhfh",
    "d": "hhjghhghf", "e": "jffgfgfdhgdgfdg", "f": "jghfjhffgmfhtrwer",
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
    "b": {"провело": "правило"},
    "e": {"текстовыя": "текстовый"},
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
    words = json.load(open(f"../asr_coffee123_34/{src}_words.json"))
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
# Episode A (mother, 21.804s): picking the right answer by elimination
# doesn't mean you can explain why the others are wrong; the app's text
# breakdown shows why exactly the wrong options don't fit
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВЫБРАЛА ОТВЕТ", "МЕТОДОМ ИСКЛЮЧЕНИЯ?"], "end": 1.53}
a_cards = [
    {"start": 1.53, "end": 2.37, "lines": [{"text": "ВЕРНЫЙ ОТВЕТ НА", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.37, "end": 3.42, "lines": [{"text": "МЕТОДОМ", "accent": False, "size": "small"}, {"text": "ИСКЛЮЧЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 3.42, "end": 4.74, "lines": [{"text": "И НЕ СУМЕТЬ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 6.60, "lines": [{"text": "ПОЧЕМУ ОСТАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 8.13, "lines": [{"text": "Я КАК ТО", "accent": False, "size": "small"}, {"text": "ПОПРОСИЛА", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.18, "lines": [{"text": "ЕЕ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.44, "lines": [{"text": "И ЭТО ОБЪЯСНЕНИЕ", "accent": False, "size": "small"}, {"text": "ДАЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 10.44, "end": 11.43, "lines": [{"text": "ЕЙ ЗАМЕТНО", "accent": False, "size": "small"}, {"text": "ТРУДНЕЕ", "accent": True, "size": "big"}]},
    {"start": 11.43, "end": 12.63, "lines": [{"text": "ЧЕМ САМ", "accent": False, "size": "small"}, {"text": "ВЫБОР ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 13.41, "end": 14.21, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.21, "end": 15.90, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 17.01, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 19.32, "lines": [{"text": "ПОЧЕМУ ИМЕННО НЕВЕРНЫЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 20.04, "end": 21.00, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 21.804, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.99, "end": 4.74}, {"start": 9.54, "end": 10.44}, {"start": 16.62, "end": 17.01}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 21.280s): a rule known perfectly in theory still slips
# on specific words in practice; the app's Russian games reinforce rules
# on concrete words, not just theory
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПРАВИЛО ЗНАЕШЬ", "БЕЗУПРЕЧНО?"], "end": 1.77}
b_cards = [
    {"start": 1.77, "end": 2.56, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "МОЖНО", "accent": True, "size": "big"}]},
    {"start": 2.56, "end": 3.87, "lines": [{"text": "В ТЕОРИИ", "accent": False, "size": "small"}, {"text": "БЕЗУПРЕЧНО", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 4.66, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ОШИБАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 4.66, "end": 6.03, "lines": [{"text": "ИМЕННО В", "accent": False, "size": "small"}, {"text": "КОНКРЕТНЫХ", "accent": True, "size": "big"}]},
    {"start": 6.03, "end": 6.83, "lines": [{"text": "СЛОВАХ НА", "accent": False, "size": "small"}, {"text": "ПРАКТИКЕ", "accent": True, "size": "big"}]},
    {"start": 7.02, "end": 8.01, "lines": [{"text": "Я ФОРМУЛИРОВАЛ", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 8.01, "end": 9.48, "lines": [{"text": "ОДНОКЛАССНИКАМ", "accent": False, "size": "small"}, {"text": "БЕЗ ЗАПИНКИ", "accent": True, "size": "big"}]},
    {"start": 9.48, "end": 10.74, "lines": [{"text": "А В ДИКТАНТЕ", "accent": False, "size": "small"}, {"text": "ОШИБАЛСЯ", "accent": True, "size": "big"}]},
    {"start": 10.74, "end": 12.30, "lines": [{"text": "ПОЧЕМУ ТО ИМЕННО", "accent": False, "size": "small"}, {"text": "НА НЕМ", "accent": True, "size": "big"}]},
    {"start": 12.69, "end": 13.48, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.48, "end": 14.85, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.85, "end": 16.59, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "big"}]},
    {"start": 16.59, "end": 18.09, "lines": [{"text": "ПРАВИЛА НА", "accent": False, "size": "small"}, {"text": "КОНКРЕТНЫХ СЛОВАХ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 19.08, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "В ТЕОРИИ", "accent": True, "size": "big"}]},
    {"start": 19.32, "end": 20.43, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.43, "end": 21.280, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.23, "end": 4.62}, {"start": 10.44, "end": 10.74}, {"start": 16.20, "end": 16.59}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 21.058s): dates known perfectly in order can get
# lost when mixed up in questions; the app's history games train dates
# specifically out of order
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ДАТЫ ПО ПОРЯДКУ", "ИДЕАЛЬНО?"], "end": 1.71}
c_cards = [
    {"start": 1.71, "end": 2.52, "lines": [{"text": "ИСТОРИИ ДЛЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.52, "end": 3.57, "lines": [{"text": "ПО ПОРЯДКУ", "accent": False, "size": "small"}, {"text": "ИДЕАЛЬНО", "accent": True, "size": "big"}]},
    {"start": 3.57, "end": 4.47, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 4.47, "end": 6.06, "lines": [{"text": "ЕСЛИ ИХ ПЕРЕМЕШАТЬ", "accent": False, "size": "small"}, {"text": "В ВОПРОСАХ", "accent": True, "size": "big"}]},
    {"start": 6.63, "end": 7.92, "lines": [{"text": "Я ПРОВЕРЯЛА ЕЕ", "accent": False, "size": "small"}, {"text": "В РАЗНОБОЙ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 9.63, "lines": [{"text": "СПЕЦИАЛЬНО И", "accent": False, "size": "small"}, {"text": "ИМЕННО ТОГДА", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 12.00, "lines": [{"text": "ДАТЫ НАЧИНАЛИ", "accent": False, "size": "small"}, {"text": "ПУТАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 13.45, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.45, "end": 14.43, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.43, "end": 16.44, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 18.51, "lines": [{"text": "ДАТЫ ИМЕННО В", "accent": False, "size": "small"}, {"text": "РАЗНОБОЙ", "accent": True, "size": "big"}]},
    {"start": 19.23, "end": 20.26, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.26, "end": 21.058, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.99, "end": 4.47}, {"start": 10.05, "end": 10.77}, {"start": 16.08, "end": 16.44}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (Рома, 19.202s): a collection can look big by volume while
# missing a whole task type; the app's FIPI bank covers all types
# without gaps
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПОДБОРКА ВЫГЛЯДИТ", "БОЛЬШОЙ?"], "end": 1.65}
d_cards = [
    {"start": 1.65, "end": 2.55, "lines": [{"text": "ЗАДАНИЙ ЕГЭ МОЖЕТ", "accent": False, "size": "small"}, {"text": "ВЫГЛЯДЕТЬ", "accent": True, "size": "big"}]},
    {"start": 2.55, "end": 3.75, "lines": [{"text": "ВНУШИТЕЛЬНОЙ ПО", "accent": False, "size": "small"}, {"text": "ОБЪЕМУ", "accent": True, "size": "big"}]},
    {"start": 3.75, "end": 5.10, "lines": [{"text": "И ПРИ ЭТОМ НЕ", "accent": False, "size": "small"}, {"text": "ОХВАТЫВАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 6.66, "lines": [{"text": "ОДИН ИЗ ТИПОВ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ СОВСЕМ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 7.92, "lines": [{"text": "Я РЕШАЛ ТАКУЮ", "accent": False, "size": "small"}, {"text": "ПОДБОРКУ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 8.71, "lines": [{"text": "ВЕСЬ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 8.71, "end": 9.93, "lines": [{"text": "ПОКА НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "НЕ ВСТРЕТИЛ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 12.06, "lines": [{"text": "ТИП ЗАДАНИЯ КОТОРОГО", "accent": False, "size": "small"}, {"text": "НЕ БЫЛО", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.30, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.30, "end": 14.28, "lines": [{"text": "СОБРАН БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.28, "end": 16.05, "lines": [{"text": "КОТОРЫЙ ОХВАТЫВАЕТ", "accent": False, "size": "small"}, {"text": "ВСЕ ТИПЫ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 16.92, "lines": [{"text": "ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "БЕЗ ПРОПУСКОВ", "accent": True, "size": "big"}]},
    {"start": 17.22, "end": 18.30, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.202, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.68, "end": 5.10}, {"start": 9.66, "end": 9.93}, {"start": 14.70, "end": 15.06}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 19.052s): checking the solution at the end of the hour
# gets postponed and an obvious mistake goes unnoticed; the app's text
# breakdown points straight to the mistake without rushing
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ПРОВЕРКА В КОНЦЕ ЧАСА", "ОТКЛАДЫВАЕТСЯ?"], "end": 1.92}
e_cards = [
    {"start": 1.92, "end": 2.85, "lines": [{"text": "ЕГЭ В КОНЦЕ", "accent": False, "size": "small"}, {"text": "ЧАСА", "accent": True, "size": "big"}]},
    {"start": 2.85, "end": 4.41, "lines": [{"text": "ОТКЛАДЫВАЕТСЯ ИЗ ЗА", "accent": False, "size": "small"}, {"text": "НЕХВАТКИ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 5.61, "lines": [{"text": "ВРЕМЕНИ И", "accent": False, "size": "small"}, {"text": "ОЧЕВИДНАЯ", "accent": True, "size": "big"}]},
    {"start": 5.61, "end": 6.72, "lines": [{"text": "ОШИБКА ПРОХОДИТ", "accent": False, "size": "small"}, {"text": "НЕЗАМЕЧЕННОЙ", "accent": True, "size": "small"}]},
    {"start": 7.23, "end": 8.67, "lines": [{"text": "Я ТАК ТОРОПИЛСЯ", "accent": False, "size": "small"}, {"text": "ЗАКОНЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 8.67, "end": 9.46, "lines": [{"text": "ВАРИАНТ ЧТО НЕ", "accent": False, "size": "small"}, {"text": "ГЛЯНУЛ", "accent": True, "size": "big"}]},
    {"start": 9.46, "end": 11.64, "lines": [{"text": "НА ЯВНУЮ ОШИБКУ В", "accent": False, "size": "small"}, {"text": "ПРЕДПОСЛЕДНЕМ", "accent": True, "size": "small"}]},
    {"start": 11.97, "end": 12.79, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.79, "end": 14.22, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.22, "end": 15.84, "lines": [{"text": "КОТОРЫЙ СРАЗУ", "accent": False, "size": "small"}, {"text": "УКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 15.84, "end": 17.01, "lines": [{"text": "НА ОШИБКУ БЕЗ", "accent": False, "size": "small"}, {"text": "СПЕШКИ", "accent": True, "size": "big"}]},
    {"start": 17.28, "end": 18.25, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.25, "end": 19.052, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 4.80, "end": 5.61}, {"start": 9.87, "end": 10.44}, {"start": 15.06, "end": 15.36}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 21.122s): a daughter confident in only one favorite
# task type avoids the rest without explanation; the app's FIPI bank
# with all types won't let a weak topic slide
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РЕШАЕТ ОДИН ЛЮБИМЫЙ", "ТИП ЗАДАНИЙ?"], "end": 1.89}
f_cards = [
    {"start": 1.89, "end": 2.94, "lines": [{"text": "ТОЛЬКО ОДИН", "accent": False, "size": "small"}, {"text": "ЛЮБИМЫЙ", "accent": True, "size": "big"}]},
    {"start": 2.94, "end": 3.78, "lines": [{"text": "ТИП", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 3.78, "end": 5.43, "lines": [{"text": "А ОСТАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ОБХОДИТЬ", "accent": True, "size": "big"}]},
    {"start": 5.43, "end": 6.24, "lines": [{"text": "СТОРОНОЙ БЕЗ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЕНИЙ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.69, "lines": [{"text": "Я ЗАМЕТИЛА", "accent": False, "size": "small"}, {"text": "ЭТО", "accent": True, "size": "big"}]},
    {"start": 7.69, "end": 8.91, "lines": [{"text": "ПО ЕЕ ТЕТРАДИ ГДЕ", "accent": False, "size": "small"}, {"text": "ОДНА", "accent": True, "size": "big"}]},
    {"start": 8.91, "end": 10.53, "lines": [{"text": "ТЕМА РАЗОБРАНА", "accent": False, "size": "small"}, {"text": "ДЕСЯТКИ РАЗ", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 12.15, "lines": [{"text": "А ДРУГИЕ ПОЧТИ", "accent": False, "size": "small"}, {"text": "НЕ ТРОНУТЫ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 13.72, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.72, "end": 14.67, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 15.99, "lines": [{"text": "СО ВСЕМИ", "accent": False, "size": "small"}, {"text": "ТИПАМИ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 15.99, "end": 17.49, "lines": [{"text": "КОТОРЫЕ НЕ ДАДУТ", "accent": False, "size": "small"}, {"text": "ПРОПУСТИТЬ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 18.45, "lines": [{"text": "НЕЛЮБИМУЮ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 19.11, "end": 20.28, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.28, "end": 21.122, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.71, "end": 4.98}, {"start": 9.27, "end": 9.72}, {"start": 16.89, "end": 17.49}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
