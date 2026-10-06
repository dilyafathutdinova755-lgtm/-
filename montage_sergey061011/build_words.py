# -*- coding: utf-8 -*-
"""Собирает words{N}.json из asr{N}.json: токены sherpa-onnx, где токен с
ведущим пробелом отмечает начало нового слова."""
import json, sys

def build(asr_path, words_path):
    segs = json.load(open(asr_path))
    words = []
    for si, seg in enumerate(segs):
        toks, ts = seg['tokens'], seg['ts']
        # группируем токены в слова по ведущему пробелу
        cur = None
        wgroups = []
        for tok, t in zip(toks, ts):
            if tok.startswith(' ') or cur is None:
                cur = {'text': tok.strip(), 'ts': [t]}
                wgroups.append(cur)
            else:
                cur['text'] += tok
                cur['ts'].append(t)
        for wi, g in enumerate(wgroups):
            start = g['ts'][0]
            last = g['ts'][-1]
            if wi + 1 < len(wgroups):
                end = round(wgroups[wi + 1]['ts'][0] - 0.02, 3)
            else:
                end = round(min(last + 0.3, seg['end']), 3)
            words.append({'w': g['text'], 't': round(start, 3), 'end': end})
    json.dump(words, open(words_path, 'w'), ensure_ascii=False, indent=1)
    return words

if __name__ == '__main__':
    for idx in ['1', '2', '3']:
        w = build(f'asr{idx}.json', f'words{idx}.json')
        print(f'=== words{idx}.json: {len(w)} слов ===')
