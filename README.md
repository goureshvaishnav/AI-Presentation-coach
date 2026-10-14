# 🎤 AI Presentation Coach

An AI-powered web application that analyzes presentation videos and provides feedback to help users improve their public speaking and presentation skills.

## 📌 About the Project

AI Presentation Coach helps users evaluate their presentation performance through video analysis. It provides estimated scores for eye contact, posture, speech pace, and engagement, along with suggestions for improvement.

The application is built using Python and Streamlit, with computer vision and speech recognition techniques.

## ✨ Features

- **Video Upload:** Upload presentation videos in supported formats.
- **Eye Contact Analysis:** Estimate eye visibility and camera-facing behavior.
- **Posture Analysis:** Evaluate approximate posture and camera framing.
- **Speech Pace Analysis:** Estimate speaking pace when speech transcription is available.
- **Filler Word Detection:** Identify common filler words when transcription succeeds.
- **Engagement Score:** Generate an approximate engagement indicator.
- **Feedback Report:** Display scores and personalized improvement suggestions.

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenCV
- SpeechRecognition
- MoviePy

## 📁 Project Structure

```text
AI-Presentation-coach/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   └── uploads/
│       └── .gitkeep
└── utils/
    ├── __init__.py
    ├── analysis.py
    └── report.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/goureshvaishnav/AI-Presentation-coach.git
cd AI-Presentation-coach
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to use the application.

## 🚀 How to Use

1. Launch the application.
2. Upload a presentation video.
3. Start the analysis.
4. Review the generated scores.
5. Read the feedback and suggestions to identify areas for improvement.

## ⚠️ Limitations

- Results depend on video quality, lighting, camera angle, and audio clarity.
- Speech pace and filler-word results depend on successful speech transcription.
- Eye-contact, posture, and engagement scores are approximate algorithmic estimates, not definitive measurements of presentation ability.
- Performance may vary depending on video length and available system memory.

## 🔮 Future Improvements

- Improve face and eye tracking accuracy.
- Add more robust speech-to-text processing.
- Provide timestamp-based feedback.
- Add presentation progress tracking.
- Improve performance on low-memory computers.

## 👨‍💻 Author

**Gouresh Vaishnav**

GitHub: [goureshvaishnav](https://github.com/goureshvaishnav)

## 🔗 Project Repository

[AI Presentation Coach](https://github.com/goureshvaishnav/AI-Presentation-coach)