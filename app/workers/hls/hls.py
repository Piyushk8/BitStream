import subprocess
import os
import re


def generate_hls_from_source(
    input_path: str,
    hls_dir: str,
    progress_callback=None,
):
    os.makedirs(hls_dir, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-filter_complex",
        "[0:v]split=2[v720][v480];"
        "[v720]scale=-2:720[v720out];"
        "[v480]scale=-2:480[v480out]",
        "-map",
        "[v720out]",
        "-map",
        "0:a",
        "-c:v:0",
        "libx264",
        "-b:v:0",
        "2500k",
        "-preset",
        "veryfast",
        "-c:a:0",
        "aac",
        "-b:a:0",
        "128k",
        "-map",
        "[v480out]",
        "-map",
        "0:a",
        "-c:v:1",
        "libx264",
        "-b:v:1",
        "1000k",
        "-preset",
        "veryfast",
        "-c:a:1",
        "aac",
        "-b:a:1",
        "96k",
        "-f",
        "hls",
        "-hls_time",
        "4",
        "-hls_playlist_type",
        "vod",
        "-hls_segment_filename",
        f"{hls_dir}/%v/segment_%03d.ts",
        "-master_pl_name",
        "master.m3u8",
        "-var_stream_map",
        "v:0,a:0 v:1,a:1",
        f"{hls_dir}/%v/playlist.m3u8",
        "-progress",
        "pipe:1",
        "-nostats",
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    time_re = re.compile(r"out_time_ms=(\d+)")

    while True:
        line = process.stdout.readline()
        if not line:
            break

        match = time_re.search(line)
        if match and progress_callback:
            ms = int(match.group(1))
            progress_callback(ms)

        if "progress=end" in line:
            break

    process.wait()

    if process.returncode != 0:
        raise RuntimeError("Adaptive HLS generation failed")
