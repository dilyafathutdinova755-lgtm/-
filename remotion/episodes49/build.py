#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTH 'coffee123' batch
(6 episodes uploaded under the same tag after five prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes49/.

Two brand-new hosts this time (neither matches any earlier coffee123 cast):
a mother in a bookshelf-lined room, speaking to parents about the app; and
a young woman in a warm-lit room, speaking as a student about her own study
habits. Content is app-feature focused, split cleanly by speaker: the mom's
three clips address parents (tutor cost, exam-time pacing, hidden mistake
stats); the student's three clips address her own habits (copying answer
keys, ignoring old mistakes, cramming the night before).
"""
import json

REAL_DURATION = {
    "a": 30.487, "b": 29.122, "c": 27.415,
    "d": 27.031, "e": 32.663, "f": 28.674,
}
SOURCE_FILE = {
    "a": "12_09_-_1__2160p", "b": "12_09_-_1_2160p", "c": "12_09_-_2_2160p",
    "d": "12_09_-_3_21_60p", "e": "12_09_-_3_2160p", "f": "default",
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
    words = json.load(open(f"../asr_coffee123_6/{src}_words.json"))
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
# Episode A (mom, 30.487s): parents budget separate tutors per subject; the
# app gives free access to the task bank across every subject at once
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПЛАТИШЬ ЗА РЕПЕТИТОРА", "ПО КАЖДОМУ ПРЕДМЕТУ?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ОТДЕЛЬНЫЙ", "accent": False, "size": "small"}, {"text": "БЮДЖЕТ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.60, "lines": [{"text": "НА РЕПЕТИТОРЫ", "accent": False, "size": "small"}, {"text": "ПОЧТИ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 6.90, "lines": [{"text": "ПО КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.20, "lines": [{"text": "ЕСЛИ ПРЕДМЕТОВ", "accent": False, "size": "small"}, {"text": "НЕСКОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 8.30, "end": 10.30, "lines": [{"text": "ОДНОВРЕМЕННО", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 11.07, "end": 12.40, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "БЕСПЛАТНО", "accent": True, "size": "big"}]},
    {"start": 12.50, "end": 13.90, "lines": [{"text": "ДОСТУП К", "accent": False, "size": "small"}, {"text": "БАНКУ", "accent": True, "size": "big"}]},
    {"start": 14.00, "end": 15.60, "lines": [{"text": "ПО ВСЕМ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТАМ", "accent": True, "size": "big"}]},
    {"start": 15.70, "end": 17.00, "lines": [{"text": "ШКОЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ПРОГРАММЫ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.50, "lines": [{"text": "БЕЗ ОПЛАТЫ", "accent": False, "size": "small"}, {"text": "ЗА КАЖДЫЙ", "accent": True, "size": "big"}]},
    {"start": 19.17, "end": 20.50, "lines": [{"text": "ЭКОНОМИЯ", "accent": False, "size": "small"}, {"text": "ЗАМЕТНА", "accent": True, "size": "big"}]},
    {"start": 20.60, "end": 23.55, "lines": [{"text": "ЕСЛИ ПРЕДМЕТОВ", "accent": False, "size": "small"}, {"text": "ЧЕТЫРЕ ПЯТЬ", "accent": True, "size": "big"}]},
    {"start": 24.18, "end": 25.60, "lines": [{"text": "ОДИН БАНК", "accent": False, "size": "small"}, {"text": "ЗАМЕНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 25.70, "end": 28.15, "lines": [{"text": "БЮДЖЕТ НА РЕПЕТИТОРОВ", "accent": False, "size": "small"}, {"text": "ВСЕ", "accent": True, "size": "big"}]},
    {"start": 28.74, "end": 30.45, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.96, "end": 4.35}, {"start": 12.06, "end": 12.48}, {"start": 22.74, "end": 22.92}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (girl, 29.122s): copying answers from solution books skips the
# logic; the app records full video walkthroughs, explained step by step
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СПИСЫВАЕШЬ ОТВЕТЫ", "ИЗ РЕШЕБНИКА?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 4.05, "lines": [{"text": "ЧУЖИЕ ОТВЕТЫ", "accent": False, "size": "small"}, {"text": "ИЗ РЕШЕБНИКА", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 5.80, "lines": [{"text": "НЕ ВИДИШЬ", "accent": False, "size": "small"}, {"text": "ЛОГИКУ", "accent": True, "size": "big"}]},
    {"start": 6.66, "end": 7.60, "lines": [{"text": "КОТОРАЯ", "accent": False, "size": "small"}, {"text": "ПРИВЕЛА", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.50, "lines": [{"text": "НЕ МОЖЕШЬ", "accent": False, "size": "small"}, {"text": "ПОВТОРИТЬ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 11.30, "lines": [{"text": "ПРИЕМ НА", "accent": False, "size": "small"}, {"text": "ПОХОЖЕМ", "accent": True, "size": "big"}]},
    {"start": 12.18, "end": 13.60, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ЗАПИСЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 13.70, "end": 15.90, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "НА ВИДЕО", "accent": True, "size": "big"}]},
    {"start": 16.59, "end": 18.55, "lines": [{"text": "КАЖДЫЙ ШАГ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 18.93, "end": 20.95, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ЦИФРА", "accent": True, "size": "big"}]},
    {"start": 21.84, "end": 23.80, "lines": [{"text": "ПРИЕМ", "accent": False, "size": "small"}, {"text": "УВИДЕННЫЙ", "accent": True, "size": "big"}]},
    {"start": 24.12, "end": 26.50, "lines": [{"text": "УЗНАЕТСЯ", "accent": False, "size": "small"}, {"text": "САМ СОБОЙ", "accent": True, "size": "big"}]},
    {"start": 27.30, "end": 29.10, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.23, "end": 1.56}, {"start": 13.02, "end": 13.50}, {"start": 22.77, "end": 23.16}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (girl, 27.415s): dozens of new tasks but old mistakes never
# revisited; the app keeps every wrong answer in a separate retry list
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НЕ ВОЗВРАЩАЕШЬСЯ", "К ОШИБКАМ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ДЕСЯТКИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 3.93, "end": 5.50, "lines": [{"text": "ВОЗВРАЩАЕШЬСЯ", "accent": False, "size": "small"}, {"text": "НЕТ", "accent": True, "size": "big"}]},
    {"start": 5.61, "end": 6.90, "lines": [{"text": "К ОШИБКАМ", "accent": False, "size": "small"}, {"text": "ЗАБЫТЫМ", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.65, "lines": [{"text": "СЧИТАЯ", "accent": False, "size": "small"}, {"text": "ЗАКРЫТОЙ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 10.20, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "РАЗБОРА", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 13.20, "lines": [{"text": "ОТКЛАДЫВАЕТ", "accent": False, "size": "small"}, {"text": "ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 13.30, "end": 15.20, "lines": [{"text": "В ОТДЕЛЬНЫЙ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 18.10, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ОТКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 18.20, "end": 19.60, "lines": [{"text": "И ПРОЙТИ", "accent": False, "size": "small"}, {"text": "ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 20.31, "end": 22.55, "lines": [{"text": "ВОЗВРАТ", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 22.59, "end": 24.95, "lines": [{"text": "ВЕРНЕЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "НОВЫЕ", "accent": True, "size": "big"}]},
    {"start": 25.68, "end": 27.35, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.23, "end": 1.44}, {"start": 12.66, "end": 13.14}, {"start": 21.63, "end": 21.99}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (mom, 27.031s): the kid knows the material but runs out of time;
# the app runs timed mocks matching the real exam's regulations
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАЕТ ТЕМУ НО", "НЕ УСПЕВАЕТ?"], "end": 2.3}
d_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ЗНАЕТ", "accent": False, "size": "small"}, {"text": "МАТЕРИАЛ", "accent": True, "size": "big"}]},
    {"start": 5.01, "end": 6.50, "lines": [{"text": "НО ТЕРЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ОТ ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.00, "lines": [{"text": "А НЕ ОТ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 12.30, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПРОБНИКИ", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 13.60, "lines": [{"text": "СТРОГО ПО", "accent": False, "size": "small"}, {"text": "РЕГЛАМЕНТУ", "accent": True, "size": "big"}]},
    {"start": 13.70, "end": 15.10, "lines": [{"text": "НАСТОЯЩЕГО", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 15.51, "end": 17.00, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "ТАЙМЕРОМ", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 19.05, "lines": [{"text": "НЕЗАВИСИМО", "accent": False, "size": "small"}, {"text": "ОТ УЧЕНИКА", "accent": True, "size": "big"}]},
    {"start": 19.62, "end": 21.95, "lines": [{"text": "ПРИВЫЧКА УКЛАДЫВАТЬСЯ", "accent": False, "size": "small"}, {"text": "ВОВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 22.26, "end": 24.70, "lines": [{"text": "СНИЖАЕТ", "accent": False, "size": "small"}, {"text": "СТРАХ", "accent": True, "size": "big"}]},
    {"start": 25.29, "end": 26.95, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 5.16, "end": 5.52}, {"start": 13.44, "end": 13.83}, {"start": 24.12, "end": 24.66}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (girl, 32.663s): cramming the whole textbook the night before;
# flashcards show the key point instantly, good for olympiad prep too
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЧИТАЕШЬ УЧЕБНИК", "ЗА ОДИН ВЕЧЕР?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 4.35, "lines": [{"text": "ВЕСЬ", "accent": False, "size": "small"}, {"text": "УЧЕБНИК", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 5.90, "lines": [{"text": "ЗА ОДИН", "accent": False, "size": "small"}, {"text": "ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 5.90, "end": 7.80, "lines": [{"text": "ВМЕСТО ТОГО", "accent": False, "size": "small"}, {"text": "ЧТОБЫ РАЗБИТЬ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 9.85, "lines": [{"text": "РАСПРЕДЕЛИТЬ", "accent": False, "size": "small"}, {"text": "ПО ДНЯМ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.00, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "СПЕШКИ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.70, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.10, "lines": [{"text": "КРАТКИЕ", "accent": False, "size": "small"}, {"text": "ПО ТЕМАМ", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 17.55, "lines": [{"text": "ПЕРЕВЕРНУЛ", "accent": False, "size": "small"}, {"text": "ГЛАВНОЕ", "accent": True, "size": "big"}]},
    {"start": 17.82, "end": 20.70, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕСКАЗА", "accent": True, "size": "big"}]},
    {"start": 21.54, "end": 24.40, "lines": [{"text": "ПОДХОДИТ И ДЛЯ", "accent": False, "size": "small"}, {"text": "ОЛИМПИАДЫ", "accent": True, "size": "big"}]},
    {"start": 24.60, "end": 25.75, "lines": [{"text": "И ДЛЯ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 26.28, "end": 30.20, "lines": [{"text": "МЕНЬШЕ ВРЕМЕНИ", "accent": False, "size": "small"}, {"text": "ЧЕМ ПОИСК", "accent": True, "size": "big"}]},
    {"start": 30.81, "end": 32.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.76, "end": 3.06}, {"start": 14.01, "end": 14.34}, {"start": 23.85, "end": 24.36}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (mom, 28.674s): parents rarely see which topics have the most
# mistakes; the app aggregates stats and surfaces the weak topic
# ---------------------------------------------------------------------------
f_intro = {"lines": ["НЕ ЗНАЕШЬ ГДЕ", "У РЕБЁНКА ОШИБКИ?"], "end": 2.3}
f_cards = [
    {"start": 2.60, "end": 4.20, "lines": [{"text": "ПО КАКИМ", "accent": False, "size": "small"}, {"text": "ТЕМАМ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 6.50, "lines": [{"text": "БОЛЬШЕ ВСЕГО", "accent": False, "size": "small"}, {"text": "ОШИБОК", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 9.45, "lines": [{"text": "СПРОСИТЬ", "accent": False, "size": "small"}, {"text": "БЕСПОЛЕЗНО", "accent": True, "size": "big"}]},
    {"start": 10.17, "end": 11.50, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СТАТИСТИКА", "accent": True, "size": "big"}]},
    {"start": 11.60, "end": 13.35, "lines": [{"text": "ВСЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.20, "lines": [{"text": "ВЫДЕЛЯЕТ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.20, "lines": [{"text": "С НАИБОЛЬШИМ", "accent": False, "size": "small"}, {"text": "ЧИСЛОМ", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 18.35, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "РАЗГОВОРА", "accent": True, "size": "big"}]},
    {"start": 18.93, "end": 21.30, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ВМЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 21.39, "end": 22.65, "lines": [{"text": "ЗА ПАРУ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 23.19, "end": 24.70, "lines": [{"text": "ЦИФРЫ", "accent": False, "size": "small"}, {"text": "СЛАБОЕ МЕСТО", "accent": True, "size": "big"}]},
    {"start": 24.87, "end": 26.50, "lines": [{"text": "ТОЧНЕЕ", "accent": False, "size": "small"}, {"text": "РАЗГОВОРА", "accent": True, "size": "big"}]},
    {"start": 27.03, "end": 28.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.46, "end": 5.70}, {"start": 12.81, "end": 13.32}, {"start": 25.59, "end": 25.95}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
