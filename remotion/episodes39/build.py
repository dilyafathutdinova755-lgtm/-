#!/usr/bin/env python3
"""One-off authoring + validation script for tag 'алиса07.09' (3 episodes).
Not a generic tool: hand-picked timings/text per episode, like build_plan.py
was for its own episode. Run from remotion/episodes39/.
"""
import json
import sys

REAL_DURATION = {1: 35.48, 2: 37.164, 3: 36.290}


def check_cards(ep, cards, total_duration):
    prev_end = 0.0
    for i, c in enumerate(cards):
        assert c["start"] < c["end"], f"ep{ep} card{i}: start>=end"
        assert c["start"] >= prev_end - 1e-6, f"ep{ep} card{i}: overlaps previous (start {c['start']} < prev_end {prev_end})"
        dur = c["end"] - c["start"]
        assert dur <= 4.0 + 1e-6, f"ep{ep} card{i}: duration {dur:.2f}s > 4s"
        assert dur >= 0.8, f"ep{ep} card{i}: duration {dur:.2f}s < 0.8s (too short)"
        n_accent = sum(1 for l in c["lines"] for l in [l] if l.get("accent"))
        assert n_accent >= 1, f"ep{ep} card{i}: no accent line"
        for l in c["lines"]:
            assert "?" not in l["text"] or l["text"].endswith("?"), f"ep{ep} card{i}: bad '?' placement"
            assert "," not in l["text"] and "." not in l["text"], f"ep{ep} card{i}: punctuation not allowed: {l['text']}"
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


def check_stock(ep, stock, cards, total_duration, clip_lengths):
    for s in stock:
        assert s["start"] > 0.5, f"ep{ep}: stock cutaway too close to start"
        assert s["end"] < total_duration - 0.5, f"ep{ep}: stock cutaway too close to end"
        src_start = s.get("sourceStart", 0)
        dur = s["end"] - s["start"]
        clip_len = clip_lengths[s["file"]]
        assert src_start + dur <= clip_len - 0.1, (
            f"ep{ep}: stock {s['file']} sourceStart {src_start} + dur {dur:.2f} "
            f"exceeds clip length {clip_len} (need margin)"
        )


def build_running_caption(words, total_duration):
    groups = [{"text": w["text"].upper(), "start": w["start"]} for w in words]
    for idx in range(len(groups)):
        groups[idx]["end"] = groups[idx + 1]["start"] if idx + 1 < len(groups) else total_duration
    groups[0]["start"] = 0.0
    return groups


CLIP_LENGTHS = {
    "stock/stock_desk_window.mp4": 10.1,
    "stock/stock_writing_1.mp4": 7.0,
    "stock/stock_writing_2.mp4": 6.3,
    "stock/stock_girl_student_1.mp4": 7.9,
    "stock/stock_girl_student_2.mp4": 7.3,
    "stock/stock_home_evening.mp4": 26.4,
    "stock/stock_home_night.mp4": 14.8,
}


