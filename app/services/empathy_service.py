import numpy as np

from app.emotion.classifier import detect_emotions, emotion_intensity
from app.emotion.mapping import compute_voice_params, apply_intensity_scaling
from app.tts.audio_utils import split_natural_pauses, format_tts_params
from app.tts.tts_engine import synthesize


async def generate_emotional_voice(text):

    sentences = split_natural_pauses(text)

    prev_params = np.array([0.0,0.0,0.0])
    prosody_values = []

    for s in sentences:

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

        prosody_values.append([pitch,rate,volume])

    prosody_values = np.array(prosody_values)

    pitch = prosody_values[:,0].mean()
    rate = prosody_values[:,1].mean()
    volume = prosody_values[:,2].mean()

    pitch_str, rate_str, volume_str = format_tts_params(
        pitch,rate,volume
    )

    output_file = "static/audio/output.mp3"

    await synthesize(
        text,
        pitch_str,
        rate_str,
        volume_str,
        output_file
    )

    return output_file
