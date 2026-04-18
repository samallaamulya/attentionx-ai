import streamlit as st
from moviepy.editor import VideoFileClip
import random
import os
import tempfile

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AttentionX AI", layout="wide")

st.title("🔥 AttentionX AI - Viral Intelligence Engine")
st.markdown("### Turn long videos into high-engagement viral shorts using AI-style analysis 🚀")

# =========================
# VIRAL HOOKS
# =========================
hooks = [
    "This changed everything 😳",
    "Wait till the end 🔥",
    "Nobody expected this 😱",
    "This is insane 🤯",
    "You won’t believe this 👀"
]

# =========================
# VIRAL CAPTION GENERATOR
# =========================
def generate_caption():
    templates = [
        "You NEED to see this 🔥",
        "This moment is unreal 😳",
        "POV: You didn’t expect this...",
        "Watch till end 👀",
        "This is going viral for a reason 🚀"
    ]
    return random.choice(templates)

# =========================
# VIRALITY SCORING ENGINE (AI SIMULATION)
# =========================
def virality_score(duration, randomness):
    # optimized heuristic model
    score = (10 - abs(duration - 12)) * 6 + randomness * 10
    return round(min(max(score, 0), 100), 2)

# =========================
# SAFE VIDEO LOADER
# =========================
def load_video(path):
    try:
        return VideoFileClip(path)
    except Exception as e:
        st.error(f"Video load error: {e}")
        return None

# =========================
# CLIP GENERATION ENGINE
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

        # =========================
        # AI INSIGHTS PANEL
        # =========================
        st.subheader("🧠 AI Video Intelligence Report")

        st.info(f"""
        Duration: {clip.duration:.2f}s  
        FPS: {clip.fps}  
        Resolution: {clip.size}  
        """)

        # =========================
        # SETTINGS
        # =========================
        st.subheader("🎯 AI Clip Settings")

        duration = st.slider("Clip Length", 5, 30, 10)

        # =========================
        # GENERATE
        # =========================
        if st.button("🚀 Generate Viral Intelligence Clips"):

            progress = st.progress(0)
            results = []

            with st.spinner("AI analyzing viral moments..."):

                for i in range(5):  # MORE CLIPS = better evaluation

                    start = random.randint(0, max_duration - duration)
                    randomness = random.randint(1, 10)

                    score = virality_score(duration, randomness)

                    output_path = os.path.join(temp_dir, f"clip_{i}.mp4")

                    result = generate_clip(clip, start, duration, output_path)

                    if result:
                        results.append({
                            "file": result,
                            "score": score
                        })

                    progress.progress((i + 1) * 20)

            progress.progress(100)
            st.success("AI analysis complete!")

            # =========================
            # SORT BY VIRALITY
            # =========================
            results.sort(key=lambda x: x["score"], reverse=True)

            best = results[0] if results else None

            # =========================
            # BEST CLIP HIGHLIGHT
            # =========================
            if best:
                st.subheader("🏆 Best Viral Clip (AI Selected)")
                st.video(best["file"])
                st.metric("Virality Score", best["score"])

                st.success("🔥 Suggested Caption: " + generate_caption())
                st.info("Hook: " + random.choice(hooks))

                with open(best["file"], "rb") as f:
                    st.download_button(
                        "⬇ Download Best Clip",
                        f,
                        file_name="best_clip.mp4",
                        mime="video/mp4"
                    )

            # =========================
            # ALL CLIPS
            # =========================
            st.subheader("🎬 All Generated Clips Ranked")

            for r in results:
                st.video(r["file"])
                st.write(f"⭐ Virality Score: {r['score']}")

                with open(r["file"], "rb") as f:
                    st.download_button(
                        "Download",
                        f,
                        file_name=os.path.basename(r["file"]),
                        mime="video/mp4"
                    )

            # =========================
            # FINAL DASHBOARD
            # =========================
            avg_score = sum(r["score"] for r in results) / len(results)

            st.subheader("📊 AI Analytics Dashboard")

            st.success(f"Average Virality Score: {round(avg_score, 2)}")

            if avg_score > 70:
                st.balloons()
                st.info("🔥 HIGH VIRAL POTENTIAL VIDEO DETECTED")
            else:
                st.warning("⚠ Moderate engagement potential")

        clip.close()