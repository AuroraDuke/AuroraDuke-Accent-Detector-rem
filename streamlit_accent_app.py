import os
import subprocess
import tempfile
import csv
import torch
import torchaudio
import streamlit as st
from speechbrain.pretrained.interfaces import foreign_class

# Load model
classifier = foreign_class(
    source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier"
)

# Extract audio
def extract_audio_ffmpeg(video_path, audio_output):
    command = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_output]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_output

# Split audio
def split_audio_ffmpeg(audio_path, chunk_length_sec, temp_dir):
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]).decode().strip())

    chunks = []
    for i in range(0, int(duration), chunk_length_sec):
        output_chunk = os.path.join(temp_dir, f"chunk_{i}.wav")
        command = ["ffmpeg", "-y", "-i", audio_path, "-ss", str(i), "-t", str(chunk_length_sec), output_chunk]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunks.append((i, output_chunk))
    return chunks

# Classify audio
def classify_accent(audio_path):
    try:
        out_prob, score, index, label = classifier.classify_file(audio_path)
        return label[0], score.item() * 100
    except Exception as e:
        return "Error", 0.0





import os

print("\n🗂 Current Working Directory Files:")
for dirpath, dirnames, filenames in os.walk(".", topdown=True):
    print(f"\n📁 {dirpath}")
    for file_name in filenames:
        print(f"   - {file_name}")



# --- STREAMLIT UI START ---
st.set_page_config(page_title="🎧 English Accent Analyzer", layout="wide")
st.title("🎧 English Accent Analyzer")

# Upload & Parameters
uploaded_file = st.file_uploader("📂 Upload a Video File", type=["mp4", "avi", "mkv"])
chunk_size = st.selectbox("⏱ Select Chunk Size (seconds)", [3, 5, 7, 10, 12, 15], index=1)

# Start button
start = st.button("🚀 Start Analysis")

if start and uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        with st.spinner("⏳ Please wait, analyzing the audio chunks..."):
            temp_video_path = os.path.join(tmpdir, uploaded_file.name)
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.read())

            temp_audio = os.path.join(tmpdir, "audio.wav")
            extract_audio_ffmpeg(temp_video_path, temp_audio)
            chunks = split_audio_ffmpeg(temp_audio, chunk_size, tmpdir)

            results = []
            st.subheader("🔍 Accent Analysis Results")

            for start_time, chunk_path in chunks:
                label, confidence = classify_accent(chunk_path)
                st.markdown(f"**⏱ {start_time}-{start_time + chunk_size} sec**")
                st.write(f"🔊 Predicted Accent: `{label}`")
                st.write(f"🎯 Confidence: `{confidence:.2f}%`")
                st.audio(chunk_path, format='audio/wav')
                results.append([f"{start_time}-{start_time + chunk_size}s", label, f"{confidence:.2f}%"])

            # Save to CSV
            csv_path = os.path.join(tmpdir, "accent_analysis_results.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Time Interval", "Predicted Accent", "Confidence"])
                writer.writerows(results)

            with open(csv_path, "rb") as f:
                st.download_button("📥 Download CSV Results", f, file_name="accent_analysis_results.csv", mime="text/csv")

        st.success("✅ Analysis complete!")
elif start and not uploaded_file:
    st.warning("⚠️ Please upload a video file before starting analysis.")
