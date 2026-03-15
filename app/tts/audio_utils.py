import re


def split_natural_pauses(text):

    pattern = r'([.!?]\s+|\s(?:and|or|but|so|because)\s+)'

    parts = re.split(pattern, text, flags=re.IGNORECASE)

    result = [parts[0].strip()]

    for i in range(1, len(parts), 2):

        delimiter = parts[i]
        content = parts[i+1] if i+1 < len(parts) else ""

        combined = (delimiter + content).strip()

        if combined:
            result.append(combined)

    return [r for r in result if r]


def format_tts_params(pitch, rate, volume):

    pitch_str = f"{int(pitch):+d}Hz"
    rate_str = f"{int(rate):+d}%"
    volume_str = f"{int(volume):+d}%"

    return pitch_str, rate_str, volume_str
