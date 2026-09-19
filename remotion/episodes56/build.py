#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTEENTH 'coffee123'
batch (9 episodes uploaded under the same tag after twelve prior batches
were delivered). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes56/.

Filenames this time are unusually messy (some don't even follow the
date-prefixed pattern, e.g. "19.60p333333.mp4" and "2.mp4") and two pairs
coincidentally share identical durations - verified via audio checksum
that these are NOT duplicate uploads (different content, just matching
length). Three returning hosts (girl with bookshelf/desk, parent woman,
girl in warm sweater) - no boy hosts in this drop. Content: learning a
solution method by reassembling shuffled steps instead of reading a
finished answer, auto-archiving a flashcard after three correct answers
in a row, one free pause per mock exam shown as unavailable in advance
after it's used, a plain solved-task count next to the progress percent,
downloading one subject's offline pack instead of the whole task bank,
a bright frame highlighting a task whose wording just changed, a
weekly position-change number instead of an absolute rank in a long
leaderboard, swapping the day's task topic once without losing a streak,
and a video walkthrough that pauses on a formula until marked
understood.
"""
import json

REAL_DURATION = {
    "a": 34.200, "b": 27.564, "c": 27.863,
    "d": 28.908, "e": 27.863, "f": 34.050,
    "g": 34.200, "h": 30.295, "i": 32.578,
}
SOURCE_FILE = {
    "a": "19_09___1_2160p111111", "b": "19_09___2_2160p22222222222222", "c": "19_09___3_2160p3333333333333333333",
    "d": "19_19___1_2160p111111", "e": "19_19___1_2160p1111111111", "f": "19_19___2_2160p222222",
    "g": "19_19___3_2160p333333", "h": "19_60p333333", "i": "2",
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
            if abs(w["start"] - 24.21) < 0.02 and w["text"] == "заменяе":
                w["text"] = "заменяет"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_13/{src}_words.json"))
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
# Episode A (girl-bookshelf, 34.200s): skipping intermediate steps and
# mixing up the method; the app shuffles the steps and asks to arrange them
# in order, so the method is learned by assembling it, not reading it
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ПРОПУСКАЕШЬ ШАГИ", "И ПУТАЕШЬ МЕТОД?"], "end": 2.3}
a_cards = [
    {"start": 2.70, "end": 4.14, "lines": [{"text": "ПРОПУСКАЕШЬ ПРОМЕЖУТОЧНЫЕ", "accent": False, "size": "small"}, {"text": "ШАГИ", "accent": True, "size": "big"}]},
    {"start": 4.35, "end": 5.46, "lines": [{"text": "РЕШЕНИЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 6.00, "end": 6.81, "lines": [{"text": "И ПОТОМ", "accent": False, "size": "small"}, {"text": "ПУТАЕШЬСЯ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 9.30, "lines": [{"text": "В САМОМ МЕТОДЕ", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 10.95, "lines": [{"text": "ПЕРЕМЕШИВАЕТ", "accent": False, "size": "small"}, {"text": "ШАГИ РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 11.25, "end": 12.69, "lines": [{"text": "ПРОСИТ РАССТАВИТЬ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНОМ", "accent": True, "size": "big"}]},
    {"start": 12.81, "end": 14.49, "lines": [{"text": "ПОРЯДКЕ", "accent": False, "size": "small"}, {"text": "ОДНИМ КАСАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 15.48, "end": 16.80, "lines": [{"text": "ПОРЯДОК", "accent": False, "size": "small"}, {"text": "СОБИРАЕТСЯ ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 17.04, "end": 18.69, "lines": [{"text": "ИЗ ПЕРЕПУТАННЫХ", "accent": False, "size": "small"}, {"text": "КАРТОЧЕК", "accent": True, "size": "big"}]},
    {"start": 19.38, "end": 20.52, "lines": [{"text": "А НЕ ПЕРЕПИСЫВАЕТСЯ С", "accent": False, "size": "small"}, {"text": "НУЛЯ", "accent": True, "size": "big"}]},
    {"start": 21.63, "end": 22.95, "lines": [{"text": "РЕШЕНИЯ ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "МЕТОД", "accent": True, "size": "big"}]},
    {"start": 23.19, "end": 24.96, "lines": [{"text": "ЧЕРЕЗ СБОРКУ А НЕ", "accent": False, "size": "small"}, {"text": "ЧЕРЕЗ ПРОСТОЕ", "accent": True, "size": "big"}]},
    {"start": 25.14, "end": 26.49, "lines": [{"text": "ЧТЕНИЕ", "accent": False, "size": "small"}, {"text": "ГОТОВОГО ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 27.57, "end": 28.77, "lines": [{"text": "ПОРЯДОК ШАГОВ", "accent": False, "size": "small"}, {"text": "СОБИРАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 28.98, "end": 29.88, "lines": [{"text": "ЗАНОВО А", "accent": False, "size": "small"}, {"text": "МЕТОД", "accent": True, "size": "big"}]},
    {"start": 30.03, "end": 31.35, "lines": [{"text": "ЗАПОМИНАЕТСЯ", "accent": False, "size": "small"}, {"text": "ЧЕРЕЗ СБОРКУ", "accent": True, "size": "big"}]},
    {"start": 32.34, "end": 34.02, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.70, "end": 3.09}, {"start": 9.60, "end": 10.11}, {"start": 22.44, "end": 22.95}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (parent host, 27.564s): the kid keeps flipping through already
# learned flashcards; the app auto-archives a card after three correct
# answers in a row
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ЛИСТАЕТ ВЫУЧЕННЫЕ", "КАРТОЧКИ ПО КРУГУ?"], "end": 2.3}
b_cards = [
    {"start": 2.52, "end": 3.42, "lines": [{"text": "ЧТО", "accent": False, "size": "small"}, {"text": "РЕБЕНОК ЛИСТАЕТ", "accent": True, "size": "big"}]},
    {"start": 3.60, "end": 4.62, "lines": [{"text": "УЖЕ ВЫУЧЕННЫЕ", "accent": False, "size": "small"}, {"text": "КАРТОЧКИ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 5.94, "lines": [{"text": "С ТЕРМИНОМ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО КРУГУ", "accent": True, "size": "big"}]},
    {"start": 6.63, "end": 7.53, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "УБИРАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 8.94, "lines": [{"text": "КАРТОЧКУ В АРХИВ", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 9.93, "lines": [{"text": "ПОСЛЕ ТРЕХ", "accent": False, "size": "small"}, {"text": "ВЕРНЫХ ОТВЕТОВ", "accent": True, "size": "big"}]},
    {"start": 10.08, "end": 10.92, "lines": [{"text": "ПОДРЯД БЕЗ", "accent": False, "size": "small"}, {"text": "ЕДИНОЙ ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 11.94, "end": 13.56, "lines": [{"text": "ВЫУЧЕННЫЙ ТЕРМИН", "accent": False, "size": "small"}, {"text": "БОЛЬШЕ НЕ", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.67, "lines": [{"text": "ПОПАДАЕТСЯ СРЕДИ", "accent": False, "size": "small"}, {"text": "НОВЫХ КАРТОЧЕК", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 16.41, "lines": [{"text": "ОТПРАВЛЯТЬ", "accent": False, "size": "small"}, {"text": "КАРТОЧКУ В АРХИВ", "accent": True, "size": "big"}]},
    {"start": 16.56, "end": 17.58, "lines": [{"text": "САМОСТОЯТЕЛЬНО", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 17.76, "end": 19.68, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "СПИСОК КАРТОЧЕК", "accent": True, "size": "big"}]},
    {"start": 19.83, "end": 20.67, "lines": [{"text": "ОСТАЕТСЯ", "accent": False, "size": "small"}, {"text": "КОРОТКИМ", "accent": True, "size": "big"}]},
    {"start": 20.79, "end": 21.93, "lines": [{"text": "И БЕЗ", "accent": False, "size": "small"}, {"text": "ЛИШНЕГО БАЛЛАСТА", "accent": True, "size": "big"}]},
    {"start": 22.38, "end": 23.49, "lines": [{"text": "КАРТОЧКА УХОДИТ", "accent": False, "size": "small"}, {"text": "В АРХИВ", "accent": True, "size": "big"}]},
    {"start": 23.61, "end": 25.44, "lines": [{"text": "САМА ПОСЛЕ ТРЕХ", "accent": False, "size": "small"}, {"text": "ВЕРНЫХ ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 25.89, "end": 27.03, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.15, "end": 3.42}, {"start": 7.29, "end": 7.53}, {"start": 22.89, "end": 23.10}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (parent host, 27.863s): worried the kid gets distracted during a
# mock exam and loses time; the app allows exactly one pause per mock
# without a time penalty, and shows in advance that a second one is gone
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ОТВЛЕЧЕТСЯ НА ПРОБНИКЕ", "И ПОТЕРЯЕТ ВРЕМЯ?"], "end": 2.3}
c_cards = [
    {"start": 2.58, "end": 3.66, "lines": [{"text": "ЧТО РЕБЕНОК", "accent": False, "size": "small"}, {"text": "ОТВЛЕЧЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 3.81, "end": 4.98, "lines": [{"text": "ВО ВРЕМЯ ПРОБНИКА", "accent": False, "size": "small"}, {"text": "ПО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.34, "end": 6.78, "lines": [{"text": "И ПОТЕРЯЕТ ДРАГОЦЕННОЕ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 9.03, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДАЕТ ПАУЗУ", "accent": True, "size": "big"}]},
    {"start": 9.21, "end": 10.38, "lines": [{"text": "ЗА ВЕСЬ ПРОБНИК", "accent": False, "size": "small"}, {"text": "БЕЗ ШТРАФА", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 12.06, "lines": [{"text": "ПО ОБЩЕМУ ВРЕМЕНИ", "accent": False, "size": "small"}, {"text": "КОРОТКИЙ", "accent": True, "size": "big"}]},
    {"start": 12.15, "end": 12.99, "lines": [{"text": "ПЕРЕРЫВ НЕ", "accent": False, "size": "small"}, {"text": "СБИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 13.14, "end": 14.25, "lines": [{"text": "ИТОГОВЫЕ", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТ ТЕСТА", "accent": True, "size": "big"}]},
    {"start": 14.88, "end": 15.81, "lines": [{"text": "ОТКАЗЫВАТЬСЯ", "accent": False, "size": "small"}, {"text": "ПОЛНОСТЬЮ", "accent": True, "size": "big"}]},
    {"start": 15.93, "end": 17.34, "lines": [{"text": "ОТ ЛЮБОГО ПЕРЕРЫВА", "accent": False, "size": "small"}, {"text": "РАДИ ЧИСТОГО", "accent": True, "size": "big"}]},
    {"start": 17.43, "end": 18.45, "lines": [{"text": "ВРЕМЕНИ НЕ", "accent": False, "size": "small"}, {"text": "ТРЕБУЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 20.43, "lines": [{"text": "ВТОРАЯ ПАУЗА УЖЕ", "accent": False, "size": "small"}, {"text": "НЕДОСТУПНА", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 21.72, "lines": [{"text": "И ЭТО ВИДНО", "accent": False, "size": "small"}, {"text": "ЗАРАНЕЕ", "accent": True, "size": "big"}]},
    {"start": 21.81, "end": 23.40, "lines": [{"text": "НА ЭКРАНЕ", "accent": False, "size": "small"}, {"text": "ОДНА ПАУЗА", "accent": True, "size": "big"}]},
    {"start": 23.55, "end": 24.69, "lines": [{"text": "ЗА ВЕСЬ ПРОБНИК", "accent": False, "size": "small"}, {"text": "НЕ СБИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 24.87, "end": 26.10, "lines": [{"text": "ИТОГОВЫЙ", "accent": False, "size": "small"}, {"text": "РЕЗУЛЬТАТ", "accent": True, "size": "big"}]},
    {"start": 26.10, "end": 27.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.21, "end": 3.66}, {"start": 8.25, "end": 8.70}, {"start": 19.98, "end": 20.43}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (warm-sweater girl, 28.908s): downloading the whole task bank
# before an exam takes too long; the app lets you download an offline pack
# for one subject instead of the whole bank
# ---------------------------------------------------------------------------
d_intro = {"lines": ["КАЧАЕШЬ ВЕСЬ БАНК", "И ЖДЕШЬ ЗАГРУЗКУ?"], "end": 2.3}
d_cards = [
    {"start": 2.61, "end": 3.93, "lines": [{"text": "КАЧАЕШЬ СРАЗУ", "accent": False, "size": "small"}, {"text": "ВЕСЬ БАНК", "accent": True, "size": "big"}]},
    {"start": 4.86, "end": 6.69, "lines": [{"text": "И ЖДУТ ЗАГРУЗКУ", "accent": False, "size": "small"}, {"text": "ДОЛЬШЕ ЧЕМ", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.61, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОЗВОЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.93, "lines": [{"text": "СКАЧАТЬ", "accent": False, "size": "small"}, {"text": "ОФФЛАЙН ПАКЕТ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 10.98, "lines": [{"text": "ПО ОДНОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 11.52, "end": 12.54, "lines": [{"text": "А НЕ ВЕСЬ", "accent": False, "size": "small"}, {"text": "БАНК ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 13.89, "lines": [{"text": "ЗА РАЗ", "accent": False, "size": "small"}, {"text": "НУЖНЫЙ", "accent": True, "size": "big"}]},
    {"start": 13.95, "end": 15.30, "lines": [{"text": "ПРЕДМЕТ К ИСПОЛЬЗОВАНИЮ", "accent": False, "size": "small"}, {"text": "ГОТОВ", "accent": True, "size": "big"}]},
    {"start": 15.57, "end": 18.09, "lines": [{"text": "УЖЕ ЧЕРЕЗ МИНУТУ", "accent": False, "size": "small"}, {"text": "БЕЗ ОЖИДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 18.81, "end": 19.89, "lines": [{"text": "ЖДАТЬ ПОЛНУЮ", "accent": False, "size": "small"}, {"text": "ЗАГРУЗКУ", "accent": True, "size": "big"}]},
    {"start": 20.04, "end": 20.94, "lines": [{"text": "РАДИ ОДНОГО", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТА", "accent": True, "size": "big"}]},
    {"start": 21.18, "end": 22.77, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТ", "accent": True, "size": "big"}]},
    {"start": 22.95, "end": 24.00, "lines": [{"text": "СКАЧИВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 24.60, "end": 26.40, "lines": [{"text": "БЕЗ ОЖИДАНИЯ", "accent": False, "size": "small"}, {"text": "ЗАГРУЗКИ БАНКА", "accent": True, "size": "big"}]},
    {"start": 27.12, "end": 28.44, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.61, "end": 2.88}, {"start": 8.25, "end": 8.61}, {"start": 22.95, "end": 23.46}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (parent host, 27.863s): the app only shows percent progress and
# it's hard to tell if that's a lot or a little; the app shows a plain
# number of solved tasks per week next to the percent
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ВИДИШЬ ТОЛЬКО ПРОЦЕНТЫ", "И НЕ ПОНИМАЕШЬ МНОГО ЛИ?"], "end": 2.3}
e_cards = [
    {"start": 2.46, "end": 3.63, "lines": [{"text": "ПРИЛОЖЕНИЕ", "accent": False, "size": "small"}, {"text": "ТОЛЬКО ПРОЦЕНТЫ", "accent": True, "size": "big"}]},
    {"start": 3.75, "end": 4.56, "lines": [{"text": "ПРОГРЕССА ПО", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.89, "end": 6.78, "lines": [{"text": "И НЕ ПОНИМАЮТ", "accent": False, "size": "small"}, {"text": "МНОГО ЛИ МАЛО", "accent": True, "size": "big"}]},
    {"start": 7.68, "end": 8.76, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 8.94, "end": 9.99, "lines": [{"text": "ПРОСТОЕ ЧИСЛО", "accent": False, "size": "small"}, {"text": "РЕШЕННЫХ", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 10.92, "lines": [{"text": "ЗАДАНИЙ ЗА", "accent": False, "size": "small"}, {"text": "НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 11.16, "end": 12.03, "lines": [{"text": "РЯДОМ С", "accent": False, "size": "small"}, {"text": "ПРОЦЕНТОМ", "accent": True, "size": "big"}]},
    {"start": 12.54, "end": 13.77, "lines": [{"text": "ЧИСЛО", "accent": False, "size": "small"}, {"text": "ПОНЯТНЕЕ ПРОЦЕНТЫ", "accent": True, "size": "big"}]},
    {"start": 13.92, "end": 14.88, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕСЧЕТА В ГОЛОВЕ", "accent": True, "size": "big"}]},
    {"start": 15.36, "end": 16.20, "lines": [{"text": "ПЕРЕВОДИТЬ", "accent": False, "size": "small"}, {"text": "ПРОЦЕНТЫ", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 17.52, "lines": [{"text": "В РЕАЛЬНОЕ", "accent": False, "size": "small"}, {"text": "КОЛИЧЕСТВО", "accent": True, "size": "big"}]},
    {"start": 17.67, "end": 18.99, "lines": [{"text": "САМОСТОЯТЕЛЬНО", "accent": False, "size": "small"}, {"text": "НЕ ТРЕБУЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 19.47, "end": 20.46, "lines": [{"text": "ОБЕ ЦИФРЫ", "accent": False, "size": "small"}, {"text": "ВИДНЫ РЯДОМ", "accent": True, "size": "big"}]},
    {"start": 20.58, "end": 21.66, "lines": [{"text": "НА ОДНОМ И", "accent": False, "size": "small"}, {"text": "ТОМ ЖЕ ЭКРАНЕ", "accent": True, "size": "big"}]},
    {"start": 22.53, "end": 24.09, "lines": [{"text": "ЧИСЛО РЕШЕННЫХ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ ПОНЯТНЕЕ", "accent": True, "size": "big"}]},
    {"start": 24.27, "end": 25.71, "lines": [{"text": "ПРОЦЕНТЫ БЕЗ", "accent": False, "size": "small"}, {"text": "ЛИШНЕГО ПЕРЕСЧЕТА", "accent": True, "size": "big"}]},
    {"start": 26.13, "end": 27.36, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.19, "end": 5.49}, {"start": 8.37, "end": 8.76}, {"start": 22.83, "end": 23.13}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (girl-bookshelf, 34.050s): not noticing a task's wording updated
# since yesterday; the app highlights the task with a bright frame right
# after the wording updates, disappearing once opened
# ---------------------------------------------------------------------------
f_intro = {"lines": ["НЕ ЗАМЕЧАЕШЬ ЧТО", "ЗАДАНИЕ ОБНОВИЛОСЬ?"], "end": 2.3}
f_cards = [
    {"start": 2.67, "end": 4.59, "lines": [{"text": "НЕ ЗАМЕЧАЕШЬ ЧТО ФОРМУЛИРОВКА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 6.66, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ОБНОВИЛАСЬ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 9.12, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР ПОДСВЕЧИВАЕТ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.75, "end": 11.13, "lines": [{"text": "ЯРКОЙ РАМКОЙ", "accent": False, "size": "small"}, {"text": "СРАЗУ ПОСЛЕ", "accent": True, "size": "big"}]},
    {"start": 11.25, "end": 12.33, "lines": [{"text": "ФОРМУЛИРОВКИ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 14.19, "lines": [{"text": "ПО ДЕМО ВЕРСИИ", "accent": False, "size": "small"}, {"text": "РАМКА", "accent": True, "size": "big"}]},
    {"start": 14.31, "end": 15.54, "lines": [{"text": "ИСЧЕЗАЕТ САМА", "accent": False, "size": "small"}, {"text": "КАК ТОЛЬКО", "accent": True, "size": "big"}]},
    {"start": 15.75, "end": 17.37, "lines": [{"text": "ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ОТКРЫТО ХОТЯ БЫ", "accent": True, "size": "big"}]},
    {"start": 18.12, "end": 18.96, "lines": [{"text": "СРАВНИВАТЬ", "accent": False, "size": "small"}, {"text": "СТАРУЮ", "accent": True, "size": "big"}]},
    {"start": 19.11, "end": 21.51, "lines": [{"text": "И НОВУЮ ФОРМУЛИРОВКУ", "accent": False, "size": "small"}, {"text": "РАДИ ЦЕЛИ", "accent": True, "size": "big"}]},
    {"start": 21.66, "end": 23.46, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "ОДИН ВЗГЛЯД", "accent": True, "size": "big"}]},
    {"start": 23.61, "end": 24.60, "lines": [{"text": "НА РАМКУ", "accent": False, "size": "small"}, {"text": "ЗАМЕНЯЕТ", "accent": True, "size": "big"}]},
    {"start": 24.75, "end": 26.58, "lines": [{"text": "ЧТЕНИЕ ВСЕЙ ФОРМУЛИРОВКИ", "accent": False, "size": "small"}, {"text": "ЗАНОВО", "accent": True, "size": "big"}]},
    {"start": 27.42, "end": 28.95, "lines": [{"text": "ЦВЕТНАЯ РАМКА САМА", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 29.13, "end": 30.93, "lines": [{"text": "ОБНОВЛЕНИЕ", "accent": False, "size": "small"}, {"text": "БЕЗ СРАВНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 32.22, "end": 33.93, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.82, "end": 3.18}, {"start": 8.58, "end": 9.12}, {"start": 28.56, "end": 28.95}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (girl-bookshelf, 34.200s): getting lost in a long leaderboard
# among hundreds of unfamiliar names; the app shows only the change in
# position over the week instead of the absolute rank
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ТЕРЯЕШЬСЯ В РЕЙТИНГЕ", "СРЕДИ ЧУЖИХ ИМЕН?"], "end": 2.3}
g_cards = [
    {"start": 2.91, "end": 4.17, "lines": [{"text": "ТЕРЯЮТСЯ", "accent": False, "size": "small"}, {"text": "В ДЛИННОМ РЕЙТИНГЕ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 6.54, "lines": [{"text": "ПО ЕГЭ СРЕДИ СОТЕН", "accent": False, "size": "small"}, {"text": "НЕЗНАКОМЫХ ИМЕН", "accent": True, "size": "big"}]},
    {"start": 7.56, "end": 8.97, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.09, "end": 10.68, "lines": [{"text": "ТОЛЬКО РАЗНИЦУ МЕСТ", "accent": False, "size": "small"}, {"text": "ЗА НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 11.22, "end": 12.33, "lines": [{"text": "А НЕ", "accent": False, "size": "small"}, {"text": "АБСОЛЮТНУЮ", "accent": True, "size": "big"}]},
    {"start": 12.54, "end": 14.07, "lines": [{"text": "ПОЗИЦИЮ СРЕДИ ВСЕХ", "accent": False, "size": "small"}, {"text": "ПОДЪЕМ", "accent": True, "size": "big"}]},
    {"start": 14.19, "end": 15.03, "lines": [{"text": "НА НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "СТРОК", "accent": True, "size": "big"}]},
    {"start": 15.24, "end": 16.38, "lines": [{"text": "ЗАМЕТНЕЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "НОМЕР", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.52, "lines": [{"text": "СРЕДИ СОТЕН", "accent": False, "size": "small"}, {"text": "ИМЕН", "accent": True, "size": "big"}]},
    {"start": 18.12, "end": 19.77, "lines": [{"text": "ПРОЛИСТЫВАТЬ ВЕСЬ", "accent": False, "size": "small"}, {"text": "ДЛИННЫЙ РЕЙТИНГ", "accent": True, "size": "big"}]},
    {"start": 19.95, "end": 21.06, "lines": [{"text": "РАДИ ОДНОЙ", "accent": False, "size": "small"}, {"text": "СВОЕЙ СТРОКИ", "accent": True, "size": "big"}]},
    {"start": 21.33, "end": 23.22, "lines": [{"text": "НЕ ПРИХОДИТСЯ", "accent": False, "size": "small"}, {"text": "НЕБОЛЬШОЙ", "accent": True, "size": "big"}]},
    {"start": 23.31, "end": 24.27, "lines": [{"text": "ПОДЪЕМ ВИДЕН", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 24.81, "end": 26.10, "lines": [{"text": "БЕЗ ЧТЕНИЯ", "accent": False, "size": "small"}, {"text": "ЧУЖИХ ИМЕН", "accent": True, "size": "big"}]},
    {"start": 26.25, "end": 27.87, "lines": [{"text": "ВОКРУГ", "accent": False, "size": "small"}, {"text": "РАЗНИЦА", "accent": True, "size": "big"}]},
    {"start": 28.02, "end": 29.52, "lines": [{"text": "МЕСТ ЗА НЕДЕЛЮ", "accent": False, "size": "small"}, {"text": "ЗАМЕТНЕЕ", "accent": True, "size": "big"}]},
    {"start": 29.76, "end": 31.35, "lines": [{"text": "ЧЕМ НОМЕР", "accent": False, "size": "small"}, {"text": "СРЕДИ СОТЕН ИМЕН", "accent": True, "size": "big"}]},
    {"start": 32.25, "end": 33.99, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.91, "end": 3.27}, {"start": 8.49, "end": 8.97}, {"start": 23.31, "end": 23.55}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (warm-sweater girl, 30.295s): the daily task topic doesn't fit
# the evening; the app lets you swap it for a different topic once a day
# without losing the streak
# ---------------------------------------------------------------------------
h_intro = {"lines": ["ТЕМА НЕ ИДЕТ", "В ЭТОТ ВЕЧЕР?"], "end": 2.3}
h_cards = [
    {"start": 2.49, "end": 3.39, "lines": [{"text": "ПО ЕГЭ НА", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.86, "lines": [{"text": "КОТОРАЯ СОВСЕМ", "accent": False, "size": "small"}, {"text": "НЕ ИДЕТ", "accent": True, "size": "big"}]},
    {"start": 4.98, "end": 7.20, "lines": [{"text": "В ЭТОТ ВЕЧЕР", "accent": False, "size": "small"}, {"text": "ЕГЭ ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 7.38, "end": 8.37, "lines": [{"text": "ПОЗВОЛЯЕТ", "accent": False, "size": "small"}, {"text": "ЗАМЕНИТЬ", "accent": True, "size": "big"}]},
    {"start": 8.52, "end": 10.14, "lines": [{"text": "ЗАДАНИЕ ДНЯ НА ДРУГУЮ", "accent": False, "size": "small"}, {"text": "ТЕМУ", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 11.34, "lines": [{"text": "ОДИН РАЗ", "accent": False, "size": "small"}, {"text": "В СУТКИ", "accent": True, "size": "big"}]},
    {"start": 11.97, "end": 12.90, "lines": [{"text": "БЕЗ ПОТЕРИ", "accent": False, "size": "small"}, {"text": "СЕРИИ", "accent": True, "size": "big"}]},
    {"start": 13.56, "end": 14.61, "lines": [{"text": "НЕПОДХОДЯЩАЯ", "accent": False, "size": "small"}, {"text": "ТЕМА", "accent": True, "size": "big"}]},
    {"start": 14.82, "end": 16.20, "lines": [{"text": "МЕНЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ОДНИМ НАЖАТИЕМ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.73, "lines": [{"text": "И НЕ ПРОПУСКАЮТСЯ", "accent": False, "size": "small"}, {"text": "СОВСЕМ", "accent": True, "size": "big"}]},
    {"start": 18.42, "end": 20.04, "lines": [{"text": "ОСТАВЛЯТЬ СЕРИЮ", "accent": False, "size": "small"}, {"text": "БЕЗ ВЫПОЛНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 20.28, "end": 21.75, "lines": [{"text": "РАДИ ОДНОЙ", "accent": False, "size": "small"}, {"text": "НЕУДАЧНОЙ ТЕМЫ", "accent": True, "size": "big"}]},
    {"start": 22.08, "end": 24.18, "lines": [{"text": "НЕ ТРЕБУЕТСЯ НЕПОДХОДЯЩАЯ", "accent": False, "size": "small"}, {"text": "ТЕМА", "accent": True, "size": "big"}]},
    {"start": 24.63, "end": 25.62, "lines": [{"text": "МЕНЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ОДИН РАЗ", "accent": True, "size": "big"}]},
    {"start": 25.77, "end": 27.39, "lines": [{"text": "В СУТКИ", "accent": False, "size": "small"}, {"text": "БЕЗ ПОТЕРИ СЕРИИ", "accent": True, "size": "big"}]},
    {"start": 28.14, "end": 29.61, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 8.10, "end": 8.37}, {"start": 14.82, "end": 15.21}, {"start": 24.63, "end": 25.02}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (warm-sweater girl, 32.578s): skipping past a formula in a video
# walkthrough without understanding it; the app pauses the video on the
# formula until it's marked as understood
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ПРОЛИСТЫВАЕШЬ ФОРМУЛУ", "НЕ РАЗОБРАВШИСЬ?"], "end": 2.3}
i_cards = [
    {"start": 2.58, "end": 3.81, "lines": [{"text": "ЗАДАНИЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "МИМО", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.70, "lines": [{"text": "ФОРМУЛЫ НЕ РАЗОБРАВШИСЬ В НЕЙ", "accent": False, "size": "small"}, {"text": "ТОЛКОМ", "accent": True, "size": "big"}]},
    {"start": 6.63, "end": 8.52, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР ОСТАНАВЛИВАЕТ", "accent": False, "size": "small"}, {"text": "РОЛИК", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 9.96, "lines": [{"text": "САМ НА МЕСТЕ", "accent": False, "size": "small"}, {"text": "С ФОРМУЛОЙ", "accent": True, "size": "big"}]},
    {"start": 10.50, "end": 11.61, "lines": [{"text": "ПОКА ОНА НЕ", "accent": False, "size": "small"}, {"text": "ОТМЕЧЕНА", "accent": True, "size": "big"}]},
    {"start": 11.73, "end": 13.62, "lines": [{"text": "ПОНЯТНОЙ", "accent": False, "size": "small"}, {"text": "ПРОЛИСТАТЬ ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 14.91, "lines": [{"text": "НЕ РАЗОБРАВШИСЬ", "accent": False, "size": "small"}, {"text": "МИМО", "accent": True, "size": "big"}]},
    {"start": 15.27, "end": 16.59, "lines": [{"text": "ЗДЕСЬ ПРОСТО НЕ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИТСЯ", "accent": True, "size": "big"}]},
    {"start": 17.67, "end": 18.90, "lines": [{"text": "ОТМЕЧАТЬ ПАУЗУ", "accent": False, "size": "small"}, {"text": "ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 19.14, "end": 20.10, "lines": [{"text": "КНОПКОЙ КАЖДЫЙ", "accent": False, "size": "small"}, {"text": "РАЗ", "accent": True, "size": "big"}]},
    {"start": 20.37, "end": 21.81, "lines": [{"text": "НЕ ТРЕБУЕТСЯ", "accent": False, "size": "small"}, {"text": "РОЛИК", "accent": True, "size": "big"}]},
    {"start": 21.90, "end": 23.25, "lines": [{"text": "ПРОДОЛЖАЕТСЯ ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ПОСЛЕ", "accent": True, "size": "big"}]},
    {"start": 23.40, "end": 24.27, "lines": [{"text": "ЧЕСТНОГО", "accent": False, "size": "small"}, {"text": "НАЖАТИЯ", "accent": True, "size": "big"}]},
    {"start": 24.54, "end": 25.74, "lines": [{"text": "ПОНЯТНО ПОД", "accent": False, "size": "small"}, {"text": "ФОРМУЛОЙ", "accent": True, "size": "big"}]},
    {"start": 26.46, "end": 27.78, "lines": [{"text": "РОЛИК САМ", "accent": False, "size": "small"}, {"text": "СТОИТ НА ФОРМУЛЕ", "accent": True, "size": "big"}]},
    {"start": 28.08, "end": 29.19, "lines": [{"text": "ПОКА ОНА НЕ", "accent": False, "size": "small"}, {"text": "ОТМЕЧЕНА", "accent": True, "size": "big"}]},
    {"start": 29.34, "end": 30.69, "lines": [{"text": "ПОНЯТНОЙ", "accent": True, "size": "big"}]},
    {"start": 30.69, "end": 32.34, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 1.29, "end": 1.83}, {"start": 7.53, "end": 8.13}, {"start": 21.90, "end": 22.53}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
