import time
import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from speechbrain.inference.interfaces import foreign_class

# Function to transcribe audio
def transcribe_audio(file_path, asr_model):
    transcribed_text = asr_model.transcribe_file(file_path)
    return transcribed_text

# Parameters for recording
fs = 44100  # Sample rate
seconds = 5  # Duration of recording in seconds
file_path = 'outputs/hindi_input.wav'

# Load ASR model
asr_model = foreign_class(source="speechbrain/asr-wav2vec2-ctc-aishell",  pymodule_file="custom_interface.py", classname="CustomEncoderDecoderASR")

# Loop for continuous recording and transcription
while True:
    # Beep at the start of recording
    print("Beep!")
    sd.play(0.1 * np.sin(2 * np.pi * 1000 * np.arange(0.1 * fs) / fs), samplerate=fs, blocking=True)
    
    # # Recording
    # print("Recording...")
    # recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    # sd.wait()  # Wait until recording is finished
    # write(file_path, fs, recording)
    
    # Transcription
    print("Transcribing...")
    start_time = time.time()
    transcribed_text = transcribe_audio(file_path, asr_model)
    end_time = time.time()
    print("Transcription:", transcribed_text)
    
    # Remove the file
    os.remove(file_path)
    
    # Print the time taken for sample generation and prediction
    print("Time taken for sample generation and prediction:", end_time - start_time, "seconds")
	
	# Wait for a while before starting the next recording
    time.sleep(1)  # adjust the duration of sleep if needed
    break
