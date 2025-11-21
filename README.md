# Multimodal Voice + Vision Chatbot (2025)

A completely **local**, **real-time**, **multimodal** AI assistant that hears you, sees through your webcam, thinks with Qwen2.5-VL, and speaks back with natural voice.

**No internet required after setup** · 100% private · Runs on your laptop

### Features
- Speech → Text (faster-whisper tiny)
- Live webcam capture
- Vision + Language understanding (Qwen2.5-VL-7B via Ollama)
- Natural text-to-speech (edge-tts + Microsoft Aria voice)
- 5-second voice questions → instant visual answers

### Demo Examples
- "How many fingers am I holding up?" → "You are holding up three fingers."
- "What color is my shirt?" → "You're wearing a blue t-shirt."
- "Describe my room" → Detailed description of everything visible

### Requirements
- Ollama installed → https://ollama.com
- Run once: `ollama pull qwen2.5vl:7b`

### Quick Start
```bash
git clone https://github.com/yourname/multimodal-chatbot.git
cd multimodal-chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py