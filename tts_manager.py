from __future__ import annotations

import asyncio
import hashlib
import logging
from pathlib import Path
from typing import Optional

import edge_tts
from pydub import AudioSegment


class TTSManager:
    """Edge-TTS narration generator for longform and shorts projects."""

    DEFAULT_VOICE = "ko-KR-HyunsuNeural"
    LONG_RATE = "-10%"
    SHORT_RATE = "+5%"
    PITCH = "0Hz"
    VOLUME = "+0%"

    CATEGORY_RATES = {
        "Economy": "-10%",
        "AI / Technology": "-5%",
        "Military": "-15%",
        "Tension / Crisis": "-15%",
        "Crisis": "-20%",
        "Ending": "-10%",
        "Documentary": "-10%",
    }

    def __init__(self, voice: str = DEFAULT_VOICE, logger: Optional[logging.Logger] = None) -> None:
        self.voice = voice
        self.logger = logger or logging.getLogger(__name__)

    def get_rate_by_category(self, category: Optional[str], is_shorts: bool = False) -> str:
        if is_shorts:
            return self.SHORT_RATE
        if not category:
            return self.LONG_RATE
        return self.CATEGORY_RATES.get(category, self.LONG_RATE)

    async def validate_voice_available(self, voice_name: Optional[str] = None) -> bool:
        target_voice = voice_name or self.voice
        voices = await edge_tts.list_voices()
        return any(voice.get("ShortName") == target_voice for voice in voices)

    async def generate_longform_tts(
        self,
        text: str,
        output_path: str | Path,
        category: Optional[str] = None,
    ) -> Path:
        return await self._generate_tts(
            text=text,
            output_path=output_path,
            rate=self.get_rate_by_category(category, is_shorts=False),
        )

    async def generate_shorts_tts(
        self,
        text: str,
        output_path: str | Path,
        shorts_index: int,
        category: Optional[str] = None,
    ) -> Path:
        path = Path(output_path)
        if path.is_dir():
            path = path / f"shorts_{shorts_index:02d}.mp3"
        return await self._generate_tts(
            text=text,
            output_path=path,
            rate=self.get_rate_by_category(category, is_shorts=True),
        )

    def measure_audio_duration(self, audio_path: str | Path) -> float:
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0

    async def _generate_tts(self, text: str, output_path: str | Path, rate: str) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        text_hash = self._text_hash(text, rate)
        hash_path = output.with_suffix(output.suffix + ".sha256")

        if output.exists() and hash_path.exists() and hash_path.read_text(encoding="utf-8") == text_hash:
            self.logger.info("TTS cache hit: %s", output)
            return output

        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=rate,
                pitch=self.PITCH,
                volume=self.VOLUME,
            )
            await communicate.save(str(output))
            hash_path.write_text(text_hash, encoding="utf-8")
            duration = self.measure_audio_duration(output)
            self.logger.info("TTS generated: %s (%.2fs)", output, duration)
            return output
        except Exception:
            self.logger.exception("TTS generation failed: %s", output)
            raise

    def _text_hash(self, text: str, rate: str) -> str:
        payload = "\n".join([self.voice, rate, self.PITCH, self.VOLUME, text])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


async def _demo() -> None:
    manager = TTSManager()
    ok = await manager.validate_voice_available()
    print(f"voice_available={ok}")


if __name__ == "__main__":
    asyncio.run(_demo())
