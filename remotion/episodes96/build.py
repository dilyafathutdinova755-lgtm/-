#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-NINTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes96/.

Three returning hosts, no new faces: "blonde in cream sweater" (a, c, h),
"blue-shirt brunette" / THE SMITHS poster room (b, d, f), "teen boy on
couch" (e, i), "Рома" / black Under Armour hoodie (g).

Sub-themes: studying in silence that only actually happens about once a
week, declining numerals by ear from the store instead of by rule,
naming only two of five family functions from the obществoznanie list,
a dead phone stranding an exam variant half-solved until evening, falling
behind a class-chat EGE marathon and switching to counting only your own
daily tasks, an hour-long argument over whose solution method counts,
nodding along three explanations instead of admitting confusion, losing
a point for an unscored criterion no one explains in advance, and losing
a point on a practice exam for an unrecorded trifle you can't predict.
"""
import json

REAL_DURATION = {
    "a": 21.058, "b": 22.920, "c": 18.327,
    "d": 20.695, "e": 17.730, "f": 20.823,
    "g": 16.620, "h": 21.360, "i": 16.108,
}
SOURCE_FILE = {
    "a": "bfhssbvsfgsdfdsfvds", "b": "bsbdsbsfsdfsf", "c": "cxfhgddsafdsfds",
    "d": "dgsgsfsdfsf", "e": "dsfsfsfsff", "f": "dshfggvdsggvsd",
    "g": "fdggfsfgdfdsf", "h": "fndgfgbsfgvgsvsd", "i": "hbsgsdvsdgfdsf",
}
FIXES = {
    "a": {"задание": "задания"},
    "b": {},
    "c": {"пообществознанию": "обществознанию"},
    "d": {},
    "e": {},
    "f": {"тренажери": "тренажере"},
    "g": {},
    "h": {},
    "i": {"тренажери": "тренажере"},
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
    with open(f"../asr_coffee123_49/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blonde in cream sweater, 21.058s): wants to study EGE in
# silence, but home is actually quiet about once a week -- learning to
# solve with background noise, starting from short tasks; the app's
# FIPI bank has short tasks solvable even in a noisy room
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗАНИМАТЬСЯ В ТИШИНЕ", "НЕ ПОЛУЧАЕТСЯ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "ЗАНИМАТЬСЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ХОЧУ В ТИШИНЕ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 5.40, "lines": [{"text": "А ДОМА ТИХО", "accent": False, "size": "small"}, {"text": "РАЗ В НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.10, "lines": [{"text": "ЖДАТЬ ТИШИНЫ", "accent": False, "size": "small"}, {"text": "БЕСПОЛЕЗНО", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 10.20, "lines": [{"text": "УЧУСЬ РЕШАТЬ", "accent": False, "size": "small"}, {"text": "ПРИ ЛЮБОМ ФОНЕ", "accent": True, "size": "big"}]},
    {"start": 10.35, "end": 11.85, "lines": [{"text": "НАЧИНАЯ С", "accent": False, "size": "small"}, {"text": "КОРОТКИХ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.65, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.70, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 16.05, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "КОРОТКИЕ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 18.50, "lines": [{"text": "И ИХ МОЖНО РЕШАТЬ", "accent": False, "size": "small"}, {"text": "ДАЖЕ В ШУМНОЙ ОБСТАНОВКЕ", "accent": True, "size": "big"}]},
    {"start": 19.10, "end": 20.15, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.15, "end": 21.058, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 7.53, "end": 8.01}, {"start": 9.33, "end": 10.08}, {"start": 14.04, "end": 14.58}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blue-shirt brunette, 22.920s): declines numerals in oblique
# cases by ear from the store, not by the textbook rule -- speech habit
# pulls one way, the rule another, until the form becomes automatic;
# the app's memory games repeat such forms in short series
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СКЛОНЯЮ НА СЛУХ", "А НЕ ПО ПРАВИЛАМ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ЧИСЛИТЕЛЬНЫЕ В", "accent": False, "size": "small"}, {"text": "КОСВЕННЫХ ПАДЕЖАХ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 5.40, "lines": [{"text": "СКЛОНЯЮ ТАК", "accent": False, "size": "small"}, {"text": "КАК СЛЫШАЛА В МАГАЗИНЕ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 6.90, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "КАК В УЧЕБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 9.30, "lines": [{"text": "УСТНАЯ РЕЧЬ", "accent": False, "size": "small"}, {"text": "ТЯНЕТ В ОДНУ СТОРОНУ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 10.50, "lines": [{"text": "ПРАВИЛА", "accent": False, "size": "small"}, {"text": "В ДРУГУЮ", "accent": True, "size": "big"}]},
    {"start": 10.80, "end": 12.60, "lines": [{"text": "ПОКА ФОРМА", "accent": False, "size": "small"}, {"text": "НЕ СТАЛА ПРИВЫЧНОЙ", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 13.80, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "СБИВАЮСЬ", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 15.90, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.70, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.85, "end": 19.50, "lines": [{"text": "ГДЕ ТАКИЕ ФОРМЫ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 19.50, "end": 20.80, "lines": [{"text": "КОРОТКИМИ", "accent": False, "size": "small"}, {"text": "СЕРИЯМИ", "accent": True, "size": "big"}]},
    {"start": 20.95, "end": 22.00, "lines": [{"text": "ССЫЛКА НА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.00, "end": 22.920, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.68, "end": 5.52}, {"start": 11.70, "end": 12.15}, {"start": 19.59, "end": 20.46}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blonde in cream sweater, 18.327s): knows the functions of
# the family for obществoznanie but the answer only names two of five --
# the rest get lost along the way and need repetition to stick; the
# app's memory games repeat the family-functions list
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НАЗЫВАЮ ТОЛЬКО ДВЕ", "ИЗ ПЯТИ ФУНКЦИЙ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ФУНКЦИИ СЕМЬИ", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ ЗНАЮ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 5.40, "lines": [{"text": "НО НАЗЫВАЮ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ДВЕ ИЗ ПЯТИ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.20, "lines": [{"text": "ОСТАЛЬНЫЕ ТРИ", "accent": False, "size": "small"}, {"text": "ТЕРЯЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 8.70, "lines": [{"text": "ПО ДОРОГЕ", "accent": False, "size": "small"}, {"text": "ПЕРЕЧИСЛЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 8.70, "end": 9.90, "lines": [{"text": "НУЖНО ЗАКРЕПИТЬ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЕМ", "accent": True, "size": "small"}]},
    {"start": 10.65, "end": 11.70, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 12.30, "end": 13.50, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.90, "end": 16.40, "lines": [{"text": "ГДЕ ФУНКЦИИ СЕМЬИ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ СПИСКОМ", "accent": True, "size": "small"}]},
    {"start": 16.55, "end": 17.50, "lines": [{"text": "ССЫЛКА НА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.50, "end": 18.327, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.38, "end": 5.34}, {"start": 8.97, "end": 9.96}, {"start": 15.03, "end": 15.96}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 20.695s): a phone dies on task three,
# leaving an exam variant half-solved until evening -- returning hours
# later means forgetting where things stopped; the app's FIPI bank lets
# solving continue on any device, picking up the next task without a
# search
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ТЕЛЕФОН РАЗРЯДИЛСЯ", "НА ТРЕТЬЕМ ЗАДАНИИ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "ТЕЛЕФОН РАЗРЯДИЛСЯ", "accent": False, "size": "small"}, {"text": "НА ТРЕТЬЕМ ЗАДАНИИ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.80, "lines": [{"text": "ВАРИАНТ ОСТАЛСЯ", "accent": False, "size": "small"}, {"text": "НЕДОРЕШЕННЫМ", "accent": True, "size": "small"}]},
    {"start": 4.95, "end": 6.00, "lines": [{"text": "ДО", "accent": False, "size": "small"}, {"text": "ВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.65, "lines": [{"text": "ВЕРНУТЬСЯ ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "НЕСКОЛЬКО ЧАСОВ", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 9.15, "lines": [{"text": "ТЯЖЕЛО", "accent": False, "size": "small"}, {"text": "Я ЗАБЫВАЮ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.65, "lines": [{"text": "НА ЧЕМ", "accent": False, "size": "small"}, {"text": "ОСТАНОВИЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 10.65, "end": 12.00, "lines": [{"text": "И ЧТО УЖЕ", "accent": False, "size": "small"}, {"text": "ПРОБОВАЛА", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 13.05, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.20, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 15.75, "lines": [{"text": "ГДЕ МОЖНО РЕШАТЬ", "accent": False, "size": "small"}, {"text": "НА ЛЮБОМ УСТРОЙСТВЕ", "accent": True, "size": "big"}]},
    {"start": 16.10, "end": 17.80, "lines": [{"text": "И БРАТЬ", "accent": False, "size": "small"}, {"text": "СЛЕДУЮЩЕЕ ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 18.70, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПОИСКА", "accent": True, "size": "big"}]},
    {"start": 18.80, "end": 19.90, "lines": [{"text": "ССЫЛКА НА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.90, "end": 20.695, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.38, "end": 4.92}, {"start": 7.74, "end": 8.04}, {"start": 15.21, "end": 15.99}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (teen boy on couch, 17.730s): a class-chat EGE marathon
# leaves him behind by day two -- falling behind feels bad, so he stops
# checking others' count and counts only his own daily tasks; the app's
# FIPI bank lets a chosen number of tasks be closed out without
# watching anyone else
# ---------------------------------------------------------------------------
e_intro = {"lines": ["НА ВТОРОЙ ДЕНЬ", "УЖЕ ОТСТАЛ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "КЛАССНЫЙ ЧАТ", "accent": False, "size": "small"}, {"text": "УСТРОИЛ МАРАФОН", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.65, "lines": [{"text": "НА ВТОРОЙ ДЕНЬ", "accent": False, "size": "small"}, {"text": "ОТСТАЛ ОТ ОСТАЛЬНЫХ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 5.70, "lines": [{"text": "ОТСТАВАТЬ", "accent": False, "size": "small"}, {"text": "НЕПРИЯТНО", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.05, "lines": [{"text": "ПОЭТОМУ Я", "accent": False, "size": "small"}, {"text": "ПЕРЕСТАЛ СМОТРЕТЬ", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 8.40, "lines": [{"text": "НА ЧУЖОЙ СЧЕТ", "accent": False, "size": "small"}, {"text": "И СЧИТАЮ СВОИ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.90, "lines": [{"text": "ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЗА ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 11.10, "lines": [{"text": "В ЕГ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 11.85, "end": 13.65, "lines": [{"text": "ГДЕ МОЖНО ВЫБРАТЬ", "accent": False, "size": "small"}, {"text": "НУЖНОЕ ЧИСЛО ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.70, "lines": [{"text": "И ЗАКРЫТЬ ЕГО", "accent": False, "size": "small"}, {"text": "БЕЗ ОГЛЯДКИ НА ДРУГИХ", "accent": True, "size": "big"}]},
    {"start": 15.80, "end": 16.80, "lines": [{"text": "ССЫЛКА НА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 17.730, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.59, "end": 1.86}, {"start": 5.10, "end": 5.52}, {"start": 14.73, "end": 15.21}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blue-shirt brunette, 20.823s): a girlfriend solves a task a
# different way and the two argue an hour over whose method counts, with
# no source to settle it; the app's text breakdown explains the method
# the way the exam actually expects it
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЧАС СПОРИЛИ", "ЧЕЙ СПОСОБ ДОПУСТИМ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ПОДРУГА РЕШИЛА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ИНАЧЕ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.65, "lines": [{"text": "ЧЕМ Я И", "accent": False, "size": "small"}, {"text": "МЫ ЧАС СПОРИЛИ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 6.30, "lines": [{"text": "ЧЕЙ СПОСОБ", "accent": False, "size": "small"}, {"text": "ДОПУСТИМ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 8.10, "lines": [{"text": "СПОР ЗАКОНЧИЛСЯ", "accent": False, "size": "small"}, {"text": "НИЧЕМ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.30, "lines": [{"text": "ПОТОМУ ЧТО У НАС", "accent": False, "size": "small"}, {"text": "НЕТ ИСТОЧНИКА", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.80, "lines": [{"text": "КОТОРЫЙ СКАЖЕТ", "accent": False, "size": "small"}, {"text": "КАКОЙ ХОД ПРИНЯТ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 13.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.40, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.85, "end": 16.45, "lines": [{"text": "ГДЕ СПОСОБ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ ОБЪЯСНЕН", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 18.50, "lines": [{"text": "ТАК КАК ЕГО", "accent": False, "size": "small"}, {"text": "ОЖИДАЮТ НА ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 18.80, "end": 19.90, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.90, "end": 20.823, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 6.63, "end": 7.47}, {"start": 9.54, "end": 10.20}, {"start": 16.14, "end": 16.56}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (Рома, 16.620s): a task gets explained three times, and on
# the third he just nods though he still doesn't understand -- nodding
# is easier than admitting it, so the question stays unresolved until
# the test; the app's text breakdown can be reread as many times as
# needed, with no one watching
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ТРИ РАЗА ОБЪЯСНИЛИ", "Я ВСЕ РАВНО КИВНУЛ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИЛИ ТРИ РАЗА", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.35, "lines": [{"text": "И В ТРЕТИЙ", "accent": False, "size": "small"}, {"text": "Я КИВНУЛ", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 5.20, "lines": [{"text": "ХОТЯ", "accent": False, "size": "small"}, {"text": "НЕ ПОНЯЛ", "accent": True, "size": "big"}]},
    {"start": 5.20, "end": 6.30, "lines": [{"text": "КИВАТЬ ПРОЩЕ", "accent": False, "size": "small"}, {"text": "ЧЕМ ПРИЗНАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 7.95, "lines": [{"text": "И ВОПРОС", "accent": False, "size": "small"}, {"text": "ОСТАЛСЯ ВИСЕТЬ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.00, "lines": [{"text": "ДО", "accent": False, "size": "small"}, {"text": "САМОГО ТЕСТА", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 9.85, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.85, "end": 10.65, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 12.45, "lines": [{"text": "КОТОРЫЙ МОЖНО", "accent": False, "size": "small"}, {"text": "ПЕРЕЧИТЫВАТЬ", "accent": True, "size": "small"}]},
    {"start": 12.45, "end": 13.80, "lines": [{"text": "СТОЛЬКО РАЗ", "accent": False, "size": "small"}, {"text": "СКОЛЬКО НУЖНО", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 14.65, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "СТЕСНЯЯСЬ", "accent": True, "size": "big"}]},
    {"start": 14.65, "end": 15.70, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.70, "end": 16.620, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 5.25, "end": 6.06}, {"start": 7.26, "end": 7.65}, {"start": 13.89, "end": 14.52}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blonde in cream sweater, 21.360s): a friend gets two of
# three points on a task and doesn't understand why the third was cut --
# grading criteria are rarely shown at school, leaving guesswork; the
# app's text breakdown explains exactly what must be written for full
# points
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ДВА БАЛЛА ИЗ ТРЕХ", "А ЗА ЧТО СНЯЛИ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ПОДРУГА ПОЛУЧИЛА", "accent": False, "size": "small"}, {"text": "ДВА БАЛЛА ИЗ ТРЕХ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 5.10, "lines": [{"text": "И НЕ ПОНЯЛА", "accent": False, "size": "small"}, {"text": "ЗА ЧТО СНЯЛИ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 6.90, "lines": [{"text": "ТРЕТИЙ", "accent": False, "size": "small"}, {"text": "КРИТЕРИЙ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.95, "lines": [{"text": "КРИТЕРИИ ОЦЕНИВАНИЯ", "accent": False, "size": "small"}, {"text": "В ШКОЛЕ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.00, "lines": [{"text": "ПОКАЗЫВАЮТ", "accent": False, "size": "small"}, {"text": "РЕДКО", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.35, "lines": [{"text": "И МЫ ГАДАЕМ", "accent": False, "size": "small"}, {"text": "ЧТО ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 10.35, "end": 12.15, "lines": [{"text": "ПРОВЕРЯЮЩИЙ", "accent": False, "size": "small"}, {"text": "ХОТЕЛ УВИДЕТЬ", "accent": True, "size": "big"}]},
    {"start": 12.30, "end": 13.35, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.25, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 16.65, "lines": [{"text": "ГДЕ ОБЪЯСНЕНО", "accent": False, "size": "small"}, {"text": "ЧТО НУЖНО ЗАПИСАТЬ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 19.00, "lines": [{"text": "ЧТОБЫ ЗАСЧИТАЛИ", "accent": False, "size": "small"}, {"text": "ПОЛНЫЙ БАЛЛ", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.30, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.30, "end": 21.360, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 4.95, "end": 5.67}, {"start": 9.39, "end": 9.60}, {"start": 17.76, "end": 18.78}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (teen boy on couch, 16.108s): a practice EGE costs a point
# over a trifle -- not recording where a number came from -- and such
# trifles can't be predicted in advance, only learned about last, when
# it's too late to fix; the app's text breakdown shows exactly what
# needs to be recorded in the solution
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ПОТЕРЯЛ БАЛЛ", "ЗА МЕЛОЧЬ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ПОТЕРЯЛ БАЛЛ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 3.90, "lines": [{"text": "ЗА МЕЛОЧЬ", "accent": False, "size": "small"}, {"text": "НЕ ЗАПИСАЛ", "accent": True, "size": "big"}]},
    {"start": 3.90, "end": 5.40, "lines": [{"text": "ОТКУДА ВЗЯЛОСЬ", "accent": False, "size": "small"}, {"text": "ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.30, "lines": [{"text": "МЕЛОЧИ НЕЛЬЗЯ", "accent": False, "size": "small"}, {"text": "УГАДАТЬ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.50, "lines": [{"text": "ЗАРАНЕЕ", "accent": False, "size": "small"}, {"text": "И КАЖДЫЙ РАЗ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.40, "lines": [{"text": "УЗНАЕШЬ О НИХ", "accent": False, "size": "small"}, {"text": "ПОСЛЕДНИМ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.30, "lines": [{"text": "КОГДА ИСПРАВИТЬ", "accent": False, "size": "small"}, {"text": "УЖЕ НЕЛЬЗЯ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.00, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.00, "lines": [{"text": "ГДЕ ПОКАЗАНО", "accent": False, "size": "small"}, {"text": "ЧТО ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.15, "lines": [{"text": "ЗАПИСЫВАЮТ", "accent": False, "size": "small"}, {"text": "В РЕШЕНИИ", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 15.30, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.108, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.52, "end": 2.97}, {"start": 7.56, "end": 8.10}, {"start": 13.05, "end": 13.44}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
