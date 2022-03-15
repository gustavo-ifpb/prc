# Requisitos
* Protocolo MQTT
* Protocolo TCP

# Regras
* 2 players por partida
* Partida 1 rodada
* Player escolhe entre 3 opções: 
** 0 = Pedra
** 1 = Papel
** 2 = Tesoura
* Jogo de turno

# Arquitetura
[servidor]
[salas2x]
[??]  [??]

[servidor]
[salas2x]
[p1]  [??]

[servidor]
[salas2x]
[p1]  [p2]

# Protocolo
## NEW_GAME (player -> server)
Caso não tenha nenhuma sala disponível, o servidor deverá criar uma sala pra mim e retornar o #ID.
Caso tenha uma sala disponível, o servidor deverá retornar o #ID da sala disponível.

## COMMAND:0|1|2:{player} (player -> server)
Essa mensagem indica qual o valor da minha jogada. (0 = Pedra, 1 = Papel, 2 = Tesoura)

## NEW_GAME_ACK:ID (server -> player)
Essa mensagem indica qual o ID da sala disponível.

## PLAYERS_READY (player -> server)

## START (server -> players)
Essa mensagem indica que a partida está pronta para começar.

## RESULT:0|1 (server -> players)
Essa mensagem indica o fim da partida, informando quem ganhou (1) ou quem perdeu (0).