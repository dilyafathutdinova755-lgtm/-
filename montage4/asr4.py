import sherpa_onnx, wave, numpy as np, json
m='sherpa-onnx-zipformer-ru-2024-09-18'
rec=sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f'{m}/encoder.int8.onnx', decoder=f'{m}/decoder.onnx',
    joiner=f'{m}/joiner.int8.onnx', tokens=f'{m}/tokens.txt',
    num_threads=4, sample_rate=16000, feature_dim=80, decoding_method='greedy_search')
vc=sherpa_onnx.VadModelConfig()
vc.silero_vad.model='silero_vad.onnx'; vc.silero_vad.threshold=0.5
vc.silero_vad.min_silence_duration=0.12; vc.silero_vad.min_speech_duration=0.10
vc.silero_vad.max_speech_duration=8.0; vc.sample_rate=16000
vad=sherpa_onnx.VoiceActivityDetector(vc, buffer_size_in_seconds=60)
w=wave.open('audio16k_4.wav'); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
win=512; segs=[]
for i in range(0,len(a),win):
    vad.accept_waveform(a[i:i+win])
    while not vad.empty():
        segs.append((vad.front.start/16000, vad.front.samples)); vad.pop()
vad.flush()
while not vad.empty():
    segs.append((vad.front.start/16000, vad.front.samples)); vad.pop()
out=[]
for st,samples in segs:
    s=rec.create_stream(); s.accept_waveform(16000, np.array(samples,dtype=np.float32)); rec.decode_stream(s)
    r=s.result; dur=len(samples)/16000
    out.append({'start':round(st,3),'end':round(st+dur,3),'text':r.text})
    print(f'[{st:6.2f} - {st+dur:6.2f}] {r.text}')
json.dump(out, open('asr4.json','w'), ensure_ascii=False, indent=1)
