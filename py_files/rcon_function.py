from rcon.source import Client

rcon_ip = '127.0.0.1'

def send_text(text, parameters_switch):
   with Client(rcon_ip, int(parameters_switch['rcon_port']), passwd = parameters_switch['rcon_password']) as client:
      response = client.run(text)

def players(text, parameters_switch):
   with Client(rcon_ip, int(parameters_switch['rcon_port']), passwd = parameters_switch['rcon_password']) as client:
      response = client.run('/players')
      #print(response)
   return response
