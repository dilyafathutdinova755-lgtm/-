#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-SEVENTH 'coffee123'
batch (9 episodes, same as batch 35). Not a generic tool: hand-picked
timings/text per episode. Run from remotion/episodes84/.

Three returning hosts, no new faces: "teen boy on couch" (a, d, f),
"Рома" (c, e, g), "mother" (b, h, i).

Sub-themes: confusing one of two similar/neighboring things (rulers,
treaty years, punctuation word-orders, task packets by profile), plus
narrow or unverified training sources -- a leaderboard that only
rewards short easy tasks, an unofficial voice-assistant skill of
unknown origin, forgetting whether order matters in a counting
problem, habitually using every number in a condition even an unused
one, and mistakes that appear only under a timer, not at a calm pace.
"""
import json

REAL_DURATION = {
    "a": 21.280, "b": 21.400, "c": 23.255,
    "d": 23.575, "e": 19.863, "f": 20.098,
    "g": 22.380, "h": 25.346, "i": 21.122,
}
SOURCE_FILE = {
    "a": "fghghfhfghhgf", "b": "fghhgfhfhh", "c": "gcvhfgjhfhtfhtfg",
    "d": "hfghfhgfhfgh", "e": "hfhfhfghfghfgh", "f": "hfhfhgfhfgh",
    "g": "hgfhfhgfhfghgfh", "h": "hgfhghgfhhfg", "i": "hghfhhgfhfhgh",
}
FIXES = {
    "d": {"фипис": "фипи"},
    "f": {"посчет": "подсчет", "почета": "подсчета"},
    "g": {"тренажери": "тренажере"},
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
    stem = SOURCE_FILE[letter]
    with open(f"../asr_coffee123_37/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy, 21.280s): remembers a historical period's traits
# well but mixes up which of two neighboring rulers a specific event
# happened under; the app's memory games lock events to the correct
# neighboring ruler specifically
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПРИ КАКОМ ПРАВИТЕЛЕ", "БЫЛО СОБЫТИЕ ПУТАЕШЬ?"], "end": 1.92}
a_cards = [
    {"start": 1.92, "end": 3.36, "lines": [{"text": "ПЕРИОДА ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОМНЮ ХОРОШО", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 5.16, "lines": [{"text": "А ВОТ ПРИ КАКОМ ИЗ ДВУХ", "accent": False, "size": "small"}, {"text": "СОСЕДНИХ", "accent": True, "size": "big"}]},
    {"start": 5.16, "end": 6.90, "lines": [{"text": "ПРАВИТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "ПРОИЗОШЛО КОНКРЕТНОЕ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.16, "lines": [{"text": "СОБЫТИЕ", "accent": False, "size": "small"}, {"text": "ИНОГДА ПУТАЮ", "accent": True, "size": "big"}]},
    {"start": 8.46, "end": 9.36, "lines": [{"text": "НА ПРОБНИКЕ Я", "accent": False, "size": "small"}, {"text": "НАЗВАЛ", "accent": True, "size": "big"}]},
    {"start": 9.36, "end": 10.17, "lines": [{"text": "ПЕРИОД", "accent": False, "size": "small"}, {"text": "ВЕРНО", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.10, "lines": [{"text": "И ПРИПИСАЛ", "accent": False, "size": "small"}, {"text": "СОБЫТИЯ", "accent": True, "size": "big"}]},
    {"start": 11.37, "end": 12.51, "lines": [{"text": "НЕ ТОМУ ИЗ ДВУХ", "accent": False, "size": "small"}, {"text": "ПРАВИТЕЛЕЙ", "accent": True, "size": "small"}]},
    {"start": 12.51, "end": 13.80, "lines": [{"text": "ПОДРЯД В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 14.61, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.61, "end": 16.41, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "small"}]},
    {"start": 16.59, "end": 17.79, "lines": [{"text": "СОБЫТИЯ СРАЗУ С", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНЫМ", "accent": True, "size": "big"}]},
    {"start": 17.79, "end": 19.17, "lines": [{"text": "ПРАВИТЕЛЕМ ИЗ ДВУХ", "accent": False, "size": "small"}, {"text": "СОСЕДНИХ", "accent": True, "size": "big"}]},
    {"start": 19.41, "end": 20.40, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.40, "end": 21.280, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.85, "end": 6.30}, {"start": 9.93, "end": 10.08}, {"start": 11.37, "end": 12.03}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 21.400s): daughter confuses which punctuation goes
# with direct speech when the author's words come after the quote
# instead of before; the app's games train both word orders separately
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЗНАК ПРИ ПРЯМОЙ", "РЕЧИ ПУТАЕШЬ?"], "end": 1.92}
b_cards = [
    {"start": 1.92, "end": 2.91, "lines": [{"text": "ПУТАЮТ КАКОЙ ЗНАК", "accent": False, "size": "small"}, {"text": "СТАВИТЬ", "accent": True, "size": "big"}]},
    {"start": 2.91, "end": 4.14, "lines": [{"text": "ПРИ ПРЯМОЙ РЕЧИ ДЛЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ ПО РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 4.59, "end": 5.52, "lines": [{"text": "ЕСЛИ СЛОВА", "accent": False, "size": "small"}, {"text": "АВТОРЫ", "accent": True, "size": "big"}]},
    {"start": 5.52, "end": 7.11, "lines": [{"text": "СТОЯТ НЕ ДО А", "accent": False, "size": "small"}, {"text": "ПОСЛЕ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.67, "lines": [{"text": "САМОЙ РЕПЛИКИ Я", "accent": False, "size": "small"}, {"text": "ПОПРОСИЛА", "accent": True, "size": "big"}]},
    {"start": 8.67, "end": 9.66, "lines": [{"text": "ЕЕ РАССТАВИТЬ", "accent": False, "size": "small"}, {"text": "ЗНАКИ", "accent": True, "size": "big"}]},
    {"start": 9.75, "end": 11.04, "lines": [{"text": "В ПРИМЕРЕ С", "accent": False, "size": "small"}, {"text": "ОБРАТНЫМ ПОРЯДКОМ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.63, "lines": [{"text": "И ДОЧЬ", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАЛА", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 13.77, "lines": [{"text": "ПРАВИЛА МЕСТАМИ В", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 14.82, "lines": [{"text": "ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.44, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.80, "end": 17.64, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 17.64, "end": 19.70, "lines": [{"text": "ОБА ПОРЯДКА", "accent": False, "size": "small"}, {"text": "ПРЯМОЙ РЕЧИ ОТДЕЛЬНО", "accent": True, "size": "small"}]},
    {"start": 19.70, "end": 20.59, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.59, "end": 21.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.64, "end": 5.85}, {"start": 8.28, "end": 8.67}, {"start": 11.76, "end": 12.18}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 23.255s): a gamified prep app's leaderboard rewards
# only speed, so its tasks are deliberately short and easy; trained
# almost exclusively there and rarely met complex tasks; the app's bank
# has every difficulty, without a leaderboard narrowing the selection
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТАБЛИЦА ЛИДЕРОВ", "НАГРАЖДАЕТ ТОЛЬКО СКОРОСТЬ?"], "end": 1.95}
c_cards = [
    {"start": 1.95, "end": 2.82, "lines": [{"text": "В ИГРОВОМ ПРИЛОЖЕНИИ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦА", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 4.53, "lines": [{"text": "ЛИДЕРОВ НАГРАЖДАЕТ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "СКОРОСТЬ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 5.85, "lines": [{"text": "РЕШЕНИЯ И ЗАДАНИЯ ТАМ", "accent": False, "size": "small"}, {"text": "ПОДОБРАНЫ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 7.26, "lines": [{"text": "СПЕЦИАЛЬНО", "accent": False, "size": "small"}, {"text": "САМЫЕ", "accent": True, "size": "big"}]},
    {"start": 7.26, "end": 8.34, "lines": [{"text": "КОРОТКИЕ И", "accent": False, "size": "small"}, {"text": "ЛЕГКИЕ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.69, "lines": [{"text": "Я ТРЕНИРОВАЛСЯ", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 10.56, "lines": [{"text": "В ЭТОМ", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИИ", "accent": True, "size": "small"}]},
    {"start": 10.56, "end": 11.61, "lines": [{"text": "РАДИ МЕСТА В", "accent": False, "size": "small"}, {"text": "ТАБЛИЦЕ", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 13.11, "lines": [{"text": "ЛИДЕРОВ И СОВСЕМ НЕ", "accent": False, "size": "small"}, {"text": "ВСТРЕЧАЛ", "accent": True, "size": "big"}]},
    {"start": 13.29, "end": 14.85, "lines": [{"text": "ТАМ СЛОЖНЫЕ И", "accent": False, "size": "small"}, {"text": "ДЛИННЫЕ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 15.97, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.97, "end": 16.80, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.39, "lines": [{"text": "СО ВСЕМИ ЗАДАНИЯМИ ПО", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТИ", "accent": True, "size": "big"}]},
    {"start": 18.39, "end": 19.83, "lines": [{"text": "БЕЗ ИГРОВЫХ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦ ЛИДЕРОВ", "accent": True, "size": "big"}]},
    {"start": 19.83, "end": 21.15, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "УРЕЗАЮТ ВЫБОРКУ", "accent": True, "size": "small"}]},
    {"start": 21.42, "end": 22.44, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.44, "end": 23.255, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.30, "end": 3.72}, {"start": 7.38, "end": 7.74}, {"start": 12.39, "end": 12.75}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (teen boy, 23.575s): trains via an unofficial voice-assistant
# skill at home and can't find any information about its author or
# source online; the app's bank has a clear source for every task
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗАДАНИЯ ЧЕРЕЗ", "ГОЛОСОВОЙ НАВЫК?"], "end": 1.89}
d_cards = [
    {"start": 1.89, "end": 3.66, "lines": [{"text": "ЧЕРЕЗ ГОЛОСОВОГО", "accent": False, "size": "small"}, {"text": "ПОМОЩНИКА ДОМА", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 4.95, "lines": [{"text": "А ЧТО СТОИТ ЗА", "accent": False, "size": "small"}, {"text": "ЭТИМ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.42, "lines": [{"text": "НЕОФИЦИАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ГОЛОСОВЫМ НАВЫКОМ", "accent": True, "size": "small"}]},
    {"start": 6.66, "end": 7.83, "lines": [{"text": "И ОТКУДА ТАМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.30, "lines": [{"text": "СОВЕРШЕННО", "accent": False, "size": "small"}, {"text": "НЕПОНЯТНО", "accent": True, "size": "small"}]},
    {"start": 9.69, "end": 10.62, "lines": [{"text": "Я ПОИСКАЛ", "accent": False, "size": "small"}, {"text": "ИНФОРМАЦИЮ", "accent": True, "size": "small"}]},
    {"start": 10.62, "end": 11.85, "lines": [{"text": "ОБ ЭТОМ НАВЫКЕ В", "accent": False, "size": "small"}, {"text": "ИНТЕРНЕТЕ", "accent": True, "size": "big"}]},
    {"start": 12.09, "end": 12.90, "lines": [{"text": "И НЕ НАШЕЛ", "accent": False, "size": "small"}, {"text": "НИЧЕГО", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.73, "lines": [{"text": "ОБ АВТОРАХ ИЛИ", "accent": False, "size": "small"}, {"text": "ИСТОЧНИКЕ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 15.95, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.95, "end": 16.95, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.95, "end": 18.33, "lines": [{"text": "С ПОНЯТНЫМ", "accent": False, "size": "small"}, {"text": "ИСТОЧНИКОМ", "accent": True, "size": "big"}]},
    {"start": 18.33, "end": 19.68, "lines": [{"text": "КАЖДОГО ЗАДАНИЯ А НЕ", "accent": False, "size": "small"}, {"text": "ГОЛОСОВЫМ НАВЫКОМ", "accent": True, "size": "small"}]},
    {"start": 19.68, "end": 21.39, "lines": [{"text": "НЕПОНЯТНОГО", "accent": False, "size": "small"}, {"text": "ПРОИСХОЖДЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 21.66, "end": 22.74, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.74, "end": 23.575, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.10, "end": 5.55}, {"start": 8.82, "end": 9.30}, {"start": 12.33, "end": 12.87}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 19.863s): remembers the correct year for a historical
# treaty but sometimes attributes it to a similarly-named one instead;
# the app's history games separate similarly-named treaties apart
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ДОГОВОР С ПОХОЖИМ", "НАЗВАНИЕМ ПУТАЕШЬ?"], "end": 1.95}
e_cards = [
    {"start": 1.95, "end": 3.03, "lines": [{"text": "ПОМНЮ", "accent": False, "size": "small"}, {"text": "С ВЕРНЫМ ГОДОМ", "accent": True, "size": "big"}]},
    {"start": 3.21, "end": 4.62, "lines": [{"text": "А ВОТ С ДРУГИМ", "accent": False, "size": "small"}, {"text": "ПОХОЖИМ ПО НАЗВАНИЮ", "accent": True, "size": "small"}]},
    {"start": 4.62, "end": 5.67, "lines": [{"text": "ДОКУМЕНТОМ", "accent": False, "size": "small"}, {"text": "ТОТ ГОД", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 6.96, "lines": [{"text": "ИНОГДА ПУТАЮ", "accent": False, "size": "small"}, {"text": "МЕСТАМИ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.73, "lines": [{"text": "НА ПРОБНИКЕ Я НАЗВАЛ", "accent": False, "size": "small"}, {"text": "ВЕРНЫЙ ГОД", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 9.63, "lines": [{"text": "НО ПРИПИСАЛ", "accent": False, "size": "small"}, {"text": "ЕГО", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 11.97, "lines": [{"text": "НЕ ТОМУ ИЗ ДВУХ ПОХОЖИХ ПО", "accent": False, "size": "small"}, {"text": "НАЗВАНИЮ ДОГОВОРОВ", "accent": True, "size": "small"}]},
    {"start": 12.21, "end": 13.03, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.03, "end": 14.07, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.07, "end": 15.57, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "РАЗВОДЯТ", "accent": True, "size": "big"}]},
    {"start": 15.57, "end": 17.10, "lines": [{"text": "ПОХОЖИЕ ПО", "accent": False, "size": "small"}, {"text": "НАЗВАНИЮ ДОГОВОРЫ", "accent": True, "size": "small"}]},
    {"start": 17.10, "end": 18.09, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНОСТИ", "accent": True, "size": "small"}]},
    {"start": 18.09, "end": 18.89, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.89, "end": 19.863, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 6.27, "end": 6.48}, {"start": 9.00, "end": 9.63}, {"start": 11.58, "end": 11.97}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy, 20.098s): forgets whether order matters when
# counting variants and picks the wrong formula as a result; the app's
# breakdown separately explains when order matters and when it doesn't
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ВАЖЕН ЛИ ПОРЯДОК", "ИНОГДА ЗАБЫВАЕШЬ?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.03, "lines": [{"text": "НА ПОДСЧЕТ ВАРИАНТОВ", "accent": False, "size": "small"}, {"text": "ЗАБЫВАЮ", "accent": True, "size": "big"}]},
    {"start": 3.21, "end": 4.02, "lines": [{"text": "ВАЖЕН ЛИ", "accent": False, "size": "small"}, {"text": "ПОРЯДОК", "accent": True, "size": "big"}]},
    {"start": 4.29, "end": 5.19, "lines": [{"text": "И ИЗ ЗА ЭТОГО", "accent": False, "size": "small"}, {"text": "ВЫБИРАЮ", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.09, "lines": [{"text": "НЕВЕРНУЮ", "accent": False, "size": "small"}, {"text": "ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 7.38, "lines": [{"text": "ПОДСЧЕТА", "accent": False, "size": "small"}, {"text": "НА ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 7.38, "end": 8.40, "lines": [{"text": "Я ПОСЧИТАЛ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.39, "lines": [{"text": "БЕЗ УЧЕТА", "accent": False, "size": "small"}, {"text": "ПОРЯДКА", "accent": True, "size": "big"}]},
    {"start": 9.39, "end": 10.95, "lines": [{"text": "ТАМ ГДЕ ПОРЯДОК НА", "accent": False, "size": "small"}, {"text": "САМОМ ДЕЛЕ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 11.88, "lines": [{"text": "ИМЕЛ", "accent": False, "size": "small"}, {"text": "ЗНАЧЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 12.30, "end": 13.12, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.12, "end": 14.43, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.43, "end": 16.02, "lines": [{"text": "КОТОРЫЙ ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 16.02, "end": 17.94, "lines": [{"text": "КОГДА ПОРЯДОК ВАЖЕН", "accent": False, "size": "small"}, {"text": "А КОГДА НЕТ", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.05, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.05, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.79, "end": 3.03}, {"start": 4.95, "end": 5.73}, {"start": 11.16, "end": 11.88}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (Рома, 22.380s): a task sometimes gives one extra unneeded
# number, but out of habit all condition numbers get plugged in; the
# app's breakdown shows exactly which numbers are actually needed
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ЛИШНЕЕ ЧИСЛО", "В ЗАДАНИИ ИСПОЛЬЗУЕШЬ?"], "end": 1.95}
g_cards = [
    {"start": 1.95, "end": 2.97, "lines": [{"text": "В ЗАДАНИИ ЕГЭ", "accent": False, "size": "small"}, {"text": "ЛИШНЕЕ ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 2.97, "end": 4.74, "lines": [{"text": "КОТОРОЕ ВООБЩЕ", "accent": False, "size": "small"}, {"text": "НЕ НУЖНО", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 5.88, "lines": [{"text": "А Я ПО ПРИВЫЧКЕ", "accent": False, "size": "small"}, {"text": "СТАРАЮСЬ", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 7.08, "lines": [{"text": "ИСПОЛЬЗОВАТЬ ВСЕ", "accent": False, "size": "small"}, {"text": "ЧИСЛА", "accent": True, "size": "big"}]},
    {"start": 7.08, "end": 7.89, "lines": [{"text": "ИЗ УСЛОВИЯ", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.21, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.05, "lines": [{"text": "Я СПЕЦИАЛЬНО", "accent": False, "size": "small"}, {"text": "ВПИСАЛ", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 10.87, "lines": [{"text": "ФОРМУЛУ И", "accent": False, "size": "small"}, {"text": "ТО САМОЕ", "accent": True, "size": "big"}]},
    {"start": 10.87, "end": 11.94, "lines": [{"text": "ЛИШНЕЕ", "accent": False, "size": "small"}, {"text": "ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 12.18, "end": 13.20, "lines": [{"text": "И ПОЛУЧИЛ ИЗ ЗА ЭТОГО", "accent": False, "size": "small"}, {"text": "НЕВЕРНЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.32, "end": 14.40, "lines": [{"text": "ОТВЕТ", "accent": False, "size": "small"}, {"text": "В ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 16.23, "lines": [{"text": "К ЗАДАНИЕМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.23, "end": 17.28, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "small"}]},
    {"start": 17.28, "end": 18.57, "lines": [{"text": "КАКИЕ ЧИСЛА ИЗ", "accent": False, "size": "small"}, {"text": "УСЛОВИЯ", "accent": True, "size": "big"}]},
    {"start": 18.57, "end": 20.22, "lines": [{"text": "НА САМОМ ДЕЛЕ", "accent": False, "size": "small"}, {"text": "НУЖНЫ ДЛЯ РЕШЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 20.49, "end": 21.30, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.30, "end": 22.380, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.34, "end": 2.61}, {"start": 9.57, "end": 9.75}, {"start": 13.32, "end": 13.68}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (mother, 25.346s): daughter solves tasks almost without
# mistakes at home in a calm pace but makes uncharacteristic simple
# mistakes under a timer; it's the rush, not the topic, causing them;
# the app's breakdown trains solving under limited-time conditions
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ДОМА БЕЗ ОШИБОК", "НА ВРЕМЕНИ ИХ ДОПУСКАЕШЬ?"], "end": 1.95}
h_cards = [
    {"start": 1.95, "end": 2.91, "lines": [{"text": "ДОЧЬ РЕШАЕТ ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОЧТИ БЕЗ ОШИБОК", "accent": True, "size": "big"}]},
    {"start": 2.91, "end": 4.29, "lines": [{"text": "ДОМА В СПОКОЙНОМ", "accent": False, "size": "small"}, {"text": "ТЕМПЕ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 5.88, "lines": [{"text": "НО ЗАСЕЧЕННОМ ПО", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 7.77, "lines": [{"text": "ПРОБНИКИ ДОПУСКАЕТ", "accent": False, "size": "small"}, {"text": "САМЫЕ ПРОСТЫЕ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 9.75, "lines": [{"text": "ОБЫЧНО", "accent": False, "size": "small"}, {"text": "НЕСВОЙСТВЕННЫЕ ЕЙ ОШИБКИ", "accent": True, "size": "small"}]},
    {"start": 10.44, "end": 11.23, "lines": [{"text": "Я ЗАСЕКЛА", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 11.23, "end": 12.36, "lines": [{"text": "СПЕЦИАЛЬНОЕ И", "accent": False, "size": "small"}, {"text": "УВИДЕЛА", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.47, "lines": [{"text": "ЧТО ИМЕННО", "accent": False, "size": "small"}, {"text": "СПЕШКА", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.46, "lines": [{"text": "А НЕ САМА", "accent": False, "size": "small"}, {"text": "ТЕМА", "accent": True, "size": "big"}]},
    {"start": 14.46, "end": 15.75, "lines": [{"text": "СТАЛА", "accent": False, "size": "small"}, {"text": "ПРИЧИНОЙ ЕЕ", "accent": True, "size": "big"}]},
    {"start": 15.75, "end": 17.22, "lines": [{"text": "ОШИБОК В", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 17.22, "end": 18.24, "lines": [{"text": "ТРЕНАЖЕРЕ К", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 18.24, "end": 19.38, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 19.38, "end": 21.00, "lines": [{"text": "КОТОРЫЙ ТРЕНИРУЕТ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 22.95, "lines": [{"text": "ИМЕННО В УСЛОВИЯХ", "accent": False, "size": "small"}, {"text": "ОГРАНИЧЕННОГО ВРЕМЕНИ", "accent": True, "size": "small"}]},
    {"start": 23.49, "end": 24.30, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 24.30, "end": 25.346, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 8.46, "end": 9.12}, {"start": 12.72, "end": 13.47}, {"start": 14.76, "end": 15.48}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (mother, 21.122s): daughter's school handed out a task packet
# for the wrong exam profile; mother cross-checked the profile number on
# the cover against the exam application and they didn't match; the
# app's bank has tasks for the correct profile, no packet mix-ups
# ---------------------------------------------------------------------------
i_intro = {"lines": ["НЕ ТОТ ПРОФИЛЬ", "В ШКОЛЕ ВЫДАЛИ?"], "end": 1.95}
i_cards = [
    {"start": 1.95, "end": 3.03, "lines": [{"text": "ДОЧЕРИ В ШКОЛЕ ВЫДАЛИ", "accent": False, "size": "small"}, {"text": "КОМПЛЕКТ", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 4.56, "lines": [{"text": "ЗАДАНИЙ ЕГЭ НЕ ТОГО", "accent": False, "size": "small"}, {"text": "ПРОФИЛЯ", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 5.94, "lines": [{"text": "КОТОРЫЙ ОНА ВООБЩЕ", "accent": False, "size": "small"}, {"text": "СДАЕТ", "accent": True, "size": "big"}]},
    {"start": 5.94, "end": 7.41, "lines": [{"text": "И ОНА ЗАМЕТИЛА ЭТО", "accent": False, "size": "small"}, {"text": "НЕ СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 7.41, "end": 8.55, "lines": [{"text": "Я СЛУЧАЙНО СВЕРИЛА", "accent": False, "size": "small"}, {"text": "НОМЕР", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.51, "lines": [{"text": "ПРОФИЛЯ НА", "accent": False, "size": "small"}, {"text": "ОБЛОЖКЕ", "accent": True, "size": "big"}]},
    {"start": 9.51, "end": 10.53, "lines": [{"text": "КОМПЛЕКТА С", "accent": False, "size": "small"}, {"text": "НОМЕРОМ", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 11.94, "lines": [{"text": "В ЕЕ ЗАЯВЛЕНИИ НА", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕН", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.17, "lines": [{"text": "ОНИ НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАЛИ", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 14.65, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.65, "end": 15.87, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 16.83, "lines": [{"text": "ИМЕННО ПОД", "accent": False, "size": "small"}, {"text": "НУЖНЫЙ ПРОФИЛЬ", "accent": True, "size": "big"}]},
    {"start": 16.83, "end": 18.57, "lines": [{"text": "БЕЗ ПУТАНИЦЫ МЕЖДУ", "accent": False, "size": "small"}, {"text": "КОМПЛЕКТАМИ", "accent": True, "size": "small"}]},
    {"start": 19.17, "end": 20.00, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.00, "end": 21.122, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 3.15, "end": 3.66}, {"start": 7.95, "end": 8.25}, {"start": 12.60, "end": 13.08}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
