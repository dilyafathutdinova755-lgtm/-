#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTY-THIRD 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes100/.

Four returning hosts, no new faces: "blue-shirt brunette" / THE SMITHS
poster + "ЕГЭ 2026" sticky note room (a, c, d), "mother" / bookshelf+
doorway apartment with small framed picture (b, g), "blonde in cream
sweater" / desk+lamp+plant+notebook room (e, h, i), "teen boy on couch"
(f).

Sub-themes: pausing a 15-minute video so often it takes forty, needing
the exact year rather than "long ago" for a history date, a cat's nap on
a date map crowding out the dates themselves, a rainy day's false sense
of no rush, a typo in a borrowed problem book wasting half an evening on
a problem that isn't even on the exam, an older brother's one piece of
advice from the far side of the exam, a hand-lettered "EGE in progress"
sign that actually works as a household agreement, a teacher's solution
erased before it could be copied down, and a list of hard words that got
lost right after it was made.
"""
import json

REAL_DURATION = {
    "a": 21.45, "b": 17.16, "c": 21.48,
    "d": 21.48, "e": 21.69, "f": 16.11,
    "g": 18.81, "h": 20.16, "i": 20.94,
}
SOURCE_FILE = {
    "a": "bfnhdhfgdgdgdg", "b": "bznhbdfzhzgzgf", "c": "dhhgsgfgsf",
    "d": "fbhadhwrbhwgvbwvg", "e": "fdhbdbvegvvff", "f": "fhdgdgfdgdgd",
    "g": "hfahggvvasvs", "h": "nbdasjhagagag", "i": "nfdanhggs",
}
FIXES = {
    "a": {},
    "b": {"эго": "егэ"},
    "c": {"код": "кот"},
    "d": {},
    "e": {"тренажерик": "тренажере", "шапте": "шапке"},
    "f": {},
    "g": {"дверь": "дверью"},
    "h": {"тренажеры": "тренажере"},
    "i": {"ни": "не"},
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
    with open(f"../asr_coffee123_53/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blue-shirt brunette, 21.45s): pausing a 15-minute video on
# every step turns it into forty -- watching once and solving right
# after, with the app's FIPI bank ready for that exact topic, beats
# pausing the video itself
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПЯТНАДЦАТЬ МИНУТ ВИДЕО", "СМОТРЮ СОРОК"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ВИДЕОУРОК ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "ПЯТНАДЦАТЬ МИНУТ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "А Я СМОТРЮ", "accent": False, "size": "small"}, {"text": "СОРОК", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НА КАЖДОМ ШАГЕ", "accent": False, "size": "small"}, {"text": "ПАУЗА", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ДО ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ДЕЛО ДОХОДИТ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "КОГДА СИЛ", "accent": False, "size": "small"}, {"text": "УЖЕ НЕТ", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "ТЕПЕРЬ СМОТРЮ", "accent": False, "size": "small"}, {"text": "ОДИН РАЗ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "А РЕШАЮ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 18.20, "lines": [{"text": "ПОСЛЕ ПРОСМОТРА", "accent": False, "size": "small"}, {"text": "МОЖНО ВЗЯТЬ ЗАДАНИЕ", "accent": True, "size": "small"}]},
    {"start": 18.20, "end": 19.80, "lines": [{"text": "ССЫЛКА НА ИГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.80, "end": 21.45, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.69, "end": 3.87}, {"start": 9.09, "end": 9.48}, {"start": 12.24, "end": 12.78}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 17.16s): "long ago" isn't an answer for a history
# exam -- the test asks for the exact year and the order of events, and
# the app's history games drill exactly that
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЗНАЕТ ЧТО ДАВНО", "НЕ ЗНАЕТ КОГДА"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ДОЧЬ ЗНАЕТ", "accent": False, "size": "small"}, {"text": "КУЛИКОВСКУЮ БИТВУ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "БЫЛА ДАВНО", "accent": False, "size": "small"}, {"text": "НО КАК ДАВНО", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ВАЖЕН ГОД", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "В ТЕСТЕ ПРОСЯТ", "accent": False, "size": "small"}, {"text": "РАССТАВИТЬ СОБЫТИЯ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "ГДЕ СОБЫТИЯ", "accent": False, "size": "small"}, {"text": "РАССТАВЛЯЮТ ПО ВРЕМЕНИ", "accent": True, "size": "small"}]},
    {"start": 14.60, "end": 16.00, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.00, "end": 17.16, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.28, "end": 2.73}, {"start": 6.33, "end": 6.87}, {"start": 8.22, "end": 9.57}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 21.48s): a cat napping on a date map
# crowds out the dates themselves -- short rounds stick better than one
# big map, and the app's history games deliver dates that way
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ИЗ ВСЕЙ ПОДГОТОВКИ", "ЗАПОМНИЛА ТОЛЬКО КОТА"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "МОЙ КОТ ЛЕГ", "accent": False, "size": "small"}, {"text": "НА КАРТУ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "С ДАТАМИ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ЭТО ЕДИНСТВЕННОЕ", "accent": False, "size": "small"}, {"text": "ЧТО Я ЗАПОМНИЛА", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО КОТ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 10.00, "lines": [{"text": "ЗНАЧИТ ДАТЫ", "accent": False, "size": "small"}, {"text": "НУЖНО ПОДАВАТЬ", "accent": True, "size": "big"}]},
    {"start": 10.00, "end": 11.60, "lines": [{"text": "ИНАЧЕ", "accent": False, "size": "small"}, {"text": "КОРОТКИМИ ИГРАМИ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.20, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "КАРТОЙ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.80, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.40, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.00, "lines": [{"text": "ДАТЫ ПОДАЮТСЯ", "accent": False, "size": "small"}, {"text": "КОРОТКИМИ РАУНДАМИ", "accent": True, "size": "small"}]},
    {"start": 18.00, "end": 19.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.60, "end": 21.48, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.84, "end": 4.59}, {"start": 7.95, "end": 8.43}, {"start": 11.13, "end": 11.97}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 21.48s): a rainy day makes it feel
# like there's no rush -- solving a task early, before that feeling
# takes over, works better than waiting for motivation to return
# ---------------------------------------------------------------------------
d_intro = {"lines": ["В ДОЖДЬ КАЖЕТСЯ", "МОЖНО НЕ ТОРОПИТЬСЯ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "В ДОЖДЬ", "accent": False, "size": "small"}, {"text": "НЕ ТОРОПЛЮСЬ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "И ЕГЭ", "accent": False, "size": "small"}, {"text": "ОТКЛАДЫВАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "ДО", "accent": False, "size": "small"}, {"text": "УТРА", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.40, "lines": [{"text": "Я ЗАМЕТИЛА", "accent": False, "size": "small"}, {"text": "ЗАКОНОМЕРНОСТЬ", "accent": True, "size": "small"}]},
    {"start": 8.40, "end": 10.20, "lines": [{"text": "ТЕПЕРЬ РЕШАЮ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЗАРАНЕЕ", "accent": True, "size": "small"}]},
    {"start": 10.20, "end": 11.80, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "РАССЛАБИЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 11.80, "end": 13.40, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.40, "end": 15.00, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.80, "lines": [{"text": "ПАРА ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ДЕСЯТЬ МИНУТ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.80, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.80, "end": 21.48, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 6.09, "end": 6.75}, {"start": 8.58, "end": 9.81}, {"start": 18.09, "end": 18.63}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde cream sweater, 21.69s): a typo in someone else's
# problem book can burn half an evening on a problem that was never
# going to be on the exam -- the app's text breakdown gives a solution
# to check against line by line
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОПЕЧАТКА ИСПОРТИЛА", "ПОЛВЕЧЕРА"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ОПЕЧАТКА", "accent": False, "size": "small"}, {"text": "В ЗАДАНИИ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 5.30, "lines": [{"text": "ИЗ ЧУЖОГО", "accent": False, "size": "small"}, {"text": "СБОРНИКА", "accent": True, "size": "big"}]},
    {"start": 5.30, "end": 6.90, "lines": [{"text": "ИСПОРТИЛА МНЕ", "accent": False, "size": "small"}, {"text": "ПОЛВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.60, "lines": [{"text": "РЕШАЛА ЗАДАЧУ", "accent": False, "size": "small"}, {"text": "НЕ ИЗ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 10.70, "lines": [{"text": "ПОНЯЛА ЭТО", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ПО ОТВЕТУ", "accent": True, "size": "small"}]},
    {"start": 10.70, "end": 12.40, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 14.00, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.00, "end": 15.60, "lines": [{"text": "УСЛОВИЯ И РЕШЕНИЯ", "accent": False, "size": "small"}, {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 17.50, "lines": [{"text": "МОЖНО СВЕРИТЬ", "accent": False, "size": "small"}, {"text": "ПОСТРОЧНО", "accent": True, "size": "big"}]},
    {"start": 17.50, "end": 19.30, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.30, "end": 21.69, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.87, "end": 5.28}, {"start": 8.19, "end": 8.55}, {"start": 18.60, "end": 19.11}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (teen boy on couch, 16.11s): an older brother's one piece of
# advice from the far side of the exam is simple -- don't put it off --
# and the app's FIPI bank makes that advice easy to follow
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СТАРШИЙ БРАТ СОВЕТУЕТ", "НЕ ТЯНУТЬ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.20, "lines": [{"text": "СТАРШИЙ БРАТ", "accent": False, "size": "small"}, {"text": "ПОСТУПИЛ В ВУЗ", "accent": True, "size": "small"}]},
    {"start": 3.20, "end": 4.80, "lines": [{"text": "РАССКАЗЫВАЕТ ПРО ЕГЭ", "accent": False, "size": "small"}, {"text": "КАК ПРО ПРОШЛОЕ", "accent": True, "size": "small"}]},
    {"start": 4.80, "end": 6.40, "lines": [{"text": "ГЛАВНЫЙ СОВЕТ", "accent": False, "size": "small"}, {"text": "НЕ ТЯНУТЬ", "accent": True, "size": "big"}]},
    {"start": 6.40, "end": 8.00, "lines": [{"text": "ЗАПИСАЛ ЕГО", "accent": False, "size": "small"}, {"text": "НА ЛИСТОК", "accent": True, "size": "big"}]},
    {"start": 8.00, "end": 9.60, "lines": [{"text": "НАД", "accent": False, "size": "small"}, {"text": "СТОЛОМ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.20, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.80, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.20, "lines": [{"text": "ТЯНУТЬ", "accent": False, "size": "small"}, {"text": "НЕЗАЧЕМ", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 15.20, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.20, "end": 16.11, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.79, "end": 7.08}, {"start": 13.02, "end": 13.77}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (mother, 18.81s): a hand-lettered "EGE in progress" sign on
# a bedroom door works as a household agreement rather than a request --
# and the app makes honoring it as short as fifteen minutes
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ТАБЛИЧКА НА ДВЕРИ", "ИДЕТ ЕГЭ"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "ДОЧЬ ВЕШАЕТ", "accent": False, "size": "small"}, {"text": "ТАБЛИЧКУ", "accent": True, "size": "big"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "НАД ДВЕРЬЮ", "accent": False, "size": "small"}, {"text": "ИДЕТ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "МЛАДШИЙ БРАТ", "accent": False, "size": "small"}, {"text": "ЕЕ НАРУШАЕТ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ТАБЛИЧКА", "accent": False, "size": "small"}, {"text": "РАБОТАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "КАК", "accent": False, "size": "small"}, {"text": "ДОГОВОР", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "ДОЧЬ САДИТСЯ", "accent": False, "size": "small"}, {"text": "ЗА СТОЛ ВОВРЕМЯ", "accent": True, "size": "small"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "МОЖНО САДИТЬСЯ", "accent": False, "size": "small"}, {"text": "НА ПЯТНАДЦАТЬ МИНУТ", "accent": True, "size": "small"}]},
    {"start": 16.20, "end": 17.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.60, "end": 18.81, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.76, "end": 3.30}, {"start": 7.29, "end": 8.13}, {"start": 15.33, "end": 15.96}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blonde cream sweater, 20.16s): a board solution erased
# before it can be copied is gone for good -- the app's text breakdown
# stays on screen for as long as it takes to actually read it
# ---------------------------------------------------------------------------
h_intro = {"lines": ["РЕШЕНИЕ СТЕРЛИ", "Я НЕ УСПЕЛА СПИСАТЬ"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "УЧИТЕЛЬ ПОКАЗАЛ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ НА ДОСКЕ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "СТЕР ЕГО", "accent": True, "size": "big"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "НЕ ДОЖДАВШИСЬ", "accent": False, "size": "small"}, {"text": "ПОКА МЫ ПЕРЕПИШЕМ", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ЗАПОМНИТЬ ШАГИ", "accent": False, "size": "small"}, {"text": "С ОДНОГО ВЗГЛЯДА", "accent": True, "size": "small"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "ОСТАЛСЯ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "РЕШЕНИЕ ОСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПЕРЕД ГЛАЗАМИ", "accent": True, "size": "small"}]},
    {"start": 16.20, "end": 17.80, "lines": [{"text": "ПОКА ТЫ", "accent": False, "size": "small"}, {"text": "ЕГО ЧИТАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 19.00, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.00, "end": 20.16, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.39, "end": 3.81}, {"start": 8.31, "end": 8.94}, {"start": 15.66, "end": 16.20}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (blonde cream sweater, 20.94s): a hand-written list of hard
# words is one more thing that can get lost -- the app's memory games
# for Russian put the same words somewhere they can't be
# ---------------------------------------------------------------------------
i_intro = {"lines": ["СОСТАВИЛА СПИСОК СЛОВ", "И ПОТЕРЯЛА ЕГО"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.40, "lines": [{"text": "СПИСОК ТРУДНЫХ СЛОВ", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ", "accent": True, "size": "small"}]},
    {"start": 3.40, "end": 5.00, "lines": [{"text": "СОСТАВИЛА", "accent": False, "size": "small"}, {"text": "А ПОТОМ ПОТЕРЯЛА", "accent": True, "size": "small"}]},
    {"start": 5.00, "end": 6.60, "lines": [{"text": "САМ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.20, "lines": [{"text": "ТЕПЕРЬ ПОВТОРЯЮ", "accent": False, "size": "small"}, {"text": "СЛОВА ТАМ", "accent": True, "size": "small"}]},
    {"start": 8.20, "end": 9.80, "lines": [{"text": "ГДЕ ИХ", "accent": False, "size": "small"}, {"text": "НЕЛЬЗЯ ПОТЕРЯТЬ", "accent": True, "size": "small"}]},
    {"start": 9.80, "end": 11.40, "lines": [{"text": "В ИГРЕ", "accent": False, "size": "small"}, {"text": "НА ТЕЛЕФОНЕ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 13.00, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.00, "end": 14.60, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 16.20, "lines": [{"text": "ГДЕ СЛОВА", "accent": False, "size": "small"}, {"text": "НЕ ТЕРЯЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.80, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ВОЗВРАЩАЮТСЯ САМИ", "accent": True, "size": "small"}]},
    {"start": 17.80, "end": 19.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.40, "end": 20.94, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 4.26, "end": 5.25}, {"start": 8.19, "end": 8.76}, {"start": 17.28, "end": 18.18}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
