#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTIETH 'coffee123'
batch (6 episodes uploaded under the same tag after twenty-nine prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes77/.

Two new hosts, no returning faces: blonde girl in cream sweater (a, d, f),
brunette girl in blue shirt / "room with THE SMITHS poster" (b, c, e).

Sub-themes: outdated/unverified source material (an old textbook scan,
a stranger's flash drive) vs. the app's up-to-date FIPI bank (a, b);
knowing something "in general terms" without surviving a precise/
different-context test -- a history term, a math formula, a grammar
rule, a dictation mistake (c, d, e, f).
"""
import json

REAL_DURATION = {
    "a": 24.023, "b": 21.960, "c": 23.618,
    "d": 21.960, "e": 24.520, "f": 22.764,
}
SOURCE_FILE = {
    "a": "ewrgfhfrewertghj", "b": "ewrgfhgtretgthf", "c": "fgdgdgdsfgdgd",
    "d": "ghtrerghffre", "e": "hjghytertgfhj", "f": "nghretfghgtre",
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
    "c": {"дле": "для", "профил": "профиля"},
    "e": {"растиряться": "растеряться", "профил": "профиля"},
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
    words = json.load(open(f"../asr_coffee123_30/{src}_words.json"))
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
# Episode A (blonde girl, 24.023s): tasks collected from image-search
# screenshots turn out to be a scan from a textbook 5 years old; the app's
# FIPI bank is verified and current-year
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗАДАНИЯ ИЗ", "ПОИСКА КАРТИНОК?"], "end": 1.71}
a_cards = [
    {"start": 1.71, "end": 3.06, "lines": [{"text": "НАЙДЕННОЕ ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ПОИСК КАРТИНОК", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 4.95, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ВЫРЕЗКОЙ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.78, "lines": [{"text": "ИЗ УЧЕБНИКА ПЯТИЛЕТНЕЙ", "accent": False, "size": "small"}, {"text": "ДАВНОСТИ", "accent": True, "size": "big"}]},
    {"start": 8.01, "end": 9.21, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "СОБИРАЛА", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.38, "lines": [{"text": "ЗАДАНИЯ ПО", "accent": False, "size": "small"}, {"text": "СКРИНШОТАМ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.91, "lines": [{"text": "ЦЕЛЫЙ МЕСЯЦ", "accent": False, "size": "small"}, {"text": "УЧИТЕЛЬ", "accent": True, "size": "big"}]},
    {"start": 11.91, "end": 12.72, "lines": [{"text": "ИХ", "accent": False, "size": "small"}, {"text": "ПРЕЖНЮЮ", "accent": True, "size": "big"}]},
    {"start": 12.72, "end": 14.43, "lines": [{"text": "ДАВНО", "accent": False, "size": "small"}, {"text": "ИЗМЕНЕННУЮ", "accent": True, "size": "big"}]},
    {"start": 16.11, "end": 16.93, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.93, "end": 18.09, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 19.95, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫМИ", "accent": True, "size": "small"}]},
    {"start": 19.95, "end": 21.33, "lines": [{"text": "ЗАДАНИЯМИ ТЕКУЩЕГО", "accent": False, "size": "small"}, {"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 22.02, "end": 23.04, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.04, "end": 24.023, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 5.82, "end": 6.78}, {"start": 11.13, "end": 11.91}, {"start": 17.46, "end": 18.09}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (brunette girl, 21.960s): training off a stranger's flash
# drive risks a 3-year-old file; the app's FIPI bank updates for the
# current year, no random archives
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ТРЕНИРУЕШЬСЯ ПО", "ЧУЖОЙ ФЛЕШКЕ?"], "end": 1.56}
b_cards = [
    {"start": 1.56, "end": 2.97, "lines": [{"text": "ПО ЗАДАНИЯМ С ЧУЖОЙ", "accent": False, "size": "small"}, {"text": "ФЛЕШКИ", "accent": True, "size": "big"}]},
    {"start": 2.97, "end": 4.08, "lines": [{"text": "ЭТО РИСК", "accent": False, "size": "small"}, {"text": "НАРВАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 5.49, "lines": [{"text": "НА ФАЙЛ", "accent": False, "size": "small"}, {"text": "ТРЕХЛЕТНЕЙ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.17, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ДЕСЯТЬ", "accent": True, "size": "big"}]},
    {"start": 7.17, "end": 8.31, "lines": [{"text": "ДНЕЙ РЕШАЛА", "accent": False, "size": "small"}, {"text": "АРХИВ", "accent": True, "size": "big"}]},
    {"start": 8.31, "end": 9.90, "lines": [{"text": "С ФЛЕШКИ", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИЦЫ", "accent": True, "size": "small"}]},
    {"start": 9.90, "end": 11.10, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "СВЕРИЛИ", "accent": True, "size": "big"}]},
    {"start": 11.10, "end": 11.97, "lines": [{"text": "С НОВОЙ", "accent": False, "size": "small"}, {"text": "ВЕРСИЕЙ", "accent": True, "size": "big"}]},
    {"start": 13.26, "end": 14.08, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.08, "end": 15.18, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 17.01, "lines": [{"text": "С ЗАДАНИЯМИ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЯЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 17.01, "end": 17.82, "lines": [{"text": "ПОД ТЕКУЩИЙ", "accent": False, "size": "small"}, {"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 17.82, "end": 19.41, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНЫХ", "accent": True, "size": "big"}]},
    {"start": 20.01, "end": 21.09, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.09, "end": 21.960, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.62, "end": 5.49}, {"start": 8.43, "end": 9.00}, {"start": 14.58, "end": 15.18}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (brunette girl, 23.618s): a history term explained in your
# own words doesn't survive a multiple-choice test; the app's memorization
# games train recognition of exact wordings
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЗНАЕШЬ ТЕРМИН", "НО НЕ УЗНАЁШЬ В ТЕСТЕ?"], "end": 1.74}
c_cards = [
    {"start": 1.74, "end": 3.15, "lines": [{"text": "ПО ИСТОРИИ ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.53, "lines": [{"text": "НА СЛОВАХ И НЕ", "accent": False, "size": "small"}, {"text": "УЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 4.53, "end": 5.61, "lines": [{"text": "В ТЕСТЕ С", "accent": False, "size": "small"}, {"text": "ВАРИАНТАМИ", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 7.62, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ПУТАЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 9.03, "lines": [{"text": "НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ФОРМУЛИРОВКАХ", "accent": True, "size": "small"}]},
    {"start": 9.03, "end": 10.50, "lines": [{"text": "ХОТЯ СВОИМИ", "accent": False, "size": "small"}, {"text": "СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.61, "lines": [{"text": "ОБЪЯСНЯЛА", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 12.81, "lines": [{"text": "ПОДРУГЕ", "accent": False, "size": "small"}, {"text": "БЕЗ ЗАПИНКИ", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 14.65, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.65, "end": 15.66, "lines": [{"text": "ПО ИСТОРИИ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 16.80, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.80, "end": 18.84, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "УЗНАВАНИЕ", "accent": True, "size": "big"}]},
    {"start": 18.84, "end": 19.92, "lines": [{"text": "ТОЧНЫХ", "accent": False, "size": "small"}, {"text": "ФОРМУЛИРОВОК", "accent": True, "size": "small"}]},
    {"start": 19.92, "end": 20.85, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 21.57, "end": 22.74, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.74, "end": 23.618, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.83, "end": 5.61}, {"start": 11.43, "end": 12.06}, {"start": 15.84, "end": 16.80}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blonde girl, 21.960s): similar math formulas are easy to mix
# up even when both are known by heart; the app's text breakdown shows
# which formula and why
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПУТАЕШЬ ФОРМУЛЫ", "НА ЕГЭ ПО МАТЕМАТИКЕ?"], "end": 1.77}
d_cards = [
    {"start": 1.77, "end": 2.56, "lines": [{"text": "ЛЕГКО", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАТЬ", "accent": True, "size": "big"}]},
    {"start": 2.56, "end": 3.51, "lines": [{"text": "ПОХОЖИЕ", "accent": False, "size": "small"}, {"text": "ФОРМУЛЫ", "accent": True, "size": "big"}]},
    {"start": 3.51, "end": 5.31, "lines": [{"text": "И ПРИМЕНИТЬ НЕ ТУ", "accent": False, "size": "small"}, {"text": "ЧТО НУЖНО", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 7.83, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ОДНАЖДЫ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.18, "lines": [{"text": "РЕШИЛА НЕ ТОЙ", "accent": False, "size": "small"}, {"text": "ФОРМУЛОЙ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 9.99, "lines": [{"text": "ХОТЯ", "accent": False, "size": "small"}, {"text": "ДОМА", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 11.19, "lines": [{"text": "ПИСАЛА ОБЕ", "accent": False, "size": "small"}, {"text": "ФОРМУЛЫ", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 12.42, "lines": [{"text": "ПО ПАМЯТИ", "accent": False, "size": "small"}, {"text": "БЕЗ ОШИБОК", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.25, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 16.02, "lines": [{"text": "ЕСТЬ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.02, "end": 17.16, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.16, "end": 18.09, "lines": [{"text": "КАКУЮ", "accent": False, "size": "small"}, {"text": "ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 19.56, "lines": [{"text": "И ПОЧЕМУ", "accent": False, "size": "small"}, {"text": "ПРИМЕНИТЬ", "accent": True, "size": "big"}]},
    {"start": 20.13, "end": 21.16, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.16, "end": 21.960, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.16, "end": 2.52}, {"start": 8.46, "end": 9.18}, {"start": 16.74, "end": 17.16}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (brunette girl, 24.520s): explaining one grammar rule well
# doesn't stop you getting lost on the similar neighboring one; the app's
# text breakdown sorts similar rules into separate "shelves"
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОБЪЯСНИЛ ПРАВИЛО", "И ЗАБЫЛ СОСЕДНЕЕ?"], "end": 1.68}
e_cards = [
    {"start": 1.68, "end": 2.50, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 2.50, "end": 3.45, "lines": [{"text": "МОЖНО ВЕРНО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 4.27, "lines": [{"text": "ОДНО", "accent": False, "size": "small"}, {"text": "ПРАВИЛО", "accent": True, "size": "big"}]},
    {"start": 4.27, "end": 5.31, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 5.31, "end": 6.48, "lines": [{"text": "НА СОСЕДНЕМ", "accent": False, "size": "small"}, {"text": "ПОХОЖЕМ", "accent": True, "size": "big"}]},
    {"start": 8.01, "end": 9.75, "lines": [{"text": "Я ПУТАЛА ПОХОЖИЕ", "accent": False, "size": "small"}, {"text": "МЕСТАМИ", "accent": True, "size": "big"}]},
    {"start": 9.75, "end": 11.58, "lines": [{"text": "ХОТЯ КАЖДАЯ ПО", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНОСТИ", "accent": True, "size": "small"}]},
    {"start": 11.58, "end": 13.02, "lines": [{"text": "ОБЪЯСНЯЛА СЕБЕ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 13.02, "end": 14.31, "lines": [{"text": "БЕЗ ЕДИНОЙ", "accent": False, "size": "small"}, {"text": "ЗАПИНКИ", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 16.23, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.23, "end": 17.88, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 17.88, "end": 19.41, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "РАЗВОДИТ", "accent": True, "size": "big"}]},
    {"start": 19.41, "end": 21.42, "lines": [{"text": "ПОХОЖИЕ ПРАВИЛА ПО РАЗНЫМ", "accent": False, "size": "small"}, {"text": "ПОЛОЧКАМ", "accent": True, "size": "big"}]},
    {"start": 22.29, "end": 23.61, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.61, "end": 24.520, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 4.83, "end": 5.31}, {"start": 8.19, "end": 8.94}, {"start": 21.09, "end": 21.42}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde girl, 22.764s): knowing spelling rules in theory
# doesn't stop the same words tripping you up in dictation; the app's
# memorization games reinforce rules directly on words, not just theory
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗНАЕШЬ ПРАВИЛА", "НО ТЕРЯЕШЬ БАЛЛЫ?"], "end": 1.83}
f_cards = [
    {"start": 1.83, "end": 2.97, "lines": [{"text": "ДЛЯ ЕГЭ МОЖНО", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 2.97, "end": 4.41, "lines": [{"text": "В ТЕОРИИ И ТЕРЯТЬ", "accent": False, "size": "small"}, {"text": "БАЛЛЫ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 5.55, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "КОНКРЕТНЫХ", "accent": True, "size": "big"}]},
    {"start": 6.51, "end": 7.62, "lines": [{"text": "Я", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЛА", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.44, "lines": [{"text": "ПРАВИЛА", "accent": False, "size": "small"}, {"text": "БЕЗУПРЕЧНО", "accent": True, "size": "big"}]},
    {"start": 8.44, "end": 9.81, "lines": [{"text": "А", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 9.81, "end": 11.04, "lines": [{"text": "ПОЧЕМУ ТО КАЖДЫЙ", "accent": False, "size": "small"}, {"text": "РАЗ", "accent": True, "size": "big"}]},
    {"start": 11.04, "end": 12.48, "lines": [{"text": "ОКАЗЫВАЛИСЬ", "accent": False, "size": "small"}, {"text": "ИМЕННО", "accent": True, "size": "big"}]},
    {"start": 13.47, "end": 14.27, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.27, "end": 15.45, "lines": [{"text": "ПО РУССКОМУ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.45, "end": 16.56, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.56, "end": 18.27, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "big"}]},
    {"start": 18.27, "end": 19.23, "lines": [{"text": "ПРАВИЛА ПРЯМО", "accent": False, "size": "small"}, {"text": "НА СЛОВАХ", "accent": True, "size": "big"}]},
    {"start": 19.23, "end": 20.46, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "В ТЕОРИИ", "accent": True, "size": "big"}]},
    {"start": 21.12, "end": 21.94, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.94, "end": 22.764, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 7.74, "end": 8.40}, {"start": 11.94, "end": 12.48}, {"start": 17.49, "end": 17.82}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
