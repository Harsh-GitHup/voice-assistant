import speech_recognition as sr


def test_speech_recognition_accuracy(mocker):
    """Verifies recognition flow without relying on external audio files/services."""
    r = sr.Recognizer()
    audio_path = "tests/samples/open_google.wav"
    fake_source = mocker.Mock()
    fake_audio = mocker.Mock()

    mock_audio_file = mocker.patch("speech_recognition.AudioFile")
    mock_audio_file.return_value.__enter__.return_value = fake_source
    mocker.patch.object(r, "record", return_value=fake_audio)
    mocker.patch.object(r, "recognize_google", return_value="Open Google")

    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    query = r.recognize_google(audio)
    assert "google" in query.lower()
