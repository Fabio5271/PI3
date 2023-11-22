from get_api import * # Funções da get_api.py
# from mkimage import * # Funções da mkimage.py
from collections import deque
from sys import exit
all_edges = []

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
        path = find_path(pos)
        print(f"Caminho do começo pro final: {path}") # Mostrar caminho
        show_dist(pos)
        resp_vald = post_vald(grpid, labrt, path)
        print(resp_vald)
        if resp_vald['caminho_valido'] is True:
            print("Caminho validado!!!")
        # print(all_edges)
        # make_img()
        exit(0)
    return


def traverse_node(next_pos): # Entra em next_pos, e depois volta pra onde estávamos
    global pos, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    print(f"traversing {next_pos}")
    move(next_pos, True)
    dist_cntr = dist[pos] # aumenta a dist

    if pos not in visited:
            visited.append(pos)
    for i in avail_mov:
        if i not in visited: # se ainda não estiverem, coloca os nós de avail_mov na fila
            all_edges.append([pos, i])
            if i not in queued:
                vert_q.append(i) # põe o nó na fila
                queued.append(i)
        if i not in dist:
            dist[i] = dist_cntr + 1 # guarda a distância de cada nó
        if i not in parent: # guarda o nó atual como pai dos nós de avail_mov se ainda não tiverem um pai guardado (uma única vez)
            parent[i] = pos 

    move(parent[pos], True)
    print(f"returned to {pos}\n")
    dist_cntr -= 1
    return


def search_node(target):
    global pos, avail_mov, dist_cntr, parent
    print(f'searching for: {target}')

    if parent[target] in avail_mov:
        print(f'found {target}!\n')
        move(parent[target], True) # entra no pai de target
        dist_cntr = dist[pos]
        return
    
    if parent[parent[target]] in avail_mov: # se o pai de target estiver na lista de adj do nó que entramos
        print(f'found parent of {target}!')
        move(parent[parent[target]], True) # entra no pai de target
        move(parent[target], True) # entra no pai de target
        dist_cntr = dist[pos]
        return

    long_search_node(target) # se ainda não encontramos target
    return


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
                move(parent[pos], True)
            j = targ_ancst.index(i)
            while pos is not parent[target]:
                j -= 1
                move(targ_ancst[j], True)
            
            dist_cntr = dist[pos]
    return


def bfs():
    global labrt, pos, end_reached, avail_mov, dist_cntr, visited, queued, vert_q, dist, parent
    while not end_reached:
        next_pos = vert_q.popleft() # pega o próx no da fila
        if next_pos in avail_mov:
            traverse_node(next_pos)
        else:
            search_node(next_pos)
            traverse_node(next_pos)
    return


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
    return


# def make_img():
#     global queued, all_edges, start
#     # nx_graph.add_node(start)
#     # add_net(queued)
#     add_edges(all_edges)
#     nx.draw(nx_graph)
#     # nt = Network()
#     # nt.from_nx(nx_graph)
#     # nt.show('nx.html')
#     # net.show(net.html)


########## MAIN ##########
resp_labrts = get_labrts() # Chama a API uma vez só
print("Labirintos disponíveis:")
for i in resp_labrts: # loop que mostra as opções de labirinto
    print(f"({resp_labrts.index(i)}) {i}")

lab_selector = int(input("Número do labirinto a ser escolhido: ")) # pega o input e converte pra int
labrt = str(get_labrts()[lab_selector])
grpid = 'Hraki'
print(f"Iniciando labirinto '{labrt}' com id '{grpid}'\n")
resp_iniciar = post_iniciar(grpid, labrt)

pos = resp_iniciar['pos_atual'] # Posição atual
start = pos # Nó onde começamos
end_reached = resp_iniciar['final'] # Guarda o valor que a API retorna, que indica se chegamos no final
avail_mov = resp_iniciar['movimentos'] # lista de adjacências do nó atual

dist[start] = 0 # Define a distância do nó inicial como 0
visited.append(pos) # põe nó no dict de visitados
for i in avail_mov:
    all_edges.append([pos, i])
    vert_q.append(i) # põe nó na fila
    queued.append(i)
    dist[i] = dist_cntr # guarda a dist do nó            
    parent[i] = pos # guarda o pai do nó

print(f"Posição inicial: {start}, iniciando BFS\n")

bfs() # Usa variáveis globais