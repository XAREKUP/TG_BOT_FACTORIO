from bot_function import *
from logging.handlers import RotatingFileHandler
import json

class tg_bot:
   def __init__(self, commands_switch, rcon_commands_switch, bot_log):
      self.commands_switch = commands_switch
      self.rcon_commands_switch = rcon_commands_switch
      parameters_filename = 'data/parameters.txt'
      file_param = open(parameters_filename, 'r')
      lines_param = file_param.readlines()
      file_param.close()

      self.parameters_switch = {}
      for line in lines_param:
         #print(line)
         line = line.split()
         self.parameters_switch[line[0]] = line[1]

      self.bot = telebot.TeleBot(self.parameters_switch['tg_token']) #токен бота
      self.time_last_call = datetime.datetime(2011,11,11,11,11)

      self.bot_log = bot_log

   def run_bot(self):
   ########BOT HELP########
      @self.bot.message_handler(commands=['start'])
      def start_bot(message):
         try:
            print_help(message, self)
            self.bot_log.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.bot_log.error(f"Ошибка при отправке сообщения в канал: {e}")

      @self.bot.message_handler(commands=['help'])
      def help_bot(message):
         try:
            print_help(message, self)
            self.bot_log.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.bot_log.error(f"User %s print command %s: {e}", message.from_user.username, message.text)

      #####SERVER CONTROL#####
      @self.bot.message_handler(commands=list(self.commands_switch.keys()))
      def control_server(message):
         try:
            command_executer(message, self)
            self.bot_log.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.bot_log.error(f"User %s print command %s: {e}", message.from_user.username, message.text)

      #######RCON COMMAND#######
      @self.bot.message_handler(commands=list(self.rcon_commands_switch.keys()))
      def rcon_command(message):
         try:
            rcon_command_executer(message, self)
            self.bot_log.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.bot_log.error(f"User %s print command %s: {e}", message.from_user.username, message.text)


      while True:
         try:
            self.bot.polling(none_stop=True)
         except Exception as e:
            self.bot_log.error(f"Class polling error: {e}")
            #print("class ERROR polling:" + str(e))
            time.sleep(15)

      #@self.bot.message_handler(content_types=["text"])

#      while True:
#         try: #добавляем try для бесперебойной работы
#            self.bot.polling(none_stop=True) #запуск бота
#         except Exception as e:
#            time.sleep(10) #в случае падения
#            self.bot_log.error(f"Telegram work ERROR: {e}")
