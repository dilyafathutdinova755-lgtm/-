#!/usr/bin/env python3
"""One-off authoring + validation script for the SIXTIETH 'coffee123'
batch (6 episodes). Not a generic tool: hand-picked timings/text per
episode. Run from remotion/episodes107/.

Three returning hosts, no new faces: "blue-shirt brunette" / THE SMITHS
poster + "ЕГЭ 2026" sticky note room (a, c), "blonde in cream sweater" /
desk+lamp+plant+notebook room (b, d, e), "mother" / bookshelf+doorway
apartment with small framed picture (f).

Sub-themes: the heat going out for two days means solving ЕГЭ in a
jacket, with cold ruled out as an excuse since ten minutes of solving
even warms you up; "-ить"/"-еть" exception verbs remembered like a train
schedule with delays, where the rare exceptions need the most repeating;
"gendarmes and censorship" summing up the whole era of Nicholas I,
needing reforms and wars added before it becomes an actual answer;
imagining the breakdown's author guiding you by the hand but letting go
for the last step, which stays yours to do; counting solved exam tasks
like a grandmother counts knitted rows, so a month's progress is visibly
measured out; and naming the spots in a breakdown where a solution turns
the other way "turning points" -- a term the narrator coined
themselves, not attributed to anything external (works around an ASR
transcript whose subject for that line could not be confidently
reconstructed).

Card/intro text was verified against the actual Golos Text Black render
(PIL getbbox at each line's real font size, small lines included) before
being written below -- consistent with the process that caught overflow
bugs in batches 58-59.
"""
import json

