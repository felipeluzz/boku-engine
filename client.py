import urllib.request
import sys
import random
import time
from math import inf
import copy

# ---------------------------- Métodos tirados do servidor ---------------------------------

# Returns a list of positions available on a board
def get_available_moves(board, player, forbidden_move):
    l = []

    for column in range(len(board)):
        for line in range(len(board[column])):
            if board[column][line] == 0:
                if not ((column + 1, line + 1) in forbidden_move):
                    l.append((column + 1, line + 1))
    return l

# Check if a board is in an end-game state. Returns the winning player or None.
def is_final_state(board):
    # test vertical
    for column in range(len(board)):
        s = ""
        for line in range(len(board[column])):
            state = board[column][line]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2

    # test upward diagonals
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[1]

    # test downward diagonals
    diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[4]

    return None


# Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left].
# None at any of those places where there's no neighbor
def neighbors(board, column, line):
    l = []

    if line > 1:
        l.append((column, line - 1))  # up
    else:
        l.append(None)

    if (column < 6 or line > 1) and (column < len(board)):
        if column >= 6:
            l.append((column + 1, line - 1))  # upper right
        else:
            l.append((column + 1, line))  # upper right
    else:
        l.append(None)
    if (column > 6 or line > 1) and (column > 1):
        if column > 6:
            l.append((column - 1, line))  # upper left
        else:
            l.append((column - 1, line - 1))  # upper left
    else:
        l.append(None)

    if line < len(board[column - 1]):
        l.append((column, line + 1))  # down
    else:
        l.append(None)

    if (column < 6 or line < len(board[column - 1])) and column < len(board):
        if column < 6:
            l.append((column + 1, line + 1))  # down right
        else:
            l.append((column + 1, line))  # down right
    else:
        l.append(None)

    if (column > 6 or line < len(board[column - 1])) and column > 1:
        if column > 6:
            l.append((column - 1, line + 1))  # down left
        else:
            l.append((column - 1, line))  # down left
    else:
        l.append(None)

    return l

# ---------------------------------------------------

# ---------------- Métodos auxiliares ----------------

def get_board():
    return [
        (1,1), (1,2), (1,3), (1,4), (1,5),
        (2,1), (2,2), (2,3), (2,4), (2,5), (2,6),
        (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),
        (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8),
        (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),
        (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10),
        (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),
        (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8),
        (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7),
        (10,1), (10,2), (10,3), (10,4), (10,5), (10,6),
        (11,1), (11,2), (11,3), (11,4), (11,5)
    ]

# Função que diz o que tem nas diagonais e seus pontos
def teste_diagonais(board_inicial, ponto_inicial, board):

    print('Ponto Atual')
    print(ponto_inicial)
    # Conteúdo das diagonais
    superior_esquerda = []
    superior_direita = []
    inferior_esquerda = []
    inferior_direita = []
    # Pontos das diagonais
    pontos_superior_esquerda = []
    pontos_superior_direita = []
    pontos_inferior_esquerda = []
    pontos_inferior_direita = []

    valid = True
    ponto_atual = ponto_inicial
    # Diagonal superior esquerda
    while valid:
        # Se está no meio do tabuleiro ou na esquerda
        if ponto_atual[0] == 6 or ponto_atual[0] < 6:
            ponto_atual = (ponto_atual[0] - 1, ponto_atual[1] -1)
            if not ponto_atual in board_inicial:
                valid = False
            else:
                superior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_superior_esquerda.append(ponto_atual)
        # Se está na direita do tabuleiro
        elif ponto_atual[0] > 6:
            ponto_atual = (ponto_atual[0] - 1, ponto_atual[1])
            if not ponto_atual in board_inicial:
                valid = False
            else:
                superior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_superior_esquerda.append(ponto_atual)

    valid = True
    ponto_atual = ponto_inicial
    # Diagonal superior direita
    while valid:
        # Se está no meio do tabuleiro ou na direita
        if ponto_atual[0] == 6 or ponto_atual[0] > 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1] -1)
            if not ponto_atual in board_inicial:
                valid = False
            else:
                superior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_superior_direita.append(ponto_atual)
        # Se está na esquerda do tabuleiro
        elif ponto_atual[0] < 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1])
            if not ponto_atual in board_inicial:
                valid = False
            else:
                superior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_superior_direita.append(ponto_atual)

    valid = True
    ponto_atual = ponto_inicial
    # Diagonal inferior esquerda
    while valid:
        # Se está no meio do tabuleiro ou na esquerda
        if ponto_atual[0] == 6 or ponto_atual[0] < 6:
            ponto_atual = (ponto_atual[0] - 1, ponto_atual[1])
            if not ponto_atual in board_inicial:
                valid = False
            else:
                inferior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_inferior_esquerda.append(ponto_atual)
        # Se está na direita do tabuleiro
        elif ponto_atual[0] > 6:
            ponto_atual = (ponto_atual[0] - 1, ponto_atual[1] + 1)
            if not ponto_atual in board_inicial:
                valid = False
            else:
                inferior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_inferior_esquerda.append(ponto_atual)

    valid = True
    ponto_atual = ponto_inicial
    # Diagonal inferior direita
    while valid:
        # Se está no meio do tabuleiro ou na direita
        if ponto_atual[0] == 6 or ponto_atual[0] > 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1])
            if not ponto_atual in board_inicial:
                valid = False
            else:
                inferior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_inferior_direita.append(ponto_atual)
        # Se está na esquerda do tabuleiro
        elif ponto_atual[0] < 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1] + 1)
            if not ponto_atual in board_inicial:
                valid = False
            else:
                inferior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                pontos_inferior_direita.append(ponto_atual)

    print('Superior Esquerda: ')
    print('\t Conteúdo: ' + str(superior_esquerda))
    print('\t Pontos: ' + str(pontos_superior_esquerda))
    print('Superior Direita: ')
    print('\t Conteúdo: ' + str(superior_direita))
    print('\t Pontos: ' + str(pontos_superior_direita))
    print('Inferior Esquerda: ')
    print('\t Conteúdo: ' + str(inferior_esquerda))
    print('\t Pontos: ' + str(pontos_inferior_esquerda))
    print('Inferior Direita: ')
    print('\t Conteúdo: ' + str(inferior_direita))
    print('\t Pontos: ' + str(pontos_inferior_direita))


