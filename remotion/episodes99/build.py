#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-SECOND 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes99/.

Three returning hosts, no new faces: "mother" / bookshelf+doorway
apartment with small framed picture (a), "blue-shirt brunette" / THE
SMITHS poster + "ЕГЭ 2026" sticky note room (b, d, e), "blonde in cream
sweater" / desk+lamp+plant+notebook room (c, f).

Sub-themes: a daughter stuck forty minutes on one task with no one to
ask, handwritten arrow-diagrams that turn unreadable an hour later,
uncertainty about formatting rules costing points even when the answer
is right, a friend's invitation competing with three unfinished tasks,
blanking on a known history date under a sibling's pop quiz, and a
library workbook due back in a week with no time to copy it all by
hand.
"""
import json

REAL_DURATION = {
    "a": 22.17, "b": 20.67, "c": 20.22,
    "d": 22.17, "e": 22.35, "f": 20.37,
}
SOURCE_FILE = {
    "a": "fdfgsfsdfdsfsf", "b": "fnsnbbsgg", "c": "gdgsgfsdgsgg",
    "d": "gsgbfdbdfbvgfdbdfb", "e": "gsgfgsgsergesg", "f": "jjdhgsdgdfgbdf",
}
FIXES = {
    "a": {},
    "b": {},
    "c": {"требует": "требуют"},
    "d": {},
    "e": {"а": "за", "побоиса": "побоища", "егат": "егэ"},
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
    with open(f"../asr_coffee123_52/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (mother, 22.17s): a daughter stuck forty minutes on one task
# isn't being stubborn, she's stuck -- the app's FIPI bank lets a hard
# task be parked and returned to later instead of blocking everything
# ---------------------------------------------------------------------------
a_intro = {"lines": ["СОРОК МИНУТ", "НА ОДНОМ ЗАДАНИИ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ДОЧЬ СИДИТ", "accent": False, "size": "small"}, {"text": "НАД ЗАДАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.40, "lines": [{"text": "УЖЕ СОРОК", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 4.40, "end": 5.90, "lines": [{"text": "И НЕ ПРОСИТ", "accent": False, "size": "small"}, {"text": "ПОМОЩИ", "accent": True, "size": "big"}]},
    {"start": 5.90, "end": 7.60, "lines": [{"text": "СОРОК МИНУТ", "accent": False, "size": "small"}, {"text": "НЕ УПОРСТВО", "accent": True, "size": "big"}]},
    {"start": 7.60, "end": 9.20, "lines": [{"text": "А", "accent": False, "size": "small"}, {"text": "ЛОВУШКА", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 11.00, "lines": [{"text": "ПОРА ИДТИ", "accent": False, "size": "small"}, {"text": "ДАЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 11.00, "end": 12.80, "lines": [{"text": "НО БЕЗ", "accent": False, "size": "small"}, {"text": "ПОДСКАЗКИ", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.60, "lines": [{"text": "ОНА НЕ", "accent": False, "size": "small"}, {"text": "УВЕРЕНА", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 18.00, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 20.00, "lines": [{"text": "МОЖНО ВЕРНУТЬСЯ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЮ ПОЗЖЕ", "accent": True, "size": "small"}]},
    {"start": 20.00, "end": 21.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 22.17, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.70, "end": 3.15}, {"start": 7.29, "end": 8.52}, {"start": 17.34, "end": 18.06}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blue-shirt brunette, 20.67s): a solution covered in arrows
# stops making sense an hour later -- the app's text breakdown puts a
# label on every step instead of relying on handwritten shorthand
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СВОИ ЖЕ СТРЕЛКИ", "НЕ ПОНИМАЮ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "НА ЛИСТЕ С", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕМ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.60, "lines": [{"text": "БОЛЬШЕ СТРЕЛОК", "accent": False, "size": "small"}, {"text": "ЧЕМ СЛОВ", "accent": True, "size": "big"}]},
    {"start": 4.60, "end": 6.20, "lines": [{"text": "ЧЕРЕЗ ЧАС", "accent": False, "size": "small"}, {"text": "НЕ ПОНИМАЮ", "accent": True, "size": "big"}]},
    {"start": 6.20, "end": 7.80, "lines": [{"text": "КУДА ОНИ", "accent": False, "size": "small"}, {"text": "ВЕДУТ", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.60, "lines": [{"text": "МОИ СТРЕЛКИ", "accent": False, "size": "small"}, {"text": "ЗАГАДКА", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "ПЕРЕДЕЛЫВАТЬ", "accent": False, "size": "small"}, {"text": "С НУЛЯ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.80, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.20, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 15.80, "lines": [{"text": "ГДЕ У ШАГА", "accent": False, "size": "small"}, {"text": "ЕСТЬ ПОДПИСЬ", "accent": True, "size": "big"}]},
    {"start": 15.80, "end": 17.40, "lines": [{"text": "ЧТО ОН", "accent": False, "size": "small"}, {"text": "ОЗНАЧАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.80, "lines": [{"text": "ССЫЛКА НА Г", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.80, "end": 20.67, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.79, "end": 3.69}, {"start": 8.34, "end": 9.57}, {"start": 16.38, "end": 16.68}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blonde cream sweater, 20.22s): the answer can be right and
# still lose points if the formatting is wrong, and the textbook rules
# for it are vague -- the app's text breakdown shows how to write it up
# ---------------------------------------------------------------------------
c_intro = {"lines": ["БАЛЛЫ СНИМАЮТ", "ЗА ОФОРМЛЕНИЕ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "РЕШИЛА ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "НО НЕ УВЕРЕНА", "accent": False, "size": "small"}, {"text": "В ОФОРМЛЕНИИ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.60, "lines": [{"text": "ПРАВИЛА В УЧЕБНИКЕ", "accent": False, "size": "small"}, {"text": "РАСПЛЫВЧАТЫ", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.40, "lines": [{"text": "ОФОРМЛЕНИЕ", "accent": False, "size": "small"}, {"text": "МЕЛОЧЬ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 10.20, "lines": [{"text": "НО ЗА НЕГО", "accent": False, "size": "small"}, {"text": "СНИМАЮТ БАЛЛЫ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 12.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.00, "end": 13.60, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 15.40, "lines": [{"text": "ГДЕ ПОКАЗАНО", "accent": False, "size": "small"}, {"text": "КАК ОФОРМЛЯТЬ", "accent": True, "size": "big"}]},
    {"start": 15.40, "end": 17.00, "lines": [{"text": "ПРАВИЛЬНОЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 17.00, "end": 18.60, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.60, "end": 20.22, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 6.69, "end": 7.62}, {"start": 9.06, "end": 9.81}, {"start": 11.49, "end": 12.06}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 22.17s): a friend's invitation doesn't
# have to compete with unfinished tasks -- one task solved in five to
# seven minutes from the app's FIPI bank buys a clean conscience
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПОДРУГА ЗОВЕТ", "А ЗАДАНИЯ ЖДУТ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ПОДРУГА ЗОВЕТ", "accent": False, "size": "small"}, {"text": "ГУЛЯТЬ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 4.80, "lines": [{"text": "А У МЕНЯ", "accent": False, "size": "small"}, {"text": "ТРИ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "СТОЮ С", "accent": False, "size": "small"}, {"text": "КУРТКОЙ В РУКАХ", "accent": True, "size": "big"}]},
    {"start": 6.40, "end": 8.60, "lines": [{"text": "РЕШИЛА", "accent": False, "size": "small"}, {"text": "ДОГОВОРИТЬСЯ С СОБОЙ", "accent": True, "size": "small"}]},
    {"start": 8.60, "end": 10.40, "lines": [{"text": "ОДНО ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ДО ВЫХОДА", "accent": True, "size": "big"}]},
    {"start": 10.40, "end": 12.20, "lines": [{"text": "ОСТАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ВЕЧЕРОМ", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 14.00, "lines": [{"text": "И СОВЕСТЬ", "accent": False, "size": "small"}, {"text": "СПОКОЙНА", "accent": True, "size": "big"}]},
    {"start": 14.00, "end": 15.60, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 17.20, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 17.20, "end": 19.00, "lines": [{"text": "УКЛАДЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПЯТЬ СЕМЬ МИНУТ", "accent": True, "size": "big"}]},
    {"start": 19.00, "end": 20.60, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.60, "end": 22.17, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.63, "end": 4.59}, {"start": 5.70, "end": 6.39}, {"start": 18.69, "end": 19.53}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 22.35s): blanking on a date you
# actually knew under a sibling's pop quiz means speed of recall needs
# its own training -- the app's history games drill fast date-naming
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЗАБЫЛА ДАТУ", "КОТОРУЮ ЗНАЛА"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "МЛАДШИЙ БРАТ", "accent": False, "size": "small"}, {"text": "ЗА ЗАВТРАКОМ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.20, "lines": [{"text": "ПРОВЕРИЛ МЕНЯ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 5.20, "end": 6.80, "lines": [{"text": "НЕ ВСПОМНИЛА", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 6.80, "end": 8.40, "lines": [{"text": "ЛЕДОВОГО", "accent": False, "size": "small"}, {"text": "ПОБОИЩА", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 10.00, "lines": [{"text": "ГОД Я", "accent": False, "size": "small"}, {"text": "ЗНАЛА", "accent": True, "size": "big"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "НО В МОМЕНТ", "accent": False, "size": "small"}, {"text": "НЕ ДОСТАЛО", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "ЗНАЧИТ НУЖНА", "accent": False, "size": "small"}, {"text": "ТРЕНИРОВКА", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "БЫСТРОГО", "accent": False, "size": "small"}, {"text": "ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.40, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.00, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 19.60, "lines": [{"text": "ГДЕ ДАТЫ", "accent": False, "size": "small"}, {"text": "НАЗЫВАЮТ БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 19.60, "end": 21.00, "lines": [{"text": "ССЫЛКА НА ЭГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 22.35, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.58, "end": 6.45}, {"start": 9.87, "end": 10.47}, {"start": 19.47, "end": 19.71}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde cream sweater, 20.37s): a library workbook due back
# in a week isn't worth copying by hand -- the app's FIPI bank keeps the
# same tasks on hand without any transcribing at all
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СБОРНИК НА НЕДЕЛЮ", "ПЕРЕПИСЫВАТЬ ДОЛГО"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "СБОРНИК ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "НА НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "КАК УСПЕТЬ", "accent": False, "size": "small"}, {"text": "ПЕРЕПИСАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ВСЕ НУЖНОЕ", "accent": False, "size": "small"}, {"text": "ИЗ НЕГО", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.60, "lines": [{"text": "ПЕРЕПИСЫВАТЬ", "accent": False, "size": "small"}, {"text": "ДОЛГО", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 10.20, "lines": [{"text": "РЕШИЛА РЕШАТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.80, "lines": [{"text": "ПРЯМО ОТТУДА", "accent": False, "size": "small"}, {"text": "А НЕ КОПИРОВАТЬ", "accent": True, "size": "big"}]},
    {"start": 11.80, "end": 13.40, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.40, "end": 15.00, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.60, "lines": [{"text": "ЗАДАНИЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ПОД РУКОЙ", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 18.20, "lines": [{"text": "ПЕРЕПИСЫВАТЬ", "accent": False, "size": "small"}, {"text": "НЕ НУЖНО", "accent": True, "size": "big"}]},
    {"start": 18.20, "end": 19.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.40, "end": 20.37, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 7.80, "end": 8.67}, {"start": 11.16, "end": 11.76}, {"start": 15.09, "end": 16.23}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
