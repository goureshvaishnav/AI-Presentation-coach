from pathlib import Path
import re, tempfile
import cv2
import numpy as np

FILLERS = ["um","uh","umm","uhh","like","actually","basically","you know","i mean","so","right"]

def _transcribe(video_path):
    try:
        import speech_recognition as sr
        from moviepy.editor import VideoFileClip
        with tempfile.TemporaryDirectory() as td:
            audio_path = str(Path(td) / "audio.wav")
            clip = VideoFileClip(video_path)
            if clip.audio is None:
                return ""
            clip.audio.write_audiofile(audio_path, logger=None)
            rec = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = rec.record(source)
            try:
                return rec.recognize_google(audio)
            except Exception:
                return ""
    except Exception:
        return ""

def _speech_metrics(transcript, duration):
    text = transcript.lower()
    words = re.findall(r"\b[\w']+\b", text)
    found = []
    for filler in FILLERS:
        found += [filler] * len(re.findall(r"\b" + re.escape(filler) + r"\b", text))
    wpm = len(words) / max(duration / 60, 1e-6)
    return {"transcript": transcript, "word_count": len(words),
            "wpm": round(wpm,1), "filler_count": len(found), "fillers": found[:50]}

def analyze_presentation(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open the video.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total / fps if total else 0

    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    step = max(1, int(fps * 0.5))
    analyzed = faces = eye_visible = 0
    posture_scores, eye_scores = [], []

    while True:
        ok, frame = cap.read()
        if not ok: break
        current = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if current % step: continue

        analyzed += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found = face_detector.detectMultiScale(gray, 1.1, 5, minSize=(60,60))

        if len(found):
            faces += 1
            x,y,w,h = max(found, key=lambda a:a[2]*a[3])
            roi = gray[y:y+h, x:x+w]
            eyes = eye_detector.detectMultiScale(roi, 1.1, 5, minSize=(15,15))
            if len(eyes): eye_visible += 1

            cx = (x+w/2) / max(frame.shape[1],1)
            center_score = max(0, 1-abs(cx-.5)*1.5)
            size_score = min(1, max(0, (w/max(frame.shape[1],1))/0.25))
            posture_scores.append(100*(.65*center_score+.35*size_score))
            eye_scores.append(100 if len(eyes) else 45)

    cap.release()

    face_visibility = 100*faces/max(analyzed,1)
    eye_proxy = 100*eye_visible/max(faces,1)
    posture = float(np.mean(posture_scores)) if posture_scores else 0

    transcript = _transcribe(video_path)
    speech = _speech_metrics(transcript, duration)

    if speech["word_count"] == 0:
        pace = 50
    else:
        pace = max(0, 100-abs(speech["wpm"]-135)*.9)

    engagement = min(100, .55*eye_proxy+.45*posture)
    overall = .30*eye_proxy+.25*posture+.20*pace+.25*engagement

    feedback = []
    if face_visibility < 70: feedback.append("Keep your face clearly visible and stay centered in the camera frame.")
    if eye_proxy < 60: feedback.append("Improve eye contact with the camera/audience.")
    if posture < 65: feedback.append("Maintain a more stable, centered posture.")
    if speech["word_count"] and speech["wpm"] > 160: feedback.append("Your speaking pace is fast; slow down and add short pauses.")
    elif speech["word_count"] and speech["wpm"] < 100: feedback.append("Your speaking pace is slow; maintain a steady rhythm.")
    if speech["filler_count"] > 8: feedback.append("Reduce filler words by replacing them with intentional pauses.")
    if not feedback: feedback.append("Good baseline performance. Practice consistently and improve one metric at a time.")

    return {
        "duration_seconds": round(duration,1),
        "scores": {"overall": max(0,min(100,overall)), "eye_contact": max(0,min(100,eye_proxy)),
                   "posture": max(0,min(100,posture)), "pace": max(0,min(100,pace)),
                   "engagement": max(0,min(100,engagement))},
        "speech": speech,
        "vision": {"frames_analyzed": analyzed, "face_visibility": face_visibility,
                   "eye_contact_proxy": eye_proxy, "posture_score": posture},
        "feedback": feedback
    }
