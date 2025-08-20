import logging
from typing import Optional
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

class AudioTranscriber:
    def __init__(self, model_size: str = "small"):
        try:
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
            logger.info(f"Whisper {model_size} model loaded.")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe(self, audio_path: str) -> Optional[str]:
        if not audio_path or not isinstance(audio_path, str):
            logger.error("Invalid audio path.")
            return None

        try:
            segments, _ = self.model.transcribe(audio_path, language="en")
            text = " ".join([seg.text for seg in segments])
            logger.info(f"Transcribed {len(segments)} segments.")
            return text.strip()
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return None
