import sherpa_onnx, wave, numpy as np, sys
M='/home/user/-/work/sherpa-onnx-zipformer-ru-2024-09-18'
rec=sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f'{M}/encoder.int8.onnx', decoder=f'{M}/decoder.onnx',
    joiner=f'{M}/joiner.int8.onnx', tokens=f'{M}/tokens.txt',
    num_threads=4, sample_rate=16000, feature_dim=80, decoding_method='greedy_search')

def redecode(wavfile, start, end):
    w = wave.open(wavfile)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    sr = w.getframerate()
    seg = a[int(start*sr):int(end*sr)]
    s = rec.create_stream()
    s.accept_waveform(sr, seg)
    rec.decode_stream(s)
    r = s.result
    for tok, ts in zip(r.tokens, r.timestamps):
        print(f'{start+ts:7.3f}  {tok!r}')
    print('TEXT:', r.text)

if __name__ == '__main__':
    wavfile, s, e = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    redecode(wavfile, s, e)
