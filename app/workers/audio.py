import subprocess
import os

def extract_audio(input_video: str, output_audio: str):
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vn",              # no video
        "-ac", "1",         # mono (better for speech)
        "-ar", "16000",     # Whisper preferred sample rate
        "-f", "wav",
        output_audio,
    ]

    subprocess.run(cmd, check=True)
