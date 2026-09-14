#!/usr/bin/env python3
"""One-off authoring + validation script for the NINTH 'coffee123' batch
(9 episodes uploaded under the same tag after eight prior batches were
delivered). Not a generic tool: hand-picked timings/text per episode.
Run from remotion/episodes52/.

Two new hosts this time (girl with bookshelf/desk, girl in warm evening
light) plus the returning sunset-window boy - no gray-bedroom boy or mom
clips in this drop. Content is app-feature focused again (voiced
walkthrough attached to a task instead of a bare chat-photo answer,
offline FIPI bank access, a confusable-formula game, a confusable-date
game, per-subject result aggregation flagging the lagging subject, a
single synced official task wording, a friend leaderboard, a classmate
leaderboard visible on open, free task bank covering extra olympiad
subjects instead of hunting a tutor).
"""
import json

REAL_DURATION = {
    "a": 28.360, "b": 23.490, "c": 32.514,
    "d": 25.644, "e": 36.354, "f": 37.240,
    "g": 27.415, "h": 31.255, "i": 35.138,
}
SOURCE_FILE = {
    "a": "14_09___1_2160p1111111111", "b": "14_09___1_2160p11111111111", "c": "14_09___1_2160p111111111111",
    "d": "14_09___2_2160p2222", "e": "14_09___2_2160p222222222222", "f": "14_09___2_2160p2222222222222",
    "g": "14_09___3_2160p33333333", "h": "14_09___3_2160p333333333333", "i": "14_09___3_2160p33333333333333333",
}

