#!/usr/bin/env python3
"""One-off authoring + validation script for the SEVENTEENTH 'coffee123'
batch (9 episodes uploaded under the same tag after sixteen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes60/.

Three episodes continue the "выпускники" olympiad thread (brunette
study-room host): per-trap-variant accuracy tracking, a toggleable
trap-variant practice mode, and a separate olympiad-track leaderboard.
Six episodes are new general-audience content split between the two
returning hosts: the mother (parent-addressed "если ребенок...") gets
memorization-game and up-to-date-FIPI-bank episodes, and the blonde
host gets second-person-direct ("готовишься"/"тебе") episodes on the
same two topics plus one on skipping error review. Content: tracking
accuracy specifically on trap/lookalike answer variants instead of one
blended percentage, a toggleable practice mode drilling exactly the
variants students confuse most, a separate leaderboard for the
olympiad track instead of burial among thousands of regular users,
memorization games for humanities subjects instead of re-reading notes,
an up-to-date FIPI-sourced task bank instead of stale internet
collections, and a full text explanation for every wrong answer instead
of just the correct one.
"""
import json

REAL_DURATION = {
    "a": 35.522, "b": 23.000, "c": 34.000,
    "d": 22.850, "e": 33.623, "f": 20.460,
    "g": 23.575, "h": 23.042, "i": 22.000,
}
SOURCE_FILE = {
    "a": "afreterwtfwetgyryery", "b": "dsrfsdteere", "c": "eafstat.vgwrtgt",
    "d": "fdhyshershysha", "e": "fdsfsfdsfsfsfsdf", "f": "gvsdfdhhdj",
    "g": "reytujejesrtuyyshe", "h": "rgeyhefhjnshye", "i": "rtgsrtdgdthdhgd",
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


def fix_words(letter, words):
    """Repair known sherpa-onnx ASR mis-transcriptions before captioning."""
    if letter == "a":
        for w in words:
            if abs(w["start"] - 7.71) < 0.02 and w["text"] == "тренажеро":
                w["text"] = "тренажер"
    if letter == "b":
        for w in words:
            if abs(w["start"] - 11.07) < 0.02 and w["text"] == "обычноя":
                w["text"] = "обычное"
    if letter == "c":
        for w in words:
            if abs(w["start"] - 22.23) < 0.02 and w["text"] == "мне":
                w["text"] = "не"
    if letter == "e":
        for w in words:
            if abs(w["start"] - 18.93) < 0.02 and w["text"] == "тысячемен":
                w["text"] = "тысяч"
        new_words = []
        skip_next = False
        for i, w in enumerate(words):
            if skip_next:
                skip_next = False
                continue
            if abs(w["start"] - 24.39) < 0.02 and w["text"] == "о" and i + 1 < len(words) and words[i + 1]["text"] == "деле":
                new_words.append({"text": "отдельный", "start": w["start"], "end": words[i + 1]["end"]})
                skip_next = True
            else:
                new_words.append(w)
        words = new_words
    if letter == "f":
        new_words = []
        for w in words:
            if abs(w["start"] - 15.78) < 0.02 and w["text"] == "объясняетсяму":
                mid = (w["start"] + w["end"]) / 2
                new_words.append({"text": "объясняет", "start": w["start"], "end": mid})
                new_words.append({"text": "саму", "start": mid, "end": w["end"]})
            else:
                new_words.append(w)
        words = new_words
    if letter == "h":
        for w in words:
            if abs(w["start"] - 1.14) < 0.02 and w["text"] == "еде":
                w["text"] = "егэ"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_17/{src}_words.json"))
    words = fix_words(letter, words)
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
# Episode A (brunette study-room host, 35.522s): olympiad participants see
# one blended accuracy percentage and can't tell which trap/lookalike
# answer variants trip them up; the app tracks accuracy on trap variants
# specifically, updating the moment a new one is answered
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВИДИШЬ ОБЩУЮ ТОЧНОСТЬ", "НЕ ЗНАЕШЬ ЧТО ПУТАЕТ?"], "end": 2.4}
a_cards = [
    {"start": 3.57, "end": 4.71, "lines": [{"text": "ПО ЕГЭ НО", "accent": False, "size": "small"}, {"text": "НЕ ЗНАЮТ", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 6.63, "lines": [{"text": "ИЗ ЗА КАКИХ ВАРИАНТОВ ЧАЩЕ", "accent": False, "size": "small"}, {"text": "ОШИБАЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.50, "end": 8.40, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СЧИТАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.52, "end": 9.33, "lines": [{"text": "ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ТОЧНОСТЬ", "accent": True, "size": "big"}]},
    {"start": 9.48, "end": 11.07, "lines": [{"text": "ИМЕННО ПО ХИТРЫМ", "accent": False, "size": "small"}, {"text": "ПОХОЖИМ ВАРИАНТАМ", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 12.42, "lines": [{"text": "ОТВЕТА А НЕ ПО ВСЕМ", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.70, "lines": [{"text": "ЧИСЛО РЯДОМ НАГЛЯДНО", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.62, "lines": [{"text": "НАСКОЛЬКО ХОРОШО РАСПОЗНАЮТСЯ", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 16.83, "end": 18.21, "lines": [{"text": "ПОХОЖИЕ ВАРИАНТЫ", "accent": False, "size": "small"}, {"text": "СМЕШИВАТЬ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 19.80, "lines": [{"text": "ЛЕГКИЕ ОДНОЗНАЧНЫЕ", "accent": False, "size": "small"}, {"text": "ВОПРОСЫ", "accent": True, "size": "big"}]},
    {"start": 20.13, "end": 21.21, "lines": [{"text": "С НАСТОЯЩИМИ", "accent": False, "size": "small"}, {"text": "ЛОВУШКАМИ", "accent": True, "size": "big"}]},
    {"start": 21.39, "end": 22.98, "lines": [{"text": "В ОДНОМ ПРОЦЕНТЕ НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 23.73, "end": 25.32, "lines": [{"text": "ОТДЕЛЬНОЕ ЧИСЛО ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 25.53, "end": 27.06, "lines": [{"text": "ПОСЛЕ КАЖДОГО НОВОГО", "accent": False, "size": "small"}, {"text": "ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 27.24, "end": 28.53, "lines": [{"text": "НА ТАКОЙ", "accent": False, "size": "small"}, {"text": "ВОПРОС", "accent": True, "size": "big"}]},
    {"start": 29.22, "end": 30.96, "lines": [{"text": "ОТДЕЛЬНОЕ ЧИСЛО ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "НАСКОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 31.17, "end": 33.06, "lines": [{"text": "ХОРОШО РАСПОЗНАЮТСЯ ПОХОЖИЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 33.78, "end": 35.61, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.57, "end": 3.90}, {"start": 7.50, "end": 7.83}, {"start": 33.78, "end": 34.11}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (mother, parent POV, 23.000s): a child prepping for the essay
# subjects (Russian, history, social studies) re-reads notes without a
# stable result; the app has memorization games for these subjects that
# lock material in through active recall instead of re-reading
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЧИТАЕТ КОНСПЕКТ", "ПО КРУГУ?"], "end": 1.65}
b_cards = [
    {"start": 2.13, "end": 4.62, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ ИЛИ ОБЩЕСТВОЗНАНИЯ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 5.07, "end": 7.53, "lines": [{"text": "СТОИТ ОБРАТИТЬ ВНИМАНИЕ НЕ ТОЛЬКО НА КОЛИЧЕСТВО", "accent": False, "size": "small"}, {"text": "ЧАСОВ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 10.26, "lines": [{"text": "А НА ТО КАК ИМЕННО ОН ЗАПОМИНАЕТ", "accent": False, "size": "small"}, {"text": "МАТЕРИАЛ", "accent": True, "size": "big"}]},
    {"start": 11.07, "end": 12.99, "lines": [{"text": "ОБЫЧНОЕ ПЕРЕЧИТЫВАНИЕ КОНСПЕКТА", "accent": False, "size": "small"}, {"text": "ЧАСТО", "accent": True, "size": "big"}]},
    {"start": 13.11, "end": 14.40, "lines": [{"text": "НЕ ДАЕТ", "accent": False, "size": "small"}, {"text": "СТОЙКОГО РЕЗУЛЬТАТА", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 16.80, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО ЭТИМ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТАМ", "accent": True, "size": "big"}]},
    {"start": 17.04, "end": 18.24, "lines": [{"text": "ЕСТЬ НА", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.66, "end": 20.94, "lines": [{"text": "МАТЕРИАЛ ЗАКРЕПЛЯЕТСЯ ЧЕРЕЗ АКТИВНОЕ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 23.04, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.13, "end": 2.46}, {"start": 15.18, "end": 15.51}, {"start": 21.21, "end": 21.54}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (brunette study-room host, 34.000s): olympiad participants
# practice a generic quiz mode with the easiest answer variants; the app
# has a toggleable trap-variant mode drilling exactly the lookalike
# answers that olympiad-level students confuse most
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ИГРАЕШЬ ПРОСТЫЕ ВАРИАНТЫ", "БЕЗ ЛОВУШЕК?"], "end": 2.85}
c_cards = [
    {"start": 3.00, "end": 3.99, "lines": [{"text": "ОБЫЧНУЮ ИГРУ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 6.00, "lines": [{"text": "С САМЫМИ ПРОСТЫМИ ВАРИАНТАМИ", "accent": False, "size": "small"}, {"text": "ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 6.57, "end": 7.68, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВКЛЮЧАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 8.88, "lines": [{"text": "ОТДЕЛЬНЫЙ", "accent": False, "size": "small"}, {"text": "РЕЖИМ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.29, "lines": [{"text": "ИМЕННО С ТЕМИ", "accent": False, "size": "small"}, {"text": "ВАРИАНТАМИ", "accent": True, "size": "big"}]},
    {"start": 10.59, "end": 12.54, "lines": [{"text": "КОТОРЫЕ ЧАЩЕ ВСЕГО ПУТАЮТ МЕЖДУ", "accent": False, "size": "small"}, {"text": "СОБОЙ", "accent": True, "size": "big"}]},
    {"start": 13.26, "end": 15.42, "lines": [{"text": "ЛОВУШКИ ПОДОБРАНЫ ПО ИТОГАМ ЧАСТЫХ", "accent": False, "size": "small"}, {"text": "ОШИБОК", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 17.40, "lines": [{"text": "ИМЕННО ОЛИМПИАДНОГО УРОВНЯ", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТИ", "accent": True, "size": "big"}]},
    {"start": 18.03, "end": 20.46, "lines": [{"text": "ОТРАБАТЫВАТЬ ТОЛЬКО ЛЕГКИЕ ОДНОЗНАЧНЫЕ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 20.82, "end": 22.89, "lines": [{"text": "ВМЕСТО НАСТОЯЩИХ ЛОВУШЕК НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 23.22, "end": 24.75, "lines": [{"text": "РЕЖИМ ЛОВУШЕК МОЖНО", "accent": False, "size": "small"}, {"text": "ВКЛЮЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 24.99, "end": 27.09, "lines": [{"text": "И ВЫКЛЮЧИТЬ ОДНИМ ПЕРЕКЛЮЧАТЕЛЕМ В", "accent": False, "size": "small"}, {"text": "НАСТРОЙКАХ", "accent": True, "size": "big"}]},
    {"start": 27.69, "end": 28.89, "lines": [{"text": "ОТДЕЛЬНЫЙ РЕЖИМ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЕТ", "accent": True, "size": "big"}]},
    {"start": 29.07, "end": 31.47, "lines": [{"text": "ИМЕННО ТЕ ВАРИАНТЫ КОТОРЫЕ ПУТАЮТ ЧАЩЕ", "accent": False, "size": "small"}, {"text": "ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 32.19, "end": 34.05, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.00, "end": 3.33}, {"start": 6.57, "end": 6.90}, {"start": 32.19, "end": 32.52}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (blonde evening-room host, 22.850s): studying from random
# internet variants of unknown origin; the app's bank is sourced straight
# from FIPI, the same tasks the actual exam commission uses
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ГОТОВИШЬСЯ ПО СЛУЧАЙНЫМ", "ВАРИАНТАМ ИЗ ИНТЕРНЕТА?"], "end": 1.65}
d_cards = [
    {"start": 1.98, "end": 3.93, "lines": [{"text": "ПО СЛУЧАЙНЫМ ВАРИАНТАМ КОТОРЫЕ НАШЛА В", "accent": False, "size": "small"}, {"text": "ИНТЕРНЕТЕ", "accent": True, "size": "big"}]},
    {"start": 4.44, "end": 7.50, "lines": [{"text": "СНАЧАЛА СТОИТ ПРОВЕРИТЬ ОТКУДА ВООБЩЕ ВЗЯТЫ ЭТИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.24, "lines": [{"text": "МНОГИЕ ТАКИЕ", "accent": False, "size": "small"}, {"text": "СБОРНИКИ", "accent": True, "size": "big"}]},
    {"start": 9.45, "end": 11.16, "lines": [{"text": "ДАВНО УСТАРЕЛИ ИЛИ НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАЮТ", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.84, "lines": [{"text": "ПО ФОРМАТУ С", "accent": False, "size": "small"}, {"text": "РЕАЛЬНЫМ ЭКЗАМЕНОМ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 14.76, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "СОБРАН", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.11, "lines": [{"text": "АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.62, "end": 19.29, "lines": [{"text": "ТЕ ЖЕ ЗАДАНИЯ ЧТО ИСПОЛЬЗУЕТ ПРИ СОСТАВЛЕНИИ", "accent": False, "size": "small"}, {"text": "КОМИССИЯ", "accent": True, "size": "big"}]},
    {"start": 19.50, "end": 20.34, "lines": [{"text": "", "accent": False, "size": "small"}, {"text": "НАСТОЯЩЕГО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 22.92, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.98, "end": 2.31}, {"start": 13.53, "end": 13.86}, {"start": 21.06, "end": 21.39}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (brunette study-room host, 33.623s): olympiad participants get
# lost in a general leaderboard of thousands of regular users; the app
# keeps a separate leaderboard for just the olympiad track, updating as
# often as the general one
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ТЕРЯЕШЬСЯ СРЕДИ СОТЕН", "УЧАСТНИКОВ?"], "end": 2.7}
e_cards = [
    {"start": 2.88, "end": 4.68, "lines": [{"text": "ВИДЯТ СЕБЯ В ОБЩЕМ РЕЙТИНГЕ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.01, "end": 6.84, "lines": [{"text": "РЯДОМ С СОТНЯМИ ОБЫЧНЫХ", "accent": False, "size": "small"}, {"text": "УЧАСТНИКОВ", "accent": True, "size": "big"}]},
    {"start": 7.68, "end": 8.76, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СОБИРАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "ОТДЕЛЬНЫЙ РЕЙТИНГ", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 10.32, "end": 12.09, "lines": [{"text": "СРЕДИ УЧАСТНИКОВ ОЛИМПИАДНОГО", "accent": False, "size": "small"}, {"text": "ТРЕКА", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 14.13, "lines": [{"text": "БЕЗ ОСТАЛЬНОЙ ПОЛЬЗОВАТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "МАССЫ", "accent": True, "size": "big"}]},
    {"start": 14.88, "end": 16.95, "lines": [{"text": "СРАВНЕНИЕ С РАВНЫМИ ПО УЧАСТНИКАМИ", "accent": False, "size": "small"}, {"text": "УРОВНЮ", "accent": True, "size": "big"}]},
    {"start": 17.28, "end": 19.41, "lines": [{"text": "ПОНЯТНЕЕ ОБЩЕГО СПИСКА ИЗ", "accent": False, "size": "small"}, {"text": "ТЫСЯЧ", "accent": True, "size": "big"}]},
    {"start": 20.16, "end": 23.10, "lines": [{"text": "ИСКАТЬ СЕБЯ СРЕДИ СОТЕН ОБЫЧНЫХ УЧАСТНИКОВ ОБЩЕГО", "accent": False, "size": "small"}, {"text": "СПИСКА", "accent": True, "size": "big"}]},
    {"start": 23.46, "end": 25.02, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНЫЙ РЕЙТИНГ", "accent": True, "size": "big"}]},
    {"start": 25.14, "end": 27.00, "lines": [{"text": "ОБНОВЛЯЕТСЯ ТАКЖЕ ЧАСТО КАК И", "accent": False, "size": "small"}, {"text": "ОБЩИЙ", "accent": True, "size": "big"}]},
    {"start": 27.57, "end": 28.95, "lines": [{"text": "СРАВНЕНИЕ С РАВНЫМИ ПО", "accent": False, "size": "small"}, {"text": "УРОВНЮ", "accent": True, "size": "big"}]},
    {"start": 29.25, "end": 31.11, "lines": [{"text": "ПОНЯТНЕЕ ОБЩЕГО СПИСКА ИЗ", "accent": False, "size": "small"}, {"text": "ТЫСЯЧ", "accent": True, "size": "big"}]},
    {"start": 31.86, "end": 33.81, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.88, "end": 3.21}, {"start": 7.68, "end": 8.01}, {"start": 31.86, "end": 32.19}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (mother, parent POV, 20.460s): a child checks the correct
# answer after a mistake and moves on, so the mistake repeats; the app
# gives a full text explanation of the actual error, not just the answer
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СМОТРИТ ОТВЕТ", "И ИДЕТ ДАЛЬШЕ?"], "end": 2.85}
f_cards = [
    {"start": 3.00, "end": 5.13, "lines": [{"text": "ПРОСТО СМОТРИТ ПРАВИЛЬНЫЙ ОТВЕТ И ИДЕТ", "accent": False, "size": "small"}, {"text": "ДАЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 5.70, "end": 7.32, "lines": [{"text": "ОШИБКА ПОЧТИ НАВЕРНЯКА", "accent": False, "size": "small"}, {"text": "ПОВТОРИТСЯ", "accent": True, "size": "big"}]},
    {"start": 7.89, "end": 9.57, "lines": [{"text": "САМО ПО СЕБЕ РЕШЕНИЕ НОВЫХ", "accent": False, "size": "small"}, {"text": "ВАРИАНТОВ", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 11.16, "lines": [{"text": "ЭТУ ПРИВЫЧКУ НЕ", "accent": False, "size": "small"}, {"text": "ИСПРАВЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.38, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 13.56, "end": 15.06, "lines": [{"text": "ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.39, "end": 16.89, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "САМУ ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.21, "lines": [{"text": "А НЕ ТОЛЬКО НАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 18.75, "end": 20.64, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 3.00, "end": 3.33}, {"start": 11.73, "end": 12.06}, {"start": 18.75, "end": 19.08}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (blonde evening-room host, 23.575s): solving tasks daily feels
# like real prep, but there's never time to actually review the mistakes;
# the app gives a full text explanation per task so the gap closes right
# away instead of getting pushed off indefinitely
# ---------------------------------------------------------------------------
g_intro = {"lines": ["РЕШАЕШЬ ЗАДАНИЯ", "НО НЕ РАЗБИРАЕШЬ ОШИБКИ?"], "end": 1.65}
g_cards = [
    {"start": 2.13, "end": 3.96, "lines": [{"text": "ДУМАТЬ ЧТО ГОТОВИШЬСЯ ТОЛЬКО ПОТОМУ", "accent": False, "size": "small"}, {"text": "ЧТО", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 5.64, "lines": [{"text": "КАЖДЫЙ ДЕНЬ ЧТО ТО", "accent": False, "size": "small"}, {"text": "РЕШАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.67, "lines": [{"text": "ЗАДАНИЯ ИДУТ ОДНО ЗА", "accent": False, "size": "small"}, {"text": "ДРУГИМ", "accent": True, "size": "big"}]},
    {"start": 9.12, "end": 9.96, "lines": [{"text": "А", "accent": False, "size": "small"}, {"text": "РАЗБИРАТЬ ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.94, "lines": [{"text": "ПО НАСТОЯЩЕМУ ПРОСТО НЕ", "accent": False, "size": "small"}, {"text": "УСПЕВАЕШЬ", "accent": True, "size": "big"}]},
    {"start": 12.93, "end": 14.73, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 16.53, "lines": [{"text": "ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 18.90, "lines": [{"text": "КОТОРЫЙ ПОМОГАЕТ ЗАКРЫТЬ", "accent": False, "size": "small"}, {"text": "ПРОБЕЛ СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 19.44, "end": 20.67, "lines": [{"text": "А НЕ ОТКЛАДЫВАТЬ ЕГО НА", "accent": False, "size": "small"}, {"text": "ПОТОМ", "accent": True, "size": "big"}]},
    {"start": 21.63, "end": 23.61, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.13, "end": 2.46}, {"start": 12.93, "end": 13.26}, {"start": 21.63, "end": 21.96}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (blonde evening-room host, 23.042s): re-reading notes feels
# like studying but barely locks anything in for the essay subjects; the
# app has memorization games for these subjects that force active recall
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ЗАПОМИНАЕШЬ АКТИВНО", "ИЛИ ПРОСТО ЧИТАЕШЬ?"], "end": 2.7}
h_cards = [
    {"start": 2.91, "end": 4.59, "lines": [{"text": "ТЕБЕ ТЫ ЗАПОМИНАЕШЬ", "accent": False, "size": "small"}, {"text": "МАТЕРИАЛ", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 6.63, "lines": [{"text": "ИЛИ ПРОСТО ПЕРЕЧИТЫВАЕШЬ", "accent": False, "size": "small"}, {"text": "АКТИВНО", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 8.85, "lines": [{"text": "ЕГО ЕЩЕ РАЗ ВТОРОЙ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 8.97, "end": 11.61, "lines": [{"text": "КАЖЕТСЯ ПОДГОТОВКОЙ НО ПОЧТИ", "accent": False, "size": "small"}, {"text": "НИЧЕГО", "accent": True, "size": "big"}]},
    {"start": 11.88, "end": 14.01, "lines": [{"text": "НЕ ЗАКРЕПЛЯЕТ В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.22, "end": 16.50, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.36, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.66, "end": 20.58, "lines": [{"text": "ГДЕ ПРИХОДИТСЯ ВСПОМИНАТЬ ОТВЕТ", "accent": False, "size": "small"}, {"text": "САМОЙ", "accent": True, "size": "big"}]},
    {"start": 21.27, "end": 23.19, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 2.91, "end": 3.24}, {"start": 13.26, "end": 13.59}, {"start": 21.27, "end": 21.60}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (mother, parent POV, 22.000s): a child studies for hours at
# home with no progress; the app's bank is sourced straight from FIPI
# instead of stale collections that no longer match the real exam
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ЧАСАМИ ЗАНИМАЕТСЯ", "БЕЗ РЕЗУЛЬТАТА?"], "end": 2.1}
i_cards = [
    {"start": 2.40, "end": 4.59, "lines": [{"text": "К ЕГЭ ДОМА А РЕЗУЛЬТАТ ПОЧТИ НЕ", "accent": False, "size": "small"}, {"text": "РАСТЕТ", "accent": True, "size": "big"}]},
    {"start": 4.92, "end": 7.65, "lines": [{"text": "СТОИТ ПРОВЕРИТЬ С КАКИМИ ЗАДАНИЯМИ ОН ВООБЩЕ", "accent": False, "size": "small"}, {"text": "ЗАНИМАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.96, "lines": [{"text": "МНОГИЕ СБОРНИКИ В СВОБОДНОМ", "accent": False, "size": "small"}, {"text": "ДОСТУПЕ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 12.30, "lines": [{"text": "ДАВНО УСТАРЕЛИ И НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАЮТ", "accent": True, "size": "big"}]},
    {"start": 12.45, "end": 13.38, "lines": [{"text": "", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ ЭКЗАМЕНОВ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.78, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ СОБРАН АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.62, "end": 18.09, "lines": [{"text": "ТЕ ЖЕ ЧТО ИСПОЛЬЗУЮТСЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 18.18, "end": 19.83, "lines": [{"text": "ПРИ СОСТАВЛЕНИИ НАСТОЯЩЕГО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 20.40, "end": 22.11, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.40, "end": 2.73}, {"start": 13.80, "end": 14.13}, {"start": 20.40, "end": 20.73}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
