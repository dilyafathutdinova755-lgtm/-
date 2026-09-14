#!/usr/bin/env python3
"""One-off authoring + validation script for the TENTH 'coffee123' batch
(3 episodes uploaded under the same tag after nine prior batches were
delivered - a smaller drop than usual). Not a generic tool: hand-picked
timings/text per episode. Run from remotion/episodes53/.

A brand-new host this time: an adult woman (parent persona), same
bookshelf-lined room across all three clips - no returning student hosts
in this drop. Content is framed from the parent's point of view watching
their eleventh-grader ("родители одиннадцатиклассников замечают/понимают/
видят что..."), which fits the brand's stated audience (CLAUDE.md 1.1:
"школьники 10-11 класса и их родители"). Themes: offline task access at
the country house once the bank is cached, mistakes made on paper staying
saved in-app instead of vanishing the moment they're corrected, and the
app replacing a nightly persuasion argument with a one-tap suggested task
whose status the parent can see without asking.
"""
import json

REAL_DURATION = {
    "a": 25.922, "b": 24.172, "c": 28.674,
}
SOURCE_FILE = {
    "a": "14_09___1_2160p111111111", "b": "14_09___2_2160p2222222222", "c": "14_09___3_2160p333333333",
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
    words = json.load(open(f"../asr_coffee123_10/{src}_words.json"))
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
# Episode A (parent host, 25.922s): at the country house without a router
# the kid puts off the EGE task until back in the city; the app copies the
# FIPI bank to the phone at the last connection at home, so no connection
# is needed after that at all
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ОТКЛАДЫВАЕТ ЕГЭ", "БЕЗ РОУТЕРА?"], "end": 2.3}
a_cards = [
    {"start": 2.73, "end": 4.08, "lines": [{"text": "В ЗАГОРОДНОМ ДОМЕ", "accent": False, "size": "small"}, {"text": "БЕЗ РОУТЕРА", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 5.88, "lines": [{"text": "РЕБЕНОК ОТКЛАДЫВАЕТ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 7.05, "lines": [{"text": "ДО ВОЗВРАЩЕНИЯ", "accent": False, "size": "small"}, {"text": "В ГОРОД", "accent": True, "size": "big"}]},
    {"start": 7.74, "end": 9.09, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "КОПИРУЕТ БАНК", "accent": True, "size": "big"}]},
    {"start": 9.24, "end": 10.29, "lines": [{"text": "ФИПИ В ПАМЯТЬ", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОНА", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.91, "lines": [{"text": "ПРИ ПОСЛЕДНЕМ ПОДКЛЮЧЕНИИ", "accent": False, "size": "small"}, {"text": "ДОМА", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.14, "lines": [{"text": "И ДАЛЬШЕ СВЯЗЬ", "accent": False, "size": "small"}, {"text": "ДЛЯ РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.94, "lines": [{"text": "ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "НЕ ТРЕБУЕТСЯ ВООБЩЕ", "accent": True, "size": "big"}]},
    {"start": 15.54, "end": 16.41, "lines": [{"text": "ЗАГОРОДНЫЙ ДОМ", "accent": False, "size": "small"}, {"text": "НИЧЕМ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 18.06, "lines": [{"text": "НЕ ОТЛИЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "ОТ КВАРТИРЫ", "accent": True, "size": "big"}]},
    {"start": 18.18, "end": 19.32, "lines": [{"text": "ДЛЯ САМОГО", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 19.89, "end": 20.76, "lines": [{"text": "ВОЗВРАЩЕНИЕ", "accent": False, "size": "small"}, {"text": "В ГОРОД", "accent": True, "size": "big"}]},
    {"start": 20.91, "end": 23.64, "lines": [{"text": "ПЕРЕСТАЕТ БЫТЬ", "accent": False, "size": "small"}, {"text": "УСЛОВИЕМ", "accent": True, "size": "big"}]},
    {"start": 24.12, "end": 25.80, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 4.62, "end": 5.04}, {"start": 15.54, "end": 15.93}, {"start": 20.91, "end": 21.24}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (parent host, 24.172s): the kid fixes a mistake on paper and
# instantly forgets it; the app saves the wrong answer together with the
# task itself, not just the corrected version on top, so it can be revisited
# any time before the exam
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ИСПРАВИЛ И ЗАБЫЛ", "ОШИБКУ НА БУМАГЕ?"], "end": 2.3}
b_cards = [
    {"start": 2.52, "end": 3.87, "lines": [{"text": "РЕБЕНОК ИСПРАВЛЯЕТ", "accent": False, "size": "small"}, {"text": "ОШИБКУ", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.16, "lines": [{"text": "В ЗАДАНИИ ЕГЭ", "accent": False, "size": "small"}, {"text": "НА БУМАГЕ", "accent": True, "size": "big"}]},
    {"start": 5.46, "end": 6.36, "lines": [{"text": "И ТУТ ЖЕ", "accent": False, "size": "small"}, {"text": "НАПРОЧЬ", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 7.25, "lines": [{"text": "ОНИ", "accent": False, "size": "small"}, {"text": "ЗАБЫВАЮТ", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 8.85, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СОХРАНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 10.02, "lines": [{"text": "НЕВЕРНЫЙ ОТВЕТ", "accent": False, "size": "small"}, {"text": "ВМЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.19, "lines": [{"text": "С САМИМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 11.28, "end": 12.51, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ВЕРСИЮ", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 13.95, "lines": [{"text": "ПОВЕРХ НЕГО", "accent": False, "size": "small"}, {"text": "ВЕРНУТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 14.04, "end": 14.97, "lines": [{"text": "К ТАКОМУ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЮ", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 16.44, "lines": [{"text": "ЧЕРЕЗ ДЕНЬ", "accent": False, "size": "small"}, {"text": "ЧЕРЕЗ НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 18.09, "lines": [{"text": "ИЛИ ПРЯМО ПЕРЕД", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНОМ", "accent": True, "size": "big"}]},
    {"start": 18.57, "end": 19.71, "lines": [{"text": "ЗАБЫТАЯ НА БУМАГЕ", "accent": False, "size": "small"}, {"text": "ОШИБКА", "accent": True, "size": "big"}]},
    {"start": 19.83, "end": 21.90, "lines": [{"text": "ОСТАЕТСЯ В", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 22.35, "end": 24.03, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.09, "end": 3.87}, {"start": 6.78, "end": 7.11}, {"start": 19.47, "end": 19.71}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (parent host, 28.674s): getting the kid to sit down for the EGE
# only happens after a long persuasion talk; the app suggests a short task
# for today the moment it opens, and the parent can see the task and its
# status right in the app without asking
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ДОЛГИЙ РАЗГОВОР", "ЧТОБЫ СЕЛ ЗА ЕГЭ?"], "end": 2.3}
c_cards = [
    {"start": 2.52, "end": 3.78, "lines": [{"text": "ЗАСТАВИТЬ РЕБЕНКА", "accent": False, "size": "small"}, {"text": "СЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 4.80, "lines": [{"text": "ЗА ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОЛУЧАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.15, "lines": [{"text": "ТОЛЬКО ЧЕРЕЗ", "accent": False, "size": "small"}, {"text": "ДОЛГИЙ РАЗГОВОР", "accent": True, "size": "big"}]},
    {"start": 6.33, "end": 7.20, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "УГОВОРАМИ", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 9.00, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "САМ ПРЕДЛАГАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.12, "end": 10.20, "lines": [{"text": "КОРОТКОЕ ДЕЛО", "accent": False, "size": "small"}, {"text": "НА СЕГОДНЯ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 11.88, "lines": [{"text": "СРАЗУ ПРИ", "accent": False, "size": "small"}, {"text": "ОТКРЫТИИ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.23, "lines": [{"text": "БЕЗ ВСЯКОГО", "accent": False, "size": "small"}, {"text": "РАЗГОВОРА", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.85, "lines": [{"text": "СО ВЗРОСЛЫМИ", "accent": False, "size": "small"}, {"text": "ДЕЛО", "accent": True, "size": "big"}]},
    {"start": 14.97, "end": 15.96, "lines": [{"text": "МЕНЯЕТСЯ НА", "accent": False, "size": "small"}, {"text": "СЛЕДУЮЩЕЕ", "accent": True, "size": "big"}]},
    {"start": 16.02, "end": 17.52, "lines": [{"text": "КАК ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ЗАКРЫТО", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 19.11, "lines": [{"text": "ДЕЛО И ЕГО", "accent": False, "size": "small"}, {"text": "СТАТУС", "accent": True, "size": "big"}]},
    {"start": 19.26, "end": 20.19, "lines": [{"text": "ВИДНО", "accent": False, "size": "small"}, {"text": "РОДИТЕЛЮ ПРЯМО", "accent": True, "size": "big"}]},
    {"start": 20.28, "end": 21.60, "lines": [{"text": "В ПРИЛОЖЕНИИ", "accent": False, "size": "small"}, {"text": "БЕЗ ПЕРЕСКАЗА", "accent": True, "size": "big"}]},
    {"start": 21.72, "end": 22.62, "lines": [{"text": "ОТДЕЛЬНОГО", "accent": False, "size": "small"}, {"text": "ВЕЧЕРОМ", "accent": True, "size": "big"}]},
    {"start": 23.31, "end": 24.45, "lines": [{"text": "ДОЛГИЙ РАЗГОВОР", "accent": False, "size": "small"}, {"text": "С УГОВОРАМИ", "accent": True, "size": "big"}]},
    {"start": 24.54, "end": 26.31, "lines": [{"text": "ЗАМЕНЯЕТСЯ ОДНИМ", "accent": False, "size": "small"}, {"text": "ОТКРЫТИЕМ", "accent": True, "size": "big"}]},
    {"start": 26.82, "end": 28.50, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 5.55, "end": 6.15}, {"start": 14.97, "end": 15.30}, {"start": 24.54, "end": 24.99}]
process("c", c_cards, c_intro, c_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
