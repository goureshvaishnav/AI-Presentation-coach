import streamlit as st
from pathlib import Path
from utils.analysis import analyze_presentation
from utils.report import build_report

st.set_page_config(page_title="AI Presentation Coach", page_icon="🎤", layout="wide")
st.title("🎤 AI Presentation Coach")
st.caption("Upload a presentation video and get automated speaking, posture, eye-contact and filler-word feedback.")

with st.sidebar:
    st.header("Project")
    st.info("Lightweight NSP prototype designed to run locally on a modest laptop.")
    st.markdown("**Input:** MP4 / MOV / AVI / MKV")

uploaded = st.file_uploader("Upload your presentation video", type=["mp4","mov","avi","mkv"])

if uploaded:
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    video_path = upload_dir / uploaded.name
    video_path.write_bytes(uploaded.getbuffer())
    st.success(f"Video uploaded successfully: {video_path.name}")


    if st.button("🚀 Analyze Presentation", type="primary"):
        with st.spinner("Analyzing..."):
            try:
                st.session_state["result"] = analyze_presentation(str(video_path))
                st.session_state["video_name"] = uploaded.name
            except Exception as e:
                st.error(f"Analysis failed: {e}")

if "result" in st.session_state:
    r = st.session_state["result"]
    st.divider()
    st.subheader("📊 Presentation Report")

    cols = st.columns(5)
    for c, (label, value) in zip(cols, [
        ("Overall", r["scores"]["overall"]),
        ("Eye Contact", r["scores"]["eye_contact"]),
        ("Posture", r["scores"]["posture"]),
        ("Speech Pace", r["scores"]["pace"]),
        ("Engagement", r["scores"]["engagement"])
    ]):
        c.metric(label, f"{value:.0f}%")

    st.subheader("🗣️ Speech")
    a,b,c = st.columns(3)
    a.metric("Words", r["speech"]["word_count"])
    b.metric("WPM", r["speech"]["wpm"])
    c.metric("Filler Words", r["speech"]["filler_count"])
    st.write("**Detected fillers:**", ", ".join(r["speech"]["fillers"]) or "None detected")

    st.subheader("💡 Feedback")
    for item in r["feedback"]:
        st.write(f"- {item}")

    st.subheader("🔍 Technical Analysis")
    st.write(f"Frames analyzed: **{r['vision']['frames_analyzed']}**")
    st.write(f"Face visibility: **{r['vision']['face_visibility']:.1f}%**")
    st.write(f"Eye-contact proxy: **{r['vision']['eye_contact_proxy']:.1f}%**")
    st.write(f"Posture score: **{r['vision']['posture_score']:.1f}%**")

    st.download_button(
        "📄 Download Report",
        data=build_report(st.session_state["video_name"], r),
        file_name="presentation_report.txt",
        mime="text/plain"
    )
