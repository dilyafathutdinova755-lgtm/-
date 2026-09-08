#!/usr/bin/env python3
"""One-off authoring + validation script for tag 'coffee123' (3 episodes).
Not a generic tool: hand-picked timings/text per episode. Run from
remotion/episodes44/.

Single host this batch (a student in a study room, travel-photo wall,
"THE SMITHS" poster, "ЕГЭ 2026" sticky note) talking about balancing EGE
prep with olympiad prep during the same week.
"""
import json

REAL_DURATION = {
    "a": 29.674, "b": 32.789, "c": 29.504,
}
SOURCE_FILE = {
    "a": "v1", "b": "v2", "c": "v3",
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


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123/{src}_words.json"))
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
# Episode A (v1): olympiad and EGE dates clash the same week; decided to go
# but cut EGE Trenazher time to a minimum for balance
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ОЛИМПИАДА И ЕГЭ", "В ОДНУ НЕДЕЛЮ?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 4.50, "lines": [
        {"text": "ПЕРЕСЕКЛИСЬ", "accent": False, "size": "small"},
        {"text": "ПО ДАТАМ", "accent": True, "size": "big"},
    ]},
    {"start": 5.20, "end": 7.10, "lines": [
        {"text": "ИДТИ ИЛИ", "accent": False, "size": "small"},
        {"text": "ПРОПУСТИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 7.30, "end": 8.20, "lines": [
        {"text": "ДАЛОСЬ", "accent": False, "size": "small"},
        {"text": "НЕПРОСТО", "accent": True, "size": "big"},
    ]},
    {"start": 8.40, "end": 9.45, "lines": [
        {"text": "ПРИ ТЕКУЩЕЙ", "accent": False, "size": "small"},
        {"text": "НАГРУЗКЕ", "accent": True, "size": "big"},
    ]},
    {"start": 10.30, "end": 11.65, "lines": [
        {"text": "ВЗВЕСИЛА", "accent": False, "size": "small"},
        {"text": "ШАНСЫ", "accent": True, "size": "big"},
    ]},
    {"start": 12.65, "end": 14.40, "lines": [
        {"text": "ПРОТИВ", "accent": False, "size": "small"},
        {"text": "ВРЕМЕНИ", "accent": True, "size": "big"},
    ]},
    {"start": 15.60, "end": 16.50, "lines": [
        {"text": "БАЗА", "accent": False, "size": "small"},
        {"text": "ПОД ЕГЭ", "accent": True, "size": "big"},
    ]},
    {"start": 17.30, "end": 18.10, "lines": [
        {"text": "РЕШИЛА", "accent": False, "size": "small"},
        {"text": "ПОЙТИ", "accent": True, "size": "big"},
    ]},
    {"start": 18.60, "end": 19.50, "lines": [
        {"text": "НО", "accent": False, "size": "small"},
        {"text": "СОКРАТИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 19.55, "end": 20.45, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 20.50, "end": 21.95, "lines": [
        {"text": "НА ЭТУ НЕДЕЛЮ", "accent": False, "size": "small"},
        {"text": "ДО МИНИМУМА", "accent": True, "size": "big"},
    ]},
    {"start": 22.15, "end": 23.00, "lines": [
        {"text": "РАДИ", "accent": False, "size": "small"},
        {"text": "БАЛАНСА", "accent": True, "size": "big"},
    ]},
    {"start": 23.70, "end": 26.45, "lines": [
        {"text": "НЕ ВСЕГДА", "accent": False, "size": "small"},
        {"text": "ОДИНАКОВО", "accent": True, "size": "big"},
    ]},
    {"start": 27.60, "end": 29.674, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
a_emphasis = [
    {"start": 6.51, "end": 6.99},
    {"start": 17.37, "end": 17.70},
    {"start": 25.50, "end": 26.01},
]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (v2): stress before the EGE exam vs before the olympiad turned
# out to be different in nature, noticed while prepping for both in parallel
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ОДИНАКОВЫЙ СТРЕСС", "ПЕРЕД ОБОИМИ?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 3.60, "lines": [
        {"text": "СТРЕСС", "accent": False, "size": "small"},
        {"text": "ПЕРЕД ОЛИМПИАДОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 4.00, "end": 6.10, "lines": [
        {"text": "ОКАЗАЛИСЬ", "accent": False, "size": "small"},
        {"text": "РАЗНЫМИ", "accent": True, "size": "big"},
    ]},
    {"start": 6.75, "end": 8.75, "lines": [
        {"text": "ЗАМЕТИЛА", "accent": False, "size": "small"},
        {"text": "НА ЭТОЙ НЕДЕЛЕ", "accent": True, "size": "big"},
    ]},
    {"start": 8.90, "end": 10.95, "lines": [
        {"text": "ПАРАЛЛЕЛЬНО", "accent": False, "size": "small"},
        {"text": "К ОБОИМ", "accent": True, "size": "big"},
    ]},
    {"start": 11.65, "end": 12.60, "lines": [
        {"text": "ПЕРЕД", "accent": False, "size": "small"},
        {"text": "ОЛИМПИАДОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 12.65, "end": 14.10, "lines": [
        {"text": "ВОЛНЕНИЕ", "accent": False, "size": "small"},
        {"text": "АЗАРТ", "accent": True, "size": "big"},
    ]},
    {"start": 14.75, "end": 17.10, "lines": [
        {"text": "ПРЕДВКУШЕНИЕ", "accent": False, "size": "small"},
        {"text": "ЗАДАЧИ", "accent": True, "size": "big"},
    ]},
    {"start": 19.60, "end": 20.55, "lines": [
        {"text": "СКОРЕЕ", "accent": False, "size": "small"},
        {"text": "ДАВЛЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 20.65, "end": 22.20, "lines": [
        {"text": "ФОРМАЛЬНОСТИ", "accent": False, "size": "small"},
        {"text": "ИТОГИ", "accent": True, "size": "big"},
    ]},
    {"start": 22.20, "end": 23.45, "lines": [
        {"text": "ДЛЯ ПОСТУПЛЕНИЯ", "accent": False, "size": "small"},
        {"text": "В ЦЕЛОМ", "accent": True, "size": "big"},
    ]},
    {"start": 24.55, "end": 27.05, "lines": [
        {"text": "РАЗНЫЕ", "accent": False, "size": "small"},
        {"text": "ОТНОШЕНИЯ", "accent": True, "size": "big"},
    ]},
    {"start": 27.50, "end": 29.95, "lines": [
        {"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"},
        {"text": "И ИНТЕНСИВЫ", "accent": True, "size": "big"},
    ]},
    {"start": 30.90, "end": 32.789, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
b_emphasis = [
    {"start": 14.16, "end": 14.43},
    {"start": 20.70, "end": 21.21},
    {"start": 25.02, "end": 25.38},
]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (v3): combined the pre-lesson warmup with the pre-olympiad
# warmup this week to save time - one action closes two tasks
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТРАТИШЬ ВРЕМЯ НА", "ДВЕ РАЗМИНКИ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 4.30, "lines": [
        {"text": "ОБЪЕДИНИЛА", "accent": False, "size": "small"},
        {"text": "РАЗМИНКУ", "accent": True, "size": "big"},
    ]},
    {"start": 4.35, "end": 5.90, "lines": [
        {"text": "ПЕРЕД", "accent": False, "size": "small"},
        {"text": "ИНТЕНСИВОМ", "accent": True, "size": "big"},
    ]},
    {"start": 6.00, "end": 6.85, "lines": [
        {"text": "НА ЭТОЙ", "accent": False, "size": "small"},
        {"text": "НЕДЕЛЕ", "accent": True, "size": "big"},
    ]},
    {"start": 7.20, "end": 8.80, "lines": [
        {"text": "ПРОСТО", "accent": False, "size": "small"},
        {"text": "СЭКОНОМИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 8.90, "end": 10.70, "lines": [
        {"text": "УТРОМ ПЕРЕД", "accent": False, "size": "small"},
        {"text": "НАГРУЗКОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 11.50, "end": 13.10, "lines": [
        {"text": "ПЯТЬ МИНУТ", "accent": False, "size": "small"},
        {"text": "ЗАДАНИЙ", "accent": True, "size": "big"},
    ]},
    {"start": 13.15, "end": 14.10, "lines": [
        {"text": "В ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 14.45, "end": 16.15, "lines": [
        {"text": "РАЗОГРЕВАЮТ", "accent": False, "size": "small"},
        {"text": "МОЗГ", "accent": True, "size": "big"},
    ]},
    {"start": 16.30, "end": 18.80, "lines": [
        {"text": "ОТДЕЛЬНОЙ", "accent": False, "size": "small"},
        {"text": "МЕТОДИКИ", "accent": True, "size": "big"},
    ]},
    {"start": 19.90, "end": 22.30, "lines": [
        {"text": "ОДНО ДЕЙСТВИЕ", "accent": False, "size": "small"},
        {"text": "ДВЕ ЗАДАЧИ", "accent": True, "size": "big"},
    ]},
    {"start": 22.40, "end": 24.20, "lines": [
        {"text": "ВМЕСТО ДВУХ", "accent": False, "size": "small"},
        {"text": "РИТУАЛОВ", "accent": True, "size": "big"},
    ]},
    {"start": 24.70, "end": 26.40, "lines": [
        {"text": "ЭКОНОМИЯ", "accent": False, "size": "small"},
        {"text": "ПРИЯТНАЯ", "accent": True, "size": "big"},
    ]},
    {"start": 27.50, "end": 29.504, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
c_emphasis = [
    {"start": 7.95, "end": 8.40},
    {"start": 14.52, "end": 15.06},
    {"start": 25.86, "end": 26.31},
]
process("c", c_cards, c_intro, c_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
