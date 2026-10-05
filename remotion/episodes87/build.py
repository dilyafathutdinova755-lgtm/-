#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTIETH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes87/.

Two returning hosts, no new faces: "teen boy on couch" / bookshelf+
plant+window room (a, d, e), "mother" / beige sweater + bookshelf+
doorway apartment (b, c, f).

Sub-themes: the same five unchecked-spelling words that refuse to
stick no matter how much the rest of the list gets memorized, a
daughter who studies Russian rules in the shower and swears it works
better, task sheets that get flour and sauce on them while solving in
the kitchen, not knowing which question to start analyzing a task
from without a given/find/method map, a deskmate who copies answers
and is then baffled the practice test goes badly, and nodding along
to an explanation that didn't actually land.
"""
import json

REAL_DURATION = {
    "a": 20.226, "b": 22.240, "c": 20.546,
    "d": 21.880, "e": 18.840, "f": 20.098,
}
SOURCE_FILE = {
    "a": "gfhfhgfhgfhf", "b": "hgfhfhgfhghfh", "c": "hgfhhfghfhfhfghfg",
    "d": "jhgngdbhtgyfhr", "e": "ngfdhtnjhgedgh", "f": "nrsgnfbdhbh",
}
FIXES = {
    "a": {"профия": "профиля"},
    "b": {"длего": "иногда"},
    "d": {"тренажерик": "тренажере", "текстовая": "текстовый"},
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
    with open(f"../asr_coffee123_40/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy on couch, 20.226s): the same five unchecked-vowel
# spelling words keep resisting no matter how well the rest of the list
# gets memorized, and rereading the whole list just for them is boring;
# the app's memory games repeat just the sticking words until they stick
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПЯТЬ СЛОВ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "В СПИСКЕ СЛОВ С", "accent": False, "size": "small"}, {"text": "НЕПРОВЕРЯЕМЫМИ ГЛАСНЫМИ", "accent": True, "size": "small"}]},
    {"start": 3.30, "end": 4.20, "lines": [{"text": "ДЛЯ ЕГЭ ПО РУССКОМУ У МЕНЯ", "accent": False, "size": "small"}, {"text": "ОСТАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 6.09, "lines": [{"text": "ОДНИ И ТЕ ЖЕ", "accent": False, "size": "small"}, {"text": "ПЯТЬ СЛОВ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.32, "lines": [{"text": "Я УПОРНО", "accent": False, "size": "small"}, {"text": "НЕ ПОМНЮ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 8.58, "lines": [{"text": "ОСТАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ЗАПОМНИЛИСЬ", "accent": True, "size": "small"}]},
    {"start": 8.76, "end": 9.93, "lines": [{"text": "А ЭТИ ПЯТЬ", "accent": False, "size": "small"}, {"text": "СОПРОТИВЛЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 10.14, "end": 12.21, "lines": [{"text": "ПЕРЕЧИТЫВАТЬ ВЕСЬ СПИСОК", "accent": False, "size": "small"}, {"text": "РАДИ НИХ СКУЧНО", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.92, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 14.19, "end": 15.24, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.42, "end": 17.07, "lines": [{"text": "ГДЕ СЛОВА", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 17.07, "end": 18.24, "lines": [{"text": "СНОВА И СНОВА", "accent": False, "size": "small"}, {"text": "ПОКА НЕ ЗАПОМНИШЬ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 19.35, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.35, "end": 20.226, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 9.15, "end": 9.93}, {"start": 11.85, "end": 12.21}, {"start": 17.70, "end": 18.24}]
process("a", a_cards, a_intro, a_emphasis)
# NB: ASR truncates "профиля" to "профия" here (see FIXES["a"]); card
# text above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode B (mother, 22.240s): a daughter studies Russian rules
# sometimes in the shower and swears it works better, and the test
# results back her up -- she remembers more than before and prefers
# repeating aloud to reading; the app's memory games let her repeat
# rules anywhere convenient, shower included
# ---------------------------------------------------------------------------
b_intro = {"lines": ["УЧИТ ПРАВИЛА", "ПОД ДУШЕМ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 4.02, "lines": [{"text": "ДОЧЬ УЧИТ ПРАВИЛА", "accent": False, "size": "small"}, {"text": "РУССКОГО ЯЗЫКА", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 5.70, "lines": [{"text": "ГОВОРИТ ЧТО ТАК", "accent": False, "size": "small"}, {"text": "ЛУЧШЕ ЗАПОМИНАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 6.06, "end": 7.17, "lines": [{"text": "И ВОЗРАЗИТЬ", "accent": False, "size": "small"}, {"text": "МНЕ НЕЧЕГО", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.27, "lines": [{"text": "Я СМОТРЕЛА НА", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТ ТЕСТА", "accent": True, "size": "big"}]},
    {"start": 9.57, "end": 10.83, "lines": [{"text": "ПОМНИТ ОНА", "accent": False, "size": "small"}, {"text": "БОЛЬШЕ ЧЕМ РАНЬШЕ", "accent": True, "size": "big"}]},
    {"start": 11.13, "end": 13.44, "lines": [{"text": "А ПОВТОРЯТЬ ВСЛУХ ЕЙ", "accent": False, "size": "small"}, {"text": "НРАВИТСЯ БОЛЬШЕ ЧЕМ ЧИТАТЬ", "accent": True, "size": "big"}]},
    {"start": 14.13, "end": 15.00, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.02, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 16.02, "end": 17.01, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.43, "end": 19.77, "lines": [{"text": "ГДЕ ПРАВИЛА МОЖНО", "accent": False, "size": "small"}, {"text": "ПОВТОРЯТЬ В ЛЮБОМ УДОБНОМ МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 20.40, "end": 21.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.40, "end": 22.240, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.70, "end": 7.17}, {"start": 8.30, "end": 8.85}, {"start": 12.00, "end": 12.48}]
process("b", b_cards, b_intro, b_emphasis)
# NB: ASR mishears "иногда" as "длего" here (see FIXES["b"]); card text
# above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode C (mother, 20.546s): a daughter solves an ЕГЭ task in the
# kitchen while mom cooks, and the task sheets get flour and sauce on
# them -- one sheet got soggy enough that the condition became
# unreadable and she solved an entirely different task; the app's
# tasks always display in full, no sauce can threaten them
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЗАДАНИЕ В МУКЕ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.24, "lines": [{"text": "ДОЧЬ РЕШАЕТ ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "НА КУХНЕ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 4.95, "lines": [{"text": "ПОКА Я ГОТОВЛЮ", "accent": False, "size": "small"}, {"text": "ЛИСТЫ С ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.27, "lines": [{"text": "У НЕЕ ВЕЧНО", "accent": False, "size": "small"}, {"text": "В МУКЕ И СОУСЕ", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 7.62, "lines": [{"text": "ОДИН ЛИСТ", "accent": False, "size": "small"}, {"text": "РАЗМОК", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 9.39, "lines": [{"text": "ТАК ЧТО УСЛОВИЕ СТАЛО", "accent": False, "size": "small"}, {"text": "НЕЧИТАЕМЫМ", "accent": True, "size": "small"}]},
    {"start": 9.72, "end": 11.88, "lines": [{"text": "И ОНА РЕШИЛА", "accent": False, "size": "small"}, {"text": "СОВСЕМ НЕ ТО", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 13.56, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.56, "end": 14.49, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 16.26, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЧИТАЕТСЯ ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 16.59, "end": 18.12, "lines": [{"text": "И НИКАКОЙ СОУС", "accent": False, "size": "small"}, {"text": "ЕМУ НЕ СТРАШЕН", "accent": True, "size": "big"}]},
    {"start": 18.66, "end": 19.71, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.71, "end": 20.546, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 7.20, "end": 7.62}, {"start": 8.70, "end": 9.39}, {"start": 17.60, "end": 18.12}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (teen boy on couch, 21.880s): "figure it out yourself" gets
# said a lot, but in an ЕГЭ task there's no telling which question to
# start analyzing from without a map -- what's given, what to find,
# what method; without it the reading starts from the middle and goes
# the wrong way; the app's text breakdown lays out exactly that order
# ---------------------------------------------------------------------------
d_intro = {"lines": ["РАЗБЕРИ САМ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.39, "lines": [{"text": "МНЕ ЧАСТО ГОВОРЯТ", "accent": False, "size": "small"}, {"text": "РАЗБЕРИ САМ", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 5.82, "lines": [{"text": "НО В ЗАДАНИИ ЕГЭ", "accent": False, "size": "small"}, {"text": "Я НЕ ЗНАЮ", "accent": True, "size": "big"}]},
    {"start": 6.12, "end": 7.56, "lines": [{"text": "С КАКОГО ВОПРОСА", "accent": False, "size": "small"}, {"text": "НАЧИНАТЬ", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 8.76, "lines": [{"text": "МНЕ НУЖНА", "accent": False, "size": "small"}, {"text": "КАРТА", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.78, "lines": [{"text": "СНАЧАЛА ЧТО", "accent": False, "size": "small"}, {"text": "ДАНО", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 11.07, "lines": [{"text": "ПОТОМ ЧТО", "accent": False, "size": "small"}, {"text": "ИСКАТЬ", "accent": True, "size": "big"}]},
    {"start": 11.07, "end": 13.02, "lines": [{"text": "ПОТОМ ЧЕМ", "accent": False, "size": "small"}, {"text": "БЕЗ НЕЕ", "accent": True, "size": "big"}]},
    {"start": 13.41, "end": 14.88, "lines": [{"text": "Я НАЧИНАЮ", "accent": False, "size": "small"}, {"text": "С СЕРЕДИНЫ", "accent": True, "size": "big"}]},
    {"start": 14.88, "end": 16.02, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.02, "end": 17.31, "lines": [{"text": "КОТОРЫЙ ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ЭТОТ ПОРЯДОК", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 19.80, "lines": [{"text": "ЧТО ДАНО ЧТО НАЙТИ", "accent": False, "size": "small"}, {"text": "И КАКИМ СПОСОБОМ", "accent": True, "size": "big"}]},
    {"start": 20.01, "end": 21.00, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 21.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.85, "end": 5.31}, {"start": 6.65, "end": 7.02}, {"start": 11.60, "end": 12.03}]
process("d", d_cards, d_intro, d_emphasis)
# NB: ASR merges "тренажере к" into "тренажерик" and mishears
# "текстовый" as "текстовая" here (see FIXES["d"]); card text above
# spells both correctly regardless.


# ---------------------------------------------------------------------------
# Episode E (teen boy on couch, 18.840s): a deskmate copies ЕГЭ answers
# at the last moment, then is baffled when nothing works on the
# practice test; decided to let him solve it himself and showed him
# where tasks are numbered -- he got through four that evening; the
# app's tasks are numbered too, start from anywhere
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СПИСАЛ В ПОСЛЕДНИЙ", "МОМЕНТ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.69, "lines": [{"text": "СОСЕД ПО ПАРТЕ", "accent": False, "size": "small"}, {"text": "СПИСЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 4.98, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "УДИВЛЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.84, "lines": [{"text": "ЧТО НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "У НЕГО НИЧЕГО", "accent": True, "size": "big"}]},
    {"start": 6.84, "end": 7.83, "lines": [{"text": "НЕ ВЫХОДИТ Я РЕШИЛ", "accent": False, "size": "small"}, {"text": "ЧТО ПУСТЬ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.06, "lines": [{"text": "РЕШАЕТ", "accent": False, "size": "small"}, {"text": "САМ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.59, "lines": [{"text": "И ПОКАЗАЛ ГДЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЛЕЖАТ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 12.18, "lines": [{"text": "ПО НОМЕРАМ ЗА ВЕЧЕР", "accent": False, "size": "small"}, {"text": "ОН РЕШИЛ ЧЕТЫРЕ", "accent": True, "size": "big"}]},
    {"start": 12.54, "end": 13.44, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.28, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.28, "end": 15.42, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЛЕЖАТ ПО НОМЕРАМ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.62, "lines": [{"text": "И НАЧАТЬ МОЖНО", "accent": False, "size": "small"}, {"text": "С ЛЮБОГО", "accent": True, "size": "big"}]},
    {"start": 16.92, "end": 17.97, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.97, "end": 18.840, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 4.30, "end": 4.98}, {"start": 7.05, "end": 7.38}, {"start": 11.85, "end": 12.18}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 20.098s): a daughter insists she explained the
# task solution; mom nodded along, understood nothing, but said she
# understood -- now it feels awkward, and the daughter thinks it all
# landed when it didn't; the app's text breakdown is something they
# can read together instead
# ---------------------------------------------------------------------------
f_intro = {"lines": ["КИВАЛА НО"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.24, "lines": [{"text": "ДОЧЬ УВЕРЯЕТ ЧТО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИЛА", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 5.19, "lines": [{"text": "А Я", "accent": False, "size": "small"}, {"text": "КИВАЛА", "accent": True, "size": "big"}]},
    {"start": 5.61, "end": 6.69, "lines": [{"text": "НО СКАЗАЛА ЧТО", "accent": False, "size": "small"}, {"text": "ПОНЯЛА", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 8.13, "lines": [{"text": "ТЕПЕРЬ МНЕ", "accent": False, "size": "small"}, {"text": "НЕЛОВКО", "accent": True, "size": "big"}]},
    {"start": 8.28, "end": 9.27, "lines": [{"text": "И ЕЙ НАВЕРНОЕ", "accent": False, "size": "small"}, {"text": "ТОЖЕ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.07, "lines": [{"text": "ОНА ДУМАЕТ ЧТО Я", "accent": False, "size": "small"}, {"text": "ВСЕ УСВОИЛА", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.42, "lines": [{"text": "А Я", "accent": False, "size": "small"}, {"text": "БОЮСЬ ПРИЗНАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 13.80, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 14.70, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.69, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.69, "end": 17.67, "lines": [{"text": "КОТОРЫЙ МЫ С ДОЧЕРЬЮ", "accent": False, "size": "small"}, {"text": "МОЖЕМ ПРОЧИТАТЬ ВМЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 18.12, "end": 19.20, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 7.65, "end": 8.13}, {"start": 10.50, "end": 11.07}, {"start": 16.75, "end": 17.22}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
