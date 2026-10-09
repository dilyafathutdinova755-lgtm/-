#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-EIGHTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes95/.

Three returning hosts, no new faces: "blonde in cream sweater" / desk
with lamp+plant+notebook room (a, c, d), "mother" / bookshelf+doorway
apartment with small framed picture (b, e, f).

Sub-themes: telling whether a word is truly "вводное" by ear alone
until it becomes automatic, a tutor's solution sheet that skips the
step from one formula line to the next, a phone timer that goes off
before task one is even read, a teacher's margin note "смотри условия"
that doesn't say which detail was missed, solving on a cramped
windowsill because the desk is taken by a younger sibling, and a slow
paper-based history quiz where the question is forgotten by the time
the page turns.
"""
import json

REAL_DURATION = {
    "a": 24.471, "b": 20.012, "c": 22.380,
    "d": 18.480, "e": 18.400, "f": 19.863,
}
SOURCE_FILE = {
    "a": "dgdgfdgdgdg", "b": "fgwgfgwffw", "c": "fsgdgdghdsg",
    "d": "gfdgdgfdgfdgg", "e": "ghgdssghgfdsr", "f": "hdgfffweff",
}
FIXES = {
    "a": {"водное": "вводное", "поторжественности": "торжественности"},
    "b": {"форму": "формул"},
    "c": {},
    "d": {},
    "e": {"илисты": "листы"},
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
    with open(f"../asr_coffee123_48/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blonde in cream sweater, 24.471s): can't tell by ear alone
# whether a word is a true "вводное слово" for the comma rule -- only
# repeating it to automatism settles it; the app's memory games drill
# exactly that kind of word set
# ---------------------------------------------------------------------------
a_intro = {"lines": ["НЕ ЗНАЕШЬ ГДЕ", "СТАВИТЬ ЗАПЯТУЮ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "ЗАПЯТУЮ ПРИ", "accent": False, "size": "small"}, {"text": "ВВОДНЫХ СЛОВАХ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.95, "lines": [{"text": "НА ЕГЭ ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "РЕШАЮ НА СЛУХ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 6.90, "lines": [{"text": "ЗВУЧИТ", "accent": False, "size": "small"}, {"text": "ТОРЖЕСТВЕННО", "accent": True, "size": "small"}]},
    {"start": 7.05, "end": 9.30, "lines": [{"text": "ВВОДНОЕ ЭТО", "accent": False, "size": "small"}, {"text": "ИЛИ НЕТ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 11.40, "lines": [{"text": "НА СЛУХ", "accent": False, "size": "small"}, {"text": "НЕ ОПРЕДЕЛИТЬ", "accent": True, "size": "big"}]},
    {"start": 11.55, "end": 13.10, "lines": [{"text": "ПРОВЕРКУ", "accent": False, "size": "small"}, {"text": "МОЖНО УБРАТЬ", "accent": True, "size": "big"}]},
    {"start": 13.25, "end": 15.05, "lines": [{"text": "ПОВТОРЯТЬ", "accent": False, "size": "small"}, {"text": "ДО АВТОМАТИЗМА", "accent": True, "size": "small"}]},
    {"start": 16.15, "end": 17.70, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 17.85, "end": 19.50, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.65, "end": 22.00, "lines": [{"text": "ГДЕ ТАКИЕ СЛОВА", "accent": False, "size": "small"}, {"text": "ИДУТ ОДИН ЗА ДРУГИМ", "accent": True, "size": "big"}]},
    {"start": 22.50, "end": 23.65, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.65, "end": 24.471, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.46, "end": 6.06}, {"start": 14.34, "end": 14.94}, {"start": 18.75, "end": 19.26}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 20.012s): a tutor's solution sheet has five lines
# of formulas but the step from one line to the next isn't written
# down, and asking feels awkward; the app's text breakdown spells out
# that exact step in words
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЛИСТОК С РЕШЕНИЕМ", "А ОБЪЯСНЕНИЯ НЕТ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДОЧЬ ПРИНЕСЛА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ПО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 4.80, "lines": [{"text": "ЛИСТОК С РЕШЕНИЕМ", "accent": False, "size": "small"}, {"text": "ОТ РЕПЕТИТОРА", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.00, "lines": [{"text": "Я НИЧЕГО", "accent": False, "size": "small"}, {"text": "НЕ ПОНЯЛА", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.50, "lines": [{"text": "ПЯТЬ СТРОК", "accent": False, "size": "small"}, {"text": "ФОРМУЛ", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 9.30, "lines": [{"text": "КАК ОДНА", "accent": False, "size": "small"}, {"text": "ПЕРЕХОДИТ В ДРУГУЮ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 10.65, "lines": [{"text": "НЕ НАПИСАНО", "accent": False, "size": "small"}, {"text": "И СПРОСИТЬ НЕЛОВКО", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.60, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 14.10, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 16.50, "lines": [{"text": "ГДЕ ПУТЬ ОТ СТРОКИ", "accent": False, "size": "small"}, {"text": "К СТРОКЕ ОБЪЯСНЕН", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 18.00, "lines": [{"text": "СЛОВАМИ", "accent": False, "size": "small"}, {"text": "И ТЕПЕРЬ ПОНЯТНО", "accent": True, "size": "big"}]},
    {"start": 18.15, "end": 19.20, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.012, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.74, "end": 5.13}, {"start": 6.66, "end": 6.87}, {"start": 8.76, "end": 9.30}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blonde in cream sweater, 22.380s): a twenty-minute phone
# timer goes off before task one is even read -- now easy tasks go
# first and the rest wait for a second pass; the app's FIPI bank lets
# several tasks be pulled in a row to train at that exact pace
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТАЙМЕР СРАБОТАЛ", "РАНЬШЕ ЧЕМ ДОЧИТАЛА"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ТАЙМЕР НА", "accent": False, "size": "small"}, {"text": "ДВАДЦАТЬ МИНУТ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 5.25, "lines": [{"text": "НА ПЕРВОМ ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ОН СРАБОТАЛ РАНЬШЕ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 7.95, "lines": [{"text": "ЧЕМ Я", "accent": False, "size": "small"}, {"text": "ДОЧИТАЛА УСЛОВИЯ", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 10.50, "lines": [{"text": "ТЕПЕРЬ РЕШАЮ", "accent": False, "size": "small"}, {"text": "СНАЧАЛА ТО ЧТО УМЕЮ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 12.90, "lines": [{"text": "ОСТАЛЬНОЕ", "accent": False, "size": "small"}, {"text": "НА ВТОРОЙ КРУГ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.55, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.90, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 18.00, "lines": [{"text": "ГДЕ МОЖНО ВЗЯТЬ", "accent": False, "size": "small"}, {"text": "НЕСКОЛЬКО ЗАДАНИЙ ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 18.15, "end": 19.80, "lines": [{"text": "И ТРЕНИРОВАТЬСЯ", "accent": False, "size": "small"}, {"text": "В ТАКОМ ТЕМПЕ", "accent": True, "size": "big"}]},
    {"start": 20.25, "end": 21.35, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.35, "end": 22.380, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.34, "end": 2.97}, {"start": 5.31, "end": 6.21}, {"start": 14.94, "end": 15.51}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blonde in cream sweater, 18.480s): a teacher's margin note
# "смотри условия" doesn't say which detail was actually missed, and
# asking feels embarrassing; the app's text breakdown points to the
# exact detail in the condition to check
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СМОТРИ УСЛОВИЯ", "А ЧТО ИМЕННО"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "УЧИТЕЛЬНИЦА ВЕРНУЛА", "accent": False, "size": "small"}, {"text": "РАБОТУ С ПОМЕТКОЙ", "accent": True, "size": "big"}]},
    {"start": 3.60, "end": 5.10, "lines": [{"text": "НА ПОЛЯХ", "accent": False, "size": "small"}, {"text": "СМОТРИ УСЛОВИЯ", "accent": True, "size": "big"}]},
    {"start": 5.25, "end": 6.90, "lines": [{"text": "ЧТО ИМЕННО", "accent": False, "size": "small"}, {"text": "В УСЛОВИЯ Я ПРОПУСТИЛА", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 8.25, "lines": [{"text": "ИЗ ПОМЕТКИ", "accent": False, "size": "small"}, {"text": "НЕ ПОНЯТЬ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.90, "lines": [{"text": "А СПРОСИТЬ", "accent": False, "size": "small"}, {"text": "Я ПОСТЕСНЯЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 10.80, "end": 11.70, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.90, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 15.00, "lines": [{"text": "ГДЕ УКАЗАНО", "accent": False, "size": "small"}, {"text": "НА КАКУЮ ДЕТАЛЬ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.35, "lines": [{"text": "УСЛОВИЯ", "accent": False, "size": "small"}, {"text": "СМОТРЕТЬ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.60, "end": 18.480, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.93, "end": 4.65}, {"start": 9.09, "end": 9.63}, {"start": 14.79, "end": 14.97}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (mother, 18.400s): the desk is taken by a younger brother,
# so a task gets solved on a narrow windowsill where the sheets keep
# falling and the second task gets given up on; the app's FIPI bank
# opens tasks on the phone so no sheets are needed there at all
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЛИСТЫ ПАДАЮТ", "С УЗКОГО ПОДОКОННИКА"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДОЧЬ РЕШАЕТ", "accent": False, "size": "small"}, {"text": "НА ПОДОКОННИКЕ", "accent": True, "size": "small"}]},
    {"start": 3.45, "end": 5.40, "lines": [{"text": "ЗА СТОЛОМ", "accent": False, "size": "small"}, {"text": "ОТВЛЕКАЕТ МЛАДШИЙ БРАТ", "accent": True, "size": "big"}]},
    {"start": 5.55, "end": 7.05, "lines": [{"text": "ПОДОКОННИК УЗКИЙ", "accent": False, "size": "small"}, {"text": "ЛИСТЫ ПАДАЮТ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.45, "lines": [{"text": "НА ВТОРОМ ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ОНА СДАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.40, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 11.55, "end": 13.20, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЮТСЯ НА ТЕЛЕФОНЕ", "accent": True, "size": "small"}]},
    {"start": 13.35, "end": 15.40, "lines": [{"text": "И ЛИСТЫ", "accent": False, "size": "small"}, {"text": "НА ПОДОКОННИКЕ НЕ НУЖНЫ", "accent": True, "size": "small"}]},
    {"start": 16.50, "end": 17.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.60, "end": 18.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.97, "end": 6.84}, {"start": 9.18, "end": 9.51}, {"start": 11.88, "end": 12.09}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 19.863s): quizzing from a paper sheet is slow
# enough that the question is forgotten before the page is turned, so
# review drags on longer than it should; the app's memory games run
# the same spaced quiz fast and without a parent reading questions out
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЧИТАЮ ВОПРОСЫ", "ПО БУМАЖКЕ МЕДЛЕННО"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДОЧЬ ПРОСИТ", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯТЬ ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 4.80, "lines": [{"text": "Я ЧИТАЮ", "accent": False, "size": "small"}, {"text": "ВОПРОСЫ ПО БУМАЖКЕ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.60, "lines": [{"text": "ТЕМП", "accent": False, "size": "small"}, {"text": "ПОЛУЧАЕТСЯ МЕДЛЕННЫМ", "accent": True, "size": "small"}]},
    {"start": 6.90, "end": 8.85, "lines": [{"text": "ОНА УСПЕВАЕТ", "accent": False, "size": "small"}, {"text": "ЗАБЫТЬ ВОПРОС", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "ПОКА Я", "accent": False, "size": "small"}, {"text": "ПЕРЕЛИСТЫВАЮ СТРАНИЦУ", "accent": True, "size": "small"}]},
    {"start": 10.35, "end": 12.15, "lines": [{"text": "ПОВТОРЕНИЕ", "accent": False, "size": "small"}, {"text": "ТЯНЕТСЯ ДОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 14.10, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 15.15, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.30, "end": 16.50, "lines": [{"text": "ГДЕ ВОПРОСЫ", "accent": False, "size": "small"}, {"text": "ИДУТ БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.80, "lines": [{"text": "БЕЗ МОЕГО", "accent": False, "size": "small"}, {"text": "УЧАСТИЯ", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 19.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.00, "end": 19.863, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.70, "end": 6.09}, {"start": 7.98, "end": 8.49}, {"start": 14.55, "end": 15.00}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
