from bot_function import *
from rcon_function import *
from subprocess import check_output
import telebot
import time
import datetime
import math
import os

commands_switch = {'start_server' :["sh sh_scripts/start_server.sh", "time_out_on", "all_users_message_on"],
                   'stop_server'  :["sh sh_scripts/stop_server.sh",  "time_out_on", "all_users_message_on"],
                   'status_server':["sh sh_scripts/status_server.sh","time_out_off","all_users_message_off"]}

rcon_commands_switch = {'send_message'  : [send_message, "send_answer_off"],
                        'players'    : [players,   "send_answer_on"],
                        'server_save': [server_save, "send_answer_on"]}

parameters_filename = 'data/parameters.txt'
file_param = open(parameters_filename, 'r')
lines_param = file_param.readlines()
file_param.close()

parameters_switch = {}
for line in lines_param:
   line = line.split()
   parameters_switch[line[0]] = line[1]

bot = telebot.TeleBot(parameters_switch['tg_token']) #токен бота
time_last_call = datetime.datetime(2011,11,11,11,11)

########BOT HELP########
@bot.message_handler(commands=['start'])
def start_bot(message):
   help_bot(message)

@bot.message_handler(commands=['help'])
def help_bot(message):
   text_str = "SERVER CONTROL\n"
   mass = list(commands_switch.keys())
   for i in mass:
      text_str = text_str + '/' + i + '\n'

   text_str = text_str + "\nRCON COMMAND\n"
   mass = list(rcon_commands_switch.keys())
   for i in mass:
      text_str = text_str + '/' + i + '\n'
   bot.send_message(message.chat.id, text_str)

#####SERVER CONTROL#####
@bot.message_handler(commands=list(commands_switch.keys()))
def control_server(message):
   command_executer(message, commands_switch, parameters_switch, bot, time_last_call)

#######RCON COMMAND#######
@bot.message_handler(commands=list(rcon_commands_switch.keys()))
def rcon_command(message):
   rcon_command_executer(message, rcon_commands_switch, parameters_switch, bot)

#@bot.message_handler(content_types=["text"])

while True:
   try: #добавляем try для бесперебойной работы
      bot.polling(none_stop=True) #запуск бота
   except:
      time.sleep(10) #в случае падения
