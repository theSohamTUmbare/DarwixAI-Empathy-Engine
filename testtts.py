import asyncio
import edge_tts

async def test():

    communicate = edge_tts.Communicate(
        text="Hello this is a test",
        voice="en-IN-NeerjaNeural"
    )

    await communicate.save("test.mp3")

asyncio.run(test())
