from faster_whisper import WhisperModel
from app.core.logging import logger

_model = None

def get_model():
    global _model
    if _model is None:
        logger.info("Loading Whisper model (lazy)")
        _model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )
    return _model


def transcribe_audio(audio_path: str, progress_callback=None):
    model = get_model()
    logger.info("Starting transcription")

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=False,
    )

    transcript = []
    total = 0

    for segment in segments:
        total += 1
        transcript.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
        })

        if progress_callback:
            # Fake but smooth progress (AI models don’t expose real progress)
            progress_callback(min(99, total * 2))

    return {
        "language": info.language,
        "segments": transcript,
    }
