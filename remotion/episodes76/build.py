#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-NINTH 'coffee123'
batch (9 episodes uploaded under the same tag after twenty-eight prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes76/.

Three returning hosts, no new faces: gray-shirt boy (a, b, c),
curly-hair boy (d, e, f), mother (g, h, i).

Sub-themes: unverified source material (a repost, a repetitor's variant,
a pre-made course) that drifted from the current exam vs. the app's
up-to-date FIPI bank (a, d, h), knowing something "in general terms"
without surviving a precise/different-context test -- a term, a
calculation shortcut, a date order, a repeated mistake (b, c, e, f, g,
i).
"""
import json

REAL_DURATION = {
    "a": 18.775, "b": 19.266, "c": 17.218,
    "d": 18.480, "e": 20.098, "f": 18.840,
    "g": 20.460, "h": 18.400, "i": 20.098,
}
SOURCE_FILE = {
    "a": "fdgghj.gjtyretthjhg", "b": "fgjfjhgewre", "c": "hjghftffhmjgytrt",
    "d": "fdjffdyetyerheg", "e": "gfddhggfdgfdg", "f": "hgfjhergggrg",
    "g": "gfdgtfdfjhgfhytr", "h": "jfhytyjhgytr", "i": "jhgtrtghjytgrtgyhj",
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
    "a": {"домоверсией": "демоверсией"},
    "c": {"главе": "голове"},
    "d": {"ис": "из"},
    "f": {"тренажери": "тренажере", "текстовыя": "текстовый"},
    "g": {"которыю": "которые"},
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
    words = json.load(open(f"../asr_coffee123_29/{src}_words.json"))
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
# Episode A (gray-shirt boy, 18.775s): a variant from a tutor without
# checking can hide a long-outdated wording; the app's FIPI bank updates
# under the current year
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВАРИАНТ ОТ РЕПЕТИТОРА", "БЕЗ ПРОВЕРКИ?"], "end": 1.71}
a_cards = [
    {"start": 1.71, "end": 3.03, "lines": [{"text": "МОЖНО ОТ", "accent": False, "size": "small"}, {"text": "РЕПЕТИТОРА", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 3.93, "lines": [{"text": "БЕЗ И", "accent": False, "size": "small"}, {"text": "ПРОВЕРКИ", "accent": True, "size": "big"}]},
    {"start": 3.93, "end": 4.89, "lines": [{"text": "НЕ В НЕМ", "accent": False, "size": "small"}, {"text": "ЗАМЕТИТЬ", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 5.85, "lines": [{"text": "ДАВНО", "accent": False, "size": "small"}, {"text": "УСТАРЕВШУЮ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 6.69, "lines": [{"text": "ФОРМУЛИРОВКУ", "accent": True, "size": "small"}]},
    {"start": 6.69, "end": 7.89, "lines": [{"text": "Я ТАКОЙ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 7.89, "end": 8.76, "lines": [{"text": "НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "НЕДЕЛЬ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.87, "lines": [{"text": "ПОКА САМ НЕ", "accent": False, "size": "small"}, {"text": "СРАВНИЛ", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 10.80, "lines": [{"text": "ЕГО С", "accent": False, "size": "small"}, {"text": "ОФИЦИАЛЬНОЙ", "accent": True, "size": "small"}]},
    {"start": 10.80, "end": 12.27, "lines": [{"text": "НА САЙТЕ", "accent": False, "size": "small"}, {"text": "ДЕМОВЕРСИЕЙ", "accent": True, "size": "small"}]},
    {"start": 12.27, "end": 13.23, "lines": [{"text": "В ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.28, "lines": [{"text": "ФИПИ", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 14.28, "end": 15.27, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 15.27, "end": 16.50, "lines": [{"text": "ОБНОВЛЯЮТСЯ ПОД", "accent": False, "size": "small"}, {"text": "ТЕКУЩИЙ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.31, "lines": [{"text": "ГОД", "accent": True, "size": "big"}]},
    {"start": 17.31, "end": 18.775, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 1.71, "end": 2.04}, {"start": 12.27, "end": 12.60}, {"start": 17.31, "end": 17.64}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (gray-shirt boy, 19.266s): a term in obshestvoznanie confused
# right during a final test at school despite answering flawlessly at
# home the night before; the app's memorization games train telling
# similar terms apart
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПУТАЕШЬ ТЕРМИНЫ", "ПО ОБЩЕСТВОЗНАНИЮ?"], "end": 1.89}
b_cards = [
    {"start": 1.89, "end": 2.70, "lines": [{"text": "МОЖНО С", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАТЬ", "accent": True, "size": "big"}]},
    {"start": 2.70, "end": 3.63, "lines": [{"text": "ПОХОЖИМ", "accent": False, "size": "small"}, {"text": "ПРЯМО", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.44, "lines": [{"text": "ВО ИТОГОВОЙ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 4.44, "end": 5.40, "lines": [{"text": "ПЕРЕД", "accent": False, "size": "small"}, {"text": "КОНТРОЛЬНОЙ", "accent": True, "size": "small"}]},
    {"start": 5.40, "end": 6.21, "lines": [{"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 6.21, "end": 7.05, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАЛ", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 8.37, "lines": [{"text": "ДВА НА", "accent": False, "size": "small"}, {"text": "КОНТРОЛЬНЫЙ", "accent": True, "size": "small"}]},
    {"start": 8.37, "end": 9.30, "lines": [{"text": "ХОТЯ", "accent": False, "size": "small"}, {"text": "НАКАНУНЕ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.11, "lines": [{"text": "НА НИХ", "accent": False, "size": "small"}, {"text": "ОТВЕЧАЛ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.13, "lines": [{"text": "БЕЗ ЕДИНОЙ", "accent": False, "size": "small"}, {"text": "ДОМА", "accent": True, "size": "big"}]},
    {"start": 11.13, "end": 12.12, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 13.62, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 14.97, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.97, "end": 16.44, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 17.49, "lines": [{"text": "ПОХОЖИХ", "accent": False, "size": "small"}, {"text": "ТЕРМИНОВ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 19.266, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 11.13, "end": 11.46}, {"start": 17.49, "end": 17.82}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (gray-shirt boy, 17.218s): doing a calculation in your head
# faster than you can put it into words; the app's text breakdown breaks
# the calculation into understandable steps
# ---------------------------------------------------------------------------
c_intro = {"lines": ["СЧИТАЕШЬ БЫСТРО", "НО НЕ МОЖЕШЬ ОБЪЯСНИТЬ?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 2.97, "lines": [{"text": "ЕГЭ ПРОИСХОДИТ", "accent": False, "size": "small"}, {"text": "ИНОГДА", "accent": True, "size": "big"}]},
    {"start": 2.97, "end": 4.17, "lines": [{"text": "ЧЕМ ПОЛУЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "БЫСТРЕЕ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 5.01, "lines": [{"text": "ЕГО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 5.01, "end": 5.82, "lines": [{"text": "Я ТАК", "accent": False, "size": "small"}, {"text": "СЛОВАМИ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 6.99, "lines": [{"text": "СЧИТАЛ В УМЕ", "accent": False, "size": "small"}, {"text": "БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 6.99, "end": 8.07, "lines": [{"text": "А ХОД МЫСЛИ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНИТЬ", "accent": True, "size": "big"}]},
    {"start": 8.07, "end": 9.33, "lines": [{"text": "ПОЛУЧАЛОСЬ", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИКАМ", "accent": True, "size": "small"}]},
    {"start": 9.33, "end": 10.32, "lines": [{"text": "С БОЛЬШИМ", "accent": False, "size": "small"}, {"text": "ТРУДОМ", "accent": True, "size": "big"}]},
    {"start": 10.32, "end": 11.22, "lines": [{"text": "В К", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.39, "lines": [{"text": "ЕСТЬ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 12.39, "end": 13.68, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "РАСКЛАДЫВАЕТ", "accent": True, "size": "small"}]},
    {"start": 13.68, "end": 14.55, "lines": [{"text": "В ГОЛОВЕ НА", "accent": False, "size": "small"}, {"text": "СЧЕТ", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 15.42, "lines": [{"text": "ПОНЯТНЫЕ", "accent": False, "size": "small"}, {"text": "ШАГИ", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 17.218, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.86, "end": 2.19}, {"start": 10.32, "end": 10.65}, {"start": 15.42, "end": 15.75}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (curly-hair boy, 18.480s): reposting an EGE task from someone
# else's social media profile can mean not noticing it's outdated; the
# app's FIPI bank has this year's tasks, no random reposts
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ЗАДАНИЕ ИЗ ЧУЖОГО", "ПРОФИЛЯ В СОЦСЕТЯХ?"], "end": 1.68}
d_cards = [
    {"start": 1.68, "end": 2.49, "lines": [{"text": "ИЗ ПРОФИЛЯ", "accent": False, "size": "small"}, {"text": "ЧУЖОГО", "accent": True, "size": "big"}]},
    {"start": 2.49, "end": 3.42, "lines": [{"text": "В МОЖНО", "accent": False, "size": "small"}, {"text": "СОЦСЕТЯХ", "accent": True, "size": "big"}]},
    {"start": 3.42, "end": 4.32, "lines": [{"text": "СЕБЕ", "accent": False, "size": "small"}, {"text": "РЕПОСТНУТЬ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 5.16, "lines": [{"text": "И НЕ ЧТО", "accent": False, "size": "small"}, {"text": "ЗАМЕТИТЬ", "accent": True, "size": "big"}]},
    {"start": 5.16, "end": 6.12, "lines": [{"text": "ОНИ", "accent": False, "size": "small"}, {"text": "УСТАРЕЛИ", "accent": True, "size": "big"}]},
    {"start": 6.12, "end": 7.02, "lines": [{"text": "Я ТАКИЕ", "accent": False, "size": "small"}, {"text": "СОХРАНЯЛ", "accent": True, "size": "big"}]},
    {"start": 7.02, "end": 8.13, "lines": [{"text": "ПОСТЫ ВЕСЬ", "accent": False, "size": "small"}, {"text": "АВГУСТ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.42, "lines": [{"text": "ПОКА СРЕДИ НИХ НЕ", "accent": False, "size": "small"}, {"text": "ВСТРЕТИЛ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 10.41, "lines": [{"text": "ИЗ ДАВНО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 10.41, "end": 11.61, "lines": [{"text": "ГОДА", "accent": False, "size": "small"}, {"text": "ПРОШЕДШЕГО", "accent": True, "size": "big"}]},
    {"start": 11.61, "end": 12.57, "lines": [{"text": "В ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.57, "end": 13.59, "lines": [{"text": "ФИПИ", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 14.79, "lines": [{"text": "С ТЕКУЩЕГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 16.05, "lines": [{"text": "ГОДА БЕЗ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНЫХ", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 17.01, "lines": [{"text": "РЕПОСТОВ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 18.480, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.68, "end": 2.01}, {"start": 11.61, "end": 11.94}, {"start": 17.01, "end": 17.34}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (curly-hair boy, 20.098s): knowing a concept in general terms
# can fall apart in front of a precise test question; the app's
# memorization games train exact, not just general, understanding
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЗНАЕШЬ ПОНЯТИЕ", "В ОБЩИХ ЧЕРТАХ?"], "end": 2.13}
e_cards = [
    {"start": 2.13, "end": 3.00, "lines": [{"text": "ЕГЭ ЗНАТЬ", "accent": False, "size": "small"}, {"text": "МОЖНО", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 3.90, "lines": [{"text": "В ОБЩИХ", "accent": False, "size": "small"}, {"text": "ЧЕРТАХ", "accent": True, "size": "big"}]},
    {"start": 3.90, "end": 4.86, "lines": [{"text": "И ПЕРЕД", "accent": False, "size": "small"}, {"text": "РАСТЕРЯТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 4.86, "end": 5.67, "lines": [{"text": "ТОЧНЫМ", "accent": False, "size": "small"}, {"text": "ВОПРОСОМ", "accent": True, "size": "big"}]},
    {"start": 5.67, "end": 6.93, "lines": [{"text": "Я ОБЪЯСНЯЛ", "accent": False, "size": "small"}, {"text": "ТЕСТА", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.04, "lines": [{"text": "В ОБЩИХ ЧЕРТАХ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЕ", "accent": True, "size": "big"}]},
    {"start": 8.04, "end": 8.85, "lines": [{"text": "А НА", "accent": False, "size": "small"}, {"text": "УВЕРЕННО", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 9.78, "lines": [{"text": "ТОЧНЫЙ", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 10.83, "lines": [{"text": "ВОПРОС ТЕСТА", "accent": False, "size": "small"}, {"text": "ЗАСТАЛ", "accent": True, "size": "big"}]},
    {"start": 10.83, "end": 11.79, "lines": [{"text": "МЕНЯ", "accent": False, "size": "small"}, {"text": "ВРАСПЛОХ", "accent": True, "size": "big"}]},
    {"start": 11.79, "end": 12.66, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 13.53, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 13.53, "end": 14.79, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 15.81, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 15.81, "end": 16.62, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ТОЧНОЕ", "accent": True, "size": "big"}]},
    {"start": 16.62, "end": 17.58, "lines": [{"text": "ОБЩЕЕ", "accent": False, "size": "small"}, {"text": "ПОНИМАНИЕ", "accent": True, "size": "big"}]},
    {"start": 17.58, "end": 18.63, "lines": [{"text": "ПОНЯТИЙ", "accent": True, "size": "big"}]},
    {"start": 18.63, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.13, "end": 2.46}, {"start": 11.79, "end": 12.12}, {"start": 18.63, "end": 18.96}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-hair boy, 18.840s): a value table in an EGE task can be
# used without understanding the principle behind it; the app's text
# breakdown explains the principle, not just a ready-made table
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ТАБЛИЦА ЗНАЧЕНИЙ", "БЕЗ ПОНИМАНИЯ?"], "end": 1.56}
f_cards = [
    {"start": 1.56, "end": 2.37, "lines": [{"text": "В ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.37, "end": 3.42, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ИСПОЛЬЗУЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 3.42, "end": 4.56, "lines": [{"text": "БЕЗ ПРИНЦИПА", "accent": False, "size": "small"}, {"text": "ПОНИМАНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 5.76, "lines": [{"text": "КОТОРЫЙ ЗА НЕЙ", "accent": False, "size": "small"}, {"text": "СТОИТ", "accent": True, "size": "big"}]},
    {"start": 5.76, "end": 6.81, "lines": [{"text": "Я ГОТОВОЙ", "accent": False, "size": "small"}, {"text": "ПОЛЬЗОВАЛСЯ", "accent": True, "size": "small"}]},
    {"start": 6.81, "end": 7.92, "lines": [{"text": "МЕСЯЦАМИ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦЕЙ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 8.85, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "ПОПРОБОВАЛ", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 9.99, "lines": [{"text": "ЕЕ ЗНАЧЕНИЕ", "accent": False, "size": "small"}, {"text": "ВЫВЕСТИ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 10.86, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "САМОСТОЯТЕЛЬНО", "accent": True, "size": "small"}]},
    {"start": 10.86, "end": 11.94, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ЧЕРНОВИКЕ", "accent": True, "size": "big"}]},
    {"start": 11.94, "end": 12.99, "lines": [{"text": "К ЗАДАНИЕМ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.10, "lines": [{"text": "ЕСТЬ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.10, "end": 14.97, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 14.97, "end": 15.90, "lines": [{"text": "А НЕ ДАЕТ", "accent": False, "size": "small"}, {"text": "ПРИНЦИП", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 16.92, "lines": [{"text": "ГОТОВУЮ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦУ", "accent": True, "size": "big"}]},
    {"start": 16.92, "end": 18.840, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.56, "end": 1.89}, {"start": 11.94, "end": 12.27}, {"start": 16.92, "end": 17.25}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (mother, 20.460s): a daughter can know history dates cold and
# swap them on the mock exam anyway; the app's memorization games train
# the order of dates, not just the list
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ДОЧЬ ЗНАЕТ ДАТЫ", "НА ЗУБОК?"], "end": 1.83}
g_cards = [
    {"start": 1.83, "end": 2.67, "lines": [{"text": "ДОЧЬ МОЖЕТ", "accent": False, "size": "small"}, {"text": "ЗНАТЬ", "accent": True, "size": "big"}]},
    {"start": 2.67, "end": 3.84, "lines": [{"text": "НА ЗУБОК И", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 4.74, "lines": [{"text": "ИХ ПРЯМО", "accent": False, "size": "small"}, {"text": "МЕСТАМИ", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 6.27, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 6.27, "end": 7.14, "lines": [{"text": "Я КАК ОНА", "accent": False, "size": "small"}, {"text": "СЛУШАЛА", "accent": True, "size": "big"}]},
    {"start": 7.14, "end": 8.34, "lines": [{"text": "ПЕРЕЧИСЛЯЕТ", "accent": False, "size": "small"}, {"text": "БЕЗОШИБОЧНО", "accent": True, "size": "small"}]},
    {"start": 8.34, "end": 9.48, "lines": [{"text": "ПО ПОРЯДКУ", "accent": False, "size": "small"}, {"text": "ДАТЫ", "accent": True, "size": "big"}]},
    {"start": 9.48, "end": 10.56, "lines": [{"text": "А НА ПОРЯДОК", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 10.56, "end": 12.03, "lines": [{"text": "СБИЛСЯ", "accent": False, "size": "small"}, {"text": "ВДРУГ", "accent": True, "size": "big"}]},
    {"start": 12.03, "end": 12.84, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.84, "end": 13.65, "lines": [{"text": "ПО ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.82, "lines": [{"text": "НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 15.84, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТ", "accent": True, "size": "big"}]},
    {"start": 15.84, "end": 16.66, "lines": [{"text": "ИМЕННО ДАТ", "accent": False, "size": "small"}, {"text": "ПОРЯДОК", "accent": True, "size": "big"}]},
    {"start": 16.66, "end": 18.69, "lines": [{"text": "А НЕ ТОЛЬКО ИХ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 18.69, "end": 20.460, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 1.83, "end": 2.16}, {"start": 12.03, "end": 12.36}, {"start": 18.69, "end": 19.02}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (mother, 18.400s): a pre-made course with ready tasks doesn't
# always update alongside the real exam format; the app's FIPI bank is
# updated to this year's actual format
# ---------------------------------------------------------------------------
h_intro = {"lines": ["КУРС ПОДГОТОВКИ", "С ГОТОВЫМИ ЗАДАНИЯМИ?"], "end": 1.71}
h_cards = [
    {"start": 1.71, "end": 2.67, "lines": [{"text": "ГОТОВЫМИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМИ", "accent": True, "size": "big"}]},
    {"start": 2.67, "end": 3.66, "lines": [{"text": "НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ОБНОВЛЯЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 3.66, "end": 4.86, "lines": [{"text": "С РЕАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 4.86, "end": 5.91, "lines": [{"text": "ЭКЗАМЕНА", "accent": True, "size": "big"}]},
    {"start": 5.91, "end": 6.90, "lines": [{"text": "Я ТАКОЙ ОПЛАТИЛА", "accent": False, "size": "small"}, {"text": "КУРС", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 8.13, "lines": [{"text": "ДОЧЕРИ В НАЧАЛЕ", "accent": False, "size": "small"}, {"text": "ГОДА", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.06, "lines": [{"text": "И ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ОСЕНЬЮ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 9.90, "lines": [{"text": "ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.77, "lines": [{"text": "О КОТОРЫХ", "accent": False, "size": "small"}, {"text": "ДАВНО", "accent": True, "size": "big"}]},
    {"start": 10.77, "end": 12.18, "lines": [{"text": "НЕТ В ДЕМО", "accent": False, "size": "small"}, {"text": "ВЕРСИИ", "accent": True, "size": "big"}]},
    {"start": 12.18, "end": 13.02, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.02, "end": 14.22, "lines": [{"text": "СОБРАН", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.22, "end": 15.48, "lines": [{"text": "ОБНОВЛЕННЫЙ ПОД", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 15.48, "end": 16.68, "lines": [{"text": "НА ЭТОТ ГОД", "accent": False, "size": "small"}, {"text": "ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 16.68, "end": 18.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 1.71, "end": 2.04}, {"start": 12.18, "end": 12.51}, {"start": 16.68, "end": 17.01}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (mother, 20.098s): a daughter can fix her own mistake in an
# EGE task and still not be able to explain what was wrong; the app's
# text breakdown explains the actual substance of the mistake, not just
# the fix
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ДОЧЬ ИСПРАВИЛА ОШИБКУ", "НО НЕ СМОГЛА ОБЪЯСНИТЬ?"], "end": 1.71}
i_cards = [
    {"start": 1.71, "end": 2.58, "lines": [{"text": "СВОЮ ЖЕ", "accent": False, "size": "small"}, {"text": "ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 2.58, "end": 3.54, "lines": [{"text": "В ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.62, "lines": [{"text": "И НЕ ОБЪЯСНИТЬ", "accent": False, "size": "small"}, {"text": "СУМЕТЬ", "accent": True, "size": "big"}]},
    {"start": 4.62, "end": 6.03, "lines": [{"text": "ЧТО БЫЛО НЕ", "accent": False, "size": "small"}, {"text": "ТАК", "accent": True, "size": "big"}]},
    {"start": 6.03, "end": 6.87, "lines": [{"text": "Я ЕЕ", "accent": False, "size": "small"}, {"text": "ПРОСИЛА", "accent": True, "size": "big"}]},
    {"start": 6.87, "end": 7.68, "lines": [{"text": "ГДЕ", "accent": False, "size": "small"}, {"text": "ПРОГОВОРИТЬ", "accent": True, "size": "small"}]},
    {"start": 7.68, "end": 9.15, "lines": [{"text": "ИМЕННО БЫЛА", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 9.15, "end": 10.29, "lines": [{"text": "И ОБЫЧНО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 10.29, "end": 12.12, "lines": [{"text": "НА СЕРЕДИНЕ", "accent": False, "size": "small"}, {"text": "ОБРЫВАЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 12.99, "lines": [{"text": "В К", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 13.80, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯМ", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 14.79, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 15.72, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 15.72, "end": 16.80, "lines": [{"text": "САМУ СУТЬ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.30, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ИСПРАВЛЕНИЕ", "accent": True, "size": "small"}]},
    {"start": 18.30, "end": 20.098, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 1.71, "end": 2.04}, {"start": 12.12, "end": 12.45}, {"start": 18.30, "end": 18.63}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
