#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-THIRD 'coffee123'
batch (9 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes90/.

Three returning hosts, no new faces: "Рома" / tight curls, black
Under Armour hoodie (a, f, h), "mother" / brunette, bookshelf+doorway
(b, g), "teen boy on couch" / wavy hair, gray tee (c, d, i), "blonde
in cream sweater" / desk+lamp+notebook (e).

Sub-themes: winning arguments with friends but losing to social-studies
terms on the EGE, a list of dreaded EGE tasks that only shrinks once
tackled one a day, solving a task to music and getting thrown off by
lyrics, an unreadable handwritten solution from a classmate forcing a
guess, a noisy cafeteria making long reading impossible but short
Q&A fine, a two-page breakdown that gets abandoned on line two, a
daughter's comma-less texting habit turned into punctuation practice,
a cousin's vague "solve more" advice with no actual number, and a
father's dinner-table history quiz answered right one time in three.
"""
import json

REAL_DURATION = {
    "a": 17.360, "b": 18.327, "c": 18.400,
    "d": 17.964, "e": 20.631, "f": 16.684,
    "g": 19.586, "h": 17.218, "i": 18.120,
}
SOURCE_FILE = {
    "a": "bdshgfvdsfvgwff", "b": "dfsfdsfdsfdsgsdb", "c": "dsfvbsbhdsgvg",
    "d": "fbdgbvvbvgwggfwvf", "e": "fdfsfsdfdsfs", "f": "fdhbgbwgrggvs",
    "g": "gdsgsgbbgwgbeg", "h": "vdsgvvsdfsfgvdf", "i": "vdswggbfgsfdsfdsf",
}
FIXES = {
    "a": {"спорох": "спорах", "побществознанию": "обществознанию"},
    "d": {"тренажери": "тренажере"},
    "f": {"текстовая": "текстовый"},
    "g": {"тигры": "игры"},
    "i": {"ат": "а", "профия": "профиля"},
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


def fix_words(letter, words):
    fixes = FIXES.get(letter, {})
    out = []
    for w in words:
        t = w["text"]
        if t in fixes:
            t = fixes[t]
        out.append({"text": t, "start": w["start"], "end": w["end"]})
    return out


def build_running_caption(words):
    return [{"text": w["text"].upper(), "start": w["start"], "end": w["end"]} for w in words]


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    stem = SOURCE_FILE[letter]
    with open(f"../asr_coffee123_43/{stem}_words.json", encoding="utf-8") as f:
        words = json.load(f)
    words = fix_words(letter, words)

    check_cards(letter, cards, total_duration)
    check_intro_vs_cards(letter, intro["end"], cards)
    check_emphasis(letter, emphasis, total_duration)

    running_caption = build_running_caption(words)

    with open(f"ep_{letter}_cards.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_intro.json", "w", encoding="utf-8") as f:
        json.dump(intro, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_emphasis.json", "w", encoding="utf-8") as f:
        json.dump(emphasis, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_running_caption.json", "w", encoding="utf-8") as f:
        json.dump(running_caption, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_stock_cutaways.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_duration.json", "w", encoding="utf-8") as f:
        json.dump({"total_duration": total_duration}, f, ensure_ascii=False, indent=2)
    with open(f"ep_{letter}_words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print(f"ep{letter}: OK, {len(cards)} cards, {len(words)} words, duration {total_duration}s")


# ---------------------------------------------------------------------------
# Episode A (Рома, 17.360s): wins every argument with friends with easy
# reasoning, but the EGE in social studies doesn't want arguments, it
# wants terms -- and terms stick only in fragments, like song lyrics,
# surfacing the wrong one at the wrong moment; the app's memory games
# drill terms until they come back whole
# ---------------------------------------------------------------------------
a_intro = {"lines": ["В СПОРЕ ПОБЕЖДАЕШЬ", "А НА ЕГЭ ТЕРМИНЫ ЗАБЫВАЕШЬ?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 2.91, "lines": [{"text": "В СПОРАХ С ДРУЗЬЯМИ", "accent": False, "size": "small"}, {"text": "ЛЕГКО ПРИВОЖУ ДОВОДЫ", "accent": True, "size": "big"}]},
    {"start": 2.91, "end": 4.41, "lines": [{"text": "А НА ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 4.59, "end": 5.82, "lines": [{"text": "НУЖНЫ НЕ ДОВОДЫ", "accent": False, "size": "small"}, {"text": "А ТЕРМИНЫ", "accent": True, "size": "big"}]},
    {"start": 6.27, "end": 7.44, "lines": [{"text": "ТЕРМИНЫ Я ЗНАЮ", "accent": False, "size": "small"}, {"text": "ОБРЫВКАМИ", "accent": True, "size": "big"}]},
    {"start": 7.62, "end": 8.49, "lines": [{"text": "КАК СЛОВА", "accent": False, "size": "small"}, {"text": "ИЗ ПЕСНИ", "accent": True, "size": "big"}]},
    {"start": 8.73, "end": 10.32, "lines": [{"text": "В НУЖНЫЙ МОМЕНТ", "accent": False, "size": "small"}, {"text": "ВСПОМИНАЮ НЕ ТЕ", "accent": True, "size": "big"}]},
    {"start": 10.68, "end": 12.18, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 12.42, "end": 13.56, "lines": [{"text": "ЕСТЬ ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 13.74, "end": 15.36, "lines": [{"text": "ГДЕ ТЕРМИНЫ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮТСЯ ПОЛНОСТЬЮ", "accent": True, "size": "small"}]},
    {"start": 15.63, "end": 16.47, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 17.360, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 3.36, "end": 4.05}, {"start": 6.27, "end": 6.54}, {"start": 9.48, "end": 9.87}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 18.327s): a daughter's list of dreaded EGE tasks
# grows from three to eleven in a week; tackling just one dreaded task
# a day finally makes the list start shrinking; the app's FIPI bank
# keeps everything in one place so the dreaded ones are easy to find
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СПИСОК СТРАШНЫХ ЗАДАНИЙ", "ТОЛЬКО РАСТЕТ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 2.67, "lines": [{"text": "ДОЧЬ ВЕДЕТ", "accent": False, "size": "small"}, {"text": "СПИСОК СТРАШНЫХ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 2.91, "end": 5.10, "lines": [{"text": "ЗА НЕДЕЛЮ ВЫРОС", "accent": False, "size": "small"}, {"text": "С ТРЕХ ДО ОДИННАДЦАТИ", "accent": True, "size": "small"}]},
    {"start": 6.36, "end": 8.52, "lines": [{"text": "Я ПРЕДЛОЖИЛА", "accent": False, "size": "small"}, {"text": "ПО ОДНОМУ В ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 8.88, "end": 10.20, "lines": [{"text": "И СПИСОК", "accent": False, "size": "small"}, {"text": "НАЧАЛ СОКРАЩАТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 10.86, "end": 12.18, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.77, "lines": [{"text": "ГДЕ ВСЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ЛЕЖАТ В ОДНОМ МЕСТЕ", "accent": True, "size": "big"}]},
    {"start": 13.89, "end": 15.93, "lines": [{"text": "И СТРАШНОЕ", "accent": False, "size": "small"}, {"text": "ЛЕГКО НАЙТИ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.40, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.327, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.62, "end": 5.10}, {"start": 9.69, "end": 10.20}, {"start": 15.48, "end": 15.93}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (teen boy on couch, 18.400s): solving an EGE task to music
# throws him off more on songs with lyrics than instrumentals, but
# picking a playlist is its own ten-minute chore before the first task
# even starts; the app's FIPI bank opens the task instantly, before the
# playlist gets a chance to distract
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПЕСНЯ СО СЛОВАМИ", "СБИВАЕТ С ЕГЭ?"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 2.70, "lines": [{"text": "РЕШАЮ ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОД МУЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 2.70, "end": 4.53, "lines": [{"text": "НА ПЕСНЕ СО СЛОВАМИ", "accent": False, "size": "small"}, {"text": "СБИВАЮСЬ ЧАЩЕ", "accent": True, "size": "small"}]},
    {"start": 5.07, "end": 5.88, "lines": [{"text": "ЧЕМ НА", "accent": False, "size": "small"}, {"text": "ИНСТРУМЕНТАЛЬНОЙ", "accent": True, "size": "small"}]},
    {"start": 6.15, "end": 7.23, "lines": [{"text": "НО ВЫБИРАТЬ", "accent": False, "size": "small"}, {"text": "ПЛЕЙЛИСТ", "accent": True, "size": "big"}]},
    {"start": 7.53, "end": 9.42, "lines": [{"text": "ЭТО ОТДЕЛЬНОЕ ЗАНЯТИЕ", "accent": False, "size": "small"}, {"text": "НА ДЕСЯТЬ МИНУТ", "accent": True, "size": "big"}]},
    {"start": 9.63, "end": 11.04, "lines": [{"text": "ЕЩЕ ДО", "accent": False, "size": "small"}, {"text": "ПЕРВОГО ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 11.43, "end": 12.81, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.61, "lines": [{"text": "ГДЕ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ОТКРЫВАЕТСЯ СРАЗУ", "accent": True, "size": "small"}]},
    {"start": 14.82, "end": 16.32, "lines": [{"text": "ПОКА ПЛЕЙЛИСТ", "accent": False, "size": "small"}, {"text": "НЕ УСПЕЛ ОТВЛЕЧЬ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.56, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.56, "end": 18.400, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 4.05, "end": 4.53}, {"start": 6.84, "end": 7.23}, {"start": 15.66, "end": 16.32}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (teen boy on couch, 17.964s): a classmate's photographed
# solution to an EGE task is in handwriting so bad that only three of
# ten lines are legible, and the rest gets guessed and retold back to
# her as a solution she never actually had; the app's text breakdown is
# typed plainly and reads whole
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПОЧЕРК НЕ РАЗОБРАТЬ", "РЕШЕНИЕ ПРИДУМЫВАЕШЬ САМ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.30, "lines": [{"text": "ОДНОКЛАССНИЦА ПРИСЛАЛА", "accent": False, "size": "small"}, {"text": "ФОТО РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 3.54, "end": 4.56, "lines": [{"text": "А ПОЧЕРК У НЕЕ", "accent": False, "size": "small"}, {"text": "ТАКОЙ", "accent": True, "size": "big"}]},
    {"start": 4.77, "end": 6.24, "lines": [{"text": "РАЗОБРАЛ ТРИ СТРОКИ", "accent": False, "size": "small"}, {"text": "ИЗ ДЕСЯТИ", "accent": True, "size": "big"}]},
    {"start": 6.57, "end": 7.83, "lines": [{"text": "ОСТАЛЬНЫЕ СЕМЬ", "accent": False, "size": "small"}, {"text": "Я УГАДЫВАЛ", "accent": True, "size": "big"}]},
    {"start": 8.01, "end": 9.93, "lines": [{"text": "И ПЕРЕСКАЗАЛ ЕЙ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.93, "end": 10.80, "lines": [{"text": "КОТОРОГО У НЕЕ", "accent": False, "size": "small"}, {"text": "НЕ БЫЛО", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 12.45, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 12.60, "end": 13.68, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.90, "lines": [{"text": "НАБРАННЫЙ КАК ТЕКСТ", "accent": False, "size": "small"}, {"text": "И ЧИТАЕТСЯ ЦЕЛИКОМ", "accent": True, "size": "big"}]},
    {"start": 16.17, "end": 17.10, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 17.964, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 3.63, "end": 3.96}, {"start": 8.43, "end": 8.82}, {"start": 14.91, "end": 15.24}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde in cream sweater, 20.631s): a noisy cafeteria makes
# re-reading Russian-language rules for the EGE impossible, catching
# herself on the same line ten times -- but short question-and-answer
# format barely gets touched by the noise; the app's Russian-language
# memory games are built on exactly that short format
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ШУМНАЯ СТОЛОВАЯ", "И ПРАВИЛА НЕ ЛЕЗУТ В ГОЛОВУ?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.33, "lines": [{"text": "В ШУМНОЙ СТОЛОВОЙ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯЮ ПРАВИЛА", "accent": True, "size": "small"}]},
    {"start": 3.33, "end": 4.86, "lines": [{"text": "РУССКОГО", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.37, "end": 7.44, "lines": [{"text": "И ЛОВЛЮ СЕБЯ", "accent": False, "size": "small"}, {"text": "НА ОДНОЙ СТРОЧКЕ", "accent": True, "size": "big"}]},
    {"start": 8.25, "end": 9.60, "lines": [{"text": "ШУМ МЕШАЕТ", "accent": False, "size": "small"}, {"text": "ДЛИННОМУ ЧТЕНИЮ", "accent": True, "size": "small"}]},
    {"start": 10.17, "end": 12.39, "lines": [{"text": "А КОРОТКИЕ ВОПРОСЫ", "accent": False, "size": "small"}, {"text": "ОН ПОЧТИ НЕ ПОРТИТ", "accent": True, "size": "big"}]},
    {"start": 13.41, "end": 14.91, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 15.27, "end": 16.38, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.68, "end": 18.15, "lines": [{"text": "ПОСТРОЕННЫЕ НА", "accent": False, "size": "small"}, {"text": "КОРОТКИХ ВОПРОСАХ", "accent": True, "size": "big"}]},
    {"start": 18.81, "end": 19.73, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.73, "end": 20.631, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 6.75, "end": 7.44}, {"start": 8.85, "end": 9.60}, {"start": 17.79, "end": 18.15}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (Рома, 16.684s): a two-page EGE task breakdown gets
# abandoned on the second line; what he actually needs is for the main
# point to fit on one screen and get read to the end; the app's
# breakdown is split into short steps, one per screen
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РАЗБОР НА ДВЕ СТРАНИЦЫ", "ЗАКРЫВАЕШЬ НА ВТОРОЙ СТРОКЕ?"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.18, "lines": [{"text": "НЕ ЛЮБЛЮ ЧИТАТЬ", "accent": False, "size": "small"}, {"text": "ДЛИННЫЕ ТЕКСТЫ", "accent": True, "size": "small"}]},
    {"start": 3.39, "end": 4.23, "lines": [{"text": "РАЗБОР ЗАДАНИЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "НА ДВЕ СТРАНИЦЫ", "accent": True, "size": "small"}]},
    {"start": 4.47, "end": 5.70, "lines": [{"text": "ЗАКРЫВАЮ", "accent": False, "size": "small"}, {"text": "НА ВТОРОЙ СТРОКЕ", "accent": True, "size": "big"}]},
    {"start": 6.03, "end": 7.65, "lines": [{"text": "МНЕ НУЖНО ЧТОБЫ", "accent": False, "size": "small"}, {"text": "ГЛАВНОЕ ПОМЕЩАЛОСЬ", "accent": True, "size": "small"}]},
    {"start": 7.83, "end": 8.63, "lines": [{"text": "НА ОДИН", "accent": False, "size": "small"}, {"text": "ЭКРАН", "accent": True, "size": "big"}]},
    {"start": 8.64, "end": 9.63, "lines": [{"text": "И ДОЧИТЫВАЛОСЬ", "accent": False, "size": "small"}, {"text": "ДО КОНЦА", "accent": True, "size": "big"}]},
    {"start": 10.05, "end": 11.34, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ТЕКСТОВЫЙ", "accent": True, "size": "small"}]},
    {"start": 11.55, "end": 12.99, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "КОРОТКИМИ ШАГАМИ", "accent": True, "size": "small"}]},
    {"start": 13.11, "end": 14.40, "lines": [{"text": "ПО ОДНОМУ", "accent": False, "size": "small"}, {"text": "НА ЭКРАН", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.77, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 15.77, "end": 16.684, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.19, "end": 5.70}, {"start": 7.95, "end": 8.40}, {"start": 13.56, "end": 13.89}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (mother, 19.586s): a daughter texts friends with zero
# commas and it worries her that the Russian-language EGE won't go
# well either -- turning comma-counting in her own texts into practice
# wins her over out of pure curiosity; the app's memory games train
# exactly that inside a game
# ---------------------------------------------------------------------------
g_intro = {"lines": ["ПИШЕТ БЕЗ ЗАПЯТЫХ", "А ЕГЭ УЖЕ СКОРО?"], "end": 1.86}
g_cards = [
    {"start": 1.86, "end": 3.12, "lines": [{"text": "ДОЧЬ ПИШЕТ", "accent": False, "size": "small"}, {"text": "СООБЩЕНИЯ ПОДРУГАМ", "accent": True, "size": "small"}]},
    {"start": 3.12, "end": 4.26, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ЗАПЯТЫХ", "accent": True, "size": "big"}]},
    {"start": 4.41, "end": 5.61, "lines": [{"text": "МНЕ СТРАШНО ЧТО", "accent": False, "size": "small"}, {"text": "ЕГЭ НЕ СДАСТ", "accent": True, "size": "big"}]},
    {"start": 6.21, "end": 7.71, "lines": [{"text": "Я ПРЕДЛОЖИЛА", "accent": False, "size": "small"}, {"text": "СЧИТАТЬ ЗАПЯТЫЕ", "accent": True, "size": "big"}]},
    {"start": 7.83, "end": 9.18, "lines": [{"text": "В СООБЩЕНИЯХ", "accent": False, "size": "small"}, {"text": "КАК ТРЕНИРОВКУ", "accent": True, "size": "small"}]},
    {"start": 9.57, "end": 11.16, "lines": [{"text": "И ОНА СОГЛАСИЛАСЬ", "accent": False, "size": "small"}, {"text": "ИЗ ЛЮБОПЫТСТВА", "accent": True, "size": "small"}]},
    {"start": 11.82, "end": 13.41, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО РУССКОМУ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 13.92, "end": 15.06, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 15.45, "end": 16.92, "lines": [{"text": "ГДЕ ЗАПЯТЫЕ", "accent": False, "size": "small"}, {"text": "ТРЕНИРУЮТСЯ В ИГРЕ", "accent": True, "size": "small"}]},
    {"start": 17.58, "end": 18.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.60, "end": 19.586, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.46, "end": 2.76}, {"start": 9.87, "end": 10.35}, {"start": 15.72, "end": 15.99}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (Рома, 17.218s): a cousin who passed the EGE last year keeps
# saying "solve more" but never explains how much is actually enough,
# leaving no way to judge whether the total amount of practice is
# anywhere close to sufficient; the app's FIPI bank is sorted by number
# so the overall volume can actually be measured
# ---------------------------------------------------------------------------
h_intro = {"lines": ["РЕШАЙ ПОБОЛЬШЕ", "НО СКОЛЬКО ИМЕННО?"], "end": 1.86}
h_cards = [
    {"start": 1.86, "end": 3.51, "lines": [{"text": "ДВОЮРОДНЫЙ БРАТ", "accent": False, "size": "small"}, {"text": "СДАЛ ЕГЭ В ПРОШЛОМ ГОДУ", "accent": True, "size": "big"}]},
    {"start": 3.51, "end": 4.80, "lines": [{"text": "И ГОВОРИТ", "accent": False, "size": "small"}, {"text": "РЕШАЙ ПОБОЛЬШЕ", "accent": True, "size": "big"}]},
    {"start": 5.04, "end": 6.03, "lines": [{"text": "НО СКОЛЬКО", "accent": False, "size": "small"}, {"text": "НЕ ОБЪЯСНИЛ", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.38, "lines": [{"text": "Я НЕ ЗНАЮ", "accent": False, "size": "small"}, {"text": "КАКОЕ ЧИСЛО", "accent": True, "size": "big"}]},
    {"start": 7.53, "end": 8.97, "lines": [{"text": "СЧИТАТЬ", "accent": False, "size": "small"}, {"text": "ДОСТАТОЧНЫМ", "accent": True, "size": "small"}]},
    {"start": 8.97, "end": 10.26, "lines": [{"text": "НУЖНО ХОТЯ БЫ", "accent": False, "size": "small"}, {"text": "ПОНЯТЬ ОБЪЕМ", "accent": True, "size": "big"}]},
    {"start": 10.71, "end": 12.36, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ЕСТЬ БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 12.51, "end": 13.74, "lines": [{"text": "ГДЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ИДУТ ПО НОМЕРАМ", "accent": True, "size": "big"}]},
    {"start": 13.98, "end": 15.09, "lines": [{"text": "И ОБЪЕМ", "accent": False, "size": "small"}, {"text": "МОЖНО ОЦЕНИТЬ", "accent": True, "size": "big"}]},
    {"start": 15.42, "end": 16.35, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.35, "end": 17.218, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 1.92, "end": 2.34}, {"start": 7.53, "end": 8.10}, {"start": 14.13, "end": 14.58}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (teen boy on couch, 18.120s): a father's dinner-table EGE
# history-date quiz gets answered correctly only about one time in
# three, and the dates stay the same every time because they only get
# studied right before a test; the app's memory games let dates get
# repeated every day instead
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ДАТЫ ПО ИСТОРИИ", "ПОМНИШЬ ОДНУ ИЗ ТРЕХ?"], "end": 1.86}
i_cards = [
    {"start": 1.86, "end": 3.09, "lines": [{"text": "ПАПА ЗА УЖИНОМ", "accent": False, "size": "small"}, {"text": "СПРАШИВАЕТ ДАТЫ", "accent": True, "size": "small"}]},
    {"start": 3.09, "end": 4.68, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.12, "lines": [{"text": "ОТВЕЧАЮ ПРАВИЛЬНО", "accent": False, "size": "small"}, {"text": "ОДИН СЛУЧАЙ ИЗ ТРЕХ", "accent": True, "size": "big"}]},
    {"start": 6.45, "end": 7.83, "lines": [{"text": "ОН СМЕЕТСЯ", "accent": False, "size": "small"}, {"text": "Я КРАСНЕЮ", "accent": True, "size": "big"}]},
    {"start": 8.16, "end": 9.21, "lines": [{"text": "А ДАТЫ", "accent": False, "size": "small"}, {"text": "ОСТАЮТСЯ ТЕ ЖЕ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 11.19, "lines": [{"text": "ПОТОМУ ЧТО УЧУ ИХ", "accent": False, "size": "small"}, {"text": "ПЕРЕД КОНТРОЛЬНОЙ", "accent": True, "size": "small"}]},
    {"start": 11.49, "end": 12.72, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "ПО ИСТОРИИ ЕСТЬ", "accent": True, "size": "small"}]},
    {"start": 12.93, "end": 14.07, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 14.25, "end": 15.78, "lines": [{"text": "ГДЕ ДАТЫ МОЖНО", "accent": False, "size": "small"}, {"text": "ПОВТОРЯТЬ КАЖДЫЙ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 17.25, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 17.25, "end": 18.120, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 6.45, "end": 6.72}, {"start": 8.16, "end": 8.43}, {"start": 14.76, "end": 15.09}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
