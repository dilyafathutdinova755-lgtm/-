#!/usr/bin/env python3
"""One-off authoring + validation script for tag 'ИИНт' (6 episodes).
Not a generic tool: hand-picked timings/text per episode. Run from
remotion/episodes41/.
"""
import json

REAL_DURATION = {1: 38.60, 2: 37.88, 3: 37.56, 4: 31.16, 5: 31.08, 6: 28.84}


def check_cards(ep, cards, total_duration):
    prev_end = 0.0
    for i, c in enumerate(cards):
        assert c["start"] < c["end"], f"ep{ep} card{i}: start>=end"
        assert c["start"] >= prev_end - 1e-6, f"ep{ep} card{i}: overlaps previous (start {c['start']} < prev_end {prev_end})"
        dur = c["end"] - c["start"]
        assert dur <= 4.0 + 1e-6, f"ep{ep} card{i}: duration {dur:.2f}s > 4s"
        assert dur >= 0.8, f"ep{ep} card{i}: duration {dur:.2f}s < 0.8s (too short)"
        n_accent = sum(1 for l in c["lines"] for l in [l] if l.get("accent"))
        assert n_accent >= 1, f"ep{ep} card{i}: no accent line"
        for l in c["lines"]:
            assert "?" not in l["text"] or l["text"].endswith("?"), f"ep{ep} card{i}: bad '?' placement"
            assert "," not in l["text"] and "." not in l["text"] and "-" not in l["text"], f"ep{ep} card{i}: punctuation not allowed: {l['text']}"
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


def check_stock(ep, stock, total_duration, clip_lengths):
    for s in stock:
        assert s["start"] > 0.5, f"ep{ep}: stock cutaway too close to start"
        assert s["end"] < total_duration - 0.5, f"ep{ep}: stock cutaway too close to end"
        src_start = s.get("sourceStart", 0)
        dur = s["end"] - s["start"]
        clip_len = clip_lengths[s["file"]]
        assert src_start + dur <= clip_len - 0.1, (
            f"ep{ep}: stock {s['file']} sourceStart {src_start} + dur {dur:.2f} "
            f"exceeds clip length {clip_len} (need margin)"
        )


def build_running_caption(words, total_duration):
    groups = [{"text": w["text"].upper(), "start": w["start"]} for w in words]
    for idx in range(len(groups)):
        groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
    groups[0]["start"] = 0.0
    return groups


CLIP_LENGTHS = {
    "stock/stock_desk_window.mp4": 10.1,
    "stock/stock_writing_1.mp4": 7.0,
    "stock/stock_writing_2.mp4": 6.3,
    "stock/stock_girl_student_1.mp4": 7.9,
    "stock/stock_girl_student_2.mp4": 7.3,
    "stock/stock_home_evening.mp4": 26.4,
    "stock/stock_home_night.mp4": 14.8,
}


