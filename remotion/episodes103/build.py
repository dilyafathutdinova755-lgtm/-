#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-SIXTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes103/.

Three returning hosts, no new faces: "Рома" / black Under Armour hoodie
(a, c, e), "mother" / bookshelf+doorway apartment with small framed
picture (b, d), "teen boy on couch" / bookshelf+plant+window room (f).

Sub-themes: a history question about 18th-century culture where only
one surname surfaced, needing more names paired with achievements;
reading a task breakdown alongside a daughter and feeling the
explanation has to be clear enough for a grown-up out of school for
years; "why" on the exam answered honestly with "because that's what
the answer key says," which needs the real reason spelled out in
words; alternating-vowel roots that are confusing one pair at a time
rather than all at once; a chess-playing relative's daily study
inspiring the same habit with exam tasks, thirty extra solved a month
later; and knowing only "the branch of power at home" as a joke
answer when the real branches of government need to be exact.
"""
import json

REAL_DURATION = {
    "a": 18.27, "b": 19.44, "c": 18.72,
    "d": 20.04, "e": 15.21, "f": 17.31,
}
SOURCE_FILE = {
    "a": "bvdfjhhdfhdfhgd", "b": "fdhgfdgdfgfdgfdg", "c": "fhshhfhgg",
    "d": "gfdhfdfghdgfdsg", "e": "hfdhgdgfdgdfgd", "f": "ngfdjhdshgghfdgfg",
}
FIXES = {
    "a": {"вегэ": "егэ"},
    "b": {},
    "c": {"ключи": "ключе", "заданием": "заданиям"},
    "d": {},
    "e": {},
    "f": {},
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
    with open(f"../asr_coffee123_56/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (Рома, 18.27s): a history question about 18th-century
# culture leaves only one surname standing -- one person doesn't make
# an era, so the app's history games pair names with achievements
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВСПОМНИЛ ТОЛЬКО", "ЛОМОНОСОВА"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "НА ЕГЭ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ВОПРОС ПРО КУЛЬТУРУ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ВОСЕМНАДЦАТОГО ВЕКА", "accent": False, "size": "small"}, {"text": "Я ВСПОМНИЛ", "accent": True, "size": "small"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ЛОМОНОСОВА", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ОДИН ЧЕЛОВЕК", "accent": False, "size": "small"}, {"text": "НЕ ДЕЛАЕТ ЭПОХУ", "accent": True, "size": "small"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "НУЖНЫ ЕЩЕ", "accent": False, "size": "small"}, {"text": "ИМЕНА И ДОСТИЖЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 15.00, "lines": [{"text": "ИМЕНА И ДОСТИЖЕНИЯ", "accent": False, "size": "small"}, {"text": "СОЕДИНЯЮТСЯ В ПАРЫ", "accent": True, "size": "small"}]},
    {"start": 15.00, "end": 16.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.27, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.55, "end": 3.81}, {"start": 5.04, "end": 7.74}, {"start": 14.97, "end": 15.93}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 19.44s): reading a task breakdown alongside a
# daughter makes a parent feel like a student again -- if it's clear to
# her, it was written well, and the app's breakdown stays clear even
# for someone long out of school
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЧИТАЮ РАЗБОР", "И ЧУВСТВУЮ СЕБЯ УЧЕНИЦЕЙ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ПОПЫТАЛАСЬ ЧИТАТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР С ДОЧЕРЬЮ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ВПЕРВЫЕ ЗА", "accent": False, "size": "small"}, {"text": "МНОГО ЛЕТ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ПОЧУВСТВОВАЛА СЕБЯ", "accent": False, "size": "small"}, {"text": "УЧЕНИЦЕЙ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ЕСЛИ РАЗБОР", "accent": False, "size": "small"}, {"text": "ПОНЯТЕН МНЕ", "accent": True, "size": "small"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ЗНАЧИТ ОН", "accent": False, "size": "small"}, {"text": "НАПИСАН ХОРОШО", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 15.00, "lines": [{"text": "ПОНЯТНЫЙ ДАЖЕ", "accent": False, "size": "small"}, {"text": "ТЕМ КТО ДАВНО", "accent": True, "size": "small"}]},
    {"start": 15.00, "end": 16.60, "lines": [{"text": "ЗАКОНЧИЛ", "accent": False, "size": "small"}, {"text": "ШКОЛУ", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 17.80, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 19.44, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.55, "end": 6.93}, {"start": 9.36, "end": 10.65}, {"start": 15.69, "end": 16.71}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 18.72s): "because that's what the answer key says"
# doesn't work outside the exam -- the reason needs to exist in words,
# and the app's breakdown writes that reason out for every answer
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЛЮБИМЫЙ ОТВЕТ", "ПОТОМУ ЧТО ТАК В КЛЮЧЕ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ЛЮБИМЫЙ ОТВЕТ", "accent": False, "size": "small"}, {"text": "НА ВОПРОС ПОЧЕМУ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ПОТОМУ ЧТО", "accent": False, "size": "small"}, {"text": "ТАК В КЛЮЧЕ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НЕ РАБОТАЕТ", "accent": False, "size": "small"}, {"text": "НИ НА УРОКЕ", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "НИ", "accent": False, "size": "small"}, {"text": "ДОМА", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ПРИЧИНУ НУЖНО", "accent": False, "size": "small"}, {"text": "ЗНАТЬ СЛОВАМИ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "ИНАЧЕ КЛЮЧ", "accent": False, "size": "small"}, {"text": "ОСТАЕТСЯ ШИФРОМ", "accent": True, "size": "small"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.60, "lines": [{"text": "У КАЖДОГО ОТВЕТА", "accent": False, "size": "small"}, {"text": "ЕСТЬ ПРИЧИНА", "accent": True, "size": "small"}]},
    {"start": 16.60, "end": 17.60, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.60, "end": 18.72, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.54, "end": 4.11}, {"start": 8.85, "end": 10.02}, {"start": 15.51, "end": 16.44}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 20.04s): alternating-vowel roots are confusing one
# pair at a time, not all at once -- the app's games repeat exactly one
# pair at a time instead of dumping the whole list together
# ---------------------------------------------------------------------------
d_intro = {"lines": ["КОРНИ НАЗЫВАЕТ", "ПЕРЕВЕРТЫШАМИ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "КОРНИ С", "accent": False, "size": "small"}, {"text": "ЧЕРЕДУЮЩИМИСЯ ГЛАСНЫМИ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НАЗЫВАЮ ИХ", "accent": False, "size": "small"}, {"text": "ПЕРЕВЕРТЫШАМИ", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ЧЕСТНО", "accent": False, "size": "small"}, {"text": "ПРИЗНАЮСЬ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ОНИ МЕНЯ", "accent": False, "size": "small"}, {"text": "ПЕРЕВОРАЧИВАЮТ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "РАЗБИРАТЬСЯ", "accent": False, "size": "small"}, {"text": "ПО ОДНОЙ ПАРЕ", "accent": True, "size": "small"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "СО ВСЕМИ СРАЗУ", "accent": True, "size": "small"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.40, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.20, "lines": [{"text": "КОРНИ ПОВТОРЯЮТСЯ", "accent": False, "size": "small"}, {"text": "ПО ОДНОЙ ПАРЕ", "accent": True, "size": "small"}]},
    {"start": 18.20, "end": 19.20, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.04, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 6.66, "end": 7.80}, {"start": 9.18, "end": 11.25}, {"start": 16.26, "end": 17.43}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 15.21s): a chess-playing relative's daily study
# inspires the same habit with exam tasks -- thirty extra solved a
# month later, and the app's FIPI bank picks a morning task in a minute
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ДЯДЯ РЕШАЕТ ЭТЮД", "Я РЕШАЮ ЗАДАНИЕ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "ДЯДЯ ШАХМАТИСТ", "accent": False, "size": "small"}, {"text": "РЕШАЕТ ЭТЮД", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "КАЖДОЕ", "accent": False, "size": "small"}, {"text": "УТРО", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "Я РЕШИЛ", "accent": False, "size": "small"}, {"text": "ТО ЖЕ САМОЕ", "accent": True, "size": "small"}]},
    {"start": 6.40, "end": 8.00, "lines": [{"text": "С ЗАДАНИЕМ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "ЧЕРЕЗ МЕСЯЦ", "accent": False, "size": "small"}, {"text": "ТРИДЦАТЬ ЗАДАНИЙ", "accent": True, "size": "small"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "А ЭТО", "accent": False, "size": "small"}, {"text": "УЖЕ ЗАМЕТНО", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.80, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 13.60, "lines": [{"text": "ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЗА МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 14.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 15.21, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.37, "end": 2.85}, {"start": 7.20, "end": 9.03}, {"start": 12.15, "end": 12.99}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 17.31s): "the branch of power at home"
# is a joke answer for the social studies exam -- the real branches and
# their functions need to be exact, and the app's games repeat them in
# rounds
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗНАЮ ТОЛЬКО", "ВЛАСТЬ РОДИТЕЛЕЙ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "НА ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "СПРОСЯТ ПРО", "accent": False, "size": "small"}, {"text": "ВИДЫ ВЛАСТИ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "А Я ПОМНЮ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ТУ", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ЧТО У", "accent": False, "size": "small"}, {"text": "РОДИТЕЛЕЙ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ВЕТВИ ВЛАСТИ", "accent": False, "size": "small"}, {"text": "И ИХ ФУНКЦИИ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "НУЖНО ЗНАТЬ", "accent": False, "size": "small"}, {"text": "ТОЧНО", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.80, "end": 16.00, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.00, "end": 17.31, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.98, "end": 3.06}, {"start": 5.49, "end": 6.12}, {"start": 14.04, "end": 15.03}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
