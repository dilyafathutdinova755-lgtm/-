#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTEENTH 'coffee123'
batch (6 episodes uploaded under the same tag after fifteen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes59/.

New sub-theme this batch: "выпускники" preparing for/competing in
olympiads (distinct from the recurring вожатый/рыбалка/родители
threads). Two genuinely new hosts, three episodes each: a brunette in
a bright study room (desk, textbooks, "ЕГЭ 2026" sticky note, photo
wall, The Smiths poster) and a blonde in a dimmer evening-lit room
(lamp, dried flowers, cream sweater). Content: no ads interrupting
rounds or tasks, an offline task bank that only pulls hard
olympiad-adjacent tasks instead of the whole course, olympiad stats
shown on their own line instead of blended into the general average,
each wrong answer tagged as carelessness vs. a real knowledge gap,
tracking a streak of high-accuracy days instead of just today's
percentage, and term cards showing the exact time to next review on
their back instead of shuffling through the whole deck.
"""
import json

REAL_DURATION = {
    "a": 36.183, "b": 38.402, "c": 38.700,
    "d": 33.346, "e": 35.040, "f": 28.280,
}
SOURCE_FILE = {
    "a": "21.09.hthrghtrhtrhr", "b": "21.09hrshhhtrhtrhr", "c": "21.rhtrdghhtrhrhrhtrhrdh",
    "d": "21htrhdhrthrhrh", "e": "htrhrdhtrhrhrhdhtdrh", "f": "htrhrhdrhdthth",
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
    if letter == "c":
        for w in words:
            if abs(w["start"] - 4.35) < 0.02 and w["text"] == "эгэ":
                w["text"] = "егэ"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_16/{src}_words.json"))
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
# Episode A (brunette study-room host, 36.183s): olympiad participants used
# to ads interrupting rounds/tasks in free prep apps; the app shows zero
# banners, ever, between tasks or short game rounds
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЖДЕШЬ РЕКЛАМУ", "МЕЖДУ РАУНДАМИ?"], "end": 2.25}
a_cards = [
    {"start": 2.28, "end": 3.09, "lines": [{"text": "ВЫПУСКНИКИ УЧАСТВУЮЩИЕ В ОЛИМПИАДАХ", "accent": False, "size": "small"}, {"text": "ПРИВЫКЛИ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 5.79, "lines": [{"text": "ЧТО БЕСПЛАТНЫЕ ПРИЛОЖЕНИЯ ДЛЯ ПОДГОТОВКИ К", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 6.03, "end": 7.68, "lines": [{"text": "ПОКАЗЫВАЮТ РЕКЛАМУ МЕЖДУ", "accent": False, "size": "small"}, {"text": "РАУНДАМИ", "accent": True, "size": "big"}]},
    {"start": 8.61, "end": 10.14, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР НЕ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.76, "lines": [{"text": "НИ ОДНОГО РЕКЛАМНОГО", "accent": False, "size": "small"}, {"text": "БАННЕРА", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.26, "lines": [{"text": "НИ МЕЖДУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 15.36, "lines": [{"text": "НИ МЕЖДУ КОРОТКИМИ РАУНДАМИ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.17, "end": 17.79, "lines": [{"text": "ЭКРАН ОСТАЕТСЯ ЧИСТЫМ ОТ", "accent": False, "size": "small"}, {"text": "РЕКЛАМЫ", "accent": True, "size": "big"}]},
    {"start": 17.94, "end": 20.22, "lines": [{"text": "НА ПРОТЯЖЕНИИ ВСЕГО ИСПОЛЬЗОВАНИЯ", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 21.24, "end": 22.92, "lines": [{"text": "ЖДАТЬ ОКОНЧАНИЯ РЕКЛАМНОГО", "accent": False, "size": "small"}, {"text": "РОЛИКА", "accent": True, "size": "big"}]},
    {"start": 23.13, "end": 24.66, "lines": [{"text": "ПЕРЕД НОВЫМ РАУНДОМ НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 25.44, "end": 27.99, "lines": [{"text": "СВОБОДНОЕ МЕСТО НА ЭКРАНЕ ЗАНИМАЕТ ТОЛЬКО ЗАДАНИЯ И", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТЫ", "accent": True, "size": "big"}]},
    {"start": 29.55, "end": 31.92, "lines": [{"text": "РЕКЛАМА НЕ ПРЕРЫВАЕТ НИ РЕШЕНИЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 32.25, "end": 33.48, "lines": [{"text": "НИ КОРОТКИЕ РАУНДЫ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 34.38, "end": 36.24, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.28, "end": 2.61}, {"start": 8.61, "end": 8.94}, {"start": 34.38, "end": 34.71}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (brunette study-room host, 38.402s): downloading the whole task
# bank before a signal-free training camp; the app's offline set only pulls
# harder olympiad-adjacent tasks, refreshing itself on every reconnect
# instead of a manual full re-download
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СКАЧИВАЕШЬ ВЕСЬ БАНК", "ПЕРЕД СБОРАМИ?"], "end": 2.25}
b_cards = [
    {"start": 2.70, "end": 4.62, "lines": [{"text": "СКАЧИВАЮТ ОФЛАЙН БАНК ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.92, "end": 7.56, "lines": [{"text": "ПЕРЕД ВЫЕЗДОМ НА СБОРЫ В ЛАГЕРЬ БЕЗ СТАБИЛЬНОЙ", "accent": False, "size": "small"}, {"text": "СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 8.58, "end": 9.81, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ОТБИРАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 11.49, "lines": [{"text": "В ОФФЛАЙН БАНК ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 12.63, "lines": [{"text": "", "accent": False, "size": "small"}, {"text": "ПОВЫШЕННОЙ СЛОЖНОСТИ", "accent": True, "size": "big"}]},
    {"start": 13.17, "end": 14.46, "lines": [{"text": "РЯДОМ С ТЕМАМИ", "accent": False, "size": "small"}, {"text": "ОЛИМПИАД", "accent": True, "size": "big"}]},
    {"start": 14.76, "end": 15.75, "lines": [{"text": "А НЕ ВЕСЬ КУРС", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 16.62, "end": 18.93, "lines": [{"text": "ОБЫЧНЫЕ ЛЕГКИЕ ЗАДАНИЯ ОСТАЮТСЯ", "accent": False, "size": "small"}, {"text": "ДОСТУПНЫ", "accent": True, "size": "big"}]},
    {"start": 19.14, "end": 20.94, "lines": [{"text": "ТОЛЬКО ПРИ АКТИВНОЙ СВЯЗИ В", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 21.72, "end": 23.91, "lines": [{"text": "СОБИРАТЬ НУЖНЫЕ СЛОЖНЫЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 24.27, "end": 25.68, "lines": [{"text": "ИЗ ОБЩЕГО БАНКА ПЕРЕД", "accent": False, "size": "small"}, {"text": "СБОРАМИ", "accent": True, "size": "big"}]},
    {"start": 25.95, "end": 28.59, "lines": [{"text": "НЕ ПРИХОДИТСЯ ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "НАБОР", "accent": True, "size": "big"}]},
    {"start": 28.80, "end": 31.02, "lines": [{"text": "САМ ПРИ КАЖДОМ НОВОМ ПОДКЛЮЧЕНИИ К", "accent": False, "size": "small"}, {"text": "ИНТЕРНЕТУ", "accent": True, "size": "big"}]},
    {"start": 31.92, "end": 35.61, "lines": [{"text": "СЛОЖНЫЕ ОЛИМПИАДНЫЕ ЗАДАНИЯ ОСТАЮТСЯ ПОД РУКОЙ ДАЖЕ ВДАЛИ ОТ", "accent": False, "size": "small"}, {"text": "СЕТИ", "accent": True, "size": "big"}]},
    {"start": 36.54, "end": 38.52, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.70, "end": 3.03}, {"start": 8.58, "end": 8.91}, {"start": 36.54, "end": 36.87}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (brunette study-room host, 38.700s): olympiad prep blends into
# one smeared overall accuracy number; the app shows olympiad-task progress
# on its own line, separate from the regular course average
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ВИДИШЬ ОДИН СМЕШАННЫЙ", "ПОКАЗАТЕЛЬ?"], "end": 2.25}
c_cards = [
    {"start": 2.94, "end": 4.47, "lines": [{"text": "ВИДЯТ В ОБЩЕЙ СТАТИСТИКЕ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.71, "end": 6.99, "lines": [{"text": "ТОЛЬКО ОДИН СМЕШАННЫЙ УСПЕВАЕМОСТИ", "accent": False, "size": "small"}, {"text": "ПОКАЗАТЕЛЬ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.15, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВЫВОДИТ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.89, "lines": [{"text": "СТАТИСТИКУ ПО ОЛИМПИАДНЫМ", "accent": False, "size": "small"}, {"text": "ЗАДАЧАМ", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 13.17, "lines": [{"text": "ОТДЕЛЬНОЙ СТРОКОЙ ОТ ОБЫЧНЫХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 13.29, "end": 16.32, "lines": [{"text": "ОСНОВНОГО КУРСА ПРОГРЕСС ПО ТРУДНЫМ НЕСТАНДАРТНЫМ", "accent": False, "size": "small"}, {"text": "ТРУДНЫМ", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 17.49, "lines": [{"text": "ЗАДАЧАМ", "accent": False, "size": "small"}, {"text": "ВИДЕН СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.83, "lines": [{"text": "БЕЗ СМЕШИВАНИЯ С ПРОСТЫМИ", "accent": False, "size": "small"}, {"text": "ТЕМАМИ", "accent": True, "size": "big"}]},
    {"start": 20.79, "end": 23.73, "lines": [{"text": "ИСКАТЬ ОЛИМПИАДНЫЕ РЕЗУЛЬТАТЫ ВНУТРИ ОБЩЕГО СПИСКА", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 24.03, "end": 26.43, "lines": [{"text": "НЕ ПРИХОДИТСЯ ОТДЕЛЬНАЯ", "accent": False, "size": "small"}, {"text": "СТРОКА", "accent": True, "size": "big"}]},
    {"start": 26.64, "end": 28.29, "lines": [{"text": "ОБНОВЛЯЕТСЯ САМА ПОСЛЕ", "accent": False, "size": "small"}, {"text": "КАЖДОГО", "accent": True, "size": "big"}]},
    {"start": 28.56, "end": 30.30, "lines": [{"text": "НОВОГО РЕШЕННОГО ЗАДАНИЯ ТАКОГО", "accent": False, "size": "small"}, {"text": "ТИПА", "accent": True, "size": "big"}]},
    {"start": 31.29, "end": 33.45, "lines": [{"text": "ОЛИМПИАДНЫЙ ПРОГРЕСС ВИДЕН ОТДЕЛЬНОЙ", "accent": False, "size": "small"}, {"text": "СТРОКОЙ", "accent": True, "size": "big"}]},
    {"start": 34.05, "end": 35.97, "lines": [{"text": "НЕ СМЕШИВАЯСЬ С ОСТАЛЬНЫМИ ТЕМАМИ", "accent": False, "size": "small"}, {"text": "КУРСА", "accent": True, "size": "big"}]},
    {"start": 36.90, "end": 38.82, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.94, "end": 3.27}, {"start": 8.13, "end": 8.46}, {"start": 36.90, "end": 37.23}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (blonde evening-room host, 33.346s): can't tell if a wrong
# answer was carelessness or a real gap without rethinking it at night; the
# app tags each mistake as one of the two the moment it happens
# ---------------------------------------------------------------------------
d_intro = {"lines": ["НЕ ПОНИМАЕШЬ ПОЧЕМУ", "ОШИБСЯ В ЗАДАНИИ?"], "end": 1.65}
d_cards = [
    {"start": 1.77, "end": 2.88, "lines": [{"text": "РАЗБИРАЮТ ОШИБКУ В ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.33, "end": 5.25, "lines": [{"text": "И НЕ ПОНИМАЕТ СЛУЧАЙНО ЭТО", "accent": False, "size": "small"}, {"text": "БЫЛА", "accent": True, "size": "big"}]},
    {"start": 5.37, "end": 7.44, "lines": [{"text": "НЕВНИМАТЕЛЬНОСТЬ ИЛИ ПРОБЕЛ В", "accent": False, "size": "small"}, {"text": "ЗНАНИЯХ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.27, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОМЕЧАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.48, "end": 11.40, "lines": [{"text": "КАЖДУЮ ОШИБКУ ОДНОЙ ИЗ ДВУХ", "accent": False, "size": "small"}, {"text": "ПРИЧИН", "accent": True, "size": "big"}]},
    {"start": 11.94, "end": 14.19, "lines": [{"text": "НЕВНИМАТЕЛЬНОСТЬ ИЛИ ПРОБЕЛ В ЗНАНИИ", "accent": False, "size": "small"}, {"text": "ТЕМЫ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.59, "lines": [{"text": "МЕТКА ВОЗНИКАЕТ СРАЗУ ПОСЛЕ", "accent": False, "size": "small"}, {"text": "ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 18.78, "lines": [{"text": "БЕЗ ОТДЕЛЬНОГО ВОПРОСА САМОГО", "accent": False, "size": "small"}, {"text": "УЧЕНИКА", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 22.05, "lines": [{"text": "РАЗБИРАТЬСЯ В ПРИЧИНЕ ОШИБКИ ЗАНОВО ПО ПАМЯТИ", "accent": False, "size": "small"}, {"text": "ВЕЧЕРОМ", "accent": True, "size": "big"}]},
    {"start": 22.29, "end": 24.18, "lines": [{"text": "НЕ ПРИХОДИТСЯ СПИСОК", "accent": False, "size": "small"}, {"text": "ОШИБОК", "accent": True, "size": "big"}]},
    {"start": 24.27, "end": 27.00, "lines": [{"text": "ПО ПРОБЕЛАМ В ЗНАНИЯХ СОБИРАЕТСЯ ОТДЕЛЬНО ДЛЯ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 27.69, "end": 29.01, "lines": [{"text": "ПРИЧИНА ОШИБКИ ВИДНА", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 29.58, "end": 30.96, "lines": [{"text": "БЕЗ ГАДАНИЯ ПО ПАМЯТИ", "accent": False, "size": "small"}, {"text": "ВЕЧЕРОМ", "accent": True, "size": "big"}]},
    {"start": 31.74, "end": 33.54, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.77, "end": 2.10}, {"start": 8.10, "end": 8.43}, {"start": 31.74, "end": 32.07}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (blonde evening-room host, 35.040s): a single bad day tanks
# today's accuracy percentage and stability looks shaky; the app tracks a
# separate streak of consistently high-accuracy days instead
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СМОТРИШЬ НА ПРОЦЕНТ", "ЗА СЕГОДНЯ?"], "end": 1.65}
e_cards = [
    {"start": 1.80, "end": 3.48, "lines": [{"text": "СМОТРЯТ НА ИТОГОВЫЙ ПРОЦЕНТ ТОЧНОСТИ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.05, "end": 6.90, "lines": [{"text": "И НЕ ПОНИМАЮТ СТАБИЛЕН ЛИ ИХ РЕЗУЛЬТАТ НА САМОМ", "accent": False, "size": "small"}, {"text": "ДЕЛЕ", "accent": True, "size": "big"}]},
    {"start": 8.01, "end": 9.24, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СЧИТАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 10.83, "lines": [{"text": "ОТДЕЛЬНУЮ", "accent": False, "size": "small"}, {"text": "СЕРИЮ ДНЕЙ ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 13.05, "lines": [{"text": "С ОДИНАКОВО ВЫСОКОЙ ТОЧНОСТЬЮ", "accent": False, "size": "small"}, {"text": "ОТВЕТОВ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 14.97, "lines": [{"text": "А НЕ ТОЛЬКО СЕГОДНЯШНИЙ", "accent": False, "size": "small"}, {"text": "ПРОЦЕНТ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 17.37, "lines": [{"text": "ОДИН СЛАБЫЙ ДЕНЬ СБИВАЕТ", "accent": False, "size": "small"}, {"text": "СЕРИЮ", "accent": True, "size": "big"}]},
    {"start": 17.76, "end": 19.50, "lines": [{"text": "ЗАТО НЕ ПОРТИТ ОБЩИЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗАТЕЛЬ", "accent": True, "size": "big"}]},
    {"start": 20.31, "end": 22.89, "lines": [{"text": "СУДИТЬ О СТАБИЛЬНОСТИ ТОЛЬКО ПО СЕГОДНЯШНЕМУ", "accent": False, "size": "small"}, {"text": "ПРОЦЕНТУ", "accent": True, "size": "big"}]},
    {"start": 23.16, "end": 24.03, "lines": [{"text": "БОЛЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 24.75, "end": 27.99, "lines": [{"text": "СЕРИЯ ДНЕЙ С ВЫСОКОЙ ТОЧНОСТЬЮ ВИДНА ПРЯМО НА ГЛАВНОМ", "accent": False, "size": "small"}, {"text": "ЭКРАНЕ", "accent": True, "size": "big"}]},
    {"start": 28.80, "end": 30.39, "lines": [{"text": "СТАБИЛЬНОСТЬ ВИДНА ПО СЕРИИ", "accent": False, "size": "small"}, {"text": "ДНЕЙ", "accent": True, "size": "big"}]},
    {"start": 30.75, "end": 32.43, "lines": [{"text": "А НЕ ПО СЛУЧАЙНОМУ ПРОЦЕНТУ ЗА", "accent": False, "size": "small"}, {"text": "СЕГОДНЯ", "accent": True, "size": "big"}]},
    {"start": 33.21, "end": 35.16, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.80, "end": 2.13}, {"start": 8.01, "end": 8.34}, {"start": 33.21, "end": 33.54}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (blonde evening-room host, 28.280s): term cards pile up in one
# big unordered heap; the app shows the exact time to next review right on
# the back of each card, so the due card floats to the top on its own
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ХРАНИШЬ КАРТОЧКИ", "БЕЗ ВСЯКОГО ПОРЯДКА?"], "end": 1.5}
f_cards = [
    {"start": 1.65, "end": 2.85, "lines": [{"text": "КАРТОЧКИ ТЕРМИНОВ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 3.99, "lines": [{"text": "В ОДНОЙ БОЛЬШОЙ", "accent": False, "size": "small"}, {"text": "КУЧЕ", "accent": True, "size": "big"}]},
    {"start": 4.38, "end": 6.12, "lines": [{"text": "И ПОВТОРЯЮТ ИХ БЕЗ ВСЯКОГО", "accent": False, "size": "small"}, {"text": "ПОРЯДКА", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.16, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 10.26, "lines": [{"text": "ТОЧНОЕ ВРЕМЯ ДО СЛЕДУЮЩЕГО", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 10.77, "end": 12.69, "lines": [{"text": "ПРЯМО НА ОБРАТНОЙ СТОРОНЕ КАЖДОЙ", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 13.41, "end": 14.94, "lines": [{"text": "ОБРАТНЫЙ ОТЧЕТ ДО НУЖНОЙ", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 17.67, "lines": [{"text": "ВИДЕН ЗАРАНЕЕ ЕЩЕ ДО ОТКРЫТИЯ ВСЕЙ", "accent": False, "size": "small"}, {"text": "КОЛОДЫ", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 20.82, "lines": [{"text": "ПЕРЕБИРАТЬ ВСЮ КОЛОДУ КАРТОЧЕК ПОДРЯД В ПОИСКАХ", "accent": False, "size": "small"}, {"text": "НУЖНОЙ", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 23.07, "lines": [{"text": "НЕ ПРИХОДИТСЯ НУЖНАЯ", "accent": False, "size": "small"}, {"text": "КАРТОЧКА", "accent": True, "size": "big"}]},
    {"start": 23.25, "end": 25.77, "lines": [{"text": "САМА ПОДНИМАЕТСЯ ВЫШЕ ОСТАЛЬНЫХ К СРОКУ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 26.49, "end": 28.35, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.65, "end": 1.98}, {"start": 6.93, "end": 7.26}, {"start": 26.49, "end": 26.82}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
