def build_report(video_name, r):
    lines = [
        "AI PRESENTATION COACH - PRESENTATION REPORT",
        "="*55, f"Video: {video_name}", f"Duration: {r['duration_seconds']} seconds", "",
        "SCORES", "-"*55,
        f"Overall: {r['scores']['overall']:.1f}%",
        f"Eye Contact: {r['scores']['eye_contact']:.1f}%",
        f"Posture: {r['scores']['posture']:.1f}%",
        f"Speech Pace: {r['scores']['pace']:.1f}%",
        f"Engagement: {r['scores']['engagement']:.1f}%", "",
        "SPEECH", "-"*55,
        f"Words: {r['speech']['word_count']}",
        f"Words/minute: {r['speech']['wpm']}",
        f"Filler count: {r['speech']['filler_count']}",
        f"Fillers: {', '.join(r['speech']['fillers']) or 'None'}", "",
        "FEEDBACK", "-"*55
    ]
    lines += [f"- {x}" for x in r["feedback"]]
    lines += ["", "NOTE", "-"*55,
              "Eye-contact and posture values are computer-vision proxies, not psychological or clinical assessments."]
    return "\n".join(lines)
