#!/usr/bin/env python3
"""One-off authoring + validation script for the EIGHTH 'coffee123' batch
(9 episodes uploaded under the same tag after seven prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes51/.

Only the two returning boy hosts this time (gray-bedroom boy, sunset-window
boy) - no girl or mom clips in this drop. Content is app-feature focused
again (narrowing an overloaded evening to one weak-topic task, auto-pruning
retired exam tasks, targeted confusable-term drills, per-task timing after
mocks, inline video walkthroughs, month-over-month mistake stats, a
per-mistake review section, offline access at olympiad camp, flashcards
replacing hand-copied paragraphs).
"""
import json

REAL_DURATION = {
    "a": 27.308, "b": 25.068, "c": 25.772,
    "d": 28.440, "e": 25.120, "f": 27.778,
    "g": 27.095, "h": 26.455, "i": 27.031,
}
SOURCE_FILE = {
    "a": "14_09_-_1_2160p11111111111111111", "b": "14_09_-_2_2160p2222222222222222222222222", "c": "14_09_-_3_2160p33333333333333",
    "d": "14_09_13_-_1_2160p111111", "e": "14_09_13_-_1_2160p1111111111", "f": "14_09_13_-_2_2160p22222",
    "g": "14_09_13_-_2_2160p222222222", "h": "14_09_13_-_3_2160p33333", "i": "14_09_13_-_3_2160p333333333",
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
    words = json.load(open(f"../asr_coffee123_8/{src}_words.json"))
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
# Episode A (gray-boy, 27.308s): planning to hit every subject in one
# evening and quitting after 10 minutes; the app narrows it to one short
# task picked from the weakest topic
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВСЕ ПРЕДМЕТЫ", "ЗА ОДИН ВЕЧЕР?"], "end": 2.3}
a_cards = [
    {"start": 2.61, "end": 4.10, "lines": [{"text": "ВСЕ ПРЕДМЕТЫ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 4.29, "end": 5.15, "lines": [{"text": "ЗА ОДИН", "accent": False, "size": "small"}, {"text": "ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.70, "lines": [{"text": "БРОСАЕШЬ", "accent": False, "size": "small"}, {"text": "ДЕСЯТЬ МИНУТ", "accent": True, "size": "big"}]},
    {"start": 7.41, "end": 8.80, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СУЖАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.90, "end": 10.50, "lines": [{"text": "ДО ОДНОГО", "accent": False, "size": "small"}, {"text": "ДЕЛА", "accent": True, "size": "big"}]},
    {"start": 10.71, "end": 12.05, "lines": [{"text": "ВМЕСТО ВСЕХ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТОВ", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 14.25, "lines": [{"text": "ПО СЛАБОЙ", "accent": False, "size": "small"}, {"text": "ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 14.46, "end": 16.25, "lines": [{"text": "НЕ СЛУЧАЙНО", "accent": False, "size": "small"}, {"text": "ПО ПЛАНУ", "accent": True, "size": "big"}]},
    {"start": 16.77, "end": 18.00, "lines": [{"text": "СЛАБАЯ ТЕМА", "accent": False, "size": "small"}, {"text": "ПО ОШИБКАМ", "accent": True, "size": "big"}]},
    {"start": 18.10, "end": 19.35, "lines": [{"text": "НЕДАВНЯЯ", "accent": False, "size": "small"}, {"text": "СТАТИСТИКА", "accent": True, "size": "big"}]},
    {"start": 19.59, "end": 20.75, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "НАУГАД", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 23.30, "lines": [{"text": "КОРОТКИЙ ПУНКТ", "accent": False, "size": "small"}, {"text": "ДЕРЖИТСЯ", "accent": True, "size": "big"}]},
    {"start": 23.43, "end": 24.95, "lines": [{"text": "ДОЛЬШЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "ПЛАН СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 25.56, "end": 27.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.37, "end": 5.73}, {"start": 8.49, "end": 8.73}, {"start": 18.45, "end": 18.87}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (gray-boy, 25.068s): checking against last year's compilation
# and finding a retired task; the app auto-removes tasks no longer on the
# exam from the bank
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СВЕРЯЕШЬ С", "ПРОШЛОГОДНИМ ВАРИАНТОМ?"], "end": 2.3}
b_cards = [
    {"start": 2.55, "end": 3.70, "lines": [{"text": "СВЕРЯЕШЬ", "accent": False, "size": "small"}, {"text": "СБОРНИК", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 5.20, "lines": [{"text": "НАХОДИШЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 5.30, "end": 6.50, "lines": [{"text": "КОТОРОГО", "accent": False, "size": "small"}, {"text": "УЖЕ НЕТ", "accent": True, "size": "big"}]},
    {"start": 6.75, "end": 8.10, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "УБИРАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.80, "lines": [{"text": "ИЗ БАНКА", "accent": False, "size": "small"}, {"text": "СТАРОЕ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 11.10, "lines": [{"text": "НЕТ В", "accent": False, "size": "small"}, {"text": "ВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 13.20, "lines": [{"text": "СБОРНИК", "accent": False, "size": "small"}, {"text": "НЕ НУЖЕН", "accent": True, "size": "big"}]},
    {"start": 13.30, "end": 14.55, "lines": [{"text": "ДЛЯ", "accent": False, "size": "small"}, {"text": "СВЕРКИ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.60, "lines": [{"text": "ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ПРОПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.22, "end": 19.10, "lines": [{"text": "УВЕДОМЛЕНИЯ", "accent": False, "size": "small"}, {"text": "БЕЗ", "accent": True, "size": "big"}]},
    {"start": 19.47, "end": 21.25, "lines": [{"text": "ЧЕГО НЕТ", "accent": False, "size": "small"}, {"text": "НА ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 21.48, "end": 23.15, "lines": [{"text": "НЕ ОТНИМАЕТ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 23.37, "end": 24.95, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.50, "end": 1.77}, {"start": 7.56, "end": 7.83}, {"start": 15.78, "end": 16.08}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (gray-boy, 25.772s): confusing similar social-studies terms on
# every other test; the app builds a mini-game for exactly those confusable
# pairs
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПУТАЕШЬ ПОХОЖИЕ", "ТЕРМИНЫ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 3.70, "lines": [{"text": "ПОХОЖИЕ", "accent": False, "size": "small"}, {"text": "ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 3.78, "end": 5.30, "lines": [{"text": "НА КАЖДОЙ", "accent": False, "size": "small"}, {"text": "РАБОТЕ", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 7.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ИГРА", "accent": True, "size": "big"}]},
    {"start": 7.70, "end": 9.80, "lines": [{"text": "ИЗ ПОХОЖИХ", "accent": False, "size": "small"}, {"text": "ТЕРМИНОВ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 11.85, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ВСЯ ТЕМА", "accent": True, "size": "big"}]},
    {"start": 12.06, "end": 13.60, "lines": [{"text": "В ПАРЕ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ТЕ", "accent": True, "size": "big"}]},
    {"start": 13.70, "end": 15.40, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ПУТАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 15.72, "end": 17.40, "lines": [{"text": "ПАРА", "accent": False, "size": "small"}, {"text": "МЕНЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 17.46, "end": 19.90, "lines": [{"text": "КОГДА НЕ", "accent": False, "size": "small"}, {"text": "ЗАПУТЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 20.19, "end": 21.95, "lines": [{"text": "ПРОЯСНЯЮТСЯ", "accent": False, "size": "small"}, {"text": "БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 22.32, "end": 23.80, "lines": [{"text": "ЗА ОДНУ", "accent": False, "size": "small"}, {"text": "РАБОТУ", "accent": True, "size": "big"}]},
    {"start": 24.03, "end": 25.70, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.50, "end": 1.71}, {"start": 7.05, "end": 7.32}, {"start": 16.71, "end": 17.04}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (sunset-boy, 28.440s): solving calmly at home without noticing
# time per task; the app flags whichever task ran long after a mock
# ---------------------------------------------------------------------------
d_intro = {"lines": ["НЕ ЗАМЕЧАЕШЬ", "СКОЛЬКО ВРЕМЕНИ УХОДИТ?"], "end": 2.3}
d_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "РЕШАЕШЬ", "accent": False, "size": "small"}, {"text": "СПОКОЙНО", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 5.35, "lines": [{"text": "НЕ ЗАМЕЧАЕШЬ", "accent": False, "size": "small"}, {"text": "МИНУТЫ", "accent": True, "size": "big"}]},
    {"start": 5.46, "end": 7.30, "lines": [{"text": "НА КАЖДОЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 9.05, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ОТМЕЧАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.30, "lines": [{"text": "ГДЕ", "accent": False, "size": "small"}, {"text": "ДОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 10.40, "end": 12.65, "lines": [{"text": "ЗАДЕРЖАЛСЯ", "accent": False, "size": "small"}, {"text": "СРЕДНЕГО", "accent": True, "size": "big"}]},
    {"start": 12.93, "end": 15.20, "lines": [{"text": "СРАЗУ", "accent": False, "size": "small"}, {"text": "ПОСЛЕ ПРОБНИКА", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 17.00, "lines": [{"text": "СЕКУНДОМЕРА", "accent": False, "size": "small"}, {"text": "БЕЗ", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 19.90, "lines": [{"text": "НЕ ПРОПАДАЕТ", "accent": False, "size": "small"}, {"text": "НИКОГДА", "accent": True, "size": "big"}]},
    {"start": 20.01, "end": 21.95, "lines": [{"text": "ОСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "ДОСТУПНОЙ", "accent": True, "size": "big"}]},
    {"start": 22.14, "end": 23.90, "lines": [{"text": "МЕДЛЕННОЕ", "accent": False, "size": "small"}, {"text": "НАХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 24.12, "end": 26.45, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕСЧЕТА", "accent": True, "size": "big"}]},
    {"start": 26.64, "end": 28.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.32, "end": 4.62}, {"start": 8.31, "end": 8.61}, {"start": 18.15, "end": 18.48}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (gray-boy, 25.120s): looking at the answer key without seeing
# the logic; the app attaches a video walkthrough right in the task card
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СМОТРИШЬ ОТВЕТ", "БЕЗ ЛОГИКИ?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 3.95, "lines": [{"text": "СМОТРИШЬ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 4.85, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 5.04, "end": 6.30, "lines": [{"text": "НЕ РАЗБИРАЕШЬСЯ", "accent": False, "size": "small"}, {"text": "ОТКУДА", "accent": True, "size": "big"}]},
    {"start": 6.40, "end": 7.60, "lines": [{"text": "САМА", "accent": False, "size": "small"}, {"text": "ЛОГИКА", "accent": True, "size": "big"}]},
    {"start": 8.31, "end": 9.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВИДЕО", "accent": True, "size": "big"}]},
    {"start": 9.70, "end": 11.90, "lines": [{"text": "РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 13.35, "lines": [{"text": "ОТ УСЛОВИЯ", "accent": False, "size": "small"}, {"text": "ДО ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 13.68, "end": 15.40, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "МОЛЧА", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 17.70, "lines": [{"text": "ВИДЕО", "accent": False, "size": "small"}, {"text": "В КАРТОЧКЕ", "accent": True, "size": "big"}]},
    {"start": 17.88, "end": 18.70, "lines": [{"text": "РЯДОМ С", "accent": False, "size": "small"}, {"text": "УСЛОВИЕМ", "accent": True, "size": "big"}]},
    {"start": 18.96, "end": 20.75, "lines": [{"text": "ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "ЛОГИКА", "accent": True, "size": "big"}]},
    {"start": 20.94, "end": 23.10, "lines": [{"text": "НЕ ОДНА", "accent": False, "size": "small"}, {"text": "ЦИФРА", "accent": True, "size": "big"}]},
    {"start": 23.37, "end": 25.00, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.20, "end": 1.44}, {"start": 8.94, "end": 9.36}, {"start": 19.77, "end": 20.19}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (sunset-boy, 27.778s): feeling like a topic is mastered until
# seeing the mistake stats; the app compares this month vs last month by
# topic
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ДУМАЕШЬ ЧТО", "РАЗОБРАЛСЯ?"], "end": 2.3}
f_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "УВЕРЕН ЧТО", "accent": False, "size": "small"}, {"text": "РАЗОБРАЛСЯ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 6.35, "lines": [{"text": "ПОКА НЕ УВИДИШЬ", "accent": False, "size": "small"}, {"text": "СТАТИСТИКУ", "accent": True, "size": "big"}]},
    {"start": 6.81, "end": 8.20, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СРАВНИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.30, "end": 9.75, "lines": [{"text": "РЕЗУЛЬТАТ ПО", "accent": False, "size": "small"}, {"text": "ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 11.50, "lines": [{"text": "С ПРОШЛЫМ", "accent": False, "size": "small"}, {"text": "МЕСЯЦЕМ", "accent": True, "size": "big"}]},
    {"start": 11.79, "end": 14.10, "lines": [{"text": "РАЗНИЦА", "accent": False, "size": "small"}, {"text": "ОДНОЙ СТРОКОЙ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 16.05, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕСЧЕТА", "accent": True, "size": "big"}]},
    {"start": 16.35, "end": 18.50, "lines": [{"text": "ПО КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 18.66, "end": 21.30, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "УСРЕДНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 21.60, "end": 24.40, "lines": [{"text": "ПРОВЕРЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ОЩУЩЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 24.63, "end": 25.85, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ПАМЯТЬЮ", "accent": True, "size": "big"}]},
    {"start": 26.04, "end": 27.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.77, "end": 2.16}, {"start": 7.59, "end": 7.98}, {"start": 19.98, "end": 20.46}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (gray-boy, 27.095s): forgetting which task had the mistake
# right after a quiz; the app keeps every mistake in its own section
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ЗАБЫВАЕШЬ ГДЕ", "БЫЛА ОШИБКА?"], "end": 2.3}
g_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "РЕШАЕШЬ КОНТРОЛЬНУЮ", "accent": False, "size": "small"}, {"text": "РАБОТУ", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 4.80, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ЗАБЫВАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 7.50, "lines": [{"text": "ГДЕ БЫЛА", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.90, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СОХРАНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.55, "lines": [{"text": "КАЖДУЮ ОШИБКУ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 10.77, "end": 12.30, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "ЗАБЫТОГО", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 14.55, "lines": [{"text": "РАЗДЕЛ", "accent": False, "size": "small"}, {"text": "ЗА ОДИН КЛИК", "accent": True, "size": "big"}]},
    {"start": 14.73, "end": 16.90, "lines": [{"text": "ПО КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 17.13, "end": 18.70, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ОТКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 18.72, "end": 20.75, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПОИСКА", "accent": True, "size": "big"}]},
    {"start": 21.03, "end": 23.30, "lines": [{"text": "ОШИБКА", "accent": False, "size": "small"}, {"text": "ДОСТУПНА", "accent": True, "size": "big"}]},
    {"start": 23.43, "end": 25.15, "lines": [{"text": "СПУСТЯ", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 25.32, "end": 26.95, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 4.89, "end": 5.19}, {"start": 8.25, "end": 8.70}, {"start": 22.29, "end": 22.62}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (sunset-boy, 26.455s): losing access to tasks at olympiad camp
# with spotty internet; the app has everything pre-saved, no re-download
# ---------------------------------------------------------------------------
h_intro = {"lines": ["БЕЗ ИНТЕРНЕТА", "НА СБОРАХ?"], "end": 2.3}
h_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "БЕЗ ДОСТУПА", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.20, "lines": [{"text": "В ЛАГЕРЕ", "accent": False, "size": "small"}, {"text": "НА СБОРАХ", "accent": True, "size": "big"}]},
    {"start": 5.30, "end": 6.95, "lines": [{"text": "ИНТЕРНЕТ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "У КОРПУСА", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 8.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.70, "lines": [{"text": "СОХРАНЕННОЕ", "accent": False, "size": "small"}, {"text": "УЖЕ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 11.30, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ОБРАЩЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.70, "lines": [{"text": "К СЕТИ", "accent": False, "size": "small"}, {"text": "КОРПУСА", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 15.50, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 17.10, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ЗАГРУЗКИ", "accent": True, "size": "big"}]},
    {"start": 17.31, "end": 19.55, "lines": [{"text": "ДОСТУП", "accent": False, "size": "small"}, {"text": "НА ВЕСЬ СРОК", "accent": True, "size": "big"}]},
    {"start": 19.68, "end": 21.20, "lines": [{"text": "НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ПЕРВЫЙ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 21.45, "end": 24.45, "lines": [{"text": "СБОРЫ БЕЗ СЕТИ", "accent": False, "size": "small"}, {"text": "БЕЗ ПАУЗЫ", "accent": True, "size": "big"}]},
    {"start": 24.66, "end": 26.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 1.53, "end": 1.80}, {"start": 8.07, "end": 8.40}, {"start": 17.94, "end": 18.39}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (gray-boy, 27.031s): copying whole paragraphs by hand before the
# exam; the app replaces the notebook with short flashcards
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ПЕРЕПИСЫВАЕШЬ", "ЦЕЛЫЙ ПАРАГРАФ?"], "end": 2.3}
i_cards = [
    {"start": 2.60, "end": 3.85, "lines": [{"text": "КОНСПЕКТИРУЕШЬ", "accent": False, "size": "small"}, {"text": "ОТ РУКИ", "accent": True, "size": "big"}]},
    {"start": 4.14, "end": 5.05, "lines": [{"text": "ХОТЯ", "accent": False, "size": "small"}, {"text": "НУЖНО", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 7.65, "lines": [{"text": "ВСЕГО", "accent": False, "size": "small"}, {"text": "ПАРА СТРОК", "accent": True, "size": "big"}]},
    {"start": 7.98, "end": 10.15, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ЗАМЕНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 10.17, "end": 11.10, "lines": [{"text": "КОНСПЕКТ", "accent": False, "size": "small"}, {"text": "КАРТОЧКАМИ", "accent": True, "size": "big"}]},
    {"start": 11.28, "end": 13.15, "lines": [{"text": "ГЛАВНОЕ", "accent": False, "size": "small"}, {"text": "НА ЭКРАНЕ", "accent": True, "size": "big"}]},
    {"start": 13.38, "end": 14.85, "lines": [{"text": "ПОВТОРИТЬ", "accent": False, "size": "small"}, {"text": "ЗА МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 17.15, "lines": [{"text": "ПЕРЕПИСЫВАНИЯ", "accent": False, "size": "small"}, {"text": "ВМЕСТО", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 20.00, "lines": [{"text": "ДЛЯ ПАУЗЫ", "accent": False, "size": "small"}, {"text": "МЕЖДУ УРОКОВ", "accent": True, "size": "big"}]},
    {"start": 20.16, "end": 21.05, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ДОРОГИ", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 23.30, "lines": [{"text": "ПАРА СТРОК", "accent": False, "size": "small"}, {"text": "ЭКОНОМИТ", "accent": True, "size": "big"}]},
    {"start": 23.49, "end": 25.00, "lines": [{"text": "ВЕРНЕЕ", "accent": False, "size": "small"}, {"text": "ЛИСТА", "accent": True, "size": "big"}]},
    {"start": 25.26, "end": 26.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 1.14, "end": 1.71}, {"start": 8.76, "end": 9.09}, {"start": 22.71, "end": 22.98}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
