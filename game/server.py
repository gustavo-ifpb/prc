import paho.mqtt.client as mqtt
from random import randrange

# Protocolo
'''
[NEW] > [GAME];[ID] - Criar uma partica

[CMD];[ID];[PLY];[NUM] > [RST];[ID];[PLY];[NUM];[-1|0|1] - Palpite
-1 = indica que o número é menor do que NUM
0 = indica que acertou
1 = indica que o número é maior do que NUM
'''

# Topicos
TOPIC_GAME = "game"

# Partidas
'''
games = {
    0 : {
        "number": 100,
        "players": 2
    },
    1 : {
        "number": 10,
        "players": 1
    }
}
'''
games = {}

# MQTT - Metodos
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe(TOPIC_GAME)

# LOGICA JOGO
def on_message(client, userdata, msg):
    data = msg.payload.decode('ascii').split(';')
    print(data)
    
    # Nova partida
    if data[0] == 'NEW':
        game_id, player_id = search_game()
        client.publish(TOPIC_GAME, f'GAME;{game_id};{player_id}')
    elif data[0] == 'CMD':
        game_id = int(data[1])
        player_id = int(data[2])
        hint = int(data[3])
        if hint == games[game_id]['number']:
            client.publish(TOPIC_GAME, f'RST;{game_id};{player_id};{hint};0')
        elif hint > games[game_id]['number']:
            client.publish(TOPIC_GAME, f'RST;{game_id};{player_id};{hint};-1')
        else:
            client.publish(TOPIC_GAME, f'RST;{game_id};{player_id};{hint};1')
            

def search_game():
    key = 0
    for key in games:
        if games[key]['players'] == 1:
            games[key]['players'] = 2
            return key, 2
    # New game
    games[key + 1] = {
        "number": randrange(0, 100),
        "players": 1
    }
    return key + 1, 1


# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()