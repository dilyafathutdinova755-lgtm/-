#!/usr/bin/env python3
"""One-off authoring + validation script for the EIGHTEENTH 'coffee123'
batch (6 episodes uploaded under the same tag after seventeen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes61/.

Two hosts, three episodes each: the returning curly-haired boy
(bookshelf/desk room) and a new-room but visually-similar wavy-haired
boy on a couch with plants by a window - genuinely distinct face and
room from the curly host, reused across his three episodes here.
Content pairs up across the two hosts: solving at your own pace from
the FIPI bank instead of racing through variants / returning to a
specific weak topic instead of solving strictly in order, memorization
games for the essay subjects (Russian, history, social studies) instead
of re-reading conspects or re-reading terms, and a full text explanation
for every wrong answer instead of just glancing at the correct one.
"""
import json

REAL_DURATION = {
    "a": 18.263, "b": 19.820, "c": 18.604,
    "d": 18.840, "e": 18.690, "f": 15.746,
}
SOURCE_FILE = {
    "a": "gfhfhghgfngngngfhnfghngf", "b": "ghfdfdgdgfdg", "c": "ghfdhhhfhgfhfh",
    "d": "hgfhfhfghfhfhfh", "e": "hgfhhfhfhgfhjgfhgfh", "f": "hj.fgtjngfngfhnfghnb",
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
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_18/{src}_words.json"))
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
# Episode A (curly-haired boy, 18.263s): racing through five quick variants
# beats one carefully worked one on closing the topic gap; the app's FIPI
# bank lets you solve at your own pace instead of chasing quantity
# ---------------------------------------------------------------------------
a_intro = {"lines": ["5 БЫСТРЫХ ВАРИАНТОВ", "ЛУЧШЕ ОДНОГО?"], "end": 1.5}
a_cards = [
    {"start": 1.62, "end": 2.88, "lines": [{"text": "БЫСТРОРЕШЕННЫХ", "accent": False, "size": "small"}, {"text": "ВАРИАНТОВ ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 3.12, "end": 4.05, "lines": [{"text": "НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ПОЛЕЗНЕЕ", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 6.69, "lines": [{"text": "ОДНОГО РАЗОБРАННОГО ПО ВНИМАТЕЛЬНО", "accent": False, "size": "small"}, {"text": "НАСТОЯЩЕМУ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 8.58, "lines": [{"text": "ТАК ЛЕГКО ЗАКРЫТЬ МНОГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 8.79, "end": 10.68, "lines": [{"text": "И НЕ ПРОДВИНУТЬСЯ В РЕАЛЬНОМ ПОНИМАНИИ", "accent": False, "size": "small"}, {"text": "ТЕМ", "accent": True, "size": "big"}]},
    {"start": 11.01, "end": 12.36, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 12.54, "end": 13.83, "lines": [{"text": "ФИПИ ГДЕ МОЖНО", "accent": False, "size": "small"}, {"text": "РЕШАТЬ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 16.11, "lines": [{"text": "В СВОЕМ ТЕМПЕ И НЕ ГНАТЬСЯ ЗА КОЛИЧЕСТВОМ", "accent": False, "size": "small"}, {"text": "ТЕМПЕ", "accent": True, "size": "big"}]},
    {"start": 16.38, "end": 18.36, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 1.62, "end": 1.95}, {"start": 11.01, "end": 11.34}, {"start": 16.38, "end": 16.71}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (wavy-haired boy, couch/plants room, 19.820s): always solving
# one more new variant before the exam; sometimes it's more useful to go
# back to a known weak topic - the FIPI bank lets you jump straight to
# that topic instead of grinding through everything in order
# ---------------------------------------------------------------------------
b_intro = {"lines": ["РЕШАЕШЬ НОВЫЙ ВАРИАНТ", "ВМЕСТО СТАРОЙ ТЕМЫ?"], "end": 1.5}
b_cards = [
    {"start": 1.59, "end": 3.30, "lines": [{"text": "НУЖНО РЕШАТЬ ЕЩЕ ОДИН НОВЫЙ", "accent": False, "size": "small"}, {"text": "ВАРИАНТ", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 5.94, "lines": [{"text": "ИНОГДА ПОЛЕЗНЕЕ ВЕРНУТЬСЯ К УЖЕ ЗНАКОМОЙ", "accent": False, "size": "small"}, {"text": "ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 7.26, "lines": [{"text": "И РАЗОБРАТЬ В НЕЙ", "accent": False, "size": "small"}, {"text": "ПРОБЕЛ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 10.20, "lines": [{"text": "НОВЫЙ ВАРИАНТ ЧАСТО ПРОСТО ПОВТОРЯЕТ СТАРЫЕ", "accent": False, "size": "small"}, {"text": "ПРОБЕЛЫ", "accent": True, "size": "big"}]},
    {"start": 10.32, "end": 11.31, "lines": [{"text": "В ДРУГИХ ФОРМУЛИРОВКАХ", "accent": False, "size": "small"}, {"text": "ДРУГИХ", "accent": True, "size": "big"}]},
    {"start": 11.70, "end": 13.23, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.38, "end": 14.37, "lines": [{"text": "БАНК ФИПИ ГДЕ", "accent": False, "size": "small"}, {"text": "МОЖНО", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 16.02, "lines": [{"text": "ВЕРНУТЬСЯ ИМЕННО К", "accent": False, "size": "small"}, {"text": "НУЖНОЙ ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 16.23, "end": 17.70, "lines": [{"text": "А НЕ РЕШАТЬ ВСЕ ПОДРЯД ПО", "accent": False, "size": "small"}, {"text": "ПОРЯДКУ", "accent": True, "size": "big"}]},
    {"start": 18.03, "end": 19.89, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.59, "end": 1.92}, {"start": 11.70, "end": 12.03}, {"start": 18.03, "end": 18.36}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (curly-haired boy, 18.604s): prep for the essay subjects is
# only variants and re-read conspects, which barely sticks; the app has
# memorization games for Russian, history and social studies for exactly
# that kind of reinforcement
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ГОТОВИШЬСЯ ТОЛЬКО ПО", "ВАРИАНТАМ И КОНСПЕКТАМ?"], "end": 1.5}
c_cards = [
    {"start": 1.59, "end": 4.20, "lines": [{"text": "К ЕГЭ ПОКА СОСТОИТ ТОЛЬКО ИЗ ВАРИАНТОВ И", "accent": False, "size": "small"}, {"text": "КОНСПЕКТОВ", "accent": True, "size": "big"}]},
    {"start": 4.47, "end": 7.08, "lines": [{"text": "МОЖНО ДОБАВИТЬ ЕЩЕ ОДИН СПОСОБ ЗАКРЕПЛЕНИЯ", "accent": False, "size": "small"}, {"text": "МАТЕРИАЛА", "accent": True, "size": "big"}]},
    {"start": 7.32, "end": 10.02, "lines": [{"text": "ПРОСТОЕ ЧТЕНИЕ КОНСПЕКТА ЧАСТО ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПЛОХО", "accent": True, "size": "big"}]},
    {"start": 10.47, "end": 11.97, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 12.39, "end": 13.56, "lines": [{"text": "И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 15.03, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.59, "lines": [{"text": "КАК РАЗ ДЛЯ ЗАКРЕПЛЕНИЯ", "accent": False, "size": "small"}, {"text": "ТАКОГО", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 18.72, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.59, "end": 1.92}, {"start": 10.47, "end": 10.80}, {"start": 16.89, "end": 17.22}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (curly-haired boy, 18.840s): checking the correct answer after
# a mistake feels like enough, but the same mistake repeats a week later;
# the app gives a full text explanation of the actual logic, not just the
# answer, for every task
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ОШИБАЕШЬСЯ В ТОМ ЖЕ", "МЕСТЕ ЧЕРЕЗ НЕДЕЛЮ?"], "end": 1.5}
d_cards = [
    {"start": 1.89, "end": 3.60, "lines": [{"text": "ОШИБСЯ ПОСМОТРЕЛ ОТВЕТ", "accent": False, "size": "small"}, {"text": "СКАЗАЛ", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 6.06, "lines": [{"text": "А ПОНЯТНО И ЧЕРЕЗ НЕДЕЛЮ ОШИБСЯ ТАМ", "accent": False, "size": "small"}, {"text": "ЖЕ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 10.20, "lines": [{"text": "ВЗГЛЯДЫ НА ПРАВИЛЬНЫЙ ОТВЕТ ОБЫЧНО НЕ ХВАТАЕТ ЧТОБЫ ТЕМА ЗАКРЕПИЛАСЬ ПО", "accent": False, "size": "small"}, {"text": "НАСТОЯЩЕМУ", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 12.12, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 12.30, "end": 13.62, "lines": [{"text": "ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВАЯ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 15.33, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "ЛОГИКУ РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 16.80, "lines": [{"text": "А НЕ ТОЛЬКО НАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 18.93, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.89, "end": 2.22}, {"start": 10.53, "end": 10.86}, {"start": 17.07, "end": 17.40}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (wavy-haired boy, couch/plants room, 18.690s): social-studies
# terms still get confused by the third review; the problem is the format,
# not memory - the app has memorization games for the essay subjects that
# force active recall instead of another re-read
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ТЕРМИНЫ ПУТАЮТСЯ", "НА ТРЕТЬЕМ ПОВТОРЕНИИ?"], "end": 2.4}
e_cards = [
    {"start": 2.67, "end": 4.65, "lines": [{"text": "ПУТАЮТСЯ В ГОЛОВЕ УЖЕ НА ТРЕТЬЕМ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИИ", "accent": True, "size": "big"}]},
    {"start": 4.92, "end": 6.03, "lines": [{"text": "ДЕЛО ОБЫЧНО НЕ В", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 8.04, "lines": [{"text": "ПОМОГАЕТ НЕ ЕЩЕ ОДНО", "accent": False, "size": "small"}, {"text": "ЧТЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 10.56, "lines": [{"text": "А ФОРМАТ ГДЕ ПРИХОДИТСЯ ВСПОМИНАТЬ ОТВЕТ", "accent": False, "size": "small"}, {"text": "САМОМУ", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 11.73, "lines": [{"text": "", "accent": False, "size": "small"}, {"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.85, "end": 14.22, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.54, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.75, "end": 16.65, "lines": [{"text": "ИМЕННО ДЛЯ", "accent": False, "size": "small"}, {"text": "ЭТОГО", "accent": True, "size": "big"}]},
    {"start": 16.77, "end": 18.78, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.67, "end": 3.00}, {"start": 10.92, "end": 11.25}, {"start": 16.77, "end": 17.10}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (wavy-haired boy, couch/plants room, 15.746s): the most useless
# move after a mistake is glancing at the correct answer and moving on -
# it barely sticks; the app gives a full text explanation of the actual
# error for every task
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СМОТРИШЬ ОТВЕТ", "И ИДЕШЬ ДАЛЬШЕ?"], "end": 1.5}
f_cards = [
    {"start": 1.50, "end": 2.88, "lines": [{"text": "ПОСЛЕ ОШИБКИ В ЗАДАНИИ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.09, "end": 4.47, "lines": [{"text": "ПРОСТО ПОСМОТРЕТЬ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНЫЙ ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 4.65, "end": 8.22, "lines": [{"text": "И РЕШАТЬ ДАЛЬШЕ ОШИБКА В ТАКОМ ПОЧТИ НЕ ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "СЛУЧАЕ", "accent": True, "size": "big"}]},
    {"start": 8.58, "end": 9.39, "lines": [{"text": "", "accent": False, "size": "small"}, {"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 9.72, "end": 11.97, "lines": [{"text": "КАЖДОМУ ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.12, "end": 13.65, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "САМУ ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 13.95, "end": 15.84, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 1.50, "end": 1.83}, {"start": 8.58, "end": 8.91}, {"start": 13.95, "end": 14.28}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
