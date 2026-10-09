#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-SEVENTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes94/.

Three returning hosts, no new faces: "blue-shirt brunette" / THE
SMITHS poster room (a, d, e), "Рома" / tight curls, black Under Armour
hoodie (b, h, i), "teen boy on couch" (c, f, g).

Sub-themes: a reform-and-ruler pairing that falls apart unless
reshuffled and repeated, legislative/executive branches swapping
places the moment an answer gets rushed, three classmates in a group
chat each sure of a different wrong answer, a one-minute solve
followed by thirty anxious minutes of checking without a plan, a
correct final answer reached by a completely different path than the
key, inflation explained with store prices when the exam wants precise
terms, a father's ten-variants-by-November deadline that swallows
three evenings once task types vary, an honest study-time count that
should be in tasks solved rather than hours half-spent on a phone, and
a three-line notebook solution versus a half-page textbook one with no
way to know which the exam actually wants.
"""
import json

REAL_DURATION = {
    "a": 20.908, "b": 17.800, "c": 16.343,
    "d": 21.676, "e": 18.480, "f": 19.202,
    "g": 19.202, "h": 18.562, "i": 18.604,
}
SOURCE_FILE = {
    "a": "gfdgdsgsfdgdtfdgbfd", "b": "gfhhgngffxhnxfnjhgth", "c": "ghdfjgdnghrhnrsdgh",
    "d": "ghjhjdfjhsdfhshsh", "e": "gjfjrshgnfbvgfhfyhh", "f": "gxjhfkmxgfhjfhnx",
    "g": "jfdjnxhjhjnxfghngxfhf", "h": "ngffxxnxnhbxnxfj", "i": "nxfnxfnfn.xfng",
}
FIXES = {
    "a": {"нажере": "тренажере"},
    "b": {"законодательное": "законодательная"},
    "c": {"поподробному": "подробному", "профия": "профиля"},
    "d": {"бесплана": "плана", "фи": "фипи"},
    "e": {"о": "а", "заданием": "заданиям"},
    "f": {"определение": "определения"},
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
    with open(f"../asr_coffee123_47/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blue-shirt brunette, 20.908s): can name a history reform
# but not which ruler it happened under -- the reform-ruler link holds
# poorly until repeated several times in shuffled order; the app's
# memory games make reforms and rulers get matched against each other
# ---------------------------------------------------------------------------
a_intro = {"lines": ["РЕФОРМА И ПРАВИТЕЛЬ", "СВЯЗКА ДЕРЖИТСЯ ПЛОХО?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 2.73, "lines": [{"text": "РЕФОРМУ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "НАЗВАТЬ МОГУ", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 4.92, "lines": [{"text": "А ПРИ КАКОМ", "accent": False, "size": "small"}, {"text": "ПРАВИТЕЛЕ ПУТАЮ", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 7.08, "lines": [{"text": "СВЯЗКА", "accent": False, "size": "small"}, {"text": "ПРАВИТЕЛЬ РЕФОРМА", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 8.64, "lines": [{"text": "ДЕРЖИТСЯ", "accent": False, "size": "small"}, {"text": "ПЛОХО", "accent": True, "size": "big"}]},
    {"start": 8.88, "end": 11.85, "lines": [{"text": "ПОКА НЕ ПОВТОРИТЬ", "accent": False, "size": "small"}, {"text": "В РАЗНОМ ПОРЯДКЕ", "accent": True, "size": "big"}]},
    {"start": 13.08, "end": 14.37, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 15.90, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.20, "end": 18.57, "lines": [{"text": "ГДЕ РЕФОРМЫ И", "accent": False, "size": "small"}, {"text": "ПРАВИТЕЛЕЙ СОПОСТАВЛЯЮТ", "accent": True, "size": "small"}]},
    {"start": 19.17, "end": 20.05, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.05, "end": 20.908, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.25, "end": 5.49}, {"start": 7.92, "end": 8.28}, {"start": 16.47, "end": 16.83}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 17.800s): can name the branches of power for the
# social-studies EGE but mixes up which does what -- legislative and
# executive swap places the moment the answer gets rushed; the app's
# memory games link each branch to its actual function
# ---------------------------------------------------------------------------
b_intro = {"lines": ["КТО ЧТО ДЕЛАЕТ", "ПУТАЕШЬ ПОД ДАВЛЕНИЕМ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ВЕТВИ ВЛАСТИ", "accent": False, "size": "small"}, {"text": "НАЗВАТЬ МОГУ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.68, "lines": [{"text": "А КТО ЧТО", "accent": False, "size": "small"}, {"text": "ДЕЛАЕТ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 7.50, "lines": [{"text": "ПЕРЕПУТЫВАЮ", "accent": False, "size": "small"}, {"text": "ЗАКОНОДАТЕЛЬНУЮ", "accent": True, "size": "small"}]},
    {"start": 7.59, "end": 10.23, "lines": [{"text": "МЕНЯЮТСЯ МЕСТАМИ", "accent": False, "size": "small"}, {"text": "ЕСЛИ ПОТОРОПИТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 10.56, "end": 12.06, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 12.33, "end": 13.38, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.59, "end": 15.57, "lines": [{"text": "ГДЕ ВЕТВИ ВЛАСТИ", "accent": False, "size": "small"}, {"text": "СВЯЗАНЫ С ФУНКЦИЯМИ", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 16.90, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.90, "end": 17.800, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.98, "end": 5.43}, {"start": 9.78, "end": 10.23}, {"start": 14.52, "end": 14.94}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (teen boy on couch, 16.343s): three classmates in a group
# chat each get a different EGE answer and each is sure they're right
# -- only a detailed solution reveals who actually erred; the app's
# text breakdown settles such disputes without needing a teacher
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТРОЕ ПОЛУЧИЛИ", "ТРИ РАЗНЫХ ЧИСЛА?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 2.97, "lines": [{"text": "СВЕРИЛ ОТВЕТЫ", "accent": False, "size": "small"}, {"text": "В ЧАТЕ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.80, "lines": [{"text": "ТРОЕ ПОЛУЧИЛИ", "accent": False, "size": "small"}, {"text": "ТРИ РАЗНЫХ ЧИСЛА", "accent": True, "size": "big"}]},
    {"start": 5.13, "end": 6.75, "lines": [{"text": "КАЖДЫЙ УВЕРЕН", "accent": False, "size": "small"}, {"text": "ЧТО ПРАВ", "accent": True, "size": "big"}]},
    {"start": 6.87, "end": 9.18, "lines": [{"text": "ВЫЯСНИТЬ КТО ОШИБСЯ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ПО РЕШЕНИЮ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 10.68, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 10.86, "end": 11.70, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 14.22, "lines": [{"text": "ПО КОТОРОМУ", "accent": False, "size": "small"}, {"text": "РЕШИТЬ СПОР БЕЗ УЧИТЕЛЯ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.45, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 16.343, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.26, "end": 4.80}, {"start": 7.11, "end": 7.35}, {"start": 12.69, "end": 12.90}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 21.676s): a bank task gets solved in
# a minute, then rechecked for half an hour without a plan -- that
# turns into anxiety, rereading the same thing, not knowing where to
# look; the app's FIPI bank shows right after the answer whether it's
# correct
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПОЛЧАСА ПРОВЕРЯЛА", "ОДНУ МИНУТНУЮ ЗАДАЧУ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "ЗАДАНИЕ ИЗ БАНКА", "accent": False, "size": "small"}, {"text": "РЕШИЛА ЗА МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 6.18, "lines": [{"text": "А ПОТОМ ПОЛЧАСА", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯЛА НЕ ОШИБЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 9.12, "lines": [{"text": "ПРОВЕРКА БЕЗ ПЛАНА", "accent": False, "size": "small"}, {"text": "ПРЕВРАЩАЕТСЯ В ТРЕВОГУ", "accent": True, "size": "small"}]},
    {"start": 9.78, "end": 11.97, "lines": [{"text": "ПЕРЕЧИТЫВАЮ", "accent": False, "size": "small"}, {"text": "ОДНО И ТО ЖЕ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.23, "lines": [{"text": "И НЕ ЗНАЮ", "accent": False, "size": "small"}, {"text": "ГДЕ ИСКАТЬ ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 14.16, "end": 14.97, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 15.99, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 19.05, "lines": [{"text": "ГДЕ ПОСЛЕ ОТВЕТА", "accent": False, "size": "small"}, {"text": "СРАЗУ ВИДНО РЕШЕНО ЛИ", "accent": True, "size": "big"}]},
    {"start": 19.80, "end": 20.80, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.80, "end": 21.676, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.70, "end": 6.18}, {"start": 8.07, "end": 8.58}, {"start": 18.30, "end": 18.63}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 18.480s): a final answer matched the
# key but the solution path was completely different -- unsure if it
# would count and no one to ask in the moment; the app's text
# breakdown lets a path be compared against the given one
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОТВЕТ СОВПАЛ", "НО ХОД СОВСЕМ ДРУГОЙ?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ОТВЕТ ПО ЗАДАНИЮ", "accent": False, "size": "small"}, {"text": "СОВПАЛ С КЛЮЧОМ", "accent": True, "size": "big"}]},
    {"start": 3.60, "end": 5.55, "lines": [{"text": "А ХОД РЕШЕНИЯ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛСЯ ДРУГИМ", "accent": True, "size": "big"}]},
    {"start": 6.18, "end": 7.56, "lines": [{"text": "НЕ ЗНАЮ", "accent": False, "size": "small"}, {"text": "ЗАСЧИТАЕТ ЛИ ТАКОЙ", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.81, "lines": [{"text": "ХОД И СПРОСИТЬ", "accent": False, "size": "small"}, {"text": "В ЭТОТ МОМЕНТ НЕКОГО", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 12.39, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.53, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 15.90, "lines": [{"text": "С КОТОРЫМ МОЖНО", "accent": False, "size": "small"}, {"text": "СРАВНИТЬ СВОЙ ХОД", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.55, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 18.480, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.25, "end": 2.49}, {"start": 5.28, "end": 5.55}, {"start": 8.25, "end": 8.58}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 19.202s): inflation explained with
# store prices is clear, but the exam wants precise terms -- rising
# general price levels, falling purchasing power; the app's memory
# games repeat definitions in short form
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ОБЪЯСНЯЮ НА ЦЕНАХ", "НО ЭКЗАМЕН ХОЧЕТ СЛОВА?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.88, "lines": [{"text": "ЧТО ТАКОЕ", "accent": False, "size": "small"}, {"text": "ИНФЛЯЦИЯ", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 4.32, "lines": [{"text": "ОБЪЯСНЯЮ", "accent": False, "size": "small"}, {"text": "НА ЦЕНАХ В МАГАЗИНЕ", "accent": True, "size": "big"}]},
    {"start": 4.59, "end": 5.82, "lines": [{"text": "НО В ТЕСТЕ", "accent": False, "size": "small"}, {"text": "НУЖНЫ ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 6.03, "end": 7.38, "lines": [{"text": "БЫТОВОЕ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЕНИЕ ПОНЯТНОЕ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.37, "lines": [{"text": "А ЭКЗАМЕН", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯЕТ СЛОВА", "accent": True, "size": "big"}]},
    {"start": 8.61, "end": 10.26, "lines": [{"text": "РОСТ ОБЩЕГО", "accent": False, "size": "small"}, {"text": "УРОВНЯ ЦЕН", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 12.06, "lines": [{"text": "СНИЖЕНИЕ", "accent": False, "size": "small"}, {"text": "ПОКУПАТЕЛЬНОЙ СПОСОБНОСТИ", "accent": True, "size": "small"}]},
    {"start": 12.39, "end": 13.92, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 14.16, "end": 15.27, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.42, "end": 17.16, "lines": [{"text": "ГДЕ ОПРЕДЕЛЕНИЯ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ КОРОТКО", "accent": True, "size": "small"}]},
    {"start": 17.43, "end": 18.35, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.35, "end": 19.202, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.05, "end": 1.47}, {"start": 9.09, "end": 9.60}, {"start": 16.26, "end": 16.68}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (teen boy on couch, 19.202s): a father's deadline of ten
# EGE variants by November sounds like one easy variant a week -- until
# mixed task types stretch it into three evenings; the app's FIPI bank
# lets tasks be taken by type, closing one type per evening
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ОДИН ВАРИАНТ", "РАСТЯГИВАЕТСЯ НА ТРИ ВЕЧЕРА?"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.45, "lines": [{"text": "ОТЕЦ ДАЛ СРОК", "accent": False, "size": "small"}, {"text": "ДЕСЯТЬ ВАРИАНТОВ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 5.70, "lines": [{"text": "Я ПОСЧИТАЛ", "accent": False, "size": "small"}, {"text": "ПО ОДНОМУ В НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.65, "lines": [{"text": "ОДИН ВАРИАНТ", "accent": False, "size": "small"}, {"text": "ЗВУЧИТ ЛЕГКО", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.63, "lines": [{"text": "НО В НЕМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ РАЗНЫХ ТИПОВ", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 11.40, "lines": [{"text": "И ОН РАСТЯГИВАЕТСЯ", "accent": False, "size": "small"}, {"text": "НА ТРИ ВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 13.56, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.74, "end": 15.24, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "МОЖНО БРАТЬ ПО ТИПАМ", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 16.92, "lines": [{"text": "И ЗАКРЫВАТЬ", "accent": False, "size": "small"}, {"text": "ОДИН ТИП ЗА ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 17.25, "end": 18.27, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.27, "end": 19.202, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.79, "end": 3.45}, {"start": 10.14, "end": 10.74}, {"start": 15.57, "end": 15.90}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (Рома, 18.562s): asked how long he studied yesterday, he
# answers "about two hours" though half of it went to his phone -- an
# honest count would be in tasks solved, not hours spent; the app's
# FIPI bank measures by tasks actually solved
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ЧЕСТНЫЙ СЧЕТ", "В ЗАДАНИЯХ А НЕ В ЧАСАХ?"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.51, "lines": [{"text": "БРАТ СПРОСИЛ", "accent": False, "size": "small"}, {"text": "СКОЛЬКО Я ЗАНИМАЛСЯ", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 6.03, "lines": [{"text": "ОТВЕТИЛ", "accent": False, "size": "small"}, {"text": "ЧАСА ДВА", "accent": True, "size": "big"}]},
    {"start": 6.63, "end": 9.03, "lines": [{"text": "ЧЕСТНЫЙ СЧЕТ", "accent": False, "size": "small"}, {"text": "В ЗАДАНИЯХ А НЕ В ЧАСАХ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 11.22, "lines": [{"text": "СКОЛЬКО РЕШЕНО", "accent": False, "size": "small"}, {"text": "СТОЛЬКО СДЕЛАНО", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 13.38, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 16.17, "lines": [{"text": "ГДЕ РЕЗУЛЬТАТ", "accent": False, "size": "small"}, {"text": "ИЗМЕРЯЕТСЯ ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 16.62, "end": 17.62, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.62, "end": 18.562, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 4.11, "end": 4.47}, {"start": 9.42, "end": 9.66}, {"start": 14.70, "end": 15.09}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (Рома, 18.604s): a textbook solution takes half a page, his
# own notebook takes three lines, and there's no way to know which the
# exam actually wants -- fear of losing points for skipped steps; the
# app's text breakdown shows exactly how many steps need to be written
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ТРИ СТРОКИ", "ИЛИ ПОЛНЫЙ ХОД?"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 5.01, "lines": [{"text": "В УЧЕБНИКЕ", "accent": False, "size": "small"}, {"text": "ПОЛСТРАНИЦЫ", "accent": True, "size": "small"}]},
    {"start": 5.34, "end": 6.18, "lines": [{"text": "НЕ ЗНАЮ", "accent": False, "size": "small"}, {"text": "ЧЬЕ ЛУЧШЕ", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 7.65, "lines": [{"text": "ТРИ СТРОКИ", "accent": False, "size": "small"}, {"text": "БЫСТРЕЕ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 10.29, "lines": [{"text": "НО БОЮСЬ ЧТО", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕН ПОТРЕБУЕТ ХОД", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 11.91, "lines": [{"text": "И ПОТЕРЯЮ БАЛЛЫ", "accent": False, "size": "small"}, {"text": "ЗА ПРОПУСКИ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.41, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 14.46, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.61, "end": 16.53, "lines": [{"text": "ГДЕ ВИДНО", "accent": False, "size": "small"}, {"text": "СКОЛЬКО ШАГОВ ЗАПИСАТЬ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 17.76, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.76, "end": 18.604, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 4.77, "end": 5.01}, {"start": 8.22, "end": 8.40}, {"start": 10.77, "end": 11.04}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
