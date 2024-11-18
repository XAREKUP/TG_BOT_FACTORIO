from class_tg_bot import *

if __name__ == '__main__':
    bot_tg = tg_bot()  # Инициализация бота с токеном из файла параметров
    bot_tg.run_bot()  # Бесконечный цикл работы бота
