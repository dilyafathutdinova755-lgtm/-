#!/usr/bin/env python3
import json
import sys
import numpy as np
import sherpa_onnx
import soundfile as sf

MODEL_DIR = "./sherpa-onnx-streaming-t-one-russian-2025-09-08"
LEFT_PAD = 0.3


def main():
    wav_path = sys.argv[1]
    out_path = sys.argv[2]

    recognizer = sherpa_onnx.OnlineRecognizer.from_t_one_ctc(
        model=f"{MODEL_DIR}/model.onnx",
        tokens=f"{MODEL_DIR}/tokens.txt",
        debug=False,
    )

    audio, sample_rate = sf.read(wav_path, dtype="float32", always_2d=True)
    audio = audio[:, 0]

    stream = recognizer.create_stream()
    left_paddings = np.zeros(int(LEFT_PAD * sample_rate), dtype=np.float32)
    stream.accept_waveform(sample_rate, left_paddings)
    stream.accept_waveform(sample_rate, audio)
    tail_paddings = np.zeros(int(0.66 * sample_rate), dtype=np.float32)
    stream.accept_waveform(sample_rate, tail_paddings)
    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    result = recognizer.get_result_all(stream)
    tokens = result.tokens
    timestamps = [t - LEFT_PAD for t in result.timestamps]

    words = []
    cur = ""
    cur_start = None
    for tok, ts in zip(tokens, timestamps):
        if tok == " ":
            if cur:
                words.append({"text": cur, "start": round(cur_start, 3), "end": round(prev_ts, 3)})
                cur = ""
                cur_start = None
            continue
        if cur_start is None:
            cur_start = ts
        cur += tok
        prev_ts = ts
    if cur:
        words.append({"text": cur, "start": round(cur_start, 3), "end": round(prev_ts, 3)})

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print(f"{len(words)} words written to {out_path}")
    for w in words:
        print(f"{w['start']:6.2f} - {w['end']:6.2f}  {w['text']}")


if __name__ == "__main__":
    main()
