#!/usr/bin/env python3
"""One-off authoring + validation script for tag 'ИНТ' (6 episodes).
Run from remotion/episodes40/.
"""
import json

REAL_DURATION = {1: 38.551, 2: 37.975, 3: 35.244, 4: 30.124, 5: 27.095, 6: 28.460}
LETTER = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}

CLIP_LENGTHS = {
    "stock/stock_desk_window.mp4": 10.1,
    "stock/stock_writing_1.mp4": 7.0,
    "stock/stock_writing_2.mp4": 6.3,
    "stock/stock_girl_student_1.mp4": 7.9,
    "stock/stock_girl_student_2.mp4": 7.3,
    "stock/stock_home_evening.mp4": 26.4,
    "stock/stock_home_night.mp4": 14.8,
}


def check_cards(ep, cards, total_duration):
    prev_end = 0.0
    for i, c in enumerate(cards):
        assert c["start"] < c["end"], f"ep{ep} card{i}: start>=end ({c})"
        assert c["start"] >= prev_end - 1e-6, f"ep{ep} card{i}: overlaps previous (start {c['start']} < prev_end {prev_end})"
        dur = c["end"] - c["start"]
        assert dur <= 4.0 + 1e-6, f"ep{ep} card{i}: duration {dur:.2f}s > 4s"
        assert dur >= 0.8, f"ep{ep} card{i}: duration {dur:.2f}s < 0.8s"
        n_accent = sum(1 for l in c["lines"] if l.get("accent"))
        assert n_accent >= 1, f"ep{ep} card{i}: no accent line"
        for l in c["lines"]:
            assert "?" not in l["text"] or l["text"].endswith("?"), f"ep{ep} card{i}: bad '?' placement"
            assert "," not in l["text"] and "." not in l["text"], f"ep{ep} card{i}: punctuation not allowed: {l['text']}"
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


def check_stock(ep, stock, total_duration):
    for s in stock:
        assert s["start"] > 0.5, f"ep{ep}: stock cutaway too close to start"
        assert s["end"] < total_duration - 0.5, f"ep{ep}: stock cutaway too close to end"
        src_start = s.get("sourceStart", 0)
        dur = s["end"] - s["start"]
        clip_len = CLIP_LENGTHS[s["file"]]
        assert src_start + dur <= clip_len - 0.1, (
            f"ep{ep}: stock {s['file']} sourceStart {src_start} + dur {dur:.2f} exceeds clip length {clip_len}"
        )


def build_running_caption(words, total_duration):
    groups = [{"text": w["text"].upper(), "start": w["start"]} for w in words]
    for idx in range(len(groups)):
        groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
    groups[0]["start"] = 0.0
    return groups


