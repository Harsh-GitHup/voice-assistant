import base64
import os

# Base64 strings representing small WAV files (Sample Rate: 16k, Mono)
AUDIO_DATA = {
    "weather_query.wav": "UklGRiYAAABXQVZFRm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",  # Simplified Placeholder
    "wikipedia_query.wav": "UklGRiYAAABXQVZFRm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
    "stop_command.wav": "UklGRiYAAABXQVZFRm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
}


def setup_test_audio():
    os.makedirs("tests/audio_samples", exist_ok=True)
    for filename, b64_string in AUDIO_DATA.items():
        with open(f"tests/audio_samples/{filename}", "wb") as f:
            f.write(base64.b64decode(b64_string))
    print("✅ Test audio samples generated in tests/audio_samples/")


if __name__ == "__main__":
    setup_test_audio()
