#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-NINTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes106/.

Four returning hosts, no new faces: "blue-shirt brunette" / THE SMITHS
poster + "ЕГЭ 2026" sticky note room (a), "teen boy on couch" /
bookshelf+plant+window room (b, g, h), "mother" / bookshelf+doorway
apartment with small framed picture (c, d), "Рома" / black Under Armour
hoodie (e, f, i).

Sub-themes: a friend's simile of a task breakdown as a metro map -- a map
without a "you are here" mark is useless, so look for the step where you
went off-route; skipping to start/end of long breakdowns like a detective
story, when the middle holds the key steps; a map of Russia on the wall
gaining a pin for every closed exam topic; an argument over noun gender
(тюль, шампунь, рояль) that should end in the right answer, not more
arguing; "the annexation of Siberia" meaning only "Yermak" until years and
outcomes get added; the "if it didn't work out" block in a breakdown as a
backup exit nobody needs until they do; comparing presidential and
parliamentary republics to two buses going the same direction, differing
on one precise fact; choosing between a yard volleyball game and one more
exam task; and a promised bicycle turning the exam goal into a measurable
number of tasks per wheel.

Card/intro text was verified against the actual Golos Text Black render
(PIL getbbox at each line's real font size) before being written below --
every line here fits the 920px available width, including small/non-accent
lines, which batch 58 showed can also overflow when long enough.
"""
import json

REAL_DURATION = {
    "a": 23.49, "b": 18.84, "c": 17.52,
    "d": 19.82, "e": 16.258, "f": 17.218,
    "g": 20.46, "h": 14.423, "i": 16.791,
}
SOURCE_FILE = {
    "a": "dhsghbdsfgsfsf", "b": "dsggbdgrfedf", "c": "fdffsfsfsd",
    "d": "fdshsvgsffasfsd", "e": "gdsvdsgdfsfdsfs", "f": "ghgarfagfad",
    "g": "gsfgvdsbsdhgf", "h": "hshsbvgdfsfds", "i": "sgbhshadgf",
}
FIXES = {
    "a": {},
    "b": {"всередину": "середину", "тренажерик": "тренажере"},
    "c": {"обрастают": "обрастает"},
    "d": {},
    "e": {},
    "f": {"тренажери": "тренажере", "заданием": "заданиям"},
    "g": {},
    "h": {},
    "i": {},
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
    with open(f"../asr_coffee123_59/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (blue-shirt brunette, 23.49s): a friend's simile -- a task
# breakdown is a metro map, useless without a "you are here" mark -- the
# app's text breakdown lets you find the exact step you went off-route
# ---------------------------------------------------------------------------
a_intro = {"lines": ["РАЗБОР КАК", "КАРТА МЕТРО"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "ПОДРУГА СРАВНИЛА", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.60, "lines": [{"text": "ЗАДАНИЯ ЕГЭ С КАРТОЙ", "accent": False, "size": "small"}, {"text": "МЕТРО", "accent": True, "size": "big"}]},
    {"start": 4.60, "end": 5.80, "lines": [{"text": "НУЖНО ЗНАТЬ", "accent": False, "size": "small"}, {"text": "ГДЕ ТЫ", "accent": True, "size": "big"}]},
    {"start": 5.80, "end": 7.00, "lines": [{"text": "И КУДА", "accent": False, "size": "small"}, {"text": "НАДО", "accent": True, "size": "big"}]},
    {"start": 7.00, "end": 8.40, "lines": [{"text": "КАРТА БЕЗ", "accent": False, "size": "small"}, {"text": "ОТМЕТКИ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.80, "lines": [{"text": "ВЫ ЗДЕСЬ", "accent": False, "size": "small"}, {"text": "БЕСПОЛЕЗНА", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "ПОЭТОМУ В РАЗБОРЕ Я ИЩУ", "accent": False, "size": "small"}, {"text": "ШАГ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.20, "lines": [{"text": "НА КОТОРОМ САМА СОШЛА С", "accent": False, "size": "small"}, {"text": "МАРШРУТА", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.40, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.00, "lines": [{"text": "ГДЕ МОЖНО НАЙТИ", "accent": False, "size": "small"}, {"text": "ШАГ", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 19.80, "lines": [{"text": "НА КОТОРОМ ТЫ СОШЕЛ С", "accent": False, "size": "small"}, {"text": "МАРШРУТА", "accent": True, "size": "big"}]},
    {"start": 19.80, "end": 21.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.40, "end": 23.49, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 9.00, "end": 9.51}, {"start": 12.75, "end": 13.95}, {"start": 19.92, "end": 20.94}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (teen boy on couch, 18.84s): skipping to the start and end of
# long task breakdowns like a detective story, when the middle holds the
# key steps -- the app's text breakdown splits long ones into parts so
# the middle doesn't get lost
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЧИТАЮ ТОЛЬКО", "НАЧАЛО И КОНЕЦ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "В СЕРЕДИНУ ДЛИННЫХ", "accent": False, "size": "small"}, {"text": "РАЗБОРОВ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "ЗАДАНИЙ ЕГЭ Я", "accent": False, "size": "small"}, {"text": "ПРОПУСКАЮ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.40, "lines": [{"text": "ЧИТАЮ НАЧАЛО И", "accent": False, "size": "small"}, {"text": "КОНЕЦ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.60, "lines": [{"text": "КАК В", "accent": False, "size": "small"}, {"text": "ДЕТЕКТИВАХ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 7.80, "lines": [{"text": "В ДЕТЕКТИВЕ СЕРЕДИНУ", "accent": False, "size": "small"}, {"text": "ПРОПУСКАТЬ", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.00, "lines": [{"text": "НЕЛЬЗЯ И В РАЗБОРЕ", "accent": False, "size": "small"}, {"text": "ТОЖЕ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "ТАМ САМЫЕ НУЖНЫЕ", "accent": False, "size": "small"}, {"text": "ШАГИ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.40, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.60, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.80, "lines": [{"text": "ГДЕ ДЛИННЫЙ РАЗБОР", "accent": False, "size": "small"}, {"text": "ПОДЕЛЕН", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.00, "lines": [{"text": "НА ЧАСТИ И", "accent": False, "size": "small"}, {"text": "СЕРЕДИНА", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.20, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ТЕРЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.84, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.03, "end": 7.86}, {"start": 9.33, "end": 10.50}, {"start": 15.54, "end": 16.62}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 17.52s): a map of Russia on the wall gains a pin for
# every ЕГЭ topic closed -- the app's FIPI bank lets closed topics be
# marked right after finishing tasks, same visible growth
# ---------------------------------------------------------------------------
c_intro = {"lines": ["КАРТА", "ОБРАСТАЕТ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ДОЧЬ ПОВЕСИЛА", "accent": False, "size": "small"}, {"text": "КАРТУ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "НАД СТОЛОМ", "accent": False, "size": "small"}, {"text": "РОССИИ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.40, "lines": [{"text": "ОТМЕЧАЕТ БУЛАВКОЙ КАЖДУЮ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.60, "lines": [{"text": "ЕГЭ КОТОРУЮ", "accent": False, "size": "small"}, {"text": "ЗАКРЫЛА", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 7.80, "lines": [{"text": "КАРТА", "accent": False, "size": "small"}, {"text": "ОБРАСТАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.00, "lines": [{"text": "БУЛАВКАМИ И Я ВИЖУ", "accent": False, "size": "small"}, {"text": "КАК РАСТЕТ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "ЕЕ", "accent": False, "size": "small"}, {"text": "УВЕРЕННОСТЬ", "accent": True, "size": "small"}]},
    {"start": 10.20, "end": 11.40, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.60, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.80, "lines": [{"text": "ГДЕ ЗАКРЫТЫЕ ТЕМЫ МОЖНО", "accent": False, "size": "small"}, {"text": "ОТМЕЧАТЬ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.00, "lines": [{"text": "СРАЗУ ПО ИТОГАМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.20, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.52, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 6.69, "end": 9.69}, {"start": 13.62, "end": 13.92}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 19.82s): an argument over noun gender (тюль,
# шампунь, рояль) for Russian ЕГЭ should end in the right answer, which
# sticks through repetition -- the app's games repeat noun gender in
# short rounds
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СПОРИМ КАКОЙ", "РОД У ТЮЛЯ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ДОЧЬ СПОРИТ", "accent": False, "size": "small"}, {"text": "КАКОГО РОДА", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.10, "lines": [{"text": "СЛОВА", "accent": False, "size": "small"}, {"text": "ТЮЛЬ", "accent": True, "size": "big"}]},
    {"start": 4.10, "end": 5.20, "lines": [{"text": "ШАМПУНЬ И", "accent": False, "size": "small"}, {"text": "РОЯЛЬ", "accent": True, "size": "big"}]},
    {"start": 5.20, "end": 6.40, "lines": [{"text": "И ДЛЯ ЕГЭ ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ТАКОЙ СПОР", "accent": True, "size": "big"}]},
    {"start": 6.40, "end": 7.50, "lines": [{"text": "ДОЛЖЕН", "accent": False, "size": "small"}, {"text": "ЗАКАНЧИВАТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 7.50, "end": 8.60, "lines": [{"text": "ВЕРНЫМ", "accent": False, "size": "small"}, {"text": "ОТВЕТОМ", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 9.80, "lines": [{"text": "ВЕРНЫЙ ОТВЕТ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 9.80, "end": 11.00, "lines": [{"text": "ПОВТОРЕНИЕМ", "accent": False, "size": "small"}, {"text": "А НЕ СПОРОМ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 12.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.40, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.40, "end": 14.60, "lines": [{"text": "НА ЗАПОМИНАНИЕ ГДЕ", "accent": False, "size": "small"}, {"text": "РОД", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 15.80, "lines": [{"text": "ТАКИХ", "accent": False, "size": "small"}, {"text": "СУЩЕСТВИТЕЛЬНЫХ", "accent": True, "size": "small"}]},
    {"start": 15.80, "end": 17.00, "lines": [{"text": "ПОВТОРЯЕТСЯ КОРОТКИМИ", "accent": False, "size": "small"}, {"text": "РАУНДАМИ", "accent": True, "size": "big"}]},
    {"start": 17.00, "end": 18.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.40, "end": 19.82, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.43, "end": 7.41}, {"start": 8.64, "end": 10.53}, {"start": 15.09, "end": 17.28}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 16.258s): "the annexation of Siberia" means only
# "Yermak" until years and outcomes get added -- the app's history games
# link the annexation to its years and outcomes together
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЗНАЮ ТОЛЬКО", "ЕРМАКА"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ПРИСОЕДИНЕНИЕ", "accent": False, "size": "small"}, {"text": "СИБИРИ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "В ЕГЭ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ДЛЯ МЕНЯ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.40, "lines": [{"text": "ЭТО ФАМИЛИЯ", "accent": False, "size": "small"}, {"text": "ЕРМАКА", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.60, "lines": [{"text": "И БОЛЬШЕ", "accent": False, "size": "small"}, {"text": "НИЧЕГО", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 7.80, "lines": [{"text": "ФАМИЛИЯ ЭТО", "accent": False, "size": "small"}, {"text": "НАЧАЛО", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.00, "lines": [{"text": "А НУЖНЫ ЕЩЕ ГОДЫ И", "accent": False, "size": "small"}, {"text": "ИТОГИ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.40, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.60, "lines": [{"text": "ГДЕ ПРИСОЕДИНЕНИЕ", "accent": False, "size": "small"}, {"text": "СИБИРИ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.80, "lines": [{"text": "СВЯЗАНО С", "accent": False, "size": "small"}, {"text": "ГОДАМИ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.019, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.019, "end": 16.258, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.30, "end": 5.01}, {"start": 7.08, "end": 8.55}, {"start": 11.67, "end": 14.19}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 17.218s): the "if it didn't work out" block in a task
# breakdown is a backup exit nobody needs until they do -- the app's text
# breakdown has that exact block too
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЛЮБЛЮ БЛОК", "НЕ ПОЛУЧИЛОСЬ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "В РАЗБОРЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.10, "lines": [{"text": "Я ЛЮБЛЮ", "accent": False, "size": "small"}, {"text": "БЛОК", "accent": True, "size": "big"}]},
    {"start": 4.10, "end": 5.20, "lines": [{"text": "ЕСЛИ НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 5.20, "end": 6.30, "lines": [{"text": "КАК ЗАПАСНОЙ", "accent": False, "size": "small"}, {"text": "ВЫХОД", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.50, "lines": [{"text": "В КИНОТЕАТРЕ ОН НЕ", "accent": False, "size": "small"}, {"text": "НУЖЕН", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.70, "lines": [{"text": "ПОКА ВСЕ ИДЕТ", "accent": False, "size": "small"}, {"text": "ПО ПЛАНУ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.90, "lines": [{"text": "НО СПОКОЙНЕЕ КОГДА ОН", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 11.10, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.10, "end": 12.30, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.30, "end": 13.50, "lines": [{"text": "ГДЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "БЛОК", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.70, "lines": [{"text": "ЕСЛИ НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.90, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 17.218, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.20, "end": 5.04}, {"start": 8.31, "end": 9.57}, {"start": 13.92, "end": 14.85}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (teen boy on couch, 20.46s): comparing presidential and
# parliamentary republics to two buses going the same direction, the
# difference just one precise fact -- the app's games drill forms of
# government by that one key feature
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ДВА АВТОБУСА", "В ОДНУ СТОРОНУ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "ПРЕЗИДЕНТСКУЮ И", "accent": False, "size": "small"}, {"text": "ПАРЛАМЕНТСКУЮ", "accent": True, "size": "small"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "РЕСПУБЛИКИ В ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "Я СРАВНИВАЮ КАК ДВА", "accent": False, "size": "small"}, {"text": "АВТОБУСА", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "ИДУЩИХ В ОДНУ", "accent": False, "size": "small"}, {"text": "СТОРОНУ", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "ОТЛИЧИЕ В ТОМ", "accent": False, "size": "small"}, {"text": "КТО", "accent": True, "size": "big"}]},
    {"start": 7.90, "end": 9.10, "lines": [{"text": "НАЗНАЧАЕТ", "accent": False, "size": "small"}, {"text": "ПРАВИТЕЛЬСТВО", "accent": True, "size": "small"}]},
    {"start": 9.10, "end": 10.70, "lines": [{"text": "И ЭТОТ ПРИЗНАК НУЖНО ЗНАТЬ", "accent": False, "size": "small"}, {"text": "ТОЧНО", "accent": True, "size": "big"}]},
    {"start": 10.70, "end": 12.10, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.10, "end": 13.50, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.90, "lines": [{"text": "ГДЕ ФОРМЫ", "accent": False, "size": "small"}, {"text": "ПРАВЛЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 14.90, "end": 16.30, "lines": [{"text": "РАЗЛИЧАЮТСЯ ПО", "accent": False, "size": "small"}, {"text": "ОДНОМУ", "accent": True, "size": "big"}]},
    {"start": 16.30, "end": 17.70, "lines": [{"text": "КЛЮЧЕВОМУ", "accent": False, "size": "small"}, {"text": "ПРИЗНАКУ", "accent": True, "size": "big"}]},
    {"start": 17.70, "end": 19.10, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.10, "end": 20.46, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 8.13, "end": 9.48}, {"start": 10.62, "end": 11.58}, {"start": 16.17, "end": 18.18}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (teen boy on couch, 14.423s): choosing between a yard
# volleyball game and one more exam task -- the app's FIPI bank: one task
# takes less time than one volleyball set
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ЗАДАНИЕ ИЛИ", "ИГРА"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 2.90, "lines": [{"text": "ВО ДВОРЕ ИГРАЮТ", "accent": False, "size": "small"}, {"text": "ВОЛЕЙБОЛ", "accent": True, "size": "big"}]},
    {"start": 2.90, "end": 3.95, "lines": [{"text": "И Я СПОРЮ", "accent": False, "size": "small"}, {"text": "С СОБОЙ", "accent": True, "size": "big"}]},
    {"start": 3.95, "end": 5.00, "lines": [{"text": "ИДТИ ЛИ В ИГРУ", "accent": False, "size": "small"}, {"text": "ИЛИ РЕШИТЬ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.00, "lines": [{"text": "ЕЩЕ ОДНО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.20, "lines": [{"text": "ДОГОВОРИЛИСЬ СНАЧАЛА ОДНО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.10, "lines": [{"text": "ПОТОМ", "accent": False, "size": "small"}, {"text": "ИГРА", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.20, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 10.20, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.30, "lines": [{"text": "ГДЕ ОДНО ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЗАНИМАЕТ", "accent": True, "size": "big"}]},
    {"start": 11.30, "end": 12.40, "lines": [{"text": "МЕНЬШЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "ОДИН СЕТ", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 13.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 13.40, "end": 14.423, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 5.73, "end": 7.95}, {"start": 10.92, "end": 12.42}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (Рома, 16.791s): a promised bicycle turns the exam goal into
# a measurable number -- the app's FIPI bank: twenty tasks equal one
# wheel of the bike
# ---------------------------------------------------------------------------
i_intro = {"lines": ["СЧИТАЮ", "В КОЛЕСАХ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "МАМА ПООБЕЩАЛА", "accent": False, "size": "small"}, {"text": "ВЕЛОСИПЕД", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.10, "lines": [{"text": "ЗА ХОРОШИЙ", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТ", "accent": True, "size": "big"}]},
    {"start": 4.10, "end": 5.20, "lines": [{"text": "ЕГЭ И Я", "accent": False, "size": "small"}, {"text": "ПОСЧИТАЛ", "accent": True, "size": "big"}]},
    {"start": 5.20, "end": 6.30, "lines": [{"text": "СКОЛЬКО ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "СТОИТ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.30, "lines": [{"text": "ОДНО", "accent": False, "size": "small"}, {"text": "КОЛЕСО", "accent": True, "size": "big"}]},
    {"start": 7.30, "end": 8.50, "lines": [{"text": "ПОЛУЧИЛОСЬ ПРИМЕРНО", "accent": False, "size": "small"}, {"text": "ДВАДЦАТЬ", "accent": True, "size": "big"}]},
    {"start": 8.50, "end": 9.70, "lines": [{"text": "И ЦЕЛЬ ВДРУГ СТАЛА", "accent": False, "size": "small"}, {"text": "ИЗМЕРИМОЙ", "accent": True, "size": "big"}]},
    {"start": 9.70, "end": 10.90, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.90, "end": 12.10, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.10, "end": 13.30, "lines": [{"text": "ГДЕ ДВАДЦАТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 13.30, "end": 14.50, "lines": [{"text": "ЭТО ОДНО", "accent": False, "size": "small"}, {"text": "КОЛЕСО", "accent": True, "size": "big"}]},
    {"start": 14.50, "end": 15.70, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.70, "end": 16.791, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 4.50, "end": 6.75}, {"start": 8.91, "end": 10.11}, {"start": 12.39, "end": 14.07}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
