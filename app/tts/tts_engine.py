import edge_tts
from app.config import VOICE_NAME


async def synthesize(text, pitch, rate, volume, output_path):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE_NAME,
        pitch=pitch,
        rate=rate,
        volume=volume
    )

    audio_bytes = b''

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    with open(output_path, "wb") as f:
        f.write(audio_bytes)
