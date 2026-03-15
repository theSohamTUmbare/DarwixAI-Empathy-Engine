import edge_tts
from io import BytesIO
from pydub import AudioSegment
from app.config import VOICE_NAME
from app.tts.audio_utils import format_tts_params


async def generate_segment_audio(text, pitch, rate, volume):

    pitch_str, rate_str, volume_str = format_tts_params(
        pitch, rate, volume
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE_NAME,
        pitch=pitch_str,
        rate=rate_str,
        volume=volume_str
    )

    audio_bytes = b''

    async for chunk in communicate.stream():

        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")

    return audio
