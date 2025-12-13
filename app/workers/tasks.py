# import subprocess
# import re


# def run_ffmpeg_with_progress(input_path: str, output_path: str, resolution="720p", progress_callback=None):
#     """
#     Transcode video to a resolution like 720p with progress.
#     """

#     # Get duration
#     try:
#         probe = subprocess.run(
#             [
#                 "ffprobe", "-v", "error",
#                 "-show_entries", "format=duration",
#                 "-of", "default=noprint_wrappers=1:nokey=1",
#                 input_path
#             ],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         duration = float(probe.stdout.strip())
#     except:
#         duration = None

#     # Extract resolution number (e.g. 720 from "720p")
#     h = resolution.lower().replace("p", "")

#     cmd = [
#         "ffmpeg",
#         "-y",
#         "-i", input_path,
#         "-vf", f"scale=-2:{h}",          # FIXED
#         "-c:v", "libx264",
#         "-preset", "medium",
#         "-crf", "23",
#         "-c:a", "aac",
#         "-b:a", "128k",
#         output_path,                    # FILE, not directory
#         "-progress", "pipe:1",
#         "-nostats",
#     ]

#     process = subprocess.Popen(
#         cmd,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True
#     )

#     time_re = re.compile(r"out_time_ms=(\d+)")

#     while True:
#         line = process.stdout.readline()
#         if not line:
#             break

#         match = time_re.search(line)
#         if match and duration:
#             ms = int(match.group(1))
#             progress = min(99, (ms / (duration * 1_000_000)) * 100)
#             if progress_callback:
#                 progress_callback(progress)


#         if "progress=end" in line:
#             if progress_callback:
#                 progress_callback(100)
#             break

#     process.wait()
#     return output_path
