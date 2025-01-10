from dotenv import dotenv_values  # библиотека для подгрузки токена
import telebot  # библиотека для создания телеграм ботов
from audio_module import audio_processing  # Аудиомодуль
import logging  # библиотека логирования
import os

def main():
    """
    This is a telegram bot that performs SST function
    """

    # Настройка записи логов
    logging.basicConfig(level=logging.INFO, filename="bot_log.log",filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    if os.path.exists(".env"):  # Проверка наличия токена
        config = dotenv_values(".env")  # Подгрузка токена
        logging.info("Token accepted")
    else:
        logging.critical("No .env detected! Shutting down")  # Лог-сообщение об отсутствии токена
        print("Токен не обнаружен! Отключаюсь")
        exit()  # Остановка скрипта


    # Подключение бота
    bot = telebot.TeleBot(config.get('TOKEN'), parse_mode=None)

    # Обработка команд /start и /help
    @bot.message_handler(commands=['start', 'help'])  # Если пользователь вводит данные комманды, то...
    def send_welcome(message):  # отправляется сообщение
        bot.reply_to(message, "Hello there! I'm able to recognize French speech from a mile. Please, upload audio file or send me a voice-message and I'll do what I can.")

    # Обработка полученных аудио-файлов и голосовых сообщений
    @bot.message_handler(content_types=['voice', 'audio'])  # Если содержимое сообщения аудио или голосове, то...
    def process_audio(message):
        if message.content_type == 'voice':  # Если содержимое -- голосовое...
            file_info = bot.get_file(message.voice.file_id)  # Получение данных об аудио-файле или голосовом сообщении
            downloaded_file = bot.download_file(file_info.file_path)  # Загрузка айдио-файла или голосового сообщения
            with open('./container/new_file.wav', 'wb') as new_file:  # Сохранение голосового сообщения в контейнере на локальной машине. (in wb "b" stands for bytes)
                new_file.write(downloaded_file)
            reply = audio_processing(r'./container/new_file.wav')  # Распознавание записанного файла функцией из смежного модуля
        elif message.content_type == 'audio':  # Если содержимое сообщения -- аудиофайл...
            file_info = bot.get_file(message.audio.file_id)  # получение информации об аудиофайле
            downloaded_file = bot.download_file(file_info.file_path)  # сохранение файла в переменную
            with open('./container/new_file.wav', 'wb') as new_file:  # запись файла на локальную машину во временный контейнер
                new_file.write(downloaded_file)
            reply = audio_processing(r'./container/new_file.wav')  # Ответ, содержимым которого является резултат работы модлуя распознавания речи
        else:
            logging.warning("Incorrect filetype recieved!")
            reply = 'Sorry! Incorrect file type.' # Если вы отправили боту что-либо другое
        bot.reply_to(message, reply)  # Отправка ответа (либо сообщение об ошибке, либо текст)


    bot.infinity_polling() # Обращение к серверу телеграмма (должно быть в самом конце)

if __name__ == "__main__":
    main()

