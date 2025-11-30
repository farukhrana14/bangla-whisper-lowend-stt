Here’s a Markdown README you can drop in as `README.md` and tweak later.

***

# Bangla Whisper STT for Low‑End PCs

Bangla speech‑to‑text pipeline using Whisper‑based models, optimized for low‑end Windows PCs.  
This repo focuses on offline Bangla ASR with CPU‑only inference, light noise reduction, and simple Tkinter dialogs to batch‑transcribe call recordings or lectures into Bangla text.

## Features

- Offline Bangla speech‑to‑text (no cloud API required)  
- CPU‑only inference suitable for low‑end laptops/desktops  
- Simple GUI file picker using Tkinter  
- Batch transcription: select multiple audio files and get one `.txt` per file  
- Optional pre‑processing step for basic noise reduction before transcription  

## Project structure

- `bangla_stt.py`  
  - Select one or more audio files  
  - Run Bangla ASR (Whisper‑based)  
  - Save `{name}_banglaSTT.txt` next to each audio file  

- `denoise_audio.py`  
  - Select a raw audio file (e.g. `.m4a`, `.wav`)  
  - Convert to 16kHz mono WAV  
  - Apply simple spectral‑gating noise reduction  
  - Save `{name}_denoised.wav` for later transcription  

You can first run `denoise_audio.py` on noisy recordings, then feed the `_denoised.wav` files to `bangla_stt.py`.

## Requirements

- Python 3.9+  
- Windows (tested)  
- Recommended:
  - `ffmpeg` on PATH (for audio conversion)  

Python packages (install via `pip`):

```bash
pip install banglaspeech2text
pip install noisereduce soundfile
```

Plus standard dependencies like `tkinter` (ships with most Python builds on Windows).

## Usage

### 1. Denoise a single audio file (optional)

```bash
python denoise_audio.py
```

- A file dialog will open.  
- Select your raw audio file (e.g. a call recording chunk).  
- Script will create `{original_name}_denoised.wav` in the same folder.

### 2. Transcribe Bangla audio (single or multiple files)

```bash
python bangla_stt.py
```

- A “select files” dialog will open.  
- Choose one or more audio files (`.mp3`, `.wav`, `.m4a`, etc. — denoised or raw).  
- For each file, a `{name}_banglaSTT.txt` will be saved beside the audio.

The transcription text is in Bangla; you can then manually clean up / edit for research or documentation.

## Implementation notes

- Uses a Whisper‑based Bangla ASR via `BanglaSpeech2Text` with the small model on CPU.  
- Noise reduction uses a simple spectral‑gating approach from the `noisereduce` package.  
- Tkinter is used only for a very lightweight file‑picker UI, to avoid CLI path hassles.  

This setup is designed for:

- Teachers and researchers dealing with Bangla call recordings or interviews  
- Users who want offline transcription on modest hardware  
- Quick exploratory analysis of qualitative data (banking, policy, etc.)

## Credits

This project builds on the excellent work of:

- BanglaSpeech2Text – offline Bangla ASR package based on Whisper  
  - https://github.com/shhossain/BanglaSpeech2Text
- OpenAI Whisper – general‑purpose speech‑to‑text model family  
  - https://github.com/openai/whisper
- noisereduce – Python noise reduction using spectral gating  
  - https://pypi.org/project/noisereduce/

Please refer to their respective repositories and licenses for details.

## License

This project is released under the **MIT License** so that others can freely use, modify, and extend the code.  
