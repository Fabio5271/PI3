from PIL import Image, ImageDraw
images = []

# Matriz do labirinto, 1 para onde tem parede, e 0 para livre:
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0 ,1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0 ,1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0 ,1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0 ,0, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0 ,0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Variáveis pra renderizar a matriz:
zoom = 20
borders = 6

# Começo e fim do labirinto:
start = 1,1
end = 5,19

def make_step(k):
  for i in range(len(path_m)):
    for j in range(len(path_m[i])): # Escanear a matriz
      if path_m[i][j] == k: # Se acharmos k
        if i>0 and path_m[i-1][j] == 0 and maze[i-1][j] == 0: # Se não tem parede e não anotamos nada nessa posição ainda
          path_m[i-1][j] = k + 1
        if j>0 and path_m[i][j-1] == 0 and maze[i][j-1] == 0: # Se não tem parede e não anotamos nada nessa posição ainda
          path_m[i][j-1] = k + 1
        if i<len(path_m)-1 and path_m[i+1][j] == 0 and maze[i+1][j] == 0: # Se não tem parede e não anotamos nada nessa posição ainda
          path_m[i+1][j] = k + 1
        if j<len(path_m[i])-1 and path_m[i][j+1] == 0 and maze[i][j+1] == 0: # Se não tem parede e não anotamos nada nessa posição ainda
           path_m[i][j+1] = k + 1

def print_m(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print( str(m[i][j]).ljust(2),end=' ') # ljust(2) formata o texto com 2 caracteres, end=' ' faz o print por espaço no final em vez de \n (default no python)
        print() # pula a linha no final de cada matriz 1D dentro de m

def draw_matrix(a,m, the_path = []):
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255)
            r = 0
            if a[i][j] == 1:
                color = (0, 0, 0)
            if i == start[0] and j == start[1]:
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
            if m[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                               fill=(255,0,0))
    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x,y,x1,y1), fill=(255, 0,0), width=5)
    draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0,255,0), width=2)
    images.append(im)

##### MAIN #####
path_m = [] # matriz que vai armazenar o caminho e distâncias:
for i in range(len(maze)):
    path_m.append([]) # Usa append para criar listas vazias dentro de path_m, tornando path_m uma lista de listas (matriz 2D)
    for j in range(len(maze[i])):
        path_m[-1].append(0) # insere j zeros no final da matriz que o for anterior criou; path_m[-1] representa o último item da matriz
i,j = start
path_m[i][j] = 1

k = 0
while path_m[end[0]][end[1]] == 0:
    k += 1
    make_step(k)
    draw_matrix(maze, path_m)


i, j = end
k = path_m[i][j]
the_path = [(i,j)]
while k > 1:
  if i > 0 and path_m[i - 1][j] == k-1:
    i, j = i-1, j
    the_path.append((i, j))
    k-=1
  elif j > 0 and path_m[i][j - 1] == k-1:
    i, j = i, j-1
    the_path.append((i, j))
    k-=1
  elif i < len(path_m) - 1 and path_m[i + 1][j] == k-1:
    i, j = i+1, j
    the_path.append((i, j))
    k-=1
  elif j < len(path_m[i]) - 1 and path_m[i][j + 1] == k-1:
    i, j = i, j+1
    the_path.append((i, j))
    k -= 1
  draw_matrix(maze, path_m, the_path)

for i in range(10):
    if i % 2 == 0:
        draw_matrix(maze, path_m, the_path)
    else:
        draw_matrix(maze, path_m)

print_m(path_m)
print("\nCaminho da volta: ")
print(the_path)


images[0].save('maze.gif',
               save_all=True, append_images=images[1:],
               optimize=False, duration=1, loop=0)