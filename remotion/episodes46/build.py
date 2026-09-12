#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRD 'coffee123' batch
(6 more episodes uploaded under the same tag after the first two batches
were delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes46/.

Two returning hosts from the teatea1 batch: the amber-room student
(v1_a/b/c, self-perspective — targeted-practice / gap-analysis angle)
and the bookshelf mom (v2_a/b/c, son-perspective — checklist / pacing
angle).
"""
import json

REAL_DURATION = {
    "a": 33.84, "b": 31.404, "c": 29.25,
    "d": 26.69, "e": 29.612, "f": 26.604,
}
SOURCE_FILE = {
    "a": "v1_a", "b": "v1_b", "c": "v1_c",
    "d": "v2_a", "e": "v2_b", "f": "v2_c",
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
    words = json.load(open(f"../asr_coffee123_3/{src}_words.json"))
    for w in words:
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
# Episode A (v1_a, student): struggled for weeks with one task type losing
# points regularly; found targeted step-by-step practice in the app and
# finally spotted the pattern she'd been missing
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ОДНА И ТА ЖЕ", "ОШИБКА СНОВА?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 4.20, "lines": [
        {"text": "С ЗАДАНИЕМ", "accent": False, "size": "small"},
        {"text": "НА ВЫВОД", "accent": True, "size": "big"},
    ]},
    {"start": 4.30, "end": 6.60, "lines": [
        {"text": "ТЕРЯЛА", "accent": False, "size": "small"},
        {"text": "БАЛЛЫ", "accent": True, "size": "big"},
    ]},
    {"start": 7.10, "end": 8.05, "lines": [
        {"text": "ОБЫЧНЫЕ", "accent": False, "size": "small"},
        {"text": "СБОРНИКИ", "accent": True, "size": "big"},
    ]},
    {"start": 8.15, "end": 9.70, "lines": [
        {"text": "ОДНОЙ", "accent": False, "size": "small"},
        {"text": "СТРОКОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 10.10, "end": 12.25, "lines": [
        {"text": "БЕЗ РАЗБОРА", "accent": False, "size": "small"},
        {"text": "ЛОГИКИ", "accent": True, "size": "big"},
    ]},
    {"start": 13.00, "end": 13.90, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 14.15, "end": 15.45, "lines": [
        {"text": "НАШЛА", "accent": False, "size": "small"},
        {"text": "ПРАКТИКУ", "accent": True, "size": "big"},
    ]},
    {"start": 15.75, "end": 17.45, "lines": [
        {"text": "ИМЕННО НА", "accent": False, "size": "small"},
        {"text": "ЦЕПОЧКИ", "accent": True, "size": "big"},
    ]},
    {"start": 17.75, "end": 19.05, "lines": [
        {"text": "КАЖДЫЙ", "accent": False, "size": "small"},
        {"text": "ШАГ", "accent": True, "size": "big"},
    ]},
    {"start": 19.60, "end": 21.65, "lines": [
        {"text": "ПОДРЯД", "accent": False, "size": "small"},
        {"text": "НЕСКОЛЬКО", "accent": True, "size": "big"},
    ]},
    {"start": 21.80, "end": 22.90, "lines": [
        {"text": "НАКОНЕЦ", "accent": False, "size": "small"},
        {"text": "УВИДЕЛА", "accent": True, "size": "big"},
    ]},
    {"start": 22.90, "end": 24.95, "lines": [
        {"text": "КОТОРУЮ", "accent": False, "size": "small"},
        {"text": "УПУСКАЛА", "accent": True, "size": "big"},
    ]},
    {"start": 25.55, "end": 26.90, "lines": [
        {"text": "ДЛЯ", "accent": False, "size": "small"},
        {"text": "АМБИЦИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 27.20, "end": 29.05, "lines": [
        {"text": "УЗКИЕ ПРОБЕЛЫ", "accent": False, "size": "small"},
        {"text": "РЕШАЮТ", "accent": True, "size": "big"},
    ]},
    {"start": 29.35, "end": 31.50, "lines": [
        {"text": "ЧЕМ", "accent": False, "size": "small"},
        {"text": "ПОВТОРЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 32.00, "end": 33.84, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
a_emphasis = [
    {"start": 5.85, "end": 6.06},
    {"start": 22.92, "end": 23.55},
    {"start": 29.64, "end": 30.15},
]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (v1_b, student): found in the app a breakdown of a task type
# strong-student courses skip as "too easy" - exactly where she lost points
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЛЁГКОЕ ЗАДАНИЕ", "САМОЕ СЛАБОЕ МЕСТО?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 3.65, "lines": [
        {"text": "ОТДЕЛЬНЫЙ", "accent": False, "size": "small"},
        {"text": "РАЗБОР", "accent": True, "size": "big"},
    ]},
    {"start": 3.75, "end": 5.20, "lines": [
        {"text": "НА КУРСАХ", "accent": False, "size": "small"},
        {"text": "ДЛЯ СИЛЬНЫХ", "accent": True, "size": "big"},
    ]},
    {"start": 5.55, "end": 7.80, "lines": [
        {"text": "ПРОСТО", "accent": False, "size": "small"},
        {"text": "ПРОПУСКАЮТ", "accent": True, "size": "big"},
    ]},
    {"start": 8.40, "end": 10.20, "lines": [
        {"text": "НА ДЕЛЕ", "accent": False, "size": "small"},
        {"text": "ТЕРЯЛА", "accent": True, "size": "big"},
    ]},
    {"start": 11.15, "end": 12.95, "lines": [
        {"text": "В ДВУХ МЕСТАХ", "accent": False, "size": "small"},
        {"text": "РАЗНЫЕ", "accent": True, "size": "big"},
    ]},
    {"start": 13.80, "end": 14.85, "lines": [
        {"text": "РАЗБОР", "accent": False, "size": "small"},
        {"text": "ПРИЛОЖЕНИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 14.95, "end": 16.30, "lines": [
        {"text": "ПОКАЗАЛ", "accent": False, "size": "small"},
        {"text": "ПОШАГОВО", "accent": True, "size": "big"},
    ]},
    {"start": 16.60, "end": 18.25, "lines": [
        {"text": "НА КУРСАХ", "accent": False, "size": "small"},
        {"text": "БЕГЛО", "accent": True, "size": "big"},
    ]},
    {"start": 18.30, "end": 19.20, "lines": [
        {"text": "ОДНОЙ", "accent": False, "size": "small"},
        {"text": "ФРАЗОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 19.40, "end": 21.40, "lines": [
        {"text": "ПОДРЯД", "accent": False, "size": "small"},
        {"text": "ПЯТЬ ЗАДАНИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 21.65, "end": 23.40, "lines": [
        {"text": "ПЕРЕСТАЛА", "accent": False, "size": "small"},
        {"text": "ОШИБАТЬСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 24.85, "end": 26.50, "lines": [
        {"text": "ЛЁГКАЯ НА ВИД", "accent": False, "size": "small"},
        {"text": "ЗАДАЧА", "accent": True, "size": "big"},
    ]},
    {"start": 26.60, "end": 28.90, "lines": [
        {"text": "САМЫМ", "accent": False, "size": "small"},
        {"text": "СЛАБЫМ", "accent": True, "size": "big"},
    ]},
    {"start": 29.45, "end": 31.40, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
b_emphasis = [
    {"start": 5.91, "end": 6.39},
    {"start": 20.34, "end": 20.43},
    {"start": 27.72, "end": 27.96},
]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (v1_c, student): keeps a separate checklist of tasks "at the
# edge of her abilities" collected from the app over a month, one evening
# a week, adding/removing items as she improves
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЕСТЬ ЗАДАНИЯ", "НА ГРАНИ ВОЗМОЖНОСТЕЙ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 3.75, "lines": [
        {"text": "НА ГРАНИ", "accent": False, "size": "small"},
        {"text": "МОИХ СИЛ", "accent": True, "size": "big"},
    ]},
    {"start": 4.15, "end": 6.05, "lines": [
        {"text": "СОБРАННЫХ", "accent": False, "size": "small"},
        {"text": "ЗА МЕСЯЦ", "accent": True, "size": "big"},
    ]},
    {"start": 6.65, "end": 8.05, "lines": [
        {"text": "ОБЫЧНЫЕ ТЕМЫ", "accent": False, "size": "small"},
        {"text": "БЫСТРО", "accent": True, "size": "big"},
    ]},
    {"start": 8.30, "end": 9.25, "lines": [
        {"text": "А ЭТИ", "accent": False, "size": "small"},
        {"text": "ОТКЛАДЫВАЮ", "accent": True, "size": "big"},
    ]},
    {"start": 9.30, "end": 10.80, "lines": [
        {"text": "НА ОТДЕЛЬНЫЙ", "accent": False, "size": "small"},
        {"text": "ВЕЧЕР", "accent": True, "size": "big"},
    ]},
    {"start": 11.50, "end": 13.20, "lines": [
        {"text": "СЕЙЧАС", "accent": False, "size": "small"},
        {"text": "ТРИ ТИПА", "accent": True, "size": "big"},
    ]},
    {"start": 13.30, "end": 15.45, "lines": [
        {"text": "ОШИБАЮСЬ", "accent": False, "size": "small"},
        {"text": "ЧАЩЕ", "accent": True, "size": "big"},
    ]},
    {"start": 16.20, "end": 17.00, "lines": [
        {"text": "КАЖДУЮ", "accent": False, "size": "small"},
        {"text": "НЕДЕЛЮ", "accent": True, "size": "big"},
    ]},
    {"start": 17.05, "end": 18.85, "lines": [
        {"text": "ДОБАВЛЯЮ", "accent": False, "size": "small"},
        {"text": "ОДНО НОВОЕ", "accent": True, "size": "big"},
    ]},
    {"start": 19.20, "end": 21.45, "lines": [
        {"text": "УБИРАЮ", "accent": False, "size": "small"},
        {"text": "РЕШЁННОЕ", "accent": True, "size": "big"},
    ]},
    {"start": 22.10, "end": 23.40, "lines": [
        {"text": "НА ГРАНИ", "accent": False, "size": "small"},
        {"text": "СПИСОК", "accent": True, "size": "big"},
    ]},
    {"start": 23.55, "end": 25.00, "lines": [
        {"text": "РАСТЁТ", "accent": False, "size": "small"},
        {"text": "МЕДЛЕННЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 25.55, "end": 27.20, "lines": [
        {"text": "ЗАТО НАГЛЯДНО", "accent": False, "size": "small"},
        {"text": "ПРОГРЕСС", "accent": True, "size": "big"},
    ]},
    {"start": 27.60, "end": 29.25, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
c_emphasis = [
    {"start": 2.94, "end": 3.72},
    {"start": 13.56, "end": 13.92},
    {"start": 26.76, "end": 27.15},
]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (v2_a, mom): started a checklist of questions to ask her son
# about the topic instead of just checking the mock-exam grade
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СПРАШИВАЕШЬ ТОЛЬКО", "СКОЛЬКО БАЛЛОВ?"], "end": 2.3}
d_cards = [
    {"start": 2.60, "end": 3.50, "lines": [
        {"text": "ЗАДАЮ", "accent": False, "size": "small"},
        {"text": "СЫНУ", "accent": True, "size": "big"},
    ]},
    {"start": 3.60, "end": 4.40, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 4.75, "end": 6.60, "lines": [
        {"text": "НЕ ТОЛЬКО", "accent": False, "size": "small"},
        {"text": "НА ОЦЕНКУ", "accent": True, "size": "big"},
    ]},
    {"start": 7.05, "end": 8.00, "lines": [
        {"text": "РАНЬШЕ", "accent": False, "size": "small"},
        {"text": "СПРАШИВАЛА", "accent": True, "size": "big"},
    ]},
    {"start": 8.05, "end": 9.10, "lines": [
        {"text": "ТОЛЬКО", "accent": False, "size": "small"},
        {"text": "БАЛЛОВ", "accent": True, "size": "big"},
    ]},
    {"start": 9.15, "end": 10.75, "lines": [
        {"text": "РАЗГОВОР", "accent": False, "size": "small"},
        {"text": "КОНЧАЛСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 11.00, "end": 11.95, "lines": [
        {"text": "ТЕПЕРЬ", "accent": False, "size": "small"},
        {"text": "СПРАШИВАЮ", "accent": True, "size": "big"},
    ]},
    {"start": 12.05, "end": 14.40, "lines": [
        {"text": "КАКОЙ ШАГ", "accent": False, "size": "small"},
        {"text": "ТРУДНЫМ", "accent": True, "size": "big"},
    ]},
    {"start": 14.40, "end": 15.35, "lines": [
        {"text": "ИМЕННО", "accent": False, "size": "small"},
        {"text": "В ЭТОТ РАЗ", "accent": True, "size": "big"},
    ]},
    {"start": 15.85, "end": 17.70, "lines": [
        {"text": "НАЧАЛ", "accent": False, "size": "small"},
        {"text": "ОБЪЯСНЯТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 17.75, "end": 18.55, "lines": [
        {"text": "ЭТО", "accent": False, "size": "small"},
        {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 18.65, "end": 19.95, "lines": [
        {"text": "БОЛЬШЕ ЧЕМ", "accent": False, "size": "small"},
        {"text": "ОЦЕНКА", "accent": True, "size": "big"},
    ]},
    {"start": 20.45, "end": 21.75, "lines": [
        {"text": "ТРИ", "accent": False, "size": "small"},
        {"text": "ВОПРОСА", "accent": True, "size": "big"},
    ]},
    {"start": 21.85, "end": 22.80, "lines": [
        {"text": "РАБОТАЕТ", "accent": False, "size": "small"},
        {"text": "ТОЧНЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 22.80, "end": 24.45, "lines": [
        {"text": "ЧЕМ ВЗГЛЯД", "accent": False, "size": "small"},
        {"text": "НА БАЛЛ", "accent": True, "size": "big"},
    ]},
    {"start": 24.90, "end": 26.69, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
d_emphasis = [
    {"start": 8.43, "end": 9.06},
    {"start": 14.04, "end": 14.31},
    {"start": 22.44, "end": 22.71},
]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (v2_b, mom): son explained a task from the app to her himself,
# unprompted, in more detail than he ever showed before
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СЫН ОБЪЯСНЯЕТ", "САМ БЕЗ ПРОСЬБЫ?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 3.60, "lines": [
        {"text": "ИЗ ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРА", "accent": True, "size": "big"},
    ]},
    {"start": 3.85, "end": 5.35, "lines": [
        {"text": "Я ПОНЯЛА", "accent": False, "size": "small"},
        {"text": "РАЗОБРАЛСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 5.40, "end": 6.80, "lines": [
        {"text": "ЛУЧШЕ ЧЕМ", "accent": False, "size": "small"},
        {"text": "РАНЬШЕ", "accent": True, "size": "big"},
    ]},
    {"start": 7.40, "end": 9.00, "lines": [
        {"text": "ОБЫЧНО НА", "accent": False, "size": "small"},
        {"text": "ВОПРОСЫ", "accent": True, "size": "big"},
    ]},
    {"start": 9.05, "end": 9.95, "lines": [
        {"text": "ОТВЕЧАЛ", "accent": False, "size": "small"},
        {"text": "КОРОТКО", "accent": True, "size": "big"},
    ]},
    {"start": 9.95, "end": 10.75, "lines": [
        {"text": "БЕЗ", "accent": False, "size": "small"},
        {"text": "ДЕТАЛЕЙ", "accent": True, "size": "big"},
    ]},
    {"start": 10.85, "end": 11.95, "lines": [
        {"text": "ПОЧТИ БЕЗ", "accent": False, "size": "small"},
        {"text": "ИНТЕРЕСА", "accent": True, "size": "big"},
    ]},
    {"start": 12.35, "end": 13.30, "lines": [
        {"text": "В ЭТОТ", "accent": False, "size": "small"},
        {"text": "РАЗ", "accent": True, "size": "big"},
    ]},
    {"start": 13.30, "end": 14.10, "lines": [
        {"text": "ДОСТАЛ", "accent": False, "size": "small"},
        {"text": "ТЕЛЕФОН", "accent": True, "size": "big"},
    ]},
    {"start": 14.25, "end": 15.10, "lines": [
        {"text": "СТАЛ", "accent": False, "size": "small"},
        {"text": "ПОКАЗЫВАТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 15.10, "end": 17.15, "lines": [
        {"text": "КАК РЕШАЕТСЯ", "accent": False, "size": "small"},
        {"text": "ЗАДАНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 17.75, "end": 18.98, "lines": [
        {"text": "СЛУШАЛА", "accent": False, "size": "small"},
        {"text": "НЕ УЗНАВАЛА", "accent": True, "size": "big"},
    ]},
    {"start": 19.00, "end": 19.95, "lines": [
        {"text": "ПРЕЖНЮЮ", "accent": False, "size": "small"},
        {"text": "НЕОХОТУ", "accent": True, "size": "big"},
    ]},
    {"start": 20.15, "end": 21.50, "lines": [
        {"text": "РАНЬШЕ САДИЛСЯ", "accent": False, "size": "small"},
        {"text": "ЗА УРОКИ", "accent": True, "size": "big"},
    ]},
    {"start": 22.50, "end": 24.35, "lines": [
        {"text": "ЛУЧШИЙ", "accent": False, "size": "small"},
        {"text": "ПОКАЗАТЕЛЬ", "accent": True, "size": "big"},
    ]},
    {"start": 24.55, "end": 26.40, "lines": [
        {"text": "КОГДА САМ", "accent": False, "size": "small"},
        {"text": "ХОЧЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 26.50, "end": 27.35, "lines": [
        {"text": "ТЕМУ", "accent": False, "size": "small"},
        {"text": "РОДИТЕЛЯМ", "accent": True, "size": "big"},
    ]},
    {"start": 27.75, "end": 29.60, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
e_emphasis = [
    {"start": 4.86, "end": 5.28},
    {"start": 14.64, "end": 15.06},
    {"start": 25.77, "end": 25.89},
]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (v2_c, mom): compared a school video-lesson vs the app at home -
# the app lets her son pause and rewatch a step until it clicks
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ОДИН ТЕМП", "НА ВЕСЬ КЛАСС?"], "end": 2.3}
f_cards = [
    {"start": 2.60, "end": 4.75, "lines": [
        {"text": "СЛОЖНАЯ ТЕМА", "accent": False, "size": "small"},
        {"text": "НА ВИДЕО", "accent": True, "size": "big"},
    ]},
    {"start": 5.15, "end": 6.50, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 6.95, "end": 9.20, "lines": [
        {"text": "УЧИТЕЛЬ ЗА УРОК", "accent": False, "size": "small"},
        {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"},
    ]},
    {"start": 9.55, "end": 11.40, "lines": [
        {"text": "НЕ РАЗБИРАЯ", "accent": False, "size": "small"},
        {"text": "ВОПРОСЫ", "accent": True, "size": "big"},
    ]},
    {"start": 11.90, "end": 14.60, "lines": [
        {"text": "ТА ЖЕ ТЕМА", "accent": False, "size": "small"},
        {"text": "ПО ШАГАМ", "accent": True, "size": "big"},
    ]},
    {"start": 14.90, "end": 16.90, "lines": [
        {"text": "МОЖНО ВЗЯТЬ", "accent": False, "size": "small"},
        {"text": "ПАУЗУ", "accent": True, "size": "big"},
    ]},
    {"start": 17.40, "end": 18.75, "lines": [
        {"text": "ПЕРЕСМОТРЕЛ", "accent": False, "size": "small"},
        {"text": "МОМЕНТ", "accent": True, "size": "big"},
    ]},
    {"start": 18.85, "end": 20.90, "lines": [
        {"text": "ТРИЖДЫ", "accent": False, "size": "small"},
        {"text": "ПРЕЖДЕ ЧЕМ", "accent": True, "size": "big"},
    ]},
    {"start": 21.35, "end": 22.25, "lines": [
        {"text": "ТАКОЙ ТЕМП", "accent": False, "size": "small"},
        {"text": "ЕМУ", "accent": True, "size": "big"},
    ]},
    {"start": 22.30, "end": 24.40, "lines": [
        {"text": "ЛУЧШЕ ЧЕМ", "accent": False, "size": "small"},
        {"text": "ОБЩИЙ ТЕМП", "accent": True, "size": "big"},
    ]},
    {"start": 24.85, "end": 26.60, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
f_emphasis = [
    {"start": 8.58, "end": 9.18},
    {"start": 18.90, "end": 19.14},
    {"start": 22.59, "end": 22.77},
]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
