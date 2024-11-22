from class_tg_bot import *
import json

if __name__ == '__main__':

   with open("json_files/commands_switch.json", "r") as my_file:
      commands_switch = json.loads(my_file.read())

   with open("json_files/rcon_commands_switch.json", "r") as my_file:
      rcon_commands_switch = json.loads(my_file.read())

   bot_tg = tg_bot(commands_switch, rcon_commands_switch)  # Инициализация бота с токеном из файла параметров

   while True:
      try:
         bot_tg.run_bot()  # Бесконечный цикл работы бота
      except Exception as e:
         print(e)
