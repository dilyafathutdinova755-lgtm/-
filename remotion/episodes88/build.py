#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-FIRST 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes88/.

Three returning hosts, no new faces: "teen boy on couch" / bookshelf+
plant+window room (a, c, i), "Рома" / Under Armour hoodie + desk room
(b, d, e), "mother" / beige sweater + bookshelf+doorway apartment
(f, g, h).

Sub-themes: grandpa's old-school pen-and-paper advice running out of
paper and fresh tasks fast, a friend who calls task breakdowns "someone
else's thoughts" while secretly loving to peek at them, a chat-bot
that only says right/wrong with no reason why, correct spelling known
in the head but lost to a hand that rushes ahead of thought, prepping
only with new tasks and leaving weak spots weak, a daughter unexpectedly
drawn into reading explanations together step by step, dates memorized
only as part of a picture that doesn't survive losing the picture, a
daughter solving tasks secretly at night, and a memorized table that
leaves columns without rows on the real test.
"""
import json

REAL_DURATION = {
    "a": 19.287, "b": 16.620, "c": 15.127,
    "d": 16.620, "e": 17.880, "f": 20.098,
    "g": 19.500, "h": 20.098, "i": 20.012,
}
SOURCE_FILE = {
    "a": "cfbdbdefrebfebebg", "b": "dbdfdfdbfdnfdn", "c": "dfgndergderfgdgv",
    "d": "fbedbdebfdbfdbgfd", "e": "fdbdfgbfvbdvdf", "f": "fdhgdghdgfdgdg",
    "g": "gdjghngdhndfghdfgd", "h": "gfgdbgdfgfdgf", "i": "vfbfdbfbfdbdbd",
}
FIXES = {
    "a": {"егтренажере": "тренажере"},
    "b": {"профия": "профиля"},
    "g": {"о": "а"},
    "h": {"дождь": "дочь", "профиль": "профиля"},
    "i": {"профил": "профиля"},
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
    with open(f"../asr_coffee123_41/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (teen boy on couch, 19.287s): grandpa's old-school advice to
# solve ЕГЭ tasks by hand on paper does help the hand remember, but
# paper runs out fast and pen-tasks need many varied ones, so the
# compilations run dry; the app's FIPI bank lets him pick needed tasks
# and still solve them by hand
# ---------------------------------------------------------------------------
a_intro = {"lines": ["РЕШАТЬ РУЧКОЙ", "НА БУМАГЕ?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.48, "lines": [{"text": "ДЕДУШКА СОВЕТУЕТ", "accent": False, "size": "small"}, {"text": "РЕШАТЬ ПО СТАРИНКЕ", "accent": True, "size": "big"}]},
    {"start": 3.48, "end": 5.07, "lines": [{"text": "РУЧКОЙ НА БУМАГЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ СМЫСЛ", "accent": True, "size": "big"}]},
    {"start": 5.46, "end": 6.33, "lines": [{"text": "РУКА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЕТ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.10, "lines": [{"text": "НО БУМАГИ Я", "accent": False, "size": "small"}, {"text": "ИСПИСЫВАЮ БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 9.87, "lines": [{"text": "А ЗАДАНИЙ ДЛЯ РУЧКИ", "accent": False, "size": "small"}, {"text": "НУЖНО МНОГО", "accent": True, "size": "big"}]},
    {"start": 10.08, "end": 12.00, "lines": [{"text": "И РАЗНЫХ И", "accent": False, "size": "small"}, {"text": "ПОДБОРКИ КОНЧАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.35, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.43, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.43, "end": 16.05, "lines": [{"text": "ОТКУДА МОЖНО", "accent": False, "size": "small"}, {"text": "ВЫБИРАТЬ НУЖНЫЕ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 17.13, "lines": [{"text": "И РЕШАТЬ ИХ ХОТЬ", "accent": False, "size": "small"}, {"text": "РУЧКОЙ", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.48, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.48, "end": 19.287, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.70, "end": 6.33}, {"start": 11.50, "end": 12.00}, {"start": 14.70, "end": 15.06}]
process("a", a_cards, a_intro, a_emphasis)
# NB: ASR merges "ег" into "тренажере" as "егтренажере" here (see
# FIXES["a"]); card text above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode B (Рома, 16.620s): a friend calls ЕГЭ task breakdowns "someone
# else's thoughts" and won't read them, but he likes peeking -- solves
# it himself first, then compares and finds moves he wouldn't have
# thought of; the app's text breakdown has exactly such moves
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЧУЖИЕ МЫСЛИ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.21, "lines": [{"text": "МОЙ ДРУГ СЧИТАЕТ", "accent": False, "size": "small"}, {"text": "РАЗБОРЫ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 3.21, "end": 4.32, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ЧУЖИМИ МЫСЛЯМИ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 5.70, "lines": [{"text": "А МНЕ НРАВИТСЯ", "accent": False, "size": "small"}, {"text": "ЗАГЛЯДЫВАТЬ", "accent": True, "size": "small"}]},
    {"start": 5.91, "end": 7.02, "lines": [{"text": "Я СНАЧАЛА", "accent": False, "size": "small"}, {"text": "РЕШАЮ САМ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.13, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "СРАВНИВАЮ", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 10.20, "lines": [{"text": "И НАХОЖУ ХОДЫ", "accent": False, "size": "small"}, {"text": "КОТОРЫЕ САМ БЫ НЕ ПРИДУМАЛ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.31, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.12, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 12.99, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.58, "lines": [{"text": "В КОТОРОМ ВСТРЕЧАЮТСЯ", "accent": False, "size": "small"}, {"text": "ТАКИЕ ХОДЫ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 15.78, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.78, "end": 16.620, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.10, "end": 5.70}, {"start": 7.50, "end": 8.13}, {"start": 9.70, "end": 10.20}]
process("b", b_cards, b_intro, b_emphasis)
# NB: ASR truncates "профиля" to "профия" here (see FIXES["b"]); card
# text above spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode C (teen boy on couch, 15.127s): checking an ЕГЭ answer in a
# chat-bot that only says correct or incorrect leaves no idea why, so
# the second attempt is almost a guess; the app's text breakdown shows
# the actual reason for the mistake
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТОЛЬКО ВЕРНО", "ИЛИ НЕВЕРНО?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.21, "lines": [{"text": "Я ПРОВЕРЯЮ РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "В ЧАТ БОТЕ", "accent": True, "size": "big"}]},
    {"start": 3.21, "end": 4.86, "lines": [{"text": "КОТОРЫЙ ВЫДАЕТ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ВЕРНО ИЛИ НЕВЕРНО", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.60, "lines": [{"text": "ОЦЕНКУ Я ЗНАЮ", "accent": False, "size": "small"}, {"text": "А ПРИЧИНУ", "accent": True, "size": "big"}]},
    {"start": 6.75, "end": 7.95, "lines": [{"text": "НЕТ И ВТОРАЯ", "accent": False, "size": "small"}, {"text": "ПОПЫТКА ИДЕТ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.06, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "НАУГАД", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.26, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.26, "end": 11.28, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.28, "end": 13.05, "lines": [{"text": "КОТОРЫЙ ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ПРИЧИНУ ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.30, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.30, "end": 15.127, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.30, "end": 4.86}, {"start": 8.30, "end": 8.82}, {"start": 12.60, "end": 13.05}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (Рома, 16.620s): the correct case ending is right in his
# head for Russian ЕГЭ, but the hand writes something else because it
# rushes ahead of thought -- the mistakes aren't from not knowing, they
# are from speed; the app's Russian memory games train response speed
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАЮ НО", "ПИШУ НЕ ТО?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.33, "lines": [{"text": "ПАДЕЖНОЕ ОКОНЧАНИЕ", "accent": False, "size": "small"}, {"text": "СТАВЛЮ ПРАВИЛЬНО", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 4.38, "lines": [{"text": "В ГОЛОВЕ А", "accent": False, "size": "small"}, {"text": "В ПИСЬМЕ", "accent": True, "size": "big"}]},
    {"start": 4.68, "end": 5.55, "lines": [{"text": "ПИШУ НЕ ТО", "accent": False, "size": "small"}, {"text": "РУКА", "accent": True, "size": "big"}]},
    {"start": 5.67, "end": 6.84, "lines": [{"text": "ТОРОПИТСЯ", "accent": False, "size": "small"}, {"text": "БЫСТРЕЕ МЫСЛЕЙ", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.70, "lines": [{"text": "И ОШИБКИ ПОЛУЧАЮТСЯ", "accent": False, "size": "small"}, {"text": "НЕ ОТ НЕЗНАНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 9.96, "lines": [{"text": "А ОТ", "accent": False, "size": "small"}, {"text": "СКОРОСТИ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 11.46, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 12.84, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.02, "end": 14.55, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "СКОРОСТЬ ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 14.85, "end": 15.75, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.75, "end": 16.620, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.50, "end": 6.00}, {"start": 8.10, "end": 8.70}, {"start": 13.20, "end": 13.71}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 17.880s): decided to prep only with new ЕГЭ tasks to
# avoid repeats and skipped review entirely; without repetition the
# weak spots stayed weak and resurfaced on the practice test; the app's
# FIPI bank lets him return straight to the specific number that didn't
# work
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ТОЛЬКО НОВЫЕ", "ЗАДАНИЯ?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.15, "lines": [{"text": "Я РЕШИЛ ГОТОВИТЬСЯ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ПО НОВЫМ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.38, "lines": [{"text": "ЗАДАНИЯМ ЧТОБЫ НЕ", "accent": False, "size": "small"}, {"text": "ВИДЕТЬ ОДНО", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 5.79, "lines": [{"text": "И ТО ЖЕ И НЕ СТАЛ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.02, "lines": [{"text": "НОВОЕ ЭТО", "accent": False, "size": "small"}, {"text": "ХОРОШО", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 9.18, "lines": [{"text": "НО БЕЗ ПОВТОРОВ", "accent": False, "size": "small"}, {"text": "СЛАБЫЕ МЕСТА", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 9.99, "lines": [{"text": "ОСТАЮТСЯ", "accent": False, "size": "small"}, {"text": "СЛАБЫМИ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 11.49, "lines": [{"text": "И НА ПРОБНИКЕ ОНИ", "accent": False, "size": "small"}, {"text": "ВЫЛЕЗЛИ СНОВА", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 12.72, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.72, "end": 13.65, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.97, "lines": [{"text": "ГДЕ МОЖНО", "accent": False, "size": "small"}, {"text": "ВЕРНУТЬСЯ К НОМЕРУ", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 16.00, "lines": [{"text": "КОТОРЫЙ НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 16.00, "end": 16.89, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 17.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 6.70, "end": 7.02}, {"start": 10.70, "end": 11.13}, {"start": 15.20, "end": 15.72}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 20.098s): a daughter asked to read ЕГЭ explanations
# together step by step and got unexpectedly drawn into it -- they read
# a step, stop, she tries to continue on her own, then check against
# the text; the app's text breakdown is step by step, comfortable to
# read together
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЧИТАТЬ ВМЕСТЕ", "ПО ШАГУ?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.36, "lines": [{"text": "ДОЧЬ ПОПРОСИЛА", "accent": False, "size": "small"}, {"text": "ЧИТАТЬ ОБЪЯСНЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 3.36, "end": 5.10, "lines": [{"text": "К ЗАДАНИЯМ ВМЕСТЕ", "accent": False, "size": "small"}, {"text": "ПО ОЧЕРЕДИ", "accent": True, "size": "big"}]},
    {"start": 5.55, "end": 6.75, "lines": [{"text": "И Я НЕОЖИДАННО", "accent": False, "size": "small"}, {"text": "ВТЯНУЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 9.03, "lines": [{"text": "МЫ ЧИТАЕМ ШАГ", "accent": False, "size": "small"}, {"text": "ОСТАНАВЛИВАЕМСЯ", "accent": True, "size": "small"}]},
    {"start": 9.54, "end": 10.77, "lines": [{"text": "ОНА ПРОБУЕТ", "accent": False, "size": "small"}, {"text": "ПРОДОЛЖИТЬ САМА", "accent": True, "size": "big"}]},
    {"start": 11.04, "end": 12.54, "lines": [{"text": "А ПОТОМ МЫ", "accent": False, "size": "small"}, {"text": "СВЕРЯЕМСЯ С ТЕКСТОМ", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.04, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.04, "end": 15.33, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.33, "end": 17.58, "lines": [{"text": "ПО ШАГАМ КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "УДОБНО ЧИТАТЬ ВДВОЕМ", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.25, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.25, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 6.20, "end": 6.75}, {"start": 8.10, "end": 9.03}, {"start": 11.40, "end": 12.06}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (mother, 19.500s): a daughter learned all the period dates
# for ЕГЭ as part of a picture timeline, but loses them entirely without
# the picture -- she remembers the picture whole but not the individual
# events on it; the app's history memory games make her recall events
# without the picture
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ПОМНИТ КАРТИНКУ", "НО НЕ СОБЫТИЯ?"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.39, "lines": [{"text": "ДОЧЬ ВЫУЧИЛА ВСЕ", "accent": False, "size": "small"}, {"text": "ДАТЫ ПЕРИОДА", "accent": True, "size": "big"}]},
    {"start": 3.39, "end": 4.38, "lines": [{"text": "ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "КАРТИНКЕ ТАЙМЛАЙНУ", "accent": True, "size": "big"}]},
    {"start": 4.38, "end": 5.52, "lines": [{"text": "А БЕЗ КАРТИНКИ", "accent": False, "size": "small"}, {"text": "ТЕРЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.38, "lines": [{"text": "Я ЗАМЕТИЛА ЧТО", "accent": False, "size": "small"}, {"text": "КАРТИНКУ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.46, "lines": [{"text": "ОНА ПОМНИТ", "accent": False, "size": "small"}, {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 10.26, "lines": [{"text": "А СОБЫТИЯ НА НЕЙ", "accent": False, "size": "small"}, {"text": "ПО ОТДЕЛЬНОСТИ", "accent": True, "size": "small"}]},
    {"start": 10.41, "end": 11.91, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ВСПОМИНАЕТ", "accent": True, "size": "small"}]},
    {"start": 11.91, "end": 12.78, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.78, "end": 13.86, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 14.85, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.85, "end": 16.86, "lines": [{"text": "ГДЕ СОБЫТИЯ НУЖНО", "accent": False, "size": "small"}, {"text": "ВСПОМИНАТЬ БЕЗ КАРТИНКИ", "accent": True, "size": "big"}]},
    {"start": 17.61, "end": 18.69, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.69, "end": 19.500, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 5.00, "end": 5.52}, {"start": 8.05, "end": 8.46}, {"start": 10.40, "end": 11.01}]
process("g", g_cards, g_intro, g_emphasis)
# NB: ASR mishears "а" as "о" here (see FIXES["g"]); card text above
# spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode H (mother, 20.098s): a daughter secretly solves ЕГЭ tasks at
# night, showing up sleepy and quiet in the morning; not scolding her
# but wanting daytime solving, they agreed on a free evening hour
# instead; the app lets her solve anytime, no night required
# ---------------------------------------------------------------------------
h_intro = {"lines": ["РЕШАЕТ НОЧЬЮ", "ПО СЕКРЕТУ?"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 2.79, "lines": [{"text": "ПО СЕКРЕТУ ОТ МЕНЯ", "accent": False, "size": "small"}, {"text": "РЕШАЕТ", "accent": True, "size": "big"}]},
    {"start": 2.79, "end": 3.90, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "НОЧЬЮ", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 5.52, "lines": [{"text": "И УТРОМ Я ВИЖУ", "accent": False, "size": "small"}, {"text": "ЕЕ СОННОЙ И ТИХОЙ", "accent": True, "size": "big"}]},
    {"start": 6.24, "end": 7.23, "lines": [{"text": "Я НЕ РУГАЮ", "accent": False, "size": "small"}, {"text": "НО ХОЧУ", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 8.40, "lines": [{"text": "ЧТОБЫ ОНА", "accent": False, "size": "small"}, {"text": "РЕШАЛА ДНЕМ", "accent": True, "size": "big"}]},
    {"start": 8.79, "end": 10.56, "lines": [{"text": "И МЫ ДОГОВОРИЛИСЬ", "accent": False, "size": "small"}, {"text": "ЧТО ВЕЧЕРОМ", "accent": True, "size": "big"}]},
    {"start": 10.68, "end": 12.27, "lines": [{"text": "У НЕЕ БУДЕТ", "accent": False, "size": "small"}, {"text": "СВОБОДНЫЙ ЧАС", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.08, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.08, "end": 14.22, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.22, "end": 15.42, "lines": [{"text": "ГДЕ ЗАДАНИЕ МОЖНО", "accent": False, "size": "small"}, {"text": "РЕШАТЬ", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 16.65, "lines": [{"text": "В УДОБНОЕ ВРЕМЯ И", "accent": False, "size": "small"}, {"text": "НОЧЬ", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 17.61, "lines": [{"text": "ДЛЯ ЭТОГО НЕ", "accent": False, "size": "small"}, {"text": "НУЖНА", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.25, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.25, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 4.50, "end": 5.10}, {"start": 8.85, "end": 9.45}, {"start": 10.50, "end": 11.10}]
process("h", h_cards, h_intro, h_emphasis)
# NB: ASR mishears "дочь" as "дождь" and truncates "профиля" to
# "профиль" here (see FIXES["h"]); card text above spells both
# correctly regardless.


# ---------------------------------------------------------------------------
# Episode I (teen boy on couch, 20.012s): state forms for social
# studies were memorized via a table, but the table disappears on the
# real test, leaving columns without rows -- the word "republic" is
# remembered as being somewhere, just not where; the app's memory games
# make him name the state form by its features instead
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ТАБЛИЦА ИСЧЕЗАЕТ", "НА ТЕСТЕ?"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 2.76, "lines": [{"text": "ФОРМА ГОСУДАРСТВА", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.76, "end": 4.17, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "Я ЗАПОМНИЛ ПО ТАБЛИЦЕ", "accent": True, "size": "big"}]},
    {"start": 4.59, "end": 6.06, "lines": [{"text": "А НА ТЕСТЕ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦА ИСЧЕЗАЕТ", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 8.16, "lines": [{"text": "В ГОЛОВЕ ОСТАЮТСЯ", "accent": False, "size": "small"}, {"text": "СТОЛБЦЫ БЕЗ СТРОК", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.90, "lines": [{"text": "И Я ПОМНЮ ЧТО", "accent": False, "size": "small"}, {"text": "ГДЕ ТО БЫЛО", "accent": True, "size": "big"}]},
    {"start": 10.02, "end": 11.16, "lines": [{"text": "СЛОВО", "accent": False, "size": "small"}, {"text": "РЕСПУБЛИКА", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 12.36, "lines": [{"text": "НО НЕ ПОМНЮ", "accent": False, "size": "small"}, {"text": "ГДЕ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.17, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.17, "end": 14.25, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 15.27, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.48, "end": 17.16, "lines": [{"text": "ГДЕ ФОРМА ГОСУДАРСТВА", "accent": False, "size": "small"}, {"text": "НУЖНО НАЗЫВАТЬ", "accent": True, "size": "big"}]},
    {"start": 17.34, "end": 18.15, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ПРИЗНАКАМ", "accent": True, "size": "big"}]},
    {"start": 18.15, "end": 19.17, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.17, "end": 20.012, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 5.55, "end": 6.06}, {"start": 10.20, "end": 10.74}, {"start": 17.30, "end": 17.82}]
process("i", i_cards, i_intro, i_emphasis)
# NB: ASR truncates "профиля" to "профил" here (see FIXES["i"]); card
# text above spells it correctly regardless.

print("ALL EPISODES BUILT AND VALIDATED")
