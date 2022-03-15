import paho.mqtt.client as mqtt

TOPIC_GAME = "topic_game"
is_connected = False
game = None
user = None
my_move = None
op_move = None
status = 0

# MQTT
def on_connect(client, userdata, flags, rc):
    global is_connected
    print('connected')
    is_connected = True
    client.subscribe(TOPIC_GAME)

def on_message(client, userdata, msg):
    global game, user, status, my_move, op_move
    data = msg.payload.decode('ascii').split(':')

    if msg.topic == TOPIC_GAME:
        if data[0] == 'NEW_GAME_ACK':
            game = data[1]
            user = data[2]
            client.subscribe(game)
            client.unsubscribe(TOPIC_GAME)
            client.publish(game, 'PLAYERS_READY')
    elif msg.topic == game:
        if data[0] == 'START':
            status = 1
            print(f'Bora jogar! Eu sou o player {user}')
        elif data[0] == 'COMMAND':
            if data[2] == user:
                my_move = data[1]
            else:
                op_move = data[1]
            
            if my_move and op_move:
                my_move = int(my_move)
                op_move = int(op_move)
                if my_move == op_move:
                    print('Empate!')
                elif my_move + op_move == 2:
                    print('Ganhei!' if my_move == 2 else 'Perdi =/')
                elif my_move + op_move == 1:
                    print('Ganhei!' if my_move == 1 else 'Perdi =/')
                elif my_move + op_move == 3:
                    print('Ganhei!' if my_move == 2 else 'Perdi =/')    

# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async("localhost", 1883, 60)
client.loop_start()

while True:
    if is_connected:
        # print('Connected on game')
        if game and status == 1:
            my_move = input('Digite a jogada: (0 = Pedra, 1 = Papel, 2 = Tesoura)')
            client.publish(game, f'COMMAND:{my_move}:{user}')
        elif status == 0:
            op = input('Digite a opção: (1 - New game)')
            if op == '1':
                client.publish(TOPIC_GAME, 'NEW_GAME')
                status = -1
        else:
            print('.', end='')