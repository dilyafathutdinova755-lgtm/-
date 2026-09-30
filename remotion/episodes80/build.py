#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-THIRD 'coffee123'
batch (9 episodes uploaded under the same tag after thirty-two prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes80/.

Three returning hosts, no new faces: blue-shirt brunette HeyGen avatar
(a, c, i), "Рома" HeyGen avatar (b, d, g), blonde-sweater HeyGen avatar
(e, f, h).

Sub-themes: outdated/unverified source material (an old collection's
numbering, an older sibling's advice, a mnemonic emptied of meaning) vs.
the app's up-to-date FIPI bank (a, d); knowing something "in general
terms" without surviving a precise/different-context test -- a
transition between steps, a method mix-up, false confidence from easy
tasks, a slip on the very last step, a wording, similar names (b, c,
e, f, g, i).
"""
import json

REAL_DURATION = {
    "a": 22.167, "b": 20.226, "c": 21.360,
    "d": 17.800, "e": 22.764, "f": 21.200,
    "g": 18.840, "h": 23.340, "i": 21.400,
}
SOURCE_FILE = {
    "a": "fdghdfgdgdgdg", "b": "gffhghfhngfhgfhf", "c": "gfjhdffdjdfhfghfd",
    "d": "gfjnherhhtrhrh", "e": "gfnfnfdhghrt", "f": "ghrhregheghehth",
    "g": "hfbnfjjnnmnejtuyhet", "h": "hgmjfjhhtbterhhgerg", "i": "jghftfhhjgftrsetgfd",
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
    "b": {"тренажери": "тренажере"},
    "f": {"тренажеры": "тренажере"},
    "i": {"игра": "егэ"},
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
    words = json.load(open(f"../asr_coffee123_33/{src}_words.json"))
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
# Episode A (brunette, 22.167s): a task number in an old collection may
# not match the same task in the current demo version; the app's bank
# uses the correct current-year numbering
# ---------------------------------------------------------------------------
a_intro = {"lines": ["НОМЕР ЗАДАНИЯ", "В СТАРОМ СБОРНИКЕ?"], "end": 1.77}
a_cards = [
    {"start": 1.77, "end": 2.58, "lines": [{"text": "ЕГЭ В СТАРОМ", "accent": False, "size": "small"}, {"text": "СБОРНИКЕ", "accent": True, "size": "big"}]},
    {"start": 2.58, "end": 3.63, "lines": [{"text": "МОЖЕТ НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.50, "lines": [{"text": "С ТЕМ ЖЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 6.00, "lines": [{"text": "В АКТУАЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 6.84, "end": 7.65, "lines": [{"text": "Я РЕШАЛА", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 8.73, "lines": [{"text": "ПО СТАРОЙ", "accent": False, "size": "small"}, {"text": "НУМЕРАЦИИ", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 9.53, "lines": [{"text": "ВЕСЬ", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 9.53, "end": 10.62, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "СВЕРИЛА", "accent": True, "size": "big"}]},
    {"start": 10.62, "end": 12.24, "lines": [{"text": "С ОФИЦИАЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИЕЙ", "accent": True, "size": "small"}]},
    {"start": 12.24, "end": 13.05, "lines": [{"text": "ЭТОГО", "accent": False, "size": "small"}, {"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 14.67, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 15.90, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 17.22, "lines": [{"text": "С ЗАДАНИЯМИ ПОД", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНОЙ", "accent": True, "size": "big"}]},
    {"start": 17.22, "end": 18.90, "lines": [{"text": "АКТУАЛЬНОЙ НА ЭТОТ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 19.69, "lines": [{"text": "С ВЕРНОЙ", "accent": False, "size": "small"}, {"text": "НУМЕРАЦИЕЙ", "accent": True, "size": "big"}]},
    {"start": 20.22, "end": 21.36, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.36, "end": 22.167, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.77, "end": 6.00}, {"start": 10.29, "end": 11.46}, {"start": 15.33, "end": 15.90}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 20.226s): each step of solving a task can be correct
# while the transition between two neighboring steps stays unclear; the
# app's text breakdown explains the transition between every pair of steps
# ---------------------------------------------------------------------------
b_intro = {"lines": ["КАЖДЫЙ ШАГ ВЕРНЫЙ", "А ПЕРЕХОД НЕПОНЯТНЫЙ?"], "end": 1.65}
b_cards = [
    {"start": 1.65, "end": 2.76, "lines": [{"text": "РЕШЕНИЯ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.76, "end": 3.69, "lines": [{"text": "МОЖЕТ БЫТЬ", "accent": False, "size": "small"}, {"text": "ВЕРНЫМ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 5.82, "lines": [{"text": "А ПЕРЕХОД МЕЖДУ", "accent": False, "size": "small"}, {"text": "СОСЕДНИМИ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 6.90, "lines": [{"text": "ШАГАМИ", "accent": False, "size": "small"}, {"text": "НЕПОНЯТНЫМ", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 8.43, "lines": [{"text": "Я РЕШАЛ ТАК", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.72, "lines": [{"text": "А ОБЪЯСНИТЬ", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИКАМ", "accent": True, "size": "small"}]},
    {"start": 9.72, "end": 11.58, "lines": [{"text": "ИМЕННО ЭТОТ ПЕРЕХОД МЕЖДУ", "accent": False, "size": "small"}, {"text": "ШАГАМИ", "accent": True, "size": "big"}]},
    {"start": 11.58, "end": 12.66, "lines": [{"text": "НЕ МОГ", "accent": False, "size": "small"}, {"text": "ТОЛКОМ", "accent": True, "size": "big"}]},
    {"start": 13.02, "end": 13.81, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.81, "end": 15.30, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.47, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "ПЕРЕХОД", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 17.88, "lines": [{"text": "МЕЖДУ КАЖДОЙ ПАРОЙ", "accent": False, "size": "small"}, {"text": "ШАГОВ", "accent": True, "size": "big"}]},
    {"start": 18.36, "end": 19.38, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.38, "end": 20.226, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.36, "end": 6.90}, {"start": 9.84, "end": 10.80}, {"start": 15.78, "end": 16.11}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (brunette, 21.360s): two similar-looking math tasks
# sometimes need completely different methods; the app's text breakdown
# clearly separates similar types of tasks from each other
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ДВА ПОХОЖИХ ЗАДАНИЯ", "РАЗНЫЕ СПОСОБЫ?"], "end": 1.92}
c_cards = [
    {"start": 1.92, "end": 3.15, "lines": [{"text": "ПОХОЖИХ НА ВИД", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.08, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "РЕШАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.85, "lines": [{"text": "СОВЕРШЕННО РАЗНЫМИ", "accent": False, "size": "small"}, {"text": "СПОСОБАМИ", "accent": True, "size": "big"}]},
    {"start": 6.81, "end": 7.92, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАЛА", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 9.30, "lines": [{"text": "ЭТИ ДВА ТИПА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.38, "lines": [{"text": "НА ПРОБНИКЕ И", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 12.12, "lines": [{"text": "РЕШАЛА НЕ ТЕМ", "accent": False, "size": "small"}, {"text": "СПОСОБОМ", "accent": True, "size": "big"}]},
    {"start": 12.84, "end": 13.63, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.63, "end": 15.48, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.48, "end": 16.44, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ЧЕТКО", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 18.18, "lines": [{"text": "РАЗДЕЛЯЕТ ПОХОЖИЕ", "accent": False, "size": "small"}, {"text": "ТИПЫ", "accent": True, "size": "big"}]},
    {"start": 18.18, "end": 19.03, "lines": [{"text": "ЗАДАНИЙ МЕЖДУ", "accent": False, "size": "small"}, {"text": "СОБОЙ", "accent": True, "size": "big"}]},
    {"start": 19.59, "end": 20.56, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.56, "end": 21.360, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.26, "end": 4.80}, {"start": 6.96, "end": 7.47}, {"start": 16.59, "end": 16.92}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (Рома, 17.800s): an older brother's 3-year-old EGE advice
# doesn't always match what will be this year; the app's FIPI bank
# reflects exactly the current year's format
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СОВЕТ БРАТА", "ТРЕХЛЕТНЕЙ ДАВНОСТИ?"], "end": 1.68}
d_cards = [
    {"start": 1.68, "end": 3.27, "lines": [{"text": "В ФОРМАТЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕХЛЕТНЕЙ", "accent": True, "size": "big"}]},
    {"start": 3.27, "end": 4.32, "lines": [{"text": "НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 5.64, "lines": [{"text": "С ТЕМ ЧТО БУДЕТ", "accent": False, "size": "small"}, {"text": "В ЭТОМ ГОДУ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.20, "lines": [{"text": "Я ГОТОВИЛСЯ ПО", "accent": False, "size": "small"}, {"text": "СОВЕТАМ", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.04, "lines": [{"text": "ВСЕ", "accent": False, "size": "small"}, {"text": "ЛЕТО", "accent": True, "size": "big"}]},
    {"start": 8.04, "end": 9.36, "lines": [{"text": "ПОКА НЕ СРАВНИЛ ИХ С", "accent": False, "size": "small"}, {"text": "ОФИЦИАЛЬНОЙ", "accent": True, "size": "small"}]},
    {"start": 9.36, "end": 10.62, "lines": [{"text": "ДЕМОВЕРСИЕЙ", "accent": False, "size": "small"}, {"text": "ЭТОГО ГОДА", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 11.71, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.71, "end": 12.69, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.69, "end": 14.91, "lines": [{"text": "ОТРАЖАЮЩИЙ ФОРМАТ ИМЕННО", "accent": False, "size": "small"}, {"text": "ТЕКУЩЕГО ГОДА", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 15.84, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ПРОШЛЫХ ЛЕТ", "accent": True, "size": "big"}]},
    {"start": 16.08, "end": 17.00, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.00, "end": 17.800, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.40, "end": 3.27}, {"start": 8.31, "end": 9.36}, {"start": 12.90, "end": 13.71}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde, 22.764s): easy tasks at the start of a variant can
# create a false sense the whole thing will be simple; the app's FIPI
# bank has tasks of varying difficulty that keep you in tone throughout
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЛЕГКИЕ ЗАДАНИЯ В НАЧАЛЕ", "ОБМАНЫВАЮТ?"], "end": 1.74}
e_cards = [
    {"start": 1.74, "end": 2.54, "lines": [{"text": "ЕГЭ В НАЧАЛЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТА", "accent": True, "size": "big"}]},
    {"start": 2.54, "end": 4.20, "lines": [{"text": "ИНОГДА СОЗДАЮТ", "accent": False, "size": "small"}, {"text": "ЛОЖНЫЕ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.25, "lines": [{"text": "ЧУВСТВА ЧТО ВЕСЬ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 5.25, "end": 6.60, "lines": [{"text": "ОКАЖЕТСЯ ТАКИМ ЖЕ", "accent": False, "size": "small"}, {"text": "ПРОСТЫМ", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 8.91, "lines": [{"text": "Я РАССЛАБЛЯЛАСЬ", "accent": False, "size": "small"}, {"text": "ПОСЛЕ", "accent": True, "size": "big"}]},
    {"start": 8.91, "end": 9.71, "lines": [{"text": "ПЕРВЫХ ЛЕГКИХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 9.71, "end": 10.89, "lines": [{"text": "И ТЕРЯЛА", "accent": False, "size": "small"}, {"text": "КОНЦЕНТРАЦИЮ", "accent": True, "size": "small"}]},
    {"start": 10.89, "end": 12.27, "lines": [{"text": "ИМЕННО НА", "accent": False, "size": "small"}, {"text": "СЛОЖНЫХ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.10, "lines": [{"text": "ЗАДАНИЯХ В КОНЦЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТА", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 14.66, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.66, "end": 15.75, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.75, "end": 17.49, "lines": [{"text": "С ЗАДАНИЯМИ РАЗНОЙ", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТИ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 19.05, "lines": [{"text": "КОТОРЫЕ ДЕРЖАТ В", "accent": False, "size": "small"}, {"text": "ТОНУСЕ", "accent": True, "size": "big"}]},
    {"start": 19.05, "end": 20.13, "lines": [{"text": "ОТ НАЧАЛА ДО", "accent": False, "size": "small"}, {"text": "КОНЦА", "accent": True, "size": "big"}]},
    {"start": 20.79, "end": 21.87, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.87, "end": 22.764, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.48, "end": 4.20}, {"start": 9.99, "end": 10.89}, {"start": 16.14, "end": 17.01}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde, 21.200s): a correct method can go wrong not
# somewhere but on the very last step; the app's text breakdown works
# through the solution to the very last step
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ВЕРНЫЙ СПОСОБ", "СВОРАЧИВАЕТ НЕ ТУДА?"], "end": 1.68}
f_cards = [
    {"start": 1.68, "end": 2.50, "lines": [{"text": "РЕШЕНИЯ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.50, "end": 3.99, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "СВОРАЧИВАЕТ", "accent": True, "size": "small"}]},
    {"start": 3.99, "end": 5.94, "lines": [{"text": "ИМЕННО НА САМОМ", "accent": False, "size": "small"}, {"text": "ПОСЛЕДНЕМ", "accent": True, "size": "big"}]},
    {"start": 6.69, "end": 8.43, "lines": [{"text": "Я ТАК ТЕРЯЛА БАЛЛЫ", "accent": False, "size": "small"}, {"text": "НА ПОСЛЕДНЕМ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.45, "lines": [{"text": "ШАГЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 11.58, "lines": [{"text": "ХОТЯ ВСЕ ДО ЭТОГО ДЕЛАЛА", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНО", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 13.71, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.71, "end": 15.36, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 17.10, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПРОРАБАТЫВАЕТ", "accent": True, "size": "small"}]},
    {"start": 17.10, "end": 18.54, "lines": [{"text": "РЕШЕНИЕ ДО САМОГО", "accent": False, "size": "small"}, {"text": "ПОСЛЕДНЕГО", "accent": True, "size": "big"}]},
    {"start": 19.26, "end": 20.34, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.34, "end": 21.200, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 3.06, "end": 3.99}, {"start": 7.08, "end": 8.43}, {"start": 16.05, "end": 16.59}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (Рома, 18.840s): a term known in one textbook's wording can
# go unrecognized in the practice test's wording; the app's history
# games train a term in different wordings at once
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ЗНАЕШЬ ТЕРМИН", "ПО СВОЕМУ УЧЕБНИКУ?"], "end": 1.53}
g_cards = [
    {"start": 1.53, "end": 2.34, "lines": [{"text": "ПО ИСТОРИИ ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 2.34, "end": 3.75, "lines": [{"text": "В ОДНОЙ ФОРМУЛИРОВКЕ", "accent": False, "size": "small"}, {"text": "УЧЕБНИКА", "accent": True, "size": "small"}]},
    {"start": 3.75, "end": 4.63, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "УЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.63, "end": 5.70, "lines": [{"text": "ФОРМУЛИРОВКИ", "accent": False, "size": "small"}, {"text": "ПРОБНИКА", "accent": True, "size": "small"}]},
    {"start": 5.97, "end": 6.78, "lines": [{"text": "Я ОТВЕЧАЛ НА", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 7.71, "lines": [{"text": "ПО СВОЕМУ", "accent": False, "size": "small"}, {"text": "УЧЕБНИКУ", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 9.12, "lines": [{"text": "УВЕРЕННО А НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.12, "end": 10.11, "lines": [{"text": "ФОРМУЛИРОВКА", "accent": False, "size": "small"}, {"text": "ЗВУЧАЛА", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.19, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "НЕЗНАКОМО", "accent": True, "size": "big"}]},
    {"start": 11.52, "end": 12.31, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.31, "end": 13.35, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.49, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.49, "end": 15.87, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 16.86, "lines": [{"text": "В РАЗНЫХ ФОРМУЛИРОВКАХ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 17.13, "end": 18.04, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.04, "end": 18.840, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 4.32, "end": 5.16}, {"start": 9.27, "end": 10.11}, {"start": 14.64, "end": 15.03}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blonde, 23.340s): a mnemonic for a grammar rule can be
# learned by heart while forgetting what it stood for; the app's games
# link the hint to the rule itself
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ВЫУЧИЛ ЗАПОМИНАЛКУ", "И ЗАБЫЛ ЗАЧЕМ ОНА?"], "end": 1.71}
h_cards = [
    {"start": 1.71, "end": 3.06, "lines": [{"text": "ДЛЯ ПРАВИЛА ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 4.71, "lines": [{"text": "ДЛЯ ЕГЭ МОЖНО", "accent": False, "size": "small"}, {"text": "ВЫУЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.71, "end": 6.42, "lines": [{"text": "И ЗАБЫТЬ ЧТО ОНА", "accent": False, "size": "small"}, {"text": "ОЗНАЧАЛА", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 8.43, "lines": [{"text": "Я ПОМНИЛА САМУ", "accent": False, "size": "small"}, {"text": "ФРАЗУ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.48, "lines": [{"text": "ПОДСКАЗКУ", "accent": False, "size": "small"}, {"text": "НАИЗУСТЬ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.40, "lines": [{"text": "А ОБЪЯСНИТЬ КАКОЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.83, "lines": [{"text": "ОНА ОБОЗНАЧАЕТ УЖЕ НЕ МОГЛА", "accent": False, "size": "small"}, {"text": "ВСПОМНИТЬ", "accent": True, "size": "big"}]},
    {"start": 14.73, "end": 15.55, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.55, "end": 16.50, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.43, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 18.63, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 18.63, "end": 19.68, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "СВЯЗЫВАЮТ", "accent": True, "size": "big"}]},
    {"start": 19.68, "end": 20.67, "lines": [{"text": "ПОДСКАЗКУ С САМИМ", "accent": False, "size": "small"}, {"text": "ПРАВИЛОМ", "accent": True, "size": "big"}]},
    {"start": 21.27, "end": 22.38, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.38, "end": 23.340, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 5.07, "end": 5.91}, {"start": 13.11, "end": 13.83}, {"start": 18.75, "end": 19.08}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (brunette, 21.400s): it's easy to mix up two historical
# figures with similar names but completely different roles; the app's
# history games train memorization of similar historical names
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ПУТАЕШЬ ИСТОРИЧЕСКИХ", "ДЕЯТЕЛЕЙ?"], "end": 1.59}
i_cards = [
    {"start": 1.59, "end": 2.42, "lines": [{"text": "НА ЕГЭ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЛЕГКО", "accent": True, "size": "big"}]},
    {"start": 2.42, "end": 4.05, "lines": [{"text": "ПЕРЕПУТАТЬ ДВУХ", "accent": False, "size": "small"}, {"text": "ДЕЯТЕЛЕЙ", "accent": True, "size": "big"}]},
    {"start": 4.05, "end": 5.85, "lines": [{"text": "С ПОХОЖИМИ ИМЕНАМИ НА", "accent": False, "size": "small"}, {"text": "РАЗНЫМИ РОЛЯМИ", "accent": True, "size": "big"}]},
    {"start": 6.66, "end": 7.77, "lines": [{"text": "Я ПУТАЛА ТАКИХ", "accent": False, "size": "small"}, {"text": "ДЕЯТЕЛЕЙ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 9.63, "lines": [{"text": "НА ПРОБНИКЕ ХОТЯ ПО", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНОСТИ", "accent": True, "size": "small"}]},
    {"start": 9.63, "end": 11.85, "lines": [{"text": "КАЖДОГО МОГЛА ОПИСАТЬ БЕЗ ЕДИНОЙ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 12.96, "end": 13.78, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.78, "end": 15.00, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.80, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 19.05, "lines": [{"text": "ПОХОЖИХ ИСТОРИЧЕСКИХ", "accent": False, "size": "small"}, {"text": "ИМЕН", "accent": True, "size": "big"}]},
    {"start": 19.62, "end": 20.60, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.60, "end": 21.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 1.89, "end": 2.34}, {"start": 6.75, "end": 7.77}, {"start": 16.47, "end": 16.80}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
