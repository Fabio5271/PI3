from get_api import * # Funções da get_api.py
from queue import Queue
from collections import deque
from PIL import Image, ImageDraw # Biblioteca que gera o GIF
images = []

pos = int
end_reached = bool
avail_mov = list # lista de adj
visited = [] # lista de visitados
queued = [] # lista dos elementos que foram adicionados à fila
qd_alt = [] # lista dos elementos que foram adicionados à fila alt
dist = {} # dicionário de distâncias
parent = {} # dicionaŕio de nós pai
vert_q = deque() # fila sem fim
dist_cntr = 1 # contador de distância


def move(next_pos, silent = False): # Faz o movimento na api e atualiza os valores no programa local
    global grpid, labrt, pos, end_reached, avail_mov
    resp_movmt = post_movmt(grpid,labrt,next_pos) # faz o mov na api e guarda o retorno no dicionário 'resp_movmt'
    if silent is False:
        print(resp_movmt)
    pos = resp_movmt['pos_atual']
    end_reached = resp_movmt['final']
    avail_mov = resp_movmt['movimentos']


def traverse_node(next_pos):
    global grpid, labrt, pos, end_reached, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    print("traversing {0}".format(next_pos))
    move(next_pos)
    dist_cntr += 1 # aumenta a dist

    for i in avail_mov:
        if i not in visited:
            if i not in queued:
                vert_q.append(i) # põe nó na fila
                queued.append(i)
            dist[i] = dist_cntr # guarda a dist do nó
        if i not in parent:
            parent[i] = pos # guarda o pai do nó

    move(parent[pos], True)
    print("returned to {0}".format(pos))
    dist_cntr -= 1


def search_node(target):
    global grpid, labrt, pos, end_reached, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    print('searching for: {0}'.format(target))
    start_pos = pos
    for i in avail_mov:
        print('looking into {0}'.format(i))
        move(i)
        print("avail_mov: {0}".format(avail_mov))
        dist_cntr += 1 # aumenta a dist
        
        if target in avail_mov:
            print('found {0}!\n'.format(target))
            break

        if parent[target] in avail_mov:
            print('found parent of {0}!'.format(target))
            move(parent[target])
            print()
            dist_cntr += 1
            break
        
        print("not found, going back to {0}".format(start_pos))
        move(start_pos)
        print("avail_mov: {0}\n".format(avail_mov))
        dist_cntr -= 1   


def bfs():
    global grpid, labrt, pos, end_reached, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    while not end_reached:
        if pos not in visited:
            visited.append(pos) # põe nó no dict de visitados
        for i in avail_mov:
            if i not in visited:
                if i not in queued:
                    vert_q.append(i) # põe nó na fila
                    queued.append(i)
                dist[i] = dist_cntr # guarda a dist do nó            
            if i not in parent:
                parent[i] = pos # guarda o pai do nó

        for i in avail_mov:
            next_pos = vert_q.popleft() # pega o próx no da fila
            print("next_pos: {0}\n".format(next_pos))

            if next_pos in avail_mov:
                traverse_node(next_pos)
            else:
                search_node(next_pos)
                traverse_node(next_pos)


##### MAIN #####
print("Labirintos disponíveis: {0}".format(get_labrts()))
labrt = str(get_labrts()[3])
print("Escolhendo labirinto '{0}'".format(labrt))

grpid = 'Hlinha'
print("Iniciando com id '{0}'\n".format(grpid))
resp_iniciar = post_iniciar(grpid, labrt)
print(resp_iniciar)

pos = resp_iniciar['pos_atual']
end_reached = resp_iniciar['final']
avail_mov = resp_iniciar['movimentos'] # lista de adj
       
bfs() # Usa variáveis globais


# print('vert_q: {0}'.format(list(vert_q)))
# print('parent: {0}'.format(parent))

# images[0].save('maze.gif',
#                save_all=True, append_images=images[1:],
#                optimize=False, duration=1, loop=0)