import numpy as np
from io import BytesIO
from pydub import AudioSegment

from app.emotion.classifier import detect_emotions, emotion_intensity
from app.emotion.mapping import compute_voice_params, apply_intensity_scaling
from app.tts.audio_utils import split_natural_pauses, trim_silence
from app.tts.tts_engine import generate_segment_audio


def punctuation_pause(text):

    if text.endswith(","):
        return 160
    if text.endswith("."):
        return 340
    if text.endswith("?"):
        return 380
    if text.endswith("!"):
        return 360

    return 210


def emotion_pause_factor(scores):

    arousal = sum(scores.get(e,0) for e in
        ["anger","annoyance","excitement","fear","surprise"])

    calm = sum(scores.get(e,0) for e in
        ["sadness","remorse","disappointment","grief"])

    factor = 1.0 + (calm * 0.5) - (arousal * 0.3)

    return max(0.6, min(1.6, factor))


def clause_pause_factor(text):

    connectors = ["but","however","although","though","because"]

    first_word = text.lower().split()[0]

    if first_word in connectors:
        return 1.5

    return 1.0


def compute_pause(text, scores):

    base = punctuation_pause(text)

    emotion_factor = emotion_pause_factor(scores)

    clause_factor = clause_pause_factor(text)

    pause = base * emotion_factor * clause_factor

    return int(pause)


async def generate_emotional_voice(text):

    segments = split_natural_pauses(text)

    prev_params = np.array([0.0,0.0,0.0])

    final_audio = AudioSegment.silent(duration=0)

    for s in segments:

        emotion_scores = detect_emotions(s)

        pitch, rate, volume = compute_voice_params(emotion_scores)

        intensity = emotion_intensity(emotion_scores)

        pitch, rate, volume = apply_intensity_scaling(
            pitch, rate, volume, intensity
        )

        current = np.array([pitch,rate,volume])

        current = prev_params * 0.6 + current * 0.4

        prev_params = current

        pitch,rate,volume = current

        if len(s.split()) > 12:
            rate += 1

        audio = await generate_segment_audio(s, pitch, rate, volume)

        audio = trim_silence(audio)

        cross = min(20, len(audio)//2, len(final_audio)//2)

        if len(final_audio) == 0:
            final_audio = audio
        else:
            final_audio = final_audio.append(audio, crossfade=cross)

        pause = compute_pause(s, emotion_scores)

        final_audio += AudioSegment.silent(duration=pause)

    output_path = "static/audio/output.wav"

    final_audio.export(output_path, format="wav")

    return output_path
