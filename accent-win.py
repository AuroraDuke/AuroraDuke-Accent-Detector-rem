import os
import subprocess
import torch
import torchaudio
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import tempfile
import csv
import webbrowser
from speechbrain.pretrained.interfaces import foreign_class

# Load SpeechBrain accent classifier using custom interface
classifier = foreign_class(
    source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier"
)

# Extract audio from video using FFmpeg
def extract_audio_ffmpeg(video_path, audio_output):
    command = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_output]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_output

# Split audio into chunks using FFmpeg
def split_audio_ffmpeg(audio_path, chunk_length_sec, temp_dir):
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", audio_path
    ]).decode().strip())

    chunks = []
    for i in range(0, int(duration), chunk_length_sec):
        output_chunk = os.path.join(temp_dir, f"chunk_{i}.wav")
        command = ["ffmpeg", "-y", "-i", audio_path, "-ss", str(i), "-t", str(chunk_length_sec), output_chunk]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunks.append((i, output_chunk))
    return chunks

# Predict accent using SpeechBrain custom classifier
def classify_accent(audio_path):
    try:
        out_prob, score, index, label = classifier.classify_file(audio_path)
        return label[0], score.item() * 100
    except Exception as e:
        return "Error", 0.0

# Play audio file
def play_audio(path):
    if os.name == 'nt':
        os.startfile(path)
    else:
        subprocess.run(['xdg-open', path])

# Main analysis logic
def run_analysis(video_path, chunk_size, result_box):
    result_box.delete("1.0", tk.END)
    results = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_audio = os.path.join(temp_dir, "audio.wav")
        extract_audio_ffmpeg(video_path, temp_audio)
        chunks = split_audio_ffmpeg(temp_audio, chunk_size, temp_dir)

        for start_time, chunk_path in chunks:
            label, confidence = classify_accent(chunk_path)
            entry_text = f"{start_time}-{start_time + chunk_size} sec\nPredicted: {label}\nConfidence: {confidence:.2f}%\n"
            result_box.insert(tk.END, entry_text)

            # Add playback button
            play_btn = ttk.Button(result_frame, text=f"▶ Play {start_time}s", command=lambda p=chunk_path: play_audio(p))
            result_box.window_create(tk.END, window=play_btn)
            result_box.insert(tk.END, "\n\n")

            results.append([f"{start_time}-{start_time + chunk_size}s", label, f"{confidence:.2f}%"])

        # Export to CSV
        with open("accent_analysis_results.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time Interval", "Predicted Accent", "Confidence"])
            writer.writerows(results)

    messagebox.showinfo("Analysis Complete", "Accent analysis is complete. Results saved to 'accent_analysis_results.csv'.")

# Browse file callback
def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[["Video Files", "*.mp4 *.avi *.mkv"]])
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

# Start button callback
def start_analysis(entry, spinbox, result_box):
    video_path = entry.get()
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "Video file not found.")
        return

    try:
        chunk_size = int(spinbox.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid chunk size.")
        return

    threading.Thread(target=run_analysis, args=(video_path, chunk_size, result_box)).start()

# GUI setup
root = tk.Tk()
root.title("🎧 English Accent Analyzer")
root.geometry("750x500")
style = ttk.Style(root)
style.theme_use('clam')

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# File selection
ttk.Label(main_frame, text="🎬 Video File:").grid(row=0, column=0, sticky='w', pady=5)
path_entry = ttk.Entry(main_frame, width=50)
path_entry.grid(row=0, column=1, padx=5)
ttk.Button(main_frame, text="Browse", command=lambda: browse_file(path_entry)).grid(row=0, column=2)

# Chunk size selection
ttk.Label(main_frame, text="⏱ Chunk Size (sec):").grid(row=1, column=0, sticky='w', pady=10)
chunk_spinbox = ttk.Combobox(main_frame, values=[3, 5, 7, 10, 12, 15], width=5)
chunk_spinbox.set(5)
chunk_spinbox.grid(row=1, column=1, sticky="w")

# Start button
ttk.Button(main_frame, text="🚀 Start Analysis", command=lambda: start_analysis(path_entry, chunk_spinbox, result_text)).grid(row=2, column=0, columnspan=3, pady=15)

# Results text box with scrollbars
ttk.Label(root, text="🔍 Results:").pack()
result_frame = ttk.Frame(root)
result_frame.pack(padx=20, pady=10, fill='both', expand=True)

scrollbar_y = ttk.Scrollbar(result_frame, orient="vertical")
scrollbar_y.pack(side='right', fill='y')



result_text = tk.Text(result_frame, wrap="none", height=15, width=80, yscrollcommand=scrollbar_y.set)
result_text.pack(side='left', fill='both', expand=True)

scrollbar_y.config(command=result_text.yview)


# Run the GUI
root.mainloop()
