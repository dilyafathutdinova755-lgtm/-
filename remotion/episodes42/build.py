#!/usr/bin/env python3
"""One-off authoring + validation script for tag '0622VAR' (6 episodes).
Not a generic tool: hand-picked timings/text per episode. Run from
remotion/episodes42/.
"""
import json

REAL_DURATION = {
    "a": 24.28, "b": 24.76, "c": 24.44, "d": 24.20, "e": 24.76, "f": 24.92,
}
SOURCE_FILE = {
    "a": "v1_plain", "b": "v1_2160p", "c": "v2_plain",
    "d": "v2_2160p", "e": "v3_plain", "f": "v3_2160p",
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
    words = json.load(open(f"../asr_0622var/{src}_fixed.json"))
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
# Episode A (v1_plain): morning plan too ambitious, evening reality half done
# ---------------------------------------------------------------------------
a_intro = {"lines": ["УТРОМ ПЛАН", "ВЕЧЕРОМ ПРОВАЛ?"], "end": 2.3}
a_cards = [
    {"start": 3.85, "end": 6.20, "lines": [
        {"text": "А ВЕЧЕРОМ", "accent": False, "size": "small"},
        {"text": "СРАВНИЛ", "accent": True, "size": "big"},
    ]},
    {"start": 6.25, "end": 8.50, "lines": [
        {"text": "ЧТО РЕАЛЬНО", "accent": False, "size": "small"},
        {"text": "УСПЕЛ", "accent": True, "size": "big"},
    ]},
    {"start": 8.90, "end": 10.55, "lines": [
        {"text": "СОВПАЛО", "accent": False, "size": "small"},
        {"text": "НАПОЛОВИНУ", "accent": True, "size": "big"},
    ]},
    {"start": 10.70, "end": 14.05, "lines": [
        {"text": "СТАЛО НЕЛОВКО", "accent": False, "size": "small"},
        {"text": "ЗА СЕБЯ", "accent": True, "size": "big"},
    ]},
    {"start": 14.10, "end": 17.55, "lines": [
        {"text": "ПЛАНЫ СКРОМНЕЕ", "accent": False, "size": "small"},
        {"text": "ЧТОБЫ ВЫПОЛНЯТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 17.60, "end": 19.35, "lines": [
        {"text": "ЧЕРЕЗ", "accent": False, "size": "small"},
        {"text": "ЕГЭ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 19.50, "end": 22.35, "lines": [
        {"text": "СКРОМНЫЙ ПЛАН", "accent": False, "size": "small"},
        {"text": "ЛУЧШЕ КРАСИВОГО", "accent": True, "size": "big"},
    ]},
    {"start": 22.40, "end": 24.28, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
a_emphasis = [
    {"start": 9.93, "end": 10.38},
    {"start": 12.42, "end": 12.84},
    {"start": 15.30, "end": 15.66},
]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (v1_2160p): turned prep into a self-scoring game
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ГОТОВИШЬСЯ", "КАК ИГРУ?"], "end": 2.3}
b_cards = [
    {"start": 3.90, "end": 6.50, "lines": [
        {"text": "НА ЭТОЙ НЕДЕЛЕ", "accent": False, "size": "small"},
        {"text": "НАЧИСЛЯЮ ОЧКИ", "accent": True, "size": "big"},
    ]},
    {"start": 6.55, "end": 9.15, "lines": [
        {"text": "ПОДРЯД", "accent": False, "size": "small"},
        {"text": "БЕЗ ОШИБОК", "accent": True, "size": "big"},
    ]},
    {"start": 9.35, "end": 10.60, "lines": [
        {"text": "ГЛУПО", "accent": True, "size": "big"},
        {"text": "ЗВУЧИТ СО СТОРОНЫ", "accent": False, "size": "small"},
    ]},
    {"start": 10.70, "end": 13.65, "lines": [
        {"text": "НО МОТИВАЦИЯ", "accent": False, "size": "small"},
        {"text": "ВЫРОСЛА ЗАМЕТНЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 13.70, "end": 16.20, "lines": [
        {"text": "ЧЕМ ОТ СЕРЬЁЗНЫХ", "accent": False, "size": "small"},
        {"text": "РАЗГОВОРОВ", "accent": True, "size": "big"},
    ]},
    {"start": 16.30, "end": 18.50, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "ЛИЧНЫЙ СЧЁТ", "accent": True, "size": "big"},
    ]},
    {"start": 18.60, "end": 20.20, "lines": [
        {"text": "СВОЙ СЧЁТ", "accent": False, "size": "small"},
        {"text": "И СТАТИСТИКА", "accent": True, "size": "big"},
    ]},
    {"start": 20.60, "end": 22.70, "lines": [
        {"text": "ИГРА ИНОГДА", "accent": False, "size": "small"},
        {"text": "ЛУЧШЕ ДИСЦИПЛИНЫ", "accent": True, "size": "big"},
    ]},
    {"start": 22.90, "end": 24.76, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
b_emphasis = [
    {"start": 5.46, "end": 5.64},
    {"start": 11.91, "end": 12.30},
    {"start": 22.11, "end": 22.59},
]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (v2_plain): testing the "21 days" habit claim on self
# ---------------------------------------------------------------------------
c_intro = {"lines": ["РАБОТАЕТ ЛИ", "ПРАВИЛО 21 ДНЯ?"], "end": 2.4}
c_cards = [
    {"start": 4.05, "end": 5.95, "lines": [
        {"text": "ПРОЧИТАЛ", "accent": False, "size": "small"},
        {"text": "В ОДНОМ РОЛИКЕ", "accent": True, "size": "big"},
    ]},
    {"start": 6.15, "end": 8.65, "lines": [
        {"text": "РЕШИЛ ПРОВЕРИТЬ", "accent": False, "size": "small"},
        {"text": "НА СЕБЕ", "accent": True, "size": "big"},
    ]},
    {"start": 8.80, "end": 10.80, "lines": [
        {"text": "БЕЗ ДОВЕРИЯ", "accent": False, "size": "small"},
        {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 10.95, "end": 13.55, "lines": [
        {"text": "СЧИТАЮ ДНИ", "accent": False, "size": "small"},
        {"text": "ПОДРЯД", "accent": True, "size": "big"},
    ]},
    {"start": 13.60, "end": 16.70, "lines": [
        {"text": "ИЗМЕНИТСЯ ЛИ", "accent": False, "size": "small"},
        {"text": "ОЩУЩЕНИЕ", "accent": True, "size": "big"},
    ]},
    {"start": 16.75, "end": 18.60, "lines": [
        {"text": "ПОКА РАНО", "accent": False, "size": "small"},
        {"text": "ДЕЛАТЬ ВЫВОДЫ", "accent": True, "size": "big"},
    ]},
    {"start": 18.65, "end": 20.95, "lines": [
        {"text": "САМ ПРОЦЕСС", "accent": False, "size": "small"},
        {"text": "УЖЕ МОТИВИРУЕТ", "accent": True, "size": "big"},
    ]},
    {"start": 21.00, "end": 22.45, "lines": [
        {"text": "НЕ ПРОПУСКАТЬ", "accent": False, "size": "small"},
        {"text": "ДНИ", "accent": True, "size": "big"},
    ]},
    {"start": 22.55, "end": 24.44, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
c_emphasis = [
    {"start": 1.41, "end": 1.65},
    {"start": 9.54, "end": 9.87},
    {"start": 20.43, "end": 20.82},
]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (v2_2160p): mock-exam anxiety then vs calm curiosity now
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПРОБНИК ЕЩЁ", "ПУГАЕТ?"], "end": 2.3}
d_cards = [
    {"start": 3.60, "end": 7.10, "lines": [
        {"text": "ПАНИКА ОТ ДАТЫ", "accent": False, "size": "small"},
        {"text": "НА ДОСКЕ", "accent": True, "size": "big"},
    ]},
    {"start": 7.25, "end": 9.15, "lines": [
        {"text": "СРАВНИЛ РЕАКЦИЮ", "accent": False, "size": "small"},
        {"text": "ТОГДА И СЕЙЧАС", "accent": True, "size": "big"},
    ]},
    {"start": 9.20, "end": 10.95, "lines": [
        {"text": "ПЕРЕД НОВЫМ", "accent": False, "size": "small"},
        {"text": "ПРОБНИКОМ", "accent": True, "size": "big"},
    ]},
    {"start": 11.00, "end": 12.15, "lines": [
        {"text": "ЗАМЕТИЛ", "accent": True, "size": "big"},
        {"text": "РАЗНИЦУ", "accent": False, "size": "small"},
    ]},
    {"start": 12.30, "end": 15.75, "lines": [
        {"text": "СПОКОЙНОЕ ЛЮБОПЫТСТВО", "accent": False, "size": "small"},
        {"text": "ВМЕСТО СТРАХА", "accent": True, "size": "big"},
    ]},
    {"start": 15.80, "end": 18.25, "lines": [
        {"text": "РЕГУЛЯРНЫЕ ЗАНЯТИЯ", "accent": False, "size": "small"},
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": True, "size": "big"},
    ]},
    {"start": 18.30, "end": 20.95, "lines": [
        {"text": "СНИЗИЛИ", "accent": False, "size": "small"},
        {"text": "ТРЕВОГУ", "accent": True, "size": "big"},
    ]},
    {"start": 21.10, "end": 22.30, "lines": [
        {"text": "БЕЗ", "accent": False, "size": "small"},
        {"text": "РЕЗКИХ СКАЧКОВ", "accent": True, "size": "big"},
    ]},
    {"start": 22.40, "end": 24.20, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
d_emphasis = [
    {"start": 3.69, "end": 3.90},
    {"start": 11.67, "end": 12.03},
    {"start": 18.69, "end": 18.96},
]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (v3_plain): the "still have time" lie catches up with him
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЕЩЁ МНОГО", "ВРЕМЕНИ?"], "end": 2.3}
e_cards = [
    {"start": 4.50, "end": 5.40, "lines": [
        {"text": "МЕСЯЦ НАЗАД", "accent": True, "size": "big"},
    ]},
    {"start": 5.80, "end": 7.70, "lines": [
        {"text": "ПОЙМАЛ СЕБЯ", "accent": False, "size": "small"},
        {"text": "НА ВРАНЬЕ", "accent": True, "size": "big"},
    ]},
    {"start": 7.75, "end": 9.85, "lines": [
        {"text": "САМ СЕБЕ", "accent": False, "size": "small"},
        {"text": "ВСЁ РЕЖЕ", "accent": True, "size": "big"},
    ]},
    {"start": 10.45, "end": 13.40, "lines": [
        {"text": "КАЛЕНДАРЬ СОКРАЩАЕТСЯ", "accent": False, "size": "small"},
        {"text": "БЫСТРЕЕ", "accent": True, "size": "big"},
    ]},
    {"start": 13.45, "end": 15.65, "lines": [
        {"text": "ОЧЕРЕДНАЯ", "accent": False, "size": "small"},
        {"text": "ОТГОВОРКА", "accent": True, "size": "big"},
    ]},
    {"start": 15.70, "end": 17.80, "lines": [
        {"text": "КАЖДЫЙ ВЕЧЕР", "accent": False, "size": "small"},
        {"text": "ОТКРЫЛ ТРЕНАЖЁР", "accent": True, "size": "big"},
    ]},
    {"start": 17.85, "end": 19.55, "lines": [
        {"text": "ВМЕСТО", "accent": False, "size": "small"},
        {"text": "САМООБМАНА", "accent": True, "size": "big"},
    ]},
    {"start": 19.60, "end": 22.55, "lines": [
        {"text": "ЧЕСТНО ПОСМОТРЕЛ", "accent": False, "size": "small"},
        {"text": "ДО МАЯ", "accent": True, "size": "big"},
    ]},
    {"start": 22.65, "end": 24.76, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
e_emphasis = [
    {"start": 7.86, "end": 7.98},
    {"start": 11.64, "end": 12.12},
    {"start": 22.32, "end": 22.44},
]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (v3_2160p): stopped fearing error statistics
# ---------------------------------------------------------------------------
f_intro = {"lines": ["БОИШЬСЯ СВОИХ", "ОШИБОК?"], "end": 2.3}
f_cards = [
    {"start": 3.55, "end": 6.35, "lines": [
        {"text": "БУДТО ЦИФРЫ", "accent": False, "size": "small"},
        {"text": "ДЕЛАЮТ ХУЖЕ", "accent": True, "size": "big"},
    ]},
    {"start": 6.45, "end": 8.75, "lines": [
        {"text": "ПРОСТЫМ", "accent": False, "size": "small"},
        {"text": "ФАКТОМ ПРОСМОТРА", "accent": True, "size": "big"},
    ]},
    {"start": 8.80, "end": 10.65, "lines": [
        {"text": "ЗАСТАВИЛ СЕБЯ", "accent": False, "size": "small"},
        {"text": "ПОСМОТРЕТЬ", "accent": True, "size": "big"},
    ]},
    {"start": 10.70, "end": 13.40, "lines": [
        {"text": "ОШИБКИ", "accent": False, "size": "small"},
        {"text": "КОНКРЕТНЫЕ", "accent": True, "size": "big"},
    ]},
    {"start": 13.50, "end": 16.15, "lines": [
        {"text": "А НЕ ПРИЗНАК", "accent": False, "size": "small"},
        {"text": "КРАХА", "accent": True, "size": "big"},
    ]},
    {"start": 16.30, "end": 17.55, "lines": [
        {"text": "В ЕГЭ ТРЕНАЖЁРЕ", "accent": False, "size": "small"},
        {"text": "ТЕПЕРЬ", "accent": True, "size": "big"},
    ]},
    {"start": 17.60, "end": 19.30, "lines": [
        {"text": "ОТКРЫВАЮ", "accent": False, "size": "small"},
        {"text": "КАЖДЫЙ ВЕЧЕР", "accent": True, "size": "big"},
    ]},
    {"start": 19.35, "end": 20.20, "lines": [
        {"text": "БЕЗ СТРАХА", "accent": True, "size": "big"},
    ]},
    {"start": 20.30, "end": 22.85, "lines": [
        {"text": "НЕ ВРАГ", "accent": False, "size": "small"},
        {"text": "А ИНСТРУМЕНТ", "accent": True, "size": "big"},
    ]},
    {"start": 22.95, "end": 24.92, "lines": [
        {"text": "ССЫЛКА", "accent": True, "size": "big"},
        {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"},
    ]},
]
f_emphasis = [
    {"start": 2.55, "end": 2.82},
    {"start": 6.09, "end": 6.21},
    {"start": 22.20, "end": 22.77},
]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
