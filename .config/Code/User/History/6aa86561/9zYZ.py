import torchaudio
from speechbrain.inference.TTS import FastSpeech2
from speechbrain.inference.vocoders import HIFIGAN
import torch.autograd.profiler as profiler
from scipy.io.wavfile import write as write_wav

# Initialize TTS (tacotron2) and Vocoder (HiFIGAN)
fastspeech2 = FastSpeech2.from_hparams(source="speechbrain/tts-fastspeech2-ljspeech", savedir="pretrained_models/tts-fastspeech2-ljspeech")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="pretrained_models/tts-hifigan-ljspeech")

# Run TTS with text input
input_text = "were the leaders in this luckless change; though our own Baskerville; who was at work some years before them; went much on the same lines;"
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
write_wav('example_TTS_input_text.wav', 22050, waveforms.squeeze(1))
