#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-SECOND 'coffee123'
batch (6 episodes uploaded under the same tag after thirty-one prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes79/.

Two returning hosts, no new faces: blonde-sweater HeyGen avatar
(a, e, f), mother HeyGen avatar (b, c, d).

Sub-themes: outdated/unverified source material (a friend's DMs, a
collection from random sources) vs. the app's up-to-date FIPI bank
(c, e); knowing something "in general terms" without surviving a
precise/different-context test -- a mental picture, forgotten logic,
a term's wording, a concept's wording (a, b, d, f).
"""
import json

REAL_DURATION = {
    "a": 23.255, "b": 20.162, "c": 20.460,
    "d": 23.490, "e": 20.546, "f": 25.772,
}
SOURCE_FILE = {
    "a": "bcxgdfgbessfgew", "b": "bnzdvxfdztts", "c": "gfbgsddgvfdsd",
    "d": "gfdgsfsfs", "e": "hgdfhdbdghrdge", "f": "xzdfgbszrvbzs",
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
    "a": {"профиль": "профиля"},
    "c": {"ягэ": "егэ"},
    "d": {"формулировко": "формулировке"},
    "f": {"растираться": "растеряться"},
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
    words = json.load(open(f"../asr_coffee123_32/{src}_words.json"))
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
# Episode A (blonde, 23.255s): a math task solved via a mental picture
# is hard to describe in words; the app's text breakdown translates
# the solution from head into understandable words
# ---------------------------------------------------------------------------
a_intro = {"lines": ["РЕШИЛ В УМЕ", "НЕ СМОГ ОБЪЯСНИТЬ?"], "end": 1.59}
a_cards = [
    {"start": 1.59, "end": 2.88, "lines": [{"text": "ЕГЭ ПО МАТЕМАТИКЕ", "accent": False, "size": "small"}, {"text": "РЕШИТЬ", "accent": True, "size": "big"}]},
    {"start": 2.88, "end": 3.99, "lines": [{"text": "ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "РИСУНОК", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.16, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "СУМЕТЬ", "accent": True, "size": "big"}]},
    {"start": 5.16, "end": 6.81, "lines": [{"text": "ОПИСАТЬ ЭТОТ РИСУНОК", "accent": False, "size": "small"}, {"text": "СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 7.74, "end": 8.82, "lines": [{"text": "Я ПРЕДСТАВЛЯЛА", "accent": False, "size": "small"}, {"text": "ЧЕРТЕЖ", "accent": True, "size": "big"}]},
    {"start": 8.82, "end": 9.90, "lines": [{"text": "В ГОЛОВЕ И", "accent": False, "size": "small"}, {"text": "РЕШАЛА", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 11.34, "lines": [{"text": "БЫСТРО А", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 11.34, "end": 13.17, "lines": [{"text": "РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИКАМ", "accent": True, "size": "small"}]},
    {"start": 13.17, "end": 14.00, "lines": [{"text": "С БОЛЬШИМ", "accent": False, "size": "small"}, {"text": "ТРУДОМ", "accent": True, "size": "big"}]},
    {"start": 14.85, "end": 15.65, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.65, "end": 17.52, "lines": [{"text": "ЗАДАНИЕМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 17.52, "end": 18.63, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПЕРЕВОДИТ", "accent": True, "size": "big"}]},
    {"start": 18.63, "end": 19.68, "lines": [{"text": "РЕШЕНИЕ ИЗ", "accent": False, "size": "small"}, {"text": "ГОЛОВЫ", "accent": True, "size": "big"}]},
    {"start": 19.68, "end": 20.73, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ПОНЯТНЫЕ СЛОВА", "accent": True, "size": "big"}]},
    {"start": 21.51, "end": 22.46, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.46, "end": 23.255, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.86, "end": 5.67}, {"start": 10.98, "end": 11.82}, {"start": 16.77, "end": 17.19}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 20.162s): a daughter can name the right answer but
# forget the logic a day later; the app's text breakdown saves the
# logic of every solution for a long time
# ---------------------------------------------------------------------------
b_intro = {"lines": ["НАЗВАЛА ОТВЕТ", "А ЛОГИКУ ЗАБЫЛА?"], "end": 1.50}
b_cards = [
    {"start": 1.50, "end": 3.03, "lines": [{"text": "ДОЧЬ МОЖЕТ НАЗВАТЬ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 3.99, "lines": [{"text": "И ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.52, "lines": [{"text": "НЕ ВСПОМНИТЬ", "accent": False, "size": "small"}, {"text": "ЛОГИКУ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.26, "lines": [{"text": "Я СПЕЦИАЛЬНО", "accent": False, "size": "small"}, {"text": "ПРОСИЛА", "accent": True, "size": "big"}]},
    {"start": 7.26, "end": 9.00, "lines": [{"text": "ЕЕ ПОВТОРИТЬ РЕШЕНИЕ", "accent": False, "size": "small"}, {"text": "ЧЕРЕЗ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.83, "lines": [{"text": "И ЛОГИКА ОБЫЧНО", "accent": False, "size": "small"}, {"text": "ТЕРЯЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 10.83, "end": 11.82, "lines": [{"text": "ГДЕ ТО НА", "accent": False, "size": "small"}, {"text": "СЕРЕДИНЕ", "accent": True, "size": "big"}]},
    {"start": 12.63, "end": 13.44, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 15.36, "lines": [{"text": "КАЖДОМУ ЗАДАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 16.83, "lines": [{"text": "КОТОРЫЙ СОХРАНЯЕТ", "accent": False, "size": "small"}, {"text": "ЛОГИКУ", "accent": True, "size": "big"}]},
    {"start": 16.83, "end": 17.79, "lines": [{"text": "РЕШЕНИЯ", "accent": False, "size": "small"}, {"text": "НАДОЛГО", "accent": True, "size": "big"}]},
    {"start": 18.27, "end": 19.35, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.35, "end": 20.162, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.26, "end": 4.65}, {"start": 10.53, "end": 10.83}, {"start": 16.05, "end": 16.41}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (mother, 20.460s): materials collected from different
# sources are rarely checked for relevance; the app's FIPI bank is
# updated for the current year, all in one place
# ---------------------------------------------------------------------------
c_intro = {"lines": ["МАТЕРИАЛЫ ИЗ РАЗНЫХ", "ИСТОЧНИКОВ НЕ ПРОВЕРЕНЫ?"], "end": 1.80}
c_cards = [
    {"start": 1.80, "end": 2.94, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "СОБРАННЫЕ", "accent": True, "size": "big"}]},
    {"start": 2.94, "end": 4.02, "lines": [{"text": "ДОЧЕРЬЮ ИЗ РАЗНЫХ", "accent": False, "size": "small"}, {"text": "ИСТОЧНИКОВ", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 6.42, "lines": [{"text": "РЕДКО ПРОВЕРЯЮТСЯ НА АКТУАЛЬНОСТЬ", "accent": False, "size": "small"}, {"text": "ВМЕСТЕ", "accent": True, "size": "small"}]},
    {"start": 7.05, "end": 7.84, "lines": [{"text": "Я РЕШИЛА", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 7.84, "end": 8.79, "lines": [{"text": "СВЕРИТЬ ЕЕ", "accent": False, "size": "small"}, {"text": "ПОДБОРКУ", "accent": True, "size": "big"}]},
    {"start": 8.79, "end": 10.29, "lines": [{"text": "С ОФИЦИАЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИЕЙ", "accent": True, "size": "small"}]},
    {"start": 10.29, "end": 12.39, "lines": [{"text": "И НАШЛА ТАМ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ПРОШЛЫХ ЛЕТ", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.03, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.03, "end": 15.15, "lines": [{"text": "СОБРАН БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 16.77, "lines": [{"text": "ОБНОВЛЕННЫЙ ПОД", "accent": False, "size": "small"}, {"text": "ТЕКУЩИЙ ГОД", "accent": True, "size": "big"}]},
    {"start": 16.77, "end": 17.64, "lines": [{"text": "В ОДНОМ", "accent": False, "size": "small"}, {"text": "МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 18.36, "end": 19.47, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.47, "end": 20.460, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.80, "end": 5.97}, {"start": 11.34, "end": 12.39}, {"start": 15.48, "end": 15.96}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (mother, 23.490s): a term known by conspectus can get lost
# seeing it in a different wording; the app's games train recognizing
# different wordings of one term
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗНАЕТ ПО КОНСПЕКТУ", "ТЕРЯЕТСЯ В ДРУГОЙ ФОРМУЛИРОВКЕ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "ЕГЭ ДОЧЬ МОЖЕТ", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 3.93, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "КОНСПЕКТУ", "accent": True, "size": "big"}]},
    {"start": 3.93, "end": 4.74, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 4.74, "end": 6.54, "lines": [{"text": "УВИДЕВ ЕГО В ДРУГОЙ", "accent": False, "size": "small"}, {"text": "ФОРМУЛИРОВКЕ", "accent": True, "size": "small"}]},
    {"start": 7.50, "end": 9.15, "lines": [{"text": "Я СЛУШАЛА КАК ОНА", "accent": False, "size": "small"}, {"text": "УВЕРЕННО", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.59, "lines": [{"text": "ЧИТАЕТ ТЕРМИН ПО", "accent": False, "size": "small"}, {"text": "КОНСПЕКТАМ", "accent": True, "size": "big"}]},
    {"start": 11.07, "end": 12.24, "lines": [{"text": "А НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ФОРМУЛИРОВКЕ", "accent": True, "size": "small"}]},
    {"start": 12.24, "end": 13.53, "lines": [{"text": "ВЫГЛЯДЕЛА", "accent": False, "size": "small"}, {"text": "СОВСЕМ ИНАЧЕ", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 15.46, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.46, "end": 16.56, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.56, "end": 17.64, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 17.64, "end": 19.38, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "УЗНАВАНИЯ", "accent": True, "size": "big"}]},
    {"start": 19.38, "end": 21.21, "lines": [{"text": "РАЗНЫХ ФОРМУЛИРОВОК", "accent": False, "size": "small"}, {"text": "ОДНОГО ТЕРМИНА", "accent": True, "size": "big"}]},
    {"start": 21.63, "end": 22.69, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.69, "end": 23.490, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.26, "end": 4.74}, {"start": 11.79, "end": 12.75}, {"start": 18.51, "end": 18.87}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde, 20.546s): a task from a friend's DMs doesn't always
# match the official exam format; the app's FIPI bank updates for the
# current year
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЗАДАНИЕ ОТ ПОДРУГИ", "В ЛИЧКЕ?"], "end": 1.50}
e_cards = [
    {"start": 1.50, "end": 2.30, "lines": [{"text": "ЕГЭ ПОЛУЧЕННОЕ ОТ", "accent": False, "size": "small"}, {"text": "ПОДРУГИ", "accent": True, "size": "big"}]},
    {"start": 2.30, "end": 3.24, "lines": [{"text": "В ЛИЧНЫХ", "accent": False, "size": "small"}, {"text": "СООБЩЕНИЯХ", "accent": True, "size": "big"}]},
    {"start": 3.24, "end": 4.47, "lines": [{"text": "НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 4.47, "end": 6.18, "lines": [{"text": "С ОФИЦИАЛЬНЫМ ФОРМАТОМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 8.13, "lines": [{"text": "Я РЕШАЛА", "accent": False, "size": "small"}, {"text": "ПРИСЛАННЫЕ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 8.94, "lines": [{"text": "ПОДРУГОЙ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 10.02, "lines": [{"text": "НЕДЕЛЮ ПОКА НЕ", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 10.02, "end": 12.30, "lines": [{"text": "СРЕДИ НИХ ДАВНО", "accent": False, "size": "small"}, {"text": "ИЗМЕНЕННУЮ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 13.99, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.99, "end": 14.79, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 16.83, "lines": [{"text": "С ЗАДАНИЯМИ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 16.83, "end": 17.82, "lines": [{"text": "ПОД ТЕКУЩИЙ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 18.48, "end": 19.62, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.62, "end": 20.546, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 4.05, "end": 4.47}, {"start": 10.77, "end": 11.61}, {"start": 14.61, "end": 14.79}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde, 25.772s): a concept known approximately falls apart
# seeing its exact wording in a test; the app's games train exactly the
# precise wording of a concept
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗНАЕШЬ ПОНЯТИЕ", "ПРИМЕРНО?"], "end": 1.98}
f_cards = [
    {"start": 1.98, "end": 3.24, "lines": [{"text": "ЕГЭ МОЖНО ЗНАТЬ", "accent": False, "size": "small"}, {"text": "ПРИМЕРНО", "accent": True, "size": "big"}]},
    {"start": 3.24, "end": 4.80, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 4.80, "end": 5.91, "lines": [{"text": "УВИДЕВ ЕГО", "accent": False, "size": "small"}, {"text": "ТОЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 5.91, "end": 7.02, "lines": [{"text": "ФОРМУЛИРОВКУ В", "accent": False, "size": "small"}, {"text": "ТЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.21, "lines": [{"text": "Я ОБЪЯСНЯЛА", "accent": False, "size": "small"}, {"text": "ПОНЯТИЕ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.65, "lines": [{"text": "СВОИМИ СЛОВАМИ", "accent": False, "size": "small"}, {"text": "УВЕРЕННО", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 12.30, "lines": [{"text": "А ТОЧНАЯ", "accent": False, "size": "small"}, {"text": "ФОРМУЛИРОВКА", "accent": True, "size": "small"}]},
    {"start": 12.30, "end": 13.77, "lines": [{"text": "В ТЕСТЕ ЗВУЧАЛА", "accent": False, "size": "small"}, {"text": "ДЛЯ МЕНЯ", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 14.88, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "НЕЗНАКОМО", "accent": True, "size": "big"}]},
    {"start": 15.99, "end": 16.78, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.78, "end": 18.39, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.39, "end": 19.83, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.83, "end": 21.39, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "ИМЕННО ТОЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 21.39, "end": 22.65, "lines": [{"text": "ФОРМУЛИРОВКУ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЯ", "accent": True, "size": "big"}]},
    {"start": 23.49, "end": 24.93, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 24.93, "end": 25.772, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.29, "end": 4.80}, {"start": 11.43, "end": 12.30}, {"start": 19.98, "end": 20.37}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
