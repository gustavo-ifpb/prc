import time
import paho.mqtt.client as mqtt

# Topicos
TOPIC_GAME = "game"

# Variveis
is_connected = False
game_id = None
player_id = None

def check_result(data):
    if data[4] == '0':
        return 'Você ganhou!'
    elif data[4] == '1':
        return f'O número é maior {data[3]}'
    else:
        return f'O número é menor {data[3]}'

# MQTT - Metodos
def on_connect(client, userdata, flags, rc):
    global is_connected

    is_connected = True
    client.subscribe(TOPIC_GAME)

    client.publish(TOPIC_GAME, 'NEW')

def on_message(client, userdata, msg):
    global game_id
    global player_id

    data = msg.payload.decode('ascii').split(';')
    print(data)

    if not game_id and data[0] == 'GAME':
        game_id = data[1]
        player_id = data[2]
    elif game_id and data[0] == 'GAME':
        hint = input('Qual o número? ')
        client.publish(TOPIC_GAME, f'CMD;{game_id};{player_id};{hint}')

    elif data[0] == 'RST' and data[1] == game_id:
        if data[2] == player_id:
            print( check_result(data) )
        else:
            if data[4] == '0':
                print('Você perdeu!')
                return None
            elif data[4] == '1':
                print(f'O número é maior {data[3]}')
            else:
                print(f'O número é menor {data[3]}')
            hint = input('Qual o número? ')
            client.publish(TOPIC_GAME, f'CMD;{game_id};{player_id};{hint}')
            



# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()

# while not is_connected:
#     print('.')
#     time.sleep(1)

# while True:
#     op = input('O que deseja fazer? [0] Novo partida [1] Sair')
#     if op == '0'.strip():
#         client.publish(TOPIC_GAME, 'NEW')