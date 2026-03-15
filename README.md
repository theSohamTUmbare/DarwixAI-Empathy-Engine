# Empathy Engine — Emotion-Aware, Expressive Text-to-Speech (TTS)

Empathy Engine generates more natural, emotionally expressive speech from plain text. Instead of speaking with fixed, monotone prosody, it detects emotions in the text and dynamically adjusts pitch, speaking rate, volume, and pause timing across segments.

The project is implemented as a small FastAPI web app with a simple UI and one main TTS endpoint.

## Capabilities

- Emotion detection using a GoEmotions transformer classifier (HuggingFace)
- Emotion → prosody mapping (pitch, rate, volume)
- Intensity scaling (stronger emotions produce stronger prosody variation)
- Prosody smoothing between segments (prevents abrupt parameter jumps)
- “SSML-like” timing without SSML:
    - natural segmentation (sentences + discourse connectors)
    - emotion-aware pauses (similar to SSML `<break>`)
- Audio post-processing:
    - trim leading/trailing silence
    - crossfade between segments
    - export final output as WAV
- Web UI for quick demo + playback

## Demo

Interface screenshot (add your screenshot here):

**[ADD SCREENSHOT HERE]**

Optional: embed a WAV sample below the screenshot.

> Note: Some Markdown renderers don’t play audio inline (GitHub often shows a link). If it doesn’t render as a player, the link still works.

```html
<audio controls src="static/audio/output.wav"></audio>
```

Direct link to the latest generated audio:

- `static/audio/output.wav`

## How it works (High-level pipeline)

1. Split input text into natural segments using punctuation and connectors (and/but/because/however…).
2. Run emotion classification per segment (GoEmotions).
3. Compute prosody parameters:
     - weighted emotion-to-prosody vector sum
     - scale by emotion intensity (max confidence)
     - smooth with previous segment prosody
4. Synthesize each segment with Edge-TTS using pitch/rate/volume controls.
5. Post-process audio:
     - trim silence
     - crossfade segments
     - insert emotion-aware pauses between segments
6. Export final audio to `static/audio/output.wav` and return that path to the UI/API.

This achieves SSML-like behavior (prosody + breaks) while keeping the implementation fully programmatic and model-driven.

## Tech stack

- Python
- FastAPI + Jinja2 (web app + UI)
- Transformers + Torch (emotion model inference)
- Edge-TTS (speech synthesis)
- PyDub + FFmpeg (audio decode/processing/export)
- NumPy (prosody math)

## Project structure

```
DarwixAI-Empathy-Engine/
├── app/
│   ├── main.py                 # FastAPI app, templates, static mounting
│   ├── config.py               # Voice + emotion weight config
│   ├── api/routes.py           # POST /speak
│   ├── services/empathy_service.py
│   ├── emotion/classifier.py   # GoEmotions inference
│   ├── emotion/mapping.py      # Emotion → prosody + intensity scaling
│   └── tts/
│       ├── tts_engine.py       # Edge-TTS synthesis
│       └── audio_utils.py      # segmentation + formatting + silence trim
├── static/audio/output.wav     # generated output (overwritten each request)
├── templates/index.html        # UI
├── requirements.txt
├── run.py
└── README.md
```

## Setup (step-by-step, with common pitfalls covered)

### 1) Prerequisites

- Python 3.10+ recommended
- FFmpeg installed and available on PATH (required by PyDub to read MP3 and export WAV)
- Working internet connection on first run (downloads model weights)

### 2) Create and activate a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install Python dependencies

```bash
pip install -r requirements.txt
```


### 4) Install FFmpeg (required for PyDub)

PyDub relies on FFmpeg for decoding MP3 and exporting WAV. Without FFmpeg you may see errors like:

- `FileNotFoundError: ffmpeg`
- `pydub.exceptions.CouldntDecodeError`

Windows (recommended via winget):

```powershell
winget install Gyan.FFmpeg
```

Alternative (Chocolatey):

```powershell
choco install ffmpeg
```

Verify FFmpeg is available:

```bash
ffmpeg -version
```

If the command is not found, ensure FFmpeg’s `bin` folder is on PATH, then restart your terminal.

macOS (Homebrew):

```bash
brew install ffmpeg
```

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### 5) API keys / tokens (if needed)

This project does **not** require a paid API key by default:

- Edge-TTS does not require you to supply an API key.
- The GoEmotions model is downloaded via HuggingFace automatically on first run.

Optional (restricted networks / rate limits): set a HuggingFace token.

Windows (PowerShell):

```powershell
setx HUGGINGFACE_HUB_TOKEN "YOUR_TOKEN_HERE"
```

macOS/Linux:

```bash
export HUGGINGFACE_HUB_TOKEN="YOUR_TOKEN_HERE"
```

Restart your terminal after `setx` so the variable is available.

## Run the application

Start the FastAPI server:

```bash
python run.py
```

Open in browser:

- http://127.0.0.1:8000

Type text, click **Generate Voice**, and the UI will play the generated audio.

## API usage

### `POST /speak`

Form field:

- `text`: the input string to synthesize

Example (curl):

```bash
curl -X POST -F "text=I’m really sorry that happened. Let’s fix it together." http://127.0.0.1:8000/speak
```

Response (JSON):

```json
{ "audio": "static/audio/output.wav" }
```

> Note: `output.wav` is overwritten each time you generate audio. This is fine for a demo. For multi-user concurrency, generate unique filenames per request.

## Design notes (methodology + SSML-like approach)

### Emotion detection

- Uses the GoEmotions model: `SamLowe/roberta-base-go_emotions`.
- Produces a score for each emotion label (28 emotion labels).

### Emotion → prosody mapping

- Each emotion maps to a 3D vector: `[pitch, rate, volume]`.
- The final prosody vector is computed as a weighted sum of `emotion_score × emotion_weight`.
- Values are scaled into practical speech-control units (Hz and percent deltas).

### Intensity scaling

- Emotion intensity is computed as the maximum confidence score across detected emotions.
- Prosody is scaled so stronger detected emotion increases expressiveness.

### Prosody smoothing

- Prosody is smoothed between segments (mix of previous and current) to avoid unnatural jumps.

### Dynamic pausing (“SSML-like breaks” without SSML)

- Text is split at natural pause locations (sentence endings and connectors like “but”, “because”, “however”…).
- Pause duration is computed from:
    - punctuation baseline timing
    - an emotion factor (calm emotions lengthen pauses; arousal emotions shorten them)
    - a clause factor (certain connectors slightly increase pause)

This reproduces the effect of SSML break control, but derived automatically from content and emotion.

### Prompt-engineering methodology (for evaluation/demo text)

Although the model inference itself is not prompt-based, the demo/evaluation text was designed intentionally to elicit distinct emotional signals and prosody outcomes:

- Use realistic empathetic-assistant phrasing (apology, reassurance, validation)
- Include punctuation and clause structures that create natural prosodic boundaries
- Vary emotional tone (reassuring, concerned, inquisitive, upbeat) to validate predictable mapping behavior

## Troubleshooting

- **FFmpeg not found / decoding failed**: install FFmpeg and ensure `ffmpeg -version` works in the same terminal.
- **First run is slow**: Transformers downloads model weights on first use.
- **`pip install -r requirements.txt` fails**: ensure you’re using a clean venv; re-run with updated requirements.
