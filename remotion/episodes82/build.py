#!/usr/bin/env python3
"""One-off authoring + validation script for the THIRTY-FIFTH 'coffee123'
batch (9 episodes this time, up from the usual 6). Not a generic tool:
hand-picked timings/text per episode. Run from remotion/episodes82/.

One NEW HeyGen avatar this batch: a teen boy, wavy dark hair, gray
t-shirt, lounging on a couch (bookshelf+plant+window room) -- episode a.
Three returning avatars: "mother" (b, g), "blue-shirt brunette" / THE
SMITHS poster room (c, d, e), "blonde in cream sweater" (f, h, i).

Sub-themes: narrow/partial exposure to practice material vs the app's
complete coverage -- quiz-turn blind spots, mixed-up answer keys, can
solve in head but not on paper, knows meaning but not grammatical form,
stale cached tasks, right method wrong final step, needs an answer-key
crutch, confused difficulty levels, inaccurate movie-memorized facts.
"""
import json

REAL_DURATION = {
    "a": 22.978, "b": 21.591, "c": 27.031,
    "d": 25.772, "e": 23.212, "f": 23.852,
    "g": 23.575, "h": 23.426, "i": 24.748,
}
SOURCE_FILE = {
    "a": "gfhnfrrtynrjn", "b": "gfjfnntrhnjtrgfnh", "c": "ghfhfhghethethge",
    "d": "ghjhnfdhnghh", "e": "hfjhghjfhngfh", "f": "hgfhfhgfhfhf",
    "g": "hgnmjyrtjnrynjryj", "h": "hrtnntrnrtnrtnrt", "i": "nfnhtntrnrnnrtn",
}
FIXES = {
    "h": {"посложности": "сложности"},
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
    with open(f"../asr_coffee123_35/{stem}_words.json", encoding="utf-8") as f:
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
# Episode A (NEW HOST -- teen boy, couch, 22.978s): quiz game with friends
# where terms cycle by turn; the term that always fell to a friend's turn
# showed up on the practice test and he never really learned it; the app's
# memory games cycle through ALL terms, not just "your turn's" subset
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ТЕРМИНЫ ИЗ ЧУЖИХ", "ХОДОВ НЕ УЧИШЬ?"], "end": 1.95}
a_cards = [
    {"start": 1.95, "end": 3.06, "lines": [{"text": "С ДРУЗЬЯМИ", "accent": False, "size": "small"}, {"text": "ПО ОЧЕРЕДИ", "accent": True, "size": "big"}]},
    {"start": 3.06, "end": 4.50, "lines": [{"text": "ОТВЕЧАЕМ НА ВОПРОСЫ", "accent": False, "size": "small"}, {"text": "ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.50, "end": 5.82, "lines": [{"text": "В ИГРЕ", "accent": False, "size": "small"}, {"text": "ВИКТОРИНЕ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 6.93, "lines": [{"text": "ТЕРМИНЫ ИЗ", "accent": False, "size": "small"}, {"text": "ЧУЖИХ ХОДОВ", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.13, "lines": [{"text": "Я ТОЛКОМ НЕ", "accent": False, "size": "small"}, {"text": "ВЫУЧИЛ", "accent": True, "size": "big"}]},
    {"start": 8.76, "end": 9.90, "lines": [{"text": "НА ПРОБНИКЕ", "accent": False, "size": "small"}, {"text": "ПОПАЛСЯ", "accent": True, "size": "big"}]},
    {"start": 9.90, "end": 10.95, "lines": [{"text": "ИМЕННО ТАКОЙ", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 12.63, "lines": [{"text": "В ИГРЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ДОСТАВАЛСЯ", "accent": True, "size": "small"}]},
    {"start": 12.63, "end": 13.80, "lines": [{"text": "НЕ МНЕ А", "accent": False, "size": "small"}, {"text": "ДРУГУ", "accent": True, "size": "big"}]},
    {"start": 14.13, "end": 14.95, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.95, "end": 15.76, "lines": [{"text": "ПО ОБЩЕСТВОЗНАНИЮ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 15.76, "end": 16.98, "lines": [{"text": "НА ЗАПОМИНАНИЕ КОТОРЫЕ", "accent": False, "size": "small"}, {"text": "ПРОХОДЯТ", "accent": True, "size": "big"}]},
    {"start": 16.98, "end": 18.84, "lines": [{"text": "ПО ВСЕМ", "accent": False, "size": "small"}, {"text": "ТЕРМИНАМ", "accent": True, "size": "big"}]},
    {"start": 18.84, "end": 20.76, "lines": [{"text": "А НЕ ТОЛЬКО ПО", "accent": False, "size": "small"}, {"text": "СВОЕЙ ОЧЕРЕДИ", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 21.63, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 21.63, "end": 22.978, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 9.54, "end": 9.90}, {"start": 11.82, "end": 12.63}, {"start": 18.51, "end": 18.84}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (mother, 21.591s): daughter collected tasks from several
# workbooks into one folder and mixed up which answers belong to which
# variant; the app's FIPI bank keeps each answer locked to its task
# ---------------------------------------------------------------------------
b_intro = {"lines": ["СОБРАЛА ЗАДАНИЯ", "ИЗ РАЗНЫХ ТЕТРАДЕЙ?"], "end": 1.80}
b_cards = [
    {"start": 1.80, "end": 2.91, "lines": [{"text": "ИЗ НЕСКОЛЬКИХ", "accent": False, "size": "small"}, {"text": "РАЗНЫХ", "accent": True, "size": "big"}]},
    {"start": 2.91, "end": 4.41, "lines": [{"text": "РАБОЧИХ ТЕТРАДЕЙ", "accent": False, "size": "small"}, {"text": "В ПАПКУ", "accent": True, "size": "big"}]},
    {"start": 4.86, "end": 6.09, "lines": [{"text": "И ПЕРЕПУТАЛА", "accent": False, "size": "small"}, {"text": "КАКИЕ ОТВЕТЫ", "accent": True, "size": "big"}]},
    {"start": 6.09, "end": 7.74, "lines": [{"text": "К КАКОМУ ВАРИАНТУ", "accent": False, "size": "small"}, {"text": "ОТНОСЯТСЯ", "accent": True, "size": "big"}]},
    {"start": 8.67, "end": 9.81, "lines": [{"text": "Я ПОМОГАЛА ЕЙ", "accent": False, "size": "small"}, {"text": "РАЗОБРАТЬСЯ", "accent": True, "size": "small"}]},
    {"start": 9.81, "end": 11.25, "lines": [{"text": "И САМА НЕ СРАЗУ", "accent": False, "size": "small"}, {"text": "ПОНЯЛА", "accent": True, "size": "big"}]},
    {"start": 11.43, "end": 12.48, "lines": [{"text": "ГДЕ ЧЕЙ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.01, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 14.01, "end": 15.12, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.12, "end": 16.35, "lines": [{"text": "У КАЖДОГО ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 16.35, "end": 17.46, "lines": [{"text": "ЗАКРЕПЛЕН ЗА НИМ", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 17.79, "end": 19.17, "lines": [{"text": "БЕЗ ПУТАНИЦЫ", "accent": False, "size": "small"}, {"text": "МЕЖДУ ВАРИАНТАМИ", "accent": True, "size": "big"}]},
    {"start": 19.77, "end": 20.80, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 20.80, "end": 21.591, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.95, "end": 5.43}, {"start": 11.43, "end": 11.58}, {"start": 16.20, "end": 16.35}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 27.031s): solves tasks instantly in her
# head but writing out the full step-by-step solution the exam requires
# comes out much worse; the app's breakdown shows the exact written format
# ---------------------------------------------------------------------------
c_intro = {"lines": ["РЕШАЕШЬ В УМЕ", "А ЗАПИСАТЬ НЕ МОЖЕШЬ?"], "end": 1.95}
c_cards = [
    {"start": 1.95, "end": 3.15, "lines": [{"text": "ИНОГДА РЕШАЮ", "accent": False, "size": "small"}, {"text": "В УМЕ", "accent": True, "size": "big"}]},
    {"start": 3.15, "end": 4.80, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "МГНОВЕННО", "accent": True, "size": "big"}]},
    {"start": 4.80, "end": 6.15, "lines": [{"text": "А ЗАПИСАТЬ ЭТО ЖЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.38, "lines": [{"text": "ПО ШАГАМ КАК", "accent": False, "size": "small"}, {"text": "ТРЕБУЕТ ЭКЗАМЕН", "accent": True, "size": "big"}]},
    {"start": 7.86, "end": 9.18, "lines": [{"text": "ПОЛУЧАЕТСЯ", "accent": False, "size": "small"}, {"text": "ГОРАЗДО ХУЖЕ", "accent": True, "size": "big"}]},
    {"start": 10.80, "end": 11.62, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 11.62, "end": 12.72, "lines": [{"text": "Я СОВЕРШЕННО ВЕРНО", "accent": False, "size": "small"}, {"text": "НАЗВАЛА", "accent": True, "size": "big"}]},
    {"start": 12.87, "end": 14.16, "lines": [{"text": "ОТВЕТ И ПОТОМ", "accent": False, "size": "small"}, {"text": "ДОЛГО", "accent": True, "size": "big"}]},
    {"start": 14.16, "end": 15.54, "lines": [{"text": "НЕ ЗНАЛА КАК ВООБЩЕ", "accent": False, "size": "small"}, {"text": "ОФОРМИТЬ", "accent": True, "size": "big"}]},
    {"start": 15.54, "end": 17.28, "lines": [{"text": "ПУТЬ К НЕМУ НА", "accent": False, "size": "small"}, {"text": "БУМАГЕ", "accent": True, "size": "big"}]},
    {"start": 18.54, "end": 19.35, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 19.35, "end": 20.76, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 22.26, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 22.53, "end": 23.91, "lines": [{"text": "ИМЕННО", "accent": False, "size": "small"}, {"text": "ОФОРМЛЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 24.12, "end": 25.68, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 25.68, "end": 27.031, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 3.30, "end": 3.72}, {"start": 12.45, "end": 12.72}, {"start": 15.30, "end": 15.54}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blue-shirt brunette, 25.772s): knows a grammar term's MEANING
# perfectly but mixes up its own grammatical form in her own sentences;
# the app's memory games train the term in its correct form, in context
# ---------------------------------------------------------------------------
d_intro = {"lines": ["СМЫСЛ ТЕРМИНА", "ЗНАЕШЬ ИДЕАЛЬНО?"], "end": 1.65}
d_cards = [
    {"start": 1.65, "end": 2.85, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ДЛЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 2.85, "end": 3.90, "lines": [{"text": "Я ЗНАЮ", "accent": False, "size": "small"}, {"text": "ОТЛИЧНО", "accent": True, "size": "big"}]},
    {"start": 4.47, "end": 6.15, "lines": [{"text": "А ВОТ ЕГО", "accent": False, "size": "small"}, {"text": "РОД И СКЛОНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 6.30, "end": 7.44, "lines": [{"text": "В СОБСТВЕННОМ", "accent": False, "size": "small"}, {"text": "ПРЕДЛОЖЕНИИ", "accent": True, "size": "small"}]},
    {"start": 7.62, "end": 8.41, "lines": [{"text": "ИНОГДА", "accent": False, "size": "small"}, {"text": "ПУТАЮ", "accent": True, "size": "big"}]},
    {"start": 9.18, "end": 10.00, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 10.00, "end": 11.19, "lines": [{"text": "Я НАПИСАЛА", "accent": False, "size": "small"}, {"text": "СМЫСЛ ТЕРМИНА", "accent": True, "size": "big"}]},
    {"start": 11.34, "end": 12.72, "lines": [{"text": "ВЕРНО А САМО", "accent": False, "size": "small"}, {"text": "СЛОВО", "accent": True, "size": "big"}]},
    {"start": 12.99, "end": 14.34, "lines": [{"text": "ПОСТАВИЛО В НЕПРАВИЛЬНУЮ", "accent": False, "size": "small"}, {"text": "ФОРМУ", "accent": True, "size": "big"}]},
    {"start": 15.93, "end": 16.76, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.76, "end": 17.60, "lines": [{"text": "ПО РУССКОМУ", "accent": False, "size": "small"}, {"text": "ЯЗЫКУ", "accent": True, "size": "big"}]},
    {"start": 17.88, "end": 19.14, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 19.56, "end": 20.79, "lines": [{"text": "КОТОРЫЕ ТРЕНИРУЮТ", "accent": False, "size": "small"}, {"text": "ТЕРМИН", "accent": True, "size": "big"}]},
    {"start": 21.00, "end": 21.99, "lines": [{"text": "СРАЗУ В", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНОЙ ФОРМЕ", "accent": True, "size": "big"}]},
    {"start": 22.14, "end": 23.01, "lines": [{"text": "ВНУТРИ", "accent": False, "size": "small"}, {"text": "ПРЕДЛОЖЕНИЯ", "accent": True, "size": "small"}]},
    {"start": 23.82, "end": 24.65, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 24.65, "end": 25.772, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 4.92, "end": 5.43}, {"start": 9.87, "end": 10.62}, {"start": 13.59, "end": 14.10}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blue-shirt brunette, 23.212s): solving ЕГЭ tasks from an old
# browser tab not refreshed in months, until noticing the cache date is
# almost a year old; the app's FIPI bank always shows current tasks
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ЗАДАНИЯ ОТКРЫТЫ", "В СТАРОЙ ВКЛАДКЕ?"], "end": 1.80}
e_cards = [
    {"start": 1.80, "end": 3.60, "lines": [{"text": "У МЕНЯ СОХРАНЕНЫ", "accent": False, "size": "small"}, {"text": "В СТАРОЙ ВКЛАДКЕ", "accent": True, "size": "big"}]},
    {"start": 4.02, "end": 5.10, "lines": [{"text": "КОТОРУЮ Я НЕ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЯЛА", "accent": True, "size": "big"}]},
    {"start": 5.25, "end": 6.21, "lines": [{"text": "УЖЕ НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "МЕСЯЦЕВ", "accent": True, "size": "big"}]},
    {"start": 6.93, "end": 8.01, "lines": [{"text": "Я РЕШАЛА ИМЕННО", "accent": False, "size": "small"}, {"text": "ЭТУ ВКЛАДКУ", "accent": True, "size": "big"}]},
    {"start": 8.16, "end": 9.03, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ПРИВЫЧКЕ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 10.23, "lines": [{"text": "ПОКА НЕ", "accent": False, "size": "small"}, {"text": "ЗАМЕТИЛА", "accent": True, "size": "big"}]},
    {"start": 10.29, "end": 11.10, "lines": [{"text": "В АДРЕСНОЙ", "accent": False, "size": "small"}, {"text": "СТРОКЕ", "accent": True, "size": "big"}]},
    {"start": 11.37, "end": 12.20, "lines": [{"text": "ДАТУ", "accent": False, "size": "small"}, {"text": "КЭША", "accent": True, "size": "big"}]},
    {"start": 12.20, "end": 13.38, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "ГОДИЧНОЙ ДАВНОСТИ", "accent": True, "size": "big"}]},
    {"start": 14.19, "end": 15.00, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.30, "end": 16.20, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.56, "end": 17.76, "lines": [{"text": "КОТОРЫЙ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ПОКАЗЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.94, "end": 18.78, "lines": [{"text": "АКТУАЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 19.08, "end": 20.46, "lines": [{"text": "БЕЗ ВСЯКИХ", "accent": False, "size": "small"}, {"text": "СТАРЫХ ВКЛАДОК", "accent": True, "size": "big"}]},
    {"start": 21.24, "end": 22.05, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.05, "end": 23.212, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 4.74, "end": 5.10}, {"start": 9.81, "end": 10.20}, {"start": 12.15, "end": 12.93}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (blonde cream sweater, 23.852s): picks the right method almost
# always, but slips specifically on the final calculation; the app's
# breakdown checks the solution together with that very last step
# ---------------------------------------------------------------------------
f_intro = {"lines": ["СПОСОБ РЕШЕНИЯ", "ВЫБИРАЕШЬ БЕЗ ОШИБОК?"], "end": 1.95}
f_cards = [
    {"start": 1.95, "end": 3.18, "lines": [{"text": "Я ВЫБИРАЮ", "accent": False, "size": "small"}, {"text": "ПРАВИЛЬНО", "accent": True, "size": "big"}]},
    {"start": 3.18, "end": 4.00, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "ВСЕГДА", "accent": True, "size": "big"}]},
    {"start": 4.56, "end": 5.64, "lines": [{"text": "А ОШИБКУ ПОТОМ", "accent": False, "size": "small"}, {"text": "ДОПУСКАЮ", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 7.29, "lines": [{"text": "ИМЕННО В", "accent": False, "size": "small"}, {"text": "ФИНАЛЬНОМ ВЫЧИСЛЕНИИ", "accent": True, "size": "small"}]},
    {"start": 8.13, "end": 8.95, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 8.95, "end": 9.96, "lines": [{"text": "Я РАСПИСАЛА ВЕСЬ", "accent": False, "size": "small"}, {"text": "ХОД", "accent": True, "size": "big"}]},
    {"start": 10.11, "end": 11.58, "lines": [{"text": "РЕШЕНИЯ БЕЗ ЕДИНОЙ", "accent": False, "size": "small"}, {"text": "ОШИБКИ", "accent": True, "size": "big"}]},
    {"start": 12.06, "end": 13.08, "lines": [{"text": "А В ПОСЛЕДНЕМ", "accent": False, "size": "small"}, {"text": "УМНОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 13.17, "end": 14.07, "lines": [{"text": "В СТОЛБИК", "accent": False, "size": "small"}, {"text": "ПРОМАХНУЛАСЬ", "accent": True, "size": "small"}]},
    {"start": 14.19, "end": 15.00, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ЕДИНИЦУ", "accent": True, "size": "big"}]},
    {"start": 15.60, "end": 16.42, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.47, "end": 17.91, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 18.30, "end": 19.44, "lines": [{"text": "КОТОРЫЙ ПРОВЕРЯЕТ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 19.65, "end": 21.36, "lines": [{"text": "ВМЕСТЕ С САМЫМ", "accent": False, "size": "small"}, {"text": "ПОСЛЕДНИМ ВЫЧИСЛЕНИЕМ", "accent": True, "size": "small"}]},
    {"start": 22.02, "end": 22.85, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.85, "end": 23.852, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 4.62, "end": 5.10}, {"start": 10.92, "end": 11.58}, {"start": 13.59, "end": 14.07}]
process("f", f_cards, f_intro, f_emphasis)


# ---------------------------------------------------------------------------
# Episode G (mother, 23.575s): daughter solves a task correctly only while
# peeking at the textbook's answer; without that crutch the same task
# causes way more trouble; the app's breakdown explains without peeking
# ---------------------------------------------------------------------------
g_intro = {"lines": ["РЕШАЕТ ПРАВИЛЬНО", "ТОЛЬКО ПОДГЛЯДЫВАЯ В ОТВЕТ?"], "end": 2.00}
g_cards = [
    {"start": 2.00, "end": 3.12, "lines": [{"text": "ПРАВИЛЬНО", "accent": False, "size": "small"}, {"text": "ПОДГЛЯДЫВАЯ", "accent": True, "size": "small"}]},
    {"start": 3.24, "end": 4.38, "lines": [{"text": "В ОТВЕТ В КОНЦЕ", "accent": False, "size": "small"}, {"text": "УЧЕБНИКА", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 5.73, "lines": [{"text": "А БЕЗ ЭТОЙ", "accent": False, "size": "small"}, {"text": "ПОДСКАЗКИ", "accent": True, "size": "big"}]},
    {"start": 5.91, "end": 6.72, "lines": [{"text": "ЧАСТО", "accent": False, "size": "small"}, {"text": "ТЕРЯЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 6.72, "end": 7.62, "lines": [{"text": "В СЕРЕДИНЕ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 8.55, "end": 9.51, "lines": [{"text": "Я СПЕЦИАЛЬНО", "accent": False, "size": "small"}, {"text": "ЗАКРЫЛА", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 10.71, "lines": [{"text": "ЕЙ СТРАНИЦУ С", "accent": False, "size": "small"}, {"text": "ОТВЕТАМИ", "accent": True, "size": "big"}]},
    {"start": 10.98, "end": 12.06, "lines": [{"text": "И ТО ЖЕ САМОЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.14, "lines": [{"text": "СРАЗУ", "accent": False, "size": "small"}, {"text": "ВЫЗВАЛО", "accent": True, "size": "big"}]},
    {"start": 13.14, "end": 14.16, "lines": [{"text": "КУДА БОЛЬШЕ", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТЕЙ", "accent": True, "size": "big"}]},
    {"start": 15.24, "end": 16.06, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.14, "end": 17.67, "lines": [{"text": "К ЗАДАНИЯМ ЕСТЬ", "accent": False, "size": "small"}, {"text": "ТЕКСТОВЫЙ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 17.82, "end": 19.05, "lines": [{"text": "КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "ОБЪЯСНЯЕТ РЕШЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 19.50, "end": 21.09, "lines": [{"text": "И БЕЗ", "accent": False, "size": "small"}, {"text": "ПОДГЛЯДЫВАНИЯ", "accent": True, "size": "small"}]},
    {"start": 21.67, "end": 22.47, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.47, "end": 23.575, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 2.61, "end": 3.12}, {"start": 9.21, "end": 9.51}, {"start": 13.35, "end": 14.16}]
process("g", g_cards, g_intro, g_emphasis)


# ---------------------------------------------------------------------------
# Episode H (blonde cream sweater, 23.426s): accidentally mixed up base-
# and profile-level math tasks and solved the wrong set for almost a
# month; the app's FIPI bank clearly separates difficulty levels
# ---------------------------------------------------------------------------
h_intro = {"lines": ["БАЗОВЫЙ И ПРОФИЛЬНЫЙ", "ПЕРЕПУТАЛА УРОВЕНЬ?"], "end": 1.95}
h_cards = [
    {"start": 1.95, "end": 3.03, "lines": [{"text": "ЗАДАНИЕ ЕГЭ", "accent": False, "size": "small"}, {"text": "БАЗОВОГО УРОВНЯ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 4.65, "lines": [{"text": "СЛУЧАЙНО", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАЛА", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 5.65, "lines": [{"text": "С", "accent": False, "size": "small"}, {"text": "ПРОФИЛЬНЫМИ", "accent": True, "size": "small"}]},
    {"start": 5.73, "end": 6.81, "lines": [{"text": "И РЕШАЛА НЕ ТОТ", "accent": False, "size": "small"}, {"text": "КОМПЛЕКТ", "accent": True, "size": "big"}]},
    {"start": 6.99, "end": 7.84, "lines": [{"text": "ПОЧТИ", "accent": False, "size": "small"}, {"text": "МЕСЯЦ", "accent": True, "size": "big"}]},
    {"start": 8.34, "end": 9.33, "lines": [{"text": "Я ЗАМЕТИЛА", "accent": False, "size": "small"}, {"text": "ПУТАНИЦУ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 10.65, "lines": [{"text": "ТОЛЬКО КОГДА", "accent": False, "size": "small"}, {"text": "ОДНОКЛАССНИЦА", "accent": True, "size": "small"}]},
    {"start": 10.77, "end": 11.94, "lines": [{"text": "УДИВИЛАСЬ ЧТО У МЕНЯ", "accent": False, "size": "small"}, {"text": "СОВСЕМ", "accent": True, "size": "big"}]},
    {"start": 12.09, "end": 13.74, "lines": [{"text": "ДРУГИЕ", "accent": False, "size": "small"}, {"text": "СЛОЖНОСТИ ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.52, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.52, "end": 16.44, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 16.89, "end": 18.24, "lines": [{"text": "С ЧЕТКИМ", "accent": False, "size": "small"}, {"text": "РАЗДЕЛЕНИЕМ УРОВНЯ", "accent": True, "size": "small"}]},
    {"start": 18.39, "end": 19.98, "lines": [{"text": "СЛОЖНОСТИ КОТОРЫЙ", "accent": False, "size": "small"}, {"text": "НЕ ДАЕТ", "accent": True, "size": "big"}]},
    {"start": 20.10, "end": 20.94, "lines": [{"text": "ПЕРЕПУТАТЬ", "accent": False, "size": "small"}, {"text": "КОМПЛЕКТ", "accent": True, "size": "big"}]},
    {"start": 21.60, "end": 22.42, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.42, "end": 23.426, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 3.75, "end": 4.65}, {"start": 6.99, "end": 7.65}, {"start": 10.77, "end": 11.25}]
process("h", h_cards, h_intro, h_emphasis)


# ---------------------------------------------------------------------------
# Episode I (blonde cream sweater, 24.748s): memorized a historical event
# for the exam from a movie, which turned out to fudge some details for
# the plot; the app's history games rely on verified facts, not a plot
# ---------------------------------------------------------------------------
i_intro = {"lines": ["СОБЫТИЕ ЗАПОМНИЛА", "ПО ФИЛЬМУ?"], "end": 1.80}
i_cards = [
    {"start": 1.80, "end": 3.39, "lines": [{"text": "ДЛЯ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПО ФИЛЬМУ", "accent": True, "size": "big"}]},
    {"start": 3.99, "end": 5.16, "lines": [{"text": "А ПОТОМ", "accent": False, "size": "small"}, {"text": "ОКАЗАЛОСЬ", "accent": True, "size": "big"}]},
    {"start": 5.34, "end": 7.05, "lines": [{"text": "В ФИЛЬМЕ", "accent": False, "size": "small"}, {"text": "ПЕРЕПУТАНЫ ДЕТАЛИ", "accent": True, "size": "big"}]},
    {"start": 7.29, "end": 8.08, "lines": [{"text": "РАДИ", "accent": False, "size": "small"}, {"text": "СЮЖЕТА", "accent": True, "size": "big"}]},
    {"start": 8.85, "end": 9.66, "lines": [{"text": "НА", "accent": False, "size": "small"}, {"text": "ПРОБНИКЕ", "accent": True, "size": "big"}]},
    {"start": 9.66, "end": 11.10, "lines": [{"text": "Я НАПИСАЛА", "accent": False, "size": "small"}, {"text": "ВЕРСИЮ ИЗ ФИЛЬМА", "accent": True, "size": "big"}]},
    {"start": 11.55, "end": 12.63, "lines": [{"text": "И ТОЛЬКО ПОТОМ", "accent": False, "size": "small"}, {"text": "ПОНЯЛА", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.64, "lines": [{"text": "ЧТО ОНА НЕ", "accent": False, "size": "small"}, {"text": "СОВПАДАЕТ С УЧЕБНИКОМ", "accent": True, "size": "big"}]},
    {"start": 15.72, "end": 16.53, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 16.53, "end": 17.35, "lines": [{"text": "ПО", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 17.35, "end": 18.39, "lines": [{"text": "ЕСТЬ ИГРЫ НА", "accent": False, "size": "small"}, {"text": "ЗАПОМИНАНИЕ", "accent": True, "size": "small"}]},
    {"start": 18.66, "end": 20.34, "lines": [{"text": "КОТОРЫЕ ОПИРАЮТСЯ НА", "accent": False, "size": "small"}, {"text": "ПРОВЕРЕННЫЕ ФАКТЫ", "accent": True, "size": "small"}]},
    {"start": 21.27, "end": 22.17, "lines": [{"text": "А НЕ НА", "accent": False, "size": "small"}, {"text": "СЮЖЕТ ФИЛЬМА", "accent": True, "size": "big"}]},
    {"start": 22.86, "end": 23.91, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 23.91, "end": 24.748, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 5.76, "end": 6.24}, {"start": 13.65, "end": 14.10}, {"start": 19.80, "end": 20.34}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
