from transformers import BarkModel, AutoProcessor
from scipy.io.wavfile import write as write_wav
import torch
import os
import sounddevice as sd
import torch.autograd.profiler as profiler


device = "cpu"
print(device)
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float32).to(device)


# Enable CPU offload for faster generation
model.enable_cpu_offload()

# Generate audio
# Multilingual speech - simplified Chinese
# inputs = processor("你好我会说中文，你今天吃了吗", voice_preset="zh_speaker_5")
# inputs = processor("Hello, my dog is cute")
# inputs = processor("♪ Hello, my dog is cute ♪") # Bark can also generate music.
inputs = processor("मैं NYU का छात्र हूं; मुझे कंप्यूटर विज्ञान पसंद है")

# Start profiling
# with profiler.profile(record_shapes=True) as prof:
#     with profiler.record_function("model_generation"):
audio_array = model.generate(**inputs)

# Print the profiler results
# print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))

audio_array = audio_array.cpu().numpy().squeeze()
# audio_array_from_audio = model.generate(**audio_inputs, tgt_lang="rus")[0].cpu().numpy().squeeze()

# # Play audio
sample_rate = model.generation_config.sample_rate
# sd.play(audio_array, sample_rate)
# status = sd.wait()

# Save audio to disk
output_path = "outputs/bark_generation.wav"
write_wav(output_path, sample_rate, audio_array)