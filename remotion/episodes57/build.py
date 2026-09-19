#!/usr/bin/env python3
"""One-off authoring + validation script for the FOURTEENTH 'coffee123'
batch (6 episodes uploaded under the same tag after thirteen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes57/.

Filenames this time are pure keyboard-mash gibberish with no date or
session info at all (e.g. "bhfgdhhhgfdhd.mp4", "gfgdgfdgfdg.mp4").
Two hosts: a genuinely new boy in a daylight living-room setting
(bookshelf, lamp, plants, couch - distinct from every prior room) and
the returning curly-haired boy. Camp-counselor ("вожатый") and
fishing-trip sub-themes both continue. Content: starting a mock exam for
the whole troop with one button instead of one counselor at a time,
showing rank for a single chosen subject instead of the full mixed
rating, downloading a video walkthrough in advance so it survives a
signal-free camp day, auto-archiving an outdated task instead of leaving
it in the general list, a one-swipe term preview instead of opening the
full card, and no monthly cap on the number of solved tasks.
"""
import json

REAL_DURATION = {
    "a": 26.455, "b": 25.772, "c": 26.050,
    "d": 27.760, "e": 27.692, "f": 25.644,
}
SOURCE_FILE = {
    "a": "bhfgdhhhgfdhd", "b": "fdgdgfdgfdg", "c": "fdgfdgdgfdgfdf",
    "d": "fdgfdgfdgffdg", "e": "fgdgfdgdgfdgd", "f": "gfgdgfdgfdg",
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
    if letter == "e":
        for w in words:
            if abs(w["start"] - 15.24) < 0.02 and w["text"] == "открывайть":
                w["text"] = "открывать"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_14/{src}_words.json"))
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
# Episode A (new living-room boy as camp counselor, 26.455s): launching a
# mock exam manually one counselor at a time; the app starts it for the
# whole troop at once with one button, and a late counselor can join an
# already-running mock
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЗАПУСКАЕШЬ ПРОБНИК", "ПО ОЧЕРЕДИ?"], "end": 2.3}
a_cards = [
    {"start": 2.49, "end": 3.30, "lines": [{"text": "ЗАПУСКАЮТ", "accent": False, "size": "small"}, {"text": "ПРОБНИК", "accent": True, "size": "big"}]},
    {"start": 3.45, "end": 4.86, "lines": [{"text": "ПО ЕГЭ ВРУЧНУЮ", "accent": False, "size": "small"}, {"text": "ДЛЯ КАЖДОГО", "accent": True, "size": "big"}]},
    {"start": 5.04, "end": 6.45, "lines": [{"text": "ИЗ ОТРЯДА", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 6.66, "end": 8.64, "lines": [{"text": "ЗАПУСКАЕТ ПРОБНИК", "accent": False, "size": "small"}, {"text": "СРАЗУ ДЛЯ ВСЕГО", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 10.50, "lines": [{"text": "ОТРЯДА ВОЖАТЫХ", "accent": False, "size": "small"}, {"text": "ОДНОЙ КНОПКОЙ", "accent": True, "size": "big"}]},
    {"start": 10.74, "end": 11.73, "lines": [{"text": "КАЖДЫЙ НАЧИНАЕТ", "accent": False, "size": "small"}, {"text": "ТЕСТ", "accent": True, "size": "big"}]},
    {"start": 11.91, "end": 12.81, "lines": [{"text": "В ОДНУ И ТУ", "accent": False, "size": "small"}, {"text": "ЖЕ МИНУТУ", "accent": True, "size": "big"}]},
    {"start": 13.11, "end": 14.22, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "РАЗНОБОЯ ПО ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 14.49, "end": 15.57, "lines": [{"text": "ЗАПУСКАТЬ ТЕСТ", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 15.78, "end": 17.28, "lines": [{"text": "ДЛЯ КАЖДОГО ИЗ", "accent": False, "size": "small"}, {"text": "ОТРЯДА ПО ОЧЕРЕДИ", "accent": True, "size": "big"}]},
    {"start": 17.49, "end": 18.90, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ОПОЗДАВШИЙ", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 20.01, "lines": [{"text": "ПРИСОЕДИНЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ВОЖАТЫЙ", "accent": True, "size": "big"}]},
    {"start": 20.16, "end": 21.24, "lines": [{"text": "К УЖЕ ИДУЩЕМУ", "accent": False, "size": "small"}, {"text": "ПРОБНИКУ", "accent": True, "size": "big"}]},
    {"start": 21.42, "end": 22.35, "lines": [{"text": "СРАЗУ ВЕСЬ", "accent": False, "size": "small"}, {"text": "ОТРЯД", "accent": True, "size": "big"}]},
    {"start": 22.53, "end": 23.52, "lines": [{"text": "СТАРТУЕТ", "accent": False, "size": "small"}, {"text": "ОДНОЙ КНОПКОЙ", "accent": True, "size": "big"}]},
    {"start": 23.79, "end": 24.69, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "РАЗНОБОЯ", "accent": True, "size": "big"}]},
    {"start": 24.69, "end": 26.28, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.49, "end": 2.82}, {"start": 6.66, "end": 6.99}, {"start": 19.41, "end": 20.01}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (curly-boy, 25.772s): on a fishing trip, the overall rating gets
# lost among all subjects at once; the app shows rank for just one chosen
# subject, picked once in settings
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ТЕРЯЕШЬСЯ В РЕЙТИНГЕ", "СРЕДИ ВСЕХ ПРЕДМЕТОВ?"], "end": 2.3}
b_cards = [
    {"start": 2.46, "end": 3.87, "lines": [{"text": "ОБЩИЙ РЕЙТИНГ ПО ЕГЭ", "accent": False, "size": "small"}, {"text": "ТЕРЯЮТСЯ", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 5.01, "lines": [{"text": "СРЕДИ ВСЕХ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТОВ", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.33, "lines": [{"text": "СРАЗУ", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 6.48, "end": 8.04, "lines": [{"text": "ПОКАЗЫВАЕТ МЕСТО", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ПО ОДНОМУ", "accent": True, "size": "big"}]},
    {"start": 8.25, "end": 9.06, "lines": [{"text": "ВЫБРАННОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 9.39, "end": 10.53, "lines": [{"text": "А НЕ ОБЩИЙ", "accent": False, "size": "small"}, {"text": "СПИСОК", "accent": True, "size": "big"}]},
    {"start": 10.74, "end": 12.57, "lines": [{"text": "ОБЩЕСТВОЗНАНИЕ СРАВНИВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 12.66, "end": 14.40, "lines": [{"text": "ОТ ОСТАЛЬНЫХ ПРЕДМЕТОВ", "accent": False, "size": "small"}, {"text": "НА СВОЕЙ СТРОКЕ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.69, "lines": [{"text": "РАЗБИРАТЬ", "accent": False, "size": "small"}, {"text": "ОБЩИЙ СПИСОК", "accent": True, "size": "big"}]},
    {"start": 15.84, "end": 17.13, "lines": [{"text": "РАДИ ОДНОГО", "accent": False, "size": "small"}, {"text": "НУЖНОГО ПРЕДМЕТА", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 18.96, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТ ДЛЯ ПОКАЗА", "accent": True, "size": "big"}]},
    {"start": 19.11, "end": 20.13, "lines": [{"text": "ВЫБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "ОДИН РАЗ", "accent": True, "size": "big"}]},
    {"start": 20.34, "end": 21.63, "lines": [{"text": "В НАСТРОЙКАХ", "accent": False, "size": "small"}, {"text": "МЕСТО ПО ОДНОМУ", "accent": True, "size": "big"}]},
    {"start": 21.75, "end": 23.82, "lines": [{"text": "ПРЕДМЕТУ ВИДНО ОТДЕЛЬНО", "accent": False, "size": "small"}, {"text": "ОТ ОБЩЕГО", "accent": True, "size": "big"}]},
    {"start": 24.15, "end": 25.62, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.48, "end": 3.87}, {"start": 6.48, "end": 6.81}, {"start": 19.11, "end": 19.53}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (new living-room boy as camp counselor, 26.050s): losing signal
# for a whole camp day and missing the video walkthrough; the app lets you
# download it in advance with one tap before the shift starts
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТЕРЯЕШЬ СВЯЗЬ", "И ПРОПУСКАЕШЬ РАЗБОР?"], "end": 2.3}
c_cards = [
    {"start": 2.73, "end": 3.60, "lines": [{"text": "НА ВЕСЬ ДЕНЬ", "accent": False, "size": "small"}, {"text": "СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 3.75, "end": 5.52, "lines": [{"text": "И НЕ УСПЕВАЮТ", "accent": False, "size": "small"}, {"text": "ПОСМОТРЕТЬ", "accent": True, "size": "big"}]},
    {"start": 5.73, "end": 6.66, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 8.07, "lines": [{"text": "ПОЗВОЛЯЕТ", "accent": False, "size": "small"}, {"text": "СКАЧАТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 8.22, "end": 9.42, "lines": [{"text": "ЗАРАНЕЕ", "accent": False, "size": "small"}, {"text": "ОДНИМ НАЖАТИЕМ", "accent": True, "size": "big"}]},
    {"start": 9.57, "end": 10.41, "lines": [{"text": "ПЕРЕД НАЧАЛОМ", "accent": False, "size": "small"}, {"text": "СМЕНЫ", "accent": True, "size": "big"}]},
    {"start": 10.56, "end": 11.61, "lines": [{"text": "С УТРА", "accent": False, "size": "small"}, {"text": "РОЛИК ОСТАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 12.66, "lines": [{"text": "ДОСТУПНЫМ", "accent": False, "size": "small"}, {"text": "ВЕСЬ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 12.81, "end": 14.37, "lines": [{"text": "СМЕНЫ", "accent": False, "size": "small"}, {"text": "БЕЗ ЕДИНОГО МЕГАБАЙТА", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 15.51, "lines": [{"text": "СВЯЗИ", "accent": False, "size": "small"}, {"text": "ЛОВИТЬ СЕТЬ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 17.01, "lines": [{"text": "МЕЖДУ ДЕЛАМИ", "accent": False, "size": "small"}, {"text": "РАДИ РОЛИКА", "accent": True, "size": "big"}]},
    {"start": 17.19, "end": 18.63, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "СКАЧАННЫЙ РОЛИК", "accent": True, "size": "big"}]},
    {"start": 18.75, "end": 19.74, "lines": [{"text": "ЗАНИМАЕТ", "accent": False, "size": "small"}, {"text": "СОВСЕМ НЕМНОГО", "accent": True, "size": "big"}]},
    {"start": 19.86, "end": 20.97, "lines": [{"text": "МЕСТА В ПАМЯТИ", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОНА", "accent": True, "size": "big"}]},
    {"start": 21.24, "end": 22.29, "lines": [{"text": "РОЛИК СКАЧАН", "accent": False, "size": "small"}, {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 22.44, "end": 24.00, "lines": [{"text": "И ДОСТУПЕН", "accent": False, "size": "small"}, {"text": "ВЕСЬ ДЕНЬ БЕЗ", "accent": True, "size": "big"}]},
    {"start": 24.30, "end": 25.86, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.95, "end": 2.16}, {"start": 6.78, "end": 7.11}, {"start": 21.57, "end": 21.78}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (new living-room boy as camp counselor, 27.760s): accidentally
# solving an outdated task found in the general list; the app auto-hides
# outdated tasks into an archive instead of leaving them in the list
# ---------------------------------------------------------------------------
d_intro = {"lines": ["РЕШАЕШЬ СЛУЧАЙНО", "УСТАРЕВШЕЕ ЗАДАНИЕ?"], "end": 2.3}
d_cards = [
    {"start": 2.40, "end": 3.72, "lines": [{"text": "СЛУЧАЙНО РЕШАЮТ", "accent": False, "size": "small"}, {"text": "УСТАРЕВШЕЕ", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.19, "lines": [{"text": "ЕГЭ НАЙДЕННОЕ", "accent": False, "size": "small"}, {"text": "МЕЖДУ ДЕЛАМИ", "accent": True, "size": "big"}]},
    {"start": 5.37, "end": 7.08, "lines": [{"text": "В ОБЩЕМ СПИСКЕ", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.40, "lines": [{"text": "ПРЯЧЕТ", "accent": False, "size": "small"}, {"text": "УСТАРЕВШЕЕ ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 8.58, "end": 9.81, "lines": [{"text": "САМО В АРХИВ", "accent": False, "size": "small"}, {"text": "НЕ ОСТАВЛЯЯ", "accent": True, "size": "big"}]},
    {"start": 9.99, "end": 10.83, "lines": [{"text": "ЕГО В ОБЩЕМ", "accent": False, "size": "small"}, {"text": "СПИСКЕ", "accent": True, "size": "big"}]},
    {"start": 11.19, "end": 12.39, "lines": [{"text": "НАЙТИ СЛУЧАЙНО", "accent": False, "size": "small"}, {"text": "УСТАРЕВШУЮ", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.56, "lines": [{"text": "ФОРМУЛИРОВКУ", "accent": False, "size": "small"}, {"text": "МЕЖДУ ДЕЛАМИ", "accent": True, "size": "big"}]},
    {"start": 13.74, "end": 14.79, "lines": [{"text": "БОЛЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИТСЯ", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.29, "lines": [{"text": "ПРОВЕРЯТЬ АКТУАЛЬНОСТЬ", "accent": False, "size": "small"}, {"text": "КАЖДОГО", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 17.64, "lines": [{"text": "НАЙДЕННОГО ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 17.97, "end": 19.05, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "АРХИВ", "accent": True, "size": "big"}]},
    {"start": 19.17, "end": 20.34, "lines": [{"text": "ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 20.61, "end": 21.69, "lines": [{"text": "И НЕ МЕШАЕТ", "accent": False, "size": "small"}, {"text": "ОСНОВНОМУ", "accent": True, "size": "big"}]},
    {"start": 21.81, "end": 23.25, "lines": [{"text": "СПИСКУ ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "УСТАРЕВШЕЕ", "accent": True, "size": "big"}]},
    {"start": 23.34, "end": 24.39, "lines": [{"text": "ЗАДАНИЕ САМО", "accent": False, "size": "small"}, {"text": "УХОДИТ", "accent": True, "size": "big"}]},
    {"start": 24.54, "end": 25.80, "lines": [{"text": "В АРХИВ ИЗ", "accent": False, "size": "small"}, {"text": "ОБЩЕГО СПИСКА", "accent": True, "size": "big"}]},
    {"start": 26.10, "end": 27.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.40, "end": 2.61}, {"start": 7.23, "end": 7.47}, {"start": 24.18, "end": 24.39}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (curly-boy, 27.692s): on a fishing trip, accidentally opening a
# term card fully instead of a quick preview; the app shows a short preview
# with one swipe without opening the card fully
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОТКРЫВАЕШЬ ЛИШНИЙ", "ТЕРМИН СЛУЧАЙНО?"], "end": 2.3}
e_cards = [
    {"start": 2.46, "end": 3.60, "lines": [{"text": "СЛУЧАЙНО ОТКРЫВАЮТ", "accent": False, "size": "small"}, {"text": "ЛИШНИЙ ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 3.81, "end": 5.31, "lines": [{"text": "ЕГЭ ВМЕСТО", "accent": False, "size": "small"}, {"text": "БЫСТРОГО ПРОСМОТРА", "accent": True, "size": "big"}]},
    {"start": 5.52, "end": 6.72, "lines": [{"text": "СПИСКА", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 6.90, "end": 7.80, "lines": [{"text": "ПОКАЗЫВАЕТ", "accent": False, "size": "small"}, {"text": "КОРОТКОЕ", "accent": True, "size": "big"}]},
    {"start": 7.89, "end": 9.27, "lines": [{"text": "ПРЕВЬЮ ТЕРМИНА", "accent": False, "size": "small"}, {"text": "ОДНИМ СВАЙПОМ", "accent": True, "size": "big"}]},
    {"start": 9.39, "end": 10.26, "lines": [{"text": "НЕ ОТКРЫВАЯ", "accent": False, "size": "small"}, {"text": "КАРТОЧКУ", "accent": True, "size": "big"}]},
    {"start": 10.47, "end": 12.03, "lines": [{"text": "ПОЛНОСТЬЮ", "accent": False, "size": "small"}, {"text": "БЫСТРО ПРОЛИСТАТЬ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 13.47, "lines": [{"text": "ВЕСЬ СПИСОК", "accent": False, "size": "small"}, {"text": "ПРЕВЬЮ ПОЛУЧАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.88, "lines": [{"text": "ЗА МИНУТУ", "accent": False, "size": "small"}, {"text": "МЕЖДУ ЗАБРОСАМИ", "accent": True, "size": "big"}]},
    {"start": 15.24, "end": 16.05, "lines": [{"text": "ОТКРЫВАТЬ И", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАТЬ", "accent": True, "size": "big"}]},
    {"start": 16.23, "end": 17.55, "lines": [{"text": "КАРТОЧКУ ПО ОТДЕЛЬНОСТИ", "accent": False, "size": "small"}, {"text": "КАЖДУЮ", "accent": True, "size": "big"}]},
    {"start": 17.79, "end": 18.96, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ПОЛНАЯ", "accent": True, "size": "big"}]},
    {"start": 19.08, "end": 19.92, "lines": [{"text": "ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "КАРТОЧКА", "accent": True, "size": "big"}]},
    {"start": 20.04, "end": 20.85, "lines": [{"text": "ОТДЕЛЬНЫМ", "accent": False, "size": "small"}, {"text": "КАСАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 21.06, "end": 22.11, "lines": [{"text": "ЕСЛИ ТЕРМИН", "accent": False, "size": "small"}, {"text": "НЕЗНАКОМ", "accent": True, "size": "big"}]},
    {"start": 22.44, "end": 23.58, "lines": [{"text": "СПИСОК ЛИСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПРЕВЬЮ", "accent": True, "size": "big"}]},
    {"start": 23.73, "end": 24.72, "lines": [{"text": "С ВАЙПОМ БЕЗ", "accent": False, "size": "small"}, {"text": "ОТКРЫТИЯ", "accent": True, "size": "big"}]},
    {"start": 24.87, "end": 25.86, "lines": [{"text": "КАЖДОЙ", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 25.86, "end": 27.51, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.46, "end": 2.79}, {"start": 6.90, "end": 7.23}, {"start": 19.50, "end": 19.92}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (curly-boy, 25.644s): solving tasks in batches on a fishing trip
# and worrying about hitting a monthly cap; the app doesn't limit the
# number of solved tasks per month at all
# ---------------------------------------------------------------------------
f_intro = {"lines": ["БОИШЬСЯ УПЕРЕТЬСЯ", "В МЕСЯЧНЫЙ ЛИМИТ?"], "end": 2.3}
f_cards = [
    {"start": 2.40, "end": 3.75, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПАЧКАМИ", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 4.92, "lines": [{"text": "И БОЯТСЯ", "accent": False, "size": "small"}, {"text": "УПЕРЕТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 5.07, "end": 6.75, "lines": [{"text": "В МЕСЯЧНЫЙ ЛИМИТ", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 7.05, "end": 7.98, "lines": [{"text": "НЕ ОГРАНИЧИВАЕТ", "accent": False, "size": "small"}, {"text": "ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 8.07, "end": 9.75, "lines": [{"text": "РЕШЕННЫХ ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "НИКАКИМ ЛИМИТОМ", "accent": True, "size": "big"}]},
    {"start": 9.87, "end": 10.71, "lines": [{"text": "В ТЕЧЕНИЕ", "accent": False, "size": "small"}, {"text": "МЕСЯЦА", "accent": True, "size": "big"}]},
    {"start": 11.04, "end": 12.21, "lines": [{"text": "ПАЧКА ЗАДАНИЙ", "accent": False, "size": "small"}, {"text": "ЗА ОДИН ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 12.39, "end": 13.29, "lines": [{"text": "НА БЕРЕГУ", "accent": False, "size": "small"}, {"text": "НИЧЕГО", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.40, "lines": [{"text": "НЕ МЕНЯЕТ", "accent": False, "size": "small"}, {"text": "В ДОСТУПЕ", "accent": True, "size": "big"}]},
    {"start": 14.73, "end": 15.75, "lines": [{"text": "СЧИТАТЬ", "accent": False, "size": "small"}, {"text": "ОСТАВШИЙСЯ ЛИМИТ", "accent": True, "size": "big"}]},
    {"start": 15.87, "end": 16.86, "lines": [{"text": "ЗАДАНИЙ ДО", "accent": False, "size": "small"}, {"text": "КОНЦА МЕСЯЦА", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 18.48, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "РЕШАТЬ МОЖНО", "accent": True, "size": "big"}]},
    {"start": 18.66, "end": 19.47, "lines": [{"text": "ХОТЬ СТО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 19.59, "end": 20.46, "lines": [{"text": "ПОДРЯД В ОДИН", "accent": False, "size": "small"}, {"text": "ВЕЧЕР", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 21.84, "lines": [{"text": "ЧИСЛО РЕШЕННЫХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 22.05, "end": 23.55, "lines": [{"text": "НЕОГРАНИЧЕНО", "accent": False, "size": "small"}, {"text": "ЛИМИТОМ ЗА МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 23.82, "end": 25.08, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.59, "end": 4.92}, {"start": 7.20, "end": 7.68}, {"start": 22.05, "end": 22.68}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
