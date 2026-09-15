# -*- coding: utf-8 -*-
"""Генератор субтитров по CLAUDE.md §1.4 (три слоя) + иконка §1.6 + эмфасис-зум §2.9.
Тёплый сет: accent = #FCF5AA, оранжевый = #FD5D01 (макс. 1 слово на ролик)."""
import json, re
from PIL import ImageFont

W, H = 1080, 1920
WHITE   = "&H00FFFFFF&"
ACCENT  = "&H00FFF5C9&"   # #C9F5FF в BGR — холодный сет (дневной свет, комната Влада)
ORANGE  = "&H00015DFD&"   # #FD5D01 в BGR — не используется в холодном сете

F_DISP = "Golos Text Black"
F_BODY = "PT Sans Narrow"

SIDE = 70
CARD_MID = 1240          # центр полосы 55-75% (1056..1440)
MAIN_PX, SMALL_PX, RUN_PX = 90, 44, 42
LINE_H = 0.90
ACCENT_BOOST = 1.10       # accent-строка крупнее белой на 10%
SLOT_RUN = (W // 2, 300)

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

def _color_hex(c):
    return {"w": WHITE, "a": ACCENT, "o": ORANGE}[c]

def _run_boost(c):
    # accent/orange runs крупнее и с собственной обводкой; белые — дефолт
    return c in ("a", "o")

def _fit_and_layout(lines, main_px, small_px, force_all_accent=False):
    """Подбирает кегль под ширину экрана, возвращает финальные (mp, sp)."""
    mp, sp = main_px, small_px
    for _ in range(40):
        widest = 0
        for ln in lines:
            w = 0
            for t, k, c in ln:
                size = mp if k == "main" else sp
                if not force_all_accent and _run_boost(c):
                    size = round(size * ACCENT_BOOST)
                w += tw(t + " ", "fonts/GolosText-Black.ttf", size)
            widest = max(widest, w)
        if widest <= W - 2 * SIDE:
            break
        mp -= 3; sp = max(30, sp - 1)
    return mp, sp

def _render_block(lines, mp, sp, force_all_accent=False):
    """Строит вертикальный блок строк с раскладкой по кеглю/цвету/обводке. Возвращает список (y_top, text_with_tags, line_h)."""
    heights = []
    for ln in lines:
        boosted = any((not force_all_accent) and _run_boost(c) and k == "main" for _, k, c in ln)
        base = mp if any(k == "main" for _, k, c in ln) else sp
        h = round(base * (ACCENT_BOOST if boosted else 1.0)) * LINE_H
        heights.append(h)
    total = sum(heights)
    y = CARD_MID - total / 2
    out = []
    for ln, lh in zip(lines, heights):
        parts = []
        for i, (t, k, c) in enumerate(ln):
            size = mp if k == "main" else sp
            color = ACCENT if force_all_accent else _color_hex(c)
            tag = f"{{\\fs{size}\\c{color}}}"
            if not force_all_accent and _run_boost(c) and k == "main":
                bsize = round(size * ACCENT_BOOST)
                # крупнее белой (§1.4), но тонкая ТЁМНАЯ обводка, не заливка тем же
                # цветом — прежний bord6 своим же цветом "съедал" буквы, читалось
                # смазанным пятном, а не текстом (правка после отзыва о чёткости)
                tag = f"{{\\fs{bsize}\\c{color}\\bord3\\3c&H00101010&}}"
            elif not force_all_accent:
                tag = f"{{\\fs{size}\\c{color}\\bord4\\3c&H00101010&}}"
            sep = " " if i < len(ln) - 1 else ""
            parts.append(tag + t + sep)
        out.append((y + lh / 2, "".join(parts) + "{\\r}", lh))
        y += lh
    return out

def card_events(cards, style="Card"):
    """cards: [(start, end, [[(text, 'main'|'small', 'w'|'a'|'o'), ...], ...])]"""
    ev = []
    for st, en, lines in cards:
        assert en - st <= 4.01, f"карточка >4с: {lines} ({en-st:.2f}c)"
        mp, sp = _fit_and_layout(lines, MAIN_PX, SMALL_PX)
        blocks = _render_block(lines, mp, sp)
        for ycenter, text, _ in blocks:
            eff = ("{\\an5\\pos(%d,%d)\\fscx94\\fscy94\\t(0,320,0.6,\\fscx100\\fscy100)\\fad(140,90)}"
                   % (W // 2, int(ycenter)))
            ev.append((st, en, style, eff + text))
    return ev

def hook_events(hook):
    """hook: {'lines': [[str,...]], 'end': float} — целиком акцентным цветом."""
    lines = [[(ln, "main" if i == 0 else "small", "a")] for i, ln in enumerate(hook["lines"])]
    mp, sp = _fit_and_layout(lines, MAIN_PX, SMALL_PX, force_all_accent=True)
    blocks = _render_block(lines, mp, sp, force_all_accent=True)
    ev = []
    for ycenter, text, _ in blocks:
        eff = ("{\\an5\\pos(%d,%d)\\fscx94\\fscy94\\t(0,320,0.6,\\fscx100\\fscy100)\\fad(140,90)}"
               % (W // 2, int(ycenter)))
        ev.append((0.0, hook["end"], "Card", eff + text))
    return ev

def run_events(words, start_from=0.0, end_at=None):
    """Слой 2: одно слово за раз, непрерывно."""
    ev = []
    n = len(words)
    for j, w in enumerate(words):
        st = start_from if j == 0 else w["t"]
        en = words[j + 1]["t"] if j + 1 < n else (end_at or w["end"])
        if en - st < 0.10: en = st + 0.10
        ev.append((st, en, "Run", "{\\an5\\pos(%d,%d)}" % SLOT_RUN + w["w"]))
    return ev

def find_icon_windows(words, duration, pattern=r"тренаж", hold=3.0, fade=0.32):
    hits = [w["t"] for w in words if re.search(pattern, w["w"], re.I)]
    if not hits: return []
    wins = []
    for h in hits:
        a, b = h, min(h + hold, duration)
        if wins and a <= wins[-1][1]:
            wins[-1] = (wins[-1][0], max(wins[-1][1], b))
        else:
            wins.append((a, b))
    return wins

def build_ass(path, cards, hook, words, duration):
    lines = hook_events(hook) + card_events(cards) + run_events(words, end_at=duration)
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
    body = []
    for st, en, sty, txt in lines:
        layer = 0 if sty == "Run" else 1
        body.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{sty},,0,0,0,,{txt}")
    open(path, "w").write(head + "\n".join(body) + "\n")
    ncards = sum(1 for _,_,s,_ in lines if s=="Card")
    return ncards

def zoom_segments_filter(windows, duration, w0=2160, h0=3840, out_w=1080, out_h=1920,
                          zoom=1.14, attack=0.28, release=0.36):
    """Эмфасис-зум §2.9 через нарезку на сегменты (trim+concat) — гигантская суммарная
    формула по всем окнам оказалась непосильной для eval-парсера ffmpeg (зависает даже
    на 5с). Каждый зум-сегмент несёт свою короткую независимую формулу с локальным t0."""
    bounds = [0.0]
    kinds = []  # ('flat', ) | ('zoom', a, b)
    for a, b in windows:
        lo, hi = max(0.0, a - attack), min(duration, b + release)
        if lo > bounds[-1]:
            bounds.append(lo); kinds.append('flat')
        bounds.append(hi); kinds.append(('zoom', a, b))
    if duration > bounds[-1]:
        bounds.append(duration); kinds.append('flat')

    parts, labels = [], []
    for i, kind in enumerate(kinds):
        s, e = bounds[i], bounds[i + 1]
        lbl = f"z{i}"
        base = f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS"
        if kind == 'flat':
            parts.append(f"{base},scale={out_w}:{out_h}:flags=lanczos,setsar=1[{lbl}]")
        else:
            _, a, b = kind
            a0, b0 = round(a - s, 4), round(b - s, 4)  # локальное время внутри сегмента
            local_end = round(e - s, 4)
            # ВАЖНО: pow() падает с ошибкой инициализации, если он лежит на "каскадной"
            # else-ветке, куда попадает t=NaN (первый прогон конфигурации фильтра до
            # первого кадра) — все lt(NaN,x) ложны, значит любой безусловный "хвостовой"
            # else обязан быть pow-free константой; pow разрешён только под ЯВНЫМ
            # истинным lt(), которое NaN никогда не удовлетворяет.
            z = (
                f"(1+{zoom-1}*("
                f"if(lt(t,{a0}),(3*pow(t/{attack},2)-2*pow(t/{attack},3)),"
                f"if(lt(t,{b0}),1,"
                f"if(lt(t,{local_end}),1-(3*pow((t-{b0})/{release},2)-2*pow((t-{b0})/{release},3)),"
                f"1)))"
                f"))"
            )
            cw = f"trunc(({w0}/{z})/2)*2"
            ch = f"trunc(({h0}/{z})/2)*2"
            parts.append(
                f"{base},crop=w='{cw}':h='{ch}':x='(in_w-ow)/2':y='(in_h-oh)/2',"
                f"scale={out_w}:{out_h}:flags=lanczos,setsar=1[{lbl}]"
            )
        labels.append(lbl)
    concat_in = "".join(f"[{l}]" for l in labels)
    parts.append(f"{concat_in}concat=n={len(labels)}:v=1:a=0[base]")
    return ";\n".join(parts)
