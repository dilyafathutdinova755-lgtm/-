#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTY-THIRD 'coffee123'
batch (9 episodes uploaded under the same tag after twenty-two prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes69/.

Three returning hosts, no new faces: the wavy-haired living-room boy
(a, b, g), the curly-haired boy (c, e, f), and the brunette study-room
host (d, h, i). Sub-themes: a detailed text breakdown that reveals the
real solution method behind a lucky/random correct answer instead of
just the right answer (a, e, i), an up-to-date FIPI bank sourced from
an official/real exam origin instead of variants of unknown/random
origin (b, f, h), memorization games that actually consolidate/test
material instead of one read-through or passive repetition (c, d, g).
"""
import json

REAL_DURATION = {
    "a": 16.108, "b": 17.068, "c": 16.556,
    "d": 20.823, "e": 16.471, "f": 17.026,
    "g": 17.440, "h": 21.960, "i": 18.690,
}
SOURCE_FILE = {
    "a": "bkldfbrandjghfcf", "b": "bvhtdhjbhcgfxbrs", "c": "dghgnmfdhjutyudbjx",
    "d": "gfggfhgdhgdfh.bfgh", "e": "gfjxkjfkjfxkjxr", "f": "jfdjnjdytrjbdtryt",
    "g": "kfdyjstbghjckgcxfd", "h": "nfcjjm.gfxj", "i": "vbnvchvjffjnfjfxc",
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
    if letter == "f":
        for w in words:
            if abs(w["start"] - 14.13) < 0.02 and w["text"] == "о":
                w["text"] = "на"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_23/{src}_words.json"))
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
# Episode A (wavy-haired living-room boy, 16.108s): a correct answer that
# comes almost by chance, without understanding the solution process,
# rarely repeats on a similar task; the app's breakdown shows the real
# solution method
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПОЛУЧАЕШЬ ОТВЕТ", "НО НЕ ПОНИМАЕШЬ КАК?"], "end": 1.77}
a_cards = [
    {"start": 1.92, "end": 3.60, "lines": [{"text": "ИНОГДА ПОЛУЧАЕТСЯ ПОЧТИ", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНО", "accent": True, "size": "big"}]},
    {"start": 3.90, "end": 5.28, "lines": [{"text": "БЕЗ ПОНИМАНИЯ ХОДА", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 5.52, "end": 6.31, "lines": [{"text": "НА ПОХОЖЕМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИИ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 8.34, "lines": [{"text": "СЛУЧАЙНОСТЬ ОБЫЧНО НЕ ПОВТОРЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ТАКАЯ", "accent": True, "size": "big"}]},
    {"start": 8.67, "end": 9.81, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 11.76, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВАЯ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.94, "end": 12.73, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 12.84, "end": 13.98, "lines": [{"text": "РЕАЛЬНЫЙ СПОСОБ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 14.25, "end": 16.108, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 1.92, "end": 2.25}, {"start": 8.67, "end": 9.00}, {"start": 14.25, "end": 14.58}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (wavy-haired living-room boy, 17.068s): a downloaded variant of
# unknown origin can look convincing and still not match the real exam
# format, and that's nearly impossible to catch by eye; the app's bank is
# the actual FIPI bank that matches the real exam
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СКАЧИВАЕШЬ ВАРИАНТЫ", "НЕИЗВЕСТНОГО ПРОИСХОЖДЕНИЯ?"], "end": 1.59}
b_cards = [
    {"start": 1.71, "end": 4.29, "lines": [{"text": "НЕИЗВЕСТНОГО ПРОИСХОЖДЕНИЯ ВЫГЛЯДЕТЬ УБЕДИТЕЛЬНО", "accent": False, "size": "small"}, {"text": "МОЖЕТ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.73, "lines": [{"text": "И ВСЕ РАВНО НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 6.61, "lines": [{"text": "С РЕАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ФОРМАТОМ", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 8.16, "lines": [{"text": "ЭКЗАМЕНА ПРОВЕРИТЬ ЭТО НА", "accent": False, "size": "small"}, {"text": "ГЛАЗ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.54, "lines": [{"text": "ОБЫЧНО НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 10.02, "end": 11.73, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 11.85, "end": 13.17, "lines": [{"text": "БАНК ФИПИ КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ТОЧНО", "accent": True, "size": "big"}]},
    {"start": 13.32, "end": 14.97, "lines": [{"text": "СООТВЕТСТВУЕТ НАСТОЯЩЕМУ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНУ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 17.068, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.71, "end": 2.04}, {"start": 10.02, "end": 10.35}, {"start": 15.21, "end": 15.54}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (curly-haired boy, 16.556s): reading a social-studies term once
# and deciding it's learned rarely survives a check a week later; the app
# has memorization games for that kind of honest check
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЧИТАЕШЬ ТЕРМИН ОДИН РАЗ", "И СЧИТАЕШЬ ЧТО ВЫУЧИЛ?"], "end": 2.10}
c_cards = [
    {"start": 2.34, "end": 3.66, "lines": [{"text": "МОЖНО ОДИН РАЗ", "accent": False, "size": "small"}, {"text": "ПРОЧИТАТЬ", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 5.19, "lines": [{"text": "И РЕШИТЬ ЧТО ОН УЖЕ", "accent": False, "size": "small"}, {"text": "ВЫУЧЕН", "accent": True, "size": "big"}]},
    {"start": 5.43, "end": 6.54, "lines": [{"text": "ПРОВЕРКА ВСЛУХ ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 8.01, "lines": [{"text": "ЧАСТО ГОВОРИТ ОБ", "accent": False, "size": "small"}, {"text": "ОБРАТНОМ", "accent": True, "size": "big"}]},
    {"start": 8.37, "end": 9.54, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 11.46, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 12.81, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.31, "lines": [{"text": "ДЛЯ ТАКОЙ ЧЕСТНОЙ", "accent": False, "size": "small"}, {"text": "ПРОВЕРКИ", "accent": True, "size": "big"}]},
    {"start": 14.58, "end": 16.556, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.34, "end": 2.67}, {"start": 8.37, "end": 8.70}, {"start": 14.58, "end": 14.91}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (brunette study-room host, 20.823s): explaining an essay topic
# to yourself and failing to retell it aloud a day later means it was
# understood but not consolidated; the app's memorization games consolidate
# material instead of just explaining it
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ОБЪЯСНЯЕШЬ ТЕМУ СЕБЕ", "НО НЕ МОЖЕШЬ ПЕРЕСКАЗАТЬ?"], "end": 1.92}
d_cards = [
    {"start": 2.19, "end": 3.39, "lines": [{"text": "МОЖНО ОБЪЯСНИТЬ САМОЙ", "accent": False, "size": "small"}, {"text": "СЕБЕ", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 6.03, "lines": [{"text": "И ЧЕРЕЗ ДЕНЬ НЕ СУМЕТЬ ПЕРЕСКАЗАТЬ ЕЕ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 8.46, "lines": [{"text": "ЗНАЧИТ ТЕМА БЫЛА", "accent": False, "size": "small"}, {"text": "ПОНЯТА", "accent": True, "size": "big"}]},
    {"start": 8.88, "end": 9.70, "lines": [{"text": "НО НЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЕНА", "accent": True, "size": "big"}]},
    {"start": 10.44, "end": 11.67, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 11.79, "end": 13.59, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 14.13, "end": 15.30, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.48, "end": 16.29, "lines": [{"text": "КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ЗАКРЕПЛЯЮТ", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 17.91, "lines": [{"text": "МАТЕРИАЛ А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЮТ", "accent": True, "size": "big"}]},
    {"start": 18.96, "end": 20.823, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.19, "end": 2.52}, {"start": 10.44, "end": 10.77}, {"start": 18.96, "end": 19.29}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (curly-haired boy, 16.471s): making the same mistake twice in a
# row at the same spot and blaming bad luck both times usually hides one
# misunderstood moment in the solution; the app's breakdown finds that
# exact moment
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ДВАЖДЫ ОШИБАЕШЬСЯ", "В ОДНОМ И ТОМ ЖЕ МЕСТЕ?"], "end": 1.68}
e_cards = [
    {"start": 1.83, "end": 3.57, "lines": [{"text": "ПОДРЯД ОШИБИТЬСЯ В ОДНОМ И ТОМ ЖЕ", "accent": False, "size": "small"}, {"text": "МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 4.98, "lines": [{"text": "И ОБА РАЗА", "accent": False, "size": "small"}, {"text": "СПИСАТЬ", "accent": True, "size": "big"}]},
    {"start": 5.10, "end": 5.89, "lines": [{"text": "ЭТО НА", "accent": False, "size": "small"}, {"text": "НЕВЕЗЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.27, "end": 7.20, "lines": [{"text": "ОБЫЧНО ЗА ЭТИМ", "accent": False, "size": "small"}, {"text": "СТОИТ", "accent": True, "size": "big"}]},
    {"start": 7.53, "end": 9.42, "lines": [{"text": "ОДИН И ТОТ ЖЕ НЕПОНЯТНЫЙ МОМЕНТ В", "accent": False, "size": "small"}, {"text": "РЕШЕНИИ", "accent": True, "size": "big"}]},
    {"start": 9.81, "end": 11.01, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 11.13, "end": 13.05, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.49, "lines": [{"text": "КОТОРЫЙ НАХОДИТ ЭТОТ", "accent": False, "size": "small"}, {"text": "МОМЕНТ", "accent": True, "size": "big"}]},
    {"start": 14.79, "end": 16.471, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.83, "end": 2.16}, {"start": 9.81, "end": 10.14}, {"start": 14.79, "end": 15.12}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-haired boy, 17.026s): random online variant collections
# risk encountering formulations that won't be on the real exam, and
# checking every file's source yourself is nearly impossible; the app's
# bank is the actual FIPI bank, same format as the real exam
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РЕШАЕШЬ СЛУЧАЙНЫЕ", "ПОДБОРКИ ИЗ ИНТЕРНЕТА?"], "end": 1.56}
f_cards = [
    {"start": 1.80, "end": 3.21, "lines": [{"text": "И СЛУЧАЙНЫЕ ПОДБОРКИ В", "accent": False, "size": "small"}, {"text": "ИНТЕРНЕТЕ", "accent": True, "size": "big"}]},
    {"start": 3.57, "end": 4.36, "lines": [{"text": "РИСК", "accent": False, "size": "small"}, {"text": "НАТКНУТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 4.36, "end": 6.75, "lines": [{"text": "ФОРМУЛИРОВКИ КОТОРЫХ НЕ БУДЕТ НА НАСТОЯЩЕМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.46, "lines": [{"text": "ПРОВЕРИТЬ ИСТОЧНИК КАЖДОГО", "accent": False, "size": "small"}, {"text": "ФАЙЛА", "accent": True, "size": "big"}]},
    {"start": 8.61, "end": 10.20, "lines": [{"text": "САМОСТОЯТЕЛЬНО ПОЧТИ", "accent": False, "size": "small"}, {"text": "НЕРЕАЛЬНО", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 12.09, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 12.21, "end": 13.44, "lines": [{"text": "БАНК ФИПИ ТОТ ЖЕ", "accent": False, "size": "small"}, {"text": "ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 14.91, "lines": [{"text": "ЧТО БУДЕТ НА НАСТОЯЩЕМ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 17.026, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.80, "end": 2.13}, {"start": 10.53, "end": 10.86}, {"start": 15.12, "end": 15.45}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (wavy-haired living-room boy, 17.440s): a list of terms repeated
# on the way to school still gets mixed up; simple repetition aloud barely
# helps without extra training; the app's memorization games give a
# longer-lasting effect
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ПОВТОРЯЕШЬ ТЕРМИНЫ", "И ВСЕ РАВНО ПУТАЕШЬСЯ?"], "end": 1.59}
g_cards = [
    {"start": 1.71, "end": 3.12, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ МОЖНО", "accent": False, "size": "small"}, {"text": "ПОВТОРИТЬ", "accent": True, "size": "big"}]},
    {"start": 3.27, "end": 4.56, "lines": [{"text": "ПО ДОРОГЕ В ШКОЛУ И ВСЕ", "accent": False, "size": "small"}, {"text": "РАВНО", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 5.73, "lines": [{"text": "ЗАПУТАТЬСЯ В НИХ НА", "accent": False, "size": "small"}, {"text": "ПАРЕ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.08, "lines": [{"text": "ПРОСТОЕ ПОВТОРЕНИЕ", "accent": False, "size": "small"}, {"text": "ВСЛУХ", "accent": True, "size": "big"}]},
    {"start": 7.20, "end": 8.01, "lines": [{"text": "ПОЧТИ НЕ", "accent": False, "size": "small"}, {"text": "ПОМОГАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.16, "end": 9.36, "lines": [{"text": "БЕЗ ДОПОЛНИТЕЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ТРЕНИРОВКИ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 10.86, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 11.01, "end": 12.60, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 13.98, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.13, "end": 15.39, "lines": [{"text": "ДЛЯ БОЛЕЕ ДОЛГОГО", "accent": False, "size": "small"}, {"text": "ЭФФЕКТА", "accent": True, "size": "big"}]},
    {"start": 15.69, "end": 17.440, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 1.71, "end": 2.04}, {"start": 9.69, "end": 10.02}, {"start": 15.69, "end": 16.02}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (brunette study-room host, 21.960s): hitting an unfamiliar task
# formulation despite having solved hundreds of variants usually means
# those variants weren't from an official source; the app's actual FIPI
# bank carries tasks exactly as they'll appear on the exam
# ---------------------------------------------------------------------------
h_intro = {"lines": ["РЕШАЕШЬ СОТНИ ВАРИАНТОВ", "И ВСТРЕЧАЕШЬ НЕЗНАКОМУЮ?"], "end": 1.71}
h_cards = [
    {"start": 1.83, "end": 2.91, "lines": [{"text": "НА ФОРМУЛИРОВКУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 3.09, "end": 4.11, "lines": [{"text": "КОТОРУЮ ВИДИШЬ", "accent": False, "size": "small"}, {"text": "ВПЕРВЫЕ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 6.42, "lines": [{"text": "ХОТЯ РЕШИЛА УЖЕ СОТНИ", "accent": False, "size": "small"}, {"text": "ВАРИАНТОВ", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 8.25, "lines": [{"text": "ОБЫЧНО ЭТО", "accent": False, "size": "small"}, {"text": "ЗНАЧИТ", "accent": True, "size": "big"}]},
    {"start": 8.40, "end": 9.36, "lines": [{"text": "ЧТО САМИ", "accent": False, "size": "small"}, {"text": "ВАРИАНТЫ", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 12.03, "lines": [{"text": "БЫЛИ СОБРАНЫ НЕ ИЗ ОФИЦИАЛЬНОГО", "accent": False, "size": "small"}, {"text": "ИСТОЧНИКА", "accent": True, "size": "big"}]},
    {"start": 12.96, "end": 14.85, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 14.97, "end": 15.78, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.11, "end": 19.29, "lines": [{"text": "ЗАДАНИЕ В ТОМ ВИДЕ В КАКОМ ОНИ РЕАЛЬНО БУДУТ НА", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНЕ", "accent": True, "size": "big"}]},
    {"start": 20.01, "end": 21.960, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 1.83, "end": 2.16}, {"start": 12.96, "end": 13.29}, {"start": 20.01, "end": 20.34}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (brunette study-room host, 18.690s): solving a task correctly
# and forgetting the method a month later without a breakdown means the
# solution stays a lucky guess, not a skill; the app's breakdown fixes the
# actual solution method
# ---------------------------------------------------------------------------
i_intro = {"lines": ["РЕШАЕШЬ ЗАДАНИЕ ПРАВИЛЬНО", "И ЗАБЫВАЕШЬ КАК ЧЕРЕЗ МЕСЯЦ?"], "end": 1.89}
i_cards = [
    {"start": 2.01, "end": 3.09, "lines": [{"text": "ПРАВИЛЬНОЕ И ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 3.27, "end": 4.32, "lines": [{"text": "ЗАБЫТЬ КАКИМ", "accent": False, "size": "small"}, {"text": "СПОСОБОМ", "accent": True, "size": "big"}]},
    {"start": 4.47, "end": 5.61, "lines": [{"text": "ТЫ ВООБЩЕ К ЭТОМУ", "accent": False, "size": "small"}, {"text": "ПРИШЛА", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 7.53, "lines": [{"text": "БЕЗ РАЗБОРА", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.79, "lines": [{"text": "ОСТАЕТСЯ СЛУЧАЙНОЙ", "accent": False, "size": "small"}, {"text": "УДАЧЕЙ", "accent": True, "size": "big"}]},
    {"start": 8.97, "end": 9.78, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "НАВЫКОМ", "accent": True, "size": "big"}]},
    {"start": 10.41, "end": 11.73, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 13.92, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.22, "end": 15.03, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ФИКСИРУЕТ", "accent": True, "size": "big"}]},
    {"start": 15.27, "end": 16.26, "lines": [{"text": "САМ СПОСОБ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 18.690, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.01, "end": 2.34}, {"start": 10.41, "end": 10.74}, {"start": 16.89, "end": 17.22}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
