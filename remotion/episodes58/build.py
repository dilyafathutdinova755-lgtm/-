#!/usr/bin/env python3
"""One-off authoring + validation script for the FIFTEENTH 'coffee123'
batch (9 episodes uploaded under the same tag after fourteen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes58/.

Filenames continue the keyboard-mash pattern from batch 14. Three
hosts this time: the returning curly-haired boy (fishing-trip theme),
the living-room boy from batch 14 (camp-counselor theme), and a
genuinely new host - a mother in a book-lined room with a wooden table
(parent-POV theme). Content: pausing a fishing-trip quiz round without
losing points on a signal drop, continuing a saved video walkthrough
from the same second after a connection drop, assigning the task of
the day to a whole camp troop with one button, marking a task-of-the-day
checkbox only on real completion instead of by schedule, capping a
study session at exactly ten term cards before suggesting a break,
excluding offline days from the streak count instead of counting them
as a failure, syncing an offline task bank once on reconnect instead of
a full re-download, a timestamp menu under a video walkthrough to jump
to one step instead of rewatching it whole, and capping a quiz session
at three questions so it can't stretch into a whole evening.
"""
import json

REAL_DURATION = {
    "a": 27.991, "b": 29.400, "c": 28.674,
    "d": 32.800, "e": 29.186, "f": 28.360,
    "g": 30.160, "h": 31.170, "i": 30.960,
}
SOURCE_FILE = {
    "a": "21.0fghfhfhfhfhf", "b": "21.0hfghfhgfhfhfhfgh", "c": "21.0hgfhfhgfhfhgfh",
    "d": "21.fghhhfhfhh", "e": "21.gfhgfhghgf", "f": "21.ghfhghfhfdhd",
    "g": "21fghfhfhgfhgfh", "h": "2fhfhfhfhgfhfh", "i": "2gfhhfhfhfhh",
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
    if letter == "d":
        for w in words:
            if abs(w["start"] - 3.72) < 0.02 and w["text"] == "яга":
                w["text"] = "егэ"
    if letter == "c":
        for w in words:
            if abs(w["start"] - 18.45) < 0.02 and w["text"] == "важатому":
                w["text"] = "вожатому"
    if letter == "h":
        for w in words:
            if abs(w["start"] - 22.38) < 0.02 and w["text"] == "миню":
                w["text"] = "меню"
        new_words = []
        for w in words:
            if abs(w["start"] - 28.11) < 0.02 and w["text"] == "наметку":
                new_words.append({"text": "на", "start": 28.11, "end": 28.20})
                new_words.append({"text": "метку", "start": 28.20, "end": 28.38})
            else:
                new_words.append(w)
        words = new_words
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_15/{src}_words.json"))
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
# Episode A (curly-boy, fishing trip, 27.991s): a random signal drop loses
# points in a short quiz round; the app auto-pauses the round the instant
# the signal drops, no points lost for the disconnect, round resumes from
# the same spot once the connection returns
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ТЕРЯЕШЬ ОЧКИ", "ОТ ОБРЫВА СВЯЗИ?"], "end": 2.25}
a_cards = [
    {"start": 2.28, "end": 3.12, "lines": [{"text": "КОРОТКОЙ ИГРЫ", "accent": False, "size": "small"}, {"text": "ОЧКИ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.41, "lines": [{"text": "ПО ЕГЭ И ЗА", "accent": False, "size": "small"}, {"text": "СЛУЧАЙНОЙ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.64, "lines": [{"text": "ПРОПАЖЕ", "accent": False, "size": "small"}, {"text": "СИГНАЛА", "accent": True, "size": "big"}]},
    {"start": 6.06, "end": 7.83, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР СТАВИТ ИГРУ", "accent": False, "size": "small"}, {"text": "НА ПАУЗУ", "accent": True, "size": "big"}]},
    {"start": 8.13, "end": 9.48, "lines": [{"text": "САМ В МОМЕНТ", "accent": False, "size": "small"}, {"text": "ПРОПАЖИ", "accent": True, "size": "big"}]},
    {"start": 9.81, "end": 11.49, "lines": [{"text": "БЕЗ СПИСАНИЯ ЗА ОБРЫВ СВЯЗИ", "accent": False, "size": "small"}, {"text": "ОЧКОВ", "accent": True, "size": "big"}]},
    {"start": 11.85, "end": 12.99, "lines": [{"text": "ПРОДОЛЖАЕТСЯ", "accent": False, "size": "small"}, {"text": "РАУНД", "accent": True, "size": "big"}]},
    {"start": 13.14, "end": 14.94, "lines": [{"text": "РОВНО С ТОГО ЖЕ МЕСТА ПОСЛЕ ВОЗВРАЩЕНИЯ", "accent": False, "size": "small"}, {"text": "СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 17.19, "lines": [{"text": "НА БЕРЕГУ ТЕРЯТЬ ЗАСЛУЖЕННО НАБРАННЫЕ", "accent": False, "size": "small"}, {"text": "ОЧКИ", "accent": True, "size": "big"}]},
    {"start": 17.37, "end": 18.84, "lines": [{"text": "ИЗ ЗА СЛУЧАЙНОГО ОБРЫВА", "accent": False, "size": "small"}, {"text": "СИГНАЛА", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 20.67, "lines": [{"text": "НЕ ПРИХОДИТСЯ ПАУЗА", "accent": False, "size": "small"}, {"text": "СНИМАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 20.82, "end": 22.74, "lines": [{"text": "САМА КАК ТОЛЬКО СИГНАЛ ВОЗВРАЩАЕТСЯ", "accent": False, "size": "small"}, {"text": "СНОВА", "accent": True, "size": "big"}]},
    {"start": 23.13, "end": 24.69, "lines": [{"text": "ПРОДОЛЖАЕТСЯ С ТОГО ЖЕ", "accent": False, "size": "small"}, {"text": "РАУНД", "accent": True, "size": "big"}]},
    {"start": 24.93, "end": 25.98, "lines": [{"text": "ПОСЛЕ ВОЗВРАТА", "accent": False, "size": "small"}, {"text": "СИГНАЛА", "accent": True, "size": "big"}]},
    {"start": 26.22, "end": 28.08, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.28, "end": 2.61}, {"start": 6.06, "end": 6.39}, {"start": 19.92, "end": 20.25}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (curly-boy, fishing trip, 29.400s): a video walkthrough loses
# its place on a connection drop at the lake shore; the app saves the
# walkthrough to the phone in advance so playback continues from the same
# second even with zero bars, all the way to the end of the trip
# ---------------------------------------------------------------------------
b_intro = {"lines": ["НАЧИНАЕШЬ РАЗБОР", "И ТЕРЯЕШЬ МЕСТО?"], "end": 2.25}
b_cards = [
    {"start": 2.46, "end": 3.84, "lines": [{"text": "НАЧИНАЮТ", "accent": False, "size": "small"}, {"text": "ВИДЕО РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 6.60, "lines": [{"text": "ЗАДАНИЯ ЕГЭ И ТЕРЯЮТ МЕСТО ПРИ ОБРЫВЕ СВЯЗИ НА БЕРЕГУ", "accent": False, "size": "small"}, {"text": "ОЗЕРА", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 9.57, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР СОХРАНЯЕТ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 10.92, "lines": [{"text": "ЦЕЛИКОМ В ПАМЯТЬ", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОНА", "accent": True, "size": "big"}]},
    {"start": 11.04, "end": 13.02, "lines": [{"text": "ЗАРАНЕЕ И ЕЩЕ ДО ВЫЕЗДА НА ДАЛЬНИЙ", "accent": False, "size": "small"}, {"text": "БЕРЕГ", "accent": True, "size": "big"}]},
    {"start": 13.26, "end": 15.42, "lines": [{"text": "ПРОСМОТР ПРОДОЛЖАЕТСЯ С ТОЙ ЖЕ САМОЙ", "accent": False, "size": "small"}, {"text": "СЕКУНДЫ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 17.16, "lines": [{"text": "ДАЖЕ БЕЗ ЕДИНОГО ДЕЛЕНИЯ", "accent": False, "size": "small"}, {"text": "СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 18.45, "lines": [{"text": "НАЧИНАТЬ", "accent": False, "size": "small"}, {"text": "РОЛИК ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 18.63, "end": 20.52, "lines": [{"text": "ПОСЛЕ КАЖДОГО СЛУЧАЙНОГО ОБРЫВА", "accent": False, "size": "small"}, {"text": "СИГНАЛА", "accent": True, "size": "big"}]},
    {"start": 20.73, "end": 22.50, "lines": [{"text": "НЕ ПРИХОДИТСЯ СОХРАНЕННЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 22.62, "end": 24.69, "lines": [{"text": "ОСТАЕТСЯ ДОСТУПЕН ДО САМОГО КОНЦА", "accent": False, "size": "small"}, {"text": "ПОЕЗДКИ", "accent": True, "size": "big"}]},
    {"start": 24.96, "end": 27.30, "lines": [{"text": "ПРОСМОТР ПРОДОЛЖАЕТСЯ С ТОЙ ЖЕ СЕКУНДЫ БЕЗ", "accent": False, "size": "small"}, {"text": "СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 27.57, "end": 29.52, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 2.46, "end": 2.79}, {"start": 15.63, "end": 15.96}, {"start": 27.57, "end": 27.90}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (living-room boy, camp counselor, 28.674s): vожатые assign the
# task of the day one at a time even though the whole troop preps together;
# the app assigns one shared task to the whole troop with one button, the
# combined result collects in one place instead of scattered per-counselor
# ---------------------------------------------------------------------------
c_intro = {"lines": ["НАЗНАЧАЕШЬ ЗАДАНИЕ", "КАЖДОМУ ПО ОДНОМУ?"], "end": 2.19}
c_cards = [
    {"start": 2.31, "end": 3.90, "lines": [{"text": "ЗАДАНИЕ ДНЯ ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "ПООДИНОЧКЕ", "accent": True, "size": "big"}]},
    {"start": 4.08, "end": 6.36, "lines": [{"text": "ХОТЯ ВЕСЬ ОТРЯД ГОТОВИТСЯ ВМЕСТЕ К", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНУ", "accent": True, "size": "big"}]},
    {"start": 6.75, "end": 8.28, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР ПОЗВОЛЯЕТ", "accent": False, "size": "small"}, {"text": "НАЗНАЧИТЬ", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.72, "lines": [{"text": "ОДНО", "accent": False, "size": "small"}, {"text": "ОБЩЕЕ ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 11.82, "lines": [{"text": "СРАЗУ ВСЕМУ ОТРЯДУ", "accent": False, "size": "small"}, {"text": "ОДНОЙ КНОПКОЙ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 14.25, "lines": [{"text": "ОБЩИЙ РЕЗУЛЬТАТ ОТРЯДА СОБИРАЕТСЯ В ОДНОМ", "accent": False, "size": "small"}, {"text": "МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 16.62, "lines": [{"text": "ВМЕСТО РАЗРОЗНЕННЫХ ЛИЧНЫХ ДОСТИЖЕНИЙ", "accent": False, "size": "small"}, {"text": "ВОЖАТЫХ", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 19.65, "lines": [{"text": "НАЗНАЧАТЬ ЗАДАНИЯ ДНЯ КАЖДОМУ ВОЖАТОМУ ОТДЕЛЬНО ПО", "accent": False, "size": "small"}, {"text": "ОДНОМУ", "accent": True, "size": "big"}]},
    {"start": 19.92, "end": 21.48, "lines": [{"text": "НЕ ПРИХОДИТСЯ ОБЩЕЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 21.66, "end": 23.28, "lines": [{"text": "МЕНЯЕТСЯ АВТОМАТИЧЕСКИ НА СЛЕДУЮЩИЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 23.46, "end": 24.54, "lines": [{"text": "СМЕНЫ", "accent": False, "size": "small"}, {"text": "ОБЩИЙ РЕЗУЛЬТАТ", "accent": True, "size": "big"}]},
    {"start": 24.69, "end": 26.10, "lines": [{"text": "ОТРЯДА СОБИРАЕТСЯ В ОДНОМ МЕСТЕ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 26.94, "end": 28.77, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.31, "end": 2.64}, {"start": 6.75, "end": 7.08}, {"start": 26.94, "end": 27.27}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (mother, parent POV, 32.800s): parents think the task of the day
# needs checking on ahead of time, before the whole evening is gone; the app
# only marks the checkbox once the task is actually finished, never just by
# schedule, so an empty box never falsely claims progress
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПРОВЕРЯЕШЬ ЗАДАНИЕ", "ЗАРАНЕЕ ПО РАСПИСАНИЮ?"], "end": 2.0}
d_cards = [
    {"start": 2.04, "end": 5.28, "lines": [{"text": "УВЕРЕНЫ ЧТО ЗАДАНИЯ ДНЯ ПО ЕГЭ НУЖНО КОНТРОЛИРОВАТЬ", "accent": False, "size": "small"}, {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 5.58, "end": 7.02, "lines": [{"text": "ЕЩЕ ДО САМОГО ВЕЧЕРА", "accent": False, "size": "small"}, {"text": "ДОМА", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.21, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ОТМЕЧАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.36, "end": 10.56, "lines": [{"text": "ЗАДАНИЕ ДНЯ ГАЛОЧКОЙ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 13.32, "lines": [{"text": "ПОСЛЕ РЕАЛЬНОГО ЗАВЕРШЕНИЯ А НЕ ЗАРАНЕЕ ПО", "accent": False, "size": "small"}, {"text": "РАСПИСАНИЮ", "accent": True, "size": "big"}]},
    {"start": 13.95, "end": 14.94, "lines": [{"text": "ПУСТАЯ ГАЛОЧКА", "accent": False, "size": "small"}, {"text": "НИЧЕГО", "accent": True, "size": "big"}]},
    {"start": 15.09, "end": 16.83, "lines": [{"text": "НЕ ГОВОРИТ О ТОМ НАЧАТО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 17.01, "end": 18.90, "lines": [{"text": "ПРОЧИТАНО ОНО ИЛИ ПРОПУЩЕНО", "accent": False, "size": "small"}, {"text": "ВОВСЕ", "accent": True, "size": "big"}]},
    {"start": 19.53, "end": 20.85, "lines": [{"text": "ПРОВЕРЯТЬ СТАТУС ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ДНЯ", "accent": True, "size": "big"}]},
    {"start": 20.94, "end": 22.68, "lines": [{"text": "В ТЕЧЕНИЕ ВСЕГО ВЕЧЕРА НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 23.34, "end": 24.57, "lines": [{"text": "ГАЛОЧКА ВОЗНИКАЕТ", "accent": False, "size": "small"}, {"text": "ОДИН РАЗ", "accent": True, "size": "big"}]},
    {"start": 24.75, "end": 26.49, "lines": [{"text": "И СРАЗУ ОСТАЕТСЯ ВИДИМОЙ НА", "accent": False, "size": "small"}, {"text": "ЭКРАНЕ", "accent": True, "size": "big"}]},
    {"start": 27.18, "end": 30.33, "lines": [{"text": "ГАЛОЧКА ВОЗНИКАЕТ ТОЛЬКО ПОСЛЕ РЕАЛЬНОГО ЗАВЕРШЕНИЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 31.05, "end": 32.88, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.04, "end": 2.37}, {"start": 7.83, "end": 8.16}, {"start": 31.05, "end": 31.38}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (living-room boy, camp counselor, 29.186s): вожатые open term
# cards for a whole hour instead of a short shift break; the app caps a
# session at exactly ten cards, then suggests a break on its own
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЛИСТАЕШЬ КАРТОЧКИ ЧАС", "ВМЕСТО ПЕРЕРЫВА?"], "end": 2.28}
e_cards = [
    {"start": 2.49, "end": 3.63, "lines": [{"text": "КАРТОЧКИ ТЕРМИНОВ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.84, "end": 6.63, "lines": [{"text": "НА ЦЕЛЫЙ ЧАС ВМЕСТО КОРОТКОГО ПЕРЕРЫВА СМЕНЫ В", "accent": False, "size": "small"}, {"text": "ЛАГЕРЯ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 8.64, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР ОГРАНИЧИВАЕТ", "accent": False, "size": "small"}, {"text": "СЕССИЮ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.99, "lines": [{"text": "РОВНО ДЕСЯТЬ КАРТОЧКАМИ", "accent": False, "size": "small"}, {"text": "ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 10.62, "end": 12.12, "lines": [{"text": "А ДАЛЬШЕ САМ ПРЕДЛАГАЕТ КОРОТКИЙ", "accent": False, "size": "small"}, {"text": "ПЕРЕРЫВ", "accent": True, "size": "big"}]},
    {"start": 12.69, "end": 14.79, "lines": [{"text": "ДЕСЯТЬ КАРТОЧЕК УКЛАДЫВАЮТСЯ В ОБЫЧНЫЙ", "accent": False, "size": "small"}, {"text": "ПЕРЕРЫВ", "accent": True, "size": "big"}]},
    {"start": 14.97, "end": 16.35, "lines": [{"text": "СМЕНЫ МЕЖДУ ДЕЛАМИ", "accent": False, "size": "small"}, {"text": "ВОЖАТОГО", "accent": True, "size": "big"}]},
    {"start": 16.59, "end": 18.15, "lines": [{"text": "РАСТЯГИВАТЬ КАРТОЧКИ НА", "accent": False, "size": "small"}, {"text": "ЦЕЛЫЙ ЧАС", "accent": True, "size": "big"}]},
    {"start": 18.36, "end": 19.41, "lines": [{"text": "ВМЕСТО", "accent": False, "size": "small"}, {"text": "КОРОТКОГО ПЕРЕРЫВА", "accent": True, "size": "big"}]},
    {"start": 19.65, "end": 21.18, "lines": [{"text": "НЕ ПРИХОДИТСЯ НОВАЯ", "accent": False, "size": "small"}, {"text": "ДЕСЯТКА", "accent": True, "size": "big"}]},
    {"start": 21.33, "end": 22.83, "lines": [{"text": "КАРТОЧЕК ОТКРЫВАЕТСЯ НА", "accent": False, "size": "small"}, {"text": "СЛЕДУЮЩЕМ", "accent": True, "size": "big"}]},
    {"start": 22.98, "end": 24.15, "lines": [{"text": "СВОБОДНОМ ПЕРЕРЫВЕ", "accent": False, "size": "small"}, {"text": "СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 24.39, "end": 26.82, "lines": [{"text": "ДЕСЯТЬ КАРТОЧЕК УКЛАДЫВАЮТСЯ РОВНО В КОРОТКИЙ ПЕРЕРЫВ", "accent": False, "size": "small"}, {"text": "СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 27.42, "end": 29.28, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.49, "end": 2.82}, {"start": 6.96, "end": 7.29}, {"start": 27.42, "end": 27.75}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-boy, fishing trip, 28.360s): stats show days without
# connection as an honest streak failure; the app silently excludes days
# with zero app opens from the streak instead of counting them as a fail,
# so a day without signal never dents the overall stats
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СЧИТАЕТ ДЕНЬ БЕЗ СВЯЗИ", "ПРОВАЛОМ СЕРИИ?"], "end": 1.95}
f_cards = [
    {"start": 2.28, "end": 3.12, "lines": [{"text": "СТАТИСТИКИ ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.30, "end": 4.47, "lines": [{"text": "ПРОПУЩЕННЫЕ ДНИ БЕЗ", "accent": False, "size": "small"}, {"text": "СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 4.74, "end": 6.06, "lines": [{"text": "КАК ЧЕСТНЫЙ ПРОВАЛ", "accent": False, "size": "small"}, {"text": "СЕРИИ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 7.59, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПРОПУСКАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 9.42, "lines": [{"text": "ДНИ БЕЗ ЕДИНОГО ОТКРЫТИЯ", "accent": False, "size": "small"}, {"text": "ПРИЛОЖЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.61, "lines": [{"text": "МОЛЧА НЕ ЗАСЧИТЫВАЯ ИХ КАК", "accent": False, "size": "small"}, {"text": "ПРОВАЛ", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 13.29, "lines": [{"text": "СЕРИИ СТАТИСТИКА СЧИТАЕТСЯ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.88, "lines": [{"text": "ПО ДНЯМ КОГДА ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "РЕАЛЬНО", "accent": True, "size": "big"}]},
    {"start": 15.03, "end": 16.11, "lines": [{"text": "ОТКРЫВАЛИСЬ И", "accent": False, "size": "small"}, {"text": "РЕШАЛИСЬ", "accent": True, "size": "big"}]},
    {"start": 16.41, "end": 18.39, "lines": [{"text": "ОПРАВДЫВАТЬСЯ ПЕРЕД СОБСТВЕННОЙ СТАТИСТИКОЙ ЗА", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 18.51, "end": 19.35, "lines": [{"text": "БЕЗ СВЯЗИ НА", "accent": False, "size": "small"}, {"text": "РЫБАЛКЕ", "accent": True, "size": "big"}]},
    {"start": 19.56, "end": 21.06, "lines": [{"text": "НЕ ПРИХОДИТСЯ ПРОПУЩЕННЫЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 21.27, "end": 22.53, "lines": [{"text": "ПРОСТО НЕ ВХОДИТ В ОБЩИЙ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 22.65, "end": 23.94, "lines": [{"text": "РЕЗУЛЬТАТОВ ПРОПУЩЕННЫЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 24.09, "end": 24.90, "lines": [{"text": "БЕЗ СВЯЗИ ПРОСТО НЕ", "accent": False, "size": "small"}, {"text": "ПРОСТО", "accent": True, "size": "big"}]},
    {"start": 25.02, "end": 26.22, "lines": [{"text": "ПОРТИТ ОБЩУЮ", "accent": False, "size": "small"}, {"text": "СТАТИСТИКУ", "accent": True, "size": "big"}]},
    {"start": 26.49, "end": 28.44, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.28, "end": 2.61}, {"start": 6.45, "end": 6.78}, {"start": 26.49, "end": 26.82}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (living-room boy, camp counselor, 30.160s): вожатые re-download
# the whole offline task bank every time before a new camp shift; the app
# syncs the offline bank once on reconnect, no full re-download, already
# saved tasks stay in place with no duplicates
# ---------------------------------------------------------------------------
g_intro = {"lines": ["СКАЧИВАЕШЬ БАНК ЗАДАНИЙ", "ПЕРЕД КАЖДОЙ СМЕНОЙ?"], "end": 2.19}
g_cards = [
    {"start": 2.37, "end": 3.72, "lines": [{"text": "ОФЛАЙН БАНК ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 5.76, "lines": [{"text": "ЗАНОВО КАЖДЫЙ РАЗ ПЕРЕД НОВОЙ", "accent": False, "size": "small"}, {"text": "СМЕНОЙ", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 8.61, "lines": [{"text": "В ЛАГЕРЕ ЕГЭ ТРЕНАЖЕР СИНХРОНИЗИРУЕТ", "accent": False, "size": "small"}, {"text": "ОФФЛАЙН", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 10.44, "lines": [{"text": "БАНК ОДИН РАЗ ПРИ ВОЗВРАТЕ", "accent": False, "size": "small"}, {"text": "СВЯЗИ", "accent": True, "size": "big"}]},
    {"start": 10.80, "end": 12.75, "lines": [{"text": "БЕЗ ПОВТОРНОГО ПОЛНОГО СКАЧИВАНИЯ", "accent": False, "size": "small"}, {"text": "ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.97, "lines": [{"text": "УЖЕ СОХРАНЕННЫЕ ЗАДАНИЯ ОСТАЮТСЯ НА", "accent": False, "size": "small"}, {"text": "МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 16.68, "lines": [{"text": "ВСЮ СМЕНУ БЕЗ ЕДИНОГО", "accent": False, "size": "small"}, {"text": "ДУБЛЯ", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.33, "lines": [{"text": "ОДИН И ТОТ ЖЕ", "accent": False, "size": "small"}, {"text": "СКАЧИВАЙТЕ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 20.28, "lines": [{"text": "ОФФЛАЙН БАНК ЗАНОВО ПЕРЕД КАЖДОЙ", "accent": False, "size": "small"}, {"text": "СМЕНОЙ", "accent": True, "size": "big"}]},
    {"start": 20.58, "end": 22.05, "lines": [{"text": "НЕ ПРИХОДИТСЯ НОВЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 22.17, "end": 23.49, "lines": [{"text": "ДОБАВЛЯЮТСЯ ТОЛЬКО ПОВЕРХ", "accent": False, "size": "small"}, {"text": "УЖЕ", "accent": True, "size": "big"}]},
    {"start": 23.58, "end": 24.99, "lines": [{"text": "СОХРАНЕННЫХ ПРЕЖНИХ ОФФЛАЙН", "accent": False, "size": "small"}, {"text": "БАНК", "accent": True, "size": "big"}]},
    {"start": 25.08, "end": 28.32, "lines": [{"text": "СИНХРОНИЗИРУЕТСЯ ОДИН РАЗ БЕЗ ПОВТОРНОГО СКАЧИВАНИЯ", "accent": False, "size": "small"}, {"text": "ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 28.53, "end": 30.24, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.37, "end": 2.70}, {"start": 6.96, "end": 7.29}, {"start": 28.53, "end": 28.86}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (mother, parent POV, 31.170s): parents used to rewatching a
# whole video walkthrough just for one short line of the solution at the
# end; the app builds a separate timestamp menu under the walkthrough, the
# needed step opens straight away with one tap on its timestamp
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ПЕРЕСМАТРИВАЕШЬ РОЛИК", "РАДИ ОДНОЙ СТРОКИ?"], "end": 2.0}
h_cards = [
    {"start": 2.04, "end": 3.63, "lines": [{"text": "РОДИТЕЛИ ЧТО ВИДЕОРАЗБОР", "accent": False, "size": "small"}, {"text": "ПРИВЫКЛИ", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 5.64, "lines": [{"text": "ЗАДАНИЯ ЕГЭ ПРИХОДИТСЯ ПЕРЕСМАТРИВАТЬ", "accent": False, "size": "small"}, {"text": "ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 7.50, "lines": [{"text": "РАДИ ОДНОЙ КОРОТКОЙ СТРОКИ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 7.59, "end": 9.51, "lines": [{"text": "В САМОМ КОНЦЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 9.69, "end": 11.19, "lines": [{"text": "СТРОИТ ОТДЕЛЬНОЕ МЕНЮ ИЗ", "accent": False, "size": "small"}, {"text": "МЕТОК", "accent": True, "size": "big"}]},
    {"start": 11.31, "end": 14.52, "lines": [{"text": "ВРЕМЕНИ ПОД САМИМ ВИДЕОРАЗБОРОМ БЕЗ ЕДИНОГО ЛИШНЕГО", "accent": False, "size": "small"}, {"text": "КЛИКА", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.38, "lines": [{"text": "ШАГ РЕШЕНИЯ ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "НУЖНЫЙ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.61, "lines": [{"text": "СРАЗУ НАЖАТИЕМ НА", "accent": False, "size": "small"}, {"text": "МЕТКУ", "accent": True, "size": "big"}]},
    {"start": 17.76, "end": 20.01, "lines": [{"text": "В СПИСКЕ ПЕРЕСМАТРИВАТЬ ВЕСЬ РОЛИК", "accent": False, "size": "small"}, {"text": "ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 20.16, "end": 21.72, "lines": [{"text": "РАДИ ОДНОГО ШАГА НЕ", "accent": False, "size": "small"}, {"text": "ПРИХОДИТСЯ", "accent": True, "size": "big"}]},
    {"start": 22.38, "end": 23.82, "lines": [{"text": "МЕНЮ МЕТОК ОСТАЕТСЯ ПОД", "accent": False, "size": "small"}, {"text": "РОЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 23.97, "end": 25.32, "lines": [{"text": "ПРИ КАЖДОМ ПОВТОРНОМ", "accent": False, "size": "small"}, {"text": "ПРОСМОТРЕ", "accent": True, "size": "big"}]},
    {"start": 25.80, "end": 27.42, "lines": [{"text": "ШАГ РЕШЕНИЯ ОТКРЫВАЮТСЯ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 27.60, "end": 28.83, "lines": [{"text": "НАЖАТИЕМ НА", "accent": False, "size": "small"}, {"text": "МЕТКУ ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 29.34, "end": 31.29, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 2.04, "end": 2.37}, {"start": 9.00, "end": 9.33}, {"start": 29.34, "end": 29.67}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (mother, parent POV, 30.960s): parents notice a short quiz
# imperceptibly stretching into a whole evening; the app caps the game at
# exactly three questions per session, a round ends in a couple of minutes,
# a new round only opens the next day
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ИГРА ПО ЕГЭ РАСТЯГИВАЕТСЯ", "НА ВЕСЬ ВЕЧЕР?"], "end": 2.0}
i_cards = [
    {"start": 2.04, "end": 3.24, "lines": [{"text": "СЛЕДЯТ КАК", "accent": False, "size": "small"}, {"text": "КОРОТКАЯ ИГРА", "accent": True, "size": "big"}]},
    {"start": 3.33, "end": 5.55, "lines": [{"text": "ПО ЕГЭ НЕЗАМЕТНО РАСТЯГИВАЕТСЯ НА ДОЛГИЙ", "accent": False, "size": "small"}, {"text": "ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 5.76, "end": 7.86, "lines": [{"text": "БЕЗ ОСТАНОВКИ ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 8.10, "end": 8.91, "lines": [{"text": "ОГРАНИЧИВАЕТ", "accent": False, "size": "small"}, {"text": "ИГРУ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.05, "lines": [{"text": "РОВНО", "accent": False, "size": "small"}, {"text": "ТРЕМЯ ВОПРОСАМИ", "accent": True, "size": "big"}]},
    {"start": 10.23, "end": 12.84, "lines": [{"text": "ЗА ОДИН ЗАХОД БЕЗ ТУРНИРНОЙ ТАБЛИЦЫ И", "accent": False, "size": "small"}, {"text": "СПЕШКИ", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.94, "lines": [{"text": "РАУНД ЗАКАНЧИВАЕТСЯ ЗА ПАРУ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 16.71, "lines": [{"text": "ЗАДОЛГО ДО ТОГО КАК ВЕЧЕР", "accent": False, "size": "small"}, {"text": "УЙДЕТ", "accent": True, "size": "big"}]},
    {"start": 16.86, "end": 19.11, "lines": [{"text": "ЦЕЛИКОМ НА ЭКРАН ИГРАТЬ БЕЗ", "accent": False, "size": "small"}, {"text": "ОСТАНОВКИ", "accent": True, "size": "big"}]},
    {"start": 19.26, "end": 20.43, "lines": [{"text": "РАДИ МЕСТА В ОБЩЕМ", "accent": False, "size": "small"}, {"text": "ТУРНИРЕ", "accent": True, "size": "big"}]},
    {"start": 20.55, "end": 22.56, "lines": [{"text": "НЕ ПРИХОДИТСЯ НОВЫЙ КОРОТКИЙ", "accent": False, "size": "small"}, {"text": "РАУНД", "accent": True, "size": "big"}]},
    {"start": 22.71, "end": 24.21, "lines": [{"text": "ОТКРЫВАЕТСЯ ТОЛЬКО НА СЛЕДУЮЩИЙ", "accent": False, "size": "small"}, {"text": "ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 24.87, "end": 26.82, "lines": [{"text": "КОРОТКИЙ РАУНД ЗАКАНЧИВАЕТСЯ ЗА ПАРУ", "accent": False, "size": "small"}, {"text": "МИНУТ", "accent": True, "size": "big"}]},
    {"start": 27.24, "end": 28.62, "lines": [{"text": "БЕЗ ДОЛГОГО ВЕЧЕРА У", "accent": False, "size": "small"}, {"text": "ЭКРАНА", "accent": True, "size": "big"}]},
    {"start": 29.19, "end": 31.08, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 2.04, "end": 2.37}, {"start": 7.29, "end": 7.62}, {"start": 29.19, "end": 29.52}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
