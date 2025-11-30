from banglaspeech2text import Speech2Text
import tkinter as tk
from tkinter import filedialog
import os

# 1) Tkinter root
root = tk.Tk()
root.withdraw()

# 2) Pick multiple audio files
audio_paths = filedialog.askopenfilenames(
    title="Select Bangla audio files",
    filetypes=[
        ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg"),
        ("All files", "*.*"),
    ],
)

if not audio_paths:
    print("No file selected. Exiting.")
    exit()

print("Selected files:")
for p in audio_paths:
    print(" -", p)

# 3) Force CPU, avoid cuDNN / GPU (load model once)
stt = Speech2Text("small", device="cpu")

# 4) Loop over files and transcribe one by one
for audio_path in audio_paths:
    print(f"\nTranscribing: {audio_path}")

    text = stt.recognize(audio_path)
    print("  Transcription finished.")

    audio_dir = os.path.dirname(audio_path)
    base_name = os.path.basename(audio_path)
    name_without_ext, _ = os.path.splitext(base_name)
    txt_path = os.path.join(audio_dir, f"{name_without_ext}_banglaSTT.txt")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"  Saved to: {txt_path}")

print("\nAll done.")
