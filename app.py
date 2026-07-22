import streamlit as st
import os
import requests
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
from streamlit_lottie import st_lottie

from summarizer import summarize_text
from quiz_generator import build_questions


@st.cache_data(show_spinner=False)
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


# -----------------------------
# Streamlit Page
# -----------------------------
st.set_page_config(
    page_title="AI Video Summarizer",
    page_icon="🎥",
    layout="centered"
)

# -----------------------------
# Custom CSS: aurora background + light cards with dark text
# -----------------------------
st.markdown("""
<style>
/* ---------- AURORA BACKGROUND ---------- */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background:
        radial-gradient(1200px 600px at 10% -10%, rgba(59,130,246,0.35), transparent 60%),
        radial-gradient(900px 500px at 110% 10%, rgba(168,85,247,0.30), transparent 60%),
        radial-gradient(800px 600px at 50% 120%, rgba(16,185,129,0.25), transparent 60%),
        linear-gradient(-45deg, #05060f, #0a0f1f, #0d0b2a, #0b1a2b) !important;
    background-size: 100% 100%, 100% 100%, 100% 100%, 400% 400% !important;
    animation: auroraShift 18s ease infinite;
    position: relative;
}

/* Transparent header so it blends with the aurora background instead of a black bar */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Shrink the uploaded video preview */
video {
    max-width: 480px !important;
    max-height: 270px !important;
    width: 100% !important;
    border-radius: 12px;
    display: block;
    margin: 0 auto;
}
@keyframes auroraShift {
    0%   { background-position: 0% 0%, 100% 0%, 50% 100%, 0% 50%; }
    50%  { background-position: 20% 10%, 80% 20%, 60% 90%, 100% 50%; }
    100% { background-position: 0% 0%, 100% 0%, 50% 100%, 0% 50%; }
}

/* Twinkling star particles */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.7), transparent 60%),
        radial-gradient(1px 1px at 70% 80%, rgba(255,255,255,0.5), transparent 60%),
        radial-gradient(1.5px 1.5px at 40% 60%, rgba(147,197,253,0.7), transparent 60%),
        radial-gradient(1px 1px at 85% 25%, rgba(196,181,253,0.6), transparent 60%),
        radial-gradient(1px 1px at 15% 85%, rgba(110,231,183,0.6), transparent 60%);
    animation: twinkle 6s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes twinkle {
    from { opacity: 0.4; }
    to   { opacity: 1; }
}

/* Floating glow orbs */
.bg-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.5;
    pointer-events: none;
    z-index: 0;
}
.bg-orb.one   { width: 380px; height: 380px; background: #3B82F6; top: 8%;  left: -80px;  animation: floatA 14s ease-in-out infinite; }
.bg-orb.two   { width: 320px; height: 320px; background: #A855F7; top: 55%; right: -60px; animation: floatB 17s ease-in-out infinite; }
.bg-orb.three { width: 280px; height: 280px; background: #10B981; bottom: -80px; left: 30%; animation: floatA 20s ease-in-out infinite reverse; }
@keyframes floatA {
    0%,100% { transform: translate(0,0) scale(1); }
    50%     { transform: translate(60px,-40px) scale(1.15); }
}
@keyframes floatB {
    0%,100% { transform: translate(0,0) scale(1); }
    50%     { transform: translate(-70px,50px) scale(1.1); }
}

.block-container, header, [data-testid="stToolbar"] { position: relative; z-index: 1; }
.block-container {
    padding-top: 2rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

/* ---------- LIGHT GLASS CARDS WITH DARK TEXT ---------- */
.stat-card, .content-card, .quiz-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(18px) saturate(140%);
    -webkit-backdrop-filter: blur(18px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    color: #0F172A;
    line-height: 1.6;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    animation: fadeInUp 0.45s ease-out both;
}
.stat-card { text-align: center; padding: 1rem 1.25rem; }
.stat-card:hover { transform: translateY(-3px); transition: transform 0.2s ease; }
.stat-label { font-size: 13px; color: #475569; margin-bottom: 4px; }
.stat-value { font-size: 24px; font-weight: 700; color: #0F172A; }
.quiz-card { margin-bottom: 1rem; color: #0F172A; }
.quiz-progress { font-size: 12px; color: #64748B; margin-bottom: 4px; }
.quiz-card strong { color: #0F172A; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---------- HERO (stays dark bg, light text — needed for contrast against aurora) ---------- */
.hero-wrap {
    position: relative;
    overflow: hidden;
    border-radius: 18px;
    padding: 3rem 2rem 2.5rem;
    background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(168,85,247,0.12));
    border: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 10px 40px rgba(59,130,246,0.15);
}
.hero-title { position: relative; z-index: 1; font-size: 28px; font-weight: 700; margin: 0 0 8px; color: #FFFFFF; animation: fadeInUp 0.5s ease-out both; }
.hero-sub   { position: relative; z-index: 1; font-size: 14px; color: #E2E8F0; margin: 0; animation: fadeInUp 0.5s ease-out 0.1s both; }

/* ---------- BUTTONS ---------- */
div.stButton > button, div.stFormSubmitButton > button, div.stDownloadButton > button {
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    color: #FFFFFF;
    border: none;
    font-weight: 600;
    border-radius: 10px;
    transition: transform 0.15s ease, box-shadow 0.2s ease, filter 0.2s ease;
    box-shadow: 0 4px 14px rgba(59,130,246,0.35);
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover, div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(139,92,246,0.5);
    filter: brightness(1.08);
    color: #FFFFFF;
}

/* Radio rows inside the (now light) quiz cards need dark text too */
div[role="radiogroup"] label {
    transition: background 0.15s ease;
    border-radius: 8px;
    color: #0F172A !important;
}
div[role="radiogroup"] label:hover { background: rgba(15,23,42,0.06); }

/* Uploader */
section[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.08);
    border: 1.5px dashed rgba(147,197,253,0.45);
    border-radius: 12px;
    transition: border-color 0.2s ease, background 0.2s ease;
}
section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(168,85,247,0.7);
    background: rgba(255,255,255,0.12);
}
</style>

<div class="bg-orb one"></div>
<div class="bg-orb two"></div>
<div class="bg-orb three"></div>
""", unsafe_allow_html=True)

