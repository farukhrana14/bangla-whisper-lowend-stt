import os
import subprocess
import soundfile as sf
import noisereduce as nr
import tkinter as tk
from tkinter import filedialog

def m4a_to_wav(input_path, wav_path):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ac", "1",        # mono
        "-ar", "16000",    # 16 kHz
        wav_path,
    ]
    subprocess.run(cmd, check=True)

def denoise_wav(input_wav, output_wav):
    data, sr = sf.read(input_wav)
    reduced = nr.reduce_noise(y=data, sr=sr)
    sf.write(output_wav, reduced, sr)

if __name__ == "__main__":
    # 1) Tkinter hidden window
    root = tk.Tk()
    root.withdraw()

    # 2) Select raw audio file
    audio_path = filedialog.askopenfilename(
        title="Select raw audio file for denoising",
        filetypes=[
            ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg"),
            ("All files", "*.*"),
        ],
    )

    if not audio_path:
        print("No file selected. Exiting.")
        exit()

    print(f"Selected file: {audio_path}")

    # 3) Build temp + output paths (same folder as source)
    audio_dir = os.path.dirname(audio_path)
    base_name = os.path.basename(audio_path)
    name_without_ext, _ = os.path.splitext(base_name)

    mid_wav = os.path.join(audio_dir, f"{name_without_ext}_16k_mono.wav")
    final_wav = os.path.join(audio_dir, f"{name_without_ext}_denoised.wav")

    # 4) Convert to 16k mono WAV
    print("Converting to 16k mono WAV...")
    m4a_to_wav(audio_path, mid_wav)

    # 5) Denoise
    print("Running noise reduction...")
    denoise_wav(mid_wav, final_wav)

    print(f"Cleaned audio saved at: {final_wav}")
