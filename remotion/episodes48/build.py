#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTH 'coffee123' batch
(9 episodes uploaded under the same tag after four prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes48/.

Same three returning hosts as the fourth batch (bookshelf girl, sunset-window
boy, gray-bedroom boy). Content angle this time is app-feature focused
(offline access, one-fact flashcards, per-task timer, targeted mini-games,
auto daily missions, step-by-step video solutions, friends/rating, price vs
free task bank, smart topic suggestion) rather than personal narrative.
"""
import json

REAL_DURATION = {
    "a": 32.151, "b": 22.920, "c": 24.800,
    "d": 32.066, "e": 26.135, "f": 24.087,
    "g": 35.991, "h": 24.663, "i": 26.007,
}
SOURCE_FILE = {
    "a": "12_09_-_1_2160p1", "b": "12_09_-_1_2160p111111", "c": "12_09_-_1_2160p1111111",
    "d": "12_09_-_2_2160p", "e": "12_09_-_2_2160p222222", "f": "12_09_-_2_2160p2222222",
    "g": "12_09_-_3_2160p_3", "h": "12_09_-_3_2160p3333333", "i": "default",
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
    words = json.load(open(f"../asr_coffee123_5/{src}_words.json"))
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
# Episode A (girl, 32.151s): offline task bank works without internet,
# useful in transit between olympiad camps with no signal
# ---------------------------------------------------------------------------
a_intro = {"lines": ["БЕЗ ИНТЕРНЕТА", "НЕ ГОТОВИШЬСЯ?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ОЛИМПИАДА", "accent": False, "size": "small"}, {"text": "И ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.60, "lines": [{"text": "ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "В ДОРОГЕ", "accent": True, "size": "big"}]},
    {"start": 5.76, "end": 7.00, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "СБОРАМИ", "accent": True, "size": "big"}]},
    {"start": 7.10, "end": 8.60, "lines": [{"text": "ИНТЕРНЕТА", "accent": False, "size": "small"}, {"text": "НЕТ ВОВСЕ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.60, "lines": [{"text": "ИСКАТЬ СЕТЬ", "accent": False, "size": "small"}, {"text": "НЕКОГДА", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 12.10, "lines": [{"text": "РАСПИСАНИЕ", "accent": False, "size": "small"}, {"text": "НЕ ЖДЁТ", "accent": True, "size": "big"}]},
    {"start": 13.08, "end": 14.65, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ХРАНИТ БАНК", "accent": True, "size": "big"}]},
    {"start": 14.80, "end": 16.55, "lines": [{"text": "КОПИЯ", "accent": False, "size": "small"}, {"text": "НА УСТРОЙСТВЕ", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 18.60, "lines": [{"text": "ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ОТКРЫТЫ", "accent": True, "size": "big"}]},
    {"start": 18.65, "end": 19.90, "lines": [{"text": "БЕЗ ЗАПРОСА", "accent": False, "size": "small"}, {"text": "К СЕРВЕРУ", "accent": True, "size": "big"}]},
    {"start": 20.43, "end": 21.85, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 22.53, "end": 23.95, "lines": [{"text": "В ЛЮБОЙ ТОЧКЕ", "accent": False, "size": "small"}, {"text": "МАРШРУТА", "accent": True, "size": "big"}]},
    {"start": 24.99, "end": 26.50, "lines": [{"text": "ПЛОХОЙ СИГНАЛ", "accent": False, "size": "small"}, {"text": "НЕ ПОМЕХА", "accent": True, "size": "big"}]},
    {"start": 26.70, "end": 29.60, "lines": [{"text": "ПОДГОТОВКА", "accent": False, "size": "small"}, {"text": "НЕ СТОИТ", "accent": True, "size": "big"}]},
    {"start": 30.15, "end": 32.10, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 13.95, "end": 14.61}, {"start": 17.64, "end": 18.15}, {"start": 23.46, "end": 23.88}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (gray boy, 22.920s): skimming a notebook before bed doesn't
# stick; one-fact flashcards remember better
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЛИСТАЕШЬ КОНСПЕКТ", "ПЕРЕД СНОМ?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "НИЧЕГО НЕ", "accent": False, "size": "small"}, {"text": "ЗАПОМНИЛ", "accent": True, "size": "big"}]},
    {"start": 4.90, "end": 6.20, "lines": [{"text": "А УТРОМ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 7.02, "end": 8.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.10, "lines": [{"text": "КОМПАКТНЫЙ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.95, "lines": [{"text": "ОДИН ФАКТ", "accent": False, "size": "small"}, {"text": "НА КАРТОЧКЕ", "accent": True, "size": "big"}]},
    {"start": 12.10, "end": 13.50, "lines": [{"text": "НЕ АБЗАЦ", "accent": False, "size": "small"}, {"text": "ТЕКСТА", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 15.90, "lines": [{"text": "ПОДХОДИТ", "accent": False, "size": "small"}, {"text": "ВЕЗДЕ", "accent": True, "size": "big"}]},
    {"start": 16.10, "end": 17.20, "lines": [{"text": "ДАЖЕ В", "accent": False, "size": "small"}, {"text": "ОЧЕРЕДИ", "accent": True, "size": "big"}]},
    {"start": 17.50, "end": 19.95, "lines": [{"text": "ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТОЧНЕЕ", "accent": True, "size": "big"}]},
    {"start": 20.00, "end": 20.95, "lines": [{"text": "ЧЕМ АБЗАЦ", "accent": False, "size": "small"}, {"text": "ПЕРЕД СНОМ", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 22.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.85, "end": 3.18}, {"start": 8.10, "end": 8.37}, {"start": 18.57, "end": 18.99}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (sunset boy, 24.800s): per-task timer during mocks shows real
# time spent, helps allocate time on the real exam
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НЕ ЗНАЕШЬ ВРЕМЯ", "НА ЗАДАНИЕ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "НЕДООЦЕНИВАЕШЬ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 5.80, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "ПРОБНИК", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.90, "lines": [{"text": "БЕЗ ПАУЗ", "accent": False, "size": "small"}, {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 8.28, "end": 9.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СЧИТАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.70, "end": 11.00, "lines": [{"text": "ВРЕМЯ ПО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 12.09, "end": 13.60, "lines": [{"text": "ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ГДЕ ДОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 13.70, "end": 14.80, "lines": [{"text": "БОЛЬШЕ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 16.50, "lines": [{"text": "РАСКЛАДКА", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 18.05, "lines": [{"text": "РАСПРЕДЕЛЯЕТ", "accent": False, "size": "small"}, {"text": "СИЛЫ", "accent": True, "size": "big"}]},
    {"start": 18.12, "end": 19.00, "lines": [{"text": "НА ЭКЗАМЕНЕ", "accent": False, "size": "small"}, {"text": "РЕАЛЬНОМ", "accent": True, "size": "big"}]},
    {"start": 19.32, "end": 20.60, "lines": [{"text": "ВИДНО", "accent": False, "size": "small"}, {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 20.70, "end": 21.80, "lines": [{"text": "ГДЕ", "accent": False, "size": "small"}, {"text": "УСКОРИТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 23.04, "end": 24.70, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.20, "end": 1.77}, {"start": 8.91, "end": 9.18}, {"start": 21.36, "end": 21.75}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (girl, 32.066s): confuse stress marks and terms despite knowing
# the topic; targeted mini-games per micro-topic instead of one mixed test
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПУТАЕШЬ УДАРЕНИЯ", "И ТЕРМИНЫ?"], "end": 2.3}
d_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ЗНАЕШЬ ТЕМУ", "accent": False, "size": "small"}, {"text": "НО ПУТАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.20, "lines": [{"text": "УДАРЕНИЯ И", "accent": False, "size": "small"}, {"text": "ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 5.55, "end": 7.20, "lines": [{"text": "КАК И", "accent": False, "size": "small"}, {"text": "ВСЕ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 9.00, "lines": [{"text": "ФОРМАЛЬНО", "accent": False, "size": "small"}, {"text": "ЗНАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 11.60, "lines": [{"text": "НО НЕ", "accent": False, "size": "small"}, {"text": "УВЕРЕН", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 14.00, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 16.75, "lines": [{"text": "НА КАЖДУЮ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 19.00, "lines": [{"text": "УДАРЕНИЯ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 19.10, "end": 20.85, "lines": [{"text": "ТЕРМИНЫ И", "accent": False, "size": "small"}, {"text": "ДАТЫ", "accent": True, "size": "big"}]},
    {"start": 21.42, "end": 23.90, "lines": [{"text": "НЕ ОДИН", "accent": False, "size": "small"}, {"text": "ОБЩИЙ ТЕСТ", "accent": True, "size": "big"}]},
    {"start": 24.81, "end": 26.30, "lines": [{"text": "ТОЧЕЧНАЯ ИГРА", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 26.40, "end": 27.90, "lines": [{"text": "КОНКРЕТНЫЙ", "accent": False, "size": "small"}, {"text": "ПРОБЕЛ", "accent": True, "size": "big"}]},
    {"start": 28.00, "end": 29.50, "lines": [{"text": "БЫСТРЕЕ", "accent": False, "size": "small"}, {"text": "ПАРАГРАФА", "accent": True, "size": "big"}]},
    {"start": 30.18, "end": 32.00, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.70, "end": 2.94}, {"start": 13.47, "end": 13.68}, {"start": 25.86, "end": 26.22}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (sunset boy, 26.135s): prepping only "when you remember" fails;
# the app auto-schedules daily missions instead of relying on memory
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ГОТОВИШЬСЯ ТОЛЬКО", "КОГДА ВСПОМНИШЬ?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "РАСПИСАНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 5.80, "lines": [{"text": "НАПОМИНАНИЙ", "accent": False, "size": "small"}, {"text": "НЕТ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.70, "lines": [{"text": "КАЖДЫЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.50, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "САМ РЕШАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.10, "lines": [{"text": "ЕЖЕДНЕВНЫЕ", "accent": False, "size": "small"}, {"text": "МИССИИ", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 13.50, "lines": [{"text": "ИГРА ИЛИ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.40, "lines": [{"text": "НЕ НАДО", "accent": False, "size": "small"}, {"text": "ПОМНИТЬ", "accent": True, "size": "big"}]},
    {"start": 15.69, "end": 18.50, "lines": [{"text": "ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "САМ", "accent": True, "size": "big"}]},
    {"start": 18.81, "end": 20.60, "lines": [{"text": "БЕЗ РОДИТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "И УЧИТЕЛЕЙ", "accent": True, "size": "big"}]},
    {"start": 20.88, "end": 23.95, "lines": [{"text": "ЗАДАЕТ", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 24.30, "end": 26.00, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.90, "end": 4.23}, {"start": 11.04, "end": 11.34}, {"start": 21.84, "end": 22.32}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (gray boy, 24.087s): checking answers against the key skips the
# reasoning; step-by-step video solutions stick better
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СВЕРЯЕШЬ ОТВЕТ", "ТОЛЬКО ПО КЛЮЧУ?"], "end": 2.3}
f_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "НЕ ПЕРЕСЧИТЫВАЯ", "accent": False, "size": "small"}, {"text": "ХОД", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 5.60, "lines": [{"text": "ОТ НАЧАЛА", "accent": False, "size": "small"}, {"text": "ДО КОНЦА", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.55, "lines": [{"text": "ЦЕЛИКОМ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.20, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДОБАВЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.15, "lines": [{"text": "К ЗАДАНИЮ", "accent": False, "size": "small"}, {"text": "ВИДЕО", "accent": True, "size": "big"}]},
    {"start": 10.17, "end": 12.30, "lines": [{"text": "ПО ШАГАМ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 12.48, "end": 14.50, "lines": [{"text": "НЕ МОЛЧА", "accent": False, "size": "small"}, {"text": "СВЕРКА", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.95, "lines": [{"text": "ПЕРЕСМОТРЕТЬ", "accent": False, "size": "small"}, {"text": "СНОВА", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 18.70, "lines": [{"text": "СТОЛЬКО РАЗ", "accent": False, "size": "small"}, {"text": "СКОЛЬКО НУЖНО", "accent": True, "size": "big"}]},
    {"start": 18.99, "end": 22.15, "lines": [{"text": "ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТОЧНЕЕ", "accent": True, "size": "big"}]},
    {"start": 22.35, "end": 24.00, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.14, "end": 1.41}, {"start": 8.61, "end": 8.94}, {"start": 19.62, "end": 20.04}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (sunset boy, 35.991s): olympiad kids prep for EGE alone, no
# rival nearby; the app's friends list and rating brings competition back
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ГОТОВИШЬСЯ К ЕГЭ", "В ОДИНОЧКУ?"], "end": 2.3}
g_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ГОТОВИШЬСЯ", "accent": False, "size": "small"}, {"text": "ОДИН", "accent": True, "size": "big"}]},
    {"start": 5.34, "end": 6.90, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "СОПЕРНИКА", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 9.00, "lines": [{"text": "СОРЕВНОВАНИЯ", "accent": False, "size": "small"}, {"text": "МОТИВИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 11.95, "lines": [{"text": "ДОЛЬШЕ ВСЕГО", "accent": False, "size": "small"}, {"text": "СРЕДИ СВОИХ", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.30, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДРУЗЬЯ", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 16.30, "lines": [{"text": "ОБЩИЙ", "accent": False, "size": "small"}, {"text": "РЕЙТИНГ", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 18.10, "lines": [{"text": "МЕСТО МЕНЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ЗА ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 19.95, "end": 21.65, "lines": [{"text": "И ЗА", "accent": False, "size": "small"}, {"text": "МИССИЮ", "accent": True, "size": "big"}]},
    {"start": 22.47, "end": 24.00, "lines": [{"text": "ДРУЗЕЙ", "accent": False, "size": "small"}, {"text": "ИЗ КЛАССА", "accent": True, "size": "big"}]},
    {"start": 24.10, "end": 26.70, "lines": [{"text": "ИЛИ", "accent": False, "size": "small"}, {"text": "КРУЖКА", "accent": True, "size": "big"}]},
    {"start": 27.69, "end": 29.00, "lines": [{"text": "ПОДТАЛКИВАЕТ", "accent": False, "size": "small"}, {"text": "ЗАНИМАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 29.10, "end": 30.50, "lines": [{"text": "ЧАЩЕ", "accent": False, "size": "small"}, {"text": "КАЖДЫЙ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 30.93, "end": 33.05, "lines": [{"text": "НЕ МЫСЛЬ", "accent": False, "size": "small"}, {"text": "О ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 34.05, "end": 35.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 4.56, "end": 4.89}, {"start": 15.93, "end": 16.20}, {"start": 28.98, "end": 29.49}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (gray boy, 24.663s): tutor prices in the class chat scare
# everyone; the same task bank and review is free
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ЦЕНЫ НА РЕПЕТИТОРА", "ПУГАЮТ?"], "end": 2.3}
h_cards = [
    {"start": 2.60, "end": 3.95, "lines": [{"text": "ЦЕНЫ В ЧАТЕ", "accent": False, "size": "small"}, {"text": "ПУГАЮТ", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 5.60, "lines": [{"text": "СУММА ЗА", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.05, "lines": [{"text": "БОЛЬШЕ", "accent": False, "size": "small"}, {"text": "КАРМАННЫХ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.10, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ТОТ ЖЕ БАНК", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 10.60, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "БЕСПЛАТНО", "accent": True, "size": "big"}]},
    {"start": 10.77, "end": 12.30, "lines": [{"text": "БЕЗ РУБЛЯ", "accent": False, "size": "small"}, {"text": "ЗА ЧАС", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 14.15, "lines": [{"text": "ИЛИ", "accent": False, "size": "small"}, {"text": "ЗА ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 14.46, "end": 16.00, "lines": [{"text": "ЭКОНОМИЯ", "accent": False, "size": "small"}, {"text": "ЗАМЕТНА", "accent": True, "size": "big"}]},
    {"start": 16.14, "end": 18.70, "lines": [{"text": "ЕСЛИ ПРЕДМЕТОВ", "accent": False, "size": "small"}, {"text": "НЕСКОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 18.99, "end": 20.30, "lines": [{"text": "БЕСПЛАТНЫЙ", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 20.40, "end": 22.55, "lines": [{"text": "ЗАМЕНЯЕТ", "accent": False, "size": "small"}, {"text": "ПЛАТНЫЙ ЧАС", "accent": True, "size": "big"}]},
    {"start": 22.86, "end": 24.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.15, "end": 3.54}, {"start": 10.20, "end": 10.56}, {"start": 18.99, "end": 19.38}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (girl, 26.007s): random topic picking before EGE with no
# system; smart suggestion by mistake-stats beats a coin flip
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ВЫБИРАЕШЬ ТЕМУ", "НАУГАД?"], "end": 2.3}
i_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "СИСТЕМЫ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.60, "lines": [{"text": "КАЖДЫЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 6.95, "lines": [{"text": "ОДНО И", "accent": False, "size": "small"}, {"text": "ТО ЖЕ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "САМ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.70, "lines": [{"text": "ПОДСКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 9.81, "end": 11.10, "lines": [{"text": "ПО СТАТИСТИКЕ", "accent": False, "size": "small"}, {"text": "ОШИБОК", "accent": True, "size": "big"}]},
    {"start": 11.20, "end": 13.25, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНО", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 15.00, "lines": [{"text": "ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 15.10, "end": 17.05, "lines": [{"text": "СПИСКОМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 17.22, "end": 18.70, "lines": [{"text": "ЭКОНОМИТ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 18.80, "end": 20.50, "lines": [{"text": "НЕ НАДО", "accent": False, "size": "small"}, {"text": "ДУМАТЬ", "accent": True, "size": "big"}]},
    {"start": 20.79, "end": 22.75, "lines": [{"text": "ПОРЯДОК", "accent": False, "size": "small"}, {"text": "СТАТИСТИКА", "accent": True, "size": "big"}]},
    {"start": 22.86, "end": 24.05, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "МОНЕТА", "accent": True, "size": "big"}]},
    {"start": 24.24, "end": 25.95, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.94, "end": 3.30}, {"start": 10.86, "end": 11.25}, {"start": 22.26, "end": 22.68}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
