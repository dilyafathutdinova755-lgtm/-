#!/usr/bin/env python3
"""One-off authoring + validation script for the SEVENTH 'coffee123' batch
(9 episodes uploaded under the same tag after six prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes50/.

All three recurring hosts appear together in this batch for the first time:
the bookshelf girl (episodes47/48), the mother (episodes49), and the
warm-lit-room girl (episodes49). Content is app-feature focused again
(video walkthroughs kept with the task, offline FIPI bank, mistake-repeat
tracking, flashcards vs textbook, weak-topic tracking, timed full mocks,
classmates' progress list, flashcards vs scattered notes, three daily
micro-tasks).
"""
import json

REAL_DURATION = {
    "a": 27.180, "b": 27.692, "c": 32.066,
    "d": 28.226, "e": 30.487, "f": 32.663,
    "g": 29.847, "h": 33.560, "i": 34.263,
}
SOURCE_FILE = {
    "a": "14_09_13_-_1_2160p", "b": "14_09_13_-_1_2160p11", "c": "14_09_13_-_1__2160p111",
    "d": "14_09_13_-_2_2160p", "e": "14_09_13_-_2_2160p22", "f": "14_09_13_-_2_2160p222",
    "g": "14_09_13_-_3_2160p", "h": "14_09_13_-_3_2160p11", "i": "14_09_13_-_3_2160p33",
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
    words = json.load(open(f"../asr_coffee123_7/{src}_words.json"))
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
# Episode A (mom, 27.180s): a corrected grade in the notebook with no
# explanation nearby; the app attaches a video walkthrough kept with the task
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ИСПРАВЛЕННАЯ ОЦЕНКА", "БЕЗ ОБЪЯСНЕНИЯ?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ИСПРАВЛЕННАЯ", "accent": False, "size": "small"}, {"text": "ОЦЕНКА", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.40, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПОМЕТКИ", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 7.00, "lines": [{"text": "НИ ОДНОЙ", "accent": False, "size": "small"}, {"text": "ЗАПИСИ", "accent": True, "size": "big"}]},
    {"start": 7.10, "end": 8.40, "lines": [{"text": "О ХОДЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.50, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВИДЕО", "accent": True, "size": "big"}]},
    {"start": 10.60, "end": 11.90, "lines": [{"text": "К", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 13.60, "lines": [{"text": "РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 13.70, "end": 14.50, "lines": [{"text": "ШАГ ЗА", "accent": False, "size": "small"}, {"text": "ШАГОМ", "accent": True, "size": "big"}]},
    {"start": 14.88, "end": 16.50, "lines": [{"text": "НЕ ОДНА", "accent": False, "size": "small"}, {"text": "ЦИФРА", "accent": True, "size": "big"}]},
    {"start": 17.16, "end": 18.70, "lines": [{"text": "РОЛИК", "accent": False, "size": "small"}, {"text": "ХРАНИТСЯ", "accent": True, "size": "big"}]},
    {"start": 18.87, "end": 20.65, "lines": [{"text": "НЕ ПРОПАДАЕТ", "accent": False, "size": "small"}, {"text": "НИКОГДА", "accent": True, "size": "big"}]},
    {"start": 21.33, "end": 23.30, "lines": [{"text": "ОЦЕНКА", "accent": False, "size": "small"}, {"text": "ПОНЯТНА", "accent": True, "size": "big"}]},
    {"start": 23.40, "end": 24.80, "lines": [{"text": "ЧЕГО РАНЬШЕ", "accent": False, "size": "small"}, {"text": "НЕ БЫЛО", "accent": True, "size": "big"}]},
    {"start": 25.44, "end": 27.10, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.42, "end": 3.96}, {"start": 9.87, "end": 10.29}, {"start": 22.14, "end": 22.59}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (warm-room girl, 27.692s): lose task access without stable
# internet; the app stores the FIPI bank offline, no server request needed
# ---------------------------------------------------------------------------
b_intro = {"lines": ["НЕТ ИНТЕРНЕТА", "НЕТ ЗАНЯТИЯ?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ТЕРЯЕШЬ", "accent": False, "size": "small"}, {"text": "ДОСТУП", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.10, "lines": [{"text": "КАЖДЫЙ РАЗ", "accent": False, "size": "small"}, {"text": "ВМЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.30, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ИНТЕРНЕТА", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 8.15, "lines": [{"text": "ДОМА ИЛИ", "accent": False, "size": "small"}, {"text": "В ШКОЛЕ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.35, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.45, "end": 11.95, "lines": [{"text": "ПРЯМО НА", "accent": False, "size": "small"}, {"text": "УСТРОЙСТВЕ", "accent": True, "size": "big"}]},
    {"start": 12.48, "end": 13.70, "lines": [{"text": "ОТКРЫВАЕТ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.15, "lines": [{"text": "БЕЗ ЗАПРОСА", "accent": False, "size": "small"}, {"text": "К СЕРВЕРУ", "accent": True, "size": "big"}]},
    {"start": 15.81, "end": 17.00, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.45, "lines": [{"text": "ЗАГРУЖАЕТСЯ", "accent": False, "size": "small"}, {"text": "ВМЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 20.70, "lines": [{"text": "НЕ ПРОПАДАЕТ", "accent": False, "size": "small"}, {"text": "БЕЗ СЕТИ", "accent": True, "size": "big"}]},
    {"start": 21.66, "end": 23.00, "lines": [{"text": "МЕСТО", "accent": False, "size": "small"}, {"text": "БЕЗ СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 23.10, "end": 25.10, "lines": [{"text": "НЕ ОТМЕНЯЕТ", "accent": False, "size": "small"}, {"text": "ЗАНЯТИЯ", "accent": True, "size": "big"}]},
    {"start": 25.86, "end": 27.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.14, "end": 1.35}, {"start": 9.93, "end": 10.17}, {"start": 14.25, "end": 14.55}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (bookshelf girl, 32.066s): redo a task right after a mistake but
# never check if the same logic repeats; the app collects mistakes by logic
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ДЕЛАЕШЬ ОШИБКУ", "И ЗАБЫВАЕШЬ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "РАЗБИРАЕШЬ", "accent": False, "size": "small"}, {"text": "ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.55, "lines": [{"text": "И ЗАБЫВАЕШЬ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.60, "lines": [{"text": "НЕ ПРОВЕРЯЕШЬ", "accent": False, "size": "small"}, {"text": "СНОВА", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 9.00, "lines": [{"text": "ТА ЖЕ", "accent": False, "size": "small"}, {"text": "ЛОГИКА", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 10.55, "lines": [{"text": "В ДРУГИХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯХ", "accent": True, "size": "big"}]},
    {"start": 11.43, "end": 12.70, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СОБИРАЕТ", "accent": True, "size": "big"}]},
    {"start": 12.80, "end": 14.55, "lines": [{"text": "ОШИБКУ", "accent": False, "size": "small"}, {"text": "В РАЗДЕЛ", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 16.50, "lines": [{"text": "ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ПОХОЖЕЕ", "accent": True, "size": "big"}]},
    {"start": 16.60, "end": 18.30, "lines": [{"text": "ГДЕ ВСТРЕЧАЛОСЬ", "accent": False, "size": "small"}, {"text": "РАНЬШЕ", "accent": True, "size": "big"}]},
    {"start": 19.08, "end": 20.60, "lines": [{"text": "ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 20.70, "end": 21.85, "lines": [{"text": "ПОСЛЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 22.38, "end": 24.55, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕНОСА", "accent": True, "size": "big"}]},
    {"start": 25.38, "end": 27.50, "lines": [{"text": "ПОВТОРНАЯ", "accent": False, "size": "small"}, {"text": "ЗА МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 27.78, "end": 29.60, "lines": [{"text": "НЕ СЛУЧАЙНО", "accent": False, "size": "small"}, {"text": "НА ОЛИМПИАДЕ", "accent": True, "size": "big"}]},
    {"start": 30.15, "end": 31.95, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.76, "end": 3.09}, {"start": 12.27, "end": 12.63}, {"start": 20.07, "end": 20.55}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (mom, 28.226s): revision postponed to the last evening because
# opening the textbook feels like a chore; short flashcards replace it
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ОТКЛАДЫВАЕТ ДО", "ПОСЛЕДНЕГО ВЕЧЕРА?"], "end": 2.3}
d_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ОТКЛАДЫВАЕТ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 5.55, "lines": [{"text": "ДО", "accent": False, "size": "small"}, {"text": "ВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 7.65, "lines": [{"text": "ТОЛСТЫЙ", "accent": False, "size": "small"}, {"text": "УЧЕБНИК", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 9.00, "lines": [{"text": "ОТКРОВЕННО", "accent": False, "size": "small"}, {"text": "ЛЕНЬ", "accent": True, "size": "big"}]},
    {"start": 10.35, "end": 11.55, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 11.65, "end": 13.60, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "УЧЕБНИКА", "accent": True, "size": "big"}]},
    {"start": 14.13, "end": 15.75, "lines": [{"text": "ГЛАВНОЕ", "accent": False, "size": "small"}, {"text": "НА ЭКРАНЕ", "accent": True, "size": "big"}]},
    {"start": 15.93, "end": 17.15, "lines": [{"text": "ПРОЛИСТЫВАНИЯ", "accent": False, "size": "small"}, {"text": "БЕЗ", "accent": True, "size": "big"}]},
    {"start": 17.70, "end": 20.00, "lines": [{"text": "ПЯТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "ПЕРЕД СНОМ", "accent": True, "size": "big"}]},
    {"start": 20.13, "end": 21.50, "lines": [{"text": "ИЛИ В", "accent": False, "size": "small"}, {"text": "ПЕРЕРЫВЕ", "accent": True, "size": "big"}]},
    {"start": 22.08, "end": 24.50, "lines": [{"text": "БОЛЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "ЦЕЛЫЙ ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 24.63, "end": 25.90, "lines": [{"text": "С УЧЕБНИКОМ", "accent": False, "size": "small"}, {"text": "В РУКАХ", "accent": True, "size": "big"}]},
    {"start": 26.49, "end": 28.15, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.06, "end": 3.45}, {"start": 11.13, "end": 11.46}, {"start": 16.47, "end": 17.10}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (warm-room girl, 30.487s): mixing subjects hides a weak topic;
# the app tracks solved tasks by topic and highlights the weak spot
# ---------------------------------------------------------------------------
e_intro = {"lines": ["НЕ ЗАМЕЧАЕШЬ", "СЛАБУЮ ТЕМУ?"], "end": 2.3}
e_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ПРЕДМЕТЫ", "accent": False, "size": "small"}, {"text": "ВПЕРЕМЕШКУ", "accent": True, "size": "big"}]},
    {"start": 4.68, "end": 6.00, "lines": [{"text": "НЕ ЗАМЕЧАЕШЬ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 7.53, "end": 9.40, "lines": [{"text": "СЛАБЕЕ", "accent": False, "size": "small"}, {"text": "ОСТАЛЬНЫХ", "accent": True, "size": "big"}]},
    {"start": 10.47, "end": 11.70, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "УЧЕТ", "accent": True, "size": "big"}]},
    {"start": 11.80, "end": 13.35, "lines": [{"text": "РЕШЕННЫХ", "accent": False, "size": "small"}, {"text": "ПО ТЕМАМ", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 15.20, "lines": [{"text": "ПОДСВЕЧИВАЕТ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.90, "lines": [{"text": "ЗАМЕТНО", "accent": False, "size": "small"}, {"text": "БОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 17.70, "end": 19.35, "lines": [{"text": "ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "САМ", "accent": True, "size": "big"}]},
    {"start": 19.56, "end": 21.05, "lines": [{"text": "ПОСЛЕ", "accent": False, "size": "small"}, {"text": "ПРОБНИКА", "accent": True, "size": "big"}]},
    {"start": 22.05, "end": 23.20, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕСЧЕТА", "accent": True, "size": "big"}]},
    {"start": 24.24, "end": 25.50, "lines": [{"text": "СЛАБОЕ", "accent": False, "size": "small"}, {"text": "МЕСТО", "accent": True, "size": "big"}]},
    {"start": 25.71, "end": 27.80, "lines": [{"text": "ДО КОНТРОЛЬНОЙ", "accent": False, "size": "small"}, {"text": "РАНЬШЕ", "accent": True, "size": "big"}]},
    {"start": 28.65, "end": 30.40, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.63, "end": 4.11}, {"start": 13.86, "end": 14.52}, {"start": 26.19, "end": 26.49}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (bookshelf girl, 32.663s): combining olympiad and EGE prep means
# rarely trying a full timed mock; the app runs one with a real countdown
# ---------------------------------------------------------------------------
f_intro = {"lines": ["НЕ ПРОБУЕШЬ", "ВАРИАНТ НА ВРЕМЯ?"], "end": 2.3}
f_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "СОВМЕЩАЕШЬ", "accent": False, "size": "small"}, {"text": "ОЛИМПИАДЫ", "accent": True, "size": "big"}]},
    {"start": 4.29, "end": 6.45, "lines": [{"text": "РЕДКО ПРОБУЕШЬ", "accent": False, "size": "small"}, {"text": "НА ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 8.50, "lines": [{"text": "НЕХВАТКА", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 8.60, "end": 10.20, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 11.07, "end": 12.30, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПРОБНИК", "accent": True, "size": "big"}]},
    {"start": 12.40, "end": 14.70, "lines": [{"text": "С ОБРАТНЫМ", "accent": False, "size": "small"}, {"text": "ОТСЧЕТОМ", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 16.60, "lines": [{"text": "НЕ ОСТАНАВЛИВАЕТСЯ", "accent": False, "size": "small"}, {"text": "НИКОГДА", "accent": True, "size": "big"}]},
    {"start": 16.70, "end": 18.25, "lines": [{"text": "ПРОДЛЕВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 19.11, "end": 20.50, "lines": [{"text": "ОДИН", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТ", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 21.80, "lines": [{"text": "ИЛИ", "accent": False, "size": "small"}, {"text": "НЕСКОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 22.00, "end": 23.85, "lines": [{"text": "ПОДРЯД", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 24.30, "end": 25.85, "lines": [{"text": "КАК", "accent": False, "size": "small"}, {"text": "НАСТОЯЩИЙ", "accent": True, "size": "big"}]},
    {"start": 26.55, "end": 27.90, "lines": [{"text": "РАСЧЕТ", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 28.02, "end": 29.95, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "СЮРПРИЗ", "accent": True, "size": "big"}]},
    {"start": 30.63, "end": 32.50, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.44, "end": 2.10}, {"start": 11.94, "end": 12.39}, {"start": 17.16, "end": 17.67}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (mom, 29.847s): the kid drops EGE prep with no one to compare
# results with; the app's classmates progress list brings that back
# ---------------------------------------------------------------------------
g_intro = {"lines": ["БРОСАЕТ ЕГЭ", "БЕЗ СРАВНЕНИЯ?"], "end": 2.3}
g_cards = [
    {"start": 2.60, "end": 3.90, "lines": [{"text": "ЛЕГКО", "accent": False, "size": "small"}, {"text": "БРОСАЕТ", "accent": True, "size": "big"}]},
    {"start": 4.00, "end": 4.85, "lines": [{"text": "ПОДГОТОВКУ", "accent": False, "size": "small"}, {"text": "К ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.28, "end": 6.50, "lines": [{"text": "ЕСЛИ", "accent": False, "size": "small"}, {"text": "НИКОГО", "accent": True, "size": "big"}]},
    {"start": 6.69, "end": 8.00, "lines": [{"text": "НЕ С КЕМ", "accent": False, "size": "small"}, {"text": "СРАВНИТЬ", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 10.20, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 10.30, "end": 11.55, "lines": [{"text": "ОДНОКЛАССНИКОВ", "accent": False, "size": "small"}, {"text": "ВНУТРИ", "accent": True, "size": "big"}]},
    {"start": 11.65, "end": 12.50, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 14.55, "lines": [{"text": "ПРОГРЕСС", "accent": False, "size": "small"}, {"text": "ЗА НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.50, "lines": [{"text": "ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 16.59, "end": 18.95, "lines": [{"text": "КОГДА КТО", "accent": False, "size": "small"}, {"text": "ЗАКРЫЛ", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 21.85, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "СКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 21.93, "end": 23.25, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "НАСТРОЙКАХ", "accent": True, "size": "big"}]},
    {"start": 23.94, "end": 26.10, "lines": [{"text": "ПРОГРЕСС ДРУГИХ", "accent": False, "size": "small"}, {"text": "МОТИВИРУЕТ", "accent": True, "size": "big"}]},
    {"start": 26.19, "end": 27.50, "lines": [{"text": "БОЛЬШЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "РАЗГОВОРЫ", "accent": True, "size": "big"}]},
    {"start": 27.99, "end": 29.75, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 3.57, "end": 3.81}, {"start": 9.66, "end": 9.99}, {"start": 25.02, "end": 25.53}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (warm-room girl, 33.560s): dozens of bookmarks and notes hoarded
# but rarely reopened; short flashcards replace them and work offline too
# ---------------------------------------------------------------------------
h_intro = {"lines": ["КОПИШЬ ЗАКЛАДКИ", "НО НЕ ОТКРЫВАЕШЬ?"], "end": 2.3}
h_cards = [
    {"start": 3.03, "end": 4.20, "lines": [{"text": "КОПИШЬ", "accent": False, "size": "small"}, {"text": "ЗАКЛАДКИ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.75, "lines": [{"text": "И ЗАМЕТКИ", "accent": False, "size": "small"}, {"text": "В ТЕЛЕФОНЕ", "accent": True, "size": "big"}]},
    {"start": 6.18, "end": 7.70, "lines": [{"text": "ОТКРЫВАЕШЬ", "accent": False, "size": "small"}, {"text": "РЕДКО", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 8.90, "lines": [{"text": "ПЕРЕД", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНОМ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 11.20, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 11.30, "end": 12.65, "lines": [{"text": "КОРОТКИЕ", "accent": False, "size": "small"}, {"text": "ПО ТЕМАМ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.80, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "ЗАКЛАДОК", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 16.95, "lines": [{"text": "ОТКРЫТЬ", "accent": False, "size": "small"}, {"text": "ЗА МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 17.16, "end": 19.05, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "ЗАНЯТИЯМИ", "accent": True, "size": "big"}]},
    {"start": 19.41, "end": 21.10, "lines": [{"text": "И ЗАКРЫТЬ", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОН", "accent": True, "size": "big"}]},
    {"start": 21.99, "end": 23.85, "lines": [{"text": "НЕ ТРЕБУЕТ", "accent": False, "size": "small"}, {"text": "ИНТЕРНЕТА", "accent": True, "size": "big"}]},
    {"start": 24.03, "end": 25.45, "lines": [{"text": "ТА ЖЕ", "accent": False, "size": "small"}, {"text": "СКОРОСТЬ", "accent": True, "size": "big"}]},
    {"start": 25.53, "end": 26.65, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ДОРОГЕ", "accent": True, "size": "big"}]},
    {"start": 27.42, "end": 30.95, "lines": [{"text": "ОДНА КАРТОЧКА", "accent": False, "size": "small"}, {"text": "ЗАМЕНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 31.71, "end": 33.45, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.03, "end": 3.30}, {"start": 10.71, "end": 10.95}, {"start": 28.23, "end": 28.53}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (bookshelf girl, 34.263s): opening the app once every few days
# and cramming it all in one sitting; the app suggests three short daily
# tasks instead
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ОТКРЫВАЕШЬ РАЗ", "В НЕСКОЛЬКО ДНЕЙ?"], "end": 2.3}
i_cards = [
    {"start": 2.60, "end": 3.50, "lines": [{"text": "ОТКРЫВАЕШЬ", "accent": False, "size": "small"}, {"text": "РЕДКО", "accent": True, "size": "big"}]},
    {"start": 3.93, "end": 4.85, "lines": [{"text": "РАЗ В", "accent": False, "size": "small"}, {"text": "НЕСКОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.50, "lines": [{"text": "НАВЕРСТЫВАЕШЬ", "accent": False, "size": "small"}, {"text": "ПОТОМ", "accent": True, "size": "big"}]},
    {"start": 6.60, "end": 8.25, "lines": [{"text": "ВСЕ", "accent": False, "size": "small"}, {"text": "ЗА РАЗ", "accent": True, "size": "big"}]},
    {"start": 9.09, "end": 10.40, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ТРИ ДЕЛА", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 12.40, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "СЕГОДНЯ", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.35, "lines": [{"text": "ИГРА", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 14.45, "end": 15.30, "lines": [{"text": "ИЛИ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 15.96, "end": 17.60, "lines": [{"text": "МЕНЬШЕ", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 17.79, "end": 20.60, "lines": [{"text": "ЧЕМ ОДНА", "accent": False, "size": "small"}, {"text": "ПОПЫТКА", "accent": True, "size": "big"}]},
    {"start": 21.51, "end": 24.65, "lines": [{"text": "ОТМЕТКА", "accent": False, "size": "small"}, {"text": "В ПРИЛОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 25.20, "end": 26.70, "lines": [{"text": "БЕЗ СПИСКА", "accent": False, "size": "small"}, {"text": "НА БУМАГЕ", "accent": True, "size": "big"}]},
    {"start": 27.45, "end": 29.90, "lines": [{"text": "ПРОПУСК ДНЕЙ", "accent": False, "size": "small"}, {"text": "НЕ СТРАШЕН", "accent": True, "size": "big"}]},
    {"start": 30.15, "end": 31.25, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ДОЛГОГО ВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 32.19, "end": 34.10, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 1.32, "end": 1.68}, {"start": 10.17, "end": 10.65}, {"start": 28.74, "end": 29.16}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
