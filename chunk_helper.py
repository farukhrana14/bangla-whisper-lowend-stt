import os
import math
import subprocess

def split_into_chunks(audio_path, chunk_seconds=300):
    """
    Split audio_path into ~chunk_seconds chunks using ffmpeg.
    Returns:
        chunks_folder: path to folder with chunks
        chunk_paths: list of full paths to chunk files
    """
    # 1) Get duration with ffprobe
    ffprobe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ]
    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
    duration_str = result.stdout.strip()
    if not duration_str:
        raise RuntimeError("Could not get duration from ffprobe.")
    total_seconds = float(duration_str)
    print(f"Audio duration: {total_seconds:.1f} seconds")

    num_chunks = math.ceil(total_seconds / chunk_seconds)
    print(f"Splitting into {num_chunks} chunk(s) of about {chunk_seconds/60:.0f} minutes each")

    # 2) Prepare chunks folder under project
    chunks_folder = os.path.join(os.getcwd(), "temp_chunks")
    os.makedirs(chunks_folder, exist_ok=True)

    # Remove old chunks
    for f in os.listdir(chunks_folder):
        os.remove(os.path.join(chunks_folder, f))

    print("Creating chunks...")

    # 3) ffmpeg command: decode once and write clean WAV segments
    out_pattern = os.path.join(chunks_folder, "chunk_%03d.wav")

    ffmpeg_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        out_pattern,
    ]

    subprocess.run(ffmpeg_cmd, check=True)
    print("All chunks created.")

    # 4) Collect chunk file paths
    chunk_files = sorted(
        f for f in os.listdir(chunks_folder) if f.startswith("chunk_")
    )
    if not chunk_files:
        raise RuntimeError("No chunk files were created.")

    chunk_paths = [os.path.join(chunks_folder, f) for f in chunk_files]
    print(f"Found {len(chunk_paths)} chunk file(s).")

    return chunks_folder, chunk_paths
