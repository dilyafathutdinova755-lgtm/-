#!/usr/bin/env python3
"""One-off authoring + validation script for the ELEVENTH 'coffee123' batch
(9 episodes uploaded under the same tag after ten prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes54/.

Three returning hosts this time (gray-bedroom boy, curly-haired boy - now
filmed in a new daylight bookshelf/desk room instead of the sunset window,
and the girl with the bookshelf/desk) - no sunset-window scene or parent
host in this drop. New sub-theme: several episodes are framed from a camp
counselor's ("вожатый") point of view managing their assigned group's EGE
prep during a camp/retreat, alongside returning fishing-trip episodes and
olympiad-prep episodes. Content: auto-grouping term flashcards by topic
instead of manual folder sorting, a confusable-concept drill that shows a
statement instead of asking "what is this", preloading a task into an
offline tab before losing signal between competition rounds, a solving-speed
arrow comparing today to a week ago, a whole-troop leaderboard instead of a
personal-friends-only one, a muted text walkthrough for a fishing trip, no
extra payment for advanced-difficulty tasks, one shared daily task visible
to the whole camp shift, and a single number showing the gap between your
best and worst subject.
"""
import json

REAL_DURATION = {
    "a": 27.991, "b": 25.922, "c": 30.960,
    "d": 31.020, "e": 23.340, "f": 25.560,
    "g": 30.295, "h": 22.000, "i": 29.040,
}
SOURCE_FILE = {
    "a": "18_09___1_2160p1111", "b": "18_09___1_2160p1111111", "c": "18_09___1_2160p11111111",
    "d": "18_09___2_2160p1111111", "e": "18_09___2_2160p2222", "f": "18_09___2_2160p22222222",
    "g": "18_09___3_2160p111111", "h": "18_09___3_2160p3333", "i": "18_09___3_2160p3333333",
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
    """Repair known sherpa-onnx ASR mis-transcriptions before captioning.
    Same pattern used for the recurring 'одиннадцатиклассники' split and
    stray-fragment merges in every prior batch."""
    if letter == "b":
        for w in words:
            if abs(w["start"] - 0.60) < 0.02 and w["text"] == "одинндцатиклассники":
                w["text"] = "одиннадцатиклассники"
    elif letter == "g":
        fixed = []
        for w in words:
            if abs(w["start"] - 3.51) < 0.02 and w["text"] == "зазадание":
                fixed.append({"text": "за", "start": 3.51, "end": 3.65})
                fixed.append({"text": "задание", "start": 3.65, "end": 3.90})
            elif abs(w["start"] - 7.56) < 0.02 and w["text"] == "егает":
                fixed.append({"text": "егэ", "start": w["start"], "end": w["end"]})
            elif abs(w["start"] - 14.91) < 0.02 and w["text"] == "г":
                fixed.append({"text": "егэ", "start": 14.91, "end": 15.12})
            else:
                fixed.append(w)
        words = fixed
    elif letter == "i":
        fixed = []
        skip_next = False
        for i, w in enumerate(words):
            if skip_next:
                skip_next = False
                continue
            if abs(w["start"] - 0.63) < 0.02 and w["text"] == "один" and words[i + 1]["text"] == "цатиклассники":
                fixed.append({"text": "одиннадцатиклассники", "start": w["start"], "end": words[i + 1]["end"]})
                skip_next = True
            else:
                fixed.append(w)
        words = fixed
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_11/{src}_words.json"))
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
# Episode A (gray-boy as camp counselor, 27.991s): manually sorting EGE term
# flashcards by topic between troop duties; the app groups cards by topic on
# its own, pre-assembled before the app even opens
# ---------------------------------------------------------------------------
a_intro = {"lines": ["РАСКЛАДЫВАЕШЬ КАРТОЧКИ", "МЕЖДУ ДЕЛАМИ?"], "end": 2.3}
a_cards = [
    {"start": 2.43, "end": 3.99, "lines": [{"text": "РАСКЛАДЫВАЕШЬ", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 4.14, "end": 5.97, "lines": [{"text": "ЕГЭ ПО ТЕМАМ", "accent": False, "size": "small"}, {"text": "МЕЖДУ ДЕЛАМИ", "accent": True, "size": "big"}]},
    {"start": 6.36, "end": 7.44, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ГРУППИРУЕТ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.79, "lines": [{"text": "КАРТОЧКИ В НАБОР", "accent": False, "size": "small"}, {"text": "ПО ТЕМЕ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 9.84, "lines": [{"text": "САМ БЕЗ", "accent": False, "size": "small"}, {"text": "РУЧНОЙ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 10.92, "lines": [{"text": "СОРТИРОВКИ", "accent": False, "size": "small"}, {"text": "ПО ПАПКАМ", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 12.27, "lines": [{"text": "НАБОР ПОД", "accent": False, "size": "small"}, {"text": "КОНКРЕТНУЮ ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 12.42, "end": 13.32, "lines": [{"text": "СОБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 13.62, "end": 14.94, "lines": [{"text": "ЕЩЕ ДО", "accent": False, "size": "small"}, {"text": "ОТКРЫТИЯ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.83, "lines": [{"text": "РАСКЛАДЫВАТЬ КАРТОЧКИ", "accent": False, "size": "small"}, {"text": "МЕЖДУ ДЕЛАМИ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 18.06, "lines": [{"text": "ПО ТЕМАМ", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 19.44, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ИСКАТЬ", "accent": True, "size": "big"}]},
    {"start": 19.59, "end": 20.94, "lines": [{"text": "НУЖНУЮ ПАПКУ", "accent": False, "size": "small"}, {"text": "СРЕДИ ДЕСЯТКОВ", "accent": True, "size": "big"}]},
    {"start": 21.12, "end": 22.29, "lines": [{"text": "ВРУЧНУЮ НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 22.56, "end": 24.30, "lines": [{"text": "КАРТОЧКИ ГРУППИРУЮТСЯ ПО ТЕМЕ", "accent": False, "size": "small"}, {"text": "САМИ", "accent": True, "size": "big"}]},
    {"start": 24.51, "end": 25.98, "lines": [{"text": "БЕЗ РУЧНОЙ", "accent": False, "size": "small"}, {"text": "РАСКЛАДКИ", "accent": True, "size": "big"}]},
    {"start": 26.22, "end": 27.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.43, "end": 2.88}, {"start": 12.42, "end": 12.78}, {"start": 22.95, "end": 23.46}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (curly-boy, new daylight room, 25.922s): confusing two similar
# social-studies concepts that both fit the same description; the app shows
# a statement and asks which of the two it belongs to, instead of asking
# "what is this" directly
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПУТАЕШЬ ДВА", "ПОХОЖИХ ПОНЯТИЯ?"], "end": 2.3}
b_cards = [
    {"start": 2.94, "end": 4.62, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "В ЗАДАНИИ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 6.45, "lines": [{"text": "ЕСЛИ ОБА ПОДХОДЯТ ПОД ОБЩЕЕ", "accent": False, "size": "small"}, {"text": "ОПИСАНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 7.44, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.54, "lines": [{"text": "УТВЕРЖДЕНИЕ И", "accent": False, "size": "small"}, {"text": "ПРОСИТ", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 10.56, "lines": [{"text": "ОПРЕДЕЛИТЬ", "accent": False, "size": "small"}, {"text": "К КАКОМУ", "accent": True, "size": "big"}]},
    {"start": 10.68, "end": 11.73, "lines": [{"text": "ИЗ ДВУХ", "accent": False, "size": "small"}, {"text": "ПОХОЖИХ ПОНЯТИЙ", "accent": True, "size": "big"}]},
    {"start": 12.03, "end": 13.20, "lines": [{"text": "ОНО ОТНОСИТСЯ", "accent": False, "size": "small"}, {"text": "ПРЯМОГО", "accent": True, "size": "big"}]},
    {"start": 13.32, "end": 14.37, "lines": [{"text": "ВОПРОСА ЧТО", "accent": False, "size": "small"}, {"text": "ЭТО ЗДЕСЬ", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 15.48, "lines": [{"text": "НЕ ЗАДАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.62, "lines": [{"text": "УТВЕРЖДЕНИЕ", "accent": False, "size": "small"}, {"text": "ДЛЯ ВЫБОРА", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 17.94, "lines": [{"text": "НОВОЕ УТВЕРЖДЕНИЕ", "accent": False, "size": "small"}, {"text": "ЧАЩЕ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 19.08, "lines": [{"text": "КАСАЕТСЯ ТЕХ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЙ", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.28, "lines": [{"text": "ГДЕ УЖЕ БЫЛА", "accent": False, "size": "small"}, {"text": "ПУТАНИЦА", "accent": True, "size": "big"}]},
    {"start": 20.55, "end": 22.11, "lines": [{"text": "ОПРЕДЕЛЯЕТСЯ ПО УТВЕРЖДЕНИЮ", "accent": False, "size": "small"}, {"text": "ПОНЯТИЕ", "accent": True, "size": "big"}]},
    {"start": 22.35, "end": 23.88, "lines": [{"text": "А НЕ ПО", "accent": False, "size": "small"}, {"text": "ПРЯМОМУ ВОПРОСУ", "accent": True, "size": "big"}]},
    {"start": 24.15, "end": 25.77, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.59, "end": 2.43}, {"start": 9.66, "end": 10.02}, {"start": 19.92, "end": 20.28}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (girl-bookshelf, 30.960s): at an olympiad, there's often no
# signal exactly when a task needs solving between rounds; the app preloads
# the task into a separate tab beforehand at home, opening offline anytime
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НЕТ СВЯЗИ", "МЕЖДУ ТУРАМИ?"], "end": 2.3}
c_cards = [
    {"start": 2.76, "end": 3.99, "lines": [{"text": "ОКАЗЫВАЕШЬСЯ ТАМ", "accent": False, "size": "small"}, {"text": "ЧАСТО", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 5.73, "lines": [{"text": "НЕТ СВЯЗИ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.94, "end": 7.53, "lines": [{"text": "НУЖНО РЕШИТЬ", "accent": False, "size": "small"}, {"text": "ИМЕННО СЕЙЧАС", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 8.90, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "ТУРАМИ", "accent": True, "size": "big"}]},
    {"start": 9.36, "end": 10.59, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВЫГРУЖАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.74, "end": 11.91, "lines": [{"text": "ЗАДАНИЕ В", "accent": False, "size": "small"}, {"text": "ВКЛАДКУ", "accent": True, "size": "big"}]},
    {"start": 12.24, "end": 13.74, "lines": [{"text": "НА ПОТОМ", "accent": False, "size": "small"}, {"text": "ОДНИМ СВАЙПОМ", "accent": True, "size": "big"}]},
    {"start": 14.04, "end": 15.54, "lines": [{"text": "ЕЩЕ ДОМА", "accent": False, "size": "small"}, {"text": "ВКЛАДКА", "accent": True, "size": "big"}]},
    {"start": 15.69, "end": 16.62, "lines": [{"text": "ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "БЕЗ СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 16.80, "end": 18.48, "lines": [{"text": "В ЛЮБОЙ МОМЕНТ", "accent": False, "size": "small"}, {"text": "ХОТЬ В ПЕРЕРЫВЕ", "accent": True, "size": "big"}]},
    {"start": 18.57, "end": 20.46, "lines": [{"text": "МЕЖДУ ТУРАМИ", "accent": False, "size": "small"}, {"text": "ИСКАТЬ СЕТЬ", "accent": True, "size": "big"}]},
    {"start": 20.55, "end": 21.99, "lines": [{"text": "СПЕЦИАЛЬНО РАДИ", "accent": False, "size": "small"}, {"text": "ОДНОГО ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 22.26, "end": 24.24, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 24.42, "end": 26.01, "lines": [{"text": "ИЗ ВКЛАДКИ ОТКРЫВАЮТСЯ", "accent": False, "size": "small"}, {"text": "ПОТОМ", "accent": True, "size": "big"}]},
    {"start": 26.22, "end": 27.33, "lines": [{"text": "БЕЗ СВЯЗИ", "accent": False, "size": "small"}, {"text": "В ЛЮБОЙ МОМЕНТ", "accent": True, "size": "big"}]},
    {"start": 27.54, "end": 28.95, "lines": [{"text": "МЕЖДУ", "accent": False, "size": "small"}, {"text": "ТУРАМИ", "accent": True, "size": "big"}]},
    {"start": 28.95, "end": 30.72, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.23, "end": 4.68}, {"start": 10.20, "end": 10.59}, {"start": 20.55, "end": 21.00}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (girl-bookshelf, 31.020s): unsure whether solving EGE tasks got
# faster than a week ago; the app compares today's average speed to a week
# ago as one arrow up or down, updated automatically after every task
# ---------------------------------------------------------------------------
d_intro = {"lines": ["БЫСТРЕЕ ЛИ РЕШАЕШЬ", "ЧЕМ НЕДЕЛЮ НАЗАД?"], "end": 2.3}
d_cards = [
    {"start": 2.82, "end": 4.32, "lines": [{"text": "НЕ ПОНИМАЕШЬ", "accent": False, "size": "small"}, {"text": "СТАЛИ ЛИ", "accent": True, "size": "big"}]},
    {"start": 4.47, "end": 6.42, "lines": [{"text": "РЕШАТЬ ЗАДАНИЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "БЫСТРЕЕ", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.43, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СРАВНИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.61, "end": 9.72, "lines": [{"text": "СРЕДНЮЮ", "accent": False, "size": "small"}, {"text": "СКОРОСТЬ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 11.16, "lines": [{"text": "СЕГОДНЯ СО", "accent": False, "size": "small"}, {"text": "СКОРОСТЬЮ", "accent": True, "size": "big"}]},
    {"start": 11.37, "end": 13.11, "lines": [{"text": "НЕДЕЛЮ НАЗАД", "accent": False, "size": "small"}, {"text": "ОДНОЙ СТРЕЛКОЙ", "accent": True, "size": "big"}]},
    {"start": 13.23, "end": 14.10, "lines": [{"text": "ВВЕРХ ИЛИ", "accent": False, "size": "small"}, {"text": "ВНИЗ", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 15.99, "lines": [{"text": "СТРЕЛКА ОБНОВЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.67, "lines": [{"text": "ПОСЛЕ КАЖДОГО", "accent": False, "size": "small"}, {"text": "ЗАКРЫТОГО", "accent": True, "size": "big"}]},
    {"start": 18.00, "end": 18.96, "lines": [{"text": "БЕЗ РУЧНЫХ", "accent": False, "size": "small"}, {"text": "ПОДСЧЕТОВ", "accent": True, "size": "big"}]},
    {"start": 19.77, "end": 20.61, "lines": [{"text": "НАПРАВЛЕНИЕ", "accent": False, "size": "small"}, {"text": "СТРЕЛКИ", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 22.47, "lines": [{"text": "ПОНЯТНО СРАЗУ", "accent": False, "size": "small"}, {"text": "БЕЗ ИЗУЧЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 22.62, "end": 23.76, "lines": [{"text": "ГРАФИКА ИЛИ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦЫ", "accent": True, "size": "big"}]},
    {"start": 23.91, "end": 25.50, "lines": [{"text": "ЦИФР", "accent": False, "size": "small"}, {"text": "СКОРОСТЬ РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 25.68, "end": 27.18, "lines": [{"text": "ЗАДАНИЯ ВИДНА", "accent": False, "size": "small"}, {"text": "ОДНОЙ СТРЕЛКОЙ", "accent": True, "size": "big"}]},
    {"start": 27.60, "end": 28.50, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ТАБЛИЦЕЙ ЦИФР", "accent": True, "size": "big"}]},
    {"start": 29.22, "end": 30.84, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.97, "end": 3.33}, {"start": 15.24, "end": 15.69}, {"start": 26.16, "end": 26.34}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (gray-boy as camp counselor, 23.340s): comparing prep only with
# personal friends instead of the whole troop of counselors; the app shows
# one overall rating for the entire troop of counselors, not just friends
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СРАВНИВАЕШЬ ТОЛЬКО", "С ДРУЗЬЯМИ?"], "end": 2.3}
e_cards = [
    {"start": 2.46, "end": 3.66, "lines": [{"text": "СРАВНИВАЕШЬ", "accent": False, "size": "small"}, {"text": "ПОДГОТОВКУ К ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.78, "end": 5.25, "lines": [{"text": "ТОЛЬКО С ЛИЧНЫМИ", "accent": False, "size": "small"}, {"text": "ДРУЗЬЯМИ", "accent": True, "size": "big"}]},
    {"start": 5.37, "end": 6.45, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "ОТРЯДОМ ВОЖАТЫХ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 7.44, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СЧИТАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 8.61, "lines": [{"text": "ОБЩИЙ РЕЙТИНГ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.90, "lines": [{"text": "ДЛЯ ВСЕГО", "accent": False, "size": "small"}, {"text": "ОТРЯДА ВОЖАТЫХ", "accent": True, "size": "big"}]},
    {"start": 10.08, "end": 11.34, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ДЛЯ ДРУЗЕЙ", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.32, "lines": [{"text": "МЕСТО ВИДНО", "accent": False, "size": "small"}, {"text": "СРЕДИ ВСЕХ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.49, "lines": [{"text": "В ОБЩИЙ", "accent": False, "size": "small"}, {"text": "СПИСОК СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 14.73, "end": 15.90, "lines": [{"text": "СОБИРАТЬ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНЫЙ СПИСОК", "accent": True, "size": "big"}]},
    {"start": 16.05, "end": 17.25, "lines": [{"text": "ЛИЧНЫХ ДРУЗЕЙ", "accent": False, "size": "small"}, {"text": "ДЛЯ СРАВНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 18.66, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "РЕЙТИНГ", "accent": True, "size": "big"}]},
    {"start": 18.81, "end": 19.86, "lines": [{"text": "ОБЩИЙ ДЛЯ", "accent": False, "size": "small"}, {"text": "ВСЕГО ОТРЯДА", "accent": True, "size": "big"}]},
    {"start": 20.10, "end": 21.27, "lines": [{"text": "А НЕ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ДЛЯ ДРУЗЕЙ", "accent": True, "size": "big"}]},
    {"start": 21.54, "end": 23.16, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 1.92, "end": 2.28}, {"start": 9.60, "end": 9.90}, {"start": 18.81, "end": 19.02}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-boy, new daylight room, 25.560s): can't turn on the sound
# for a video walkthrough while morning fishing without scaring the fish;
# the app's text matches the voiceover word-for-word, readable with the
# phone fully muted
# ---------------------------------------------------------------------------
f_intro = {"lines": ["БОИШЬСЯ ВКЛЮЧИТЬ ЗВУК", "НА РЫБАЛКЕ?"], "end": 2.3}
f_cards = [
    {"start": 2.61, "end": 3.57, "lines": [{"text": "НЕ МОГУТ", "accent": False, "size": "small"}, {"text": "ВКЛЮЧИТЬ ЗВУК", "accent": True, "size": "big"}]},
    {"start": 3.72, "end": 4.74, "lines": [{"text": "ВИДЕОРАЗБОРА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.30, "lines": [{"text": "ЕГЭ ЧТОБЫ", "accent": False, "size": "small"}, {"text": "НЕ СПУГНУТЬ РЫБУ", "accent": True, "size": "big"}]},
    {"start": 6.69, "end": 7.77, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.92, "end": 8.85, "lines": [{"text": "ТЕКСТ РАЗБОРА", "accent": False, "size": "small"}, {"text": "КОТОРЫЙ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 9.99, "lines": [{"text": "СЛОВО В СЛОВО", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.01, "lines": [{"text": "С ГОЛОСОМ", "accent": False, "size": "small"}, {"text": "ЗА КАДРОМ", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.27, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ЧИТАЕТСЯ ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 12.45, "end": 13.77, "lines": [{"text": "ПРИ ПОЛНОСТЬЮ ВЫКЛЮЧЕННОМ", "accent": False, "size": "small"}, {"text": "ЗВУКЕ", "accent": True, "size": "big"}]},
    {"start": 13.95, "end": 14.79, "lines": [{"text": "ТЕЛЕФОНА", "accent": False, "size": "small"}, {"text": "ВКЛЮЧАТЬ", "accent": True, "size": "big"}]},
    {"start": 14.91, "end": 16.02, "lines": [{"text": "ЗВУК РАДИ РАЗБОРА", "accent": False, "size": "small"}, {"text": "НА БЕРЕГУ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.40, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ЧИТАТЬ ТЕКСТ", "accent": True, "size": "big"}]},
    {"start": 17.55, "end": 18.48, "lines": [{"text": "МОЖНО ПРЯМО", "accent": False, "size": "small"}, {"text": "С ЭКРАНА", "accent": True, "size": "big"}]},
    {"start": 18.75, "end": 20.01, "lines": [{"text": "НЕ ПОДНОСЯ", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОН К УХУ", "accent": True, "size": "big"}]},
    {"start": 20.31, "end": 22.05, "lines": [{"text": "РАЗБОР ЧИТАЕТСЯ ПРИ ВЫКЛЮЧЕННОМ", "accent": False, "size": "small"}, {"text": "ЗВУКЕ", "accent": True, "size": "big"}]},
    {"start": 22.38, "end": 23.43, "lines": [{"text": "БЕЗ РИСКА", "accent": False, "size": "small"}, {"text": "СПУГНУТЬ РЫБУ", "accent": True, "size": "big"}]},
    {"start": 23.70, "end": 25.32, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.64, "end": 5.97}, {"start": 13.08, "end": 13.47}, {"start": 22.83, "end": 23.16}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (girl-bookshelf, 30.295s): used to paying extra for
# advanced-difficulty tasks in olympiad compilations; the app opens tasks of
# any difficulty level with no extra payment for the advanced tier
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ПЛАТИШЬ ЗА", "СЛОЖНЫЕ ЗАДАНИЯ?"], "end": 2.3}
g_cards = [
    {"start": 2.46, "end": 3.36, "lines": [{"text": "ДОПЛАЧИВАТЬ", "accent": False, "size": "small"}, {"text": "ПРИВЫКЛИ", "accent": True, "size": "big"}]},
    {"start": 3.51, "end": 5.25, "lines": [{"text": "ЗА ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОВЫШЕННОЙ", "accent": True, "size": "big"}]},
    {"start": 5.55, "end": 6.60, "lines": [{"text": "СЛОЖНОСТИ В", "accent": False, "size": "small"}, {"text": "СБОРНИКАХ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.76, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.91, "end": 9.72, "lines": [{"text": "ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ЛЮБОГО", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 10.74, "lines": [{"text": "УРОВНЯ", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТИ", "accent": True, "size": "big"}]},
    {"start": 11.28, "end": 12.99, "lines": [{"text": "БЕЗ ДОПЛАТЫ ЗА УГЛУБЛЕННЫЙ", "accent": False, "size": "small"}, {"text": "УРОВЕНЬ", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 15.12, "lines": [{"text": "СЛОЖНЫЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ПО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.65, "lines": [{"text": "ДОСТУПНЫ", "accent": False, "size": "small"}, {"text": "В ДОСТУПЕ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 18.84, "lines": [{"text": "ЧТО И ПРОСТЫЕ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 20.61, "lines": [{"text": "ПЛАТНЫЙ РАЗДЕЛ ДЛЯ ПРОДВИНУТОГО", "accent": False, "size": "small"}, {"text": "УРОВНЯ", "accent": True, "size": "big"}]},
    {"start": 20.82, "end": 22.38, "lines": [{"text": "ПРОСТО НЕ ПРЕДУСМОТРЕН", "accent": False, "size": "small"}, {"text": "ЗДЕСЬ", "accent": True, "size": "big"}]},
    {"start": 23.22, "end": 24.09, "lines": [{"text": "УГЛУБЛЕННЫЙ", "accent": False, "size": "small"}, {"text": "УРОВЕНЬ", "accent": True, "size": "big"}]},
    {"start": 24.24, "end": 25.71, "lines": [{"text": "ЗАДАНИЙ НЕ", "accent": False, "size": "small"}, {"text": "ТРЕБУЕТ ДОПЛАТЫ", "accent": True, "size": "big"}]},
    {"start": 25.92, "end": 27.75, "lines": [{"text": "В ОТЛИЧИЕ ОТ ОЛИМПИАДНЫХ", "accent": False, "size": "small"}, {"text": "СБОРНИКОВ", "accent": True, "size": "big"}]},
    {"start": 28.47, "end": 30.12, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.91, "end": 3.36}, {"start": 18.45, "end": 18.84}, {"start": 21.78, "end": 22.38}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (gray-boy as camp counselor, 22.000s): asking around the shift
# who already closed the day's shared task; the app gives one shared daily
# task for the whole camp shift that anyone can close
# ---------------------------------------------------------------------------
h_intro = {"lines": ["СПРАШИВАЕШЬ ПО КРУГУ", "КТО РЕШИЛ?"], "end": 2.3}
h_cards = [
    {"start": 2.37, "end": 3.57, "lines": [{"text": "ВСПОМИНАЮТ", "accent": False, "size": "small"}, {"text": "КТО ИЗ СМЕНА", "accent": True, "size": "big"}]},
    {"start": 3.69, "end": 4.92, "lines": [{"text": "УЖЕ ЗАКРЫЛ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 5.13, "end": 6.54, "lines": [{"text": "ДНЯ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 8.04, "lines": [{"text": "ДАЕТ ОДНО", "accent": False, "size": "small"}, {"text": "ОБЩЕЕ ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.19, "end": 9.06, "lines": [{"text": "ДНЯ ДЛЯ", "accent": False, "size": "small"}, {"text": "ВСЕЙ СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.56, "lines": [{"text": "ВОЖАТЫХ СРАЗУ", "accent": False, "size": "small"}, {"text": "ЗАКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 10.68, "end": 11.67, "lines": [{"text": "МОЖЕТ", "accent": False, "size": "small"}, {"text": "ЛЮБОЙ ИЗ СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 11.91, "end": 13.29, "lines": [{"text": "А НЕ СТРОГО", "accent": False, "size": "small"}, {"text": "КАЖДЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.59, "end": 15.42, "lines": [{"text": "УТОЧНЯТЬ ПО КРУГУ", "accent": False, "size": "small"}, {"text": "КТО РЕШИЛ", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 16.86, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ОБЩЕЕ", "accent": True, "size": "big"}]},
    {"start": 16.92, "end": 17.91, "lines": [{"text": "ЗАДАНИЕ ДНЯ", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 18.09, "end": 20.07, "lines": [{"text": "ЛЮБОЙ ИЗ СМЕНЫ", "accent": False, "size": "small"}, {"text": "БЕЗ УТОЧНЕНИЙ", "accent": True, "size": "big"}]},
    {"start": 20.31, "end": 21.84, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 2.37, "end": 2.73}, {"start": 10.11, "end": 10.35}, {"start": 17.61, "end": 17.91}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (curly-boy, new daylight room, 29.040s): not sure how far one
# subject lags behind the strongest one; the app shows the gap between the
# best and worst subject as a single number on the main screen
# ---------------------------------------------------------------------------
i_intro = {"lines": ["НЕ ЗНАЕШЬ НАСКОЛЬКО", "ОТСТАЕТ ПРЕДМЕТ?"], "end": 2.3}
i_cards = [
    {"start": 2.30, "end": 3.63, "lines": [{"text": "НЕ ПОНИМАЮТ", "accent": False, "size": "small"}, {"text": "НАСКОЛЬКО СИЛЬНО", "accent": True, "size": "big"}]},
    {"start": 3.93, "end": 4.77, "lines": [{"text": "ОДИН ПРЕДМЕТ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 6.42, "lines": [{"text": "ОТСТАЕТ", "accent": False, "size": "small"}, {"text": "ОТ САМОГО", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.95, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.57, "lines": [{"text": "РАЗНИЦУ МЕЖДУ", "accent": False, "size": "small"}, {"text": "ЛУЧШИМ И ХУДШИМ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.01, "lines": [{"text": "ПРЕДМЕТОМ", "accent": False, "size": "small"}, {"text": "ОДНОЙ ЦИФРОЙ", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 12.54, "lines": [{"text": "НА ГЛАВНОМ ЭКРАНЕ", "accent": False, "size": "small"}, {"text": "РАЗНИЦА", "accent": True, "size": "big"}]},
    {"start": 12.69, "end": 14.19, "lines": [{"text": "ВИДНА СРАЗУ", "accent": False, "size": "small"}, {"text": "БЕЗ СРАВНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 14.34, "end": 15.63, "lines": [{"text": "ПРЕДМЕТОВ ПО ОТДЕЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "ВСЕХ", "accent": True, "size": "big"}]},
    {"start": 15.93, "end": 17.16, "lines": [{"text": "ПОНИМАТЬ МАСШТАБ", "accent": False, "size": "small"}, {"text": "ОТСТАВАНИЯ", "accent": True, "size": "big"}]},
    {"start": 17.34, "end": 18.21, "lines": [{"text": "ПО ОЩУЩЕНИЮ", "accent": False, "size": "small"}, {"text": "БОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 18.36, "end": 19.56, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАТЬ", "accent": True, "size": "big"}]},
    {"start": 19.68, "end": 21.06, "lines": [{"text": "ОТДЕЛЬНУЮ ТАБЛИЦУ", "accent": False, "size": "small"}, {"text": "С ПРОЦЕНТАМИ", "accent": True, "size": "big"}]},
    {"start": 21.21, "end": 22.02, "lines": [{"text": "ПО КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 22.32, "end": 23.52, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "РАЗНИЦА", "accent": True, "size": "big"}]},
    {"start": 23.64, "end": 24.69, "lines": [{"text": "МЕЖДУ ЛУЧШИМ И", "accent": False, "size": "small"}, {"text": "ХУДШИМ", "accent": True, "size": "big"}]},
    {"start": 24.78, "end": 26.46, "lines": [{"text": "ПРЕДМЕТОМ", "accent": False, "size": "small"}, {"text": "ВИДНА ОДНОЙ ЦИФРОЙ", "accent": True, "size": "big"}]},
    {"start": 27.15, "end": 28.86, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 4.98, "end": 5.28}, {"start": 16.32, "end": 16.59}, {"start": 23.25, "end": 23.52}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
