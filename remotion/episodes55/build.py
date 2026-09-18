#!/usr/bin/env python3
"""One-off authoring + validation script for the TWELFTH 'coffee123' batch
(6 episodes uploaded under the same tag after eleven prior batches were
delivered - a smaller drop than the usual nine). Not a generic tool:
hand-picked timings/text per episode. Run from remotion/episodes55/.

Two returning hosts this time (the parent woman, the warm-sweater girl) -
no boy hosts in this drop. Content: a steady-voice walkthrough with no
flashy editing cuts instead of blogger-style effects before bed, a
"verified against the current demo version" badge on tasks that
auto-updates instead of manual change-history checking, refusing to let
a corrected-on-paper mistake pass without an explanation in your own
words, an instant rating-position recalculation instead of a once-daily
one, closing the day's task the evening before when the morning will be
packed, and remembering the exact task where a mock exam was interrupted
instead of scrolling back through the whole variant.
"""
import json

REAL_DURATION = {
    "a": 27.266, "b": 33.047, "c": 27.180,
    "d": 28.140, "e": 25.068, "f": 28.400,
}
SOURCE_FILE = {
    "a": "18_09___1_2160p11111", "b": "18_09___1_2160p111111", "c": "18_09___2_2160p2222",
    "d": "18_09___2_2160p22222", "e": "18_09___3_2160p3333", "f": "18_09___3_2160p333333",
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
    """Repair known sherpa-onnx ASR mis-transcriptions before captioning.
    Same pattern used for the recurring split/merge fixes in every prior
    batch."""
    if letter == "b":
        fixed = []
        for w in words:
            if abs(w["start"] - 2.85) < 0.02 and w["text"] == "сферено":
                fixed.append({"text": "сверено", "start": w["start"], "end": w["end"]})
            elif abs(w["start"] - 3.87) < 0.02 and w["text"] == "егэс":
                fixed.append({"text": "егэ", "start": 3.87, "end": 4.02})
                fixed.append({"text": "с", "start": 4.02, "end": 4.17})
            elif abs(w["start"] - 17.34) < 0.02 and w["text"] == "демоверсиип":
                fixed.append({"text": "демо", "start": 17.34, "end": 17.76})
                fixed.append({"text": "версии", "start": 17.76, "end": 18.18})
            else:
                fixed.append(w)
        words = fixed
    elif letter == "c":
        for w in words:
            if abs(w["start"] - 12.93) < 0.02 and w["text"] == "формальнае":
                w["text"] = "формальная"
    elif letter == "e":
        for w in words:
            if abs(w["start"] - 4.80) < 0.02 and w["text"] == "ягэ":
                w["text"] = "егэ"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_12/{src}_words.json"))
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
# Episode A (parent host, 27.266s): kid gets tired of the flashy editing in
# blogger video walkthroughs; the app voices the walkthrough in a steady
# voice with no editing cuts or visual flash, easier on the eyes before bed
# ---------------------------------------------------------------------------
a_intro = {"lines": ["УСТАЕТ ОТ ЭФФЕКТОВ", "В РАЗБОРЕ?"], "end": 2.3}
a_cards = [
    {"start": 2.43, "end": 3.30, "lines": [{"text": "РЕБЕНОК", "accent": False, "size": "small"}, {"text": "УСТАЕТ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 4.53, "lines": [{"text": "ОТ МЕЛЬКАЮЩИХ", "accent": False, "size": "small"}, {"text": "ЭФФЕКТОВ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.93, "lines": [{"text": "В РАЗБОРЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ У БЛОГЕРОВ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 9.09, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ОЗВУЧИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.27, "end": 10.29, "lines": [{"text": "РАЗБОР РОВНЫМ", "accent": False, "size": "small"}, {"text": "ГОЛОСОМ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.49, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "МОНТАЖНЫХ ВСТАВОК", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 12.78, "lines": [{"text": "РЕЗКОЙ СМЕНЫ", "accent": False, "size": "small"}, {"text": "КАРТИНКИ", "accent": True, "size": "big"}]},
    {"start": 13.38, "end": 14.94, "lines": [{"text": "ВНИМАНИЕ УХОДИТ", "accent": False, "size": "small"}, {"text": "НА РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 16.23, "lines": [{"text": "А НЕ НА", "accent": False, "size": "small"}, {"text": "ВИЗУАЛЬНЫЙ ЭФФЕКТЫ", "accent": True, "size": "big"}]},
    {"start": 16.32, "end": 17.70, "lines": [{"text": "ВОКРУГ НЕГО", "accent": False, "size": "small"}, {"text": "СМОТРЕТЬ", "accent": True, "size": "big"}]},
    {"start": 17.85, "end": 19.11, "lines": [{"text": "РАЗБОР ПЕРЕД СНОМ", "accent": False, "size": "small"}, {"text": "БЕЗ ЛИШНЕГО", "accent": True, "size": "big"}]},
    {"start": 19.23, "end": 20.13, "lines": [{"text": "НАПРЯЖЕНИЯ", "accent": False, "size": "small"}, {"text": "ДЛЯ ГЛАЗ", "accent": True, "size": "big"}]},
    {"start": 20.46, "end": 21.27, "lines": [{"text": "СТАНОВИТСЯ", "accent": False, "size": "small"}, {"text": "ПРОЩЕ", "accent": True, "size": "big"}]},
    {"start": 21.90, "end": 23.46, "lines": [{"text": "РОВНЫЙ ГОЛОС", "accent": False, "size": "small"}, {"text": "БЕЗ ВСТАВОК", "accent": True, "size": "big"}]},
    {"start": 23.61, "end": 24.93, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "УТОМЛЯЕТ ГЛАЗА", "accent": True, "size": "big"}]},
    {"start": 25.53, "end": 27.09, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.06, "end": 3.30}, {"start": 8.67, "end": 9.09}, {"start": 20.46, "end": 20.85}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (girl-bookshelf, 33.047s): can't tell by eye whether a task is
# synced to the current demo version or outdated; the app shows a short
# "verified" badge next to the task that auto-updates on every bank change
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЗАДАНИЕ АКТУАЛЬНОЕ", "ИЛИ УСТАРЕЛО?"], "end": 2.3}
b_cards = [
    {"start": 2.79, "end": 3.66, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "СВЕРЕНО ЛИ", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 5.31, "lines": [{"text": "ЗАДАНИЕ ЕГЭ С", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНОЙ", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 7.38, "lines": [{"text": "ИЛИ ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "УСТАРЕВШУЮ", "accent": True, "size": "big"}]},
    {"start": 8.37, "end": 9.63, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 11.31, "lines": [{"text": "КОРОТКУЮ ПОМЕТКУ", "accent": False, "size": "small"}, {"text": "СВЕРЕНО", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.17, "lines": [{"text": "РЯДОМ С ЗАДАНИЕМ", "accent": False, "size": "small"}, {"text": "СРАЗУ ПОСЛЕ", "accent": True, "size": "big"}]},
    {"start": 13.29, "end": 15.03, "lines": [{"text": "ПРОВЕРКИ ВЕРСИИ", "accent": False, "size": "small"}, {"text": "ПОМЕТКА", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 17.13, "lines": [{"text": "ОБНОВЛЯЕТСЯ САМА", "accent": False, "size": "small"}, {"text": "ПРИ КАЖДОМ", "accent": True, "size": "big"}]},
    {"start": 17.34, "end": 18.18, "lines": [{"text": "ИЗМЕНЕНИИ", "accent": False, "size": "small"}, {"text": "ДЕМО ВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 20.58, "lines": [{"text": "ГАДАТЬ АКТУАЛЬНО ЛИ", "accent": False, "size": "small"}, {"text": "ВЕРСИЯ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 21.66, "lines": [{"text": "БОЛЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 22.68, "end": 23.85, "lines": [{"text": "ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ОТКРЫВАТЬ ИСТОРИЮ", "accent": True, "size": "big"}]},
    {"start": 24.00, "end": 25.50, "lines": [{"text": "ИЗМЕНЕНИЙ РАДИ", "accent": False, "size": "small"}, {"text": "ОДНОЙ ПОМЕТКИ", "accent": True, "size": "big"}]},
    {"start": 25.74, "end": 27.15, "lines": [{"text": "НЕ НУЖНО", "accent": False, "size": "small"}, {"text": "ПОМЕТКА", "accent": True, "size": "big"}]},
    {"start": 27.42, "end": 28.32, "lines": [{"text": "СВЕРЕНА У", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 28.50, "end": 30.51, "lines": [{"text": "ЗАМЕНЯЕТ ГАДАНИЕ ОБ АКТУАЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "ВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 31.35, "end": 32.94, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.01, "end": 2.46}, {"start": 15.21, "end": 15.66}, {"start": 28.50, "end": 28.77}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (parent host, 27.180s): the kid fixes a mistake fast without
# explaining the reason; the app won't move forward until the mistake is
# explained in the kid's own words - "fixed and forgot" doesn't pass
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ИСПРАВИЛ БЫСТРО", "БЕЗ ОБЪЯСНЕНИЯ?"], "end": 2.3}
c_cards = [
    {"start": 2.34, "end": 3.69, "lines": [{"text": "КАК", "accent": False, "size": "small"}, {"text": "БЫСТРО ИСПРАВЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 4.92, "lines": [{"text": "ОШИБКУ В", "accent": False, "size": "small"}, {"text": "ЗАДАНИИ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.28, "end": 6.09, "lines": [{"text": "ТОЛКОМ НЕ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИВ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.20, "lines": [{"text": "В ЧЕМ БЫЛА", "accent": False, "size": "small"}, {"text": "ПРИЧИНА", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 8.94, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "НЕ ПУСКАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.09, "end": 9.96, "lines": [{"text": "ДАЛЬШЕ ПОКА", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.40, "lines": [{"text": "НЕ ОБЪЯСНЕНА", "accent": False, "size": "small"}, {"text": "СВОИМИ СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 12.45, "lines": [{"text": "ПРЯМО В", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 12.93, "end": 14.37, "lines": [{"text": "ФОРМАЛЬНАЯ", "accent": False, "size": "small"}, {"text": "ИСПРАВИЛ И ЗАБЫЛ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.99, "lines": [{"text": "ЗДЕСЬ ПРОСТО НЕ", "accent": False, "size": "small"}, {"text": "ПРОХОДЯТ ПРОВЕРКУ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.82, "lines": [{"text": "ПЕРЕХОД К", "accent": False, "size": "small"}, {"text": "СЛЕДУЮЩЕМУ ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 17.97, "end": 18.87, "lines": [{"text": "ТРЕБУЕТ", "accent": False, "size": "small"}, {"text": "НАСТОЯЩЕГО", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 20.64, "lines": [{"text": "ОБЪЯСНЕНИЯ", "accent": False, "size": "small"}, {"text": "А НЕ ГАЛОЧКИ", "accent": True, "size": "big"}]},
    {"start": 21.24, "end": 22.65, "lines": [{"text": "ФОРМАЛЬНАЯ", "accent": False, "size": "small"}, {"text": "ИСПРАВИЛ И ЗАБЫЛ", "accent": True, "size": "big"}]},
    {"start": 22.83, "end": 25.02, "lines": [{"text": "БОЛЬШЕ НЕ ПРОХОДИТ", "accent": False, "size": "small"}, {"text": "БЕЗ НАСТОЯЩЕГО", "accent": True, "size": "big"}]},
    {"start": 25.56, "end": 26.82, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.30, "end": 3.69}, {"start": 8.52, "end": 8.94}, {"start": 21.24, "end": 21.78}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (girl-bookshelf, 28.140s): expects a rating position to update
# only the next day; the app recalculates it immediately after a task is
# closed, no waiting for a scheduled recalculation
# ---------------------------------------------------------------------------
d_intro = {"lines": ["МЕСТО В РЕЙТИНГЕ", "ОБНОВИТСЯ ЗАВТРА?"], "end": 2.3}
d_cards = [
    {"start": 2.58, "end": 3.45, "lines": [{"text": "ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "ОБНОВИТСЯ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 5.58, "lines": [{"text": "НЕ СРАЗУ А ТОЛЬКО", "accent": False, "size": "small"}, {"text": "НА СЛЕДУЮЩИЙ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 8.07, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР ПЕРЕСЧИТЫВАЕТ", "accent": False, "size": "small"}, {"text": "МЕСТО", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.09, "lines": [{"text": "В РЕЙТИНГЕ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 9.27, "end": 10.38, "lines": [{"text": "ПОСЛЕ ТОГО КАК", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 10.56, "end": 12.45, "lines": [{"text": "ЗАКРЫТО", "accent": False, "size": "small"}, {"text": "БЕЗ ЗАДЕРЖКИ", "accent": True, "size": "big"}]},
    {"start": 13.14, "end": 14.73, "lines": [{"text": "НОВАЯ ПОЗИЦИЯ", "accent": False, "size": "small"}, {"text": "ВИДНА ТУТ ЖЕ", "accent": True, "size": "big"}]},
    {"start": 15.06, "end": 15.87, "lines": [{"text": "НА ЭТОМ ЖЕ", "accent": False, "size": "small"}, {"text": "ЭКРАНЕ", "accent": True, "size": "big"}]},
    {"start": 16.32, "end": 18.03, "lines": [{"text": "БЕЗ ВЫХОДА", "accent": False, "size": "small"}, {"text": "И ПОВТОРНОГО", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 20.10, "lines": [{"text": "ЖДАТЬ ОБЩЕГО", "accent": False, "size": "small"}, {"text": "ПЕРЕСЧЕТА", "accent": True, "size": "big"}]},
    {"start": 20.22, "end": 21.72, "lines": [{"text": "ПО РАСПИСАНИЮ", "accent": False, "size": "small"}, {"text": "НЕ ТРЕБУЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 22.56, "end": 23.70, "lines": [{"text": "МЕСТО В РЕЙТИНГЕ", "accent": False, "size": "small"}, {"text": "МЕНЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 23.94, "end": 25.38, "lines": [{"text": "СРАЗУ А НЕ", "accent": False, "size": "small"}, {"text": "НА СЛЕДУЮЩИЙ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 26.16, "end": 27.96, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.06, "end": 3.45}, {"start": 7.23, "end": 7.71}, {"start": 23.37, "end": 23.70}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (parent host, 25.068s): worried there is no time for the daily
# task before school in the morning; the app lets the task be closed in
# advance the evening before if the morning will be packed
# ---------------------------------------------------------------------------
e_intro = {"lines": ["НЕТ ВРЕМЕНИ УТРОМ", "НА ЗАДАНИЕ ДНЯ?"], "end": 2.3}
e_cards = [
    {"start": 2.70, "end": 3.60, "lines": [{"text": "ЧТО УТРОМ", "accent": False, "size": "small"}, {"text": "ПЕРЕД ШКОЛОЙ", "accent": True, "size": "big"}]},
    {"start": 3.81, "end": 4.92, "lines": [{"text": "НА ЗАДАНИЕ ДНЯ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.07, "end": 6.30, "lines": [{"text": "СОВСЕМ НЕ", "accent": False, "size": "small"}, {"text": "ОСТАЕТСЯ ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 6.99, "end": 8.01, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОЗВОЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 8.97, "lines": [{"text": "ЗАКРЫТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ДНЯ", "accent": True, "size": "big"}]},
    {"start": 9.09, "end": 9.90, "lines": [{"text": "ЗАРАНЕЕ С", "accent": False, "size": "small"}, {"text": "ВЕЧЕРА", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.73, "lines": [{"text": "ЕСЛИ УТРО", "accent": False, "size": "small"}, {"text": "ТОЧНО ПЛОТНЫМ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.23, "lines": [{"text": "ЗАДАНИЕ НЕ", "accent": False, "size": "small"}, {"text": "ПРОПАДАЮТ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.55, "lines": [{"text": "И НЕ СГОРАЮТ ЕСЛИ", "accent": False, "size": "small"}, {"text": "РЕШЕНО", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 16.11, "lines": [{"text": "ПОДСТРАИВАТЬСЯ", "accent": False, "size": "small"}, {"text": "НАКАНУНЕ", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.88, "lines": [{"text": "ПОД СВОБОДНОЕ УТРО КАЖДЫЙ РАЗ", "accent": False, "size": "small"}, {"text": "ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 18.06, "end": 19.62, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ ДНЯ", "accent": True, "size": "big"}]},
    {"start": 19.80, "end": 20.94, "lines": [{"text": "МОЖНО", "accent": False, "size": "small"}, {"text": "ЗАКРЫТЬ ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 21.12, "end": 22.74, "lines": [{"text": "ВЕЧЕРОМ ЕСЛИ", "accent": False, "size": "small"}, {"text": "УТРО ПЛОТНЫМ", "accent": True, "size": "big"}]},
    {"start": 23.22, "end": 24.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.10, "end": 2.52}, {"start": 7.68, "end": 8.01}, {"start": 15.54, "end": 16.11}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (girl-bookshelf, 28.400s): interrupts a mock exam halfway and
# can't remember which task was left off; the app remembers the exact task
# where it was interrupted, resuming there without scrolling the whole
# variant again
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ПРЕРВАЛ ПРОБНИК", "И ЗАБЫЛ МЕСТО?"], "end": 2.3}
f_cards = [
    {"start": 2.73, "end": 3.99, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "СЕРЕДИНЕ И ПОТОМ", "accent": True, "size": "big"}]},
    {"start": 4.26, "end": 5.43, "lines": [{"text": "НЕ ПОМНЯТ", "accent": False, "size": "small"}, {"text": "НА КАКОМ ЗАДАНИИ", "accent": True, "size": "big"}]},
    {"start": 5.61, "end": 6.69, "lines": [{"text": "ОСТАНОВИЛИСЬ", "accent": False, "size": "small"}, {"text": "ПРОШЛЫЙ РАЗ", "accent": True, "size": "big"}]},
    {"start": 7.53, "end": 8.76, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.26, "lines": [{"text": "ТОЧНОЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "НА КОТОРОМ", "accent": True, "size": "big"}]},
    {"start": 10.47, "end": 11.97, "lines": [{"text": "ПРОБНИК БЫЛ", "accent": False, "size": "small"}, {"text": "ПРЕРВАН В ПРОШЛЫЙ РАЗ", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 14.52, "lines": [{"text": "ПРОДОЛЖИТЬ МОЖНО", "accent": False, "size": "small"}, {"text": "РОВНО С ЭТОГО МЕСТА", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 16.02, "lines": [{"text": "БЕЗ ПРОЛИСТЫВАНИЯ", "accent": False, "size": "small"}, {"text": "ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 16.11, "end": 17.85, "lines": [{"text": "ВАРИАНТА", "accent": False, "size": "small"}, {"text": "ВСПОМИНАТЬ", "accent": True, "size": "big"}]},
    {"start": 18.06, "end": 19.20, "lines": [{"text": "МЕСТО ОСТАНОВКИ", "accent": False, "size": "small"}, {"text": "ПО ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 20.40, "lines": [{"text": "БОЛЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "ТРЕБУЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 21.36, "end": 22.47, "lines": [{"text": "МЕСТО ОСТАНОВКИ", "accent": False, "size": "small"}, {"text": "В ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 22.71, "end": 23.70, "lines": [{"text": "ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "САМО", "accent": True, "size": "big"}]},
    {"start": 24.30, "end": 25.86, "lines": [{"text": "БЕЗ ПРОЛИСТЫВАНИЯ", "accent": False, "size": "small"}, {"text": "ВАРИАНТА ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 26.55, "end": 27.96, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.26, "end": 1.62}, {"start": 8.34, "end": 8.76}, {"start": 22.71, "end": 23.28}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
