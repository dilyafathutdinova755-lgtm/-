#!/usr/bin/env python3
"""One-off authoring + validation script for the FORTY-SECOND 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes89/.

Two returning hosts, no new faces: "blonde in cream sweater" (a, c, f),
"blue-shirt brunette" / THE SMITHS poster room (b, d, e).

Sub-themes: a whispered task explanation from an older brother that
keeps losing both of them their train of thought, a teacher's "see the
breakdown" note with nowhere to actually find one, a list of rulers
that only holds in strict order and collapses out of sequence, an
elevator-ride window too short to answer a social-studies term, a
weekly-schedule cell that stays empty three weeks running, and a
friend's retelling of a task that changes phrasing every time.
"""
import json

REAL_DURATION = {
    "a": 22.850, "b": 20.460, "c": 21.058,
    "d": 23.340, "e": 24.087, "f": 21.122,
}
SOURCE_FILE = {
    "a": "dsvsbvbwrnbwbh", "b": "fdvdbegbvfbsdgv", "c": "fsvsbhhbrewhwg",
    "d": "gdffdgdbgfdbgvve", "e": "gfgdgddfgfdgd", "f": "vbgdfbdbdgbv",
}
FIXES = {
    "a": {"ему": "мы"},
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
    with open(f"../asr_coffee123_42/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (blonde cream sweater, 22.850s): an older brother explains
# an ЕГЭ task in a whisper to avoid waking mom, half the words get
# missed, asking again makes him irritated, and they both lose their
# train of thought -- the evening yields just one task; the app's text
# breakdown can be read calmly in silence
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ШЕПОТОМ ЧТОБЫ", "НЕ РАЗБУДИТЬ МАМУ?"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.36, "lines": [{"text": "СТАРШИЙ БРАТ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ ШЕПОТОМ", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 4.83, "lines": [{"text": "ЧТОБЫ НЕ", "accent": False, "size": "small"}, {"text": "РАЗБУДИТЬ МАМУ", "accent": True, "size": "big"}]},
    {"start": 5.31, "end": 6.96, "lines": [{"text": "И ПОЛОВИНУ СЛОВ Я", "accent": False, "size": "small"}, {"text": "НЕ РАЗБИРАЮ", "accent": True, "size": "big"}]},
    {"start": 7.65, "end": 9.63, "lines": [{"text": "Я ПЕРЕСПРАШИВАЮ", "accent": False, "size": "small"}, {"text": "ОН РАЗДРАЖАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 9.99, "end": 11.28, "lines": [{"text": "МЫ ОБА", "accent": False, "size": "small"}, {"text": "СБИВАЕМСЯ С МЫСЛИ", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 13.89, "lines": [{"text": "ПОЭТОМУ ЗА ВЕЧЕР", "accent": False, "size": "small"}, {"text": "ВЫХОДИТ ОДНО ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 15.54, "end": 16.53, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 18.09, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 18.48, "end": 20.31, "lines": [{"text": "КОТОРЫЙ МОЖНО", "accent": False, "size": "small"}, {"text": "СПОКОЙНО ЧИТАТЬ В ТИШИНЕ", "accent": True, "size": "big"}]},
    {"start": 20.97, "end": 22.02, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.02, "end": 22.850, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 8.85, "end": 9.63}, {"start": 12.60, "end": 13.08}, {"start": 19.10, "end": 19.50}]
process("a", a_cards, a_intro, a_emphasis)
# NB: ASR mishears "мы" as "ему" here (see FIXES["a"]); card text above
# spells it correctly regardless.


# ---------------------------------------------------------------------------
# Episode B (blue-shirt brunette, 20.460s): a teacher wrote "see the
# breakdown" on an ЕГЭ paper but never explained where to find one;
# classmates each named a different source and the resulting answers
# came out different; the app's text breakdown sits right next to the
# task itself
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СМОТРИ РАЗБОР", "НО ГДЕ ЕГО ИСКАТЬ?"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 4.29, "lines": [{"text": "НА МОЕЙ РАБОТЕ ПО ЕГЭ УЧИТЕЛЬ ПИШЕТ", "accent": False, "size": "small"}, {"text": "СМОТРИ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 4.29, "end": 6.18, "lines": [{"text": "А ГДЕ ЭТОТ РАЗБОР", "accent": False, "size": "small"}, {"text": "ИСКАТЬ НЕ ОБЪЯСНИЛ", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 8.28, "lines": [{"text": "Я СПРОСИЛА У", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИКОВ", "accent": True, "size": "small"}]},
    {"start": 8.49, "end": 10.02, "lines": [{"text": "И КАЖДЫЙ НАЗВАЛ", "accent": False, "size": "small"}, {"text": "СВОЙ ИСТОЧНИК", "accent": True, "size": "big"}]},
    {"start": 10.53, "end": 12.30, "lines": [{"text": "А РЕШЕНИЕ У ВСЕХ", "accent": False, "size": "small"}, {"text": "ПОЛУЧИЛИСЬ РАЗНЫМИ", "accent": True, "size": "small"}]},
    {"start": 13.08, "end": 13.92, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.92, "end": 14.76, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 14.76, "end": 16.17, "lines": [{"text": "ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.17, "end": 18.00, "lines": [{"text": "КОТОРЫЙ ЛЕЖИТ РЯДОМ", "accent": False, "size": "small"}, {"text": "С САМИМ ЗАДАНИЕМ", "accent": True, "size": "big"}]},
    {"start": 18.63, "end": 19.60, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.60, "end": 20.460, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 5.65, "end": 6.18}, {"start": 11.75, "end": 12.30}, {"start": 17.40, "end": 18.00}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blonde cream sweater, 21.058s): a list of history rulers
# memorized strictly in order falls apart the moment it's asked out of
# sequence -- can't name even the second one without starting from the
# very beginning and climbing the list like steps; the app's history
# memory games shuffle the questions on purpose
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ТОЛЬКО ПО ПОРЯДКУ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.51, "lines": [{"text": "СПИСОК ПРАВИТЕЛЕЙ", "accent": False, "size": "small"}, {"text": "Я ВЫУЧИЛА ПО ПОРЯДКУ", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 6.66, "lines": [{"text": "А ВНЕ ПОРЯДКА НЕ МОГУ", "accent": False, "size": "small"}, {"text": "НАЗВАТЬ ДАЖЕ ВТОРОГО", "accent": True, "size": "big"}]},
    {"start": 7.47, "end": 8.55, "lines": [{"text": "ПОРЯДОК", "accent": False, "size": "small"}, {"text": "ДЕРЖИТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 10.23, "lines": [{"text": "ТОЛЬКО ЕСЛИ Я", "accent": False, "size": "small"}, {"text": "НАЧИНАЮ С САМОГО НАЧАЛА", "accent": True, "size": "big"}]},
    {"start": 10.59, "end": 12.18, "lines": [{"text": "И ИДУ ПО СПИСКУ", "accent": False, "size": "small"}, {"text": "КАК ПО СТУПЕНЬКАМ", "accent": True, "size": "big"}]},
    {"start": 13.83, "end": 14.64, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.64, "end": 15.63, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 15.63, "end": 16.98, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 16.98, "end": 18.45, "lines": [{"text": "ГДЕ ВОПРОСЫ ИДУТ", "accent": False, "size": "small"}, {"text": "ВПЕРЕМЕШКУ", "accent": True, "size": "big"}]},
    {"start": 19.20, "end": 20.22, "lines": [{"text": "ССЫЛКА НА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.22, "end": 21.058, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 7.70, "end": 8.22}, {"start": 11.60, "end": 12.18}, {"start": 17.85, "end": 18.45}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 23.340s): a neighbor's elevator-ride
# question about a social-studies term leaves no time to answer before
# the floor arrives -- three floors is three seconds, and the right
# answer always surfaces on the fourth floor, doors already open; the
# app's memory games train answering fast
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ТРИ ЭТАЖА", "ТРИ СЕКУНДЫ?"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.66, "lines": [{"text": "СОСЕД В ЛИФТЕ", "accent": False, "size": "small"}, {"text": "ИНОГДА СПРАШИВАЕТ", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 4.71, "lines": [{"text": "У МЕНЯ ТЕРМИН ПО", "accent": False, "size": "small"}, {"text": "ОБЩЕСТВОЗНАНИЮ", "accent": True, "size": "small"}]},
    {"start": 4.71, "end": 6.75, "lines": [{"text": "ДЛЯ ЕГЭ И Я", "accent": False, "size": "small"}, {"text": "НЕ УСПЕВАЮ ОТВЕТИТЬ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.45, "lines": [{"text": "ТРИ ЭТАЖА ЭТО", "accent": False, "size": "small"}, {"text": "ТРИ СЕКУНДЫ", "accent": True, "size": "big"}]},
    {"start": 9.96, "end": 11.34, "lines": [{"text": "А ПРАВИЛЬНЫЙ ОТВЕТ", "accent": False, "size": "small"}, {"text": "ВСПОМИНАЕТСЯ", "accent": True, "size": "small"}]},
    {"start": 11.43, "end": 13.98, "lines": [{"text": "МНЕ ТОЛЬКО НА", "accent": False, "size": "small"}, {"text": "ЧЕТВЕРТОМ КОГДА ДВЕРИ", "accent": True, "size": "big"}]},
    {"start": 15.96, "end": 16.83, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.83, "end": 17.73, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ЕСТЬ", "accent": True, "size": "big"}]},
    {"start": 17.73, "end": 19.02, "lines": [{"text": "ИГРЫ", "accent": False, "size": "small"}, {"text": "НА ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.02, "end": 20.76, "lines": [{"text": "КОТОРЫЕ ПРИУЧАЮТ", "accent": False, "size": "small"}, {"text": "ОТВЕЧАТЬ БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 21.45, "end": 22.50, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.50, "end": 23.340, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 9.00, "end": 9.45}, {"start": 10.75, "end": 11.34}, {"start": 13.45, "end": 13.98}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 24.087s): an empty cell for an ЕГЭ
# task in the weekly schedule stays empty three weeks running -- each
# morning brings a promise, each evening brings not knowing where to
# start, so it gets pushed to tomorrow; the app's FIPI bank puts needed
# tasks right in front of the eyes, one link
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ПУСТАЯ КЛЕТКА", "ТРЕТИЙ РАЗ ПОДРЯД?"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.03, "lines": [{"text": "В РАСПИСАНИИ", "accent": False, "size": "small"}, {"text": "НА НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 3.03, "end": 4.83, "lines": [{"text": "У МЕНЯ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ПУСТАЯ КЛЕТКА", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 7.26, "lines": [{"text": "И ОНА ОСТАЕТСЯ ПУСТОЙ", "accent": False, "size": "small"}, {"text": "УЖЕ ТРЕТИЙ РАЗ ПОДРЯД", "accent": True, "size": "big"}]},
    {"start": 9.27, "end": 11.07, "lines": [{"text": "УТРОМ Я ОБЕЩАЮ СЕБЕ", "accent": False, "size": "small"}, {"text": "СДЕЛАТЬ ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 11.25, "end": 12.48, "lines": [{"text": "ВЕЧЕРОМ А ВЕЧЕРОМ", "accent": False, "size": "small"}, {"text": "НЕ ЗНАЮ", "accent": True, "size": "big"}]},
    {"start": 12.75, "end": 13.80, "lines": [{"text": "КУДА", "accent": False, "size": "small"}, {"text": "ОТКРЫТЬ", "accent": True, "size": "big"}]},
    {"start": 14.01, "end": 15.09, "lines": [{"text": "И ОТКЛАДЫВАЮ", "accent": False, "size": "small"}, {"text": "НА ЗАВТРА", "accent": True, "size": "big"}]},
    {"start": 16.26, "end": 17.16, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 17.16, "end": 18.51, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 18.51, "end": 19.47, "lines": [{"text": "ОДНА", "accent": False, "size": "small"}, {"text": "ССЫЛКА", "accent": True, "size": "big"}]},
    {"start": 19.47, "end": 21.30, "lines": [{"text": "И НУЖНЫЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "СРАЗУ ПЕРЕД ГЛАЗАМИ", "accent": True, "size": "big"}]},
    {"start": 22.08, "end": 23.22, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.22, "end": 24.087, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.50, "end": 5.94}, {"start": 14.00, "end": 14.55}, {"start": 20.80, "end": 21.30}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde cream sweater, 21.122s): a friend retells an ЕГЭ
# task from a practice test purely from memory, and the phrasing comes
# out slightly different every time -- there's no telling from a
# retelling what the actual condition looked like; the app's FIPI bank
# has the real wordings, no retelling involved
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ПЕРЕСКАЗ", "КАЖДЫЙ РАЗ ДРУГОЙ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.06, "lines": [{"text": "ПОДРУГА", "accent": False, "size": "small"}, {"text": "ПЕРЕСКАЗЫВАЕТ", "accent": True, "size": "small"}]},
    {"start": 3.06, "end": 3.96, "lines": [{"text": "МНЕ ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "СО ВЧЕРАШНЕГО", "accent": True, "size": "small"}]},
    {"start": 3.96, "end": 4.95, "lines": [{"text": "ПРОБНИКА", "accent": False, "size": "small"}, {"text": "ПО ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 4.95, "end": 6.81, "lines": [{"text": "И КАЖДЫЙ РАЗ", "accent": False, "size": "small"}, {"text": "НЕМНОГО ДРУГАЯ", "accent": True, "size": "big"}]},
    {"start": 7.71, "end": 8.82, "lines": [{"text": "ИЗ ПЕРЕСКАЗА НЕ", "accent": False, "size": "small"}, {"text": "ПОЙМЕШЬ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 10.77, "lines": [{"text": "КАК ВЫГЛЯДЕЛО", "accent": False, "size": "small"}, {"text": "НАСТОЯЩЕЕ УСЛОВИЕ", "accent": True, "size": "big"}]},
    {"start": 11.34, "end": 12.93, "lines": [{"text": "А МНЕ ВАЖНО ВИДЕТЬ", "accent": False, "size": "small"}, {"text": "ТОЧНЫЕ СЛОВА", "accent": True, "size": "big"}]},
    {"start": 13.08, "end": 14.76, "lines": [{"text": "ЗАДАНИЯ В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.27, "end": 16.29, "lines": [{"text": "ЕСТЬ", "accent": False, "size": "small"}, {"text": "БАНК ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 17.94, "lines": [{"text": "С НАСТОЯЩИМИ", "accent": False, "size": "small"}, {"text": "ФОРМУЛИРОВКАМИ", "accent": True, "size": "small"}]},
    {"start": 17.94, "end": 19.23, "lines": [{"text": "БЕЗ", "accent": False, "size": "small"}, {"text": "ПЕРЕСКАЗОВ", "accent": True, "size": "big"}]},
    {"start": 19.23, "end": 20.31, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.31, "end": 21.122, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 8.30, "end": 8.82}, {"start": 10.30, "end": 10.77}, {"start": 12.25, "end": 12.69}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
