from bot_commands import *
from subprocess import check_output
import telebot
import time
import datetime
import math

bot = telebot.TeleBot("TOKEN") #токен бота
commands_switch = {"/start_server" :["sh sh_scripts/start_server.sh", "time_out_on", "all_users_message_on"],
                   "/stop_server"  :["sh sh_scripts/stop_server.sh",  "time_out_on", "all_users_message_on"],
                   "/status_server":["sh sh_scripts/status_server.sh","time_out_off","all_users_message_off"]}

time_last_call = datetime.datetime(2011,11,11,11,11)
time_out=5.0

def command_executer(message):
   global time_last_call
   time_diff = (datetime.datetime.now() - time_last_call).total_seconds()
   if (1 == 1): #проверяем, что пишет именно владелец
      command = message.text  #текст сообщения
      command = command.lower()
      try:
         if(commands_switch[command][1] == "time_out_on"):
            if(time_diff >= time_out):
               bot.send_message(message.chat.id, check_output(commands_switch[command][0], shell = True))
               time_last_call = datetime.datetime.now()
            else:
               bot.send_message(message.chat.id, "Timeout: " + str(round(time_diff, 1)) + "/" + str(time_out))

         else:
            bot.send_message(message.chat.id, check_output(commands_switch[command][0], shell = True))
      except:
         bot.send_message(message.chat.id, 'error: ' + command) #если команда некорректна


########BOT HELP########
@bot.message_handler(commands=['start'])
def start_bot(message):
   help_bot(message)

@bot.message_handler(commands=['help'])
def help_bot(message):
   mass = list(commands_switch.keys())
   text_str = ""
   for i in mass:
      text_str = text_str + i + '\n'
   bot.send_message(message.chat.id, text_str)

#####SERVER CONTROL#####
@bot.message_handler(commands=['status_server'])
def status_server(message):
   command_executer(message)

@bot.message_handler(commands=['start_server'])
def start_server(message):
   command_executer(message)

@bot.message_handler(commands=['stop_server'])
def stop_server(message):
   command_executer(message)

#@bot.message_handler(content_types=["text"])

while True:
   try: #добавляем try для бесперебойной работы
      bot.polling(none_stop=True) #запуск бота
   except:
      time.sleep(10) #в случае падения
