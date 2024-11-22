#!/bin/bash
echo "****************START****************"

# Установка зависимостей
sudo apt install pip
sudo pip install pytelegrambotapi --break-system-packages
sudo pip install rcon --break-system-packages

# Запрос значений параметров у пользователя
read -p "Enter your Telegram token: " tg_token
http_code=$(curl -o /dev/null 2>/dev/null -w '%{http_code}\n' https://api.telegram.org/bot${tg_token}/getMe)

if [ "$http_code" = "200" ]; then
    echo "The Telegram token is correct"
else
    echo "There is something wrong with the token. Code: ${http_code}"
fi

read -p "Enter the waiting time (in seconds) [5]: " time_out
time_out=${time_out:-5}

read -p "Enter the name of the bot's user data file [users.txt]: " users_filename
users_filename=${time_out:-users.txt}

#read -p "IP-адрес для RCON: " rcon_ip

read -p "Enter the password for RCON: " rcon_password

read -p "Enter the port for RCON [25555]: " rcon_port
rcon_port=${rcon_port:-25555}

while true; do
   #echo "Would you like to on S3 backup saves? (yes or no)"

   read -p "Would you like to on S3 backup saves (yes or no): " s3_on_off

   if [ "$s3_on_off" = "yes" ]; then
       echo "S3 command on."
       s3_on_off='yes'
       break

   elif [ "$s3_on_off" = "no" ]; then
       echo "S3 command off."
       s3_on_off='no'
       break
   else
       echo "Please, print yes or no"
   fi
done

if [ "$s3_on_off" = "yes" ]; then
   read -p "Enter the aws key ID: " aws_key_id
   read -p "Enter the aws secret key: " aws_secret_key
   read -p "Enter the bucket name: " bucket_name
   #read -p "Enter the zone: " zone
else
   aws_key_id=$("no")
   aws_secret_key=$("no")
   bucket_name=$("no")
   zone=$("no")
fi

# Сохранение параметров в файл
echo "tg_token ${tg_token}" > ./data/parameters.txt
echo "time_out ${time_out}" >> ./data/parameters.txt
echo "users_filename ./data/${users_filename}" >> ./data/parameters.txt
#echo "rcon_ip ${rcon_ip}" >> ./parameters.txt
echo "rcon_port ${rcon_port}" >> ./data/parameters.txt

echo "rcon_password ${rcon_password}" >> ./data/parameters.txt
echo "aws_key_id ${aws_key_id}" >> ./data/parameters.txt
echo "aws_secret_key ${aws_secret_key}" >> ./data/parameters.txt
echo "bucket_name ${bucket_name}" >> ./data/parameters.txt
#echo "zone ${zone}" >> ./data/parameters.txt


# Установка Factorio
version=$(curl -s https://factorio.com/download/sha256sums/ | grep factorio_linux | head -n 1 | grep factorio_linux | grep -oP '[0-9]*\.[0-9]*\.[0-9]*')
actual_verison_url='https://factorio.com/get-download/'$version'/headless/linux64'
sudo wget -O factorio_headless.tar.gz $actual_verison_url
sudo tar -xf factorio_headless.tar.gz
sudo mv factorio /opt
sudo rm factorio_headless.tar.gz

# Создание директории для модов
sudo mkdir /opt/factorio/mods

# Изменение прав доступа к папке Factorio
sudo chmod 777 /opt/factorio -R

# Настройка сервера Factorio
sudo touch /etc/systemd/user/factorio_server.service
echo "[Unit]
Description=Factorio Headless Server

[Service]
Type=simple
ExecStart=/opt/factorio/bin/x64/factorio --start-server /opt/factorio/saves/world.zip  --rcon-port ${rcon_port} --rcon-password '${rcon_password}'
" | sudo tee /etc/systemd/user/factorio_server.service

# Cоздание мира
/opt/factorio/bin/x64/factorio --create /opt/factorio/saves/world.zip

# Перезагрузка демона systemd
systemctl --user daemon-reload

echo "****************END****************"