def process(ep, cards, intro, emphasis, stock):
    total_duration = REAL_DURATION[ep]
    words = json.load(open(f"../asr_int/words{ep}_fixed.json"))
    for w in words:
        w["start"] = min(w["start"], total_duration)
        w["end"] = min(w["end"], total_duration)

    check_intro_vs_cards(ep, intro["end"], cards)
    check_cards(ep, cards, total_duration)
    check_emphasis(ep, emphasis, total_duration)
    check_stock(ep, stock, total_duration)

    running_caption = build_running_caption(words, total_duration)

    letter = LETTER[ep]
    json.dump(words, open(f"ep_{letter}_words.json", "w"), ensure_ascii=False, indent=2)
    json.dump(cards, open(f"ep_{letter}_cards.json", "w"), ensure_ascii=False, indent=2)
    json.dump(running_caption, open(f"ep_{letter}_running_caption.json", "w"), ensure_ascii=False, indent=2)
    json.dump({"total_duration": total_duration}, open(f"ep_{letter}_duration.json", "w"), indent=2)
    json.dump(intro, open(f"ep_{letter}_intro.json", "w"), ensure_ascii=False, indent=2)
    json.dump(emphasis, open(f"ep_{letter}_emphasis.json", "w"), ensure_ascii=False, indent=2)
    json.dump(stock, open(f"ep_{letter}_stock_cutaways.json", "w"), ensure_ascii=False, indent=2)
    print(f"ep{ep} ({letter}): OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode 1 (int1): parent checklist -- how to introduce the app to a teen
# ---------------------------------------------------------------------------
ep1_intro = {"lines": ["ПОДРОСТОК", "ИГНОРИТ СОВЕТЫ?"], "end": 2.3}
ep1_cards = [
    {"start": 2.40, "end": 4.85, "lines": [
        {"text": "КАК ПРЕДЛОЖИТЬ", "accent": False, "size": "small"},
        {"text": "ПРИЛОЖЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 5.00, "end": 7.10, "lines": [
        {"text": "ЧТОБЫ ОН САМ", "accent": False, "size": "small"},
        {"text": "ЗАХОТЕЛ", "accent": True, "size": "big"},
    ]},
    {"start": 7.70, "end": 9.45, "lines": [
        {"text": "НЕ ПРИСЫЛАЙТЕ", "accent": False, "size": "small"},
        {"text": "ССЫЛКУ С ПОДПИСЬЮ", "accent": True, "size": "big"},
    ]},
    {"start": 9.60, "end": 12.90, "lines": [
        {"text": "ЭТО ВЫЗОВЕТ", "accent": False, "size": "small"},
        {"text": "ОБРАТНУЮ РЕАКЦИЮ", "accent": True, "size": "big"},
    ]},
    {"start": 14.35, "end": 16.50, "lines": [
        {"text": "ПОКАЖИТЕ", "accent": False, "size": "small"},
        {"text": "НА СВОЁМ ТЕЛЕФОНЕ", "accent": True, "size": "big"},
    ]},
    {"start": 17.80, "end": 20.30, "lines": [
        {"text": "БЕЗ ОЖИДАНИЯ", "accent": False, "size": "small"},
        {"text": "МГНОВЕННОЙ РЕАКЦИИ", "accent": True, "size": "big"},
    ]},
    {"start": 20.70, "end": 23.65, "lines": [
        {"text": "ПРЕДЛОЖИТЕ", "accent": False, "size": "small"},
        {"text": "КАК ЭКСПЕРИМЕНТ", "accent": True, "size": "big"},
    ]},
    {"start": 23.90, "end": 25.90, "lines": [
        {"text": "А НЕ ОБЯЗАТЕЛЬНОЕ", "accent": False, "size": "small"},
        {"text": "ЗАДАНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 26.25, "end": 29.15, "lines": [
        {"text": "НЕ СПРАШИВАЙТЕ", "accent": False, "size": "small"},
        {"text": "РЕЗУЛЬТАТ СРАЗУ", "accent": True, "size": "big"},
    ]},
    {"start": 29.40, "end": 30.55, "lines": [
        {"text": "ДАЙТЕ", "accent": True, "size": "big"},
        {"text": "ПРОСТРАНСТВО", "accent": False, "size": "small"},
    ]},
    {"start": 30.90, "end": 34.10, "lines": [
        {"text": "ФОРМАТ", "accent": False, "size": "small"},
        {"text": "КОРОТКИЙ И ИГРОВОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 34.30, "end": 36.15, "lines": [
        {"text": "ЧТОБЫ ОН", "accent": False, "size": "small"},
        {"text": "САМ ВЕРНУЛСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 36.50, "end": 38.551, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep1_emphasis = [
    {"start": 11.55, "end": 11.76},
    {"start": 18.12, "end": 18.54},
    {"start": 29.49, "end": 29.85},
]
ep1_stock = [
    {"start": 20.73, "end": 23.49, "file": "stock/stock_writing_1.mp4", "sourceStart": 0.0},
]
process(1, ep1_cards, ep1_intro, ep1_emphasis, ep1_stock)

# ---------------------------------------------------------------------------
# Episode 2 (int2): parent, rationalist -- letting go of control
# ---------------------------------------------------------------------------
ep2_intro = {"lines": ["ХОЧЕТСЯ", "КОНТРОЛИРОВАТЬ?"], "end": 2.3}
ep2_cards = [
    {"start": 2.50, "end": 3.85, "lines": [
        {"text": "КАК РОДИТЕЛЯ", "accent": False, "size": "small"},
        {"text": "РАЦИОНАЛИСТА", "accent": True, "size": "big"},
    ]},
    {"start": 4.20, "end": 5.70, "lines": [
        {"text": "НЕ НАЙТИ", "accent": False, "size": "small"},
        {"text": "ИНСТРУМЕНТ", "accent": True, "size": "big"},
    ]},
    {"start": 6.00, "end": 7.50, "lines": [
        {"text": "А ОТПУСТИТЬ", "accent": False, "size": "small"},
        {"text": "КОНТРОЛЬ", "accent": True, "size": "big"},
    ]},
    {"start": 7.70, "end": 9.20, "lines": [
        {"text": "КАК ИМ", "accent": False, "size": "small"},
        {"text": "ПОЛЬЗУЕТСЯ РЕБЁНОК", "accent": True, "size": "big"},
    ]},
    {"start": 9.60, "end": 12.30, "lines": [
        {"text": "ПРИВЫКЛА", "accent": False, "size": "small"},
        {"text": "СРАВНИВАТЬ И СЧИТАТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 12.60, "end": 14.10, "lines": [
        {"text": "ЧИТАТЬ ОТЗЫВЫ", "accent": False, "size": "small"},
        {"text": "И ПОСЛЕ ВЫБОРА", "accent": True, "size": "big"},
    ]},
    {"start": 14.50, "end": 16.10, "lines": [
        {"text": "ХОЧЕТСЯ", "accent": False, "size": "small"},
        {"text": "ПРОВЕРЯТЬ КАЖДЫЙ ШАГ", "accent": True, "size": "big"},
    ]},
    {"start": 17.30, "end": 19.60, "lines": [
        {"text": "НА ДЕЛЕ КОНТРОЛЬ", "accent": False, "size": "small"},
        {"text": "РАЗДРАЖАЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 20.55, "end": 22.95, "lines": [
        {"text": "СНИЖАЕТ ЖЕЛАНИЕ", "accent": False, "size": "small"},
        {"text": "ЗАНИМАТЬСЯ САМОМУ", "accent": True, "size": "big"},
    ]},
    {"start": 23.60, "end": 25.30, "lines": [
        {"text": "ПОКАЗАЛА СЫНУ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 25.55, "end": 27.45, "lines": [
        {"text": "ОБЪЯСНИЛА", "accent": False, "size": "small"},
        {"text": "КОРОТКО", "accent": True, "size": "big"},
    ]},
    {"start": 27.90, "end": 30.20, "lines": [
        {"text": "ПЕРЕСТАЛА СПРАШИВАТЬ", "accent": False, "size": "small"},
        {"text": "ПРО ПРОГРЕСС", "accent": True, "size": "big"},
    ]},
    {"start": 30.95, "end": 33.90, "lines": [
        {"text": "РЕШЕНИЕ ОКАЗАЛОСЬ", "accent": False, "size": "small"},
        {"text": "НЕ В ИНСТРУМЕНТЕ", "accent": True, "size": "big"},
    ]},
    {"start": 34.30, "end": 35.60, "lines": [
        {"text": "А В", "accent": False, "size": "small"},
        {"text": "ДОВЕРИИ", "accent": True, "size": "big"},
    ]},
    {"start": 36.10, "end": 37.975, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep2_emphasis = [
    {"start": 6.69, "end": 7.02},
    {"start": 19.08, "end": 19.53},
    {"start": 34.59, "end": 34.86},
]
ep2_stock = []
process(2, ep2_cards, ep2_intro, ep2_emphasis, ep2_stock)

# ---------------------------------------------------------------------------
# Episode 3 (int3): final checklist before recommending -- FIPI, free, tested
# ---------------------------------------------------------------------------
ep3_intro = {"lines": ["ДОВЕРЯЕШЬ", "ОТЗЫВАМ В СЕТИ?"], "end": 2.3}
ep3_cards = [
    {"start": 2.50, "end": 3.90, "lines": [
        {"text": "ПЕРЕД ТЕМ КАК", "accent": False, "size": "small"},
        {"text": "ПОРЕКОМЕНДОВАТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 5.40, "end": 7.50, "lines": [
        {"text": "НЕ НА ВЕРУ", "accent": False, "size": "small"},
        {"text": "ОТЗЫВАМ", "accent": True, "size": "big"},
    ]},
    {"start": 7.90, "end": 9.90, "lines": [
        {"text": "ПРОВЕРИЛА", "accent": False, "size": "small"},
        {"text": "БАНК ЗАДАНИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 9.95, "end": 11.60, "lines": [
        {"text": "ОФИЦИАЛЬНОМУ", "accent": False, "size": "small"},
        {"text": "ФИПИ ЛИЧНО", "accent": True, "size": "big"},
    ]},
    {"start": 12.40, "end": 13.75, "lines": [
        {"text": "А НЕ НА СЛОВО", "accent": False, "size": "small"},
        {"text": "РАЗРАБОТЧИКАМ", "accent": True, "size": "big"},
    ]},
    {"start": 14.20, "end": 16.75, "lines": [
        {"text": "ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"},
        {"text": "ПОД ТЕКУЩИЙ ГОД", "accent": True, "size": "big"},
    ]},
    {"start": 17.20, "end": 18.65, "lines": [
        {"text": "НЕ ОСТАЛСЯ", "accent": False, "size": "small"},
        {"text": "АРХИВНОЙ ВЕРСИЕЙ", "accent": True, "size": "big"},
    ]},
    {"start": 19.00, "end": 20.80, "lines": [
        {"text": "ПРОШЛА САМА", "accent": False, "size": "small"},
        {"text": "ОДНУ ТЕМУ ЦЕЛИКОМ", "accent": True, "size": "big"},
    ]},
    {"start": 20.90, "end": 23.10, "lines": [
        {"text": "ЧТОБЫ ПОНИМАТЬ", "accent": False, "size": "small"},
        {"text": "ФОРМАТ РЕБЁНКА", "accent": True, "size": "big"},
    ]},
    {"start": 23.55, "end": 25.60, "lines": [
        {"text": "СРАВНИЛА", "accent": False, "size": "small"},
        {"text": "СТОИМОСТЬ КОНКУРЕНТОВ", "accent": True, "size": "big"},
    ]},
    {"start": 25.90, "end": 28.60, "lines": [
        {"text": "ОКАЗАЛОСЬ", "accent": False, "size": "small"},
        {"text": "ПОЛНОСТЬЮ БЕСПЛАТНЫМ", "accent": True, "size": "big"},
    ]},
    {"start": 29.10, "end": 30.85, "lines": [
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": False, "size": "small"},
        {"text": "ПРОШЁЛ ВСЁ", "accent": True, "size": "big"},
    ]},
    {"start": 30.85, "end": 33.05, "lines": [
        {"text": "БЕЗ ЕДИНОГО", "accent": False, "size": "small"},
        {"text": "ПРОПУСКА", "accent": True, "size": "big"},
    ]},
    {"start": 33.35, "end": 35.244, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep3_emphasis = [
    {"start": 11.34, "end": 11.55},
    {"start": 24.66, "end": 24.87},
    {"start": 32.58, "end": 32.97},
]
ep3_stock = [
    {"start": 19.14, "end": 23.07, "file": "stock/stock_writing_2.mp4", "sourceStart": 0.0},
]
process(3, ep3_cards, ep3_intro, ep3_emphasis, ep3_stock)

# ---------------------------------------------------------------------------
# Episode 4 (int4): summer plans vs September reality
# ---------------------------------------------------------------------------
ep4_intro = {"lines": ["ЛЕТНИЕ ПЛАНЫ", "РАЗБИЛИСЬ О СЕНТЯБРЬ?"], "end": 2.3}
ep4_cards = [
    {"start": 2.50, "end": 4.65, "lines": [
        {"text": "СМОТРЮ ВИДЕО", "accent": False, "size": "small"},
        {"text": "ОДИННАДЦАТИКЛАССНИКОВ", "accent": True, "size": "big"},
    ]},
    {"start": 4.90, "end": 6.30, "lines": [
        {"text": "КАК ПРЕДСТАВЛЯЛИ", "accent": False, "size": "small"},
        {"text": "УЧЁБУ ЛЕТОМ", "accent": True, "size": "big"},
    ]},
    {"start": 6.90, "end": 8.10, "lines": [
        {"text": "И КАК ВЫШЛО", "accent": False, "size": "small"},
        {"text": "НА ДЕЛЕ", "accent": True, "size": "big"},
    ]},
    {"start": 9.00, "end": 11.30, "lines": [
        {"text": "ПЛАНИРОВАЛ", "accent": False, "size": "small"},
        {"text": "ТРИ ЧАСА В ДЕНЬ", "accent": True, "size": "big"},
    ]},
    {"start": 11.60, "end": 13.85, "lines": [
        {"text": "В СЕНТЯБРЕ ОТКРЫЛ", "accent": False, "size": "small"},
        {"text": "ОДИН РАЗ", "accent": True, "size": "big"},
    ]},
    {"start": 15.40, "end": 18.10, "lines": [
        {"text": "УЗНАЮ ВСЕХ", "accent": False, "size": "small"},
        {"text": "ВКЛЮЧАЯ СЕБЯ", "accent": True, "size": "big"},
    ]},
    {"start": 18.40, "end": 19.95, "lines": [
        {"text": "БЕЗ ИЛЛЮЗИЙ", "accent": False, "size": "small"},
        {"text": "О ДИСЦИПЛИНЕ", "accent": True, "size": "big"},
    ]},
    {"start": 20.75, "end": 22.80, "lines": [
        {"text": "КТО-ТО СКИНУЛ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 23.10, "end": 25.35, "lines": [
        {"text": "ДЕСЯТЬ МИНУТ", "accent": False, "size": "small"},
        {"text": "РЕАЛИСТИЧНЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 25.45, "end": 26.55, "lines": [
        {"text": "ЧЕМ", "accent": False, "size": "small"},
        {"text": "ТРИ ЧАСА КОНСПЕКТА", "accent": True, "size": "big"},
    ]},
    {"start": 26.80, "end": 28.30, "lines": [
        {"text": "БЕРУ НА ЗАМЕТКУ", "accent": False, "size": "small"},
        {"text": "ЭТОТ ФОРМАТ", "accent": True, "size": "big"},
    ]},
    {"start": 28.35, "end": 30.124, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep4_emphasis = [
    {"start": 12.69, "end": 12.96},
    {"start": 24.75, "end": 25.32},
]
ep4_stock = [
    {"start": 9.03, "end": 12.24, "file": "stock/stock_desk_window.mp4", "sourceStart": 0.0},
]
process(4, ep4_cards, ep4_intro, ep4_emphasis, ep4_stock)

# ---------------------------------------------------------------------------
# Episode 5 (int5): 10th grader watching the anxiety approach
# ---------------------------------------------------------------------------
ep5_intro = {"lines": ["СКОРО ВСЕ", "НАЧНУТ ПАНИКОВАТЬ?"], "end": 2.3}
ep5_cards = [
    {"start": 2.55, "end": 4.10, "lines": [
        {"text": "УЖЕ ВИЖУ", "accent": False, "size": "small"},
        {"text": "ЧТО БУДЕТ В СЕНТЯБРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 4.20, "end": 6.10, "lines": [
        {"text": "БУДУТ ГОВОРИТЬ", "accent": False, "size": "small"},
        {"text": "ТОЛЬКО ПРО БАЛЛЫ", "accent": True, "size": "big"},
    ]},
    {"start": 6.25, "end": 7.40, "lines": [
        {"text": "ПРЯМО", "accent": False, "size": "small"},
        {"text": "ЗА ЗАВТРАКОМ", "accent": True, "size": "big"},
    ]},
    {"start": 8.10, "end": 9.55, "lines": [
        {"text": "ГОД НАЗАД Я", "accent": False, "size": "small"},
        {"text": "ЗАЛИПАЛ В ТЕЛЕФОН", "accent": True, "size": "big"},
    ]},
    {"start": 9.75, "end": 12.50, "lines": [
        {"text": "НЕ ДУМАЛ", "accent": False, "size": "small"},
        {"text": "НИ ПРО КАКОЙ ЭКЗАМЕН", "accent": True, "size": "big"},
    ]},
    {"start": 12.80, "end": 15.60, "lines": [
        {"text": "ЧЕРЕЗ ГОД", "accent": False, "size": "small"},
        {"text": "ТА ЖЕ ЖИЗНЬ", "accent": True, "size": "big"},
    ]},
    {"start": 15.70, "end": 17.20, "lines": [
        {"text": "ТОЛЬКО С", "accent": False, "size": "small"},
        {"text": "ФОНОВОЙ ТРЕВОГОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 17.45, "end": 19.00, "lines": [
        {"text": "ВО ВСЕХ", "accent": False, "size": "small"},
        {"text": "РАЗГОВОРАХ В ЧАТЕ", "accent": True, "size": "big"},
    ]},
    {"start": 19.05, "end": 20.75, "lines": [
        {"text": "ПОКА ЭТА ПАНИКА", "accent": False, "size": "small"},
        {"text": "МЕНЯ НЕ КОСНУЛАСЬ", "accent": True, "size": "big"},
    ]},
    {"start": 21.00, "end": 24.30, "lines": [
        {"text": "ПРОСТО ОСТАВЛЮ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР ФОНОМ", "accent": True, "size": "big"},
    ]},
    {"start": 24.50, "end": 25.45, "lines": [
        {"text": "БЕЗ ОБЯЗАТЕЛЬСТВ", "accent": False, "size": "small"},
        {"text": "ДЕЛАТЬ СЕЙЧАС", "accent": True, "size": "big"},
    ]},
    {"start": 25.60, "end": 27.095, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep5_emphasis = [
    {"start": 9.78, "end": 10.05},
    {"start": 16.65, "end": 16.95},
    {"start": 20.31, "end": 20.73},
]
ep5_stock = []
process(5, ep5_cards, ep5_intro, ep5_emphasis, ep5_stock)

# ---------------------------------------------------------------------------
# Episode 6 (int6): everyone acting like EGE is tomorrow
# ---------------------------------------------------------------------------
ep6_intro = {"lines": ["ВСЕ ВОКРУГ", "УЖЕ ПАНИКУЮТ?"], "end": 2.3}
ep6_cards = [
    {"start": 2.50, "end": 3.65, "lines": [
        {"text": "ВЕДЁТ СЕБЯ ТАК", "accent": False, "size": "small"},
        {"text": "БУДТО ЗАВТРА", "accent": True, "size": "big"},
    ]},
    {"start": 3.80, "end": 6.10, "lines": [
        {"text": "МЕЖДУ НАМИ", "accent": False, "size": "small"},
        {"text": "И ЭКЗАМЕНОМ", "accent": True, "size": "big"},
    ]},
    {"start": 6.20, "end": 7.65, "lines": [
        {"text": "ЦЕЛЫЙ ГОД", "accent": False, "size": "small"},
        {"text": "ЕЩЁ НЕ НАЧАЛСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 8.20, "end": 9.90, "lines": [
        {"text": "УЗНАЛА СЛОВО", "accent": False, "size": "small"},
        {"text": "ПРОБНИК", "accent": True, "size": "big"},
    ]},
    {"start": 10.00, "end": 11.20, "lines": [
        {"text": "ТОЛЬКО ИЗ", "accent": False, "size": "small"},
        {"text": "ЧУЖИХ СТОРИС", "accent": True, "size": "big"},
    ]},
    {"start": 11.40, "end": 13.70, "lines": [
        {"text": "ПОКА БЕЗ", "accent": False, "size": "small"},
        {"text": "ЛИЧНОЙ ПАНИКИ", "accent": True, "size": "big"},
    ]},
    {"start": 13.90, "end": 15.30, "lines": [
        {"text": "УЧИТЕЛЯ", "accent": False, "size": "small"},
        {"text": "УЖЕ НАМЕКАЮТ", "accent": True, "size": "big"},
    ]},
    {"start": 15.35, "end": 16.70, "lines": [
        {"text": "ОДНОКЛАССНИКИ", "accent": False, "size": "small"},
        {"text": "НЕРВНИЧАЮТ В ЧАТЕ", "accent": True, "size": "big"},
    ]},
    {"start": 17.50, "end": 19.30, "lines": [
        {"text": "А Я ПРОСТО", "accent": False, "size": "small"},
        {"text": "ЖДУ ПЕРВОЕ СЕНТЯБРЯ", "accent": True, "size": "big"},
    ]},
    {"start": 19.35, "end": 20.30, "lines": [
        {"text": "КАК", "accent": False, "size": "small"},
        {"text": "ОБЫЧНУЮ ДАТУ", "accent": True, "size": "big"},
    ]},
    {"start": 20.40, "end": 22.60, "lines": [
        {"text": "ГДЕ-ТО НА ФОНЕ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 22.65, "end": 25.95, "lines": [
        {"text": "СКИНУЛ ОТЛИЧНИК", "accent": False, "size": "small"},
        {"text": "НА ВСЯКИЙ СЛУЧАЙ", "accent": True, "size": "big"},
    ]},
    {"start": 26.40, "end": 28.460, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep6_emphasis = [
    {"start": 3.03, "end": 3.21},
    {"start": 14.67, "end": 15.09},
    {"start": 23.52, "end": 23.85},
]
ep6_stock = []
process(6, ep6_cards, ep6_intro, ep6_emphasis, ep6_stock)

print("ALL 6 EPISODES BUILT AND VALIDATED")
