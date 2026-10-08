#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-FIFTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes92/.

Four returning hosts, no new faces: "mother" (a, c), "blue-shirt
brunette" / THE SMITHS poster room (b, g, h), "blonde in cream sweater"
(d, f), "teen boy on couch" (e, i).

Sub-themes: a calculator that confirms the number but not the
reasoning, a deskmate's spelling question answered a beat too late
because knowing the rule isn't the same as reacting fast, a printer at
work side-eyeing a mother who prints EGE tasks for her daughter before
every lesson, confusing task numbers 12 and 16 without a number+topic
pairing to anchor them, an older brother's EGE printouts rotting in a
box on the balcony, grandma's one word for every kind of tax against
the EGE's need to tell direct from indirect, one shared family computer
and twenty minutes before lights-out, three near-identical formulas
and no explanation of how to pick the right one, and chat-typing habits
bleeding into a Russian dictation.
"""
import json

REAL_DURATION = {
    "a": 21.360, "b": 24.520, "c": 17.602,
    "d": 20.012, "e": 17.730, "f": 21.960,
    "g": 27.692, "h": 20.332, "i": 16.855,
}
SOURCE_FILE = {
    "a": "dhbdhjfdhfdh", "b": "fdhdjfdhdhndg", "c": "fhdjhdhfdhdgd",
    "d": "gdhhfdjdh", "e": "gdhjfdjdfj", "f": "gfhhfdhhdh",
    "g": "gfnfdjejehehy", "h": "jhfdehjghefheghe", "i": "tehnjtdhdhdh",
}
FIXES = {
    "a": {"здания": "задания", "она": "на", "нерассуждения": "рассуждения"},
    "e": {"лезь": "лезть"},
    "h": {"задании": "заданию"},
    "i": {"чатовтянутся": "чата"},
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
    with open(f"../asr_coffee123_45/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (mother, 21.360s): a calculator confirms the number is
# right but gets lost on a similar task -- it checks the number, not
# the reasoning, so it is useless on anything new; the app's text
# breakdown checks the reasoning itself
# ---------------------------------------------------------------------------
a_intro = {"lines": ["КАЛЬКУЛЯТОР ПОДТВЕРДИЛ", "НО ЗАДАНИЕ НЕ ЗАШЛО?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 4.20, "lines": [{"text": "СВОЕ РЕШЕНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПРОВЕРИЛА КАЛЬКУЛЯТОРОМ", "accent": True, "size": "small"}]},
    {"start": 4.65, "end": 6.33, "lines": [{"text": "НА ПОХОЖЕМ ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "Я ПОТЕРЯЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.70, "lines": [{"text": "КАЛЬКУЛЯТОР", "accent": False, "size": "small"}, {"text": "ПОДТВЕРЖДАЕТ ЧИСЛО", "accent": True, "size": "small"}]},
    {"start": 9.15, "end": 10.26, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "РАССУЖДЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 10.26, "end": 12.75, "lines": [{"text": "ПОЭТОМУ НА НОВЫХ", "accent": False, "size": "small"}, {"text": "НИЧЕМ НЕ ПОМОГАЕТ", "accent": True, "size": "big"}]},
    {"start": 13.68, "end": 15.03, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 15.18, "end": 16.20, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 18.78, "lines": [{"text": "КОТОРЫЙ ПРОВЕРЯЕТ", "accent": False, "size": "small"}, {"text": "НЕ ЧИСЛО А РАССУЖДЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 19.56, "end": 20.50, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.50, "end": 21.360, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.85, "end": 6.33}, {"start": 7.74, "end": 8.22}, {"start": 18.24, "end": 18.78}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blue-shirt brunette, 24.520s): a deskmate's spelling
# question gets answered a beat too late -- the rule is known, but in
# the moment the answer doesn't come, proving speed matters as much as
# knowledge; the app's memory games drill words until they come back
# instantly
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ОТВЕТ НЕ ПРИШЕЛ", "ВОВРЕМЯ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.45, "lines": [{"text": "СОСЕДКА ПО ПАРТЕ", "accent": False, "size": "small"}, {"text": "СПРОСИЛА ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 6.30, "lines": [{"text": "Я ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ОТВЕТИЛА НЕ СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 9.00, "lines": [{"text": "ПРАВИЛО Я", "accent": False, "size": "small"}, {"text": "ЗНАЮ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 11.40, "lines": [{"text": "НО В МОМЕНТ", "accent": False, "size": "small"}, {"text": "ОТВЕТ НЕ ПРИШЕЛ", "accent": True, "size": "big"}]},
    {"start": 12.03, "end": 14.73, "lines": [{"text": "ЗНАЧИТ НУЖНА", "accent": False, "size": "small"}, {"text": "БЫСТРАЯ РЕАКЦИЯ", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 17.43, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 17.91, "end": 19.20, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.47, "end": 21.78, "lines": [{"text": "ГДЕ СЛОВА", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ СНОВА", "accent": True, "size": "small"}]},
    {"start": 22.56, "end": 23.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.60, "end": 24.520, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 11.13, "end": 11.40}, {"start": 12.90, "end": 13.23}, {"start": 20.37, "end": 20.88}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 17.602s): a daughter asks for EGE tasks printed
# before every lesson, and the office printer, the mother carrying
# paper, and the daughter waiting are all equally tired of it; the
# app's FIPI bank opens tasks with no printing involved
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПРИНТЕР СМОТРИТ", "С УКОРОМ?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.81, "lines": [{"text": "ДОЧЬ ПРОСИТ", "accent": False, "size": "small"}, {"text": "РАСПЕЧАТАТЬ ЕГЭ", "accent": True, "size": "small"}]},
    {"start": 4.17, "end": 6.45, "lines": [{"text": "ПРИНТЕР НА РАБОТЕ", "accent": False, "size": "small"}, {"text": "СМОТРИТ С УКОРОМ", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.43, "lines": [{"text": "МНЕ НАДОЕЛО", "accent": False, "size": "small"}, {"text": "НОСИТЬ БУМАГУ", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 10.89, "lines": [{"text": "ДОЧЕРИ НАДОЕЛО", "accent": False, "size": "small"}, {"text": "ЖДАТЬ МЕНЯ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.35, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.56, "end": 15.15, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЮТСЯ БЕЗ ПЕЧАТИ", "accent": True, "size": "small"}]},
    {"start": 15.72, "end": 16.65, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 17.602, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 6.09, "end": 6.45}, {"start": 9.21, "end": 9.48}, {"start": 14.16, "end": 14.55}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blonde cream sweater, 20.012s): EGE task numbers twelve
# and sixteen get confused constantly, forcing a cheat-sheet check
# every time -- seeing the number and topic together is what makes
# them stick; the app's FIPI bank numbers every task so it's easy to
# find
# ---------------------------------------------------------------------------
d_intro = {"lines": ["НОМЕРА ЗАДАНИЙ", "ПУТАЕШЬ КАЖДЫЙ РАЗ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 4.08, "lines": [{"text": "НОМЕРА ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ПУТАЮ КАЖДЫЙ РАЗ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 6.60, "lines": [{"text": "ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ЗАГЛЯДЫВАТЬ В БУМАЖКУ", "accent": True, "size": "small"}]},
    {"start": 7.29, "end": 9.78, "lines": [{"text": "НУЖНО ВИДЕТЬ", "accent": False, "size": "small"}, {"text": "НОМЕР И ТЕМУ РЯДОМ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 11.40, "lines": [{"text": "ЧТОБЫ ОНИ", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЛИСЬ ВМЕСТЕ", "accent": True, "size": "small"}]},
    {"start": 12.33, "end": 13.98, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 17.28, "lines": [{"text": "ГДЕ У КАЖДОГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ ЕСТЬ НОМЕР", "accent": True, "size": "big"}]},
    {"start": 18.15, "end": 19.17, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.17, "end": 20.012, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.61, "end": 3.15}, {"start": 8.25, "end": 8.43}, {"start": 16.47, "end": 16.77}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (teen boy on couch, 17.730s): an older brother's old EGE
# printouts sit in a box on the balcony -- dusty, damp, maybe mice --
# and still have to be dug through to find the right pages; the app's
# FIPI bank is clean, no digging, no mice
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СТАРЫЕ РАСПЕЧАТКИ", "НА БАЛКОНЕ С МЫШАМИ?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 4.02, "lines": [{"text": "БРАТ ХРАНИТ РАСПЕЧАТКИ", "accent": False, "size": "small"}, {"text": "В КОРОБКЕ НА БАЛКОНЕ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 5.61, "lines": [{"text": "А ЛЕЗТЬ ТУДА", "accent": False, "size": "small"}, {"text": "НЕ ХОЧЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.08, "lines": [{"text": "ТАМ", "accent": False, "size": "small"}, {"text": "ПЫЛЬ И СЫРОСТЬ", "accent": True, "size": "big"}]},
    {"start": 7.26, "end": 9.33, "lines": [{"text": "И ВОЗМОЖНО", "accent": False, "size": "small"}, {"text": "МЫШИ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.25, "lines": [{"text": "НУЖНЫЕ СТРАНИЦЫ", "accent": False, "size": "small"}, {"text": "ЕЩЕ НАДО НАЙТИ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 13.47, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.71, "end": 15.60, "lines": [{"text": "ГДЕ ЗАДАНИЯ ЧИСТЫЕ", "accent": False, "size": "small"}, {"text": "И БЕЗ МЫШЕЙ", "accent": True, "size": "big"}]},
    {"start": 15.93, "end": 16.90, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.90, "end": 17.730, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.72, "end": 4.02}, {"start": 9.15, "end": 9.33}, {"start": 15.21, "end": 15.60}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde cream sweater, 21.960s): grandma calls every kind
# of tax by one word, but the EGE in social studies needs direct and
# indirect told apart -- invisible at home, worth a point on the exam,
# and a table alone doesn't make it stick; the app's memory games force
# recalling the distinction
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ПРЯМЫЕ И КОСВЕННЫЕ", "ДОМА РАЗНИЦА НЕЗАМЕТНА?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "БАБУШКА", "accent": False, "size": "small"}, {"text": "НАЛОГИ", "accent": True, "size": "big"}]},
    {"start": 3.33, "end": 4.80, "lines": [{"text": "А МНЕ ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 4.98, "end": 7.05, "lines": [{"text": "НУЖНО РАЗЛИЧАТЬ", "accent": False, "size": "small"}, {"text": "ПРЯМЫЕ И КОСВЕННЫЕ", "accent": True, "size": "big"}]},
    {"start": 7.98, "end": 9.12, "lines": [{"text": "ДОМА", "accent": False, "size": "small"}, {"text": "РАЗНИЦА НЕЗАМЕТНА", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 11.07, "lines": [{"text": "А НА ЭКЗАМЕНЕ", "accent": False, "size": "small"}, {"text": "ОНА СТОИТ БАЛЛА", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.02, "lines": [{"text": "И ТАБЛИЦА", "accent": False, "size": "small"}, {"text": "ЕЕ НЕ ЗАКРЕПЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 15.63, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 15.87, "end": 17.04, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.22, "end": 19.38, "lines": [{"text": "КОТОРЫЕ ЗАСТАВЛЯЮТ", "accent": False, "size": "small"}, {"text": "ВСПОМИНАТЬ РАЗЛИЧИЯ", "accent": True, "size": "big"}]},
    {"start": 20.13, "end": 21.05, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.05, "end": 21.960, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 6.63, "end": 7.05}, {"start": 10.44, "end": 10.65}, {"start": 18.15, "end": 18.54}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (blue-shirt brunette, 27.692s): one shared family computer
# means twenty minutes before lights-out once her turn finally comes --
# so evenings stopped stretching and two or three tasks now have to fit
# before the keyboard changes hands; the app's FIPI bank finds the
# needed task fast enough that twenty minutes covers several
# ---------------------------------------------------------------------------
g_intro = {"lines": ["КОМПЬЮТЕР ОДИН", "НА ТРОИХ?"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 4.86, "lines": [{"text": "КОМПЬЮТЕР ОДИН", "accent": False, "size": "small"}, {"text": "НА ТРОИХ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.15, "lines": [{"text": "РЕШАТЬ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 8.34, "lines": [{"text": "ОСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "ДВАДЦАТЬ МИНУТ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 11.58, "lines": [{"text": "Я ПЕРЕСТАЛА", "accent": False, "size": "small"}, {"text": "РАСТЯГИВАТЬ", "accent": True, "size": "small"}]},
    {"start": 11.76, "end": 14.76, "lines": [{"text": "И ПРОБУЮ УЛОЖИТЬСЯ", "accent": False, "size": "small"}, {"text": "В ДВА ТРИ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 15.06, "end": 16.89, "lines": [{"text": "ПОКА НИКТО", "accent": False, "size": "small"}, {"text": "НЕ ВЕРНУЛ КЛАВИАТУРУ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 20.22, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 20.61, "end": 22.62, "lines": [{"text": "ГДЕ НУЖНОЕ", "accent": False, "size": "small"}, {"text": "НАХОДИТСЯ БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 23.01, "end": 25.05, "lines": [{"text": "И ДВАДЦАТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "ХВАТАЕТ НА НЕСКОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 25.71, "end": 26.75, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 26.75, "end": 27.692, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 7.02, "end": 7.32}, {"start": 16.41, "end": 16.89}, {"start": 23.13, "end": 23.46}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blue-shirt brunette, 20.332s): a classmate's vague
# explanation sends her hunting for the right formula, three similar
# ones turn up and the wrong one gets picked because nobody explained
# how to choose; the app's text breakdown explains why that specific
# formula was the right one
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ТРИ ПОХОЖИЕ ФОРМУЛЫ", "ВЫБРАЛА НЕ ТУ?"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.93, "lines": [{"text": "ОБЪЯСНЕНИЕ ОТ", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИЦЫ", "accent": True, "size": "small"}]},
    {"start": 4.59, "end": 5.52, "lines": [{"text": "ЗВУЧАЛО", "accent": False, "size": "small"}, {"text": "НУ ТАМ ПО ФОРМУЛЕ", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 7.89, "lines": [{"text": "Я ПОШЛА", "accent": False, "size": "small"}, {"text": "ИСКАТЬ ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.81, "lines": [{"text": "НАШЛА ТРИ ПОХОЖИХ", "accent": False, "size": "small"}, {"text": "И ВЫБРАЛА НЕ ТУ", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 12.12, "lines": [{"text": "ПОТОМУ ЧТО НИКТО", "accent": False, "size": "small"}, {"text": "НЕ ОБЪЯСНИЛ", "accent": True, "size": "big"}]},
    {"start": 12.96, "end": 14.52, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 14.67, "end": 16.08, "lines": [{"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": False, "size": "small"}, {"text": "ГДЕ НАПИСАНО", "accent": True, "size": "big"}]},
    {"start": 16.23, "end": 18.03, "lines": [{"text": "ПОЧЕМУ ВЫБРАНА", "accent": False, "size": "small"}, {"text": "ИМЕННО ЭТА ФОРМУЛА", "accent": True, "size": "big"}]},
    {"start": 18.48, "end": 19.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.40, "end": 20.332, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 8.31, "end": 8.70}, {"start": 10.92, "end": 11.34}, {"start": 16.59, "end": 16.92}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (teen boy on couch, 16.855s): friends write however it
# comes out in chat, he picked up the same habit, and the EGE in
# Russian won't forgive it -- chat shortcuts leak into a dictation and
# have to be corrected one at a time; the app's memory games cement
# the correct pairs instead
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ПРИВЫЧКИ ИЗ ЧАТА", "В ДИКТАНТЕ НЕ ПРОСТЯТ?"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.06, "lines": [{"text": "МОИ ДРУЗЬЯ", "accent": False, "size": "small"}, {"text": "ПИШУТ КАК ПРИДЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 3.36, "end": 4.20, "lines": [{"text": "И Я", "accent": False, "size": "small"}, {"text": "НАЧАЛ ТАКЖЕ", "accent": True, "size": "big"}]},
    {"start": 4.59, "end": 6.24, "lines": [{"text": "А ЕГЭ ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЭТОГО НЕ ПРОСТИТ", "accent": True, "size": "big"}]},
    {"start": 6.81, "end": 8.37, "lines": [{"text": "ПРИВЫЧКИ ИЗ ЧАТА", "accent": False, "size": "small"}, {"text": "ПОПАДАЮТ В ДИКТАНТ", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.78, "lines": [{"text": "И ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ИСПРАВЛЯТЬ ПО ОДНОЙ", "accent": True, "size": "big"}]},
    {"start": 10.35, "end": 11.85, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 12.06, "end": 14.61, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "ГДЕ ПАРЫ ЗАКРЕПЛЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 14.94, "end": 15.95, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.95, "end": 16.855, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 5.85, "end": 6.24}, {"start": 9.12, "end": 9.48}, {"start": 14.07, "end": 14.61}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
