#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-SIXTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes83/.

Three returning hosts, no new faces: "teen boy on couch" (a, e),
"Рома" (b, c, f), "mother" (d).

Sub-themes: process failures that corrupt otherwise-correct work --
a shared doc resurrecting a deleted task, alphabetically-neighboring
terms swapped in memory, a wrong first step silently propagated
through an otherwise flawless solution, a similarly-spelled surname
confused in writing, a false symmetry assumed without checking it
applies, and a wrong book delivered under a near-identical cover.
"""
import json

REAL_DURATION = {
    "a": 24.471, "b": 20.695, "c": 22.240,
    "d": 22.978, "e": 22.000, "f": 22.444,
}
SOURCE_FILE = {
    "a": "fgjgjjfhfhfgh", "b": "gfhgfhfhfghfghg", "c": "gfhhfhfhfhfghfghf",
    "d": "hgfhfhfhfhfh", "e": "hgfhhgfhhfh", "f": "hgfhhhgfhfhf",
}
FIXES = {
    "e": {"тренажери": "тренажере"},
    "f": {"фип": "фипи"},
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
    with open(f"../asr_coffee123_36/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy, 24.471s): teacher collects ЕГЭ homework in a shared
# doc edited by several teachers; old deleted tasks sometimes resurface --
# a task marked outdated and removed got accidentally restored; the app's
# bank has no accidental rollbacks
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗАДАНИЕ УДАЛИЛИ", "А ОНО ВЕРНУЛОСЬ?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.60, "lines": [{"text": "НАШ УЧИТЕЛЬ СОБИРАЕТ", "accent": False, "size": "small"}, {"text": "В ДОКУМЕНТЕ", "accent": True, "size": "big"}]},
    {"start": 3.60, "end": 4.83, "lines": [{"text": "КОТОРЫЙ РЕДАКТИРУЕТ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 5.82, "lines": [{"text": "НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "УЧИТЕЛЕЙ", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 7.32, "lines": [{"text": "И СТАРЫЕ", "accent": False, "size": "small"}, {"text": "УДАЛЕННЫЕ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 7.47, "end": 8.34, "lines": [{"text": "ТАМ ИНОГДА", "accent": False, "size": "small"}, {"text": "ВСПЛЫВАЮТ", "accent": True, "size": "big"}]},
    {"start": 8.52, "end": 9.84, "lines": [{"text": "Я РЕШАЛ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 10.83, "lines": [{"text": "КОТОРОЕ", "accent": False, "size": "small"}, {"text": "ОКАЗЫВАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 11.01, "end": 12.30, "lines": [{"text": "ЕЩЕ НА ТОЙ НЕДЕЛЕ", "accent": False, "size": "small"}, {"text": "ПРИЗНАЛИ", "accent": True, "size": "big"}]},
    {"start": 12.30, "end": 13.53, "lines": [{"text": "ЕГО", "accent": False, "size": "small"}, {"text": "НЕАКТУАЛЬНЫМ", "accent": True, "size": "small"}]},
    {"start": 13.77, "end": 14.91, "lines": [{"text": "А ПОТОМ КТО ТО", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНО", "accent": True, "size": "big"}]},
    {"start": 15.06, "end": 15.90, "lines": [{"text": "ВЕРНУЛ ЕГО", "accent": False, "size": "small"}, {"text": "ОБРАТНО", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.06, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.06, "end": 17.94, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 18.18, "end": 19.14, "lines": [{"text": "БЕЗ СЛУЧАЙНЫХ", "accent": False, "size": "small"}, {"text": "ОТКАТОВ", "accent": True, "size": "big"}]},
    {"start": 19.44, "end": 20.67, "lines": [{"text": "ОДИН РАЗ УСТАРЕВШЕЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 20.85, "end": 22.20, "lines": [{"text": "ТАМ ПРОСТО НЕ", "accent": False, "size": "small"}, {"text": "ПОЯВИТСЯ СНОВА", "accent": True, "size": "big"}]},
    {"start": 22.50, "end": 23.58, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.58, "end": 24.471, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 10.41, "end": 10.83}, {"start": 14.64, "end": 15.27}, {"start": 18.36, "end": 18.69}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 20.695s): two Russian-language terms sit alphabetically
# next to each other in the dictionary and get mixed up by that
# neighborliness; the app's memory games specifically untangle such
# alphabetical-neighbor pairs
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ДВА ТЕРМИНА РЯДОМ", "ПО АЛФАВИТУ ПУТАЕШЬ?"], "end": 1.89}
b_cards = [
    {"start": 1.89, "end": 2.76, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "СТОЯЩИЕ", "accent": True, "size": "big"}]},
    {"start": 2.76, "end": 3.60, "lines": [{"text": "РЯДОМ", "accent": False, "size": "small"}, {"text": "ПО АЛФАВИТУ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.80, "lines": [{"text": "В СЛОВАРИКЕ Я ДО", "accent": False, "size": "small"}, {"text": "СИХ ПОР", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 5.76, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ПУТАЮ", "accent": True, "size": "big"}]},
    {"start": 5.76, "end": 7.23, "lines": [{"text": "МЕЖДУ СОБОЙ ПРОСТО", "accent": False, "size": "small"}, {"text": "ПО СОСЕДСТВУ", "accent": True, "size": "big"}]},
    {"start": 7.38, "end": 8.40, "lines": [{"text": "В СПИСКЕ Я", "accent": False, "size": "small"}, {"text": "НАЗЫВАЮ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.30, "lines": [{"text": "ОДИН", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.26, "lines": [{"text": "А В ГОЛОВЕ", "accent": False, "size": "small"}, {"text": "ВСПЛЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.26, "end": 11.40, "lines": [{"text": "СОСЕД ПО", "accent": False, "size": "small"}, {"text": "СЛОВАРНОЙ СТРАНИЦЕ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 12.63, "lines": [{"text": "А НЕ ТО ЧТО", "accent": False, "size": "small"}, {"text": "СПРОСИЛИ", "accent": True, "size": "big"}]},
    {"start": 12.96, "end": 13.80, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 14.70, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.75, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.93, "end": 17.40, "lines": [{"text": "КОТОРЫЕ РАЗВОДЯТ", "accent": False, "size": "small"}, {"text": "ТАКИЕ АЛФАВИТНЫЕ", "accent": True, "size": "small"}]},
    {"start": 17.40, "end": 18.51, "lines": [{"text": "СОСЕДСТВА", "accent": False, "size": "small"}, {"text": "СПЕЦИАЛЬНО", "accent": True, "size": "big"}]},
    {"start": 18.51, "end": 19.53, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 20.695, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.95, "end": 5.43}, {"start": 9.75, "end": 10.08}, {"start": 12.06, "end": 12.63}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 22.240s): makes a mistake right at the start of a
# multi-step task, then confidently builds the rest on that wrong number;
# the app's breakdown checks the solution starting from the very first step
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ОШИБАЕШЬСЯ В САМОМ", "НАЧАЛЕ РЕШЕНИЯ?"], "end": 1.89}
c_cards = [
    {"start": 1.89, "end": 3.00, "lines": [{"text": "В МНОГОХОДОВОМ ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ОШИБАЮСЬ", "accent": True, "size": "big"}]},
    {"start": 3.12, "end": 4.59, "lines": [{"text": "В САМОМ НАЧАЛЕ А ДАЛЬШЕ", "accent": False, "size": "small"}, {"text": "СЧИТАЮ", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 6.03, "lines": [{"text": "СОВЕРШЕННО ВЕРНЫМ", "accent": False, "size": "small"}, {"text": "СПОСОБОМ", "accent": True, "size": "big"}]},
    {"start": 6.24, "end": 8.10, "lines": [{"text": "ПРОСТО ОПИРАЯСЬ НА УЖЕ", "accent": False, "size": "small"}, {"text": "НЕВЕРНОЕ ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.96, "lines": [{"text": "НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ВТОРАЯ ЧАСТЬ РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 10.08, "end": 10.92, "lines": [{"text": "БЫЛА", "accent": False, "size": "small"}, {"text": "БЕЗУПРЕЧНОЙ", "accent": True, "size": "small"}]},
    {"start": 11.10, "end": 11.91, "lines": [{"text": "А", "accent": False, "size": "small"}, {"text": "НЕВЕРНОЙ ОКАЗАЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 12.00, "end": 13.23, "lines": [{"text": "ТОЛЬКО САМАЯ ПЕРВАЯ", "accent": False, "size": "small"}, {"text": "ЦИФРА", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.40, "lines": [{"text": "С КОТОРОЙ ВСЕ", "accent": False, "size": "small"}, {"text": "НАЧАЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 14.76, "end": 15.63, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 16.83, "lines": [{"text": "К ЗАДАНИЕМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.92, "end": 18.27, "lines": [{"text": "КОТОРЫЙ ПРОВЕРЯЕТ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 18.27, "end": 20.13, "lines": [{"text": "ЦЕЛИКОМ С САМОГО", "accent": False, "size": "small"}, {"text": "ПЕРВОГО ШАГА", "accent": True, "size": "big"}]},
    {"start": 20.43, "end": 21.30, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.30, "end": 22.240, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.64, "end": 3.00}, {"start": 10.38, "end": 10.92}, {"start": 12.75, "end": 13.23}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 22.978s): daughter confidently remembers facts about
# a historical figure but mixes up the surname with a similarly-spelled
# neighboring one in writing; the app's history games train such
# similarly-spelled surnames apart from each other
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ФАМИЛИЮ ПУТАЕШЬ", "С ПОХОЖЕЙ?"], "end": 1.89}
d_cards = [
    {"start": 1.89, "end": 2.97, "lines": [{"text": "ДОЧЬ УВЕРЕННО ПОМНИТ", "accent": False, "size": "small"}, {"text": "ФАКТЫ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 4.89, "lines": [{"text": "А ВОТ ФАМИЛИЮ", "accent": False, "size": "small"}, {"text": "ЭТОЙ ЛИЧНОСТИ", "accent": True, "size": "big"}]},
    {"start": 5.07, "end": 5.90, "lines": [{"text": "НА ПИСЬМЕ", "accent": False, "size": "small"}, {"text": "ПУТАЕТ", "accent": True, "size": "big"}]},
    {"start": 5.91, "end": 7.86, "lines": [{"text": "С ПОХОЖЕЙ ПО НАПИСАНИЮ", "accent": False, "size": "small"}, {"text": "СОСЕДНЕЙ ФАМИЛИИ", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.69, "lines": [{"text": "Я ПРОВЕРЯЛА ЕЕ", "accent": False, "size": "small"}, {"text": "ТЕТРАДЬ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 11.01, "lines": [{"text": "И УВИДЕЛА ТАМ", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 12.21, "lines": [{"text": "ЭТУ ОШИБКУ В", "accent": False, "size": "small"}, {"text": "НАПИСАНИИ", "accent": True, "size": "big"}]},
    {"start": 12.39, "end": 13.77, "lines": [{"text": "ФАМИЛИИ НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "РАЗ ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 14.28, "end": 15.15, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 16.05, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 17.58, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 17.73, "end": 18.99, "lines": [{"text": "НАПИСАНИЕ", "accent": False, "size": "small"}, {"text": "ПОХОЖИХ ФАМИЛИЙ", "accent": True, "size": "big"}]},
    {"start": 19.62, "end": 20.55, "lines": [{"text": "ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ДРУГ ОТ ДРУГА", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 21.90, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.90, "end": 22.978, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.55, "end": 5.76}, {"start": 10.77, "end": 11.01}, {"start": 13.29, "end": 13.77}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (teen boy, 22.000s): assumes symmetry in an ЕГЭ task where
# there isn't any, and doesn't check whether the shortcut actually applies
# to that specific case; the app's breakdown verifies the symmetry applies
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СИММЕТРИЮ ПРЕДПОЛАГАЕШЬ", "ТАМ ГДЕ ЕЕ НЕТ?"], "end": 1.98}
e_cards = [
    {"start": 1.98, "end": 2.94, "lines": [{"text": "В ЗАДАНИИ ЕГЭ", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 2.94, "end": 4.65, "lines": [{"text": "ПРЕДПОЛАГАЮ ТАМ ГДЕ", "accent": False, "size": "small"}, {"text": "НА САМОМ ДЕЛЕ НЕТ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.36, "lines": [{"text": "И ИЗ ЗА ЭТОГО", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.89, "lines": [{"text": "ПОЛУЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "НЕВЕРНЫМ", "accent": True, "size": "big"}]},
    {"start": 7.89, "end": 9.03, "lines": [{"text": "НА ПРОБНИКЕ Я", "accent": False, "size": "small"}, {"text": "ПОСТРОИЛ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 9.90, "lines": [{"text": "РЕШЕНИЕ ИМЕННО НА", "accent": False, "size": "small"}, {"text": "ТАКОЙ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.80, "lines": [{"text": "ЛОЖНОЙ", "accent": False, "size": "small"}, {"text": "СИММЕТРИИ", "accent": True, "size": "big"}]},
    {"start": 10.98, "end": 11.91, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "ГЛЯНУЛ", "accent": True, "size": "big"}]},
    {"start": 11.91, "end": 13.17, "lines": [{"text": "РАБОТАЕТ ЛИ ОНА ДЛЯ", "accent": False, "size": "small"}, {"text": "ЭТОГО", "accent": True, "size": "big"}]},
    {"start": 13.17, "end": 13.98, "lines": [{"text": "КОНКРЕТНОГО", "accent": False, "size": "small"}, {"text": "СЛУЧАЯ", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 14.78, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.78, "end": 16.38, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.38, "end": 17.76, "lines": [{"text": "КОТОРЫЙ ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯЕТ", "accent": True, "size": "big"}]},
    {"start": 17.76, "end": 18.96, "lines": [{"text": "ДЕЙСТВИТЕЛЬНО ЛИ", "accent": False, "size": "small"}, {"text": "СИММЕТРИЯ", "accent": True, "size": "big"}]},
    {"start": 18.96, "end": 19.89, "lines": [{"text": "ПРИМЕНИМА В", "accent": False, "size": "small"}, {"text": "ЗАДАЧЕ", "accent": True, "size": "big"}]},
    {"start": 20.19, "end": 21.00, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 22.000, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.49, "end": 2.94}, {"start": 10.02, "end": 10.80}, {"start": 17.91, "end": 18.33}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 22.444s): ordered an ЕГЭ prep book online by title, got
# sent one with an almost-identical cover but completely different
# content; solved it for a week before spotting the mismatch against the
# official demo version; the app's bank has no such cover/title confusion
# ---------------------------------------------------------------------------
f_intro = {"lines": ["КНИГУ ЗАКАЗАЛ", "А ПРИСЛАЛИ ДРУГУЮ?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.82, "lines": [{"text": "ПОСОБИЕ С ЗАДАНИЯМИ", "accent": False, "size": "small"}, {"text": "ОНЛАЙН", "accent": True, "size": "big"}]},
    {"start": 2.82, "end": 3.69, "lines": [{"text": "Я ЗАКАЗАЛ", "accent": False, "size": "small"}, {"text": "ПО НАЗВАНИЮ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 4.89, "lines": [{"text": "А ПРИСЛАЛИ", "accent": False, "size": "small"}, {"text": "ПОЧТИ ТАКУЮ ЖЕ", "accent": True, "size": "big"}]},
    {"start": 5.04, "end": 5.95, "lines": [{"text": "ПО ОБЛОЖКЕ", "accent": False, "size": "small"}, {"text": "НО", "accent": True, "size": "big"}]},
    {"start": 5.95, "end": 7.11, "lines": [{"text": "СОВСЕМ ДРУГУЮ ПО", "accent": False, "size": "small"}, {"text": "СОДЕРЖАНИЮ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.37, "lines": [{"text": "КНИГУ ДРУГОГО", "accent": False, "size": "small"}, {"text": "АВТОРА", "accent": True, "size": "big"}]},
    {"start": 8.64, "end": 9.51, "lines": [{"text": "Я РЕШАЛ ЕЕ", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 9.51, "end": 10.86, "lines": [{"text": "ПОКА НЕ СВЕРИЛ ПАРУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 10.86, "end": 11.97, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 11.97, "end": 13.95, "lines": [{"text": "И НЕ УВИДЕЛ ЯВНОЕ", "accent": False, "size": "small"}, {"text": "НЕСОВПАДЕНИЕ ФОРМАТА", "accent": True, "size": "small"}]},
    {"start": 14.25, "end": 15.10, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.10, "end": 15.95, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 17.10, "lines": [{"text": "БЕЗ ПУТАНИЦЫ С", "accent": False, "size": "small"}, {"text": "ПОХОЖИМИ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.42, "lines": [{"text": "ОБЛОЖКАМИ И", "accent": False, "size": "small"}, {"text": "НАЗВАНИЯМИ", "accent": True, "size": "small"}]},
    {"start": 18.75, "end": 20.28, "lines": [{"text": "ТАМ СРАЗУ ТОЧНО", "accent": False, "size": "small"}, {"text": "ТО ЧТО НУЖНО", "accent": True, "size": "big"}]},
    {"start": 20.55, "end": 21.40, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.40, "end": 22.444, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.26, "end": 4.80}, {"start": 8.76, "end": 9.51}, {"start": 12.57, "end": 12.93}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
