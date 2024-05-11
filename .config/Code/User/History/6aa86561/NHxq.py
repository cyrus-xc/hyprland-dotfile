import torchaudio
from speechbrain.inference.TTS import FastSpeech2
from speechbrain.inference.vocoders import HIFIGAN
import torch.autograd.profiler as profiler

# Initialize TTS (tacotron2) and Vocoder (HiFIGAN)
fastspeech2 = FastSpeech2.from_hparams(source="speechbrain/tts-fastspeech2-ljspeech", savedir="pretrained_models/tts-fastspeech2-ljspeech")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="pretrained_models/tts-hifigan-ljspeech")

# Run TTS with text input
input_text = "嗨我是一名纽约大学的学生我爱计算机科学;"
mel_output, durations, pitch, energy = fastspeech2.encode_text(
    [input_text],
    pace=1.0,        # scale up/down the speed
    pitch_rate=1.0,  # scale up/down the pitch
    energy_rate=1.0, # scale up/down the energy
)

# Start profiling
with profiler.profile(record_shapes=True) as prof:
    with profiler.record_function("model_generation"):
        # Running Vocoder (spectrogram-to-waveform)
        waveforms = hifi_gan.decode_batch(mel_output)

# Print the profiler results
print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))

# Save the waveform using scipy
torchaudio.save('example_TTS_input_phoneme.wav', waveforms.squeeze(1), 22050)