def process(ep, cards, intro, emphasis, stock):
    total_duration = REAL_DURATION[ep]
    words = json.load(open(f"../asr_iint/words{ep}_fixed.json"))
    for w in words:
        w["start"] = min(w["start"], total_duration)
        w["end"] = min(w["end"], total_duration)

    check_intro_vs_cards(ep, intro["end"], cards)
    check_cards(ep, cards, total_duration)
    check_emphasis(ep, emphasis, total_duration)
    check_stock(ep, stock, total_duration, CLIP_LENGTHS)

    running_caption = build_running_caption(words, total_duration)

    letter = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}[ep]
    json.dump(words, open(f"ep_{letter}_words.json", "w"), ensure_ascii=False, indent=2)
    json.dump(cards, open(f"ep_{letter}_cards.json", "w"), ensure_ascii=False, indent=2)
    json.dump(running_caption, open(f"ep_{letter}_running_caption.json", "w"), ensure_ascii=False, indent=2)
    json.dump({"total_duration": total_duration}, open(f"ep_{letter}_duration.json", "w"), indent=2)
    json.dump(intro, open(f"ep_{letter}_intro.json", "w"), ensure_ascii=False, indent=2)
    json.dump(emphasis, open(f"ep_{letter}_emphasis.json", "w"), ensure_ascii=False, indent=2)
    json.dump(stock, open(f"ep_{letter}_stock_cutaways.json", "w"), ensure_ascii=False, indent=2)
    print(f"ep{ep} ({letter}): OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode 1 (clip1): advanced ЕГЭ checklist for those past basics
# ---------------------------------------------------------------------------
ep1_intro = {"lines": ["БАЗУ УЖЕ", "ЗАКРЫЛ?"], "end": 2.3}
ep1_cards = [
    {"start": 6.55, "end": 9.55, "lines": [
        {"text": "ИЩЕШЬ НЕ МОТИВАЦИЮ", "accent": False, "size": "small"},
        {"text": "КОНКРЕТИКУ", "accent": True, "size": "big"},
    ]},
    {"start": 10.45, "end": 12.70, "lines": [
        {"text": "ЗАСЕКАЙ ВРЕМЯ", "accent": False, "size": "small"},
        {"text": "НА КАЖДОЕ ЗАДАНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 12.80, "end": 16.00, "lines": [
        {"text": "НЕ ТОЛЬКО ИТОГ", "accent": False, "size": "small"},
        {"text": "А КАЖДЫЙ ПРОБНИК", "accent": True, "size": "big"},
    ]},
    {"start": 16.85, "end": 19.35, "lines": [
        {"text": "ПОВТОРЯЮЩИХСЯ", "accent": False, "size": "small"},
        {"text": "ОШИБОК", "accent": True, "size": "big"},
    ]},
    {"start": 19.45, "end": 22.80, "lines": [
        {"text": "И СПИСОК НОВЫХ ТЕМ", "accent": False, "size": "small"},
        {"text": "ЭТО РАЗНОЕ", "accent": True, "size": "big"},
    ]},
    {"start": 23.65, "end": 27.10, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "ПОЛНЫЙ ПРОБНИК", "accent": True, "size": "big"},
    ]},
    {"start": 27.95, "end": 29.60, "lines": [
        {"text": "А НЕ ТЕМЫ", "accent": False, "size": "small"},
        {"text": "ВРАЗБРОС", "accent": True, "size": "big"},
    ]},
    {"start": 30.45, "end": 32.60, "lines": [
        {"text": "ДЛЯ ТЕХ КТО", "accent": False, "size": "small"},
        {"text": "ВЫШЕ СРЕДНЕГО", "accent": True, "size": "big"},
    ]},
    {"start": 32.85, "end": 35.80, "lines": [
        {"text": "ЭКОНОМИЯ ВРЕМЕНИ", "accent": False, "size": "small"},
        {"text": "ВАЖНЕЕ МОТИВАЦИИ", "accent": True, "size": "big"},
    ]},
    {"start": 36.35, "end": 38.60, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep1_emphasis = [
    {"start": 8.76, "end": 9.36},
    {"start": 27.15, "end": 27.48},
    {"start": 32.04, "end": 32.43},
]
ep1_stock = [
    {"start": 17.15, "end": 22.90, "file": "stock/stock_desk_window.mp4", "sourceStart": 0.5},
]
process(1, ep1_cards, ep1_intro, ep1_emphasis, ep1_stock)

# ---------------------------------------------------------------------------
# Episode 2 (clip2): hidden domain restriction in profile math
# ---------------------------------------------------------------------------
ep2_intro = {"lines": ["ТЕРЯЕШЬ БАЛЛЫ", "НА РОВНОМ МЕСТЕ?"], "end": 2.4}
ep2_cards = [
    {"start": 3.95, "end": 6.10, "lines": [
        {"text": "В ШКОЛЕ", "accent": False, "size": "small"},
        {"text": "ОБЪЯСНЯЮТ БЕГЛО", "accent": True, "size": "big"},
    ]},
    {"start": 6.20, "end": 8.35, "lines": [
        {"text": "А НА ЭКЗАМЕНЕ", "accent": False, "size": "small"},
        {"text": "ТЕРЯЮТ БАЛЛЫ", "accent": True, "size": "big"},
    ]},
    {"start": 8.45, "end": 10.00, "lines": [
        {"text": "ДАЖЕ", "accent": False, "size": "small"},
        {"text": "СИЛЬНЫЕ УЧЕНИКИ", "accent": True, "size": "big"},
    ]},
    {"start": 11.20, "end": 14.30, "lines": [
        {"text": "СКРЫТАЯ", "accent": False, "size": "small"},
        {"text": "ЛОВУШКА", "accent": True, "size": "big"},
    ]},
    {"start": 14.60, "end": 17.20, "lines": [
        {"text": "ЛЕГКО УПУСТИТЬ", "accent": False, "size": "small"},
        {"text": "ПРИ БЫСТРОМ ЧТЕНИИ", "accent": True, "size": "big"},
    ]},
    {"start": 17.80, "end": 19.80, "lines": [
        {"text": "ПОД ДАВЛЕНИЕМ", "accent": False, "size": "small"},
        {"text": "ВРЕМЕНИ", "accent": True, "size": "big"},
    ]},
    {"start": 20.70, "end": 23.20, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "ЕСТЬ ИГРА", "accent": True, "size": "big"},
    ]},
    {"start": 23.35, "end": 25.75, "lines": [
        {"text": "НА ТАКИЕ", "accent": False, "size": "small"},
        {"text": "ЛОВУШКИ", "accent": True, "size": "big"},
    ]},
    {"start": 26.00, "end": 29.50, "lines": [
        {"text": "ЗАМЕЧАТЬ РАНЬШЕ", "accent": False, "size": "small"},
        {"text": "ЧЕМ РЕШАТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 30.30, "end": 32.30, "lines": [
        {"text": "Я САМА", "accent": False, "size": "small"},
        {"text": "ТЕРЯЛА БАЛЛЫ", "accent": True, "size": "big"},
    ]},
    {"start": 32.40, "end": 35.25, "lines": [
        {"text": "ПОКА НЕ ПРОШЛА", "accent": False, "size": "small"},
        {"text": "СПЕЦИАЛЬНО", "accent": True, "size": "big"},
    ]},
    {"start": 35.90, "end": 37.88, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep2_emphasis = [
    {"start": 12.69, "end": 13.32},
    {"start": 19.29, "end": 19.62},
    {"start": 30.96, "end": 31.20},
]
ep2_stock = [
    {"start": 11.50, "end": 15.60, "file": "stock/stock_writing_1.mp4", "sourceStart": 0.0},
]
process(2, ep2_cards, ep2_intro, ep2_emphasis, ep2_stock)

# ---------------------------------------------------------------------------
# Episode 3 (clip3): optimizing an existing prep schedule
# ---------------------------------------------------------------------------
ep3_intro = {"lines": ["РАСПИСАНИЕ ЕСТЬ", "А РЕЗУЛЬТАТА НЕТ?"], "end": 2.4}
ep3_cards = [
    {"start": 3.35, "end": 5.20, "lines": [
        {"text": "ЕСЛИ ВРЕМЯ", "accent": False, "size": "small"},
        {"text": "УЖЕ ЗАНЯТО", "accent": True, "size": "big"},
    ]},
    {"start": 5.30, "end": 8.35, "lines": [
        {"text": "НО ХОЧЕШЬ", "accent": False, "size": "small"},
        {"text": "ВЫЖАТЬ БОЛЬШЕ", "accent": True, "size": "big"},
    ]},
    {"start": 8.95, "end": 12.70, "lines": [
        {"text": "ОДНА ТЕМА", "accent": False, "size": "small"},
        {"text": "ОДИН ИСТОЧНИК", "accent": True, "size": "big"},
    ]},
    {"start": 12.85, "end": 15.30, "lines": [
        {"text": "ДВА УЧЕБНИКА", "accent": False, "size": "small"},
        {"text": "ОБЪЯСНЯЮТ ОДНО", "accent": True, "size": "big"},
    ]},
    {"start": 16.05, "end": 17.00, "lines": [
        {"text": "ОСТАВЬ", "accent": False, "size": "small"},
        {"text": "ОДИН", "accent": True, "size": "big"},
    ]},
    {"start": 17.75, "end": 20.15, "lines": [
        {"text": "ГРУППИРУЙ ПОХОЖИЕ", "accent": False, "size": "small"},
        {"text": "ПО ФОРМАТУ", "accent": True, "size": "big"},
    ]},
    {"start": 20.20, "end": 22.80, "lines": [
        {"text": "ПОДРЯД", "accent": False, "size": "small"},
        {"text": "А НЕ ВРАЗБРОС", "accent": True, "size": "big"},
    ]},
    {"start": 23.55, "end": 25.75, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "УСТРОЕНО РОВНО ТАК", "accent": True, "size": "big"},
    ]},
    {"start": 26.55, "end": 28.35, "lines": [
        {"text": "АКТИВНОЕ ЗАКРЕПЛЕНИЕ", "accent": False, "size": "small"},
        {"text": "А НЕ ПОВТОР", "accent": True, "size": "big"},
    ]},
    {"start": 29.95, "end": 32.35, "lines": [
        {"text": "ОПТИМИЗАЦИЯ", "accent": False, "size": "small"},
        {"text": "НЕ ПРО ЧАСЫ", "accent": True, "size": "big"},
    ]},
    {"start": 32.65, "end": 35.10, "lines": [
        {"text": "А ПРО МЕНЬШЕ", "accent": False, "size": "small"},
        {"text": "ПОТЕРЬ ВРЕМЕНИ", "accent": True, "size": "big"},
    ]},
    {"start": 35.50, "end": 37.56, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep3_emphasis = [
    {"start": 15.09, "end": 15.63},
    {"start": 30.09, "end": 30.66},
    {"start": 34.11, "end": 34.47},
]
ep3_stock = [
    {"start": 18.05, "end": 22.80, "file": "stock/stock_writing_2.mp4", "sourceStart": 0.0},
]
process(3, ep3_cards, ep3_intro, ep3_emphasis, ep3_stock)

# ---------------------------------------------------------------------------
# Episode 4 (clip4): opened app randomly, month later mock-exam bet
# ---------------------------------------------------------------------------
ep4_intro = {"lines": ["НЕТ ПЛАНА", "ПОДГОТОВКИ?"], "end": 2.3}
ep4_cards = [
    {"start": 2.35, "end": 4.50, "lines": [
        {"text": "СЛУЧАЙНО ОТ СКУКИ", "accent": False, "size": "small"},
        {"text": "В ОЧЕРЕДИ К ВРАЧУ", "accent": True, "size": "big"},
    ]},
    {"start": 4.60, "end": 7.15, "lines": [
        {"text": "БЕЗ ПЛАНА", "accent": False, "size": "small"},
        {"text": "ДОКАЗАТЬ СЕБЕ", "accent": True, "size": "big"},
    ]},
    {"start": 7.20, "end": 10.00, "lines": [
        {"text": "ТО В ОЧЕРЕДИ", "accent": False, "size": "small"},
        {"text": "ТО ПЕРЕД СНОМ", "accent": True, "size": "big"},
    ]},
    {"start": 10.05, "end": 11.20, "lines": [
        {"text": "ВМЕСТО ЛЕНТЫ", "accent": True, "size": "big"},
    ]},
    {"start": 11.25, "end": 13.70, "lines": [
        {"text": "БЕЗ РАСПИСАНИЯ", "accent": False, "size": "small"},
        {"text": "И ОБЕЩАНИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 13.85, "end": 16.20, "lines": [
        {"text": "ОДНОКЛАССНИК ПРЕДЛОЖИЛ", "accent": False, "size": "small"},
        {"text": "ПРОБНИК", "accent": True, "size": "big"},
    ]},
    {"start": 16.30, "end": 18.80, "lines": [
        {"text": "РАДИ СПОРА", "accent": False, "size": "small"},
        {"text": "БЕЗ ПОДГОТОВКИ", "accent": True, "size": "big"},
    ]},
    {"start": 19.00, "end": 20.55, "lines": [
        {"text": "ОБА", "accent": False, "size": "small"},
        {"text": "ОФИГЕЛИ ОДИНАКОВО", "accent": True, "size": "big"},
    ]},
    {"start": 20.60, "end": 21.65, "lines": [
        {"text": "ОН", "accent": False, "size": "small"},
        {"text": "ОТ ПРОИГРЫША", "accent": True, "size": "big"},
    ]},
    {"start": 21.70, "end": 24.45, "lines": [
        {"text": "А Я", "accent": False, "size": "small"},
        {"text": "ЗАХОДЫ ПОВЛИЯЛИ", "accent": True, "size": "big"},
    ]},
    {"start": 24.55, "end": 25.68, "lines": [
        {"text": "НИКАКОГО СЕКРЕТА", "accent": True, "size": "big"},
    ]},
    {"start": 25.75, "end": 29.28, "lines": [
        {"text": "ЧАСТЫЕ И КОРОТКИЕ", "accent": False, "size": "small"},
        {"text": "ВМЕСТО МАРАФОНА", "accent": True, "size": "big"},
    ]},
    {"start": 29.35, "end": 31.16, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep4_emphasis = [
    {"start": 15.12, "end": 15.42},
    {"start": 19.35, "end": 19.65},
    {"start": 23.91, "end": 24.30},
]
ep4_stock = []
process(4, ep4_cards, ep4_intro, ep4_emphasis, ep4_stock)

# ---------------------------------------------------------------------------
# Episode 5 (clip5): opened app for fun, geography topic, decent result
# ---------------------------------------------------------------------------
ep5_intro = {"lines": ["ДРУГ ЗАДОЛБАЛ", "СКРИНАМИ?"], "end": 2.3}
ep5_cards = [
    {"start": 2.35, "end": 4.65, "lines": [
        {"text": "ОДНОКЛАССНИК", "accent": False, "size": "small"},
        {"text": "ЗАДОЛБАЛ СКРИНАМИ", "accent": True, "size": "big"},
    ]},
    {"start": 4.70, "end": 6.85, "lines": [
        {"text": "ПРОГРЕССА", "accent": False, "size": "small"},
        {"text": "КАЖДЫЙ ДЕНЬ В ЧАТЕ", "accent": True, "size": "big"},
    ]},
    {"start": 6.90, "end": 8.65, "lines": [
        {"text": "ОЖИДАЛ", "accent": False, "size": "small"},
        {"text": "СКУЧНЫЙ СПИСОК ПРАВИЛ", "accent": True, "size": "big"},
    ]},
    {"start": 8.70, "end": 10.75, "lines": [
        {"text": "НАШЁЛ ИГРУ", "accent": False, "size": "small"},
        {"text": "УГАДАЙ ЗАДАНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 10.85, "end": 13.05, "lines": [
        {"text": "БЫСТРЕЕ ЧЕМ", "accent": False, "size": "small"},
        {"text": "ЧИТАЕШЬ ЦЕЛИКОМ", "accent": True, "size": "big"},
    ]},
    {"start": 13.15, "end": 15.30, "lines": [
        {"text": "ТЕМА ПО ГЕОГРАФИИ", "accent": False, "size": "small"},
        {"text": "РАДИ ИНТЕРЕСА", "accent": True, "size": "big"},
    ]},
    {"start": 15.85, "end": 18.00, "lines": [
        {"text": "БЕЗ ЦЕЛИ", "accent": False, "size": "small"},
        {"text": "ГОТОВИТЬСЯ СЕРЬЁЗНО", "accent": True, "size": "big"},
    ]},
    {"start": 18.05, "end": 20.00, "lines": [
        {"text": "РЕЗУЛЬТАТ", "accent": False, "size": "small"},
        {"text": "НЕОЖИДАННО ПРИЛИЧНЫЙ", "accent": True, "size": "big"},
    ]},
    {"start": 20.40, "end": 23.30, "lines": [
        {"text": "НЕ ОТКРЫВАЛ УЧЕБНИК", "accent": False, "size": "small"},
        {"text": "С ДЕСЯТОГО КЛАССА", "accent": True, "size": "big"},
    ]},
    {"start": 23.40, "end": 24.60, "lines": [
        {"text": "ТРОЕЧНИК Я", "accent": False, "size": "small"},
        {"text": "ИЛИ НЕТ?", "accent": True, "size": "big"},
    ]},
    {"start": 24.65, "end": 26.25, "lines": [
        {"text": "ФОРМАТ ОКАЗАЛСЯ", "accent": False, "size": "small"},
        {"text": "НЕСКУЧНЫМ", "accent": True, "size": "big"},
    ]},
    {"start": 26.30, "end": 29.15, "lines": [
        {"text": "РЕДКОСТЬ ДЛЯ ВСЕГО", "accent": False, "size": "small"},
        {"text": "СО СЛОВОМ ЭКЗАМЕН", "accent": True, "size": "big"},
    ]},
    {"start": 29.20, "end": 31.08, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep5_emphasis = [
    {"start": 3.42, "end": 3.69},
    {"start": 19.44, "end": 19.86},
    {"start": 23.52, "end": 23.91},
]
ep5_stock = [
    {"start": 13.45, "end": 18.00, "file": "stock/stock_writing_2.mp4", "sourceStart": 0.0},
]
process(5, ep5_cards, ep5_intro, ep5_emphasis, ep5_stock)

# ---------------------------------------------------------------------------
# Episode 6 (clip6): friend wants a table, narrator prefers app progress
# ---------------------------------------------------------------------------
ep6_intro = {"lines": ["НУЖЕН ПЛАН", "С ТАБЛИЦЕЙ?"], "end": 2.3}
ep6_cards = [
    {"start": 3.50, "end": 5.40, "lines": [
        {"text": "ДРУГ ХОЧЕТ", "accent": False, "size": "small"},
        {"text": "ТАБЛИЦУ И ЧАСЫ", "accent": True, "size": "big"},
    ]},
    {"start": 5.45, "end": 8.25, "lines": [
        {"text": "А У МЕНЯ", "accent": False, "size": "small"},
        {"text": "ТОЛЬКО СКРИНШОТ", "accent": True, "size": "big"},
    ]},
    {"start": 8.40, "end": 10.55, "lines": [
        {"text": "ОТКРЫВАЮ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 10.65, "end": 12.15, "lines": [
        {"text": "ТЕМЫ", "accent": False, "size": "small"},
        {"text": "ЗЕЛЁНЫМ ЦВЕТОМ", "accent": True, "size": "big"},
    ]},
    {"start": 12.25, "end": 14.50, "lines": [
        {"text": "ПЛАН ЭТО И ЕСТЬ", "accent": False, "size": "small"},
        {"text": "ОТКРЫВАТЬ ЕГО", "accent": True, "size": "big"},
    ]},
    {"start": 14.55, "end": 15.40, "lines": [
        {"text": "МЕЖДУ ДЕЛОМ", "accent": True, "size": "big"},
    ]},
    {"start": 15.65, "end": 17.75, "lines": [
        {"text": "ОН НЕ ВПЕЧАТЛЁН", "accent": False, "size": "small"},
        {"text": "БЕЗ ТАБЛИЦЫ", "accent": True, "size": "big"},
    ]},
    {"start": 18.00, "end": 21.00, "lines": [
        {"text": "НЕ БУДУ ЗАВОДИТЬ", "accent": False, "size": "small"},
        {"text": "РАДИ ВИДА", "accent": True, "size": "big"},
    ]},
    {"start": 21.25, "end": 22.40, "lines": [
        {"text": "У КАЖДОГО", "accent": False, "size": "small"},
        {"text": "СВОЙ ФОРМАТ", "accent": True, "size": "big"},
    ]},
    {"start": 22.70, "end": 25.45, "lines": [
        {"text": "ЕМУ ТАБЛИЦА", "accent": False, "size": "small"},
        {"text": "МНЕ ЖИВОЙ ПРОГРЕСС", "accent": True, "size": "big"},
    ]},
    {"start": 25.65, "end": 27.05, "lines": [
        {"text": "БЕЗ СТРОЧКИ", "accent": False, "size": "small"},
        {"text": "В ЭКСЕЛЕ", "accent": True, "size": "big"},
    ]},
    {"start": 27.30, "end": 28.84, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep6_emphasis = [
    {"start": 0.87, "end": 1.23},
    {"start": 16.14, "end": 16.56},
    {"start": 26.61, "end": 26.94},
]
ep6_stock = [
    {"start": 21.55, "end": 25.70, "file": "stock/stock_writing_1.mp4", "sourceStart": 0.0},
]
process(6, ep6_cards, ep6_intro, ep6_emphasis, ep6_stock)

print("ALL EPISODES BUILT AND VALIDATED")
