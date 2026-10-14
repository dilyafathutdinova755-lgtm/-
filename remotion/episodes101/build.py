#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-FOURTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes101/.

Three returning hosts, no new faces: "teen boy on couch" / bookshelf+
plant+window room (a, b), "Рома" / black Under Armour hoodie (c, e, f),
"mother" / bookshelf+doorway apartment with small framed picture (d).

Sub-themes: ordering Petrine-era events that come out like a garland
with half its bulbs burnt out, an olympiad method that agrees with the
exam answer but not certainly with the exam's expected method, a
table-reading habit (by row, not by column) that has to be unlearned on
purpose, a parent who can check an answer but not the steps that got
there, two hours spent hunting the perfect study spot instead of
starting, and a cheat-sheet thought experiment that reveals diagrams
stick but the exam still needs the words.
"""
import json

REAL_DURATION = {
    "a": 19.47, "b": 16.47, "c": 16.14,
    "d": 20.28, "e": 16.35, "f": 17.67,
}
SOURCE_FILE = {
    "a": "dbhsdgvsfdsfsd", "b": "fdbsbsvdffv", "c": "fdcnbfsdcsfsdvf",
    "d": "fsdfdsfgdsfdsf", "e": "gdsfgffsfsdf", "f": "sdhgsfdsfdsfsd",
}
FIXES = {
    "a": {"гирлянды": "гирлянда"},
    "b": {},
    "c": {},
    "d": {"опроверка": "проверка", "тренажери": "тренажере"},
    "e": {},
    "f": {"запоминается": "запоминаются"},
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
    with open(f"../asr_coffee123_54/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy on couch, 19.47s): ordering Petrine-era events
# comes out like a garland with half its bulbs burnt out -- only
# repetition finds which ones are dark; the app's history games drill
# exactly that ordering
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПОЛОВИНА СОБЫТИЙ", "ПЕРЕГОРЕЛА В ПАМЯТИ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "СОБЫТИЯ ПЕТРОВСКОЙ", "accent": False, "size": "small"}, {"text": "ЭПОХИ ПО ПОРЯДКУ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ПОЛУЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "ГИРЛЯНДА", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "С ПЕРЕГОРЕВШИМИ", "accent": False, "size": "small"}, {"text": "ЛАМПОЧКАМИ", "accent": True, "size": "small"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "ЧАСТЬ ГОРИТ", "accent": False, "size": "small"}, {"text": "ЧАСТЬ НЕТ", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "НАЙТИ ИХ", "accent": False, "size": "small"}, {"text": "МОЖНО ПОВТОРЕНИЕМ", "accent": True, "size": "small"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "СОБЫТИЯ", "accent": False, "size": "small"}, {"text": "РАССТАВЛЯЮТСЯ ПО ПОРЯДКУ", "accent": True, "size": "small"}]},
    {"start": 16.20, "end": 17.80, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 19.47, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.53, "end": 5.37}, {"start": 7.05, "end": 8.88}, {"start": 10.95, "end": 11.46}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (teen boy on couch, 16.47s): two different methods landing
# on the same answer doesn't settle which one the exam actually expects
# -- the app's text breakdown shows the accepted method directly
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ДВА СПОСОБА", "ОДИН ОТВЕТ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "НА ОЛИМПИАДЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ КАК НА ЕГЭ", "accent": True, "size": "small"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "РЕШИЛ", "accent": False, "size": "small"}, {"text": "ДРУГИМ СПОСОБОМ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "ДВА СПОСОБА", "accent": False, "size": "small"}, {"text": "ОДИН ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 6.40, "end": 8.00, "lines": [{"text": "НО КАКОЙ БЛИЖЕ", "accent": False, "size": "small"}, {"text": "К ЭКЗАМЕНУ", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "Я НЕ", "accent": False, "size": "small"}, {"text": "ПОНИМАЮ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.80, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.40, "lines": [{"text": "ГДЕ ПОКАЗАНО", "accent": False, "size": "small"}, {"text": "ПРИНЯТЫЙ СПОСОБ", "accent": True, "size": "small"}]},
    {"start": 14.40, "end": 15.40, "lines": [{"text": "ССЫЛКА НА ИГО", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 16.47, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.46, "end": 6.99}, {"start": 9.06, "end": 9.42}, {"start": 13.56, "end": 14.40}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 16.14s): a table read by rows instead of columns is a
# school habit that has to be unlearned on purpose -- the app's text
# breakdown shows the right way to read it
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЧИТАЮ ТАБЛИЦУ", "НЕ ТАК КАК НАДО"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "С ТАБЛИЦЕЙ", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "РЕШАЮ", "accent": False, "size": "small"}, {"text": "НЕВЕРНО", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "ЧИТАЮ ПО СТРОКАМ", "accent": False, "size": "small"}, {"text": "А НУЖНО ПО СТОЛБЦАМ", "accent": True, "size": "small"}]},
    {"start": 6.40, "end": 8.00, "lines": [{"text": "ПРИВЫЧКА", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЕНА ШКОЛОЙ", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "МЕНЯТЬ ЕЕ", "accent": False, "size": "small"}, {"text": "НАДО ОСОЗНАННО", "accent": True, "size": "small"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.80, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.30, "lines": [{"text": "ГДЕ ПОКАЗАНО", "accent": False, "size": "small"}, {"text": "КАК ЧИТАТЬ ТАБЛИЦУ", "accent": True, "size": "small"}]},
    {"start": 14.30, "end": 15.30, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.14, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.95, "end": 2.58}, {"start": 4.71, "end": 5.67}, {"start": 7.17, "end": 9.72}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 20.28s): checking a child's solution for an answer
# is easy, checking whether the steps that got there make sense is not
# -- the app's text breakdown lets the process be checked step by step
# ---------------------------------------------------------------------------
d_intro = {"lines": ["МОГУ СВЕРИТЬ ОТВЕТ", "НЕ МОГУ ОЦЕНИТЬ ШАГИ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "РЕШЕНИЕ ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "ДОЧЬ ПРОТЯГИВАЕТ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "СМОТРЮ НА ЛИСТОК", "accent": False, "size": "small"}, {"text": "И НЕ ЗНАЮ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ЧТО ИМЕННО", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ОТВЕТ МОГУ", "accent": False, "size": "small"}, {"text": "СВЕРИТЬ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "НО ШАГИ", "accent": False, "size": "small"}, {"text": "ОЦЕНИТЬ НЕ МОГУ", "accent": True, "size": "small"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "НУЖНА ПРОВЕРКА", "accent": False, "size": "small"}, {"text": "НЕ ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "А", "accent": False, "size": "small"}, {"text": "ХОДА", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.40, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.00, "lines": [{"text": "ХОД МОЖНО", "accent": False, "size": "small"}, {"text": "ПРОВЕРИТЬ ШАГ ЗА ШАГОМ", "accent": True, "size": "small"}]},
    {"start": 18.00, "end": 19.20, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.28, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.34, "end": 6.42}, {"start": 8.88, "end": 9.96}, {"start": 12.30, "end": 12.66}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 16.35s): two hours spent hunting the perfect study
# spot solved nothing -- starting does, not the place; the app opens
# tasks from the FIPI bank wherever a task is started
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ИСКАЛ ИДЕАЛЬНОЕ МЕСТО", "РЕШИЛ НОЛЬ ЗАДАНИЙ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "ДВА ЧАСА", "accent": False, "size": "small"}, {"text": "ИСКАЛ МЕСТО", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "ДЛЯ ЗАНЯТИЙ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "И НЕ РЕШИЛ", "accent": False, "size": "small"}, {"text": "НИ ОДНОГО ЗАДАНИЯ", "accent": True, "size": "small"}]},
    {"start": 6.40, "end": 8.00, "lines": [{"text": "МЕСТО НЕ РЕШАЕТ", "accent": False, "size": "small"}, {"text": "РЕШАЕТ НАЧАЛО", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "ТЕПЕРЬ ОТКРЫВАЮ", "accent": False, "size": "small"}, {"text": "ТАМ ГДЕ СИЖУ", "accent": True, "size": "small"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.80, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.40, "lines": [{"text": "ЗАДАНИЕ ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТАМ ГДЕ ТЫ", "accent": True, "size": "small"}]},
    {"start": 14.40, "end": 15.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 16.35, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.41, "end": 1.65}, {"start": 4.11, "end": 5.55}, {"start": 6.78, "end": 7.68}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 17.67s): diagrams stick in memory better than words,
# but the exam itself needs words -- the app's memory games keep the
# diagram and the term together instead of making a choice between them
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РИСОВАЛ БЫ СХЕМЫ", "А НЕ ТЕРМИНЫ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ЕСЛИ БЫ РАЗРЕШАЛИ", "accent": False, "size": "small"}, {"text": "ШПАРГАЛКИ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "Я БЫ РИСОВАЛ", "accent": False, "size": "small"}, {"text": "СХЕМЫ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НЕ ПИСАЛ", "accent": False, "size": "small"}, {"text": "ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "СХЕМЫ", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЮТСЯ ЛУЧШЕ", "accent": True, "size": "small"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "НО В ТЕСТЕ", "accent": False, "size": "small"}, {"text": "НУЖНЫ СЛОВА", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "НУЖНЫ ОБА", "accent": False, "size": "small"}, {"text": "РИСУНОК И ТЕРМИН", "accent": True, "size": "small"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.60, "end": 16.00, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.00, "end": 17.67, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.28, "end": 3.18}, {"start": 5.04, "end": 7.20}, {"start": 9.06, "end": 10.53}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