def process(ep, cards, intro, emphasis, stock):
    total_duration = REAL_DURATION[ep]
    words = json.load(open(f"../asr/words{ep}_fixed.json"))
    for w in words:
        w["start"] = min(w["start"], total_duration)
        w["end"] = min(w["end"], total_duration)

    check_intro_vs_cards(ep, intro["end"], cards)
    check_cards(ep, cards, total_duration)
    check_emphasis(ep, emphasis, total_duration)
    check_stock(ep, stock, cards, total_duration, CLIP_LENGTHS)

    running_caption = build_running_caption(words, total_duration)

    letter = {1: "a", 2: "b", 3: "c"}[ep]
    json.dump(words, open(f"ep_{letter}_words.json", "w"), ensure_ascii=False, indent=2)
    json.dump(cards, open(f"ep_{letter}_cards.json", "w"), ensure_ascii=False, indent=2)
    json.dump(running_caption, open(f"ep_{letter}_running_caption.json", "w"), ensure_ascii=False, indent=2)
    json.dump({"total_duration": total_duration}, open(f"ep_{letter}_duration.json", "w"), indent=2)
    json.dump(intro, open(f"ep_{letter}_intro.json", "w"), ensure_ascii=False, indent=2)
    json.dump(emphasis, open(f"ep_{letter}_emphasis.json", "w"), ensure_ascii=False, indent=2)
    json.dump(stock, open(f"ep_{letter}_stock_cutaways.json", "w"), ensure_ascii=False, indent=2)
    print(f"ep{ep} ({letter}): OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode 1 (clip1): olympiad timing myth -> parallel prep -> app
# ---------------------------------------------------------------------------
ep1_intro = {"lines": ["ГОТОВИШЬСЯ", "ВПУСТУЮ?"], "end": 2.3}
ep1_cards = [
    {"start": 3.85, "end": 6.85, "lines": [
        {"text": "МНОГИЕ ПУТАЮТ", "accent": False, "size": "small"},
        {"text": "КОГДА ОПРАВДАНО", "accent": True, "size": "big"},
    ]},
    {"start": 7.35, "end": 10.40, "lines": [
        {"text": "А КОГДА ЭТО", "accent": False, "size": "small"},
        {"text": "ПРОСТО ЗРЯ", "accent": True, "size": "big"},
    ]},
    {"start": 10.60, "end": 14.20, "lines": [
        {"text": "УЗНАЙ ЗАРАНЕЕ", "accent": False, "size": "small"},
        {"text": "СРОКИ ЭТАПОВ", "accent": True, "size": "big"},
    ]},
    {"start": 14.40, "end": 18.10, "lines": [
        {"text": "НАЧИНАЮТСЯ РАНЬШЕ", "accent": False, "size": "small"},
        {"text": "В СЕНТЯБРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 19.05, "end": 22.55, "lines": [
        {"text": "ФОРМАТ ОЛИМПИАДЫ", "accent": False, "size": "small"},
        {"text": "СОВСЕМ ДРУГОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 22.80, "end": 25.35, "lines": [
        {"text": "НЕ ВМЕСТО", "accent": False, "size": "small"},
        {"text": "ПАРАЛЛЕЛЬНО", "accent": True, "size": "big"},
    ]},
    {"start": 26.25, "end": 29.90, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "ЗАКРЫВАЮ ТЕМЫ", "accent": True, "size": "big"},
    ]},
    {"start": 30.00, "end": 32.90, "lines": [
        {"text": "ЧТОБЫ НЕ ТЕРЯТЬ", "accent": False, "size": "small"},
        {"text": "БАЗУ", "accent": True, "size": "big"},
    ]},
    {"start": 33.40, "end": 35.48, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
# fix small overlap: card2 end 10.40 vs card3 start 10.60 fine; card1 end 6.85 vs card2 start 7.35 fine
ep1_emphasis = [
    {"start": 17.58, "end": 17.91},
    {"start": 23.82, "end": 24.30},
    {"start": 32.13, "end": 32.34},
]
ep1_stock = [
    {"start": 10.77, "end": 17.60, "file": "stock/stock_desk_window.mp4", "sourceStart": 0.3},
]
process(1, ep1_cards, ep1_intro, ep1_emphasis, ep1_stock)

# ---------------------------------------------------------------------------
# Episode 2 (clip2): olympiad vs EGE format/criteria/dates -> app
# ---------------------------------------------------------------------------
ep2_intro = {"lines": ["ПУТАЕШЬ ЕГЭ", "И ОЛИМПИАДУ?"], "end": 2.4}
ep2_cards = [
    {"start": 4.90, "end": 6.75, "lines": [
        {"text": "ПУТАТЬ ИХ", "accent": False, "size": "small"},
        {"text": "ЧАСТАЯ ОШИБКА", "accent": True, "size": "big"},
    ]},
    {"start": 6.90, "end": 10.10, "lines": [
        {"text": "СРЕДИ ТЕХ КТО МЕТИТ", "accent": False, "size": "small"},
        {"text": "НА СТО БАЛЛОВ", "accent": True, "size": "big"},
    ]},
    {"start": 11.00, "end": 13.35, "lines": [
        {"text": "ЕГЭ УСТРОЕН", "accent": False, "size": "small"},
        {"text": "ПО ЧЁТКИМ КРИТЕРИЯМ", "accent": True, "size": "big"},
    ]},
    {"start": 13.65, "end": 15.95, "lines": [
        {"text": "КОНКРЕТНАЯ", "accent": False, "size": "small"},
        {"text": "ФОРМУЛИРОВКА", "accent": True, "size": "big"},
    ]},
    {"start": 16.10, "end": 18.30, "lines": [
        {"text": "КОНКРЕТНЫЕ БАЛЛЫ", "accent": False, "size": "small"},
        {"text": "ЗА ШАГ", "accent": True, "size": "big"},
    ]},
    {"start": 18.75, "end": 20.10, "lines": [
        {"text": "СРОКИ", "accent": False, "size": "small"},
        {"text": "ТОЖЕ РАЗНЫЕ", "accent": True, "size": "big"},
    ]},
    {"start": 20.35, "end": 23.35, "lines": [
        {"text": "ЭТАПЫ ОЛИМПИАД", "accent": False, "size": "small"},
        {"text": "С ОСЕНИ ДО ВЕСНЫ", "accent": True, "size": "big"},
    ]},
    {"start": 23.60, "end": 26.40, "lines": [
        {"text": "А ЭКЗАМЕН", "accent": False, "size": "small"},
        {"text": "ОДНОЙ ДАТОЙ", "accent": True, "size": "big"},
    ]},
    {"start": 26.90, "end": 29.40, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "ЗАКРЫВАЮ ОТДЕЛЬНО", "accent": True, "size": "big"},
    ]},
    {"start": 29.40, "end": 32.30, "lines": [
        {"text": "ФОРМАТ ЭКЗАМЕНА", "accent": False, "size": "small"},
        {"text": "ЧТОБЫ НЕ ТЕРЯТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 32.40, "end": 34.55, "lines": [
        {"text": "РАДИ", "accent": False, "size": "small"},
        {"text": "НЕСТАНДАРТНОСТИ", "accent": True, "size": "big"},
    ]},
    {"start": 35.10, "end": 37.164, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep2_emphasis = [
    {"start": 8.34, "end": 8.79},
    {"start": 24.03, "end": 24.30},
    {"start": 33.66, "end": 34.41},
]
ep2_stock = [
    {"start": 11.16, "end": 17.85, "file": "stock/stock_writing_1.mp4", "sourceStart": 0.0},
]
process(2, ep2_cards, ep2_intro, ep2_emphasis, ep2_stock)

# ---------------------------------------------------------------------------
# Episode 3 (clip3): 7-day diary experiment combining both -> app
# ---------------------------------------------------------------------------
ep3_intro = {"lines": ["СЕМЬ ДНЕЙ", "БЕЗ ПРОВАЛА?"], "end": 2.5}
ep3_cards = [
    {"start": 3.90, "end": 6.15, "lines": [
        {"text": "ПОПРОБОВАЛА", "accent": False, "size": "small"},
        {"text": "СОВМЕСТИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 6.30, "end": 7.55, "lines": [
        {"text": "СЕМЬ ДНЕЙ", "accent": True, "size": "big"},
        {"text": "ПОДРЯД", "accent": False, "size": "small"},
    ]},
    {"start": 9.35, "end": 11.30, "lines": [
        {"text": "ДЕНЬ ПЕРВЫЙ", "accent": True, "size": "big"},
        {"text": "ЧАСТИЧНО ОЛИМПИАДА", "accent": False, "size": "small"},
    ]},
    {"start": 11.75, "end": 14.35, "lines": [
        {"text": "ДВАДЦАТЬ МИНУТ", "accent": False, "size": "small"},
        {"text": "НА ЭКЗАМЕН", "accent": True, "size": "big"},
    ]},
    {"start": 14.95, "end": 16.90, "lines": [
        {"text": "ДЕНЬ ТРЕТИЙ", "accent": True, "size": "big"},
        {"text": "ФОРМАТЫ ПУТАЮТСЯ", "accent": False, "size": "small"},
    ]},
    {"start": 17.55, "end": 19.85, "lines": [
        {"text": "РАЗВЕЛА ИХ", "accent": False, "size": "small"},
        {"text": "ПО ВРЕМЕНИ ДНЯ", "accent": True, "size": "big"},
    ]},
    {"start": 20.85, "end": 22.45, "lines": [
        {"text": "ДЕНЬ СЕДЬМОЙ", "accent": True, "size": "big"},
        {"text": "КОРОТКИЙ ПРОБНИК", "accent": False, "size": "small"},
    ]},
    {"start": 24.50, "end": 26.65, "lines": [
        {"text": "БАЗА", "accent": False, "size": "small"},
        {"text": "НЕ ПРОСЕЛА", "accent": True, "size": "big"},
    ]},
    {"start": 26.70, "end": 28.30, "lines": [
        {"text": "ЗА НЕДЕЛЮ", "accent": False, "size": "small"},
        {"text": "ОЛИМПИАДНОГО ФОКУСА", "accent": True, "size": "big"},
    ]},
    {"start": 28.70, "end": 31.10, "lines": [
        {"text": "СОВМЕЩАТЬ РЕАЛЬНО", "accent": False, "size": "small"},
        {"text": "ЕСЛИ ЧЁТКО", "accent": True, "size": "big"},
    ]},
    {"start": 32.05, "end": 34.00, "lines": [
        {"text": "НЕ СМЕШИВАТЬ", "accent": False, "size": "small"},
        {"text": "ФОРМАТЫ", "accent": True, "size": "big"},
    ]},
    {"start": 34.30, "end": 36.290, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
ep3_emphasis = [
    {"start": 6.42, "end": 6.78},
    {"start": 22.17, "end": 22.41},
    {"start": 26.10, "end": 26.43},
]
ep3_stock = [
    {"start": 9.51, "end": 14.31, "file": "stock/stock_writing_2.mp4", "sourceStart": 0.0},
]
process(3, ep3_cards, ep3_intro, ep3_emphasis, ep3_stock)

print("ALL EPISODES BUILT AND VALIDATED")
