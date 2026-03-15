import numpy as np

VOICE_NAME = "en-IN-NeerjaNeural"

emotion_weights = {

    "joy":        np.array([0.6, 0.5, 0.3]),
    "gratitude":  np.array([0.4, 0.3, 0.2]),
    "excitement": np.array([0.7, 0.6, 0.4]),
    "admiration": np.array([0.4, 0.3, 0.2]),
    "optimism":   np.array([0.5, 0.4, 0.3]),
    "love":       np.array([0.5, 0.3, 0.2]),

    "anger":          np.array([0.4, 0.7, 0.7]),
    "annoyance":      np.array([0.3, 0.5, 0.5]),
    "disapproval":    np.array([0.2, 0.4, 0.4]),
    "disappointment": np.array([-0.3, -0.3, -0.2]),

    "sadness": np.array([-0.6, -0.5, -0.4]),
    "grief":   np.array([-0.7, -0.6, -0.5]),
    "remorse": np.array([-0.4, -0.3, -0.2]),

    "fear":        np.array([0.2, 0.3, 0.1]),
    "nervousness": np.array([0.2, 0.2, 0.1]),
    "confusion":   np.array([0.1, -0.1, 0.0]),

    "surprise": np.array([0.5, 0.3, 0.2]),
    "realization": np.array([0.2, 0.1, 0.0]),

    "relief": np.array([-0.2, -0.1, 0.0]),
    "approval": np.array([0.2, 0.2, 0.1]),

    "neutral": np.array([0.0, 0.0, 0.0])
}
