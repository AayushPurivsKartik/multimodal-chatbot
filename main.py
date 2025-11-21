# main.py → FINAL MULTIMODAL CHATBOT (hears, sees, thinks, speaks!)
import ollama
from utils import capture_photo, record_for_5_seconds, transcribe_audio, speak_sync
import os

MODEL = "qwen2.5vl:7b"

print("="*60)
print(" MULTIMODAL VOICE+VISION CHATBOT READY")
print("   Speak your question → AI sees you → answers out loud")
print("="*60)

while True:
    try:
        print("\nGet ready... You have 5 seconds to speak!")
        input("Press Enter to start listening...")  # Optional: removes auto-start

        # 1. Record 5 seconds
        audio_file = record_for_5_seconds()
        user_text = transcribe_audio(audio_file)

        if not user_text.strip():
            print("No speech detected. Try again.")
            continue

        # 2. Capture what the AI sees
        photo_path = capture_photo("captures/query.jpg")

        # 3. Ask Qwen2.5-VL
        print("AI is thinking...")
        response = ollama.chat(
            model=MODEL,
            messages=[{
                'role': 'user',
                'content': f"User asked: \"{user_text}\"\nAnswer naturally and conversationally using what you see in the image.",
                'images': [photo_path]
            }]
        )
        answer = response['message']['content']

        # 4. Print + SPEAK the answer
        print("\nAI ANSWER:")
        print(answer)
        print("-"*60)

        speak_sync(answer)

        print("\nReady for next question...")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue