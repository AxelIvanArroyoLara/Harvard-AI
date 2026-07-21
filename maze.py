# ============================================================
# PROGRAMA: RESOLVER UN LABERINTO
#
# El laberinto se lee desde un archivo de texto.
#
# A = punto de inicio
# B = punto de llegada
# " " = espacio por donde se puede caminar
# Cualquier otro carácter = pared
#
# El programa busca un camino desde A hasta B.
# ============================================================


# Importamos sys para leer el nombre del archivo escrito
# en la terminal.
#
# Ejemplo:
# python maze.py maze.txt
#
# En ese caso:
# sys.argv[0] sería "maze.py"
# sys.argv[1] sería "maze.txt"
import sys


# ============================================================
# CLASE NODE
# ============================================================

class Node:
    """
    Un nodo representa una posición visitada durante la búsqueda.

    Guarda tres datos:

    state:
        La posición actual, por ejemplo (3, 5).

    parent:
        El nodo anterior desde el cual llegamos.

    action:
        El movimiento realizado para llegar aquí:
        "up", "down", "left" o "right".
    """

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# Ejemplo de un nodo:
#
# nodo = Node(
#     state=(2, 4),
#     parent=otro_nodo,
#     action="right"
# )
#
# Significa:
# Estamos en la fila 2, columna 4.
# Llegamos desde otro_nodo.
# Para llegar nos movimos hacia la derecha.


# ============================================================
# CLASE STACKFRONTIER
# ============================================================

class StackFrontier:
    """
    La frontera guarda los nodos que todavía faltan explorar.

    Esta frontera funciona como una PILA.

    Una pila sigue la regla:
    último en entrar, primero en salir.

    Ejemplo:

    Agregamos:
    A, B, C

    Sacamos:
    C, B, A

    Esto produce una búsqueda en profundidad:
    DFS, Depth-First Search.
    """

    def __init__(self):
        # Lista donde se guardan los nodos pendientes.
        self.frontier = []

    def add(self, node):
        """
        Agrega un nuevo nodo al final de la lista.
        """
        self.frontier.append(node)

    def contains_state(self, state):
        """
        Comprueba si una posición ya está dentro de la frontera.

        Esto evita agregar varias veces la misma posición.
        """

        # any devuelve True si al menos un nodo cumple la condición.
        return any(
            node.state == state
            for node in self.frontier
        )

    def empty(self):
        """
        Devuelve True si la frontera está vacía.
        """

        return len(self.frontier) == 0

    def remove(self):
        """
        Saca el último nodo agregado.

        Por eso esta estructura es una pila.
        """

        # Si no hay nodos, no podemos sacar ninguno.
        if self.empty():
            raise Exception("empty frontier")

        # [-1] significa: último elemento de la lista.
        node = self.frontier[-1]

        # Conservamos todos los elementos menos el último.
        self.frontier = self.frontier[:-1]

        return node


# ============================================================
# CLASE QUEUEFRONTIER
# ============================================================

class QueueFrontier(StackFrontier):
    """
    Esta clase hereda de StackFrontier.

    Hereda:
    - add
    - contains_state
    - empty

    Solo cambia el método remove.

    Esta frontera funciona como una COLA.

    Una cola sigue la regla:
    primero en entrar, primero en salir.

    Ejemplo:

    Agregamos:
    A, B, C

    Sacamos:
    A, B, C

    Esto produce una búsqueda en anchura:
    BFS, Breadth-First Search.
    """

    def remove(self):
        """
        Saca el primer nodo agregado.
        """

        if self.empty():
            raise Exception("empty frontier")

        # [0] significa: primer elemento de la lista.
        node = self.frontier[0]

        # Conservamos los elementos desde la posición 1.
        # Es decir, eliminamos el primero.
        self.frontier = self.frontier[1:]

        return node


# ============================================================
# CLASE MAZE
# ============================================================

class Maze:
    """
    Esta clase representa todo el laberinto.

    Se encarga de:

    1. Leer el archivo.
    2. Detectar paredes.
    3. Encontrar el inicio A.
    4. Encontrar el objetivo B.
    5. Buscar un camino.
    6. Mostrar la solución.
    """

    def __init__(self, filename):

        # ----------------------------------------------------
        # 1. LEER EL ARCHIVO
        # ----------------------------------------------------

        # Abrimos el archivo.
        with open(filename) as f:
            # Leemos todo el contenido.
            contents = f.read()

        # ----------------------------------------------------
        # 2. COMPROBAR QUE HAYA UN SOLO INICIO Y UN SOLO FINAL
        # ----------------------------------------------------

        # Debe existir exactamente una letra A.
        if contents.count("A") != 1:
            raise Exception(
                "maze must have exactly one start point"
            )

        # Debe existir exactamente una letra B.
        if contents.count("B") != 1:
            raise Exception(
                "maze must have exactly one goal"
            )

        # ----------------------------------------------------
        # 3. CALCULAR ALTO Y ANCHO
        # ----------------------------------------------------

        # splitlines convierte el texto en una lista de líneas.
        #
        # Por ejemplo:
        #
        # "███\n█A█\n█B█"
        #
        # se convierte en:
        #
        # ["███", "█A█", "█B█"]
        contents = contents.splitlines()

        # El alto es la cantidad de filas.
        self.height = len(contents)

        # El ancho es la longitud de la fila más larga.
        self.width = max(
            len(line)
            for line in contents
        )

        # ----------------------------------------------------
        # 4. CREAR LA MATRIZ DE PAREDES
        # ----------------------------------------------------

        # self.walls será una matriz de valores booleanos.
        #
        # True  = hay pared
        # False = se puede caminar
        self.walls = []

        # Recorremos cada fila.
        for i in range(self.height):

            # Aquí construiremos una fila de la matriz.
            row = []

            # Recorremos cada columna.
            for j in range(self.width):

                try:
                    # Revisamos qué carácter hay en la posición
                    # fila i, columna j.

                    if contents[i][j] == "A":
                        # Guardamos la posición inicial.
                        self.start = (i, j)

                        # En A se puede caminar.
                        row.append(False)

                    elif contents[i][j] == "B":
                        # Guardamos la posición final.
                        self.goal = (i, j)

                        # En B se puede caminar.
                        row.append(False)

                    elif contents[i][j] == " ":
                        # Un espacio es un camino libre.
                        row.append(False)

                    else:
                        # Cualquier otro carácter es una pared.
                        row.append(True)

                except IndexError:
                    # Puede ocurrir si alguna fila es más corta
                    # que el ancho máximo.
                    #
                    # En ese caso se agrega un espacio libre.
                    row.append(False)

            # Agregamos la fila terminada a la matriz.
            self.walls.append(row)

        # Al principio todavía no existe una solución.
        self.solution = None


    # ========================================================
    # MÉTODO PRINT
    # ========================================================

    def print(self):
        """
        Muestra el laberinto en la terminal.

        █ = pared
        A = inicio
        B = objetivo
        * = parte de la solución
        """

        # Si ya encontramos una solución,
        # tomamos la lista de celdas del camino.
        if self.solution is not None:
            solution = self.solution[1]
        else:
            solution = None

        print()

        # Recorremos cada fila.
        for i, row in enumerate(self.walls):

            # Recorremos cada columna.
            for j, col in enumerate(row):

                # col será True si hay una pared.
                if col:
                    print("█", end="")

                # Comprobamos si esta posición es el inicio.
                elif (i, j) == self.start:
                    print("A", end="")

                # Comprobamos si esta posición es el objetivo.
                elif (i, j) == self.goal:
                    print("B", end="")

                # Comprobamos si esta posición está
                # dentro del camino encontrado.
                elif (
                    solution is not None
                    and (i, j) in solution
                ):
                    print("*", end="")

                # Si no es nada de lo anterior,
                # mostramos un espacio.
                else:
                    print(" ", end="")

            # Salto de línea después de cada fila.
            print()

        print()


    # ========================================================
    # MÉTODO NEIGHBORS
    # ========================================================

    def neighbors(self, state):
        """
        Devuelve los vecinos válidos de una posición.

        Por ejemplo, desde una celda podemos intentar:

        - subir
        - bajar
        - ir a la izquierda
        - ir a la derecha
        """

        # state es una tupla como (fila, columna).
        row, col = state

        # Creamos los cuatro movimientos posibles.
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Aquí guardaremos únicamente los movimientos válidos.
        result = []

        # Revisamos cada movimiento posible.
        for action, (r, c) in candidates:

            # La nueva posición debe cumplir:
            #
            # 1. La fila debe estar dentro del laberinto.
            # 2. La columna debe estar dentro del laberinto.
            # 3. No debe ser una pared.
            if (
                0 <= r < self.height
                and 0 <= c < self.width
                and not self.walls[r][c]
            ):
                result.append(
                    (action, (r, c))
                )

        return result


    # ========================================================
    # MÉTODO SOLVE
    # ========================================================

    def solve(self):
        """
        Busca un camino desde A hasta B.

        El proceso general es:

        1. Empezar desde A.
        2. Guardar A en la frontera.
        3. Sacar una posición de la frontera.
        4. Comprobar si es B.
        5. Si no es B, agregar sus vecinos.
        6. Repetir.
        """

        # Cuenta cuántos nodos fueron explorados.
        self.num_explored = 0

        # ----------------------------------------------------
        # CREAR EL NODO INICIAL
        # ----------------------------------------------------

        start = Node(
            state=self.start,

            # No tiene padre porque es el primer nodo.
            parent=None,

            # No se realizó ningún movimiento para llegar a él.
            action=None
        )

        # ----------------------------------------------------
        # CREAR LA FRONTERA
        # ----------------------------------------------------

        # StackFrontier hace búsqueda en profundidad, DFS.
        frontier = StackFrontier()

        # Para usar búsqueda en anchura, BFS:
        #
        # frontier = QueueFrontier()

        # Agregamos el nodo inicial.
        frontier.add(start)

        # ----------------------------------------------------
        # CREAR EL CONJUNTO DE EXPLORADOS
        # ----------------------------------------------------

        # Aquí guardaremos las posiciones que ya visitamos.
        self.explored = set()

        # ----------------------------------------------------
        # EMPEZAR LA BÚSQUEDA
        # ----------------------------------------------------

        while True:

            # Si la frontera está vacía,
            # ya no quedan lugares por revisar.
            #
            # Por tanto, el laberinto no tiene solución.
            if frontier.empty():
                raise Exception("no solution")

            # Sacamos un nodo de la frontera.
            node = frontier.remove()

            # Contamos este nodo como explorado.
            self.num_explored += 1

            # ------------------------------------------------
            # COMPROBAR SI LLEGAMOS AL OBJETIVO
            # ------------------------------------------------

            if node.state == self.goal:

                # Guardará los movimientos de la solución.
                actions = []

                # Guardará las posiciones de la solución.
                cells = []

                # En este momento node es el objetivo.
                #
                # Vamos a retroceder usando parent:
                #
                # objetivo -> padre -> padre -> inicio
                while node.parent is not None:

                    # Guardamos el movimiento usado.
                    actions.append(node.action)

                    # Guardamos la posición.
                    cells.append(node.state)

                    # Retrocedemos al nodo anterior.
                    node = node.parent

                # Las listas quedaron al revés:
                #
                # objetivo -> inicio
                #
                # Por eso las invertimos para obtener:
                #
                # inicio -> objetivo
                actions.reverse()
                cells.reverse()

                # Guardamos la solución.
                self.solution = (
                    actions,
                    cells
                )

                # Terminamos el método.
                return

            # ------------------------------------------------
            # MARCAR EL NODO COMO EXPLORADO
            # ------------------------------------------------

            self.explored.add(node.state)

            # ------------------------------------------------
            # REVISAR LOS VECINOS
            # ------------------------------------------------

            for action, state in self.neighbors(node.state):

                # Solo agregamos un vecino si:
                #
                # 1. No está ya en la frontera.
                # 2. No fue explorado antes.
                if (
                    not frontier.contains_state(state)
                    and state not in self.explored
                ):

                    # Creamos un nodo para esa posición.
                    child = Node(
                        state=state,

                        # El nodo actual será su padre.
                        parent=node,

                        # Guardamos el movimiento utilizado.
                        action=action
                    )

                    # Agregamos el vecino a la frontera.
                    frontier.add(child)


    # ========================================================
    # MÉTODO OUTPUT_IMAGE
    # ========================================================

    def output_image(
        self,
        filename,
        show_solution=True,
        show_explored=False
    ):
        """
        Crea una imagen del laberinto.

        show_solution:
            Muestra el camino encontrado.

        show_explored:
            Muestra las posiciones revisadas durante la búsqueda.
        """

        # Importamos Pillow para crear imágenes.
        from PIL import Image, ImageDraw

        # Cada celda medirá 50 x 50 píxeles.
        cell_size = 50

        # Espacio usado para separar visualmente las celdas.
        cell_border = 2

        # Creamos una imagen negra.
        img = Image.new(
            "RGBA",
            (
                self.width * cell_size,
                self.height * cell_size
            ),
            "black"
        )

        # Objeto que permite dibujar sobre la imagen.
        draw = ImageDraw.Draw(img)

        # Obtenemos las celdas de la solución.
        if self.solution is not None:
            solution = self.solution[1]
        else:
            solution = None

        # Recorremos todas las celdas.
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Elegimos el color de cada celda.

                # Pared: gris oscuro.
                if col:
                    fill = (40, 40, 40)

                # Inicio: rojo.
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Objetivo: verde.
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solución: amarillo claro.
                elif (
                    solution is not None
                    and show_solution
                    and (i, j) in solution
                ):
                    fill = (220, 235, 113)

                # Explorados: rojo claro.
                elif (
                    solution is not None
                    and show_explored
                    and (i, j) in self.explored
                ):
                    fill = (212, 97, 85)

                # Camino libre: casi blanco.
                else:
                    fill = (237, 240, 252)

                # Dibujamos un rectángulo para representar la celda.
                draw.rectangle(
                    [
                        (
                            j * cell_size + cell_border,
                            i * cell_size + cell_border
                        ),
                        (
                            (j + 1) * cell_size - cell_border,
                            (i + 1) * cell_size - cell_border
                        )
                    ],
                    fill=fill
                )

        # Guardamos la imagen.
        img.save(filename)


# ============================================================
# CÓDIGO PRINCIPAL
# ============================================================

# Debemos ejecutar el programa indicando un archivo.
#
# Forma correcta:
#
# python maze.py maze.txt
#
# sys.argv debe contener dos elementos:
#
# 1. El nombre del programa.
# 2. El nombre del archivo del laberinto.
if len(sys.argv) != 2:
    sys.exit(
        "Usage: python maze.py maze.txt"
    )


# Creamos el laberinto usando el archivo indicado.
m = Maze(sys.argv[1])


# Mostramos el laberinto antes de resolverlo.
print("Maze:")
m.print()


# Avisamos que comienza la búsqueda.
print("Solving...")


# Buscamos la solución.
m.solve()


# Mostramos cuántos estados fueron explorados.
print(
    "States Explored:",
    m.num_explored
)


# Mostramos el laberinto resuelto.
print("Solution:")
m.print()


# Creamos una imagen llamada maze.png.
#
# show_explored=True permite ver también
# las posiciones que el algoritmo revisó.
m.output_image(
    "maze.png",
    show_explored=True
)
