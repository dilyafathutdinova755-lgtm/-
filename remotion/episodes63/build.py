#!/usr/bin/env python3
"""One-off authoring + validation script for the TWENTIETH 'coffee123'
batch (6 episodes uploaded under the same tag after nineteen prior
batches were delivered). Not a generic tool: hand-picked timings/text
per episode. Run from remotion/episodes63/.

Five hosts, one new face: the curly-haired boy (a), a brand-new
"study-room" girl with light-brown hair in a cream sweater, neutral
daytime lighting (b, e), and the wavy-haired living-room boy (c, d, f).
Three sub-themes repeat across hosts: memorization games for the essay
subjects instead of re-reading terms/date lists, a full text
explanation for every wrong answer instead of glancing at the correct
one, and an up-to-date FIPI-sourced task bank instead of stale
internet variants of unknown origin.
"""
import json

REAL_DURATION = {
    "a": 16.386, "b": 20.802, "c": 17.026,
    "d": 15.511, "e": 22.338, "f": 14.722,
}
SOURCE_FILE = {
    "a": "bdgffhbtgfnufjf", "b": "fdbhjnfnjfgyjyuj", "c": "fgdgfdgfdsgdgdfgd",
    "d": "gtrftgfdgdgfdg", "e": "nfjtgjhgjngfyjygu", "f": "rstbghrgftgdbhdgfydh",
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
    if letter == "a":
        for w in words:
            if abs(w["start"] - 0.66) < 0.02 and w["text"] == "термина":
                w["text"] = "термины"
    if letter == "c":
        for w in words:
            if abs(w["start"] - 0.99) < 0.02 and w["text"] == "да":
                w["text"] = "дат"
    return words


def process(letter, cards, intro, emphasis):
    total_duration = REAL_DURATION[letter]
    src = SOURCE_FILE[letter]
    words = json.load(open(f"../asr_coffee123_20/{src}_words.json"))
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
# Episode A (curly-haired boy, 16.386s): social-studies terms rarely stick
# after one read of the textbook; recalling them yourself beats another
# re-read; the app has memorization games for Russian/history/social studies
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ЧИТАЕШЬ ТЕРМИНЫ", "И ТУТ ЖЕ ЗАБЫВАЕШЬ?"], "end": 2.1}
a_cards = [
    {"start": 2.25, "end": 4.44, "lines": [{"text": "РЕДКО ЗАПОМИНАЮТСЯ С ПЕРВОГО ЧТЕНИЯ", "accent": False, "size": "small"}, {"text": "УЧЕБНИКА", "accent": True, "size": "big"}]},
    {"start": 4.71, "end": 6.99, "lines": [{"text": "ПОМОГАЕТ НЕ ЕЩЕ ОДНО ПЕРЕЧИТЫВАНИЕ А", "accent": False, "size": "small"}, {"text": "СПОСОБ", "accent": True, "size": "big"}]},
    {"start": 7.17, "end": 8.73, "lines": [{"text": "ГДЕ ПРИХОДИТСЯ ВСПОМИНАТЬ ИХ", "accent": False, "size": "small"}, {"text": "САМОМУ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.23, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 10.38, "end": 12.06, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.33, "end": 13.47, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.73, "end": 16.386, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 2.25, "end": 2.58}, {"start": 9.06, "end": 9.39}, {"start": 14.73, "end": 15.06}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (new study-room girl, 20.802s): understanding a solution now and
# being able to redo it yourself a week later are different things; the app
# gives a detailed text breakdown explaining the full logic start to end
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ПОНИМАЕШЬ РЕШЕНИЕ", "А ЧЕРЕЗ НЕДЕЛЮ ЗАБЫВАЕШЬ?"], "end": 1.98}
b_cards = [
    {"start": 1.98, "end": 3.48, "lines": [{"text": "РЕШЕНИЕ ЗАДАНИЙ ЕГЭ", "accent": False, "size": "small"}, {"text": "ПОНЯТНО", "accent": True, "size": "big"}]},
    {"start": 3.96, "end": 4.92, "lines": [{"text": "ЗНАЧИТ ТЕМА", "accent": False, "size": "small"}, {"text": "ЗАКРЫТА", "accent": True, "size": "big"}]},
    {"start": 5.46, "end": 6.42, "lines": [{"text": "НО ЭТО НЕ ВСЕГДА", "accent": False, "size": "small"}, {"text": "ТАК", "accent": True, "size": "big"}]},
    {"start": 6.96, "end": 9.21, "lines": [{"text": "ПОНЯТНОЕ РЕШЕНИЕ И РЕШЕНИЕ КОТОРОЕ", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 9.33, "end": 11.58, "lines": [{"text": "ПОВТОРИШЬ ЧЕРЕЗ НЕДЕЛЮ ЭТО РАЗНЫЕ", "accent": False, "size": "small"}, {"text": "ВЕЩИ", "accent": True, "size": "big"}]},
    {"start": 12.36, "end": 13.71, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 13.86, "end": 15.90, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 16.29, "end": 17.46, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ", "accent": False, "size": "small"}, {"text": "ЛОГИКУ", "accent": True, "size": "big"}]},
    {"start": 17.73, "end": 18.54, "lines": [{"text": "ОТ НАЧАЛА ДО", "accent": False, "size": "small"}, {"text": "КОНЦА", "accent": True, "size": "big"}]},
    {"start": 19.29, "end": 20.802, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 1.98, "end": 2.31}, {"start": 12.36, "end": 12.69}, {"start": 19.29, "end": 19.62}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (wavy-haired living-room boy, 17.026s): a list of history dates
# can be reread ten times and the order still gets mixed up on the exam;
# the app has memorization games built on active repetition, not rereading
# ---------------------------------------------------------------------------
c_intro = {"lines": ["СПИСОК ДАТ ПУТАЕТСЯ", "НА ЭКЗАМЕНЕ?"], "end": 1.95}
c_cards = [
    {"start": 2.10, "end": 3.45, "lines": [{"text": "МОЖНО ПЕРЕЧИТАТЬ ДЕСЯТЬ", "accent": False, "size": "small"}, {"text": "РАЗ", "accent": True, "size": "big"}]},
    {"start": 3.63, "end": 5.07, "lines": [{"text": "И ВСЕ РАВНО ПЕРЕПУТАТЬ", "accent": False, "size": "small"}, {"text": "ПОРЯДОК", "accent": True, "size": "big"}]},
    {"start": 5.19, "end": 6.69, "lines": [{"text": "НА ЭКЗАМЕНЕ ПРОСТОЕ", "accent": False, "size": "small"}, {"text": "ЧТЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 6.84, "end": 9.30, "lines": [{"text": "СПИСКА ПЛОХО ПРЕВРАЩАЕТСЯ В УВЕРЕННОЕ", "accent": False, "size": "small"}, {"text": "ЗНАНИЕ", "accent": True, "size": "big"}]},
    {"start": 9.60, "end": 10.77, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 10.92, "end": 12.54, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 12.84, "end": 13.92, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 14.04, "end": 14.97, "lines": [{"text": "ДЛЯ ТАКОГО", "accent": False, "size": "small"}, {"text": "МАТЕРИАЛА", "accent": True, "size": "big"}]},
    {"start": 15.21, "end": 17.026, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 2.10, "end": 2.43}, {"start": 9.60, "end": 9.93}, {"start": 15.21, "end": 15.54}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (wavy-haired living-room boy, 15.511s): the right answer on a
# similar task is sometimes guessed rather than truly understood, and that
# luck won't repeat; the app explains the solution step by step
# ---------------------------------------------------------------------------
d_intro = {"lines": ["УГАДЫВАЕШЬ ОТВЕТ", "НО НЕ ПОНИМАЕШЬ ПОЧЕМУ?"], "end": 2.1}
d_cards = [
    {"start": 2.10, "end": 4.77, "lines": [{"text": "ИНОГДА УГАДЫВАЕТСЯ А НЕ ПО НАСТОЯЩЕМУ", "accent": False, "size": "small"}, {"text": "ПОНИМАЕТСЯ", "accent": True, "size": "big"}]},
    {"start": 5.13, "end": 5.94, "lines": [{"text": "НА ПОХОЖЕМ", "accent": False, "size": "small"}, {"text": "ЗАДАНИИ", "accent": True, "size": "big"}]},
    {"start": 6.15, "end": 7.80, "lines": [{"text": "УДАЧА ОБЫЧНО НЕ ПОВТОРЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ТАКАЯ", "accent": True, "size": "big"}]},
    {"start": 8.16, "end": 9.42, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 9.54, "end": 11.61, "lines": [{"text": "ЗАДАНИЮ ЕСТЬ ПОДРОБНЫЙ ТЕКСТОВЫЙ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 11.76, "end": 13.44, "lines": [{"text": "КОТОРЫЙ ОБЪЯСНЯЕТ РЕШЕНИЕ ПО", "accent": False, "size": "small"}, {"text": "ШАГАМ", "accent": True, "size": "big"}]},
    {"start": 13.77, "end": 15.511, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 2.10, "end": 2.43}, {"start": 8.16, "end": 8.49}, {"start": 13.77, "end": 14.10}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (new study-room girl, 22.338s): a whole evening of prep and
# barely anything sticks by morning because rereading text passively isn't
# the same as recalling it; the app has memorization games for active recall
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ГОТОВИШЬСЯ ВЕЧЕРОМ", "А НАУТРО НИЧЕГО НЕ ПОМНИШЬ?"], "end": 2.28}
e_cards = [
    {"start": 2.49, "end": 5.55, "lines": [{"text": "ВЕЧЕР А В ГОЛОВЕ НАУТРО ОСТАЕТСЯ НА УДИВЛЕНИЕ", "accent": False, "size": "small"}, {"text": "НЕМНОГО", "accent": True, "size": "big"}]},
    {"start": 7.08, "end": 8.58, "lines": [{"text": "ДЕЛО ЧАСТО В ФОРМАТЕ", "accent": False, "size": "small"}, {"text": "ПОВТОРЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 8.91, "end": 10.14, "lines": [{"text": "ПРОСТО ЧИТАЙ ТЕКСТ", "accent": False, "size": "small"}, {"text": "СНОВА", "accent": True, "size": "big"}]},
    {"start": 10.41, "end": 12.36, "lines": [{"text": "НЕ ТО ЖЕ САМОЕ ЧТО ВСПОМИНАТЬ ЕГО", "accent": False, "size": "small"}, {"text": "САМОЙ", "accent": True, "size": "big"}]},
    {"start": 13.20, "end": 14.37, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ПО", "accent": False, "size": "small"}, {"text": "РУССКОМУ", "accent": True, "size": "big"}]},
    {"start": 14.52, "end": 16.32, "lines": [{"text": "ЯЗЫКУ И ОБЩЕСТВОЗНАНИЮ", "accent": False, "size": "small"}, {"text": "ИСТОРИИ", "accent": True, "size": "big"}]},
    {"start": 16.83, "end": 17.97, "lines": [{"text": "ЕСТЬ НА ЗАПОМИНАНИЕ", "accent": False, "size": "small"}, {"text": "ИГРЫ", "accent": True, "size": "big"}]},
    {"start": 18.21, "end": 20.25, "lines": [{"text": "ГДЕ ПРИХОДИТСЯ ВСПОМИНАТЬ ОТВЕТ", "accent": False, "size": "small"}, {"text": "АКТИВНО", "accent": True, "size": "big"}]},
    {"start": 20.76, "end": 22.338, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 2.49, "end": 2.82}, {"start": 13.20, "end": 13.53}, {"start": 20.76, "end": 21.09}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (wavy-haired living-room boy, 14.722s): training on old-textbook
# variants is risky if you don't check they're still current, since the
# exam format can shift in a couple of years; the app's bank is the actual
# FIPI bank, updated alongside the real exam
# ---------------------------------------------------------------------------
f_intro = {"lines": ["ЗАНИМАЕШЬСЯ ПО СТАРЫМ", "ВАРИАНТАМ ЕГЭ?"], "end": 2.1}
f_cards = [
    {"start": 2.10, "end": 3.90, "lines": [{"text": "СТАРЫХ УЧЕБНИКОВ РИСКОВАННАЯ", "accent": False, "size": "small"}, {"text": "ПРИВЫЧКА", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 6.03, "lines": [{"text": "ЕСЛИ НЕ ПРОВЕРЯТЬ ИХ АКТУАЛЬНОСТЬ", "accent": False, "size": "small"}, {"text": "ФОРМАТ", "accent": True, "size": "big"}]},
    {"start": 6.18, "end": 8.13, "lines": [{"text": "ЗАДАНИЙ ЗА ПАРУ ЛЕТ ВПОЛНЕ МОГ", "accent": False, "size": "small"}, {"text": "ИЗМЕНИТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 8.43, "end": 9.96, "lines": [{"text": "В ЕГЭ ТРЕНАЖЕРЕ ЕСТЬ", "accent": False, "size": "small"}, {"text": "АКТУАЛЬНЫЙ", "accent": True, "size": "big"}]},
    {"start": 10.08, "end": 10.92, "lines": [{"text": "БАНК", "accent": False, "size": "small"}, {"text": "ФИПИ", "accent": True, "size": "big"}]},
    {"start": 11.01, "end": 12.78, "lines": [{"text": "ОБНОВЛЯЕТСЯ ВМЕСТЕ С РЕАЛЬНЫМ", "accent": False, "size": "small"}, {"text": "ЭКЗАМЕНОМ", "accent": True, "size": "big"}]},
    {"start": 12.96, "end": 14.722, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 2.10, "end": 2.43}, {"start": 8.43, "end": 8.76}, {"start": 12.96, "end": 13.29}]
process("f", f_cards, f_intro, f_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