# ASR mis-transcriptions to fix in place before building captions (same
# pattern used for the recurring "одиннадцатиклассники" split in earlier
# batches): keyed by episode letter, each entry {index_from_end_ignored: ...}
# simpler here: list of (old_text, start, new_text) matched by start time.
WORD_FIXES = {
    "f": [(16.56, "вторая")],  # stray "п" fragment merged into the next word
    "i": [(3.75, "тратят"), (4.56, "поиск")],
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
    words = json.load(open(f"../asr_coffee123_9/{src}_words.json"))
    for w in words:
        w["start"] = min(w["start"], total_duration)
        w["end"] = min(w["end"], total_duration)

    fixes = WORD_FIXES.get(letter, [])
    if fixes:
        fixed = []
        skip_next_merge = False
        for i, w in enumerate(words):
            matched = None
            for start_ts, new_text in fixes:
                if abs(w["start"] - start_ts) < 0.02:
                    matched = new_text
                    break
            if matched is not None and letter == "f":
                # merge the stray "п" fragment into the following word
                nxt = words[i + 1]
                fixed.append({"text": matched, "start": w["start"], "end": nxt["end"]})
                skip_next_merge = True
                continue
            if skip_next_merge:
                skip_next_merge = False
                continue
            if matched is not None:
                fixed.append({"text": matched, "start": w["start"], "end": w["end"]})
                continue
            fixed.append(w)
        words = fixed

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
# Episode A (girl-bookshelf, 28.360s): judging a solution from a classmate's
# chat-photo showing only the final answer; the app attaches a voiced
# walkthrough right to the task that stays even without the photo
# ---------------------------------------------------------------------------
a_intro = {"lines": ["ВИДНО ТОЛЬКО", "ОТВЕТ В ЧАТЕ?"], "end": 2.3}
a_cards = [
    {"start": 2.61, "end": 4.05, "lines": [{"text": "РАЗБИРАЕШЬ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ПО ФОТО", "accent": True, "size": "big"}]},
    {"start": 4.11, "end": 5.40, "lines": [{"text": "ФОТО ОДНОКЛАССНИКОВ", "accent": False, "size": "small"}, {"text": "ЧАТА", "accent": True, "size": "big"}]},
    {"start": 7.23, "end": 8.55, "lines": [{"text": "ВИДЕН ТОЛЬКО", "accent": False, "size": "small"}, {"text": "ОТВЕТ", "accent": True, "size": "big"}]},
    {"start": 9.51, "end": 10.68, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДОБАВЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 10.83, "end": 12.30, "lines": [{"text": "К ЗАДАНИЮ", "accent": False, "size": "small"}, {"text": "РАЗБОР", "accent": True, "size": "big"}]},
    {"start": 14.46, "end": 15.81, "lines": [{"text": "ОТ УСЛОВИЯ", "accent": False, "size": "small"}, {"text": "ДО ОТВЕТА", "accent": True, "size": "big"}]},
    {"start": 16.65, "end": 17.67, "lines": [{"text": "РАЗБОР", "accent": False, "size": "small"}, {"text": "ХРАНИТСЯ РЯДОМ", "accent": True, "size": "big"}]},
    {"start": 18.48, "end": 20.82, "lines": [{"text": "НЕ ТЕРЯЕТСЯ", "accent": False, "size": "small"}, {"text": "СРЕДИ ФОТО", "accent": True, "size": "big"}]},
    {"start": 21.75, "end": 23.85, "lines": [{"text": "ХОД МЫСЛЕЙ", "accent": False, "size": "small"}, {"text": "ПОНЯТЕН", "accent": True, "size": "big"}]},
    {"start": 24.06, "end": 25.71, "lines": [{"text": "БЕЗ ЧУЖОГО", "accent": False, "size": "small"}, {"text": "ФОТО", "accent": True, "size": "big"}]},
    {"start": 26.46, "end": 28.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
a_emphasis = [{"start": 7.80, "end": 8.55}, {"start": 13.44, "end": 14.16}, {"start": 22.95, "end": 23.85}]
process("a", a_cards, a_intro, a_emphasis)

# ---------------------------------------------------------------------------
# Episode B (sunset-boy, 23.490s): losing a whole prep day fishing with dad
# where signal drops out; the app keeps the FIPI bank on the phone already,
# opens just as fast with or without signal
# ---------------------------------------------------------------------------
b_intro = {"lines": ["ДЕНЬ БЕЗ СВЯЗИ", "НА РЫБАЛКЕ?"], "end": 2.3}
b_cards = [
    {"start": 2.43, "end": 3.48, "lines": [{"text": "ТЕРЯЕШЬ ДЕНЬ", "accent": False, "size": "small"}, {"text": "НА РЫБАЛКЕ", "accent": True, "size": "big"}]},
    {"start": 3.66, "end": 5.52, "lines": [{"text": "СВЯЗЬ ПРОПАДАЕТ", "accent": False, "size": "small"}, {"text": "НА ВЕСЬ ДЕНЬ", "accent": True, "size": "big"}]},
    {"start": 5.88, "end": 7.35, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДЕРЖИТ БАНК", "accent": True, "size": "big"}]},
    {"start": 7.44, "end": 8.91, "lines": [{"text": "В ПАМЯТИ", "accent": False, "size": "small"}, {"text": "ТЕЛЕФОНА", "accent": True, "size": "big"}]},
    {"start": 9.10, "end": 9.93, "lines": [{"text": "И ДЕНЬ", "accent": False, "size": "small"}, {"text": "НА РЫБАЛКЕ", "accent": True, "size": "big"}]},
    {"start": 10.20, "end": 11.34, "lines": [{"text": "НЕ ВЫПАДАЕТ", "accent": False, "size": "small"}, {"text": "ИЗ ПОДГОТОВКИ", "accent": True, "size": "big"}]},
    {"start": 11.67, "end": 12.50, "lines": [{"text": "ОТКРЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 12.60, "end": 13.74, "lines": [{"text": "ТАК ЖЕ РОВНО", "accent": False, "size": "small"}, {"text": "КАК В КОМНАТЕ", "accent": True, "size": "big"}]},
    {"start": 14.01, "end": 14.97, "lines": [{"text": "С ПОЛНЫМ", "accent": False, "size": "small"}, {"text": "СИГНАЛОМ СЕТИ", "accent": True, "size": "big"}]},
    {"start": 15.39, "end": 16.20, "lines": [{"text": "ЛОВИТ СЕТЬ", "accent": False, "size": "small"}, {"text": "ИЛИ НЕТ", "accent": True, "size": "big"}]},
    {"start": 16.35, "end": 18.18, "lines": [{"text": "ЗАДАНИЯ ОТКРЫВАЮТСЯ", "accent": False, "size": "small"}, {"text": "ОДИНАКОВО БЫСТРО", "accent": True, "size": "big"}]},
    {"start": 18.20, "end": 19.05, "lines": [{"text": "ДЕНЬ", "accent": False, "size": "small"}, {"text": "НА РЫБАЛКЕ", "accent": True, "size": "big"}]},
    {"start": 19.23, "end": 21.45, "lines": [{"text": "ПЕРЕСТАЕТ ВЫПАДАТЬ", "accent": False, "size": "small"}, {"text": "ИЗ ГРАФИКА", "accent": True, "size": "big"}]},
    {"start": 21.75, "end": 23.49, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
b_emphasis = [{"start": 3.93, "end": 4.68}, {"start": 12.06, "end": 12.78}, {"start": 19.23, "end": 20.07}]
process("b", b_cards, b_intro, b_emphasis)

# ---------------------------------------------------------------------------
# Episode C (girl-warm-sweater, 32.514s): confusing similar physics formulas
# on every other test; the app builds a dedicated game for exactly those
# formulas and switches to a new one automatically once they stop confusing
# ---------------------------------------------------------------------------
c_intro = {"lines": ["ПУТАЕШЬ ПОХОЖИЕ", "ФОРМУЛЫ ПО ФИЗИКЕ?"], "end": 2.3}
c_cards = [
    {"start": 2.55, "end": 3.84, "lines": [{"text": "ПУТАЕШЬ ФОРМУЛЫ", "accent": False, "size": "small"}, {"text": "ПО ФИЗИКЕ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 5.82, "lines": [{"text": "КАЖДЫЙ КОНТРОЛЬНЫЙ", "accent": False, "size": "small"}, {"text": "ВТОРОЙ", "accent": True, "size": "big"}]},
    {"start": 6.78, "end": 8.04, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВЫДЕЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 8.28, "end": 9.66, "lines": [{"text": "ПОД ТАКИЕ", "accent": False, "size": "small"}, {"text": "ФОРМУЛЫ", "accent": True, "size": "big"}]},
    {"start": 9.84, "end": 11.49, "lines": [{"text": "ОТДЕЛЬНУЮ ИГРУ", "accent": False, "size": "small"}, {"text": "С ВАРИАНТАМИ", "accent": True, "size": "big"}]},
    {"start": 12.42, "end": 13.41, "lines": [{"text": "ПОХОЖИМИ", "accent": False, "size": "small"}, {"text": "ДРУГ НА ДРУГА", "accent": True, "size": "big"}]},
    {"start": 13.65, "end": 14.97, "lines": [{"text": "СПЕЦИАЛЬНО", "accent": False, "size": "small"}, {"text": "ИГРА", "accent": True, "size": "big"}]},
    {"start": 15.18, "end": 16.02, "lines": [{"text": "УСЛОЖНЯЕТСЯ", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 16.17, "end": 17.91, "lines": [{"text": "ПРОСТЫЕ ВАРИАНТЫ", "accent": False, "size": "small"}, {"text": "ПЕРЕСТАЮТ", "accent": True, "size": "big"}]},
    {"start": 19.23, "end": 21.75, "lines": [{"text": "ПЕРЕКЛЮЧАЕТСЯ САМА", "accent": False, "size": "small"}, {"text": "НА ФОРМУЛУ", "accent": True, "size": "big"}]},
    {"start": 22.44, "end": 23.64, "lines": [{"text": "БЕЗ ВЫБОРА", "accent": False, "size": "small"}, {"text": "ТЕМЫ ВРУЧНУЮ", "accent": True, "size": "big"}]},
    {"start": 23.88, "end": 24.93, "lines": [{"text": "ПЕРЕД КАЖДЫМ", "accent": False, "size": "small"}, {"text": "РАУНДОМ", "accent": True, "size": "big"}]},
    {"start": 25.83, "end": 27.60, "lines": [{"text": "ПОХОЖИЕ ФОРМУЛЫ", "accent": False, "size": "small"}, {"text": "ПЕРЕСТАЮТ ПУТАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 27.87, "end": 29.91, "lines": [{"text": "ЧЕРЕЗ НЕСКОЛЬКО", "accent": False, "size": "small"}, {"text": "КОРОТКИХ РАУНДОВ", "accent": True, "size": "big"}]},
    {"start": 30.69, "end": 32.40, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
c_emphasis = [{"start": 1.68, "end": 2.40}, {"start": 15.18, "end": 15.69}, {"start": 26.79, "end": 27.60}]
process("c", c_cards, c_intro, c_emphasis)

# ---------------------------------------------------------------------------
# Episode D (sunset-boy, 25.644s): confusing similar dates when events are
# only a couple of years apart; the app builds a dedicated game for exactly
# those close pairs, selected automatically
# ---------------------------------------------------------------------------
d_intro = {"lines": ["ПУТАЕШЬ ПОХОЖИЕ", "ДАТЫ ПО ЕГЭ?"], "end": 2.3}
d_cards = [
    {"start": 2.34, "end": 4.11, "lines": [{"text": "ПОХОЖИЕ ДАТЫ", "accent": False, "size": "small"}, {"text": "ПО ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 4.23, "end": 5.46, "lines": [{"text": "ПРОХОДИТ", "accent": False, "size": "small"}, {"text": "ПАРА ЛЕТ", "accent": True, "size": "big"}]},
    {"start": 5.82, "end": 7.71, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ВЫДЕЛЯЕТ ИГРУ", "accent": True, "size": "big"}]},
    {"start": 7.95, "end": 9.21, "lines": [{"text": "БЛИЗКИЕ ПО", "accent": False, "size": "small"}, {"text": "ВРЕМЕНИ ДАТЫ", "accent": True, "size": "big"}]},
    {"start": 9.36, "end": 10.53, "lines": [{"text": "РАЗНИЦА", "accent": False, "size": "small"}, {"text": "МЕЖДУ НИМИ", "accent": True, "size": "big"}]},
    {"start": 10.71, "end": 12.03, "lines": [{"text": "ЗАКРЕПЛЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ОТДЕЛЬНО", "accent": True, "size": "big"}]},
    {"start": 12.21, "end": 13.26, "lines": [{"text": "ИГРА ПРЕДЛАГАЕТ", "accent": False, "size": "small"}, {"text": "ТАКИЕ ПАРЫ", "accent": True, "size": "big"}]},
    {"start": 14.31, "end": 15.30, "lines": [{"text": "ПУТАНИЦА", "accent": False, "size": "small"}, {"text": "НЕ ПРОПАДЕТ", "accent": True, "size": "big"}]},
    {"start": 15.66, "end": 16.92, "lines": [{"text": "ПОДБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "ПАРА ДАТ", "accent": True, "size": "big"}]},
    {"start": 17.04, "end": 18.69, "lines": [{"text": "АВТОМАТИЧЕСКИ", "accent": False, "size": "small"}, {"text": "БЕЗ ВЫБОРА", "accent": True, "size": "big"}]},
    {"start": 18.84, "end": 19.74, "lines": [{"text": "КОНКРЕТНОГО", "accent": False, "size": "small"}, {"text": "СОБЫТИЯ", "accent": True, "size": "big"}]},
    {"start": 20.07, "end": 21.21, "lines": [{"text": "ПАРА ЛЕТ", "accent": False, "size": "small"}, {"text": "МЕЖДУ СОБЫТИЯМИ", "accent": True, "size": "big"}]},
    {"start": 21.36, "end": 22.20, "lines": [{"text": "ПЕРЕСТАЕТ", "accent": False, "size": "small"}, {"text": "СТИРАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 22.44, "end": 23.55, "lines": [{"text": "РАСПЛЫВЧАТЫЙ", "accent": False, "size": "small"}, {"text": "ПЕРИОД", "accent": True, "size": "big"}]},
    {"start": 23.85, "end": 25.60, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
d_emphasis = [{"start": 1.89, "end": 2.49}, {"start": 14.31, "end": 14.73}, {"start": 21.87, "end": 22.20}]
process("d", d_cards, d_intro, d_emphasis)

# ---------------------------------------------------------------------------
# Episode E (girl-bookshelf, 36.354s): juggling olympiad prep across several
# subjects while one EGE subject quietly slips; the app aggregates results
# per subject and flags whichever one is falling behind, before it can hurt
# the overall result
# ---------------------------------------------------------------------------
e_intro = {"lines": ["ОДИН ПРЕДМЕТ", "ПРОСЕДАЕТ НЕЗАМЕТНО?"], "end": 2.3}
e_cards = [
    {"start": 2.40, "end": 3.66, "lines": [{"text": "ПО НЕСКОЛЬКИМ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТАМ СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 4.17, "end": 5.73, "lines": [{"text": "НЕ ЗАМЕЧАЕШЬ", "accent": False, "size": "small"}, {"text": "КАКОЙ ПРЕДМЕТ", "accent": True, "size": "big"}]},
    {"start": 5.97, "end": 6.90, "lines": [{"text": "ЕГЭ", "accent": False, "size": "small"}, {"text": "ПРОСЕДАЕТ", "accent": True, "size": "big"}]},
    {"start": 7.02, "end": 8.46, "lines": [{"text": "НЕЗАМЕТНО", "accent": False, "size": "small"}, {"text": "НА ФОНЕ", "accent": True, "size": "big"}]},
    {"start": 9.78, "end": 11.46, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СКЛАДЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 11.64, "end": 13.47, "lines": [{"text": "ПО КАЖДОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 14.01, "end": 16.11, "lines": [{"text": "ВЫДЕЛЯЕТ ТОТ", "accent": False, "size": "small"}, {"text": "ЧТО ОТСТАЕТ", "accent": True, "size": "big"}]},
    {"start": 17.07, "end": 18.42, "lines": [{"text": "КАРТИНА ПЕРЕСЧИТЫВАЕТСЯ", "accent": False, "size": "small"}, {"text": "САМА", "accent": True, "size": "big"}]},
    {"start": 18.72, "end": 20.25, "lines": [{"text": "ПОСЛЕ КАЖДОГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 20.85, "end": 21.90, "lines": [{"text": "БЕЗ РУЧНОГО", "accent": False, "size": "small"}, {"text": "СРАВНЕНИЯ", "accent": True, "size": "big"}]},
    {"start": 22.86, "end": 23.94, "lines": [{"text": "ТАКАЯ КАРТИНА", "accent": False, "size": "small"}, {"text": "УЧИТЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 24.06, "end": 25.71, "lines": [{"text": "ТОЛЬКО РЕАЛЬНО", "accent": False, "size": "small"}, {"text": "РЕШЕННЫЕ", "accent": True, "size": "big"}]},
    {"start": 26.19, "end": 27.66, "lines": [{"text": "А НЕ ОБЩЕЕ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 28.83, "end": 30.45, "lines": [{"text": "ОТСТАЮЩИЙ ПРЕДМЕТ", "accent": False, "size": "small"}, {"text": "ЗАМЕТЕН", "accent": True, "size": "big"}]},
    {"start": 30.57, "end": 33.45, "lines": [{"text": "РАНЬШЕ ЧЕМ", "accent": False, "size": "small"}, {"text": "ПОВЛИЯЕТ", "accent": True, "size": "big"}]},
    {"start": 34.50, "end": 36.15, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
e_emphasis = [{"start": 6.54, "end": 7.44}, {"start": 17.49, "end": 18.09}, {"start": 29.67, "end": 30.45}]
process("e", e_cards, e_intro, e_emphasis)

# ---------------------------------------------------------------------------
# Episode F (girl-warm-sweater, 37.240s): comparing an EGE task against an
# old textbook / internet version and finding different wording; the app
# keeps only one current official wording, synced automatically with every
# bank update
# ---------------------------------------------------------------------------
f_intro = {"lines": ["РАЗНЫЕ ФОРМУЛИРОВКИ", "У ОДНОГО ЗАДАНИЯ?"], "end": 2.3}
f_cards = [
    {"start": 2.43, "end": 3.66, "lines": [{"text": "СРАВНИВАЕШЬ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "И УЧЕБНИК", "accent": True, "size": "big"}]},
    {"start": 4.20, "end": 5.37, "lines": [{"text": "ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "ИЗ ИНТЕРНЕТА", "accent": True, "size": "big"}]},
    {"start": 5.85, "end": 7.98, "lines": [{"text": "НАХОДИШЬ РАЗНЫЕ ФОРМУЛИРОВКИ", "accent": False, "size": "small"}, {"text": "УСЛОВИЯ", "accent": True, "size": "big"}]},
    {"start": 9.03, "end": 10.14, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДЕРЖИТ", "accent": True, "size": "big"}]},
    {"start": 10.32, "end": 11.79, "lines": [{"text": "ТОЛЬКО ДЕЙСТВУЮЩУЮ", "accent": False, "size": "small"}, {"text": "ОДНУ", "accent": True, "size": "big"}]},
    {"start": 11.97, "end": 13.32, "lines": [{"text": "ФОРМУЛИРОВКУ", "accent": False, "size": "small"}, {"text": "КОТОРАЯ", "accent": True, "size": "big"}]},
    {"start": 13.44, "end": 14.25, "lines": [{"text": "МЕНЯЕТСЯ", "accent": False, "size": "small"}, {"text": "ВСЛЕД", "accent": True, "size": "big"}]},
    {"start": 14.55, "end": 16.23, "lines": [{"text": "ЗА ОФИЦИАЛЬНОЙ", "accent": False, "size": "small"}, {"text": "ДЕМО ВЕРСИЕЙ", "accent": True, "size": "big"}]},
    {"start": 16.56, "end": 18.93, "lines": [{"text": "УСТАРЕВШАЯ", "accent": False, "size": "small"}, {"text": "ВЕРСИЯ", "accent": True, "size": "big"}]},
    {"start": 19.14, "end": 20.52, "lines": [{"text": "ТОГО ЖЕ ЗАДАНИЯ", "accent": False, "size": "small"}, {"text": "ПРОСТО", "accent": True, "size": "big"}]},
    {"start": 20.85, "end": 21.87, "lines": [{"text": "НЕ ВОЗНИКАЕТ", "accent": False, "size": "small"}, {"text": "В ПРИЛОЖЕНИИ", "accent": True, "size": "big"}]},
    {"start": 22.56, "end": 23.49, "lines": [{"text": "ФОРМУЛИРОВКИ", "accent": False, "size": "small"}, {"text": "ПРОВЕРКА", "accent": True, "size": "big"}]},
    {"start": 23.67, "end": 24.87, "lines": [{"text": "АВТОМАТИЧЕСКИ", "accent": False, "size": "small"}, {"text": "ПРОИСХОДИТ", "accent": True, "size": "big"}]},
    {"start": 25.41, "end": 26.76, "lines": [{"text": "ПРИ КАЖДОМ", "accent": False, "size": "small"}, {"text": "ОБНОВЛЕНИИ", "accent": True, "size": "big"}]},
    {"start": 27.39, "end": 28.89, "lines": [{"text": "БЕЗ СВЕРКИ", "accent": False, "size": "small"}, {"text": "ПО ДАТАМ", "accent": True, "size": "big"}]},
    {"start": 29.70, "end": 31.80, "lines": [{"text": "РАЗНОЧТЕНИЯ", "accent": False, "size": "small"}, {"text": "ПРОПАДАЮТ", "accent": True, "size": "big"}]},
    {"start": 32.13, "end": 33.99, "lines": [{"text": "КОГДА ИСТОЧНИК", "accent": False, "size": "small"}, {"text": "ОДИН", "accent": True, "size": "big"}]},
    {"start": 34.98, "end": 36.90, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
f_emphasis = [{"start": 5.94, "end": 7.41}, {"start": 22.56, "end": 23.49}, {"start": 31.35, "end": 31.80}]
process("f", f_cards, f_intro, f_emphasis)

# ---------------------------------------------------------------------------
# Episode G (sunset-boy, 27.415s): comparing your own results only by memory
# of last week with no other benchmark; the app adds a friend score that
# updates the instant anyone on the list closes a new task
# ---------------------------------------------------------------------------
g_intro = {"lines": ["СРАВНИВАЕШЬ ПО ПАМЯТИ", "О ПРОШЛОЙ НЕДЕЛЕ?"], "end": 2.3}
g_cards = [
    {"start": 2.46, "end": 3.78, "lines": [{"text": "СРАВНИВАЕШЬ", "accent": False, "size": "small"}, {"text": "ПО ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 3.87, "end": 5.04, "lines": [{"text": "СОБСТВЕННОЙ", "accent": False, "size": "small"}, {"text": "ПАМЯТЬЮ", "accent": True, "size": "big"}]},
    {"start": 5.37, "end": 6.24, "lines": [{"text": "БЕЗ ДРУГИХ", "accent": False, "size": "small"}, {"text": "ОРИЕНТИРОВ", "accent": True, "size": "big"}]},
    {"start": 6.99, "end": 8.01, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ДОБАВЛЯЕТ", "accent": True, "size": "big"}]},
    {"start": 8.22, "end": 9.24, "lines": [{"text": "ОБЩИЙ СЧЕТ", "accent": False, "size": "small"}, {"text": "СРЕДИ ДРУЗЕЙ", "accent": True, "size": "big"}]},
    {"start": 9.42, "end": 10.44, "lines": [{"text": "КОТОРЫЕ ДАЮТ", "accent": False, "size": "small"}, {"text": "ОРИЕНТИР", "accent": True, "size": "big"}]},
    {"start": 10.65, "end": 11.79, "lines": [{"text": "ТОЧНЕЕ", "accent": False, "size": "small"}, {"text": "ПАМЯТИ", "accent": True, "size": "big"}]},
    {"start": 12.21, "end": 13.23, "lines": [{"text": "ОБНОВЛЯЕТСЯ СРАЗУ", "accent": False, "size": "small"}, {"text": "СЧЕТ", "accent": True, "size": "big"}]},
    {"start": 13.35, "end": 14.49, "lines": [{"text": "КАК ТОЛЬКО", "accent": False, "size": "small"}, {"text": "КТО ТО", "accent": True, "size": "big"}]},
    {"start": 14.67, "end": 15.84, "lines": [{"text": "ЗАКРЫВАЕТ", "accent": False, "size": "small"}, {"text": "НОВОЕ ЗАДАНИЕ", "accent": True, "size": "big"}]},
    {"start": 16.20, "end": 17.22, "lines": [{"text": "СПИСОК ДРУЗЕЙ", "accent": False, "size": "small"}, {"text": "ДЛЯ СЧЕТА", "accent": True, "size": "big"}]},
    {"start": 17.40, "end": 18.33, "lines": [{"text": "СОБИРАЕТСЯ", "accent": False, "size": "small"}, {"text": "ОДИН РАЗ", "accent": True, "size": "big"}]},
    {"start": 18.51, "end": 19.50, "lines": [{"text": "И НЕ", "accent": False, "size": "small"}, {"text": "ТРЕБУЕТ", "accent": True, "size": "big"}]},
    {"start": 19.62, "end": 20.91, "lines": [{"text": "ПРИГЛАШЕНИЯ", "accent": False, "size": "small"}, {"text": "КАЖДУЮ НЕДЕЛЮ", "accent": True, "size": "big"}]},
    {"start": 21.33, "end": 22.29, "lines": [{"text": "ОБЩИЙ СЧЕТ", "accent": False, "size": "small"}, {"text": "СРЕДИ ДРУЗЕЙ", "accent": True, "size": "big"}]},
    {"start": 22.47, "end": 24.06, "lines": [{"text": "СТАНОВИТСЯ", "accent": False, "size": "small"}, {"text": "ТОЧНЫМ", "accent": True, "size": "big"}]},
    {"start": 24.18, "end": 25.38, "lines": [{"text": "ЧЕМ ПАМЯТЬ", "accent": False, "size": "small"}, {"text": "О НЕДЕЛЕ", "accent": True, "size": "big"}]},
    {"start": 25.68, "end": 27.30, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
g_emphasis = [{"start": 3.87, "end": 4.17}, {"start": 12.48, "end": 12.90}, {"start": 22.47, "end": 22.83}]
process("g", g_cards, g_intro, g_emphasis)

# ---------------------------------------------------------------------------
# Episode H (girl-warm-sweater, 31.255s): giving up mid-month when there is
# no one to compare results with; the app shows an overall classmate rank
# updated after every closed task, visible right when the app opens
# ---------------------------------------------------------------------------
h_intro = {"lines": ["БРОСАЕШЬ ЕГЭ", "В СЕРЕДИНЕ МЕСЯЦА?"], "end": 2.3}
h_cards = [
    {"start": 2.55, "end": 3.75, "lines": [{"text": "БРОСАЕШЬ ЗАДАНИЕ", "accent": False, "size": "small"}, {"text": "В СЕРЕДИНЕ", "accent": True, "size": "big"}]},
    {"start": 4.32, "end": 6.30, "lines": [{"text": "ЕСЛИ РЕЗУЛЬТАТ", "accent": False, "size": "small"}, {"text": "СРАВНИТЬ", "accent": True, "size": "big"}]},
    {"start": 6.42, "end": 7.25, "lines": [{"text": "НЕ С", "accent": False, "size": "small"}, {"text": "КЕМ", "accent": True, "size": "big"}]},
    {"start": 7.77, "end": 8.82, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "СЧИТАЕТ", "accent": True, "size": "big"}]},
    {"start": 9.06, "end": 10.53, "lines": [{"text": "ОБЩИЙ СРЕДИ ОДНОКЛАССНИКОВ", "accent": False, "size": "small"}, {"text": "БАЛЛ", "accent": True, "size": "big"}]},
    {"start": 10.95, "end": 11.85, "lines": [{"text": "ОБНОВЛЯЕТ", "accent": False, "size": "small"}, {"text": "МЕСТО", "accent": True, "size": "big"}]},
    {"start": 12.45, "end": 13.92, "lines": [{"text": "ПОСЛЕ КАЖДОГО", "accent": False, "size": "small"}, {"text": "ЗАДАНИЯ", "accent": True, "size": "big"}]},
    {"start": 14.70, "end": 16.17, "lines": [{"text": "СПИСОК ВИДЕН", "accent": False, "size": "small"}, {"text": "ВНУТРИ", "accent": True, "size": "big"}]},
    {"start": 16.44, "end": 18.30, "lines": [{"text": "И НЕ ТРЕБУЕТ", "accent": False, "size": "small"}, {"text": "ГРУППЫ", "accent": True, "size": "big"}]},
    {"start": 19.02, "end": 19.89, "lines": [{"text": "СПИСОК ВИДНО", "accent": False, "size": "small"}, {"text": "СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 20.04, "end": 21.00, "lines": [{"text": "ПРИ ВХОДЕ", "accent": False, "size": "small"}, {"text": "В ПРИЛОЖЕНИЕ", "accent": True, "size": "big"}]},
    {"start": 21.51, "end": 23.49, "lines": [{"text": "БЕЗ ПЕРЕХОДА", "accent": False, "size": "small"}, {"text": "В РАЗДЕЛ СТАТИСТИКИ", "accent": True, "size": "big"}]},
    {"start": 24.57, "end": 25.83, "lines": [{"text": "СЕРЕДИНА МЕСЯЦА", "accent": False, "size": "small"}, {"text": "ПЕРЕСТАЕТ", "accent": True, "size": "big"}]},
    {"start": 25.98, "end": 27.33, "lines": [{"text": "БЫТЬ ТОЧКОЙ", "accent": False, "size": "small"}, {"text": "ГДЕ ПРОПАДАЕТ", "accent": True, "size": "big"}]},
    {"start": 27.51, "end": 28.53, "lines": [{"text": "ВЕСЬ ИНТЕРЕС", "accent": False, "size": "small"}, {"text": "ЗАНИМАТЬСЯ", "accent": True, "size": "big"}]},
    {"start": 29.46, "end": 31.20, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
h_emphasis = [{"start": 1.26, "end": 1.92}, {"start": 14.70, "end": 15.18}, {"start": 25.44, "end": 25.83}]
process("h", h_cards, h_intro, h_emphasis)

# ---------------------------------------------------------------------------
# Episode I (girl-bookshelf, 35.138s): combining olympiad prep with EGE and
# wasting time hunting a tutor for each extra subject; the app covers those
# subjects with a free task bank and explanations instead
# ---------------------------------------------------------------------------
i_intro = {"lines": ["ИЩЕШЬ РЕПЕТИТОРА", "НА КАЖДЫЙ ПРЕДМЕТ?"], "end": 2.3}
i_cards = [
    {"start": 2.49, "end": 3.33, "lines": [{"text": "ОЛИМПИАДЫ", "accent": False, "size": "small"}, {"text": "С ЕГЭ", "accent": True, "size": "big"}]},
    {"start": 3.75, "end": 4.74, "lines": [{"text": "ТРАТИШЬ ВРЕМЯ", "accent": False, "size": "small"}, {"text": "НА ПОИСК", "accent": True, "size": "big"}]},
    {"start": 4.83, "end": 6.00, "lines": [{"text": "К РЕПЕТИТОРУ", "accent": False, "size": "small"}, {"text": "КАЖДОМУ", "accent": True, "size": "big"}]},
    {"start": 6.12, "end": 7.80, "lines": [{"text": "ДОПОЛНИТЕЛЬНОМУ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТУ", "accent": True, "size": "big"}]},
    {"start": 8.70, "end": 9.96, "lines": [{"text": "ЕГЭ ТРЕНАЖЕР", "accent": False, "size": "small"}, {"text": "ЗАКРЫВАЕТ", "accent": True, "size": "big"}]},
    {"start": 10.14, "end": 11.37, "lines": [{"text": "ТАКИЕ ДОПОЛНИТЕЛЬНЫЕ", "accent": False, "size": "small"}, {"text": "ПРЕДМЕТЫ", "accent": True, "size": "big"}]},
    {"start": 11.82, "end": 13.20, "lines": [{"text": "БЕСПЛАТНЫМ", "accent": False, "size": "small"}, {"text": "БАНКОМ ЗАДАНИЙ", "accent": True, "size": "big"}]},
    {"start": 13.47, "end": 15.00, "lines": [{"text": "И РАЗБОРАМ", "accent": False, "size": "small"}, {"text": "БЕЗ ПОИСКА", "accent": True, "size": "big"}]},
    {"start": 15.15, "end": 16.11, "lines": [{"text": "ОТДЕЛЬНОГО", "accent": False, "size": "small"}, {"text": "РЕПЕТИТОРА", "accent": True, "size": "big"}]},
    {"start": 16.74, "end": 18.21, "lines": [{"text": "НА ПОИСК ОСВОБОЖДАЕТСЯ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 18.33, "end": 20.64, "lines": [{"text": "ДЛЯ ЗАНЯТИЙ ОЛИМПИАДНЫМИ", "accent": False, "size": "small"}, {"text": "ЗАДАЧАМИ", "accent": True, "size": "big"}]},
    {"start": 21.39, "end": 22.59, "lines": [{"text": "ОСВОБОДИВШЕЕСЯ ОТ", "accent": False, "size": "small"}, {"text": "ВРЕМЯ", "accent": True, "size": "big"}]},
    {"start": 22.92, "end": 24.27, "lines": [{"text": "ПОИСКОВ", "accent": False, "size": "small"}, {"text": "МОЖНО СРАЗУ", "accent": True, "size": "big"}]},
    {"start": 24.45, "end": 25.92, "lines": [{"text": "ПОТРАТИТЬ НА", "accent": False, "size": "small"}, {"text": "РАЗБОР СЛОЖНЫЙ", "accent": True, "size": "big"}]},
    {"start": 26.07, "end": 26.97, "lines": [{"text": "ОЛИМПИАДНОЙ", "accent": False, "size": "small"}, {"text": "ЗАДАЧИ", "accent": True, "size": "big"}]},
    {"start": 27.78, "end": 29.34, "lines": [{"text": "ВРЕМЯ НА", "accent": False, "size": "small"}, {"text": "ПОДГОТОВКУ", "accent": True, "size": "big"}]},
    {"start": 29.76, "end": 30.66, "lines": [{"text": "БОЛЬШЕ НЕ", "accent": False, "size": "small"}, {"text": "УХОДИТ", "accent": True, "size": "big"}]},
    {"start": 30.78, "end": 32.52, "lines": [{"text": "НА БЕСКОНЕЧНЫЙ", "accent": False, "size": "small"}, {"text": "ПОИСК", "accent": True, "size": "big"}]},
    {"start": 33.18, "end": 34.98, "lines": [{"text": "ССЫЛКА", "accent": True, "size": "big"}, {"text": "В ШАПКЕ ПРОФИЛЯ", "accent": False, "size": "small"}]},
]
i_emphasis = [{"start": 3.75, "end": 4.74}, {"start": 17.64, "end": 18.21}, {"start": 30.45, "end": 30.66}]
process("i", i_cards, i_intro, i_emphasis)

print("ALL EPISODES BUILT AND VALIDATED")
