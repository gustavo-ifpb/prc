import paho.mqtt.client as mqtt

TOPIC_GAME = "topic_game"

'''
{ 'id': 0, 'players': 0 }
'''
games = []

# MQTT
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe(TOPIC_GAME)

def on_message(client, userdata, msg):
    print(userdata)
    data = msg.payload.decode('ascii').split(':')
    print(data)

    if msg.topic == TOPIC_GAME:
        if data[0] == 'NEW_GAME':
            print('Criar uma nova partida')
            topic, created = new_game(client)
            client.publish(TOPIC_GAME, f'NEW_GAME_ACK:{topic}:{0 if created else 1}')
            print(games)
            if not created:
                # Sala completa
                client.subscribe(str(topic))
    else:
        if data[0] == 'PLAYERS_READY':
            client.publish(msg.topic, 'START')

def new_game(client):
    for game in games:
        if game['players'] == 1:
            game['players'] += 1
            return game['id'], False
    topic = len(games)
    games.append({ 'id': topic, 'players': 1 })
    return topic, True

# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()