import speech_recognition as sr


def test_end_to_end_speech_to_command(mocker):
    r = sr.Recognizer()
    fake_source = mocker.Mock()
    fake_audio = mocker.Mock()
    mock_audio_file = mocker.patch("speech_recognition.AudioFile")
    mock_audio_file.return_value.__enter__.return_value = fake_source
    mocker.patch.object(r, "record", return_value=fake_audio)
    mocker.patch.object(r, "recognize_google", return_value="What is the weather")

    with sr.AudioFile("tests/audio_samples/weather_query.wav") as source:
        audio = r.record(source)

    query = r.recognize_google(audio)
    assert "weather" in query.lower()
