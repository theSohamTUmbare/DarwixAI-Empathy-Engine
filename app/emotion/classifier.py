from transformers import pipeline

classifier = pipeline(
    task="text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)


def detect_emotions(text):

    result = classifier(text)[0]

    emotion_scores = {}

    for r in result:
        emotion_scores[r["label"]] = r["score"]

    return emotion_scores


def emotion_intensity(emotion_scores):

    return max(emotion_scores.values())
