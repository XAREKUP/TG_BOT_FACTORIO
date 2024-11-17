#!/bin/bash
echo "****************START****************"

# Установка зависимостей
sudo apt install unzip
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


read -p "Enter the waiting time (in seconds): " time_out
read -p "Enter the name of the bot's user data file: " users_filename
#read -p "IP-адрес для RCON: " rcon_ip
read -p "Enter the password for RCON: " rcon_password
read -p "Enter the port for RCON: " rcon_port

# Сохранение параметров в файл
echo "tg_token ${tg_token}" > ./data/parameters.txt
echo "time_out ${time_out}" >> ./data/parameters.txt
echo "users_filename ./data/${users_filename}" >> ./data/parameters.txt
#echo "rcon_ip ${rcon_ip}" >> ./parameters.txt
echo "rcon_password ${rcon_password}" >> ./data/parameters.txt
echo "rcon_port ${rcon_port}" >> ./data/parameters.txt

# Установка Factorio
sudo wget -O factorio_headless.tar.gz https://factorio.com/get-download/stable/headless/linux64
sudo tar -xf factorio_headless.tar.gz
sudo mv factorio /opt
sudo rm factorio_headless.tar.gz

# Создание директории для модов
sudo mkdir /opt/factorio/mods

# Изменение прав доступа к папке Factorio
sudo chmod 777 /opt/factorio -R

# Распаковка бота
#wget https://github.com/XAREKUP/TG_BOT_FACTORIO/archive/refs/heads/main.zip
#unzip main.zip -d ./tg_bot_factorio
#rm main.zip

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
