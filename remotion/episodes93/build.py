#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-SIXTH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes93/.

Two returning hosts, no new faces: "Рома" / tight curls, black Under
Armour hoodie (a, c, f -- one of these filmed by a different window
with a sunset cityscape, same host and hoodie), "teen boy on couch"
(b), "mother" (d, e).

Sub-themes: signing up for an EGE course and realizing the night
before that he doesn't know his own starting level, a task explained
with a drawing that's gone by evening leaving only arrows pointing
nowhere, word-transfer rules written off as "easy" in school and
exactly where points get lost, a daughter who can retell the news but
not name the social-studies term for it, a vague "how did you solve
it" that only opens up once asked to write the first sentence in
words, and a fear that a task breakdown will be cluttered turning out
wrong once it's broken into skippable steps.
"""
import json

REAL_DURATION = {
    "a": 15.426, "b": 15.084, "c": 15.362,
    "d": 18.562, "e": 19.650, "f": 16.620,
}
SOURCE_FILE = {
    "a": "fcvcjndfjhbhgdgfdgfd", "b": "frujhhghfhhy", "c": "gfdjhfdjhdhdgfd",
    "d": "gfnjbnghbfghh", "e": "jdjnhgdyhh", "f": "jgfngdhnfnfnb",
}
FIXES = {
    "a": {"профия": "профиля"},
    "b": {"тренажери": "тренажере"},
    "d": {"гэ": "егэ"},
    "e": {"отвечают": "отвечает"},
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
    with open(f"../asr_coffee123_46/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (Рома, 15.426s): signs up for an EGE prep course, and the
# day before realizes he has no idea what he already knows -- wants to
# walk in with a sense of his own level, not empty-handed; the app's
# FIPI bank lets a couple of tasks get solved first to gauge that level
# ---------------------------------------------------------------------------
a_intro = {"lines": ["НА КУРСЫ С ЧЕМ", "С УРОВНЕМ ИЛИ ПУСТЫМИ РУКАМИ?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.93, "lines": [{"text": "ЗАПИСАЛСЯ НА КУРСЫ", "accent": False, "size": "small"}, {"text": "А В ПЯТНИЦУ ПОНЯЛ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 4.98, "lines": [{"text": "ЧТО", "accent": False, "size": "small"}, {"text": "НЕ ЗНАЮ ЧТО УМЕЮ", "accent": True, "size": "big"}]},
    {"start": 5.22, "end": 6.99, "lines": [{"text": "ХОЧЕТСЯ ПРИЙТИ", "accent": False, "size": "small"}, {"text": "С ПРЕДСТАВЛЕНИЕМ", "accent": True, "size": "small"}]},
    {"start": 7.08, "end": 8.88, "lines": [{"text": "О СВОЕМ УРОВНЕ", "accent": False, "size": "small"}, {"text": "А НЕ С ПУСТЫМИ РУКАМИ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.86, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.98, "end": 12.27, "lines": [{"text": "ГДЕ МОЖНО", "accent": False, "size": "small"}, {"text": "РЕШИТЬ ПАРУ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.62, "lines": [{"text": "И ОЦЕНИТЬ", "accent": False, "size": "small"}, {"text": "СВОЙ УРОВЕНЬ", "accent": True, "size": "big"}]},
    {"start": 13.70, "end": 14.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 15.426, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.22, "end": 5.49}, {"start": 8.28, "end": 8.88}, {"start": 12.63, "end": 12.90}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (teen boy on couch, 15.084s): a task gets explained with a
# drawing, but by evening the drawing is gone and nobody wrote down the
# words, leaving only arrows in his head that lead nowhere; the app's
# text breakdown has everything spelled out in words
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СТРЕЛКИ В ГОЛОВЕ", "ВЕДУТ В НИКУДА?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 2.73, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИЛИ РИСУНКОМ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.38, "lines": [{"text": "НО РИСУНОК", "accent": False, "size": "small"}, {"text": "ВЕЧЕРОМ НЕ НАШЕЛ", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 5.76, "lines": [{"text": "А СЛОВ", "accent": False, "size": "small"}, {"text": "НИКТО НЕ ЗАПИСАЛ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.44, "lines": [{"text": "ОСТАЛИСЬ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "СТРЕЛКИ В ГОЛОВЕ", "accent": True, "size": "big"}]},
    {"start": 7.68, "end": 8.61, "lines": [{"text": "И ОНИ ВЕДУТ", "accent": False, "size": "small"}, {"text": "В НИКУДА", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.25, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.90, "lines": [{"text": "В КОТОРОМ ВСЕ", "accent": False, "size": "small"}, {"text": "ЗАПИСАНО СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 13.17, "end": 14.05, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.05, "end": 15.084, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 6.75, "end": 7.02}, {"start": 8.40, "end": 8.61}, {"start": 12.09, "end": 12.45}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 15.362s): word-transfer rules for Russian EGE are
# only known vaguely because school dismissed them as "easy" and barely
# taught them -- exactly where points end up getting lost; the app's
# memory games test the easy rules too
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЛЕГКИЕ ПРАВИЛА", "ИМЕННО НА НИХ ТЕРЯЮТСЯ БАЛЛЫ?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 2.91, "lines": [{"text": "ПРАВИЛА ПЕРЕНОСА", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ ПО РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 3.18, "end": 4.77, "lines": [{"text": "ЗНАЮ СМУТНО", "accent": False, "size": "small"}, {"text": "В ШКОЛЕ СЧИТАЛИ ЛЕГКИМИ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.99, "lines": [{"text": "ЛЕГКОЕ УЧАТ", "accent": False, "size": "small"}, {"text": "МАЛО", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.58, "lines": [{"text": "ИМЕННО НА НЕМ", "accent": False, "size": "small"}, {"text": "ТЕРЯЮТСЯ БАЛЛЫ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 10.23, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.55, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 11.70, "end": 13.56, "lines": [{"text": "ГДЕ ПРОВЕРЯЮТСЯ", "accent": False, "size": "small"}, {"text": "И ЛЕГКИЕ ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 13.74, "end": 14.55, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 15.362, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.64, "end": 6.06}, {"start": 7.89, "end": 8.19}, {"start": 12.87, "end": 13.20}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 18.562s): a daughter can retell the news fluently
# but goes silent when asked to name the social-studies term from it --
# she knows the news, not yet the academic language to describe it; the
# app's memory games cement terms on short examples
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАЕТ НОВОСТИ", "НО НЕ ЗНАЕТ ТЕРМИН?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.18, "lines": [{"text": "ДОЧЬ ПЕРЕСКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "НОВОСТИ", "accent": True, "size": "big"}]},
    {"start": 3.42, "end": 5.16, "lines": [{"text": "НО СПРОСИ ТЕРМИН", "accent": False, "size": "small"}, {"text": "ИЗ НИХ ПО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.37, "end": 6.90, "lines": [{"text": "И ОНА", "accent": False, "size": "small"}, {"text": "МОЛЧИТ", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 9.54, "lines": [{"text": "НОВОСТИ ОНА ЗНАЕТ", "accent": False, "size": "small"}, {"text": "ЯЗЫК НАУКИ ПОКА НЕТ", "accent": True, "size": "big"}]},
    {"start": 11.04, "end": 12.57, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 12.75, "end": 13.92, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.10, "end": 16.20, "lines": [{"text": "ГДЕ ТЕРМИНЫ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТСЯ НА ПРИМЕРАХ", "accent": True, "size": "small"}]},
    {"start": 16.71, "end": 17.75, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.75, "end": 18.562, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.37, "end": 5.88}, {"start": 9.15, "end": 9.54}, {"start": 14.34, "end": 14.64}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (mother, 19.650s): "how did you solve it" gets a vague
# answer and the conversation ends there, until asked to write the
# first sentence of the solution in words -- and unexpectedly she opens
# up about her reasoning; the app's text breakdown gives a model to
# start the retelling from
# ---------------------------------------------------------------------------
e_intro = {"lines": ["КАК РЕШИЛА", "И РАЗГОВОР ЗАКОНЧИЛСЯ?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.27, "lines": [{"text": "ДОЧЬ НА ВОПРОС", "accent": False, "size": "small"}, {"text": "КАК РЕШИЛА", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 4.74, "lines": [{"text": "ОТВЕЧАЕТ", "accent": False, "size": "small"}, {"text": "НО Я ПОСЧИТАЛА", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 6.30, "lines": [{"text": "И РАЗГОВОР", "accent": False, "size": "small"}, {"text": "НА ЭТОМ ЗАКАНЧИВАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 6.81, "end": 8.19, "lines": [{"text": "Я ПОПРОСИЛА", "accent": False, "size": "small"}, {"text": "ЗАПИСАТЬ ПЕРВОЕ", "accent": True, "size": "big"}]},
    {"start": 8.28, "end": 9.66, "lines": [{"text": "ПРЕДЛОЖЕНИЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 11.76, "lines": [{"text": "И НЕОЖИДАННО", "accent": False, "size": "small"}, {"text": "ОНА ЗАГОВОРИЛА", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.53, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 13.71, "end": 14.67, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 16.92, "lines": [{"text": "ПО ОБРАЗЦУ КОТОРОГО", "accent": False, "size": "small"}, {"text": "ЛЕГКО НАЧАТЬ РАССКАЗ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 18.55, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.55, "end": 19.650, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.61, "end": 6.30}, {"start": 9.96, "end": 10.50}, {"start": 15.99, "end": 16.14}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 16.620s): fear that a task breakdown will be
# cluttered with extra stuff keeps it as a last resort, until it turns
# out the extra stuff is easy to skip once it's broken into clear
# steps; the app's text breakdown is exactly that -- steps you can skip
# or read
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РАЗБОР СЛИШКОМ", "МНОГО ЛИШНЕГО?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.45, "lines": [{"text": "БОЮСЬ ЧТО В РАЗБОРЕ", "accent": False, "size": "small"}, {"text": "БУДЕТ МНОГО ЛИШНЕГО", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 5.43, "lines": [{"text": "И ОТКРЫВАЮ ЕГО", "accent": False, "size": "small"}, {"text": "ТОЛЬКО В КРАЙНЕМ СЛУЧАЕ", "accent": True, "size": "big"}]},
    {"start": 5.76, "end": 7.47, "lines": [{"text": "ОКАЗАЛОСЬ ЧТО", "accent": False, "size": "small"}, {"text": "ЛИШНЕЕ ЛЕГКО ПРОПУСТИТЬ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 9.27, "lines": [{"text": "ЕСЛИ ОНО РАЗБИТО", "accent": False, "size": "small"}, {"text": "НА ПОНЯТНЫЕ ШАГИ", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 11.88, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 14.61, "lines": [{"text": "РАЗБИТЫЙ НА ШАГИ", "accent": False, "size": "small"}, {"text": "МОЖНО ПРОПУСТИТЬ ИЛИ ПРОЧИТАТЬ", "accent": True, "size": "big"}]},
    {"start": 14.85, "end": 15.78, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.78, "end": 16.620, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 3.18, "end": 3.45}, {"start": 7.11, "end": 7.47}, {"start": 12.12, "end": 12.45}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
