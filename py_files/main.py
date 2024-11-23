from class_tg_bot import *
import json
from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
   log_filename = str(datetime.datetime.now().strftime("logs/%Y_%m_%d_time_%H_%M_%S_bot.log"))
   log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
   logger = RotatingFileHandler(log_filename, mode='a', maxBytes=50*1024*1024,
                                 backupCount=1, encoding=None, delay=0)
   logger.setFormatter(log_formatter)
   logger.setLevel(logging.INFO)

   bot_log = logging.getLogger(__name__)
   bot_log.setLevel(logging.INFO)

   bot_log.addHandler(logger)

   bot_log.info(f"Start bot")

   with open("json_files/commands_switch.json", "r") as my_file:
      commands_switch = json.loads(my_file.read())

   with open("json_files/rcon_commands_switch.json", "r") as my_file:
      rcon_commands_switch = json.loads(my_file.read())

   bot_tg = tg_bot(commands_switch, rcon_commands_switch, bot_log)  # Инициализация бота с токеном из файла параметров

   while True:
      try:
         bot_tg.run_bot()  # Бесконечный цикл работы бота
      except Exception as e:
         bot_log.error(f"Main polling error: {e}")
