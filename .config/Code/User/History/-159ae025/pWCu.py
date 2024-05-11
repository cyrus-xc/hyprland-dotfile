import time
import os
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import sounddevice as sd
import wavio
import numpy as np

models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/fastspeech2-en-ljspeech",
    arg_overrides={"vocoder": "hifigan", "fp16": False}
)
model = models[0]
TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
generator = task.build_generator([model], cfg)

text = "Hello, this is a test run."

# Measure the time taken for sample generation and prediction
start_time = time.time()
sample = TTSHubInterface.get_model_input(task, text)
wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)
end_time = time.time()

# Convert audio data to NumPy array and then to 16-bit integer type
wav_np = wav.numpy()
wav_int16 = (wav_np * (2**15 - 1)).astype(np.int16)

# Save audio to a WAV file
wavio.write("outputs/text-speech.wav", wav_int16, rate)

# Play audio using sounddevice
print("Playing audio...")
sd.play(wav_int16, rate)
sd.wait()
os.remove("outputs/text-speech.wav")

# Print the time taken for sample generation and prediction
print("Time taken for sample generation and prediction:", end_time - start_time, "seconds")
