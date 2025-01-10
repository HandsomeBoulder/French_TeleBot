import whisper  # библиотека распознавания речи

def audio_processing(path):
    model = whisper.load_model("base")  # Подгрузка модели
    result = model.transcribe(path, language="fr")  # распознавание
    text = result['text']  # Запись текса в отдельную переменнуюы
    return text