# AI Presentation Coach — NSP Project

## Title
AI-Powered Presentation Coach Using Deep Learning for Real-Time Public Speaking Analysis

## Current prototype
- Video upload
- Face visibility
- Eye-visibility proxy
- Camera framing/posture proxy
- Speech transcription when available
- Speaking pace
- Filler-word detection
- Presentation score
- Feedback
- Downloadable report

## Run on Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Important
This is a runnable baseline/prototype, not the final research-grade deep-learning model. For the final NSP version, the lightweight OpenCV proxies should be upgraded to a trained temporal model (LSTM/GRU/Transformer) with pose/face features and a labeled evaluation dataset. This makes the research contribution defensible.

Speech transcription may use Google's Web Speech service through SpeechRecognition and therefore can require internet access.
