#!/usr/bin/env python3
"""One-off authoring + validation script for the FOURTH 'coffee123' batch
(9 episodes uploaded under the same tag after three prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes47/.

Single returning host: the amber-room student seen in episodes44/46 A-C
and the coffee123 batches. Content angle spans multiple facets of the
same core idea (balancing olympiad + EGE prep, late-night app pull,
cost-vs-value vs paid courses, honest self-tracking).
"""
import json

REAL_DURATION = {
    "a": 33.58, "b": 21.506, "c": 23.49,
    "d": 32.88, "e": 23.618, "f": 24.663,
    "g": 32.30, "h": 21.591, "i": 24.172,
}
SOURCE_FILE = {
    "a": "a1_v1", "b": "a2_v1b", "c": "a3_v1c",
    "d": "b1_v2", "e": "b2_v2b", "f": "b3_v2c",
    "g": "c1_v3", "h": "c2_v3b", "i": "c3_v3c",
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
    words = json.load(open(f"../asr_coffee123_4/{src}_words.json"))
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
# Episode A (a1_v1): missed a whole EGE base topic during 3 days of olympiad
# camp, closed the gap in one evening sitting in the app - no lost points
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПРОПУСТИЛА ТЕМУ", "ЦЕЛУЮ НЕДЕЛЮ?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 3.75, "lines": [{"text": "ГОТОВЛЮСЬ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.55, "lines": [{"text": "ПОНЯЛА", "accent": False, "size": "small"}, {"text": "ПРОПУСТИЛА", "accent": True, "size": "big"}]},
    {"start": 5.65, "end": 7.65, "lines": [{"text": "ТЕМУ ПО", "accent": False, "size": "small"}, {"text": "ФУНКЦИЯМ", "accent": True, "size": "big"}]},
    {"start": 8.45, "end": 9.40, "lines": [{"text": "ТРИ ДНЯ", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 9.50, "end": 11.45, "lines": [{"text": "ТОЛЬКО НА", "accent": False, "size": "small"}, {"text": "СБОРАХ", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.80, "lines": [{"text": "НЕ ОТКРЫВАЛА", "accent": False, "size": "small"}, {"text": "ПРОГРАММУ", "accent": True, "size": "big"}]},
    {"start": 14.75, "end": 16.80, "lines": [{"text": "ВЕЧЕРОМ", "accent": False, "size": "small"}, {"text": "ПРОШЛА", "accent": True, "size": "big"}]},
    {"start": 16.90, "end": 17.75, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 18.98, "lines": [{"text": "ЗА ОДИН", "accent": False, "size": "small"}, {"text": "ПРИСЕСТ", "accent": True, "size": "big"}]},
    {"start": 19.50, "end": 21.35, "lines": [{"text": "ВИДЕО ПЛЮС", "accent": False, "size": "small"}, {"text": "ИГРА", "accent": True, "size": "big"}]},
    {"start": 22.10, "end": 23.40, "lines": [{"text": "НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ПО ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 23.60, "end": 25.20, "lines": [{"text": "НИ ОДНОГО", "accent": False, "size": "small"}, {"text": "БАЛЛА", "accent": True, "size": "big"}]},
    {"start": 25.40, "end": 27.10, "lines": [{"text": "ХОТЯ", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 27.90, "end": 29.15, "lines": [{"text": "КОРОТКИЙ", "accent": False, "size": "small"}, {"text": "ЗАХОД", "accent": True, "size": "big"}]},
    {"start": 29.20, "end": 31.20, "lines": [{"text": "БЫСТРЕЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "ОЖИДАЛА", "accent": True, "size": "big"}]},
    {"start": 31.70, "end": 33.58, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.98, "end": 5.49}, {"start": 18.54, "end": 18.93}, {"start": 24.96, "end": 25.17}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (a2_v1b): "5 minutes before bed" turned into 15 minutes in the
# app, the classic pull of one topic
# ---------------------------------------------------------------------------
b_intro = {"lines": ["5 МИНУТ ПРЕВРАТИЛИСЬ", "В 15?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 4.75, "lines": [{"text": "НЕ ЗАМЕТИЛ", "accent": False, "size": "small"}, {"text": "15 МИНУТ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 6.95, "lines": [{"text": "КЛАССИКА", "accent": False, "size": "small"}, {"text": "БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 7.15, "end": 8.70, "lines": [{"text": "А ТЕМА", "accent": False, "size": "small"}, {"text": "ЗАТЯГИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.80, "end": 10.75, "lines": [{"text": "ХОТЕЛ", "accent": False, "size": "small"}, {"text": "ВЗГЛЯНУТЬ", "accent": True, "size": "big"}]},
    {"start": 10.85, "end": 12.65, "lines": [{"text": "ВСЮ ТЕМУ", "accent": False, "size": "small"}, {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 12.85, "end": 15.15, "lines": [{"text": "БУДИЛЬНИК", "accent": False, "size": "small"}, {"text": "НАПОМНИЛ", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 16.15, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАТЬ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 18.15, "lines": [{"text": "5 МИНУТ", "accent": False, "size": "small"}, {"text": "ПРОТИВ", "accent": True, "size": "big"}]},
    {"start": 18.20, "end": 19.55, "lines": [{"text": "СНОВА", "accent": False, "size": "small"}, {"text": "ПРОИГРАЛИ", "accent": True, "size": "big"}]},
    {"start": 19.70, "end": 21.51, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.32, "end": 4.71}, {"start": 11.94, "end": 12.18}, {"start": 18.54, "end": 18.87}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (a3_v1c): almost overslept before a test, 15 minutes on the bus
# in the app replaced an evening he'd slept through
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЧУТЬ НЕ ПРОСПАЛ", "КОНТРОЛЬНУЮ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 3.95, "lines": [{"text": "ПЕРЕД", "accent": False, "size": "small"}, {"text": "ЗАНЯТИЕМ", "accent": True, "size": "big"}]},
    {"start": 4.10, "end": 5.85, "lines": [{"text": "ВСКОЧИЛ", "accent": False, "size": "small"}, {"text": "В ПАНИКЕ", "accent": True, "size": "big"}]},
    {"start": 6.55, "end": 8.40, "lines": [{"text": "ВМЕСТО УЧЕБНИКА", "accent": False, "size": "small"}, {"text": "ОТКРЫЛ", "accent": True, "size": "big"}]},
    {"start": 8.50, "end": 9.70, "lines": [{"text": "ТЕМА", "accent": False, "size": "small"}, {"text": "СОВПАЛА", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 10.80, "lines": [{"text": "С ЗАВТРАШНЕЙ", "accent": False, "size": "small"}, {"text": "ПРОВЕРКОЙ", "accent": True, "size": "big"}]},
    {"start": 10.90, "end": 11.70, "lines": [{"text": "ПРОБЕЖАЛ", "accent": False, "size": "small"}, {"text": "ВИДЕО", "accent": True, "size": "big"}]},
    {"start": 11.80, "end": 13.50, "lines": [{"text": "КОРОТКУЮ", "accent": False, "size": "small"}, {"text": "ИГРУ", "accent": True, "size": "big"}]},
    {"start": 13.55, "end": 14.75, "lines": [{"text": "ПРЯМО", "accent": False, "size": "small"}, {"text": "В АВТОБУСЕ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.95, "lines": [{"text": "НАПИСАЛ", "accent": False, "size": "small"}, {"text": "ЛУЧШЕ", "accent": True, "size": "big"}]},
    {"start": 17.35, "end": 18.70, "lines": [{"text": "СПРОСОНЬЯ", "accent": False, "size": "small"}, {"text": "15 МИНУТ", "accent": True, "size": "big"}]},
    {"start": 18.80, "end": 19.70, "lines": [{"text": "В ПРИЛОЖЕНИИ", "accent": False, "size": "small"}, {"text": "ЗАМЕНИЛИ", "accent": True, "size": "big"}]},
    {"start": 19.80, "end": 21.45, "lines": [{"text": "ВЕЧЕР", "accent": False, "size": "small"}, {"text": "ПРОСПАЛ", "accent": True, "size": "big"}]},
    {"start": 21.70, "end": 23.49, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 6.09, "end": 6.33}, {"start": 16.02, "end": 16.14}, {"start": 20.64, "end": 20.88}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (b1_v2): olympiad team treats EGE as unimportant, she quietly
# does 15 minutes a day in the app without telling anyone
# ---------------------------------------------------------------------------
d_intro = {"lines": ["КОМАНДА ИГНОРИТ", "ЕГЭ ЦЕЛИКОМ?"], "end": 2.3}
d_cards = [
    {"start": 2.60, "end": 3.95, "lines": [{"text": "ГОТОВИТСЯ", "accent": False, "size": "small"}, {"text": "НИКАК", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 6.20, "lines": [{"text": "ВСЕ СЧИТАЮТ", "accent": False, "size": "small"}, {"text": "МЕНЕЕ ВАЖНЫМ", "accent": True, "size": "big"}]},
    {"start": 6.25, "end": 7.55, "lines": [{"text": "ЧЕМ", "accent": False, "size": "small"}, {"text": "ПРИЗОВОЕ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 9.35, "lines": [{"text": "ТРЕНЕР", "accent": False, "size": "small"}, {"text": "ПОШУТИЛ", "accent": True, "size": "big"}]},
    {"start": 9.50, "end": 10.40, "lines": [{"text": "ЧТО БАЛЛЫ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.45, "lines": [{"text": "НАЙДУТ", "accent": False, "size": "small"}, {"text": "САМИ", "accent": True, "size": "big"}]},
    {"start": 11.45, "end": 12.95, "lines": [{"text": "ЕСЛИ ВЫИГРАЕМ", "accent": False, "size": "small"}, {"text": "ОЛИМПИАДУ", "accent": True, "size": "big"}]},
    {"start": 13.60, "end": 14.65, "lines": [{"text": "Я В ЭТО", "accent": False, "size": "small"}, {"text": "НЕ ПОВЕРИЛА", "accent": True, "size": "big"}]},
    {"start": 14.90, "end": 16.25, "lines": [{"text": "ТИХО", "accent": False, "size": "small"}, {"text": "ПРОХОЖУ", "accent": True, "size": "big"}]},
    {"start": 16.55, "end": 17.45, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 18.60, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "ТРЕНИРОВОК", "accent": True, "size": "big"}]},
    {"start": 19.00, "end": 20.15, "lines": [{"text": "НИКОМУ", "accent": False, "size": "small"}, {"text": "НЕ ГОВОРЯ", "accent": True, "size": "big"}]},
    {"start": 20.70, "end": 21.50, "lines": [{"text": "15 МИНУТ", "accent": False, "size": "small"}, {"text": "ВЕЧЕРОМ", "accent": True, "size": "big"}]},
    {"start": 21.55, "end": 22.90, "lines": [{"text": "ОДНА", "accent": False, "size": "small"}, {"text": "ТЕМА", "accent": True, "size": "big"}]},
    {"start": 23.10, "end": 24.60, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ОБЪЯВЛЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 25.55, "end": 26.90, "lines": [{"text": "ЕСЛИ ДИПЛОМ", "accent": False, "size": "small"}, {"text": "НЕ ЗАЩИТИТ", "accent": True, "size": "big"}]},
    {"start": 26.95, "end": 28.25, "lines": [{"text": "НА ВСЕ", "accent": False, "size": "small"}, {"text": "СТО ПРОЦЕНТОВ", "accent": True, "size": "big"}]},
    {"start": 28.60, "end": 30.35, "lines": [{"text": "УЖЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАКРЫТАЯ БАЗА", "accent": True, "size": "big"}]},
    {"start": 30.90, "end": 32.88, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 12.45, "end": 12.90}, {"start": 19.56, "end": 20.10}, {"start": 30.12, "end": 30.27}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (b2_v2b): compared results with a friend paying for courses for
# half a year - almost identical scores for very different money
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОДИНАКОВЫЙ РЕЗУЛЬТАТ", "РАЗНЫЕ ДЕНЬГИ?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 4.20, "lines": [{"text": "КУРСЫ", "accent": False, "size": "small"}, {"text": "КАЖДЫЙ МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.10, "lines": [{"text": "УЖЕ", "accent": False, "size": "small"}, {"text": "ПОЛГОДА", "accent": True, "size": "big"}]},
    {"start": 5.15, "end": 6.60, "lines": [{"text": "НА ПОСЛЕДНЕМ", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 6.65, "end": 8.10, "lines": [{"text": "ОКАЗАЛИСЬ", "accent": False, "size": "small"}, {"text": "ПОХОЖИМИ", "accent": True, "size": "big"}]},
    {"start": 8.20, "end": 9.30, "lines": [{"text": "РАЗНИЦА", "accent": False, "size": "small"}, {"text": "В БАЛЛАХ", "accent": True, "size": "big"}]},
    {"start": 10.30, "end": 11.60, "lines": [{"text": "ВСЁ ЭТО ВРЕМЯ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 11.65, "end": 12.80, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРОМ", "accent": True, "size": "big"}]},
    {"start": 12.95, "end": 14.45, "lines": [{"text": "БЕЗ ЕДИНОГО", "accent": False, "size": "small"}, {"text": "ЗАНЯТИЯ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.55, "lines": [{"text": "ДРУГ", "accent": False, "size": "small"}, {"text": "УДИВИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.50, "lines": [{"text": "БОЛЬШЕ МЕНЯ", "accent": False, "size": "small"}, {"text": "УЗНАЛ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 18.05, "lines": [{"text": "СКОЛЬКО", "accent": False, "size": "small"}, {"text": "ПОТРАТИЛА", "accent": True, "size": "big"}]},
    {"start": 18.35, "end": 19.25, "lines": [{"text": "ОДИНАКОВЫЙ", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТ", "accent": True, "size": "big"}]},
    {"start": 19.35, "end": 20.15, "lines": [{"text": "ЗА РАЗНЫЕ", "accent": False, "size": "small"}, {"text": "ДЕНЬГИ", "accent": True, "size": "big"}]},
    {"start": 20.20, "end": 21.60, "lines": [{"text": "ЗАСТАВИЛ", "accent": False, "size": "small"}, {"text": "ЗАДУМАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 21.80, "end": 23.62, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 7.53, "end": 8.04}, {"start": 14.01, "end": 14.40}, {"start": 21.12, "end": 21.54}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (b3_v2c): a blogger recommended 7 paid courses at once; one
# free app covers the same ground
# ---------------------------------------------------------------------------
f_intro = {"lines": ["7 ПЛАТНЫХ КУРСОВ", "СРАЗУ?"], "end": 2.3}
f_cards = [
    {"start": 2.60, "end": 4.45, "lines": [{"text": "ПОСОВЕТОВАЛ", "accent": False, "size": "small"}, {"text": "7 КУРСОВ", "accent": True, "size": "big"}]},
    {"start": 4.60, "end": 6.40, "lines": [{"text": "ОДНОВРЕМЕННО", "accent": False, "size": "small"}, {"text": "ПОСЧИТАЛ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 7.60, "lines": [{"text": "СКОЛЬКО ЭТО", "accent": False, "size": "small"}, {"text": "ОБОЙДЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.75, "end": 10.30, "lines": [{"text": "ЦИФРА", "accent": False, "size": "small"}, {"text": "ПУГАЮЩАЯ", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 11.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДАЁТ", "accent": True, "size": "big"}]},
    {"start": 11.65, "end": 12.55, "lines": [{"text": "ПОХОЖИЙ", "accent": False, "size": "small"}, {"text": "НАБОР", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.85, "lines": [{"text": "БЕСПЛАТНО", "accent": False, "size": "small"}, {"text": "БЕЗ ПОДПИСКИ", "accent": True, "size": "big"}]},
    {"start": 13.90, "end": 15.05, "lines": [{"text": "НА СЕМЬ", "accent": False, "size": "small"}, {"text": "СЕРВИСОВ", "accent": True, "size": "big"}]},
    {"start": 15.20, "end": 16.95, "lines": [{"text": "НАПИСАЛ", "accent": False, "size": "small"}, {"text": "БЛОГЕРУ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.65, "lines": [{"text": "ОТВЕТА", "accent": False, "size": "small"}, {"text": "НЕ ДОЖДАЛСЯ", "accent": True, "size": "big"}]},
    {"start": 19.05, "end": 20.50, "lines": [{"text": "7 КУРСОВ И", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 20.55, "end": 22.60, "lines": [{"text": "РЕШАЮТ", "accent": False, "size": "small"}, {"text": "ОДНУ ЗАДАЧУ", "accent": True, "size": "big"}]},
    {"start": 22.85, "end": 24.663, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 8.91, "end": 9.33}, {"start": 18.24, "end": 18.63}, {"start": 20.58, "end": 21.03}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (c1_v3): first mock exam disappointed, 15 min/evening in the
# app for a month while olympiad kept the days - second mock jumped 8pts
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ПЕРВЫЙ ПРОБНИК", "РАЗОЧАРОВАЛ?"], "end": 2.3}
g_cards = [
    {"start": 2.60, "end": 3.65, "lines": [{"text": "НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.15, "lines": [{"text": "ВОТ ЧТО ДАЛО", "accent": False, "size": "small"}, {"text": "ЗА МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.70, "lines": [{"text": "ПЕРВЫЙ", "accent": False, "size": "small"}, {"text": "ПРОБНИК", "accent": True, "size": "big"}]},
    {"start": 8.15, "end": 9.85, "lines": [{"text": "НА БАЛЛ", "accent": False, "size": "small"}, {"text": "НИЖЕ", "accent": True, "size": "big"}]},
    {"start": 10.10, "end": 11.10, "lines": [{"text": "СИЛЬНО", "accent": False, "size": "small"}, {"text": "ОГОРЧИЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.55, "lines": [{"text": "15 МИНУТ", "accent": False, "size": "small"}, {"text": "В ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.60, "end": 15.55, "lines": [{"text": "КАЖДЫЙ ВЕЧЕР", "accent": False, "size": "small"}, {"text": "ВМЕСТО ЧАСА", "accent": True, "size": "big"}]},
    {"start": 16.10, "end": 16.95, "lines": [{"text": "ЗА", "accent": False, "size": "small"}, {"text": "КОНСПЕКТОМ", "accent": True, "size": "big"}]},
    {"start": 17.20, "end": 18.10, "lines": [{"text": "ВТОРОЙ", "accent": False, "size": "small"}, {"text": "ПРОБНИК", "accent": True, "size": "big"}]},
    {"start": 18.20, "end": 19.70, "lines": [{"text": "ВЫРОС СРАЗУ", "accent": False, "size": "small"}, {"text": "НА 8 БАЛЛОВ", "accent": True, "size": "big"}]},
    {"start": 20.50, "end": 21.70, "lines": [{"text": "ОЛИМПИАДНОЕ", "accent": False, "size": "small"}, {"text": "РАСПИСАНИЕ", "accent": True, "size": "big"}]},
    {"start": 21.70, "end": 23.25, "lines": [{"text": "ВРЕМЯ", "accent": False, "size": "small"}, {"text": "ЦЕЛО", "accent": True, "size": "big"}]},
    {"start": 23.25, "end": 24.10, "lines": [{"text": "НИ НА", "accent": False, "size": "small"}, {"text": "МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 24.85, "end": 26.95, "lines": [{"text": "ВОСЕМЬ БАЛЛОВ", "accent": False, "size": "small"}, {"text": "ЗА МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 27.20, "end": 28.50, "lines": [{"text": "ОКАЗАЛИСЬ", "accent": False, "size": "small"}, {"text": "СИЛЬНЕЕ", "accent": True, "size": "big"}]},
    {"start": 28.55, "end": 29.75, "lines": [{"text": "ЛЮБОГО ПЛАНА", "accent": False, "size": "small"}, {"text": "НА БУМАГЕ", "accent": True, "size": "big"}]},
    {"start": 30.30, "end": 32.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 10.44, "end": 11.04}, {"start": 19.02, "end": 19.20}, {"start": 27.81, "end": 28.44}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (c2_v3b): mixed up phone icons in the dark, opened the app
# instead of a game and got hooked on a topic for 15 minutes
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ПЕРЕПУТАЛ ИКОНКИ", "В ТЕМНОТЕ?"], "end": 2.3}
h_cards = [
    {"start": 2.60, "end": 3.70, "lines": [{"text": "ВМЕСТО ИГРЫ", "accent": False, "size": "small"}, {"text": "ИКОНКИ", "accent": True, "size": "big"}]},
    {"start": 3.75, "end": 4.75, "lines": [{"text": "НА ТЕЛЕФОНЕ", "accent": False, "size": "small"}, {"text": "В ТЕМНОТЕ", "accent": True, "size": "big"}]},
    {"start": 4.90, "end": 5.75, "lines": [{"text": "ХОТЕЛ", "accent": False, "size": "small"}, {"text": "ЗАКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 5.80, "end": 6.70, "lines": [{"text": "НАЙТИ", "accent": False, "size": "small"}, {"text": "ИГРУ", "accent": True, "size": "big"}]},
    {"start": 6.85, "end": 8.20, "lines": [{"text": "НО", "accent": False, "size": "small"}, {"text": "ЗАЦЕПИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 8.25, "end": 9.50, "lines": [{"text": "НА ЭКРАНЕ", "accent": False, "size": "small"}, {"text": "ЗАЛИП", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 10.80, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "УРОВНЯ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 12.40, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "15 МИНУТ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 14.20, "lines": [{"text": "ИГРА", "accent": False, "size": "small"}, {"text": "НЕТРОНУТОЙ", "accent": True, "size": "big"}]},
    {"start": 14.30, "end": 15.40, "lines": [{"text": "ЗАТО ТЕМА", "accent": False, "size": "small"}, {"text": "ЗАКРЫТА", "accent": True, "size": "big"}]},
    {"start": 16.35, "end": 18.25, "lines": [{"text": "ПЕРЕПУТАННЫЕ", "accent": False, "size": "small"}, {"text": "ПОЛЕЗНЫМИ", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.25, "lines": [{"text": "ДОВОЛЬНО", "accent": False, "size": "small"}, {"text": "ОШИБКОЙ", "accent": True, "size": "big"}]},
    {"start": 19.75, "end": 21.591, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 4.41, "end": 4.71}, {"start": 9.00, "end": 9.18}, {"start": 18.81, "end": 19.20}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (c3_v3c): friend fakes studying by flipping through old notes;
# the app removes the self-deception because progress is visible or not
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ДРУГ ДЕЛАЕТ ВИД", "ЧТО ГОТОВИТСЯ?"], "end": 2.3}
i_cards = [
    {"start": 2.60, "end": 3.45, "lines": [{"text": "ПРОСТО", "accent": False, "size": "small"}, {"text": "ЛИСТАЕТ", "accent": True, "size": "big"}]},
    {"start": 3.65, "end": 4.50, "lines": [{"text": "СТАРЫЕ", "accent": False, "size": "small"}, {"text": "КОНСПЕКТЫ", "accent": True, "size": "big"}]},
    {"start": 4.60, "end": 5.45, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "МЫСЛИ", "accent": True, "size": "big"}]},
    {"start": 5.60, "end": 6.75, "lines": [{"text": "У МЕНЯ ТОЖЕ", "accent": False, "size": "small"}, {"text": "ТАК БЫЛО", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.30, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "ОТКРЫЛ", "accent": True, "size": "big"}]},
    {"start": 8.45, "end": 9.65, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "ИМИТАЦИИ", "accent": True, "size": "big"}]},
    {"start": 9.80, "end": 11.00, "lines": [{"text": "БУМАЖНОЙ", "accent": False, "size": "small"}, {"text": "УЧЁБЫ", "accent": True, "size": "big"}]},
    {"start": 11.15, "end": 12.30, "lines": [{"text": "ПРОШЕЛ ТЕМУ", "accent": False, "size": "small"}, {"text": "ИЛИ НЕТ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 14.10, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "САМООБМАНА", "accent": True, "size": "big"}]},
    {"start": 14.20, "end": 16.10, "lines": [{"text": "ПОКАЗАЛ", "accent": False, "size": "small"}, {"text": "СТАТИСТИКУ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.60, "lines": [{"text": "ЗАВИС", "accent": False, "size": "small"}, {"text": "МОЛЧА", "accent": True, "size": "big"}]},
    {"start": 17.80, "end": 18.95, "lines": [{"text": "ИМИТАЦИЯ", "accent": False, "size": "small"}, {"text": "ПОДГОТОВКИ", "accent": True, "size": "big"}]},
    {"start": 19.05, "end": 20.80, "lines": [{"text": "РЕАЛЬНАЯ", "accent": False, "size": "small"}, {"text": "ВЫГЛЯДИТ", "accent": True, "size": "big"}]},
    {"start": 20.85, "end": 22.30, "lines": [{"text": "СНАРУЖИ ОДИНАКОВО", "accent": False, "size": "small"}, {"text": "А ВНУТРИ НЕТ", "accent": True, "size": "big"}]},
    {"start": 22.40, "end": 24.172, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 12.84, "end": 13.23}, {"start": 17.34, "end": 17.55}, {"start": 20.97, "end": 21.42}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
