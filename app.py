import streamlit as st
from PIL import Image

# FIX FOR ANTIALIAS ISSUE
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import VideoFileClip
import random
import os
import tempfile

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AttentionX AI", layout="wide")

st.title("🔥 AttentionX AI - Viral Intelligence Engine")
st.markdown("### Turn long videos into high-engagement viral shorts 🚀")

# =========================
# DATA
# =========================
hooks = [
    "This changed everything 😳",
    "Wait till the end 🔥",
    "Nobody expected this 😱",
    "This is insane 🤯",
    "You won’t believe this 👀"
]

captions = [
    "You NEED to see this 🔥",
    "This moment is unreal 😳",
    "POV: You didn’t expect this...",
    "Watch till end 👀",
    "This is going viral 🚀"
]

# =========================
# STATE CONTROL (IMPORTANT FIX)
# =========================
if "generated" not in st.session_state:
    st.session_state.generated = False

# =========================
# VIRALITY SCORE
# =========================
def virality_score(duration, randomness):
    score = (10 - abs(duration - 12)) * 6 + randomness * 10
    return round(max(0, min(score, 100)), 2)

# =========================
# LOAD VIDEO
# =========================
def load_video(path):
    try:
        return VideoFileClip(path)
    except Exception as e:
        st.error(f"Video load error: {e}")
        return None

# =========================
# GENERATE CLIP
# =========================
def generate_clip(clip, start, duration, output_path):
    try:
        subclip = clip.subclip(start, start + duration)
        subclip = subclip.resize(height=480)
        subclip.write_videofile(output_path, logger=None, audio=False)
        return output_path
    except Exception as e:
        st.error(f"Clip generation failed: {e}")
        return None

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

if uploaded_file:

    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, "input.mp4")

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(input_path)
    st.success("Upload successful!")

    clip = load_video(input_path)

    if clip:

        max_duration = int(clip.duration)

        st.subheader("🧠 AI Video Intelligence Report")
        st.info(f"""
        Duration: {clip.duration:.2f}s  
        FPS: {clip.fps}  
        Resolution: {clip.size}  
        """)

        duration = st.slider("Clip Length (seconds)", 5, 30, 10)

        # RESET BUTTON (IMPORTANT)
        if st.button("🔄 Reset"):
            st.session_state.generated = False

        # GENERATE BUTTON (ONLY ONCE)
        if st.button("🚀 Generate Viral Clips") and not st.session_state.generated:

            progress = st.progress(0)
            results = []

            with st.spinner("AI analyzing viral moments..."):

                for i in range(3):  # reduced for clean UI

                    if max_duration > duration:
                        start = random.randint(0, max_duration - duration)
                    else:
                        start = 0

                    randomness = random.randint(1, 10)
                    score = virality_score(duration, randomness)

                    output_path = os.path.join(temp_dir, f"clip_{i}.mp4")

                    result = generate_clip(clip, start, duration, output_path)

                    if result is not None:
                        results.append({
                            "file": result,
                            "score": score
                        })

                    progress.progress((i + 1) * 33)

            progress.progress(100)
            st.success("AI analysis complete!")

            # STORE RESULTS IN SESSION
            st.session_state.results = results
            st.session_state.generated = True

        # =========================
        # SHOW RESULTS ONLY IF GENERATED
        # =========================
        if st.session_state.generated:

            results = st.session_state.results

            if len(results) > 0:

                results.sort(key=lambda x: x["score"], reverse=True)
                best = results[0]

                st.subheader("🏆 Best Viral Clip")
                st.video(best["file"])
                st.metric("Virality Score", best["score"])

                st.success("🔥 Caption: " + random.choice(captions))
                st.info("Hook: " + random.choice(hooks))

                st.subheader("🎬 All Clips")

                for r in results:
                    st.video(r["file"])
                    st.write(f"⭐ Score: {r['score']}")

                avg_score = sum(r["score"] for r in results) / len(results)

                st.subheader("📊 AI Analytics Dashboard")
                st.success(f"Average Score: {round(avg_score, 2)}")

                if avg_score >= 70:
                    st.balloons()
                    st.info("🔥 HIGH VIRAL POTENTIAL")
                else:
                    st.warning("⚠ Medium engagement")

        try:
            clip.close()
        except:
            pass
