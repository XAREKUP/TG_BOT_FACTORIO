#!/bin/bash
echo "****************START****************"

sudo wget -O factorio_headless.tar.gz https://www.factorio.com/get-download/2.0.15/headless/linux64
sudo tar -xf factorio_headless.tar.gz
sudo mv factorio /opt
sudo rm factorio_headless.tar.gz

sudo touch /etc/systemd/user/factorio_server.service
echo "[Unit]
Description=Factorio Headless Server

[Service]
Type=simple
ExecStart=/opt/factorio/bin/x64/factorio --start-server /opt/factorio/saves/world.zip  --rcon-port 25575 --rcon-password '123'
" | sudo tee /etc/systemd/user/factorio_server.service

sudo /opt/factorio/bin/x64/factorio --create /opt/factorio/saves/world.zip
sudo chmod 777 /opt/factorio -R
systemctl --user daemon-reload

sudo apt install pip
sudo pip install pytelegrambotapi --break-system-packages

echo "****************END****************"
