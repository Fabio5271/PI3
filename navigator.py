from get_api import * # Funções da get_api.py
from collections import deque
from PIL import Image, ImageDraw # Biblioteca que gera o GIF
from sys import exit
images = []

##### Variáveis Globais #####
pos = int # Posição atual
start = int # Nó onde começamos
end_reached = bool # Guarda o valor que a API retorna, que indica se chegamos no final
avail_mov = list # lista de adjacências do nó atual
visited = [] # lista de visitados
queued = [] # lista dos elementos que foram adicionados à fila
dist = {} # dicionário de distâncias de cada nó para o começo
parent = {} # dicionaŕio de nós pai
vert_q = deque() # fila de nós a serem percorridos
dist_cntr = 1 # contador de distância


def move(next_pos, silent = False): # Faz o movimento na api e atualiza os valores no programa local
    global grpid, labrt, pos, end_reached, avail_mov, parent
    resp_movmt = post_movmt(grpid,labrt,next_pos) # faz o mov na api e guarda o retorno no dicionário 'resp_movmt'
    if silent is False: # Mostrar o output da API
        print(resp_movmt)
    
    try: # Tratar a exceção que acontece quando fazemos um movimento inválido, o que está no try sempre roda
        pos = resp_movmt['pos_atual']
        end_reached = resp_movmt['final']
        avail_mov = resp_movmt['movimentos']
    except TypeError: # Caso aconteça a exceção que acontece quando fazemos um movimento inválido
        print(f"Erro: {resp_movmt}")
        print(f'parent: {parent}')
        exit(1)

    if end_reached is True: # Quando a API disser que chegamos no final
        print("\nAchamos o final!!!!!!!!\n")
        print(f"Caminho do começo pro final:\n{find_path(pos)}") # Mostrar caminho
        show_dist(pos)
        exit(0)


def traverse_node(next_pos): # Entra em next_pos, e depois volta pra onde estávamos
    global pos, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    print(f"traversing {next_pos}")
    move(next_pos)
    dist_cntr = dist[pos] # aumenta a dist

    for i in avail_mov:
        if i not in visited: # se ainda não estiverem, coloca os nós de avail_mov na fila
            # print(f"{pos} {i}")
            if i not in queued:
                vert_q.append(i) # põe o nó na fila
                queued.append(i)
        if i not in dist:
            dist[i] = dist_cntr + 1 # guarda a distância de cada nó
            # print(f"dist_cntr: {dist_cntr}, i: {i}")
        if i not in parent: # guarda o nó atual como pai dos nós de avail_mov se ainda não tiverem um pai guardado (uma única vez)
            parent[i] = pos 

    move(parent[pos], True)
    print(f"returned to {pos}")
    dist_cntr -= 1


def search_node(target):
    global pos, avail_mov, dist_cntr, parent
    print(f'searching for: {target}')
    start_pos = pos # posição na qual a busca começou
    for i in avail_mov: # loop que entra em todos os nós da lista de adj de start_pos
        print(f'looking into {i}')
        move(i, True) # entra no nó
        dist_cntr = dist[pos]
        print(f"avail_mov: {avail_mov}")
        
        if target in avail_mov: # se target estiver na lista de adj do nó que entramos
            print(f'found {target}!\n')
            return

        if parent[target] in avail_mov: # se o pai de target estiver na lista de adj do nó que entramos
            print(f'found parent of {target}!')
            move(parent[target]) # entra no pai de target
            dist_cntr = dist[pos]
            print()
            return
        
        print(f"not found, going back to {start_pos}")
        move(start_pos) # volta se não achar nada
        dist_cntr = dist[pos]
        print(f"avail_mov: {avail_mov}\n")
    # se ainda não encontramos target:
    long_search_node(target)


def long_search_node(target):
    global pos, parent, start, dist_cntr, dist
    print(f'long searching for: {target}')
    pos_ancst = []
    targ_ancst = []
    x = parent[pos]
    y = parent[target]
    while x is not start:
        pos_ancst.append(x)
        x = parent[x]
    while y is not start:
        targ_ancst.append(y)
        y = parent[y]
    pos_ancst.append(x)
    targ_ancst.append(y)

    for i in pos_ancst:
        if i in targ_ancst:
            while pos is not i:
                move(parent[pos])
            j = targ_ancst.index(i)
            while pos is not parent[target]:
                j -= 1
                move(targ_ancst[j])
            
            dist_cntr = dist[pos]


def bfs():
    global labrt, pos, end_reached, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    while not end_reached:
        if pos not in visited:
            visited.append(pos) # põe nó no dict de visitados
        for i in avail_mov:
            if i not in visited:
                if i not in queued:
                    vert_q.append(i) # põe nó na fila
                    queued.append(i)
            if i not in dist:
                dist[i] = dist_cntr # guarda a dist do nó            
            if i not in parent:
                parent[i] = pos # guarda o pai do nó

        for i in avail_mov:
            next_pos = vert_q.popleft() # pega o próx no da fila
            print(f"next_pos: {next_pos}\n")

            if next_pos in avail_mov:
                traverse_node(next_pos)
            else:
                search_node(next_pos)
                traverse_node(next_pos)


def find_path(pos):       # Encontra o caminho de volta do final pro início utilizando os nós pai
    global parent, start  # e depois o inverte, para retornar o caminho do começo até o final. 
    node = pos            # Como o programa usa BFS, esse método sempre retorna o caminho mais curto.
    path = []

    while node is not start: # loop que guarda o caminho da volta em path
        path.append(node)
        node = parent[node]
    
    path.append(node) # Adiciona o nó do início
    path.reverse()
    return path


def show_dist(pos):
    global dist
    print(f"Distância: {dist[pos]}")
    # for i in dist:
    #     print(f"{i}: {dist[i]}")


########## MAIN ##########
resp_labrts = get_labrts() # Chama a API uma vez só
print("Labirintos disponíveis:")
for i in resp_labrts: # loop que mostra as opções de labirinto
    print(f"({resp_labrts.index(i)}) {i}")

lab_selector = int(input("Número do labirinto a ser escolhido: ")) # pega o input e converte pra int
labrt = str(get_labrts()[lab_selector])
print(f"Escolhendo labirinto '{labrt}'")

grpid = 'Hraki'
print(f"Iniciando com id '{grpid}'\n")
resp_iniciar = post_iniciar(grpid, labrt)
print(resp_iniciar)

pos = resp_iniciar['pos_atual']
start = pos
end_reached = resp_iniciar['final']
avail_mov = resp_iniciar['movimentos'] # lista de adj
dist[start] = 0
       
bfs() # Usa variáveis globais



# images[0].save('maze.gif',
#                save_all=True, append_images=images[1:],
#                optimize=False, duration=1, loop=0)