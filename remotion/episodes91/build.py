#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-FOURTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes91/.

Three returning hosts, no new faces: "blonde in cream sweater" (a, b),
"blue-shirt brunette" / THE SMITHS poster room (c, d, e), "mother" (f).

Sub-themes: finding a year-old solved EGE task in an old notebook and
being motivated by seeing her own growth instead of horrified by it,
guessing the bottom half of a board solution hidden behind a tall
classmate's head and getting the guess wrong, two EGE folders where
the "deal with later" one grows into a mountain faster than the
"practiced" one, writing history dates on a palm before a quiz when
the real exam won't allow it, a notebook where red-pen corrections
now outnumber black ink and the red itself becomes the reason to stop
reviewing it, and a mother's "be more careful" that never works because
carefulness turns out to be a consequence of understanding, not a skill.
"""
import json

REAL_DURATION = {
    "a": 22.240, "b": 24.172, "c": 22.338,
    "d": 21.591, "e": 23.575, "f": 21.360,
}
SOURCE_FILE = {
    "a": "fdsgvsdbsdgsdfvgsdf", "b": "fgsgfvgsdfdfsd", "c": "gdgdgfdgvbsgsf",
    "d": "gdhyehehrytg", "e": "retetertert", "f": "rgegdfggert",
}
FIXES = {
    "a": {"ужаснось": "ужаснулась"},
    "f": {"поневнимательности": "невнимательности", "перестало": "перестала"},
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
    with open(f"../asr_coffee123_44/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blonde cream sweater, 22.240s): an old notebook turns up a
# year-old EGE solution, horrifyingly sloppy -- but seeing her own
# growth is itself motivating, so she redoes the same tasks from
# scratch; the app's FIPI bank lets any task be revisited and resolved
# ---------------------------------------------------------------------------
a_intro = {"lines": ["СТАРАЯ ТЕТРАДЬ", "РЕШЕНИЯ ГОДИЧНОЙ ДАВНОСТИ?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 4.17, "lines": [{"text": "В СТАРОЙ ТЕТРАДИ", "accent": False, "size": "small"}, {"text": "НАШЛА РЕШЕНИЕ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 6.87, "lines": [{"text": "И УЖАСНУЛАСЬ", "accent": False, "size": "small"}, {"text": "КАК КОРЯВО БЫЛО", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 10.35, "lines": [{"text": "Я ПОНЯЛА ЧТО", "accent": False, "size": "small"}, {"text": "СВОЙ РОСТ МОТИВИРУЕТ", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 13.02, "lines": [{"text": "И ЗАХОТЕЛА", "accent": False, "size": "small"}, {"text": "РЕШИТЬ ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 13.89, "end": 15.90, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.52, "lines": [{"text": "ГДЕ К ЛЮБОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 17.76, "end": 19.68, "lines": [{"text": "МОЖНО ВЕРНУТЬСЯ", "accent": False, "size": "small"}, {"text": "И РЕШИТЬ ПОВТОРНО", "accent": True, "size": "big"}]},
    {"start": 20.37, "end": 21.30, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.30, "end": 22.240, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.10, "end": 5.76}, {"start": 9.93, "end": 10.35}, {"start": 18.09, "end": 18.42}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde cream sweater, 24.172s): sitting behind a tall
# classmate during a board review, only the top half of the solution is
# visible, the bottom half gets guessed and the guess turns out wrong
# at home; the app's text breakdown shows the full solution top to
# bottom, nothing blocked
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ВИЖУ ТОЛЬКО", "ПОЛОВИНУ РЕШЕНИЯ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.06, "lines": [{"text": "НА УРОКЕ УЧИТЕЛЬ", "accent": False, "size": "small"}, {"text": "РАЗБИРАЛ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 5.79, "lines": [{"text": "Я СИДЕЛА ЗА СПИНОЙ", "accent": False, "size": "small"}, {"text": "ВЫСОКОГО ОДНОКЛАССНИКА", "accent": True, "size": "small"}]},
    {"start": 6.12, "end": 8.25, "lines": [{"text": "И ВИДЕЛА ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ВЕРХНЮЮ ПОЛОВИНУ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.44, "lines": [{"text": "НИЖНЮЮ ЧАСТЬ", "accent": False, "size": "small"}, {"text": "ДОПИСЫВАЛА ПО ДОГАДКЕ", "accent": True, "size": "big"}]},
    {"start": 11.58, "end": 13.89, "lines": [{"text": "И ДОМА ВЫЯСНИЛОСЬ", "accent": False, "size": "small"}, {"text": "ДОГАДКА БЫЛА НЕВЕРНОЙ", "accent": True, "size": "big"}]},
    {"start": 14.61, "end": 16.83, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ТЕКСТОВЫЙ", "accent": True, "size": "small"}]},
    {"start": 16.95, "end": 19.17, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ГДЕ РЕШЕНИЕ ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 19.77, "end": 21.45, "lines": [{"text": "ОТ ПЕРВОЙ СТРОКИ", "accent": False, "size": "small"}, {"text": "ДО ПОСЛЕДНЕЙ", "accent": True, "size": "big"}]},
    {"start": 22.23, "end": 23.37, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.37, "end": 24.172, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.99, "end": 7.38}, {"start": 13.50, "end": 13.89}, {"start": 18.87, "end": 19.17}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 22.338s): two EGE folders, one for
# practiced tasks and one for later, and the second grows faster than
# the first -- everything scary to open piles up into a mountain; the
# app's FIPI bank keeps tasks in order so hard ones can't be siloed away
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ОДНА ПАПКА ЕГЭ", "РАСТЕТ БЫСТРЕЕ ДРУГОЙ?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.72, "lines": [{"text": "У МЕНЯ ДВЕ ПАПКИ", "accent": False, "size": "small"}, {"text": "ЕГЭ ПРОБНЫЕ И ПОТОМ", "accent": True, "size": "big"}]},
    {"start": 4.26, "end": 6.06, "lines": [{"text": "И ВТОРАЯ", "accent": False, "size": "small"}, {"text": "РАСТЕТ БЫСТРЕЕ", "accent": True, "size": "big"}]},
    {"start": 7.68, "end": 10.26, "lines": [{"text": "ПОТОМ Я СКЛАДЫВАЮ", "accent": False, "size": "small"}, {"text": "ВСЕ ЧТО СТРАШНО", "accent": True, "size": "big"}]},
    {"start": 10.59, "end": 12.90, "lines": [{"text": "И ОНО КОПИТСЯ", "accent": False, "size": "small"}, {"text": "ПРЕВРАЩАЕТСЯ В ГОРУ", "accent": True, "size": "small"}]},
    {"start": 13.89, "end": 15.90, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.11, "end": 17.43, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ИДУТ ПО ПОРЯДКУ", "accent": True, "size": "big"}]},
    {"start": 17.79, "end": 19.77, "lines": [{"text": "И СЛОЖНЫЕ", "accent": False, "size": "small"}, {"text": "НЕ ПРЯЧУТСЯ В ПАПКУ", "accent": True, "size": "big"}]},
    {"start": 20.49, "end": 21.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.40, "end": 22.338, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.31, "end": 5.64}, {"start": 12.72, "end": 12.90}, {"start": 18.60, "end": 18.93}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 21.591s): history dates for the EGE
# get written on a palm before a quiz, but the real exam won't allow
# that -- only what got repeated at least five times actually survives
# in memory; the app's memory games repeat dates over and over instead
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ДАТЫ НА ЛАДОНИ", "НА ЭКЗАМЕНЕ ТАК НЕ ВЫЙДЕТ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 4.17, "lines": [{"text": "ДАТЫ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЗАПИСЫВАЮ НА ЛАДОНИ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 6.18, "lines": [{"text": "А НА ЭКЗАМЕНЕ", "accent": False, "size": "small"}, {"text": "ТАК НЕ РАЗРЕШАТ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 9.27, "lines": [{"text": "ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАТЬ", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 12.81, "lines": [{"text": "В ПАМЯТИ ОСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТО ЧТО ПОВТОРИЛА", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 15.63, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 15.81, "end": 16.77, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.22, "end": 19.02, "lines": [{"text": "ГДЕ ДАТЫ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ ПОМНОГУ", "accent": True, "size": "small"}]},
    {"start": 19.68, "end": 20.76, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 21.591, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.82, "end": 6.18}, {"start": 12.42, "end": 12.81}, {"start": 17.73, "end": 18.18}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 23.575s): red-pen corrections on EGE
# mistakes now outnumber the black ink in her notebook, and the red
# itself becomes scary enough that she stops returning to those pages,
# even though they are the most useful ones; the app's text breakdown
# is calm plain text, safe to revisit without dread
# ---------------------------------------------------------------------------
e_intro = {"lines": ["КРАСНОГО БОЛЬШЕ", "ЧЕМ ЧЕРНОГО?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.75, "lines": [{"text": "ОШИБКИ В ЕГЭ", "accent": False, "size": "small"}, {"text": "РАЗБИРАЮ КРАСНОЙ РУЧКОЙ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 6.60, "lines": [{"text": "И КРАСНОГО В НЕЙ", "accent": False, "size": "small"}, {"text": "БОЛЬШЕ ЧЕМ ЧЕРНОГО", "accent": True, "size": "big"}]},
    {"start": 8.22, "end": 9.03, "lines": [{"text": "КРАСНАЯ", "accent": False, "size": "small"}, {"text": "ПУГАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.36, "end": 11.49, "lines": [{"text": "Я ПЕРЕСТАЛА", "accent": False, "size": "small"}, {"text": "ВОЗВРАЩАТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 11.94, "end": 14.04, "lines": [{"text": "ХОТЯ ОНИ", "accent": False, "size": "small"}, {"text": "САМЫЕ ПОЛЕЗНЫЕ", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 17.73, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 19.35, "lines": [{"text": "СПОКОЙНЫЙ ТЕКСТ", "accent": False, "size": "small"}, {"text": "КОТОРОМУ", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 20.97, "lines": [{"text": "МОЖНО ВОЗВРАЩАТЬСЯ", "accent": False, "size": "small"}, {"text": "БЕЗ СТРАХА", "accent": True, "size": "big"}]},
    {"start": 21.63, "end": 22.70, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.70, "end": 23.575, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 8.76, "end": 9.03}, {"start": 13.68, "end": 14.04}, {"start": 20.73, "end": 20.97}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 21.360s): a daughter's careless EGE mistakes meet
# "be more careful" that never helps -- the mother realizes carefulness
# is a consequence of understanding, not a skill, and stops repeating
# the advice; the app's text breakdown builds understanding instead of
# just telling her to focus
# ---------------------------------------------------------------------------
f_intro = {"lines": ["БУДЬ ВНИМАТЕЛЬНЕЕ", "НИКОГДА НЕ ПОМОГАЕТ?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.39, "lines": [{"text": "ДОЧЬ РЕШАЕТ ЕГЭ", "accent": False, "size": "small"}, {"text": "С ОШИБКАМИ", "accent": True, "size": "big"}]},
    {"start": 3.90, "end": 5.31, "lines": [{"text": "Я ГОВОРЮ", "accent": False, "size": "small"}, {"text": "БУДЬ ВНИМАТЕЛЬНЕЕ", "accent": True, "size": "small"}]},
    {"start": 5.73, "end": 6.99, "lines": [{"text": "И ЭТО", "accent": False, "size": "small"}, {"text": "НИКОГДА НЕ ПОМОГАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.04, "end": 9.33, "lines": [{"text": "Я ПОНЯЛА ЧТО", "accent": False, "size": "small"}, {"text": "ВНИМАТЕЛЬНОСТЬ", "accent": True, "size": "small"}]},
    {"start": 9.63, "end": 10.74, "lines": [{"text": "НЕ НАВЫК", "accent": False, "size": "small"}, {"text": "А СЛЕДСТВИЕ", "accent": True, "size": "big"}]},
    {"start": 10.89, "end": 12.81, "lines": [{"text": "ПОНИМАНИЯ И", "accent": False, "size": "small"}, {"text": "Я ПЕРЕСТАЛА ПОВТОРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 16.17, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 18.69, "lines": [{"text": "КОТОРЫЙ ПОМОГАЕТ", "accent": False, "size": "small"}, {"text": "ПОНЯТЬ А НЕ СОБРАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 19.41, "end": 20.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.40, "end": 21.360, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.74, "end": 5.31}, {"start": 8.73, "end": 9.33}, {"start": 17.37, "end": 17.55}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
