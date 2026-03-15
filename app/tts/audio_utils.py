import re
from pydub import AudioSegment


def split_natural_pauses(text):

    pattern = r'([.!?]\s+|\s(?:and|or|but|so|because|although|however|therefore)\s+)'

    parts = re.split(pattern, text, flags=re.IGNORECASE)

    result = [parts[0].strip()]

    for i in range(1, len(parts), 2):

        delimiter = parts[i]
        content = parts[i+1] if i+1 < len(parts) else ""

        combined = (delimiter + content).strip()

        if combined:
            result.append(combined)

    return [r for r in result if r]


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


def trim_silence(audio, threshold=-40.0, chunk_size=10):

    start_trim = 0
    end_trim = len(audio)

    while start_trim < len(audio) and audio[start_trim:start_trim+chunk_size].dBFS < threshold:
        start_trim += chunk_size

    while end_trim > 0 and audio[end_trim-chunk_size:end_trim].dBFS < threshold:
        end_trim -= chunk_size

    return audio[start_trim:end_trim]


def format_tts_params(pitch, rate, volume):

    pitch_str = f"{int(pitch):+d}Hz"
    rate_str = f"{int(rate):+d}%"
    volume_str = f"{int(volume):+d}%"

    return pitch_str, rate_str, volume_str
