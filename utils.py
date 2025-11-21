# utils.py
import cv2
import time
import os

def capture_photo(save_path="captures/current.jpg"):
    """
    Opens webcam, shows live feed, press SPACE or wait 2 sec to capture,
    then press ESC or close window to continue.
    """
    os.makedirs("captures", exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open webcam! Check camera connection.")

    print("Webcam opened – look at camera – photo in 2 seconds...")
    time.sleep(2)  # Give you time to pose

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(save_path, frame)
        print(f"Photo saved → {save_path}")
        
        # Optional: show the captured image for 1 sec
        cv2.imshow("Captured – sending to AI...", frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    else:
        raise Exception("Failed to grab frame")
    
    cap.release()
    return save_path


# utils.py - add this at the bottom
from faster_whisper import WhisperModel
import pyaudio
import wave
import threading
import time
import torch

# Load model once (tiny is fast & accurate enough for trigger + full sentences)
# whisper_model = WhisperModel("tiny", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16")
import torch

# Load model once — smart device & compute_type selection
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"   # ← int8 is fastest on CPU

print(f"Loading Whisper 'tiny' model on {device} with {compute_type}... (first run takes ~10 sec)")
whisper_model = WhisperModel("tiny", device=device, compute_type=compute_type)

def record_for_5_seconds(filename="sounds/input.wav"):
    """
    Records exactly 5 seconds from microphone.
    """
    os.makedirs("sounds", exist_ok=True)
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Recording... Speak now! (5 seconds)")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    print("Recording done. Transcribing...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def transcribe_audio(audio_path="sounds/input.wav"):
    segments, info = whisper_model.transcribe(audio_path, beam_size=5, language="en", vad_filter=True)
    text = " ".join(seg.text for seg in segments).strip()
    print(f"You said: {text}")
    return text


import asyncio
import edge_tts
import tempfile
import os
from playsound import playsound  # pip install playsound==1.3.0 (1.3.0 works on Windows)

async def speak_text(text: str, voice="en-US-AriaNeural"):
    """
    Converts text to speech and plays it with natural voice
    """
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(tmp_path)

    print("AI is speaking...")
    playsound(tmp_path)  # Blocks until finished
    os.unlink(tmp_path)   # Delete temp file

# Synchronous wrapper so we can call from main.py
def speak_sync(text: str):
    asyncio.run(speak_text(text))