import tkinter as tk
from tkinter import filedialog
import os
import whisper

from chunk_helper import split_into_chunks

# -------- 1. Pick the large audio file --------
root = tk.Tk()
root.withdraw()

audio_path = filedialog.askopenfilename(
    title="Select large audio file",
    filetypes=[
        ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg"),
        ("All files", "*.*"),
    ],
)

if not audio_path:
    print("No file selected. Exiting.")
    exit()

print(f"Selected file: {audio_path}")

# -------- 2. Split into chunks --------
chunks_folder, chunk_paths = split_into_chunks(audio_path)
total_chunks = len(chunk_paths)

# -------- 3. Prepare output .txt next to source audio --------
audio_dir = os.path.dirname(audio_path)
base_name = os.path.basename(audio_path)
name_without_ext, _ = os.path.splitext(base_name)
txt_filename = f"{name_without_ext}_chunks.txt"
txt_path = os.path.join(audio_dir, txt_filename)

# Remove old file if exists
if os.path.exists(txt_path):
    os.remove(txt_path)

print(f"Transcriptions will be saved to:\n{txt_path}")

# -------- 4. Load Whisper once --------
print("Loading Whisper model (small)...")
model = whisper.load_model("small")

# -------- 5. Loop over chunks and transcribe --------
for idx, chunk_path in enumerate(chunk_paths, start=1):
    chunk_name = os.path.basename(chunk_path)
    print(f"\nTranscribing chunk {idx}/{total_chunks}: {chunk_name}")

    result = model.transcribe(chunk_path)
    text = result.get("text", "").strip()

    # Append to output file with separators
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n----- Chunk {idx}/{total_chunks}: {chunk_name} -----\n")
        f.write(text)

    percent = idx * 100 / total_chunks
    print(f"Chunk {idx}/{total_chunks} done ({percent:.1f}% complete)")

print(f"\nAll chunks transcribed. Full text saved to:\n{txt_path}")
