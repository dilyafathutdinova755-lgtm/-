#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-FIFTH 'coffee123'
batch (9 episodes uploaded under the same tag after twenty-four prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes72/.

Two brand-new hosts this batch (both teenage boys, first appearance in
the series): curly-hair boy in black Under Armour hoodie (a, b, c) and
wavy-hair boy in gray t-shirt, different room (d, e, f). The mother
(parent POV, returning) covers g, h, i.
Sub-themes: confusing similar concepts/events without independent
recall practice (a, d, g), a correct answer that isn't real
understanding of the solution method (b, e, i), a task bank/variant
set that drifted from the current exam format (c, f, h).
"""
import json

REAL_DURATION = {
    "a": 18.840, "b": 18.480, "c": 17.218,
    "d": 18.040, "e": 17.880, "f": 17.026,
    "g": 19.266, "h": 19.500, "i": 18.400,
}
SOURCE_FILE = {
    "a": "gfhdhfghgfhgfh", "b": "gfhdjgsfkjjksfj", "c": "gsrjmxfjfrtjtx",
    "d": "gfjxmxkjhnx", "e": "gfkfshhdhgh", "f": "hkgdjmftyhtfhn",
    "g": "gfnfdgbvcfxgc", "h": "gngcfhngnfcgbn", "i": "m.xfghnxhngxfh",
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
    "b": {"тестовое": "тестовую", "участь": "часть", "текстовыя": "текстовый"},
    "c": {"фипис": "фипи"},
    "d": {"училс": "учился"},
    "e": {"текстовая": "текстовый"},
    "f": {"фипис": "фипи"},
    "h": {"фипис": "фипи"},
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
    words = json.load(open(f"../asr_coffee123_25/{src}_words.json"))
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
# Episode A (new host: curly-hair boy, 18.840s): confusing two similar
# concepts in obshestvoznanie despite feeling sure you remembered the
# definition; the app's memorization games make you distinguish similar
# concepts independently
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПУТАЕШЬ ПОХОЖИЕ", "ПОНЯТИЯ НА ЕГЭ?"], "end": 2.37}
a_cards = [
    {"start": 2.37, "end": 3.33, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ПРОЧИТАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.33, "end": 4.56, "lines": [{"text": "ПЕРЕСКАЗАТЬ ЕГО ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 6.24, "lines": [{"text": "СОВСЕМ ДРУГИМИ", "accent": False, "size": "small"}, {"text": "СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 6.24, "end": 7.50, "lines": [{"text": "Я БЫЛ ЧТО ПОМНЮ", "accent": False, "size": "small"}, {"text": "УВЕРЕН", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 9.12, "lines": [{"text": "ОПРЕДЕЛЕНИЕ ПОКА НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.12, "end": 9.96, "lines": [{"text": "НЕ ДВА", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАЛ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 11.16, "lines": [{"text": "ПОХОЖИХ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЯ", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 13.08, "lines": [{"text": "В ЕГЭ ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.08, "end": 14.55, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 15.36, "lines": [{"text": "ГДЕ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЯ", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 16.86, "lines": [{"text": "НУЖНО САМОСТОЯТЕЛЬНО", "accent": False, "size": "small"}, {"text": "РАЗЛИЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 18.840, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.37, "end": 2.70}, {"start": 11.16, "end": 11.49}, {"start": 16.86, "end": 17.19}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (curly-hair boy, 18.480s): the method of elimination can give
# a correct answer on the EGE without understanding the real solution
# method; the app's text breakdown shows the true method start to finish
# ---------------------------------------------------------------------------
b_intro = {"lines": ["МЕТОД ИСКЛЮЧЕНИЯ", "ЭТО НЕ ПОНИМАНИЕ"], "end": 1.62}
b_cards = [
    {"start": 1.62, "end": 2.55, "lines": [{"text": "ЕГЭ ДАЕТ", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 2.55, "end": 3.54, "lines": [{"text": "ВЕРНЫЙ БЕЗ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.62, "lines": [{"text": "ПОНИМАНИЯ", "accent": False, "size": "small"}, {"text": "НАСТОЯЩЕГО", "accent": True, "size": "big"}]},
    {"start": 4.62, "end": 5.73, "lines": [{"text": "СПОСОБА", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 6.87, "lines": [{"text": "Я ТАК ТЕСТОВУЮ", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЛ", "accent": True, "size": "big"}]},
    {"start": 6.87, "end": 7.92, "lines": [{"text": "ЧАСТЬ ПОКА", "accent": False, "size": "small"}, {"text": "МЕСЯЦАМИ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 9.15, "lines": [{"text": "ПОХОЖЕЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.95, "lines": [{"text": "НЕ БЕЗ ВАРИАНТОВ", "accent": False, "size": "small"}, {"text": "ПОПАЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 12.36, "lines": [{"text": "В ЕГЭ К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.74, "lines": [{"text": "ТЕКСТОВЫЙ КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.74, "end": 14.70, "lines": [{"text": "ВЕРНЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.63, "lines": [{"text": "СПОСОБ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 16.65, "lines": [{"text": "ОТ НАЧАЛА ДО", "accent": False, "size": "small"}, {"text": "КОНЦА", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 18.480, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.62, "end": 1.95}, {"start": 10.95, "end": 11.28}, {"start": 16.65, "end": 16.98}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (curly-hair boy, 17.218s): a variant downloaded long ago from
# an old folder can drift from the current exam format; the app's FIPI
# bank updates together with the actual exam
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ВАРИАНТ ЕГЭ", "СКАЧАННЫЙ ДАВНО?"], "end": 1.89}
c_cards = [
    {"start": 1.89, "end": 3.18, "lines": [{"text": "СТАРОЙ ПАПКИ НА", "accent": False, "size": "small"}, {"text": "КОМПЬЮТЕРЕ", "accent": True, "size": "big"}]},
    {"start": 3.18, "end": 4.11, "lines": [{"text": "МОЖЕТ НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 5.04, "lines": [{"text": "С ТЕКУЩИМ", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 5.04, "end": 5.88, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 7.26, "lines": [{"text": "ТРЕНИРОВАЛСЯ ПО ТАКОЙ", "accent": False, "size": "small"}, {"text": "ПАПКЕ", "accent": True, "size": "big"}]},
    {"start": 7.26, "end": 8.16, "lines": [{"text": "ВСЕ ПОКА", "accent": False, "size": "small"}, {"text": "ЛЕТО", "accent": True, "size": "big"}]},
    {"start": 8.16, "end": 9.15, "lines": [{"text": "НЕ ЗАДАНИЯ СО", "accent": False, "size": "small"}, {"text": "СВЕРИЛ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.62, "lines": [{"text": "ДЕМОВЕРСИЕЙ", "accent": False, "size": "small"}, {"text": "СВЕЖЕЙ", "accent": True, "size": "big"}]},
    {"start": 10.62, "end": 11.64, "lines": [{"text": "В ЕГЭ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.64, "end": 12.69, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.69, "end": 13.53, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 14.76, "lines": [{"text": "ОБНОВЛЯЮТСЯ ПОД", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЕ", "accent": True, "size": "big"}]},
    {"start": 14.76, "end": 15.60, "lines": [{"text": "ЭКЗАМЕН", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 17.218, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 10.62, "end": 10.95}, {"start": 15.60, "end": 15.93}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (new host: wavy-hair boy, 18.040s): historical events for the
# EGE are easy to confuse with similar ones the very next day; the app's
# memorization games bring the topic back after a real gap, not just once
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПУТАЕШЬ СОБЫТИЯ", "ПО ИСТОРИИ?"], "end": 2.04}
d_cards = [
    {"start": 2.04, "end": 3.09, "lines": [{"text": "МОЖНО НАЗВАТЬ НА", "accent": False, "size": "small"}, {"text": "УВЕРЕННО", "accent": True, "size": "big"}]},
    {"start": 3.09, "end": 4.23, "lines": [{"text": "И ПЕРЕПУТАТЬ", "accent": False, "size": "small"}, {"text": "УРОКЕ", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 5.40, "lines": [{"text": "С ПОХОЖИМ УЖЕ НА", "accent": False, "size": "small"}, {"text": "СЛЕДУЮЩИЙ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.33, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 7.23, "lines": [{"text": "СОБЫТИЯ ПЕРЕД", "accent": False, "size": "small"}, {"text": "УЧИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.04, "lines": [{"text": "НО", "accent": False, "size": "small"}, {"text": "ПРОБНИКОМ", "accent": True, "size": "big"}]},
    {"start": 8.04, "end": 8.88, "lines": [{"text": "ИЗ НИХ НЕ", "accent": False, "size": "small"}, {"text": "ПОЛОВИНА", "accent": True, "size": "big"}]},
    {"start": 8.88, "end": 9.84, "lines": [{"text": "ВСПОМНИЛАСЬ В", "accent": False, "size": "small"}, {"text": "НУЖНЫЙ", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 10.71, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "МОМЕНТ", "accent": True, "size": "big"}]},
    {"start": 10.71, "end": 11.76, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 13.02, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.02, "end": 13.98, "lines": [{"text": "КОТОРЫЕ К", "accent": False, "size": "small"}, {"text": "ВОЗВРАЩАЮТ", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 14.91, "lines": [{"text": "ЧЕРЕЗ ДЕНЬ", "accent": False, "size": "small"}, {"text": "ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 16.05, "lines": [{"text": "А НЕ ОДИН", "accent": False, "size": "small"}, {"text": "РАЗ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 18.040, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.04, "end": 2.37}, {"start": 10.71, "end": 11.04}, {"start": 16.05, "end": 16.38}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (wavy-hair boy, 17.880s): getting the right answer doesn't
# mean the solution method was understood to the end; the app's text
# breakdown explains the correct method start to finish, not just result
# ---------------------------------------------------------------------------
e_intro = {"lines": ["РЕШИЛ ЗАДАНИЕ", "НО ПОНЯЛ ЛИ СПОСОБ?"], "end": 1.98}
e_cards = [
    {"start": 1.98, "end": 3.06, "lines": [{"text": "ЕГЭ НЕ", "accent": False, "size": "small"}, {"text": "ЗНАЧИТ", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 4.17, "lines": [{"text": "ЧТО РЕШЕНИЯ БЫЛ", "accent": False, "size": "small"}, {"text": "СПОСОБ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 5.52, "lines": [{"text": "ПОНЯТ ДО", "accent": False, "size": "small"}, {"text": "КОНЦА", "accent": True, "size": "big"}]},
    {"start": 5.52, "end": 6.36, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ПРОХОДИЛ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.23, "lines": [{"text": "ВАРИАНТ ЗА ПОКА", "accent": False, "size": "small"}, {"text": "ВАРИАНТОМ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.91, "lines": [{"text": "НА КОНСУЛЬТАЦИИ НЕ", "accent": False, "size": "small"}, {"text": "ПОПРОСИЛИ", "accent": True, "size": "big"}]},
    {"start": 8.91, "end": 10.56, "lines": [{"text": "РЕШЕНИЕ ВСЛУХ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 10.56, "end": 11.49, "lines": [{"text": "В К", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.49, "end": 12.72, "lines": [{"text": "ЕСТЬ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 12.72, "end": 13.92, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.92, "end": 14.91, "lines": [{"text": "РЕШЕНИЯ А", "accent": False, "size": "small"}, {"text": "СПОСОБ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 15.99, "lines": [{"text": "НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТ", "accent": True, "size": "big"}]},
    {"start": 15.99, "end": 17.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.98, "end": 2.31}, {"start": 10.56, "end": 10.89}, {"start": 15.99, "end": 16.32}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (wavy-hair boy, 17.026s): a task bank recommended in the class
# chat doesn't always match the official format; the app's bank has
# checked, up-to-date tasks for this year
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СБОРНИК ИЗ ЧАТА", "КЛАССА НАДЕЖЕН?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.70, "lines": [{"text": "КОТОРЫЙ В", "accent": False, "size": "small"}, {"text": "СОВЕТУЕТ", "accent": True, "size": "big"}]},
    {"start": 2.70, "end": 3.63, "lines": [{"text": "КЛАССА НЕ", "accent": False, "size": "small"}, {"text": "ЧАТЕ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.50, "lines": [{"text": "ВСЕГДА С", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.73, "lines": [{"text": "ОФИЦИАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 6.99, "lines": [{"text": "Я ТАКОЙ СБОРНИК", "accent": False, "size": "small"}, {"text": "РЕШАЛ", "accent": True, "size": "big"}]},
    {"start": 6.99, "end": 8.19, "lines": [{"text": "МЕСЯЦ ПОКА НЕ", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛ", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.09, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.09, "end": 10.53, "lines": [{"text": "УПРАЗДНЕННОЙ ФОРМУЛИРОВКОЙ", "accent": False, "size": "small"}, {"text": "ДАВНО", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 11.73, "lines": [{"text": "В ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.05, "lines": [{"text": "БАНК ПРОВЕРЕННЫМИ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.31, "lines": [{"text": "И АКТУАЛЬНЫМИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 14.31, "end": 15.11, "lines": [{"text": "ЭТОГО", "accent": False, "size": "small"}, {"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 15.11, "end": 17.026, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.86, "end": 2.19}, {"start": 10.53, "end": 10.86}, {"start": 15.11, "end": 15.44}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (mother, 19.266s): a history topic sometimes survives in a
# child's memory only until the end of the lesson, and dates get mixed up
# days later; the app's memorization games return to the topic after it
# already seemed learned
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ИСТОРИЯ ДЕРЖИТСЯ В ПАМЯТИ", "ТОЛЬКО ДО КОНЦА УРОКА?"], "end": 2.07}
g_cards = [
    {"start": 2.07, "end": 2.97, "lines": [{"text": "ИНОГДА В", "accent": False, "size": "small"}, {"text": "ДЕРЖИТСЯ", "accent": True, "size": "big"}]},
    {"start": 2.97, "end": 3.78, "lines": [{"text": "РОВНО ДО", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 3.78, "end": 5.10, "lines": [{"text": "УРОКА", "accent": False, "size": "small"}, {"text": "КОНЦА", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 5.97, "lines": [{"text": "Я ЧТО", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 5.97, "end": 7.38, "lines": [{"text": "ДОЧЬ ПЕРЕСКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "УВЕРЕННО", "accent": True, "size": "big"}]},
    {"start": 7.38, "end": 8.19, "lines": [{"text": "ВЕЧЕРОМ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.03, "lines": [{"text": "А ЧЕРЕЗ ДВА", "accent": False, "size": "small"}, {"text": "ДНЯ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 10.50, "lines": [{"text": "В ДАТАХ", "accent": False, "size": "small"}, {"text": "ПУТАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.37, "lines": [{"text": "В ПО", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.37, "end": 12.33, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.41, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.41, "end": 14.46, "lines": [{"text": "К", "accent": False, "size": "small"}, {"text": "ВОЗВРАЩАЮТ", "accent": True, "size": "big"}]},
    {"start": 14.46, "end": 15.33, "lines": [{"text": "УЖЕ ПОСЛЕ", "accent": False, "size": "small"}, {"text": "ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 15.33, "end": 16.26, "lines": [{"text": "ТОГО КАК ОНА", "accent": False, "size": "small"}, {"text": "ВРОДЕ", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.58, "lines": [{"text": "БЫ", "accent": False, "size": "small"}, {"text": "ВЫУЧЕНА", "accent": True, "size": "big"}]},
    {"start": 17.58, "end": 19.266, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.07, "end": 2.40}, {"start": 10.50, "end": 10.83}, {"start": 17.58, "end": 17.91}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (mother, 19.500s): a task collection bought a year ago can
# drift from the real exam format by spring, so the child loses points on
# a mock exam despite solving tasks correctly; the app's FIPI bank updates
# under the actual format
# ---------------------------------------------------------------------------
h_intro = {"lines": ["СБОРНИК ДЛЯ ЕГЭ", "КУПЛЕННЫЙ ГОД НАЗАД?"], "end": 2.31}
h_cards = [
    {"start": 2.31, "end": 3.48, "lines": [{"text": "ГОД НАЗАД", "accent": False, "size": "small"}, {"text": "КУПЛЕННЫЙ", "accent": True, "size": "big"}]},
    {"start": 3.48, "end": 4.50, "lines": [{"text": "К МОЖЕТ", "accent": False, "size": "small"}, {"text": "ВЕСНЕ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.70, "lines": [{"text": "УЖЕ НЕ С РЕАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "СОВПАДАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 6.96, "lines": [{"text": "ЭКЗАМЕНА", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 7.98, "lines": [{"text": "Я НЕ СРАЗУ", "accent": False, "size": "small"}, {"text": "ПОНЯЛА", "accent": True, "size": "big"}]},
    {"start": 7.98, "end": 8.94, "lines": [{"text": "СЫН РЕШАЮТ", "accent": False, "size": "small"}, {"text": "ПОЧЕМУ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 10.14, "lines": [{"text": "ПРАВИЛЬНО А", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.22, "lines": [{"text": "НА ВСЕ РАВНО", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.36, "lines": [{"text": "БАЛЛЫ", "accent": False, "size": "small"}, {"text": "ТЕРЯЕТ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.53, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 14.70, "lines": [{"text": "СОБРАН БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.66, "lines": [{"text": "С КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 16.92, "lines": [{"text": "ОБНОВЛЯЮТСЯ ПОД", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 16.92, "end": 17.72, "lines": [{"text": "ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 17.72, "end": 19.500, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 2.31, "end": 2.64}, {"start": 12.36, "end": 12.69}, {"start": 17.72, "end": 18.05}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (mother, 18.400s): a child can solve a task wrong while being
# fully confident in the answer; the app's text breakdown shows exactly
# where the logic went wrong, not just the result
# ---------------------------------------------------------------------------
i_intro = {"lines": ["РЕБЕНОК УВЕРЕН", "В ОТВЕТЕ КОТОРЫЙ НЕВЕРНЫЙ?"], "end": 2.34}
i_cards = [
    {"start": 2.34, "end": 4.08, "lines": [{"text": "НЕПРАВИЛЬНО И ПРИ ЭТОМ БЫТЬ", "accent": False, "size": "small"}, {"text": "ПОЛНОСТЬЮ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.52, "lines": [{"text": "В ОТВЕТЕ", "accent": False, "size": "small"}, {"text": "УВЕРЕН", "accent": True, "size": "big"}]},
    {"start": 5.52, "end": 6.54, "lines": [{"text": "Я ОБ", "accent": False, "size": "small"}, {"text": "ОШИБКЕ", "accent": True, "size": "big"}]},
    {"start": 6.54, "end": 7.35, "lines": [{"text": "ТОЛЬКО ПОСЛЕ", "accent": False, "size": "small"}, {"text": "СЫНА", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 8.34, "lines": [{"text": "КАК", "accent": False, "size": "small"}, {"text": "ПОКАЗАЛА", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 10.02, "lines": [{"text": "РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "РЕПЕТИТОРУ", "accent": True, "size": "big"}]},
    {"start": 10.02, "end": 10.95, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 11.97, "lines": [{"text": "К ЗАДАНИЮ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 11.97, "end": 13.23, "lines": [{"text": "ЕСТЬ РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.49, "lines": [{"text": "СРАЗУ ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "КОТОРЫЙ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.36, "lines": [{"text": "ГДЕ ЛОГИКА", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 16.50, "lines": [{"text": "НЕ ТУДА", "accent": False, "size": "small"}, {"text": "ПОШЛА", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 18.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.34, "end": 2.67}, {"start": 10.02, "end": 10.35}, {"start": 16.50, "end": 16.83}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