REAL_DURATION = {
    "a": 20.760, "b": 21.911, "c": 23.852,
    "d": 21.591, "e": 20.546, "f": 18.562,
}
SOURCE_FILE = {
    "a": "cfgvfsdfsdfds", "b": "dbshdbdsfsd", "c": "dsffsfdsfsdfs",
    "d": "dshbbgdsfgsdfs", "e": "gbgvdsgvsfvsd", "f": "sdghgsdfsdfsdf",
}
FIXES = {
    "a": {},
    "b": {"тренажеры": "тренажере"},
    "c": {"певого": "первого", "певог": "первого"},
    "d": {"читай": "читаю", "тренажерик": "тренажере"},
    "e": {"каждая": "каждое"},
    "f": {"разборы": "разбора"},
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
    with open(f"../asr_coffee123_60/{letter}_words.json", encoding="utf-8") as f:
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
# Episode A (blue-shirt brunette, 20.760s): the heat went out for two
# days in October, solving ЕГЭ in a jacket -- cold is ruled out as an
# excuse since ten minutes of solving even warms you up, and the app's
# FIPI bank gives exactly a ten-minute task, no excuses either
# ---------------------------------------------------------------------------
a_intro = {"lines": ["РЕШАЛА ЕГЭ", "В КУРТКЕ"], "end": 1.86}
a_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "В ОКТЯБРЕ НАМ", "accent": False, "size": "small"}, {"text": "ОТКЛЮЧИЛИ", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "ОТОПЛЕНИЕ НА", "accent": False, "size": "small"}, {"text": "ДВА ДНЯ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "И Я ВПЕРВЫЕ", "accent": False, "size": "small"}, {"text": "РЕШАЛА ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "В", "accent": False, "size": "small"}, {"text": "КУРТКЕ", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "ХОЛОД НЕ", "accent": False, "size": "small"}, {"text": "ОПРАВДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 7.90, "end": 9.10, "lines": [{"text": "ПАЛЬЦЫ", "accent": False, "size": "small"}, {"text": "МЕРЗНУТ", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 10.30, "lines": [{"text": "А ГОЛОВА", "accent": False, "size": "small"}, {"text": "РАБОТАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.30, "end": 11.50, "lines": [{"text": "ДЕСЯТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "РЕШЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 11.50, "end": 12.70, "lines": [{"text": "ДАЖЕ", "accent": False, "size": "small"}, {"text": "СОГРЕВАЮТ", "accent": True, "size": "big"}]},
    {"start": 12.70, "end": 13.90, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.90, "end": 15.10, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 15.10, "end": 16.30, "lines": [{"text": "ГДЕ ДЕСЯТЬ МИНУТ", "accent": False, "size": "small"}, {"text": "ДАЮТ", "accent": True, "size": "big"}]},
    {"start": 16.30, "end": 17.50, "lines": [{"text": "ЗАДАНИЕ БЕЗ", "accent": False, "size": "small"}, {"text": "ОПРАВДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 17.50, "end": 18.90, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.90, "end": 20.760, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.49, "end": 3.45}, {"start": 8.31, "end": 9.00}, {"start": 10.56, "end": 12.54}]
process("a", a_cards, a_intro, a_emphasis)


# ---------------------------------------------------------------------------
# Episode B (blonde in cream sweater, 21.911s): "-ить"/"-еть" exception
# verbs for Russian ЕГЭ remembered like a train schedule with delays --
# the rare exceptions, met less often, need the most repeating, and the
# app's games bring those rare exceptions back more often than the rest
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ИСКЛЮЧЕНИЯ", "ОПОЗДАВШИЕ"], "end": 1.86}
b_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "ГЛАГОЛЫ", "accent": False, "size": "small"}, {"text": "ИСКЛЮЧЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "НА ИТЬ И ЕТЬ", "accent": False, "size": "small"}, {"text": "В ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "ПО РУССКОМУ Я", "accent": False, "size": "small"}, {"text": "ПОМНЮ", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "КАК РАСПИСАНИЕ", "accent": False, "size": "small"}, {"text": "ПОЕЗДОВ", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "ПОЕЗДОВ С", "accent": False, "size": "small"}, {"text": "ОПОЗДАНИЯМИ", "accent": True, "size": "small"}]},
    {"start": 7.90, "end": 9.30, "lines": [{"text": "ОПАЗДЫВАЮТ ТЕ ЧТО", "accent": False, "size": "small"}, {"text": "ВСТРЕЧАЮТСЯ", "accent": True, "size": "small"}]},
    {"start": 9.30, "end": 10.70, "lines": [{"text": "РЕЖЕ ЗНАЧИТ", "accent": False, "size": "small"}, {"text": "ПОВТОРЯТЬ", "accent": True, "size": "big"}]},
    {"start": 10.70, "end": 12.10, "lines": [{"text": "НУЖНО ИМЕННО", "accent": False, "size": "small"}, {"text": "ИХ", "accent": True, "size": "big"}]},
    {"start": 12.10, "end": 13.50, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.90, "lines": [{"text": "ПО РУССКОМУ ЯЗЫКУ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.90, "end": 16.30, "lines": [{"text": "ГДЕ РЕДКИЕ", "accent": False, "size": "small"}, {"text": "ИСКЛЮЧЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 16.30, "end": 17.70, "lines": [{"text": "ВОЗВРАЩАЮТСЯ", "accent": False, "size": "small"}, {"text": "ЧАЩЕ", "accent": True, "size": "big"}]},
    {"start": 17.70, "end": 19.70, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 19.70, "end": 21.911, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 4.77, "end": 9.33}, {"start": 16.59, "end": 19.17}]
process("b", b_cards, b_intro, b_emphasis)


# ---------------------------------------------------------------------------
# Episode C (blue-shirt brunette, 23.852s): "gendarmes and censorship"
# sums up the whole era of Nicholas I for history ЕГЭ -- an answer can't
# be built from two words, reforms and wars need adding, and the app's
# history games assemble the era from reforms, wars and laws together
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ЭПОХА ИЗ", "ДВУХ СЛОВ"], "end": 1.86}
c_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "ЖАНДАРМЫ И", "accent": False, "size": "small"}, {"text": "ЦЕНЗУРА", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "ВОТ И ВСЯ", "accent": False, "size": "small"}, {"text": "ЭПОХА", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "НИКОЛАЯ", "accent": False, "size": "small"}, {"text": "ПЕРВОГО", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "КОТОРУЮ Я", "accent": False, "size": "small"}, {"text": "ПОМНЮ", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "ДЛЯ ЕГЭ ПО", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 7.90, "end": 9.10, "lines": [{"text": "ИЗ ДВУХ СЛОВ", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 10.30, "lines": [{"text": "НЕ", "accent": False, "size": "small"}, {"text": "СЛОЖИТЬ", "accent": True, "size": "big"}]},
    {"start": 10.30, "end": 11.50, "lines": [{"text": "НУЖНЫ ЕЩЕ", "accent": False, "size": "small"}, {"text": "РЕФОРМЫ", "accent": True, "size": "big"}]},
    {"start": 11.50, "end": 12.70, "lines": [{"text": "И", "accent": False, "size": "small"}, {"text": "ВОЙНЫ", "accent": True, "size": "big"}]},
    {"start": 12.70, "end": 13.90, "lines": [{"text": "ЭТОГО", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ", "accent": True, "size": "big"}]},
    {"start": 13.90, "end": 15.10, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 15.10, "end": 16.50, "lines": [{"text": "ПО ИСТОРИИ", "accent": False, "size": "small"}, {"text": "ЕСТЬ ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 16.50, "end": 17.90, "lines": [{"text": "ГДЕ ЭПОХА", "accent": False, "size": "small"}, {"text": "НИКОЛАЯ", "accent": True, "size": "big"}]},
    {"start": 17.90, "end": 19.30, "lines": [{"text": "ПЕРВОГО СОБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "ИЗ РЕФОРМ", "accent": True, "size": "big"}]},
    {"start": 19.30, "end": 20.70, "lines": [{"text": "ВОЙН И", "accent": False, "size": "small"}, {"text": "ЗАКОНОВ", "accent": True, "size": "big"}]},
    {"start": 20.70, "end": 22.10, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 22.10, "end": 23.852, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.40, "end": 4.14}, {"start": 7.65, "end": 8.79}, {"start": 18.39, "end": 21.18}]
process("c", c_cards, c_intro, c_emphasis)


# ---------------------------------------------------------------------------
# Episode D (blonde in cream sweater, 21.591s): imagining the breakdown's
# author guiding you by the hand, but letting go for the last step -- the
# app's text breakdown leaves exactly that last step for an independent
# attempt
# ---------------------------------------------------------------------------
d_intro = {"lines": ["АВТОР ВЕДЕТ", "ЗА РУКУ"], "end": 1.86}
d_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "ЧИТАЮ РАЗБОР", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "Я ПРЕДСТАВЛЯЮ ЧТО", "accent": False, "size": "small"}, {"text": "АВТОР", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "СИДИТ РЯДОМ И", "accent": False, "size": "small"}, {"text": "ГОВОРИТ", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "А ТЕПЕРЬ ПОСМОТРИ", "accent": False, "size": "small"}, {"text": "СЮДА", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "ТАКОЙ РАЗБОР", "accent": False, "size": "small"}, {"text": "ВЕДЕТ", "accent": True, "size": "big"}]},
    {"start": 7.90, "end": 9.10, "lines": [{"text": "ЗА РУКУ НО В", "accent": False, "size": "small"}, {"text": "КОНЦЕ", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 10.30, "lines": [{"text": "ОТПУСКАЕТ И", "accent": False, "size": "small"}, {"text": "ПОСЛЕДНИЙ", "accent": True, "size": "big"}]},
    {"start": 10.30, "end": 11.50, "lines": [{"text": "ШАГ ДЕЛАЕШЬ", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 11.50, "end": 12.90, "lines": [{"text": "В ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 12.90, "end": 14.30, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.30, "end": 15.70, "lines": [{"text": "В КОТОРОМ ПОСЛЕДНИЙ", "accent": False, "size": "small"}, {"text": "ШАГ", "accent": True, "size": "big"}]},
    {"start": 15.70, "end": 17.10, "lines": [{"text": "ОСТАВЛЕН ДЛЯ", "accent": False, "size": "small"}, {"text": "ПОПЫТКИ", "accent": True, "size": "big"}]},
    {"start": 17.10, "end": 18.50, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.50, "end": 21.591, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.34, "end": 4.17}, {"start": 8.34, "end": 12.06}, {"start": 16.29, "end": 18.84}]
process("d", d_cards, d_intro, d_emphasis)


# ---------------------------------------------------------------------------
# Episode E (blonde in cream sweater, 20.546s): counting solved ЕГЭ
# tasks like a grandmother counts knitted rows -- by month's end the
# scarf and the stack of solved tasks will be equally long, and the
# app's FIPI bank makes each solved task one more counted row
# ---------------------------------------------------------------------------
e_intro = {"lines": ["СЧИТАЮ КАК", "БАБУШКА РЯДЫ"], "end": 1.86}
e_cards = [
    {"start": 1.86, "end": 3.10, "lines": [{"text": "БАБУШКА ВЯЖЕТ", "accent": False, "size": "small"}, {"text": "ШАРФ", "accent": True, "size": "big"}]},
    {"start": 3.10, "end": 4.30, "lines": [{"text": "И СЧИТАЕТ", "accent": False, "size": "small"}, {"text": "РЯДЫ", "accent": True, "size": "big"}]},
    {"start": 4.30, "end": 5.50, "lines": [{"text": "А Я РЕШАЮ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 5.50, "end": 6.70, "lines": [{"text": "И ТОЖЕ", "accent": False, "size": "small"}, {"text": "СЧИТАЮ", "accent": True, "size": "big"}]},
    {"start": 6.70, "end": 7.90, "lines": [{"text": "КАЖДЫЙ РЯД ОДНО", "accent": False, "size": "small"}, {"text": "РЕШЕННОЕ", "accent": True, "size": "big"}]},
    {"start": 7.90, "end": 9.30, "lines": [{"text": "К КОНЦУ МЕСЯЦА", "accent": False, "size": "small"}, {"text": "ШАРФ", "accent": True, "size": "big"}]},
    {"start": 9.30, "end": 10.70, "lines": [{"text": "И СТОПКА", "accent": False, "size": "small"}, {"text": "ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 10.70, "end": 12.10, "lines": [{"text": "БУДУТ ОДИНАКОВО", "accent": False, "size": "small"}, {"text": "ДЛИННЫМИ", "accent": True, "size": "big"}]},
    {"start": 12.10, "end": 13.50, "lines": [{"text": "В ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 13.50, "end": 14.70, "lines": [{"text": "ЕСТЬ БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 15.90, "lines": [{"text": "ГДЕ КАЖДОЕ", "accent": False, "size": "small"}, {"text": "РЕШЕННОЕ", "accent": True, "size": "big"}]},
    {"start": 15.90, "end": 17.30, "lines": [{"text": "ЗАДАНИЕ ЕЩЕ ОДИН", "accent": False, "size": "small"}, {"text": "РЯД", "accent": True, "size": "big"}]},
    {"start": 17.30, "end": 18.70, "lines": [{"text": "ССЫЛКА НА ЕГЭ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 18.70, "end": 20.546, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 5.88, "end": 7.56}, {"start": 11.37, "end": 12.57}, {"start": 15.78, "end": 18.09}]
process("e", e_cards, e_intro, e_emphasis)


# ---------------------------------------------------------------------------
# Episode F (mother, 18.562s): naming the spots in a task breakdown
# where the solution turns the other way "turning points" -- every
# breakdown has its own, and the app's text breakdown highlights that
# turning point separately
# ---------------------------------------------------------------------------
f_intro = {"lines": ["НАЗЫВАЮ ИХ", "ПОВОРОТАМИ"], "end": 1.86}
f_cards = [
    {"start": 1.86, "end": 3.00, "lines": [{"text": "НАЗЫВАЮ", "accent": False, "size": "small"}, {"text": "ПОВОРОТАМИ", "accent": True, "size": "big"}]},
    {"start": 3.00, "end": 4.20, "lines": [{"text": "ТЕ МЕСТА В РАЗБОРЕ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.40, "lines": [{"text": "ГДЕ РЕШЕНИЕ ИДЕТ", "accent": False, "size": "small"}, {"text": "В ДРУГУЮ", "accent": True, "size": "big"}]},
    {"start": 5.40, "end": 6.60, "lines": [{"text": "СТОРОНУ МНЕ", "accent": False, "size": "small"}, {"text": "ПОНРАВИЛОСЬ", "accent": True, "size": "small"}]},
    {"start": 6.60, "end": 7.80, "lines": [{"text": "У КАЖДОГО", "accent": False, "size": "small"}, {"text": "РАЗБОРА", "accent": True, "size": "big"}]},
    {"start": 7.80, "end": 9.00, "lines": [{"text": "СВОЯ ТОЧКА", "accent": False, "size": "small"}, {"text": "ПОВОРОТА", "accent": True, "size": "big"}]},
    {"start": 9.00, "end": 10.20, "lines": [{"text": "И ДОЧЬ УМЕЕТ", "accent": False, "size": "small"}, {"text": "ЕЕ НАХОДИТЬ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.40, "lines": [{"text": "В ЕГА", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕРЕ", "accent": True, "size": "big"}]},
    {"start": 11.40, "end": 12.60, "lines": [{"text": "К ЗАДАНИЯМ", "accent": False, "size": "small"}, {"text": "ЕСТЬ РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.80, "lines": [{"text": "ГДЕ ТОЧКА", "accent": False, "size": "small"}, {"text": "ПОВОРОТА", "accent": True, "size": "big"}]},
    {"start": 13.80, "end": 15.00, "lines": [{"text": "РЕШЕНИЯ", "accent": False, "size": "small"}, {"text": "ВЫДЕЛЕНА", "accent": True, "size": "big"}]},
    {"start": 15.00, "end": 16.40, "lines": [{"text": "ССЫЛКА НА ЕГ", "accent": False, "size": "small"}, {"text": "ТРЕНАЖЕР", "accent": True, "size": "big"}]},
    {"start": 16.40, "end": 18.562, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 7.17, "end": 10.56}, {"start": 14.04, "end": 16.23}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