# -----------------------------
# Folders
# -----------------------------
folders = ["uploads", "audio", "transcript"]
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)


@st.cache_resource(show_spinner=False)
def load_whisper_model():
    return WhisperModel("tiny", device="cpu", compute_type="int8")


def format_duration(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s" if minutes else f"{secs}s"


# -----------------------------
# Session state
# -----------------------------
for key in ["page", "transcript", "summary", "quiz", "duration_str", "word_count", "quiz_score"]:
    if key not in st.session_state:
        st.session_state[key] = "upload" if key == "page" else None


def go_to_upload_page():
    for key in ["page", "transcript", "summary", "quiz", "duration_str", "word_count", "quiz_score"]:
        st.session_state[key] = "upload" if key == "page" else None


def render_footer():
    st.markdown("""
    <hr style="border-color: rgba(255,255,255,0.15);">
    <div style="text-align:center; color:#E2E8F0; font-size:13px;">
        <p><strong>Developed by Amulya</strong></p>
        <p>AI Video Summarization &amp; Quiz Generation</p>
        <p>Python | Streamlit | Whisper | NLP</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PAGE 1: UPLOAD
# =========================================================
if st.session_state["page"] == "upload":

    st.markdown("""
    <div class="hero-wrap">
        <h1 class="hero-title">🎥 AI Video Intelligence System</h1>
        <p class="hero-sub">Transform videos into smart summaries and interactive quizzes — runs fully offline</p>
    </div>
    """, unsafe_allow_html=True)

    lottie_ai = load_lottie("https://assets4.lottiefiles.com/packages/lf20_qp1q7mct.json")
    if lottie_ai:
        st_lottie(lottie_ai, height=200, key="lottie_intro")

    uploaded_video = st.file_uploader(
        "Upload your video",
        type=["mp4", "avi", "mov", "mkv"]
    )

    if uploaded_video is not None:
        video_path = os.path.join("uploads", uploaded_video.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        st.video(video_path)

        if st.button("🚀 Generate Summary & Quiz", use_container_width=True):

            progress = st.progress(0, text="Extracting audio...")

            audio_path = os.path.join(
                "audio", os.path.splitext(uploaded_video.name)[0] + ".mp3"
            )
            video = VideoFileClip(video_path)
            duration_seconds = video.duration
            video.audio.write_audiofile(audio_path)
            st.session_state["duration_str"] = format_duration(duration_seconds)
            progress.progress(25, text="Generating transcript...")

            model = load_whisper_model()
            segments, info = model.transcribe(audio_path)
            transcript = " ".join(segment.text for segment in segments).strip()
            progress.progress(60, text="Generating summary...")

            transcript_path = os.path.join(
                "transcript", os.path.splitext(uploaded_video.name)[0] + ".txt"
            )
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript)

            st.session_state["transcript"] = transcript
            st.session_state["word_count"] = len(transcript.split())

            st.session_state["summary"] = summarize_text(transcript)
            progress.progress(85, text="Creating quiz...")

            st.session_state["quiz"] = build_questions(transcript, num_questions=5)
            progress.progress(100, text="Done!")

            st.session_state["page"] = "results"
            st.balloons()
            st.rerun()

    render_footer()


# =========================================================
# PAGE 2: RESULTS
# =========================================================
elif st.session_state["page"] == "results":

    st.markdown("""
    <div class="hero-wrap">
        <h1 class="hero-title">✅ Your video is ready</h1>
        <p class="hero-sub">Transcript, summary and quiz generated successfully</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅ Upload another video"):
        go_to_upload_page()
        st.rerun()

    score_display = st.session_state["quiz_score"] or "—"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">⏱ Duration</div>
            <div class="stat-value">{st.session_state['duration_str'] or '—'}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📄 Word count</div>
            <div class="stat-value">{st.session_state['word_count'] or '—'}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🎯 Quiz score</div>
            <div class="stat-value">{score_display}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    tab1, tab2, tab3 = st.tabs(["📝 Transcript", "📌 Summary", "❓ Quiz"])

    with tab1:
        st.markdown(f'<div class="content-card">{st.session_state["transcript"]}</div>', unsafe_allow_html=True)
        st.download_button(
            "📄 Download Transcript",
            st.session_state["transcript"],
            file_name="Transcript.txt"
        )

    with tab2:
        if st.session_state["summary"]:
            st.markdown(f'<div class="content-card">{st.session_state["summary"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "📑 Download Summary",
                st.session_state["summary"],
                file_name="Summary.txt"
            )
        else:
            st.info("Summary will appear here once generated.")

    with tab3:
        quiz = st.session_state["quiz"]

        if quiz is None:
            st.info("Quiz not generated yet.")
        elif len(quiz) == 0:
            st.warning(
                "⚠️ Couldn't generate quiz questions from this video — the transcript is too short "
                "or doesn't have enough distinct topics/names/numbers to build fair multiple-choice options. "
                "Try a longer video (1-2+ minutes) with more spoken content."
            )
        else:
            user_answers = {}

            with st.form("quiz_form"):
                for i, q in enumerate(quiz):
                    st.markdown(f"""
                    <div class="quiz-card">
                        <div class="quiz-progress">Question {i + 1} of {len(quiz)}</div>
                        <div><strong>{q['question']}</strong></div>
                    </div>
                    """, unsafe_allow_html=True)
                    user_answers[i] = st.radio(
                        label=f"Select your answer for Q{i + 1}",
                        options=q["options"],
                        key=f"quiz_q_{i}",
                        label_visibility="collapsed"
                    )

                submitted = st.form_submit_button("✅ Submit Quiz", use_container_width=True)

            if submitted:
                score = 0
                for i, q in enumerate(quiz):
                    if user_answers[i] == q["answer"]:
                        score += 1

                st.session_state["quiz_score"] = f"{score}/{len(quiz)}"
                st.success(f"🎯 You scored {score} / {len(quiz)}")
                st.snow()

                with st.expander("See correct answers"):
                    for i, q in enumerate(quiz):
                        is_correct = user_answers[i] == q["answer"]
                        icon = "✅" if is_correct else "❌"
                        st.write(f"{icon} Q{i + 1}: Correct answer — **{q['answer']}**")

                st.rerun()

    render_footer()