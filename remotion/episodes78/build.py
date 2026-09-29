#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-FIRST 'coffee123'
batch (9 episodes uploaded under the same tag after thirty prior batches
were delivered). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes78/.

Two returning hosts, no new faces: "Рома" HeyGen avatar (a, b, c, d, e, f),
blue-shirt brunette HeyGen avatar (g, h, i).

Sub-themes: outdated/unverified source material (a stale methodichka, an
old file from a random site, saved phone notes) vs. the app's up-to-date
FIPI bank (b, d, g); knowing something "in general terms" without
surviving a precise/different-context test -- a date, a pattern, an
analogy, a classification order, a term, a grammar rule (a, c, e, f, h, i).
"""
import json

REAL_DURATION = {
    "a": 18.562, "b": 19.266, "c": 18.690,
    "d": 16.258, "e": 18.604, "f": 21.880,
    "g": 20.802, "h": 23.042, "i": 22.082,
}
SOURCE_FILE = {
    "a": "hgffhhjghfghf", "b": "hgfgfnbfhnfxh", "c": "hgfhjggfdg",
    "d": "hgkgjuytrjh", "e": "hmgvnndfhngfdnhd", "f": "mjdhgfmmfgmm",
    "g": "mnvmb.mbvbv", "h": "ncncngndfnfdn", "i": "vgcbnb.d",
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


FIXES = {
    "b": {"фипис": "фипи"},
    "d": {"фипис": "фипи"},
    "g": {"профил": "профиля"},
}


def fix_words(letter, words):
    """Repair known sherpa-onnx ASR mis-transcriptions before captioning."""
    fixes = FIXES.get(letter, {})
    for w in words:
        if w["text"] in fixes:
            w["text"] = fixes[w["text"]]
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_31/{src}_words.json"))
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
# Episode A (Рома, 18.562s): a familiar history date can get mixed up
# with a very similar neighboring date; the app's history games train
# exactly similar dates
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗНАКОМАЯ ДАТА", "МОЖЕТ ПОДВЕСТИ?"], "end": 1.53}
a_cards = [
    {"start": 1.53, "end": 2.35, "lines": [{"text": "ЗНАКОМАЯ", "accent": False, "size": "small"}, {"text": "ДАТА", "accent": True, "size": "big"}]},
    {"start": 2.35, "end": 3.51, "lines": [{"text": "ДЛЯ ЕГЭ МОЖЕТ", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 3.51, "end": 5.43, "lines": [{"text": "С ОЧЕНЬ ПОХОЖЕЙ", "accent": False, "size": "small"}, {"text": "СОСЕДНЕЙ", "accent": True, "size": "big"}]},
    {"start": 5.79, "end": 6.93, "lines": [{"text": "Я УВЕРЕННО", "accent": False, "size": "small"}, {"text": "НАЗЫВАЛ", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.19, "lines": [{"text": "ДАТУ НА УРОКЕ", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.39, "lines": [{"text": "ПЕРЕПУТАЛ ЕЕ С", "accent": False, "size": "small"}, {"text": "СОБЫТИЕМ", "accent": True, "size": "big"}]},
    {"start": 9.39, "end": 10.98, "lines": [{"text": "БУКВАЛЬНО ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 11.43, "end": 12.22, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.22, "end": 13.29, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 13.29, "end": 14.88, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 14.88, "end": 16.65, "lines": [{"text": "ИМЕННО ПОХОЖИХ", "accent": False, "size": "small"}, {"text": "ДАТ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 17.77, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.77, "end": 18.562, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.23, "end": 5.13}, {"start": 8.31, "end": 9.39}, {"start": 13.56, "end": 13.98}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (Рома, 19.266s): a task downloaded with a movie from a random
# site is not the most reliable source; the app's FIPI bank updates for
# the current year, no random archives
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СКАЧАЛ ЗАДАНИЕ", "ВМЕСТЕ С ФИЛЬМОМ?"], "end": 1.50}
b_cards = [
    {"start": 1.50, "end": 2.40, "lines": [{"text": "ЕГЭ СКАЧАННОЕ ВМЕСТЕ", "accent": False, "size": "small"}, {"text": "С ФИЛЬМОМ", "accent": True, "size": "big"}]},
    {"start": 2.40, "end": 3.27, "lines": [{"text": "СО", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНОГО", "accent": True, "size": "big"}]},
    {"start": 3.27, "end": 4.62, "lines": [{"text": "ТОЧНО НЕ САМЫЙ", "accent": False, "size": "small"}, {"text": "НАДЕЖНЫЙ", "accent": True, "size": "big"}]},
    {"start": 4.62, "end": 5.67, "lines": [{"text": "ИСТОЧНИК ДЛЯ", "accent": False, "size": "small"}, {"text": "ПОДГОТОВКИ", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 7.68, "lines": [{"text": "Я ТАК СЛУЧАЙНО", "accent": False, "size": "small"}, {"text": "НАШЕЛ", "accent": True, "size": "big"}]},
    {"start": 7.68, "end": 8.67, "lines": [{"text": "АРХИВ С", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 8.67, "end": 9.84, "lines": [{"text": "И РЕШАЛ ЕГО", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 11.52, "lines": [{"text": "ПОКА НЕ ЗАМЕТИЛ", "accent": False, "size": "small"}, {"text": "СТАРЫЙ ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 11.79, "end": 12.58, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.58, "end": 13.62, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 14.85, "lines": [{"text": "С ЗАДАНИЯМИ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЕННЫМИ", "accent": True, "size": "small"}]},
    {"start": 14.85, "end": 15.69, "lines": [{"text": "ПОД ТЕКУЩИЙ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 15.69, "end": 17.22, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНЫХ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 18.47, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.47, "end": 19.266, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.58, "end": 3.27}, {"start": 10.41, "end": 11.52}, {"start": 13.32, "end": 13.62}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (Рома, 18.690s): guessing a pattern is easier than proving it
# to the teacher in words; the app's text breakdown proves the pattern,
# not just guesses it
# ---------------------------------------------------------------------------
c_intro = {"lines": ["УГАДАЛ ЗАКОНОМЕРНОСТЬ", "НЕ СМОГ ДОКАЗАТЬ?"], "end": 1.65}
c_cards = [
    {"start": 1.65, "end": 2.58, "lines": [{"text": "ЗАДАНИЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПРОЩЕ", "accent": True, "size": "big"}]},
    {"start": 2.58, "end": 4.11, "lines": [{"text": "ЧЕМ ПОТОМ", "accent": False, "size": "small"}, {"text": "ДОКАЗАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 4.90, "lines": [{"text": "СЛОВАМИ", "accent": False, "size": "small"}, {"text": "УЧИТЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 6.57, "lines": [{"text": "Я УГАДЫВАЛ", "accent": False, "size": "small"}, {"text": "ЗАКОНОМЕРНОСТЬ", "accent": True, "size": "small"}]},
    {"start": 6.57, "end": 7.36, "lines": [{"text": "В ЧИСЛАХ", "accent": False, "size": "small"}, {"text": "БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 7.36, "end": 8.46, "lines": [{"text": "А ДОКАЗАТЬ ЕЕ", "accent": False, "size": "small"}, {"text": "УЧИТЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 8.46, "end": 10.41, "lines": [{"text": "СЛОВАМИ ПОЛУЧАЛОСЬ", "accent": False, "size": "small"}, {"text": "ХУЖЕ", "accent": True, "size": "big"}]},
    {"start": 11.10, "end": 11.89, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.89, "end": 13.44, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.40, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ДОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 14.40, "end": 16.47, "lines": [{"text": "ЗАКОНОМЕРНОСТЬ А НЕ", "accent": False, "size": "small"}, {"text": "УГАДЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 16.74, "end": 17.79, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.79, "end": 18.690, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.19, "end": 6.12}, {"start": 9.12, "end": 10.41}, {"start": 14.07, "end": 14.40}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (Рома, 16.258s): an old methodichka can be older than it
# looks; the app's FIPI bank updates for the current year
# ---------------------------------------------------------------------------
d_intro = {"lines": ["МЕТОДИЧКА ОТ", "СТАРШЕГО КЛАССА?"], "end": 1.74}
d_cards = [
    {"start": 1.74, "end": 2.58, "lines": [{"text": "ЗАДАНИЯМИ ЕГЭ", "accent": False, "size": "small"}, {"text": "ДОСТАВШАЯСЯ", "accent": True, "size": "small"}]},
    {"start": 2.58, "end": 3.57, "lines": [{"text": "ОТ ПРЕДЫДУЩЕГО", "accent": False, "size": "small"}, {"text": "КЛАССА", "accent": True, "size": "big"}]},
    {"start": 3.57, "end": 5.55, "lines": [{"text": "МОЖЕТ БЫТЬ НА ПАРУ ЛЕТ СТАРШЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "КАЖЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 5.76, "end": 6.81, "lines": [{"text": "Я РЕШАЛ ТАКУЮ", "accent": False, "size": "small"}, {"text": "МЕТОДИЧКУ", "accent": True, "size": "big"}]},
    {"start": 6.81, "end": 7.83, "lines": [{"text": "ВЕСЬ", "accent": False, "size": "small"}, {"text": "СЕНТЯБРЬ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.00, "lines": [{"text": "ПОКА НЕ СРАВНИЛ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.26, "lines": [{"text": "СО СВЕЖЕЙ", "accent": False, "size": "small"}, {"text": "ВЕРСИЕЙ", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 11.32, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.32, "end": 12.24, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.24, "end": 14.28, "lines": [{"text": "С ЗАДАНИЯМИ ОБНОВЛЕННЫМИ ПОД", "accent": False, "size": "small"}, {"text": "ТЕКУЩИЙ ГОД", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.46, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.46, "end": 16.258, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.01, "end": 2.58}, {"start": 8.07, "end": 8.76}, {"start": 11.97, "end": 12.24}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (Рома, 18.604s): an analogy with a similar task fails because
# of one unnoticed difference in conditions; the app's text breakdown
# notes the important difference between similar tasks
# ---------------------------------------------------------------------------
e_intro = {"lines": ["АНАЛОГИЯ С", "ПОХОЖИМ ЗАДАНИЕМ ПОДВЕЛА?"], "end": 1.50}
e_cards = [
    {"start": 1.50, "end": 2.46, "lines": [{"text": "ЗАДАНИЕМ ЕГЭ", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 2.46, "end": 3.69, "lines": [{"text": "ПОДВОДИТ ИЗ ЗА", "accent": False, "size": "small"}, {"text": "ОДНОГО", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 5.52, "lines": [{"text": "НЕЗАМЕЧЕННОГО ОТЛИЧИЯ", "accent": False, "size": "small"}, {"text": "В УСЛОВИИ", "accent": True, "size": "big"}]},
    {"start": 6.18, "end": 7.11, "lines": [{"text": "Я ТАК ОДНАЖДЫ", "accent": False, "size": "small"}, {"text": "ПЕРЕНЕС", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 8.37, "lines": [{"text": "РЕШЕНИЕ С", "accent": False, "size": "small"}, {"text": "ПРИМЕРА", "accent": True, "size": "big"}]},
    {"start": 8.37, "end": 9.66, "lines": [{"text": "НА ДРУГОЙ А", "accent": False, "size": "small"}, {"text": "ОТЛИЧИЕ", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 11.01, "lines": [{"text": "В УСЛОВИИ ВСЕ", "accent": False, "size": "small"}, {"text": "ИСПОРТИЛА", "accent": True, "size": "big"}]},
    {"start": 11.34, "end": 12.14, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.14, "end": 13.59, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 14.82, "lines": [{"text": "КОТОРЫЙ ОТМЕЧАЕТ", "accent": False, "size": "small"}, {"text": "ВАЖНОЕ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.53, "lines": [{"text": "ОТЛИЧИЕ МЕЖДУ", "accent": False, "size": "small"}, {"text": "ПОХОЖИМИ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 17.81, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.81, "end": 18.604, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 3.99, "end": 4.95}, {"start": 10.35, "end": 11.01}, {"start": 14.07, "end": 14.82}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 21.880s): a classification memorized as one block can
# lose element order when retelling; the app's games train element
# order, not just the list
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ВЫУЧИЛ КЛАССИФИКАЦИЮ", "А ПОРЯДОК ЗАБЫЛ?"], "end": 1.50}
f_cards = [
    {"start": 1.50, "end": 2.55, "lines": [{"text": "ПОНЯТИЙ ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 2.55, "end": 4.05, "lines": [{"text": "ДЛЯ ЕГЭ МОЖНО", "accent": False, "size": "small"}, {"text": "ЗАПОМНИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.05, "end": 4.95, "lines": [{"text": "ОДНИМ", "accent": False, "size": "small"}, {"text": "БЛОКОМ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 5.74, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 5.74, "end": 7.35, "lines": [{"text": "ПОРЯДОК ЭЛЕМЕНТОВ ПРИ", "accent": False, "size": "small"}, {"text": "ПЕРЕСКАЗЕ", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 8.65, "lines": [{"text": "Я ПОМНЮ", "accent": False, "size": "small"}, {"text": "ВСЮ", "accent": True, "size": "big"}]},
    {"start": 8.65, "end": 9.69, "lines": [{"text": "КЛАССИФИКАЦИЮ", "accent": False, "size": "small"}, {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.31, "lines": [{"text": "НО ПРИ ПЕРЕСКАЗЕ", "accent": False, "size": "small"}, {"text": "НА ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.27, "lines": [{"text": "ПОРЯДОК", "accent": False, "size": "small"}, {"text": "ЭЛЕМЕНТОВ", "accent": True, "size": "big"}]},
    {"start": 12.27, "end": 13.06, "lines": [{"text": "ВДРУГ", "accent": False, "size": "small"}, {"text": "СБИЛСЯ", "accent": True, "size": "big"}]},
    {"start": 13.29, "end": 14.08, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.08, "end": 15.24, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.24, "end": 16.68, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.68, "end": 18.21, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "ПОРЯДОК", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.56, "lines": [{"text": "А НЕ ТОЛЬКО ИХ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 19.89, "end": 21.03, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.03, "end": 21.880, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.22, "end": 5.61}, {"start": 11.52, "end": 12.57}, {"start": 16.86, "end": 17.67}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (blue-shirt brunette, 20.802s): a task saved in phone notes
# is easy to confuse with a fresher version of the same file; the app's
# FIPI bank is updated, no version confusion
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ЗАДАНИЕ В ЗАМЕТКАХ", "НА ТЕЛЕФОНЕ?"], "end": 1.50}
g_cards = [
    {"start": 1.50, "end": 3.00, "lines": [{"text": "ЕГЭ СОХРАНЕННОЕ", "accent": False, "size": "small"}, {"text": "В ЗАМЕТКАХ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "НА ТЕЛЕФОНЕ ЛЕГКО", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.52, "lines": [{"text": "С БОЛЕЕ", "accent": False, "size": "small"}, {"text": "СВЕЖЕЙ", "accent": True, "size": "big"}]},
    {"start": 5.52, "end": 6.31, "lines": [{"text": "ВЕРСИЕЙ ТОГО ЖЕ", "accent": False, "size": "small"}, {"text": "ФАЙЛА", "accent": True, "size": "big"}]},
    {"start": 7.11, "end": 7.98, "lines": [{"text": "Я РЕШАЛА", "accent": False, "size": "small"}, {"text": "СТАРЫЕ", "accent": True, "size": "big"}]},
    {"start": 7.98, "end": 9.06, "lines": [{"text": "ЗАМЕТКИ", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.50, "lines": [{"text": "ПОКА НЕ ЗАМЕТИЛА", "accent": False, "size": "small"}, {"text": "РЯДОМ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 12.42, "lines": [{"text": "СОВСЕМ ДРУГОЙ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЕННЫЙ", "accent": True, "size": "small"}]},
    {"start": 13.80, "end": 14.62, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.62, "end": 15.45, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 17.13, "lines": [{"text": "ОБНОВЛЕННЫЙ ПОД", "accent": False, "size": "small"}, {"text": "ТЕКУЩИЙ ГОД", "accent": True, "size": "big"}]},
    {"start": 17.67, "end": 18.66, "lines": [{"text": "БЕЗ ПУТАНИЦЫ", "accent": False, "size": "small"}, {"text": "ВЕРСИЙ", "accent": True, "size": "big"}]},
    {"start": 19.14, "end": 20.00, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.00, "end": 20.802, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 3.75, "end": 4.20}, {"start": 10.71, "end": 12.03}, {"start": 15.24, "end": 15.45}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blue-shirt brunette, 23.042s): a term known in the context
# of a paragraph can get lost when it appears alone in a test; the app's
# history games train the term specifically without context
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ТЕРМИН В ПАРАГРАФЕ", "БЕЗ НЕГО ТЕРЯЕШЬСЯ?"], "end": 1.59}
h_cards = [
    {"start": 1.59, "end": 2.67, "lines": [{"text": "ПО ИСТОРИИ ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 2.67, "end": 3.87, "lines": [{"text": "МОЖНО В", "accent": False, "size": "small"}, {"text": "КОНТЕКСТЕ", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 4.68, "lines": [{"text": "ПАРАГРАФА И", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 4.68, "end": 6.39, "lines": [{"text": "ВСТРЕТИВ ЕГО", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 7.35, "end": 8.73, "lines": [{"text": "Я УВЕРЕННО", "accent": False, "size": "small"}, {"text": "НАХОДИЛА", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 9.69, "lines": [{"text": "ТЕРМИН В ТЕКСТЕ", "accent": False, "size": "small"}, {"text": "УЧЕБНИКА", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.52, "lines": [{"text": "А В ТЕСТЕ БЕЗ", "accent": False, "size": "small"}, {"text": "КОНТЕКСТА", "accent": True, "size": "big"}]},
    {"start": 11.52, "end": 12.96, "lines": [{"text": "РАСТЕРЯЛАСЬ НА", "accent": False, "size": "small"}, {"text": "ПУСТОМ МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 14.19, "end": 15.00, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.26, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.70, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.70, "end": 19.08, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 19.08, "end": 20.52, "lines": [{"text": "ИМЕННО БЕЗ", "accent": False, "size": "small"}, {"text": "КОНТЕКСТА", "accent": True, "size": "big"}]},
    {"start": 21.12, "end": 22.17, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.17, "end": 23.042, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 4.26, "end": 4.68}, {"start": 11.73, "end": 12.66}, {"start": 17.82, "end": 18.21}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (blue-shirt brunette, 22.082s): every punctuation mark
# correct but not a single rule remembered; the app's text breakdown
# translates intuition into an understandable rule
# ---------------------------------------------------------------------------
i_intro = {"lines": ["РАССТАВИЛ ВСЕ ЗНАКИ", "НО ПРАВИЛА НЕ ПОМНИШЬ?"], "end": 2.13}
i_cards = [
    {"start": 2.13, "end": 3.48, "lines": [{"text": "МОЖНО РАССТАВИТЬ", "accent": False, "size": "small"}, {"text": "ВСЕ ЗНАКИ", "accent": True, "size": "big"}]},
    {"start": 3.48, "end": 4.30, "lines": [{"text": "ВСЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНО", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 6.12, "lines": [{"text": "И НЕ ВСПОМНИТЬ НИ", "accent": False, "size": "small"}, {"text": "ОДНОГО ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.40, "lines": [{"text": "Я ЗАКРЫЛА ЦЕЛЫЙ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.20, "lines": [{"text": "СОВСЕМ", "accent": False, "size": "small"}, {"text": "ИНТУИТИВНО", "accent": True, "size": "big"}]},
    {"start": 9.20, "end": 11.07, "lines": [{"text": "А ОБЪЯСНИТЬ ХОТЬ ОДНО", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 11.07, "end": 12.51, "lines": [{"text": "УЧИТЕЛЮ ПОТОМ", "accent": False, "size": "small"}, {"text": "НЕ СМОГЛА", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 14.63, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.63, "end": 16.50, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 18.15, "lines": [{"text": "КОТОРЫЙ ПЕРЕВОДИТ", "accent": False, "size": "small"}, {"text": "ИНТУИЦИЮ", "accent": True, "size": "big"}]},
    {"start": 18.15, "end": 19.38, "lines": [{"text": "В ПОНЯТНОЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 20.07, "end": 21.21, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 22.082, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 4.65, "end": 5.10}, {"start": 9.66, "end": 10.62}, {"start": 17.19, "end": 18.15}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
