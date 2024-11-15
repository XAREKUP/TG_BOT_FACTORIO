from subprocess import check_output
import telebot
import time
import datetime
import math

bot = telebot.TeleBot("7696433195:AAFAd3PZcijsClJ7aUHtnS_Cjv12cYIvLs0") #токен бота
commands_switch = {"start" :["sh start_server.sh", "time_out_on", "all_users_message_on"],
                   "stop"  :["sh stop_server.sh",  "time_out_on", "all_users_message_on"],
                   "status":["sh status_server.sh","time_out_off","all_users_message_off"]}

time_last_call = datetime.datetime(2011,11,11,11,11)
time_out=10.0



def send_message_id(message, id):
   bot.send_message(id, message)



@bot.message_handler(content_types=["text"])

def main(message):
   global time_last_call
   time_diff = (datetime.datetime.now() - time_last_call).total_seconds()

#   exist_line = False
#   with open('users.txt') as f:
#      for line in f:
#         if ((str(message.from_user.id) + " " + message.from_user.username) == line):
#            exist_line = True

#   if(exist_line == False):
#      users_file = open('users.txt', 'a')
#      users_file.write(str(message.from_user.id) + " " + message.from_user.username)
#      users_file.close()


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

#      try:
#         if(commands_switch[command][2] == "all_users_message_on"):
#            with open('users.txt') as f:
#               for line in f:
#                  data = line.split()
#                  bot.send_message(user_id, data[1])
#                  bot.send_message(int(data[0]), message.from_user.username + ": "+ command)
#      except:
#         pass

if __name__ == '__main__':
    while True:
        try: #добавляем try для бесперебойной работы
            bot.polling(none_stop=True) #запуск бота
        except:
            time.sleep(10) #в случае падения
