from rcon.source import Client

rcon_port = 25575
rcon_password = '123'
rcon_ip = '127.0.0.1'

def send_text(text):
   with Client(rcon_ip, rcon_port, passwd = rcon_password) as client:
      response = client.run(text)

def players(text):
   with Client(rcon_ip, rcon_port, passwd = rcon_password) as client:
      response = client.run('/players')
      #print(response)
   return response
