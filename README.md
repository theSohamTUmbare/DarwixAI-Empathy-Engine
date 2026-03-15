# Empathy Engine – Emotion-Aware Text-to-Speech

## Overview

The **Empathy Engine** is a system designed to generate emotionally expressive speech from text. Traditional Text-to-Speech systems often sound monotonic because they apply fixed prosody parameters during synthesis. This project attempts to bridge that gap by dynamically adjusting vocal parameters based on the emotional content of the input text.

The system analyzes text to detect emotional signals and then modulates speech characteristics such as **pitch**, **rate**, and **volume** before synthesizing audio output.

The result is a more natural and expressive voice output compared to baseline TTS.

---

## Key Features

- Emotion detection using a **GoEmotions transformer model**
- Emotion-to-prosody mapping using **weighted emotional vectors**
- Dynamic modulation of:
  - Pitch
  - Speech Rate
  - Volume
- Emotion intensity scaling
- Prosody smoothing across sentence segments
- Natural pause detection for better speech flow
- Web interface for quick demonstration

---

## System Architecture


---

## Emotion Detection

The system uses the **GoEmotions model** (`SamLowe/roberta-base-go_emotions`) from HuggingFace Transformers.

Unlike simple sentiment classifiers (positive/negative/neutral), this model detects a wide range of emotions such as:

- joy
- excitement
- admiration
- sadness
- fear
- anger
- confusion
- relief
- etc.

Each emotion is returned with a confidence score.

Example output:

```
    {
    "joy": 0.62,
    "excitement": 0.21,
    "admiration": 0.10,
    "sadness": 0.01
    }
```


---

## Emotion → Voice Parameter Mapping

Each detected emotion contributes to speech modulation using predefined **prosody weight vectors**:

[pitch, rate, volume]

Example: 
joy → [0.6, 0.5, 0.3]
sadness → [-0.6, -0.5, -0.4]
anger → [0.4, 0.7, 0.7]


The final prosody vector is computed as a **weighted sum of all emotion scores**.

prosody = Summition of  (emotion_score × emotion_weight)


These values are then scaled to produce final speech parameters.

---

## Emotion Intensity Scaling

Emotion intensity is calculated using the **maximum emotion confidence score**.

Higher intensity increases prosody variation:

```
    pitch = pitch × (1 + intensity)
    rate = rate × (1 + 0.7 × intensity)
    volume = volume × (1 + 0.4 × intensity)
```


This allows stronger emotions to produce more expressive speech.

---

## Prosody Smoothing

Speech parameters are smoothed across segments using an exponential smoothing approach:

smoothed = previous × *alpha* + current × (1 − *alpha*)



This prevents abrupt changes in pitch or speaking rate between sentence segments.

---

## Natural Pause Detection

The system splits text at natural linguistic boundaries such as:

- sentence endings (`.`, `?`, `!`)
- conjunctions (`and`, `but`, `so`, `because`)

This helps produce more natural phrasing and improves emotion analysis granularity.

---

## Technology Stack

- **Python**
- **FastAPI** – Web interface and API
- **Transformers (HuggingFace)** – Emotion detection
- **Edge-TTS** – Speech synthesis
- **NumPy** – Prosody computation

---

## Project Structure

```
    empathy-engine/
    │
    ├── app/
    │   ├── __init__.py
    │
    │   ├── main.py
    │   ├── config.py
    │
    │   ├── emotion/
    │   │   ├── classifier.py
    │   │   └── mapping.py
    │
    │   ├── tts/
    │   │   ├── tts_engine.py
    │   │   └── audio_utils.py
    │
    │   ├── services/
    │   │   └── empathy_service.py
    │
    │   ├── api/
    │   │   └── routes.py
    │
    ├── static/
    │   └── audio/
    │       └── output.mp3
    │
    ├── templates/
    │   └── index.html
    │
    ├── requirements.txt
    ├── README.md
    └── run.py
```


---

## Installation

Clone the repository:

```
    git clone https://github.com/theSohamTUmbare/DarwixAI-Empathy-Engine.git
```


Install dependencies:

```
    pip install -r requirements.txt
```


---

## Running the Application

Start the server:

```
    python run.py
```


Open in browser:

```
    http://localhost:8000
```
