import asyncio
import edge_tts
import os

async def generate_podcast(text, filename="output/podcast.mp3"):
    """
    Generates a podcast audio from the report text.

    Args:
        text (str): Report content.
        filename (str): Output MP3 file.
    """

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"
    )

    await communicate.save(filename)

    print(f"Podcast saved successfully: {filename}")


def create_podcast(text, filename="output/podcast.mp3"):
    asyncio.run(generate_podcast(text, filename))