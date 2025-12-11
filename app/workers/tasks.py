# app/workers/tasks.py
import os
import subprocess
from typing import Dict, Any
from pathlib import Path

def extract_metadata_and_thumbnail(saved_path: str, output_dir: str) -> Dict[str, Any]:
    """
    CPU-bound: run ffprobe and ffmpeg to extract metadata and one thumbnail.
    This function is intended to be executed in a ProcessPoolExecutor.
    Returns a dict with metadata and thumbnail path.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # metadata via ffprobe (must be installed in system)
    # If ffprobe not present in your environment, replace with a simulated metadata dict.
    try:
        ffprobe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=width,height,codec_name",
            "-of",
            "json",
            saved_path,
        ]
        completed = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        metadata_json = completed.stdout
    except FileNotFoundError:
        # ffprobe not installed locally — return simulated metadata
        metadata_json = '{"format": {"duration": "0.0"}, "streams": []}'
    except subprocess.CalledProcessError:
        # ffprobe failed on file — return minimal metadata
        metadata_json = '{"format": {"duration": "0.0"}, "streams": []}'

    # create thumbnail (grab frame at 1s)
    thumb_path = os.path.join(output_dir, f"{Path(saved_path).stem}_thumb.jpg")
    try:
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            saved_path,
            "-ss",
            "00:00:01.000",
            "-vframes",
            "1",
            thumb_path,
        ]
        subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
        thumbnail_ok = True
    except FileNotFoundError:
        thumbnail_ok = False
    except subprocess.CalledProcessError:
        thumbnail_ok = False

    return {
        "metadata": metadata_json,
        "thumbnail_path": thumb_path if thumbnail_ok else None,
    }
