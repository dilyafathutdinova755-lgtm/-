# -*- coding: utf-8 -*-
"""Двухслойные субтитры по brand-kit.md §4 (карточка + бегущая подпись) -> ASS."""
import json
from PIL import ImageFont

W, H = 1080, 1920
WHITE  = "&H00FFFFFF&"
ACCENT = "&H00FFF5C9&"          # #C9F5FF, BGR
GREY   = "&H00F0F0F0&"
F_DISP = "Golos Text Black"
F_BODY = "Manrope Caption"

SIDE      = 70                   # поля по бокам (delivery-specs §4)
TOP_UI    = 180                  # зона иконок платформы
BOT_UI    = 420                  # зона UI TikTok -> текст выше y=1500
CARD_MID  = 1240                 # центр полосы 55-75% высоты (1056..1440)

_fc = {}
def _font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def tw(text, path, size):
    f = _font(path, size)
    return f.getbbox(text)[2] - f.getbbox(text)[0]

def ts(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

# ── КАРТОЧКИ (слой 1) ────────────────────────────────────────────────────────
# (start, end, [ [ (текст, 'main'|'small', 'w'|'a'), ... ] строки ])
CARDS = [
 (0.09, 2.45, [[("РАСПИСАНИЕ","main","w")], [("К ЕГЭ","small","a")]]),
 (2.57, 4.25, [[("ПРИЛОЖЕНИЕ","main","w")], [("для планирования","small","a")]]),
 (4.45, 6.60, [[("ЦВЕТНЫЕ БЛОКИ","main","w")], [("и напоминания","small","a")]]),
 (6.97, 8.20, [[("ЭТО Я","main","w")]]),
 (8.35, 10.35,[[("ИДЕАЛЬНОЕ","small","a")], [("РАСПИСАНИЕ","main","w")]]),
 (10.61,11.85,[[("ЭТО ЖЕ Я","main","w")]]),
 (11.95,14.75,[[("ИГНОРИРУЮ","main","a")], [("всё подряд","small","w")]]),
 (15.45,17.00,[[("ПРИЛОЖЕНИЕ","main","w")]]),
 (17.05,18.15,[[("реальная","small","w")], [("СИЛА ВОЛИ","main","a")]]),
 (18.29,20.90,[[("ДВЕ РАЗНЫЕ","small","w")], [("ИСТОРИИ","main","a")]]),
 (22.04,23.90,[[("ПЕРЕСТАЛ","main","w")], [("городить системы","small","a")]]),
 (24.44,26.30,[[("ЕГЭ","small","w")], [("ТРЕНАЖЁР","main","a")]]),
 (26.44,28.55,[[("БЕЗ","small","w")], [("ПОСРЕДНИКОВ","main","w")]]),
 (28.72,30.53,[[("ССЫЛКА","main","a")], [("в шапке профиля","small","w")]]),
]
MAIN_PX, SMALL_PX, RUN_PX = 112, 56, 42
LINE_H = 0.90   # плотный межстрочный интервал в карточке

def card_events():
    ev = []
    for st, en, lines in CARDS:
        assert en - st <= 4.0, f"карточка >4с: {lines}"
        # ужимаем кегль, а не переносим (brand-kit §4)
        mp, sp = MAIN_PX, SMALL_PX
        for _ in range(40):
            widest = 0
            for ln in lines:
                w = sum(tw(t + " ", "fonts/GolosText-Black.ttf", mp if k == "main" else sp) for t, k, _ in ln)
                widest = max(widest, w)
            if widest <= W - 2 * SIDE: break
            mp -= 3; sp = max(34, sp - 1)
        n = len(lines)
        block_h = sum(mp if any(k == "main" for _, k, _ in ln) else sp for ln in lines) * LINE_H
        y = CARD_MID - block_h / 2
        for ln in lines:
            lh = (mp if any(k == "main" for _, k, _ in ln) else sp) * LINE_H
            parts = "".join(
                f"{{\\fs{mp if k=='main' else sp}\\c{ACCENT if c=='a' else WHITE}}}{t}"
                + ("{\\fs%d} " % (mp if k == 'main' else sp) if i < len(ln) - 1 else "")
                for i, (t, k, c) in enumerate(ln))
            eff = ("{\\an5\\pos(%d,%d)\\fscx94\\fscy94\\t(0,320,0.6,\\fscx100\\fscy100)\\fad(140,90)}"
                   % (W // 2, int(y + lh / 2)))
            ev.append((st, en, "Card", eff + parts))
            y += lh
    return ev

# ── БЕГУЩАЯ ПОДПИСЬ (слой 2) ─────────────────────────────────────────────────
# Слоты вне лица, вне полосы карточки, вне верхних 180px и нижних 420px.
SLOT_RUN = (W // 2, 300)      # единственный слот: сверху по центру, над лицом

def run_events():
    words = json.load(open("words.json"))
    fix = {"красивая": "красивое", "любую": "любующийся", "егэ": "ЕГЭ", "тренажёр": "Тренажёр"}
    units, i = [], 0
    while i < len(words):
        grp = words[i:i + 2] if len(words[i]["w"]) <= 5 and i + 1 < len(words) else words[i:i + 1]
        units.append(grp); i += len(grp)
    ev = []
    for j, grp in enumerate(units):
        st = 0.0 if j == 0 else grp[0]["t"]
        en = units[j + 1][0]["t"] if j + 1 < len(units) else 30.53
        txt = " ".join(fix.get(w["w"], w["w"]) for w in grp)
        ev.append((st, en, "Run", "{\\an5\\pos(%d,%d)}" % SLOT_RUN + txt))
    return ev

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Card,{F_DISP},{MAIN_PX},{WHITE},{WHITE},&H00101010&,&H80000000&,0,0,0,0,100,100,1,0,1,4,3,5,{SIDE},{SIDE},0,204
Style: Run,{F_BODY},{RUN_PX},{WHITE},{WHITE},&H00000000&,&HB0000000&,0,0,0,0,100,100,0,0,1,0,3,5,{SIDE},{SIDE},0,204

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for st, en, sty, txt in run_events():
    lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},Run,,0,0,0,,{txt}")
for st, en, sty, txt in card_events():
    lines.append(f"Dialogue: 1,{ts(st)},{ts(en)},Card,,0,0,0,,{txt}")
open("subs.ass", "w").write(head + "\n".join(lines) + "\n")
print("карточек:", len(CARDS), "| событий:", len(lines))
