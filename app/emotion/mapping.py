import numpy as np
from app.config import emotion_weights


def compute_voice_params(emotion_scores):

    prosody = np.array([0.0, 0.0, 0.0])

    for emotion, score in emotion_scores.items():

        if emotion in emotion_weights:
            prosody += score * emotion_weights[emotion]

    pitch, rate, volume = prosody

    pitch = int(pitch * 20)
    rate = int(rate * 30)
    volume = int(volume * 15)

    return pitch, rate, volume


def apply_intensity_scaling(pitch, rate, volume, intensity):

    pitch = pitch * (1 + intensity)
    rate = rate * (1 + intensity * 0.7)
    volume = volume * (1 + intensity * 0.4)

    return pitch, rate, volume
