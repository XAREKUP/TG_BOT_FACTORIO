from subprocess import check_output
import telebot
import time
import datetime
import math
import os

def collect_data_user(message, tg_bot_self):
   users_filename = tg_bot_self.parameters_switch['users_filename']
   if(os.path.isfile(users_filename) == False):
      with open(users_filename, 'w') as fp:
         pass

   file_str = open(users_filename, 'r')
   lines = file_str.readlines()
   #tg_bot_self.bot.send_message(message.chat.id, str(lines))
   file_str.close()

   str_user = str(message.chat.id) + ' ' + message.from_user.first_name \
              + ' ' + message.from_user.last_name + ' ' +message.from_user.username + '\n'

   #tg_bot_self.bot.send_message(message.chat.id, str_user)
   if((str_user in lines) == False):
      file_str = open(users_filename, 'a')
      file_str.write(str_user)
      file_str.close()

def rcon_command_executer(message, tg_bot_self):
   collect_data_user(message, tg_bot_self)

   tg_bot_self.bot.send_message(message.chat.id, 'rcon')
   command = message.text[1::].split()
   #tg_bot_self.bot.send_message(message.chat.id, message.from_user.username + ": " + ' '.join(command[1::]))
   response = tg_bot_self.rcon_commands_switch[command[0]][0](message.from_user.username + ": " + ' '.join(command[1::]), tg_bot_self.parameters_switch)

   if(tg_bot_self.rcon_commands_switch[command[0]][1] == "send_answer_on"):
      tg_bot_self.bot.send_message(message.chat.id, response)

def command_executer(message,  tg_bot_self):
   collect_data_user(message, tg_bot_self)

   time_diff = (datetime.datetime.now() - tg_bot_self.time_last_call).total_seconds()
   #tg_bot_self.bot.send_message(message.chat.id, str(time_diff))
   time_out = int(tg_bot_self.parameters_switch['time_out'])

   if (1 == 1): #проверяем, что пишет именно владелец
      command = message.text[1::]  #текст сообщения
      command = command.lower()

      if(tg_bot_self.commands_switch[command][1] == "time_out_on"):
         if(time_diff >= time_out):
            tg_bot_self.bot.send_message(message.chat.id, check_output(tg_bot_self.commands_switch[command][0], shell = True))
            #tg_bot_self.bot.send_message(message.chat.id,str(tg_bot_self.time_last_call))
            tg_bot_self.time_last_call = datetime.datetime.now()
            #tg_bot_self.bot.send_message(message.chat.id,str(tg_bot_self.time_last_call))
         else:
            tg_bot_self.bot.send_message(message.chat.id, "Timeout: " + str(round(time_diff, 1)) + "/" + str(time_out))
      else:
         tg_bot_self.bot.send_message(message.chat.id, check_output(tg_bot_self.commands_switch[command][0], shell = True))

      users_filename = tg_bot_self.parameters_switch['users_filename']
      if(tg_bot_self.commands_switch[command][2] == "all_users_message_on" and \
         not (tg_bot_self.commands_switch[command][1] == "time_out_on" and time_diff < time_out)):
         file_str = open(users_filename, 'r')
         lines = file_str.readlines()
         #tg_bot_self.bot.send_message(message.chat.id, str(lines))
         file_str.close()

         for line in lines:
            id = int(line.split()[0])
            if(id == id): #!= message.chat.id):
               str_text = message.from_user.username + ": " + command
               tg_bot_self.bot.send_message(id, str_text)
