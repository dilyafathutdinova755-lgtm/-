#!/usr/bin/env python3
"""One-off authoring + validation script for the NINETEENTH 'coffee123'
batch (9 episodes uploaded under the same tag after eighteen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes62/.

Four returning hosts, no new faces this time: the mother (parent POV,
"если ребенок"/"родители"), the brunette study-room host, the curly-
haired boy, and the blonde evening-room host. Three sub-themes repeat
across hosts: memorization games for the essay subjects instead of
re-reading conspects/terms, an up-to-date FIPI-sourced task bank
instead of stale internet collections of unknown origin, and a full
text explanation for every wrong answer instead of just glancing at
the correct one.
"""
import json

REAL_DURATION = {
    "a": 20.226, "b": 15.682, "c": 24.172,
    "d": 18.400, "e": 24.663, "f": 14.722,
    "g": 19.202, "h": 16.108, "i": 20.012,
}
SOURCE_FILE = {
    "a": "fdasfgretyraeyeytre", "b": "gfddgfdgdfgfdgdfgf", "c": "gvrsgehhrhhjjs",
    "d": "regrafttbyysryryry", "e": "sryyvtyryryrseggfdg", "f": "vgrdxgfxdffdhvgfdgf",
    "g": "vgrgsgdrgsrgdfg", "h": "vrdsgdgdfgfgdvgdvvg", "i": "vrgdsggrdgrdgvdrg",
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
    if letter == "d":
        for w in words:
            if abs(w["start"] - 18.30) < 0.02 and w["text"] == "проия":
                w["text"] = "профиля"
    if letter == "f":
        for w in words:
            if abs(w["start"] - 1.32) < 0.02 and w["text"] == "игэ":
                w["text"] = "егэ"
    if letter == "g":
        for w in words:
            if abs(w["start"] - 14.19) < 0.02 and w["text"] == "о":
                w["text"] = "от"
    if letter == "i":
        for w in words:
            if abs(w["start"] - 14.82) < 0.02 and w["text"] == "випи":
                w["text"] = "фипи"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_19/{src}_words.json"))
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
# Episode A (mother, 20.226s): memorizing dates by rote for history/social
# studies barely sticks; the app has memorization games for the essay
# subjects for a more durable result
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗАУЧИВАЕШЬ СПИСОК ДАТ", "НАИЗУСТЬ?"], "end": 3.0}
a_cards = [
    {"start": 3.15, "end": 6.96, "lines": [{"text": "ИНОГДА ПРОЩЕ ВЫУЧИТЬ СПИСОК ДАТ НАИЗУСТЬ ЧЕМ РАЗОБРАТЬСЯ ЗАЧЕМ ОН", "accent": False, "size": "small"}, {"text": "НУЖЕН", "accent": True, "size": "big"}]},
    {"start": 8.28, "end": 10.80, "lines": [{"text": "ТАКОЕ ЗАУЧИВАНИЕ ДЕРЖИТСЯ В ПАМЯТИ СОВСЕМ", "accent": False, "size": "small"}, {"text": "НЕДОЛГО", "accent": True, "size": "big"}]},
    {"start": 11.34, "end": 12.93, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 13.26, "end": 14.46, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЯ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 15.96, "lines": [{"text": "ЕСТЬ НА", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.14, "end": 17.55, "lines": [{"text": "ЗАПОМИНАНИЕ ДЛЯ БОЛЕЕ", "accent": False, "size": "small"}, {"text": "ПРОЧНОГО", "accent": True, "size": "big"}]},
    {"start": 18.39, "end": 20.31, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.15, "end": 3.48}, {"start": 11.34, "end": 11.67}, {"start": 18.39, "end": 18.72}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (mother, 15.682s): hard to tell from outside which variants a
# child is actually training on, and a lot of free material is outdated;
# the app's bank is sourced straight from FIPI
# ---------------------------------------------------------------------------
b_intro = {"lines": ["НЕ ПОНИМАЕШЬ ПО КАКИМ", "ВАРИАНТАМ ОН ГОТОВИТСЯ?"], "end": 2.34}
b_cards = [
    {"start": 2.46, "end": 4.53, "lines": [{"text": "НА САМОМ ДЕЛЕ", "accent": False, "size": "small"}, {"text": "ГОТОВЯТСЯ РЕБЕНОК", "accent": True, "size": "big"}]},
    {"start": 5.46, "end": 8.25, "lines": [{"text": "ЧАСТЬ ТАКИХ МАТЕРИАЛОВ В СВОБОДНОМ ДОСТУПЕ", "accent": False, "size": "small"}, {"text": "УСТАРЕЛА", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.81, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 11.67, "lines": [{"text": "СОБРАН АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 13.53, "lines": [{"text": "ЗАДАНИЯ ОТ СОСТАВИТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 15.78, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.46, "end": 2.79}, {"start": 8.70, "end": 9.03}, {"start": 13.98, "end": 14.31}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (brunette study-room host, 24.172s): grammar rules for Russian
# barely survive a single read before the next day; the app has
# memorization games for the essay subjects built on repetition
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПРАВИЛА ВЫВЕТРИВАЮТСЯ", "ЗА ОДИН ДЕНЬ?"], "end": 2.19}
c_cards = [
    {"start": 2.19, "end": 3.63, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ МНОГИЕ", "accent": False, "size": "small"}, {"text": "ПРАВИЛА", "accent": True, "size": "big"}]},
    {"start": 4.05, "end": 5.07, "lines": [{"text": "ДЕРЖАТСЯ В ГОЛОВЕ РОВНО ДО", "accent": False, "size": "small"}, {"text": "ДНЯ", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 8.43, "lines": [{"text": "ПРИЧИНА ОБЫЧНО НЕ В", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТИ", "accent": True, "size": "big"}]},
    {"start": 8.79, "end": 10.77, "lines": [{"text": "ПРАВИЛА А В ТОМ ЧТО ЕГО ОДИН РАЗ", "accent": False, "size": "small"}, {"text": "ПРОЧИТАЛИ", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.09, "lines": [{"text": "И ЗАКРЫЛИ", "accent": False, "size": "small"}, {"text": "УЧЕБНИК", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.16, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.31, "end": 15.18, "lines": [{"text": "ЕСТЬ НА", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.33, "end": 17.79, "lines": [{"text": "ЗАПОМИНАНИЕ ПО РУССКОМУ ЯЗЫКУ И", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 20.25, "lines": [{"text": "МАТЕРИАЛ ЗАКРЕПЛЯЕТСЯ ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 20.67, "end": 21.69, "lines": [{"text": "А НЕ ОДНО", "accent": False, "size": "small"}, {"text": "ПРОЧТЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 22.32, "end": 24.24, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.19, "end": 2.52}, {"start": 12.99, "end": 13.32}, {"start": 22.32, "end": 22.65}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (mother, 18.400s): a child solves honestly every day but keeps
# tripping on the same mistake, because it never gets reviewed step by
# step; the app gives a full text explanation of where each error comes
# from for every task
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СПОТЫКАЕТСЯ ОБ ОДНУ", "И ТУ ЖЕ ОШИБКУ?"], "end": 2.46}
d_cards = [
    {"start": 2.73, "end": 5.64, "lines": [{"text": "КАЖДЫЙ ДЕНЬ И ВСЕ РАВНО СПОТЫКАЕТСЯ ОБ ОДНО И ТУ ЖЕ", "accent": False, "size": "small"}, {"text": "ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 6.48, "end": 7.53, "lines": [{"text": "ДЕЛО ОБЫЧНО НЕ В", "accent": False, "size": "small"}, {"text": "ЛЕНИ", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 9.39, "lines": [{"text": "А В ТОМ ЧТО ОШИБКУ НИКТО НЕ", "accent": False, "size": "small"}, {"text": "РАЗБИРАЛ", "accent": True, "size": "big"}]},
    {"start": 9.57, "end": 10.83, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ШАГАМ", "accent": True, "size": "big"}]},
    {"start": 10.98, "end": 12.24, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ К КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 12.42, "end": 13.89, "lines": [{"text": "ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.04, "end": 16.02, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ ОТКУДА", "accent": False, "size": "small"}, {"text": "БЕРЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.51, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.73, "end": 3.06}, {"start": 10.98, "end": 11.31}, {"start": 16.80, "end": 17.13}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (brunette study-room host, 24.663s): a mistake looks random the
# first time and resurfaces a month later unreviewed; the app gives a full
# text explanation showing exactly where the error happens
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОШИБКА КАЖЕТСЯ", "СЛУЧАЙНОЙ?"], "end": 1.80}
e_cards = [
    {"start": 1.80, "end": 3.48, "lines": [{"text": "ЕГЭ ОШИБКА КАЖЕТСЯ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНОЙ", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 5.85, "lines": [{"text": "А ЧЕРЕЗ МЕСЯЦ ТА ЖЕ САМАЯ", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 6.12, "end": 7.17, "lines": [{"text": "ВСТРЕЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "СНОВА", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 10.50, "lines": [{"text": "ДЕЛО НЕ В НЕВНИМАТЕЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "ОБЫЧНО", "accent": True, "size": "big"}]},
    {"start": 10.89, "end": 13.86, "lines": [{"text": "А В ТОМ ЧТО ОШИБКУ ТАК НИКТО И НЕ РАЗОБРАЛ ПО", "accent": False, "size": "small"}, {"text": "ШАГАМ", "accent": True, "size": "big"}]},
    {"start": 14.64, "end": 16.02, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ К КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 16.74, "end": 18.48, "lines": [{"text": "ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 18.84, "end": 21.69, "lines": [{"text": "КОТОРЫЙ ПОКАЗЫВАЕТ ГДЕ ИМЕННО ВОЗНИКАЕТ", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 22.62, "end": 24.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.80, "end": 2.13}, {"start": 14.64, "end": 14.97}, {"start": 22.62, "end": 22.95}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-haired boy, 14.722s): solving whatever variants pop up
# first in a search rarely matches the real exam format; the app's bank is
# sourced from the actual FIPI task compilers
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РЕШАЕШЬ ЧТО НАШЛОСЬ", "ПЕРВЫМ В ПОИСКЕ?"], "end": 2.37}
f_cards = [
    {"start": 2.37, "end": 4.50, "lines": [{"text": "ВАРИАНТЫ ПРОСТО ПОТОМУ ЧТО ОНИ", "accent": False, "size": "small"}, {"text": "НАШЛИСЬ", "accent": True, "size": "big"}]},
    {"start": 4.92, "end": 6.90, "lines": [{"text": "НЕ ВСЕ ТАКИЕ ПОДБОРКИ ПЕРЕСЕКАЮТСЯ", "accent": False, "size": "small"}, {"text": "ВООБЩЕ", "accent": True, "size": "big"}]},
    {"start": 7.08, "end": 8.52, "lines": [{"text": "С НАСТОЯЩИМ", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 8.79, "end": 10.59, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ СОБРАН БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 12.75, "lines": [{"text": "ЗАДАНИЕ ОТ СОСТАВИТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "РЕАЛЬНОГО", "accent": True, "size": "big"}]},
    {"start": 13.05, "end": 14.79, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.37, "end": 2.70}, {"start": 8.79, "end": 9.12}, {"start": 13.05, "end": 13.38}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (blonde evening-room host, 19.202s): preparing from tasks of
# unknown origin is unreliable since much of it won't appear on the real
# exam; the app's bank is sourced from the people who actually write it
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ГОТОВИШЬСЯ ПО ЗАДАНИЯМ", "НЕИЗВЕСТНОГО ПРОИСХОЖДЕНИЯ?"], "end": 3.0}
g_cards = [
    {"start": 3.90, "end": 5.31, "lines": [{"text": "НЕ САМОЕ НАДЕЖНАЯ", "accent": False, "size": "small"}, {"text": "СТРАТЕГИЯ", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 6.93, "lines": [{"text": "ЧАСТЬ ТАКИХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 7.14, "end": 9.30, "lines": [{"text": "НЕ ВСТРЕТИТСЯ НА НАСТОЯЩЕМ ЭКЗАМЕНЕ", "accent": False, "size": "small"}, {"text": "ВООБЩЕ", "accent": True, "size": "big"}]},
    {"start": 10.26, "end": 11.58, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 12.96, "lines": [{"text": "СОБРАН АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 16.20, "lines": [{"text": "ЗАДАНИЕ ОТ ТЕХ КТО СОСТАВЛЯЕТ", "accent": False, "size": "small"}, {"text": "НАСТОЯЩИЕ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 18.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 3.90, "end": 4.23}, {"start": 10.26, "end": 10.59}, {"start": 17.01, "end": 17.34}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (curly-haired boy, 16.108s): losing points to the same
# unresolved mistake instead of a real knowledge gap; the app gives a full
# text explanation of the actual cause for every task
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ТЕРЯЕШЬ БАЛЛЫ НА ОДНОЙ", "И ТОЙ ЖЕ ОШИБКЕ?"], "end": 2.85}
h_cards = [
    {"start": 3.33, "end": 6.15, "lines": [{"text": "ИЗ ЗА ОДНОЙ И ТОЙ ЖЕ НЕВЫЯСНЕННОЙ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 7.86, "lines": [{"text": "ПОСМОТРЕТЬ ОТВЕТ НЕ ТО ЖЕ", "accent": False, "size": "small"}, {"text": "САМОЕ", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 9.06, "lines": [{"text": "ЧТО ПОНЯТЬ ГДЕ ПРОИЗОШЕЛ", "accent": False, "size": "small"}, {"text": "СБОЙ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.32, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 10.44, "end": 11.70, "lines": [{"text": "КАЖДОМУ ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВАЯ", "accent": True, "size": "big"}]},
    {"start": 12.18, "end": 13.65, "lines": [{"text": "РАЗБОР КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "ПРИЧИНУ", "accent": True, "size": "big"}]},
    {"start": 14.34, "end": 16.08, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.33, "end": 3.66}, {"start": 9.18, "end": 9.51}, {"start": 14.34, "end": 14.67}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (brunette study-room host, 20.012s): variants circulating in
# chats with no cited source drift from the current exam format; the app's
# bank is synced to the same formulations that will actually appear
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ГОТОВИШЬСЯ ПО ВАРИАНТАМ", "ИЗ ЧАТОВ?"], "end": 2.43}
i_cards = [
    {"start": 3.03, "end": 4.80, "lines": [{"text": "КОТОРЫЕ ГУЛЯЮТ ПО ЧАТАМ И", "accent": False, "size": "small"}, {"text": "ГРУППАМ", "accent": True, "size": "big"}]},
    {"start": 5.16, "end": 6.87, "lines": [{"text": "БЕЗ ЕДИНОГО УКАЗАНИЯ", "accent": False, "size": "small"}, {"text": "ИСТОЧНИКА", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.73, "lines": [{"text": "ПОЛОВИНА ТАКИХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 11.67, "lines": [{"text": "УЖЕ НЕ СООТВЕТСТВУЕТ НЫНЕШНИМ ФОРМУЛИРОВКАМ", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.80, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ МОЖНО", "accent": False, "size": "small"}, {"text": "РЕШАТЬ", "accent": True, "size": "big"}]},
    {"start": 14.01, "end": 15.00, "lines": [{"text": "АКТУАЛЬНЫЙ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 17.61, "lines": [{"text": "ТЕ ЖЕ ФОРМУЛИРОВКИ ЧТО БУДУТ В", "accent": False, "size": "small"}, {"text": "РЕАЛЬНЫХ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 20.01, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 3.03, "end": 3.36}, {"start": 12.33, "end": 12.66}, {"start": 18.09, "end": 18.42}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
