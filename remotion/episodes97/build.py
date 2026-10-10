#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTIETH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes97/.

Two returning hosts, no new faces: "Рома" / black Under Armour hoodie
(a, e), "teen boy on couch" (b), "mother" / bookshelf+doorway apartment
with small framed picture (c, d, f).

Sub-themes: confusing status and role in obществoznanie until repeated
examples settle it, memorizing war maps as pictures but mixing up who
fought whom without repetition, a daughter whose event recall falls
apart the moment history events arrive out of textbook order, a quiet
return from a practice exam where asking about the score feels too
early, three textbooks that each explain a topic differently until it
turns into confusion, and a parent asked to sit beside a child solving
a task realizing the help needed isn't the answer itself but why the
formula works.
"""
import json

REAL_DURATION = {
    "a": 18.400, "b": 20.162, "c": 20.098,
    "d": 18.200, "e": 17.964, "f": 19.202,
}
SOURCE_FILE = {
    "a": "dghfdgdhgfhgfhgfhf", "b": "fdgsghfgstg", "c": "fdhbsjdshsgbdgdg",
    "d": "fdzhghfdzgdg", "e": "hfhehfdgsdfgdg", "f": "hshbhhgegtf",
}
FIXES = {
    "a": {"напримерах": "примерах"},
    "b": {},
    "c": {"у": "в", "яга": "егэ"},
    "d": {"сипи": "фипи", "профиле": "профиля", "балах": "баллах"},
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
    with open(f"../asr_coffee123_50/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (Рома, 18.400s): confuses status and role in obществoznanie
# depending on mood -- the concepts are similar and only repeated
# examples settle which is which; the app's memory games match statuses
# and roles against examples
# ---------------------------------------------------------------------------
a_intro = {"lines": ["СТАТУС ИЛИ РОЛЬ", "ЗАВИСИТ ОТ НАСТРОЕНИЯ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "РОЛИ И СТАТУСЫ", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ ПУТАЮ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.95, "lines": [{"text": "УЧИТЕЛЬ ЭТО", "accent": False, "size": "small"}, {"text": "СТАТУС ИЛИ РОЛЬ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.00, "lines": [{"text": "ЗАВИСИТ", "accent": False, "size": "small"}, {"text": "ОТ НАСТРОЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.35, "lines": [{"text": "ПОНЯТИЕ", "accent": False, "size": "small"}, {"text": "ПОХОЖЕЕ", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 9.00, "lines": [{"text": "РАЗЛИЧАТЬ ИХ МОЖНО", "accent": False, "size": "small"}, {"text": "ТОЛЬКО НА ПРИМЕРАХ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.80, "lines": [{"text": "КОТОРЫЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ПРОКРУЧИВАТЬ МНОГО РАЗ", "accent": True, "size": "small"}]},
    {"start": 11.10, "end": 12.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.00, "end": 12.90, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 12.90, "end": 14.25, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.25, "end": 16.35, "lines": [{"text": "ГДЕ СТАТУСЫ И РОЛИ", "accent": False, "size": "small"}, {"text": "СООТНОСЯТСЯ С ПРИМЕРАМИ", "accent": True, "size": "small"}]},
    {"start": 16.50, "end": 17.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.60, "end": 18.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.95, "end": 5.97}, {"start": 8.49, "end": 8.94}, {"start": 13.68, "end": 14.13}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (teen boy on couch, 20.162s): remembers war maps as pictures
# with everything fixed in place, but the test asks to name who fought
# whom, and without repetition the participants swap places; the app's
# memory games make wars and their participants get matched against
# each other
# ---------------------------------------------------------------------------
b_intro = {"lines": ["КРАСИВЫЕ КАРТЫ", "А КТО С КЕМ ВОЕВАЛ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "СОЮЗНИКОВ И", "accent": False, "size": "small"}, {"text": "ПРОТИВНИКОВ РОССИИ", "accent": True, "size": "small"}]},
    {"start": 3.30, "end": 4.50, "lines": [{"text": "В ВОЙНАХ", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 6.00, "lines": [{"text": "Я ПОМНЮ", "accent": False, "size": "small"}, {"text": "КРАСИВЫЕ КАРТЫ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.00, "lines": [{"text": "А КТО С КЕМ", "accent": False, "size": "small"}, {"text": "ВОЕВАЛ ПУТАЮ", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 8.70, "lines": [{"text": "НА КАРТЕ ВСЕ", "accent": False, "size": "small"}, {"text": "СТОИТ НА МЕСТАХ", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 10.50, "lines": [{"text": "А В ТЕСТЕ", "accent": False, "size": "small"}, {"text": "НАДО НАЗВАТЬ УЧАСТНИКОВ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 12.60, "lines": [{"text": "БЕЗ ПОВТОРЕНИЯ", "accent": False, "size": "small"}, {"text": "ОНИ МЕНЯЮТСЯ МЕСТАМИ", "accent": True, "size": "big"}]},
    {"start": 13.10, "end": 14.15, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.15, "end": 15.00, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 15.85, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.85, "end": 17.45, "lines": [{"text": "ГДЕ ВОЙНЫ И", "accent": False, "size": "small"}, {"text": "ИХ УЧАСТНИКОВ", "accent": True, "size": "big"}]},
    {"start": 17.45, "end": 18.30, "lines": [{"text": "НУЖНО", "accent": False, "size": "small"}, {"text": "СОПОСТАВЛЯТЬ", "accent": True, "size": "small"}]},
    {"start": 18.35, "end": 19.30, "lines": [{"text": "ССЫЛКА НА ИГО", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.30, "end": 20.162, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.53, "end": 5.28}, {"start": 11.94, "end": 12.72}, {"start": 17.61, "end": 18.15}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 20.098s): a daughter recalls history events in
# textbook order, which holds while she's looking at the page, but the
# exam gives them scrambled and the order falls apart; the app's memory
# games deliver events scrambled and make her arrange them
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПОРЯДОК УЧЕБНИКА", "А В ТЕСТЕ ВПЕРЕМЕЖКУ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "ДОЧЬ НАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "СОБЫТИЯ ДЛЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.65, "lines": [{"text": "ПО ИСТОРИИ В", "accent": False, "size": "small"}, {"text": "ПОРЯДКЕ УЧЕБНИКА", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 5.55, "lines": [{"text": "А В ТЕСТЕ", "accent": False, "size": "small"}, {"text": "ОНИ ВПЕРЕМЕЖКУ", "accent": True, "size": "big"}]},
    {"start": 5.90, "end": 7.20, "lines": [{"text": "ПОРЯДОК УЧЕБНИКА", "accent": False, "size": "small"}, {"text": "ДЕРЖИТ ЕЕ", "accent": True, "size": "big"}]},
    {"start": 7.40, "end": 8.80, "lines": [{"text": "ПОКА ОНА", "accent": False, "size": "small"}, {"text": "СМОТРИТ В СТРАНИЦУ", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 10.90, "lines": [{"text": "А ВПЕРЕМЕЖКУ", "accent": False, "size": "small"}, {"text": "СОБЫТИЯ РАЗВАЛИВАЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 11.60, "end": 12.55, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.55, "end": 13.35, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.35, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.75, "end": 16.45, "lines": [{"text": "ГДЕ СОБЫТИЯ", "accent": False, "size": "small"}, {"text": "ПРИХОДЯТ ВПЕРЕМЕЖКУ", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 18.10, "lines": [{"text": "И ИХ НУЖНО", "accent": False, "size": "small"}, {"text": "РАССТАВЛЯТЬ", "accent": True, "size": "small"}]},
    {"start": 18.15, "end": 19.20, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.04, "end": 5.49}, {"start": 10.41, "end": 11.01}, {"start": 17.19, "end": 17.67}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 18.200s): a daughter comes back from a practice
# exam quiet, and asking about the score feels too early -- so the
# mother offers to go over only the tasks that seemed easy; the app's
# FIPI bank lets her solve calmly without grades or comparisons
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ДОЧЬ ВЕРНУЛАСЬ", "МОЛЧАЛИВОЙ С ПРОБНИКА"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ВЕРНУЛАСЬ С ПРОБНИКА", "accent": False, "size": "small"}, {"text": "МОЛЧАЛИВОЙ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "Я НЕ ЗНАЛА", "accent": False, "size": "small"}, {"text": "О ЧЕМ СПРАШИВАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.70, "lines": [{"text": "СПРАШИВАТЬ", "accent": False, "size": "small"}, {"text": "О БАЛЛАХ РАНО", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.10, "lines": [{"text": "ПОЭТОМУ Я", "accent": False, "size": "small"}, {"text": "ПРЕДЛОЖИЛА РАЗОБРАТЬ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.40, "lines": [{"text": "ТОЛЬКО ТЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ КОТОРЫЕ", "accent": True, "size": "big"}]},
    {"start": 9.40, "end": 10.80, "lines": [{"text": "ПОКАЗАЛИСЬ ЕЙ", "accent": False, "size": "small"}, {"text": "ЛЕГКИМИ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 11.95, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.95, "end": 13.00, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.30, "lines": [{"text": "ГДЕ МОЖНО", "accent": False, "size": "small"}, {"text": "СПОКОЙНО РЕШАТЬ", "accent": True, "size": "big"}]},
    {"start": 14.30, "end": 15.95, "lines": [{"text": "ЗАДАНИЯ БЕЗ", "accent": False, "size": "small"}, {"text": "ОЦЕНОК И СРАВНЕНИЙ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.30, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.30, "end": 18.200, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.13, "end": 2.58}, {"start": 5.70, "end": 6.18}, {"start": 13.62, "end": 14.19}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 17.964s): three textbooks each explain a topic
# differently, so three explanations in a row turn into confusion --
# what's needed is one working source and lots of tasks; the app's
# FIPI bank lets practice start right away without choosing between
# textbooks
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ТРИ УЧЕБНИКА", "ВСЕ ОБЪЯСНЯЮТ ПО СВОЕМУ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "У МЕНЯ ТРИ", "accent": False, "size": "small"}, {"text": "УЧЕБНИКА ПО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.35, "lines": [{"text": "КАЖДЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "ТЕМУ ПО СВОЕМУ", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 5.70, "lines": [{"text": "ПОЭТОМУ Я НЕ ЗНАЮ", "accent": False, "size": "small"}, {"text": "С КАКОГО НАЧИНАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.50, "lines": [{"text": "ТРИ ОБЪЯСНЕНИЯ", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.70, "lines": [{"text": "ПРЕВРАЩАЮТСЯ", "accent": False, "size": "small"}, {"text": "В ПУТАНИЦУ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.75, "lines": [{"text": "МНЕ НУЖНО", "accent": False, "size": "small"}, {"text": "ОДНО РАБОЧЕЕ", "accent": True, "size": "big"}]},
    {"start": 9.75, "end": 10.80, "lines": [{"text": "И МНОГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 11.95, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.95, "end": 12.95, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.95, "end": 14.45, "lines": [{"text": "ГДЕ МОЖНО СРАЗУ", "accent": False, "size": "small"}, {"text": "ПЕРЕХОДИТЬ К ПРАКТИКЕ", "accent": True, "size": "big"}]},
    {"start": 14.50, "end": 16.00, "lines": [{"text": "НЕ ВЫБИРАЯ", "accent": False, "size": "small"}, {"text": "МЕЖДУ УЧЕБНИКАМИ", "accent": True, "size": "small"}]},
    {"start": 16.05, "end": 17.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.00, "end": 17.964, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.67, "end": 3.78}, {"start": 6.90, "end": 7.98}, {"start": 13.11, "end": 13.71}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 19.202s): a daughter asks her mother to sit beside
# her while solving a task, and the mother realizes she can't help with
# the answer itself -- the help needed is someone explaining what's
# behind the formulas; the app's text breakdown explains the steps in
# words a parent can follow too
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ПОПРОСИЛА ПОСИДЕТЬ", "НО ПОМОЧЬ НЕЧЕМ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ДОЧЬ ПОПРОСИЛА", "accent": False, "size": "small"}, {"text": "ПОСИДЕТЬ РЯДОМ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.65, "lines": [{"text": "ПОКА ОНА РЕШАЕТ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 6.30, "lines": [{"text": "И Я ПОНЯЛА", "accent": False, "size": "small"}, {"text": "ЧТО МНЕ НЕЧЕМ ПОМОЧЬ", "accent": True, "size": "big"}]},
    {"start": 7.00, "end": 8.40, "lines": [{"text": "ПОМОЩЬ ЕЙ НУЖНА", "accent": False, "size": "small"}, {"text": "НЕ В ОТВЕТЕ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.90, "lines": [{"text": "А В ТОМ ЧТОБЫ", "accent": False, "size": "small"}, {"text": "КТО ТО ОБЪЯСНИЛ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 11.40, "lines": [{"text": "ЧТО СТОИТ", "accent": False, "size": "small"}, {"text": "ЗА ФОРМУЛАМИ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 12.50, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.50, "end": 13.35, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.40, "end": 14.70, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "ГДЕ ШАГИ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 16.10, "lines": [{"text": "ОПИСАНЫ", "accent": False, "size": "small"}, {"text": "СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 16.10, "end": 17.20, "lines": [{"text": "ПОНЯТНЫМИ", "accent": False, "size": "small"}, {"text": "И МНЕ", "accent": True, "size": "big"}]},
    {"start": 17.30, "end": 18.30, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.202, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.61, "end": 6.21}, {"start": 9.18, "end": 9.84}, {"start": 16.05, "end": 16.47}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
