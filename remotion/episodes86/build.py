#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-NINTH 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes86/.

Three returning hosts, no new faces: curly-haired teen boy / Under Armour
hoodie room (a, d, e), "blonde in cream sweater" (b, c-no wait see below, f, h),
"blue-shirt brunette" / THE SMITHS poster room (c, g, i).

Sub-themes: an ambitious daily-task plan that collapses without a ready
list to pull from, writing Russian by ear and only recalling the rule
afterward, solving a task inside the same chat where friends interrupt
mid-thought, a class chat where the first (usually wrong) answer gets
rubber-stamped, history dates memorized disconnected from their events,
handwriting beauty eating the time meant for actually learning spelling
rules, phone storage forcing deletion of downloaded tasks, a friend's
hallway explanation forgotten by evening, and voice memos that are
impossible to tell apart by name.
"""
import json

REAL_DURATION = {
    "a": 21.200, "b": 23.042, "c": 23.575,
    "d": 17.520, "e": 18.327, "f": 23.490,
    "g": 25.068, "h": 24.520, "i": 26.050,
}
SOURCE_FILE = {
    "a": "bnvhnfbfbghbfgb", "b": "bvmfnmfgnfnfn", "c": "fmnhmfmghbnghbn",
    "d": "gfhfjfjfnfnfnfn", "e": "gfmfmgfnmnfnbf", "f": "gfnngfnfngfnfgnfn",
    "g": "mhmgnfgnfgrhngfnbgf", "h": "nb.mhnfnnfgngfn", "i": "ngbfngfnfnfnfnf",
}
FIXES = {
    "d": {"тренажери": "тренажере"},
    "e": {"уидет": "идет"},
    "g": {"сорфограммами": "орфограммами"},
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
    with open(f"../asr_coffee123_39/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (curly teen boy, 21.200s): an ambitious plan to solve 5 ЕГЭ
# tasks a day collapses on day two because picking which 5 each time is
# its own chore; the app's ordered FIPI bank lets you pick up exactly
# where you left off
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПЛАН НА 5 ЗАДАНИЙ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.54, "lines": [{"text": "НА КАНИКУЛАХ", "accent": False, "size": "small"}, {"text": "СОСТАВИЛ ПЛАН", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.95, "lines": [{"text": "ПЯТЬ ЗАДАНИЙ ЕГЭ", "accent": False, "size": "small"}, {"text": "В ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.06, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "СЛОМАЛСЯ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.17, "lines": [{"text": "НА ВТОРОЙ ДЕНЬ ПОТОМУ ЧТО", "accent": False, "size": "small"}, {"text": "НЕ ЗНАЛ", "accent": True, "size": "big"}]},
    {"start": 7.17, "end": 8.34, "lines": [{"text": "КАКИЕ ПЯТЬ", "accent": False, "size": "small"}, {"text": "ВЫБИРАТЬ", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 9.78, "lines": [{"text": "КАЖДЫЙ РАЗ", "accent": False, "size": "small"}, {"text": "УЖЕ ПОЛОВИНА УСТАЛОСТИ", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 11.28, "lines": [{"text": "А САМИ ПЯТЬ ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "БЫЛИ БЫ", "accent": True, "size": "big"}]},
    {"start": 11.28, "end": 12.51, "lines": [{"text": "ЕРУНДОЙ ЕСЛИ БЫ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.38, "lines": [{"text": "БЫЛ", "accent": False, "size": "small"}, {"text": "ГОТОВ", "accent": True, "size": "big"}]},
    {"start": 13.38, "end": 14.34, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.34, "end": 15.21, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 16.32, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ИДУТ ПО ПОРЯДКУ", "accent": True, "size": "big"}]},
    {"start": 16.32, "end": 17.55, "lines": [{"text": "И ПЯТЬ ПОДРЯД", "accent": False, "size": "small"}, {"text": "МОЖНО БРАТЬ", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 19.05, "lines": [{"text": "С ТОГО МЕСТА", "accent": False, "size": "small"}, {"text": "ГДЕ ОСТАНОВИЛСЯ", "accent": True, "size": "small"}]},
    {"start": 19.35, "end": 20.37, "lines": [{"text": "НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.37, "end": 21.200, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.53, "end": 4.95}, {"start": 12.20, "end": 12.75}, {"start": 16.80, "end": 17.28}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde cream sweater, 23.042s): writes a Russian dictation by
# ear and only recalls the actual spelling rule afterward, so the hand
# has already written and correcting becomes unavoidable; the app's
# memory games train applying the rule before the hand writes
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПИШЕШЬ КАК СЛЫШИШЬ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.48, "lines": [{"text": "СЛИТНО ИЛИ РАЗДЕЛЬНО", "accent": False, "size": "small"}, {"text": "В ДИКТАНТЕ", "accent": True, "size": "big"}]},
    {"start": 3.48, "end": 4.65, "lines": [{"text": "Я ПИШУ ТАК", "accent": False, "size": "small"}, {"text": "КАК СЛЫШУ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 8.10, "lines": [{"text": "А ПРАВИЛО", "accent": False, "size": "small"}, {"text": "ВСПОМИНАЮ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.18, "lines": [{"text": "ПОКА ВСПОМИНАЮ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.50, "lines": [{"text": "РУКА", "accent": False, "size": "small"}, {"text": "УСПЕВАЕТ НАПИСАТЬ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 12.09, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ИСПРАВЛЯТЬ ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 12.09, "end": 13.89, "lines": [{"text": "УЖЕ", "accent": False, "size": "small"}, {"text": "В РАБОТЕ", "accent": True, "size": "big"}]},
    {"start": 13.89, "end": 14.76, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.76, "end": 15.87, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 16.98, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.37, "end": 19.05, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "ПРИМЕНЯТЬ ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 19.35, "end": 20.76, "lines": [{"text": "ДО ТОГО КАК", "accent": False, "size": "small"}, {"text": "РУКА НАПИШЕТ", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 22.05, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.05, "end": 23.042, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.46, "end": 5.94}, {"start": 10.80, "end": 11.25}, {"start": 17.60, "end": 18.12}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 23.575s): solves an ЕГЭ task in the
# same chat where friends keep messaging, each notification cutting the
# thought off mid-way; by evening there are five started tasks and zero
# finished ones; the app's FIPI bank opens tasks away from the chat
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЗАДАНИЕ В ЧАТЕ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.78, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "В ТОМ ЖЕ ЧАТЕ", "accent": True, "size": "big"}]},
    {"start": 3.78, "end": 6.09, "lines": [{"text": "КАЖДОЕ СООБЩЕНИЕ", "accent": False, "size": "small"}, {"text": "ОБРЫВАЕТ МЫСЛЬ", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 8.19, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "СЕРЕДИНЕ", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 10.14, "lines": [{"text": "У МЕНЯ ПЯТЬ", "accent": False, "size": "small"}, {"text": "НАЧАТЫХ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.58, "lines": [{"text": "И НИ ОДНОГО", "accent": False, "size": "small"}, {"text": "ЗАКОНЧЕННОГО", "accent": True, "size": "small"}]},
    {"start": 12.06, "end": 14.97, "lines": [{"text": "ПОТОМУ ЧТО УЖЕ", "accent": False, "size": "small"}, {"text": "ЗАБЫЛА ЗАЧЕМ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.64, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.64, "end": 18.87, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 18.87, "end": 21.00, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЮТСЯ ОТДЕЛЬНО", "accent": True, "size": "small"}]},
    {"start": 21.57, "end": 22.68, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.68, "end": 23.575, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.30, "end": 5.73}, {"start": 10.90, "end": 11.58}, {"start": 12.85, "end": 13.26}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (curly teen boy, 17.520s): the class checks ЕГЭ answers in a
# shared chat, and whoever posts first is almost always wrong but still
# collects agreeing pluses because nobody wants to verify; the app's
# text breakdown lets you check an answer without the chat
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПЕРВЫЙ В ЧАТЕ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.54, "lines": [{"text": "В НАШЕМ КЛАССЕ", "accent": False, "size": "small"}, {"text": "СВЕРЯТЬ ОТВЕТЫ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.86, "lines": [{"text": "ПО ЕГЭ В ЧАТЕ", "accent": False, "size": "small"}, {"text": "КТО ПЕРВЫЙ", "accent": True, "size": "big"}]},
    {"start": 4.86, "end": 6.18, "lines": [{"text": "ПОЧТИ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ОШИБАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 6.48, "end": 7.83, "lines": [{"text": "ОСТАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "СОГЛАШАЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 7.83, "end": 8.65, "lines": [{"text": "ПОТОМУ ЧТО ЛЕНЬ", "accent": False, "size": "small"}, {"text": "ПРОВЕРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 8.65, "end": 10.59, "lines": [{"text": "НЕВЕРНЫЙ ОТВЕТ", "accent": False, "size": "small"}, {"text": "НАБИРАЕТ ПЯТЬ ПЛЮСОВ", "accent": True, "size": "big"}]},
    {"start": 10.86, "end": 11.70, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 13.17, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.17, "end": 15.36, "lines": [{"text": "ПО КОТОРОМУ ОТВЕТ", "accent": False, "size": "small"}, {"text": "МОЖНО ПРОВЕРИТЬ БЕЗ ЧАТА", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.68, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.68, "end": 17.520, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.60, "end": 6.18}, {"start": 8.70, "end": 9.15}, {"start": 14.30, "end": 14.67}]
process("d", d_cards, d_intro, d_emphasis)
# NB: ASR mishears "тренажере" as "тренажери" here (word-ending garble,
# see FIXES["d"]); card text above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode E (curly teen boy, 18.327s): a history notebook has three pages
# of dates disconnected from their events, memorized like a phone book
# and just as fast to forget; the app's history memory games pair the
# date with the event immediately
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ДАТЫ БЕЗ СОБЫТИЙ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.60, "lines": [{"text": "В ТЕТРАДИ ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ТРИ СТРАНИЦЫ", "accent": True, "size": "big"}]},
    {"start": 3.60, "end": 5.85, "lines": [{"text": "И НИ ОДНА ДАТА", "accent": False, "size": "small"}, {"text": "НЕ СВЯЗАНА", "accent": True, "size": "big"}]},
    {"start": 6.24, "end": 7.17, "lines": [{"text": "ЭТО", "accent": False, "size": "small"}, {"text": "СТОЛБИК ЦИФР", "accent": True, "size": "big"}]},
    {"start": 7.38, "end": 9.90, "lines": [{"text": "УЧИТЬ ЕГО", "accent": False, "size": "small"}, {"text": "КАК ТЕЛЕФОННУЮ КНИГУ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.31, "lines": [{"text": "БЫСТРО", "accent": False, "size": "small"}, {"text": "ЗАБЫВАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.18, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.18, "end": 13.38, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.38, "end": 14.25, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.25, "end": 15.54, "lines": [{"text": "ГДЕ ДАТА СРАЗУ", "accent": False, "size": "small"}, {"text": "ИДЁТ ВМЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 15.54, "end": 16.62, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "СОБЫТИЕМ", "accent": True, "size": "big"}]},
    {"start": 16.62, "end": 17.43, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 18.327, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 6.30, "end": 6.75}, {"start": 10.40, "end": 10.95}, {"start": 15.60, "end": 16.14}]
process("e", e_cards, e_intro, e_emphasis)
# NB: ASR mishears "идет" as "уидет" here (see FIXES["e"]); card text
# above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode F (blonde cream sweater, 23.490s): phone storage runs out and
# the downloaded ЕГЭ tasks are first to go since they weigh the most, so
# solving them gets postponed to an evening at the computer that keeps
# not happening; the app's FIPI bank opens tasks by link, nothing to
# download
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ПАМЯТЬ ЗАПОЛНЕНА"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.72, "lines": [{"text": "ТЕЛЕФОН ВЫДАЛ", "accent": False, "size": "small"}, {"text": "ПАМЯТЬ ЗАПОЛНЕНА", "accent": True, "size": "big"}]},
    {"start": 3.72, "end": 4.95, "lines": [{"text": "И ПЕРВЫМИ", "accent": False, "size": "small"}, {"text": "УДАЛИЛА ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.87, "lines": [{"text": "ПОТОМУ ЧТО ОНИ", "accent": False, "size": "small"}, {"text": "ВЕСИЛИ БОЛЬШЕ ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 8.31, "end": 9.33, "lines": [{"text": "РЕШАТЬ ИХ ТЕПЕРЬ", "accent": False, "size": "small"}, {"text": "НЕГДЕ", "accent": True, "size": "big"}]},
    {"start": 9.72, "end": 10.80, "lines": [{"text": "ОТКЛАДЫВАЮ", "accent": False, "size": "small"}, {"text": "ДО ВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 11.13, "end": 12.30, "lines": [{"text": "КОГДА ДОБЕРУСЬ", "accent": False, "size": "small"}, {"text": "ДО КОМПЬЮТЕРА", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 14.76, "lines": [{"text": "А ДО ВЕЧЕРА ОБЫЧНО", "accent": False, "size": "small"}, {"text": "ЧТО НИБУДЬ СЛУЧАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 16.71, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.71, "end": 18.15, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 18.15, "end": 19.65, "lines": [{"text": "ЗАДАНИЕ КОТОРОГО", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЮТСЯ ПО ССЫЛКЕ", "accent": True, "size": "small"}]},
    {"start": 20.04, "end": 21.21, "lines": [{"text": "И СКАЧИВАТЬ ФАЙЛЫ", "accent": False, "size": "small"}, {"text": "НЕ НУЖНО", "accent": True, "size": "big"}]},
    {"start": 21.72, "end": 22.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.60, "end": 23.490, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 3.30, "end": 3.72}, {"start": 9.00, "end": 9.33}, {"start": 14.10, "end": 14.76}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (blue-shirt brunette, 25.068s): trying so hard to make a
# Russian spelling-rules notebook look beautiful that the handwriting
# itself distracts from the meaning of the rules, eating the evening on
# page formatting instead of repeating the rules aloud; the app's
# memory games don't care about handwriting, only about answering
# ---------------------------------------------------------------------------
g_intro = {"lines": ["КРАСИВЫЙ ПОЧЕРК"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 2.70, "lines": [{"text": "НА ТЕТРАДИ С", "accent": False, "size": "small"}, {"text": "ОРФОГРАММАМИ", "accent": True, "size": "small"}]},
    {"start": 3.18, "end": 4.80, "lines": [{"text": "Я ТАК СТАРАЮСЬ", "accent": False, "size": "small"}, {"text": "ПИСАТЬ КРАСИВО", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.27, "lines": [{"text": "ЧТО КРАСОТА", "accent": False, "size": "small"}, {"text": "ПОЧЕРКА", "accent": True, "size": "big"}]},
    {"start": 6.51, "end": 8.46, "lines": [{"text": "ОТВЛЕКАЕТ ОТ СМЫСЛА", "accent": False, "size": "small"}, {"text": "САМИХ ПРАВИЛ", "accent": True, "size": "big"}]},
    {"start": 10.35, "end": 11.73, "lines": [{"text": "Я ТРАЧУ ВЕЧЕР", "accent": False, "size": "small"}, {"text": "НА ОФОРМЛЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 11.88, "end": 14.22, "lines": [{"text": "И ПОЧТИ НЕ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮ ПРАВИЛА ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.47, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 17.64, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 17.64, "end": 18.75, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.26, "end": 20.37, "lines": [{"text": "ГДЕ КРАСОТА", "accent": False, "size": "small"}, {"text": "НИ ПРИЧЕМ", "accent": True, "size": "big"}]},
    {"start": 20.94, "end": 22.20, "lines": [{"text": "А НУЖНО", "accent": False, "size": "small"}, {"text": "ОТВЕТИТЬ НА ВОПРОС", "accent": True, "size": "big"}]},
    {"start": 23.19, "end": 24.24, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 24.24, "end": 25.068, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 5.80, "end": 6.27}, {"start": 11.20, "end": 11.73}, {"start": 19.90, "end": 20.37}]
process("g", g_cards, g_intro, g_emphasis)
# NB: ASR merges "с орфограммами" into "сорфограммами" here (see
# FIXES["g"]); card text above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode H (blonde cream sweater, 24.520s): a friend explains a task in
# two minutes at recess, nodded-along but forgotten by the end of it;
# retrying alone in the evening gets stuck on the second step, and
# calling back feels awkward; the app's text breakdown lets you reread
# just that step as many times as needed, no one to ask
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ПОДРУГА ОБЪЯСНИЛА"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.81, "lines": [{"text": "ПОДРУГА ОБЪЯСНИЛА", "accent": False, "size": "small"}, {"text": "ЗА ДВЕ МИНУТЫ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 6.12, "lines": [{"text": "Я КИВАЛА ХОТЯ", "accent": False, "size": "small"}, {"text": "К КОНЦУ ПЕРЕМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 7.44, "lines": [{"text": "УЖЕ НЕ ПОМНИЛА", "accent": False, "size": "small"}, {"text": "НАЧАЛА", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 9.90, "lines": [{"text": "ВЕЧЕРОМ ПОПРОБОВАЛА", "accent": False, "size": "small"}, {"text": "ПОВТОРИТЬ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.46, "lines": [{"text": "И ЗАСТРЯЛА", "accent": False, "size": "small"}, {"text": "НА ВТОРОМ ШАГЕ", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 14.19, "lines": [{"text": "А ЗВОНИТЬ ПОДРУГЕ", "accent": False, "size": "small"}, {"text": "ВТОРОЙ РАЗ НЕЛОВКО", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.70, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.05, "lines": [{"text": "ВТОРОЙ ШАГ", "accent": False, "size": "small"}, {"text": "КОТОРОГО", "accent": True, "size": "big"}]},
    {"start": 19.32, "end": 20.73, "lines": [{"text": "МОЖНО ПЕРЕЧИТАТЬ", "accent": False, "size": "small"}, {"text": "СКОЛЬКО НУЖНО", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 21.90, "lines": [{"text": "НИКОГО НЕ", "accent": False, "size": "small"}, {"text": "СПРАШИВАЯ", "accent": True, "size": "big"}]},
    {"start": 22.59, "end": 23.67, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.67, "end": 24.520, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 6.50, "end": 7.02}, {"start": 10.10, "end": 10.68}, {"start": 13.70, "end": 14.19}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (blue-shirt brunette, 26.050s): voice memos explaining ЕГЭ
# tasks pile up named only by date, so finding the right one among forty
# identical names means scrolling long enough to forget which task was
# even being asked about; the app's text breakdown is attached directly
# to the task itself, nothing to search by name
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ГОЛОСОВЫЕ ЗАМЕТКИ"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.99, "lines": [{"text": "ЗАПИСЫВАЮ В ТЕЛЕФОН", "accent": False, "size": "small"}, {"text": "ГОЛОСОВЫЕ ЗАМЕТКИ", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.25, "lines": [{"text": "С ОБЪЯСНЕНИЕМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.25, "end": 6.60, "lines": [{"text": "НЕ МОГУ", "accent": False, "size": "small"}, {"text": "НАЙТИ НУЖНУЮ", "accent": True, "size": "big"}]},
    {"start": 6.84, "end": 8.70, "lines": [{"text": "СРЕДИ СОРОКА", "accent": False, "size": "small"}, {"text": "ОДИНАКОВЫХ НАЗВАНИЙ", "accent": True, "size": "big"}]},
    {"start": 9.54, "end": 11.07, "lines": [{"text": "В НАЗВАНИИ СТОИТ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ДАТА", "accent": True, "size": "big"}]},
    {"start": 11.55, "end": 12.63, "lines": [{"text": "И ПОКА Я", "accent": False, "size": "small"}, {"text": "ИЩУ ЗАПИСЬ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 15.00, "lines": [{"text": "ЗАБЫВАЮ О КАКОМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИИ СПРАШИВАЛА", "accent": True, "size": "big"}]},
    {"start": 16.41, "end": 17.49, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 18.30, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.17, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 21.21, "lines": [{"text": "КОТОРЫЙ ПРИВЯЗАН", "accent": False, "size": "small"}, {"text": "К САМОМУ ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 21.66, "end": 23.40, "lines": [{"text": "И ИСКАТЬ ЕГО", "accent": False, "size": "small"}, {"text": "ПО НАЗВАНИЮ НЕ НУЖНО", "accent": True, "size": "big"}]},
    {"start": 24.12, "end": 25.20, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 25.20, "end": 26.050, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 6.15, "end": 6.60}, {"start": 12.90, "end": 13.32}, {"start": 19.80, "end": 20.28}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
