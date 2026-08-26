#!/usr/bin/env python3
import sys
import numpy as np
import sherpa_onnx
import soundfile as sf

MODEL_DIR = "./sherpa-onnx-streaming-t-one-russian-2025-09-08"


def create_recognizer():
    return sherpa_onnx.OnlineRecognizer.from_t_one_ctc(
        model=f"{MODEL_DIR}/model.onnx",
        tokens=f"{MODEL_DIR}/tokens.txt",
        debug=False,
    )


def main():
    wav_path = sys.argv[1]
    recognizer = create_recognizer()

    audio, sample_rate = sf.read(wav_path, dtype="float32", always_2d=True)
    audio = audio[:, 0]

    stream = recognizer.create_stream()
    left_paddings = np.zeros(int(0.3 * sample_rate), dtype=np.float32)
    stream.accept_waveform(sample_rate, left_paddings)
    stream.accept_waveform(sample_rate, audio)
    tail_paddings = np.zeros(int(0.66 * sample_rate), dtype=np.float32)
    stream.accept_waveform(sample_rate, tail_paddings)
    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    result = recognizer.get_result_all(stream)
    print("=== repr ===")
    print(repr(result))
    print("=== dir ===")
    print([a for a in dir(result) if not a.startswith("_")])
    print("=== text ===")
    print(getattr(result, "text", None))
    print("=== tokens ===")
    print(getattr(result, "tokens", None))
    print("=== timestamps ===")
    print(getattr(result, "timestamps", None))


if __name__ == "__main__":
    main()
