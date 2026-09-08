#!/usr/bin/env python3
"""One-off authoring + validation script for tag 'teatea1' (6 episodes).
Not a generic tool: hand-picked timings/text per episode. Run from
remotion/episodes43/.

This batch has two hosts sharing the release: a mom (v1_a, v2_b, v3_b,
talking about her son's prep) and a student (v1_b, v2_a, v3_a, talking
about her own prep). Hook wording is written per speaker.
"""
import json

REAL_DURATION = {
    "a": 28.80, "b": 32.17, "c": 30.14, "d": 27.29, "e": 30.23, "f": 27.67,
}
SOURCE_FILE = {
    "a": "v1_a", "b": "v1_b", "c": "v2_a",
    "d": "v2_b", "e": "v3_a", "f": "v3_b",
}
# Cosmetic ASR misrecognitions to fix before building the running caption
# (timings are correct, only the recognized word text is wrong).
WORD_FIXES = {
    "c": {(3.45, 3.48): "с"},
    "e": {(0.93, 1.02): "тему", (1.11, 1.14): "я"},
    "f": {(21.00, 21.09): "не"},
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


def build_running_caption(words, total_duration):
    groups = [{"text": w["text"].upper(), "start": w["start"]} for w in words]
    for idx in range(len(groups)):
        groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
    groups[0]["start"] = 0.0
    return groups


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_teatea1/{src}_words.json"))
    fixes = WORD_FIXES.get(letter, {})
    for w in words:
        key = (w["start"], w["end"])
        if key in fixes:
            w["text"] = fixes[key]
        w["start"] = min(w["start"], total_duration)
        w["end"] = min(w["end"], total_duration)

    check_intro_vs_cards(letter, intro["end"], cards)
    check_cards(letter, cards, total_duration)
    check_emphasis(letter, emphasis, total_duration)

    running_caption = build_running_caption(words, total_duration)

    json.dump(words, open(f"ep_{letter}_words.json", "w"), ensure_ascii=False, indent=2)
    json.dump(cards, open(f"ep_{letter}_cards.json", "w"), ensure_ascii=False, indent=2)
    json.dump(running_caption, open(f"ep_{letter}_running_caption.json", "w"), ensure_ascii=False, indent=2)
    json.dump({"total_duration": total_duration}, open(f"ep_{letter}_duration.json", "w"), indent=2)
    json.dump(intro, open(f"ep_{letter}_intro.json", "w"), ensure_ascii=False, indent=2)
    json.dump(emphasis, open(f"ep_{letter}_emphasis.json", "w"), ensure_ascii=False, indent=2)
    json.dump([], open(f"ep_{letter}_stock_cutaways.json", "w"))
    print(f"ep{letter}: OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode A (v1_a, mom): honest money talk with her son about prep budget
# ---------------------------------------------------------------------------
a_intro = {"lines": ["МОЛЧИШЬ О ДЕНЬГАХ", "НА ПОДГОТОВКУ?"], "end": 2.3}
a_cards = [
    {"start": 3.70, "end": 4.95, "lines": [
        {"text": "НАЧАЛА", "accent": False, "size": "small"},
        {"text": "ЧЕСТНО", "accent": True, "size": "big"},
    ]},
    {"start": 5.20, "end": 6.95, "lines": [
        {"text": "ВМЕСТО", "accent": False, "size": "small"},
        {"text": "МОЛЧАНИЯ", "accent": True, "size": "big"},
    ]},
    {"start": 7.10, "end": 8.98, "lines": [
        {"text": "О БЮДЖЕТЕ", "accent": False, "size": "small"},
        {"text": "СЕМЬИ", "accent": True, "size": "big"},
    ]},
    {"start": 9.30, "end": 11.85, "lines": [
        {"text": "СКОЛЬКО ГОТОВА", "accent": False, "size": "small"},
        {"text": "ПОТРАТИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 12.00, "end": 15.20, "lines": [
        {"text": "НАЧИНАЕМ", "accent": False, "size": "small"},
        {"text": "БЕСПЛАТНО", "accent": True, "size": "big"},
    ]},
    {"start": 15.65, "end": 18.10, "lines": [
        {"text": "РЕАКЦИЯ", "accent": False, "size": "small"},
        {"text": "ВЗРОСЛЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 18.35, "end": 19.80, "lines": [
        {"text": "ОЦЕНИЛА", "accent": False, "size": "small"},
        {"text": "ОТКРЫТОСТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 19.85, "end": 21.55, "lines": [
        {"text": "БОЛЬШЕ ЧЕМ ОБИДУ", "accent": False, "size": "small"},
        {"text": "НА ЗАПРЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 21.90, "end": 24.30, "lines": [
        {"text": "ПРОДОЛЖАЕМ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 24.40, "end": 26.40, "lines": [
        {"text": "ПОНИМАНИЕ", "accent": False, "size": "small"},
        {"text": "С ОБЕИХ СТОРОН", "accent": True, "size": "big"},
    ]},
    {"start": 26.80, "end": 28.80, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
a_emphasis = [
    {"start": 3.78, "end": 4.05},
    {"start": 11.34, "end": 11.73},
    {"start": 18.96, "end": 19.32},
]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (v1_b, student): picked a fixed number of attempts before
# switching strategy, instead of going by gut feeling
# ---------------------------------------------------------------------------
b_intro = {"lines": ["КОГДА МЕНЯТЬ", "СТРАТЕГИЮ?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 4.40, "lines": [
        {"text": "ПЕРЕД СМЕНОЙ", "accent": False, "size": "small"},
        {"text": "СТРАТЕГИИ", "accent": True, "size": "big"},
    ]},
    {"start": 4.90, "end": 7.65, "lines": [
        {"text": "ОПРЕДЕЛИЛА", "accent": False, "size": "small"},
        {"text": "ЧИСЛО", "accent": True, "size": "big"},
    ]},
    {"start": 8.30, "end": 10.55, "lines": [
        {"text": "А НЕ", "accent": False, "size": "small"},
        {"text": "ИНТУИЦИЕЙ", "accent": True, "size": "big"},
    ]},
    {"start": 11.45, "end": 12.65, "lines": [
        {"text": "ТРИ ВАРИАНТА", "accent": False, "size": "small"},
        {"text": "ПОДРЯД", "accent": True, "size": "big"},
    ]},
    {"start": 12.80, "end": 14.55, "lines": [
        {"text": "ОДИНАКОВЫЙ", "accent": False, "size": "small"},
        {"text": "РЕЗУЛЬТАТ", "accent": True, "size": "big"},
    ]},
    {"start": 14.85, "end": 16.05, "lines": [
        {"text": "СИГНАЛ", "accent": False, "size": "small"},
        {"text": "МЕНЯТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 16.45, "end": 17.85, "lines": [
        {"text": "НЕ ДВА", "accent": False, "size": "small"},
        {"text": "И НЕ ПЯТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 18.55, "end": 20.55, "lines": [
        {"text": "МЕНЬШЕ", "accent": False, "size": "small"},
        {"text": "СЛУЧАЙНО", "accent": True, "size": "big"},
    ]},
    {"start": 21.00, "end": 22.95, "lines": [
        {"text": "БОЛЬШЕ", "accent": False, "size": "small"},
        {"text": "ВПУСТУЮ", "accent": True, "size": "big"},
    ]},
    {"start": 23.15, "end": 24.85, "lines": [
        {"text": "ЯВНО", "accent": False, "size": "small"},
        {"text": "НЕ РАБОТАЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 25.85, "end": 28.25, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "СТАТИСТИКА", "accent": True, "size": "big"},
    ]},
    {"start": 28.40, "end": 29.85, "lines": [
        {"text": "ПО", "accent": False, "size": "small"},
        {"text": "ВАРИАНТАМ", "accent": True, "size": "big"},
    ]},
    {"start": 30.30, "end": 32.17, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
b_emphasis = [
    {"start": 3.30, "end": 3.69},
    {"start": 13.92, "end": 14.46},
    {"start": 22.47, "end": 22.86},
]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (v2_a, student): careless mistakes measurably decreasing week
# over week with practice
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТЕРЯЕШЬ БАЛЛЫ", "НА МЕЛОЧАХ?"], "end": 2.3}
c_cards = [
    {"start": 3.95, "end": 5.55, "lines": [
        {"text": "СРАВНИЛА", "accent": False, "size": "small"},
        {"text": "СТАТИСТИКУ", "accent": True, "size": "big"},
    ]},
    {"start": 5.65, "end": 7.90, "lines": [
        {"text": "ПЕРВАЯ И", "accent": False, "size": "small"},
        {"text": "ТЕКУЩАЯ НЕДЕЛЯ", "accent": True, "size": "big"},
    ]},
    {"start": 8.15, "end": 9.65, "lines": [
        {"text": "СПЕЦИАЛЬНО", "accent": False, "size": "small"},
        {"text": "НАБЛЮДЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 10.65, "end": 11.80, "lines": [
        {"text": "В НАЧАЛЕ", "accent": False, "size": "small"},
        {"text": "ТЕРЯЛАСЬ", "accent": True, "size": "big"},
    ]},
    {"start": 11.90, "end": 13.10, "lines": [
        {"text": "В МЕЛКИХ", "accent": False, "size": "small"},
        {"text": "ДЕТАЛЯХ", "accent": True, "size": "big"},
    ]},
    {"start": 13.50, "end": 15.30, "lines": [
        {"text": "КАЖДОЕ ТРЕТЬЕ", "accent": False, "size": "small"},
        {"text": "ЗАДАНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 16.35, "end": 18.30, "lines": [
        {"text": "СЕЙЧАС", "accent": False, "size": "small"},
        {"text": "РЕЖЕ", "accent": True, "size": "big"},
    ]},
    {"start": 19.75, "end": 22.15, "lines": [
        {"text": "БЕЗ", "accent": False, "size": "small"},
        {"text": "УСИЛИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 22.85, "end": 23.90, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 23.95, "end": 25.35, "lines": [
        {"text": "ПРОГРЕСС", "accent": False, "size": "small"},
        {"text": "ПО ФОКУСУ", "accent": True, "size": "big"},
    ]},
    {"start": 25.45, "end": 26.90, "lines": [
        {"text": "ВИДЕН", "accent": False, "size": "small"},
        {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"},
    ]},
    {"start": 28.20, "end": 30.14, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
c_emphasis = [
    {"start": 1.35, "end": 1.68},
    {"start": 17.16, "end": 17.64},
    {"start": 24.03, "end": 24.48},
]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (v2_b, mom): son now takes prep questions calmly, after she
# cut down how often she asks
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЛЮБОЙ ВОПРОС", "БЕСИТ СЫНА?"], "end": 2.3}
d_cards = [
    {"start": 2.40, "end": 4.50, "lines": [
        {"text": "СЫН", "accent": False, "size": "small"},
        {"text": "СПОКОЙНЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 5.55, "end": 6.90, "lines": [
        {"text": "ЕЩЁ МЕСЯЦ", "accent": False, "size": "small"},
        {"text": "НАЗАД", "accent": True, "size": "big"},
    ]},
    {"start": 6.95, "end": 8.90, "lines": [
        {"text": "ЛЮБОЙ ВОПРОС", "accent": False, "size": "small"},
        {"text": "РАЗДРАЖАЛ", "accent": True, "size": "big"},
    ]},
    {"start": 8.95, "end": 10.10, "lines": [
        {"text": "И", "accent": False, "size": "small"},
        {"text": "КОРОТКО", "accent": True, "size": "big"},
    ]},
    {"start": 10.50, "end": 11.55, "lines": [
        {"text": "РАЗНИЦА", "accent": False, "size": "small"},
        {"text": "ПОЯВИЛАСЬ", "accent": True, "size": "big"},
    ]},
    {"start": 11.60, "end": 14.20, "lines": [
        {"text": "ПЕРЕСТАЛА", "accent": False, "size": "small"},
        {"text": "СПРАШИВАТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 14.85, "end": 16.70, "lines": [
        {"text": "ПАРУ РАЗ", "accent": False, "size": "small"},
        {"text": "В НЕДЕЛЮ", "accent": True, "size": "big"},
    ]},
    {"start": 17.05, "end": 19.65, "lines": [
        {"text": "МЕНЬШЕ ВОПРОСОВ", "accent": False, "size": "small"},
        {"text": "БОЛЬШЕ ОТКРЫТОСТИ", "accent": True, "size": "big"},
    ]},
    {"start": 19.90, "end": 21.85, "lines": [
        {"text": "СТРАННО", "accent": False, "size": "small"},
        {"text": "НА ПЕРВЫЙ ВЗГЛЯД", "accent": True, "size": "big"},
    ]},
    {"start": 22.25, "end": 23.25, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 23.30, "end": 24.98, "lines": [
        {"text": "ОСТАЛЬНОЕ", "accent": False, "size": "small"},
        {"text": "СПОКОЙНО", "accent": True, "size": "big"},
    ]},
    {"start": 25.30, "end": 27.29, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
d_emphasis = [
    {"start": 3.48, "end": 4.38},
    {"start": 13.38, "end": 13.74},
    {"start": 18.69, "end": 19.08},
]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (v3_a, student): three self-defined criteria for calling a
# topic actually learned, checked every time in the app
# ---------------------------------------------------------------------------
e_intro = {"lines": ["КОГДА ТЕМА", "ДЕЙСТВИТЕЛЬНО ГОТОВА?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 3.70, "lines": [
        {"text": "ДЛЯ ПЕРЕХОДА", "accent": False, "size": "small"},
        {"text": "ДАЛЬШЕ", "accent": True, "size": "big"},
    ]},
    {"start": 3.95, "end": 5.00, "lines": [
        {"text": "ПО ТРЁМ", "accent": False, "size": "small"},
        {"text": "ПРИЗНАКАМ", "accent": True, "size": "big"},
    ]},
    {"start": 5.30, "end": 6.50, "lines": [
        {"text": "ВЫВЕЛА", "accent": False, "size": "small"},
        {"text": "ДЛЯ СЕБЯ", "accent": True, "size": "big"},
    ]},
    {"start": 6.55, "end": 8.10, "lines": [
        {"text": "МЕТОДОМ ПРОБ", "accent": False, "size": "small"},
        {"text": "ЗА ЭТО ВРЕМЯ", "accent": True, "size": "big"},
    ]},
    {"start": 9.05, "end": 10.65, "lines": [
        {"text": "РЕШАЯ", "accent": False, "size": "small"},
        {"text": "ЗАДАНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 10.85, "end": 12.60, "lines": [
        {"text": "БЕЗ ОШИБОК", "accent": False, "size": "small"},
        {"text": "ПЯТЬ РАЗ ПОДРЯД", "accent": True, "size": "big"},
    ]},
    {"start": 12.90, "end": 13.70, "lines": [
        {"text": "БЕЗ", "accent": False, "size": "small"},
        {"text": "ИСКЛЮЧЕНИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 14.20, "end": 16.10, "lines": [
        {"text": "МОГУ", "accent": False, "size": "small"},
        {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 16.30, "end": 17.80, "lines": [
        {"text": "БЕЗ КОНСПЕКТА", "accent": False, "size": "small"},
        {"text": "В ГОЛОВЕ", "accent": True, "size": "big"},
    ]},
    {"start": 18.00, "end": 20.90, "lines": [
        {"text": "ВООБЩЕ НЕ", "accent": False, "size": "small"},
        {"text": "ПУТАЮ", "accent": True, "size": "big"},
    ]},
    {"start": 21.10, "end": 22.95, "lines": [
        {"text": "ПРИ БЫСТРОМ", "accent": False, "size": "small"},
        {"text": "ТАЙМЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 23.50, "end": 24.50, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 24.70, "end": 27.35, "lines": [
        {"text": "ВСЕ ТРИ ПУНКТА", "accent": False, "size": "small"},
        {"text": "ПРОВЕРЯЮ", "accent": True, "size": "big"},
    ]},
    {"start": 28.40, "end": 30.23, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
e_emphasis = [
    {"start": 11.82, "end": 12.09},
    {"start": 14.58, "end": 14.97},
    {"start": 19.41, "end": 19.80},
]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (v3_b, mom): son suddenly sped up his pace this week, worried
# about burnout, turned out to just be absorbed in one topic
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СЫН ВДРУГ", "ЗАНИМАЕТСЯ БОЛЬШЕ?"], "end": 2.3}
f_cards = [
    {"start": 2.35, "end": 3.60, "lines": [
        {"text": "СЫН РЕЗКО", "accent": False, "size": "small"},
        {"text": "УСКОРИЛ", "accent": True, "size": "big"},
    ]},
    {"start": 3.75, "end": 5.00, "lines": [
        {"text": "БЕЗ ВИДИМОЙ", "accent": False, "size": "small"},
        {"text": "ПРИЧИНЫ", "accent": True, "size": "big"},
    ]},
    {"start": 5.60, "end": 7.45, "lines": [
        {"text": "ЗАНИМАЕТСЯ", "accent": False, "size": "small"},
        {"text": "ДОЛЬШЕ", "accent": True, "size": "big"},
    ]},
    {"start": 7.50, "end": 8.70, "lines": [
        {"text": "КАЖДЫЙ ВЕЧЕР", "accent": False, "size": "small"},
        {"text": "ПОДРЯД", "accent": True, "size": "big"},
    ]},
    {"start": 9.20, "end": 10.90, "lines": [
        {"text": "ПЕРВАЯ МЫСЛЬ", "accent": False, "size": "small"},
        {"text": "РАДОСТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 11.00, "end": 12.60, "lines": [
        {"text": "ВТОРАЯ", "accent": False, "size": "small"},
        {"text": "ТРЕВОГА", "accent": True, "size": "big"},
    ]},
    {"start": 12.80, "end": 14.50, "lines": [
        {"text": "СТРАХ", "accent": False, "size": "small"},
        {"text": "ВЫГОРАНИЯ", "accent": True, "size": "big"},
    ]},
    {"start": 14.60, "end": 16.35, "lines": [
        {"text": "РЫВОК ВПЕРЁД", "accent": False, "size": "small"},
        {"text": "ПОСМОТРЕЛА", "accent": True, "size": "big"},
    ]},
    {"start": 16.45, "end": 17.60, "lines": [
        {"text": "ВНИМАТЕЛЬНЕЕ", "accent": False, "size": "small"},
        {"text": "ПОНЯЛА", "accent": True, "size": "big"},
    ]},
    {"start": 17.90, "end": 19.65, "lines": [
        {"text": "ПРОСТО", "accent": False, "size": "small"},
        {"text": "УВЛЁКСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 19.75, "end": 20.60, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 20.90, "end": 22.80, "lines": [
        {"text": "НЕ ГОНИТСЯ", "accent": False, "size": "small"},
        {"text": "ЗА ЦИФРАМИ", "accent": True, "size": "big"},
    ]},
    {"start": 23.20, "end": 25.35, "lines": [
        {"text": "РАЗНЫЙ", "accent": False, "size": "small"},
        {"text": "МОТИВ", "accent": True, "size": "big"},
    ]},
    {"start": 25.70, "end": 27.67, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
f_emphasis = [
    {"start": 2.49, "end": 2.73},
    {"start": 12.90, "end": 13.53},
    {"start": 18.33, "end": 18.63},
]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