# ------------- Métodos de tomada de decisão ----------

# Função de heurística básica
def heuristic(board, player):
    # Verifica vertical
    for col in range(0, len(board)):
        if player == "1":
            if board[col].count(1) + board[col].count(0) <= 5:
                if board[col].count(2) + board[col].count(0) >=5:
                    return 10
                else:
                    return -10

        if player == "2":
            if board[col].count(2) + board[col].count(0) <= 5:
                if board[col].count(1) + board[col].count(0) >=5:
                    return -10
                else:
                    return 10

     #TODO verificar as diagonais
    return 0

# Método que faz um minimax com poda alpha beta, e escolhe o próximo movimento
def alpha_beta_pruning(board, depth, player, initial_depth, initial_player, forbidden_move, alpha= -inf, beta = inf):

    # Checa se chegou ao objetivo
    final_state = is_final_state(board)
    if final_state is not None:
        if final_state == 1:
            return -10, board
        else:
            return 10, board

    # Encerra quando descer até uma certa profundidade, neste caso 2
    if depth == initial_depth - 2:
        h = heuristic(board, initial_player)
        return h, board

    # Para o primeiro jogador
    if player == '1':
        best_val = inf
        best_mov = None
        for move in get_available_moves(board, '1', forbidden_move):
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 1
            value, _ = alpha_beta_pruning(board_cpy, depth-1, '2', initial_depth, initial_player, forbidden_move, alpha, beta)
            if best_val > value:
                best_mov = move

            best_val = min(value, best_val)
            beta = min(alpha, best_val)
            if alpha >= beta:
                break
        return best_val, best_mov

    # Para o segundo jogador
    else:
        best_val = -inf
        best_mov = None
        for move in get_available_moves(board, '2', forbidden_move):
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 2
            value, _ = alpha_beta_pruning(board_cpy, depth-1, '1', initial_depth, initial_player, forbidden_move, alpha, beta)
            if best_val < value:
                best_mov = move

            best_val = max(value, best_val)
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
        return best_val, best_mov

# ----------------------------------------------------------------

if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])
if player == 1:
    adversary = 2
else:
    adversary = 1

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
must_remove = False

initial_board = get_board()

while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == 0, o jogo acabou e o cliente perdeu
    if player_turn==0:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        time.sleep(1)

        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        #Pega o tabuleiro completo
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        board = eval(resp.read()) #lista com 11 listas representando cada fileira na vertical (0 vazio, 1 player 1 e 2 player 2)

        # Pega os movimentos proibidos
        forbidden_move = list(set(initial_board) - set(movimentos))

        # Escolhe um movimento com heurística, a não ser que precise remover, se precisar remove aleatóriamente

        movimento = random.choice(movimentos)
        teste_diagonais(initial_board, movimento, board)
        movimento = (10, movimento)

        #if must_remove:
        #    movimento = random.choice(movimentos)
        #    movimento = (0, movimento)
        #    print(movimento)
        #    must_remove = False
        #else:
         #   movimento = alpha_beta_pruning(board, len(movimentos), str(player), len(movimentos), str(player), forbidden_move)
          #  print(movimento)

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
        msg = eval(resp.read())

        # Verifica se deve remover uma peça
        if (msg[0] == 2):
            must_remove = True
        print(msg)

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])

    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)