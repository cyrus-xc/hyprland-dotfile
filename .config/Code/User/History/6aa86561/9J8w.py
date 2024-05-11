import os
import urllib.request
import sounddevice as sd
import torch
from speechbrain.lobes.models.FastSpeech2 import FastSpeech2

# Function to download the file if it doesn't exist
def download_if_not_exist(url, directory):
    filename = url.split('/')[-1]
    file_path = os.path.join(directory, filename)
    
    if not os.path.exists(file_path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"{filename} downloaded successfully.")
    else:
        print(f"{filename} already exists.")
        
# Function to generate audio using FastSpeech2
def generate_audio(text, model):
    with torch.no_grad():
        waveform, _ = model.encode_text(text)
    return waveform

# Directory to save the pretrained models
model_dir = "./pretrained_models/TTS_models"
os.makedirs(model_dir, exist_ok=True)

# Download FastSpeech2 pretrained model if not exists
fastspeech2_url = "https://drive.google.com/uc?export=download&id=1eRG23lQngmG68gh8Xhy_Nsh5ijie5bMd"
download_if_not_exist(fastspeech2_url, model_dir)

# Load FastSpeech2 model
fastspeech2 = FastSpeech2.from_hparams(source=model_dir)

# Text to be synthesized
text = "Hello, how are you?"

# Generate audio
with profiler.profile(record_shapes=True) as prof:
    with profiler.record_function("model_generation"):
        audio = generate_audio(text, fastspeech2)


# Play audio
print("Playing audio...")
sd.play(audio.squeeze().numpy(), fastspeech2.sample_rate)

# Wait for audio to finish playing
status = sd.wait()

print("Audio playback finished.")
