# Inspired by https://github.com/openai/openai-python/blob/main/examples/audio.py
import pyaudio


def stream_to_speakers(openai_client, input) -> None:
    player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    with openai_client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            response_format="pcm",  # similar to WAV, but without a header chunk at the start.
            input=input,
    ) as response:
        for chunk in response.iter_bytes(chunk_size=1024):
            player_stream.write(chunk)
