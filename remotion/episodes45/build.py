#!/usr/bin/env python3
"""One-off authoring + validation script for the SECOND 'coffee123' batch
(3 more episodes uploaded under the same tag after the first 3 were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes45/.

Original teen host is back (same bedroom setting as the earliest batches).
Content angle: discovering EGE Trenazher through classmates, the app
feeling like a short-video feed, beating procrastination in small doses.
"""
import json

REAL_DURATION = {
    "a": 22.85, "b": 26.924, "c": 25.48,
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
    words = json.load(open(f"../asr_coffee123_2/{src}_words.json"))
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
# Episode A (v1): almost nobody in class knows about the app, found it by
# accident in the class chat and got hooked for 15 minutes like it's TikTok
# ---------------------------------------------------------------------------
a_intro = {"lines": ["СЛУЧАЙНО ЗАЛИП", "НА 15 МИНУТ?"], "end": 2.3}
a_cards = [
    {"start": 2.60, "end": 3.70, "lines": [
        {"text": "ПРО", "accent": False, "size": "small"},
        {"text": "ПРИЛОЖЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 3.90, "end": 4.90, "lines": [
        {"text": "А ЗРЯ", "accent": False, "size": "small"},
        {"text": "НАЗЫВАЕТСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 5.10, "end": 6.10, "lines": [
        {"text": "ОНО", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"},
    ]},
    {"start": 6.30, "end": 7.20, "lines": [
        {"text": "НАТКНУЛСЯ", "accent": False, "size": "small"},
        {"text": "СЛУЧАЙНО", "accent": True, "size": "big"},
    ]},
    {"start": 7.65, "end": 8.50, "lines": [
        {"text": "В ЧАТЕ", "accent": False, "size": "small"},
        {"text": "КЛАССА", "accent": True, "size": "big"},
    ]},
    {"start": 8.55, "end": 9.40, "lines": [
        {"text": "ОТКРЫЛ", "accent": False, "size": "small"},
        {"text": "ОТ СКУКИ", "accent": True, "size": "big"},
    ]},
    {"start": 9.90, "end": 11.00, "lines": [
        {"text": "ЗАЛИП НА", "accent": False, "size": "small"},
        {"text": "15 МИНУТ", "accent": True, "size": "big"},
    ]},
    {"start": 11.05, "end": 11.90, "lines": [
        {"text": "ВМЕСТО", "accent": False, "size": "small"},
        {"text": "ЛЕНТЫ", "accent": True, "size": "big"},
    ]},
    {"start": 12.00, "end": 14.20, "lines": [
        {"text": "КОРОТКИЕ ВИДЕО", "accent": False, "size": "small"},
        {"text": "ПО ТЕМАМ", "accent": True, "size": "big"},
    ]},
    {"start": 14.30, "end": 15.40, "lines": [
        {"text": "ИГРЫ", "accent": False, "size": "small"},
        {"text": "ЗАКРЕПИТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 15.45, "end": 16.75, "lines": [
        {"text": "ПРЯМО КАК", "accent": False, "size": "small"},
        {"text": "ТИКТОК", "accent": True, "size": "big"},
    ]},
    {"start": 16.85, "end": 18.55, "lines": [
        {"text": "ПОКА КЛАСС", "accent": False, "size": "small"},
        {"text": "ПАНИКУЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 18.70, "end": 19.90, "lines": [
        {"text": "ПРОСТО ИНОГДА", "accent": False, "size": "small"},
        {"text": "ОТКРЫВАЮ", "accent": True, "size": "big"},
    ]},
    {"start": 20.00, "end": 20.90, "lines": [
        {"text": "МЕЖДУ", "accent": False, "size": "small"},
        {"text": "ДЕЛОМ", "accent": True, "size": "big"},
    ]},
    {"start": 21.00, "end": 22.85, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
a_emphasis = [
    {"start": 10.02, "end": 10.20},
    {"start": 16.44, "end": 16.71},
    {"start": 19.59, "end": 19.86},
]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (v2): half the class was already using it, he found out last;
# everyone pretended to just scroll their feed while actually studying
# ---------------------------------------------------------------------------
b_intro = {"lines": ["УЗНАЛ ОБ ЭТОМ", "ПОСЛЕДНИМ?"], "end": 2.3}
b_cards = [
    {"start": 2.60, "end": 3.60, "lines": [
        {"text": "В ПРИЛОЖЕНИИ", "accent": False, "size": "small"},
        {"text": "ДЛЯ ЕГЭ", "accent": True, "size": "big"},
    ]},
    {"start": 3.70, "end": 4.90, "lines": [
        {"text": "КОТОРОЕ", "accent": False, "size": "small"},
        {"text": "НАЗЫВАЕТСЯ", "accent": True, "size": "big"},
    ]},
    {"start": 5.00, "end": 6.00, "lines": [
        {"text": "ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"},
    ]},
    {"start": 6.10, "end": 7.20, "lines": [
        {"text": "УЗНАЛ", "accent": False, "size": "small"},
        {"text": "ПОСЛЕДНИМ", "accent": True, "size": "big"},
    ]},
    {"start": 7.70, "end": 8.60, "lines": [
        {"text": "ВСЕ", "accent": False, "size": "small"},
        {"text": "ХИТРИЛИ", "accent": True, "size": "big"},
    ]},
    {"start": 8.65, "end": 9.70, "lines": [
        {"text": "ПРОСТО", "accent": False, "size": "small"},
        {"text": "ЛИСТАЮТ", "accent": True, "size": "big"},
    ]},
    {"start": 10.20, "end": 11.00, "lines": [
        {"text": "А НА", "accent": False, "size": "small"},
        {"text": "САМОМ ДЕЛЕ", "accent": True, "size": "big"},
    ]},
    {"start": 11.10, "end": 12.65, "lines": [
        {"text": "ПРОХОДИЛИ", "accent": False, "size": "small"},
        {"text": "ТЕМЫ", "accent": True, "size": "big"},
    ]},
    {"start": 12.90, "end": 14.40, "lines": [
        {"text": "СКАЧАЛ", "accent": False, "size": "small"},
        {"text": "ИЗ ИНТЕРЕСА", "accent": True, "size": "big"},
    ]},
    {"start": 14.55, "end": 15.95, "lines": [
        {"text": "ЗАВИС", "accent": False, "size": "small"},
        {"text": "НА ПОЛЧАСА", "accent": True, "size": "big"},
    ]},
    {"start": 16.45, "end": 17.35, "lines": [
        {"text": "ВИДЕО", "accent": False, "size": "small"},
        {"text": "КОРОТКИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 17.45, "end": 18.30, "lines": [
        {"text": "ИГРА", "accent": False, "size": "small"},
        {"text": "ПРОСТАЯ", "accent": True, "size": "big"},
    ]},
    {"start": 18.45, "end": 20.15, "lines": [
        {"text": "НЕ ПОХОЖЕ", "accent": False, "size": "small"},
        {"text": "НА УЧЕБНИК", "accent": True, "size": "big"},
    ]},
    {"start": 20.75, "end": 21.60, "lines": [
        {"text": "ТЕПЕРЬ", "accent": False, "size": "small"},
        {"text": "Я ТОЖЕ", "accent": True, "size": "big"},
    ]},
    {"start": 21.65, "end": 22.95, "lines": [
        {"text": "ЧАСТЬ", "accent": False, "size": "small"},
        {"text": "ПОЛОВИНЫ", "accent": True, "size": "big"},
    ]},
    {"start": 23.05, "end": 24.95, "lines": [
        {"text": "ПРОСТО ТИХО", "accent": False, "size": "small"},
        {"text": "БЕЗ ПОСТОВ", "accent": True, "size": "big"},
    ]},
    {"start": 25.10, "end": 26.924, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
b_emphasis = [
    {"start": 7.14, "end": 7.56},
    {"start": 13.89, "end": 14.37},
    {"start": 20.25, "end": 20.52},
]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (v3): found a way to study even on the laziest days - opens the
# app instead of a feed for exactly one topic, closed more topics in a
# month than all summer with a textbook
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЛЕНЬ ПОБЕЖДАЕТ", "КАЖДЫЙ РАЗ?"], "end": 2.3}
c_cards = [
    {"start": 2.60, "end": 4.30, "lines": [
        {"text": "ДАЖЕ В ДНИ", "accent": False, "size": "small"},
        {"text": "ЛЕНИ", "accent": True, "size": "big"},
    ]},
    {"start": 4.40, "end": 5.90, "lines": [
        {"text": "НАЗЫВАЕТСЯ", "accent": False, "size": "small"},
        {"text": "ПРИЛОЖЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 6.00, "end": 6.95, "lines": [
        {"text": "ЕГЭ", "accent": False, "size": "small"},
        {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"},
    ]},
    {"start": 7.05, "end": 7.90, "lines": [
        {"text": "ОТКРЫВАЯ", "accent": False, "size": "small"},
        {"text": "ЕГО", "accent": True, "size": "big"},
    ]},
    {"start": 7.95, "end": 9.80, "lines": [
        {"text": "ВМЕСТО ЛЕНТЫ", "accent": False, "size": "small"},
        {"text": "НА ОДНУ ТЕМУ", "accent": True, "size": "big"},
    ]},
    {"start": 9.95, "end": 11.65, "lines": [
        {"text": "НЕ ОЩУЩАЕТСЯ", "accent": False, "size": "small"},
        {"text": "КАК УЧЁБА", "accent": True, "size": "big"},
    ]},
    {"start": 11.75, "end": 12.65, "lines": [
        {"text": "15 МИНУТ", "accent": False, "size": "small"},
        {"text": "ПРОХОДИТ", "accent": True, "size": "big"},
    ]},
    {"start": 13.15, "end": 14.45, "lines": [
        {"text": "БЫСТРЕЕ ЧЕМ", "accent": False, "size": "small"},
        {"text": "РОЛИК", "accent": True, "size": "big"},
    ]},
    {"start": 14.50, "end": 15.40, "lines": [
        {"text": "ПРО ЧУЖУЮ", "accent": False, "size": "small"},
        {"text": "ЖИЗНЬ", "accent": True, "size": "big"},
    ]},
    {"start": 15.55, "end": 16.80, "lines": [
        {"text": "ЗА МЕСЯЦ", "accent": False, "size": "small"},
        {"text": "ЗАХОДОВ", "accent": True, "size": "big"},
    ]},
    {"start": 16.80, "end": 17.65, "lines": [
        {"text": "ЗАКРЫЛ", "accent": False, "size": "small"},
        {"text": "БОЛЬШЕ ТЕМ", "accent": True, "size": "big"},
    ]},
    {"start": 18.05, "end": 19.75, "lines": [
        {"text": "ЧЕМ ЗА ЛЕТО", "accent": False, "size": "small"},
        {"text": "С УЧЕБНИКОМ", "accent": True, "size": "big"},
    ]},
    {"start": 20.35, "end": 21.50, "lines": [
        {"text": "ЛЕНЬ", "accent": False, "size": "small"},
        {"text": "НИКУДА", "accent": True, "size": "big"},
    ]},
    {"start": 21.55, "end": 23.35, "lines": [
        {"text": "ТЕПЕРЬ", "accent": False, "size": "small"},
        {"text": "РЕЖЕ", "accent": True, "size": "big"},
    ]},
    {"start": 23.50, "end": 25.48, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
c_emphasis = [
    {"start": 3.06, "end": 3.93},
    {"start": 13.23, "end": 13.74},
    {"start": 22.53, "end": 22.65},
]
process("c", c_cards, c_intro, c_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
