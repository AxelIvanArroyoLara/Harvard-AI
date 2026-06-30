import sys


class Node():
    def __init__(self, state, parent, action):
        # state representa la posición actual del nodo en el laberinto.
        # Normalmente es una tupla con formato (fila, columna).
        self.state = state

        # parent guarda el nodo desde el cual se llegó a este nodo.
        # Esto permite reconstruir el camino final cuando se encuentra la meta.
        self.parent = parent

        # action representa la acción tomada para llegar a este nodo
        # desde su nodo padre, por ejemplo: "up", "down", "left" o "right".
        self.action = action


# Frontera en forma de stack LIFO
class StackFrontier():
    def __init__(self):
        # Lista que almacenará los nodos pendientes por explorar.
        self.frontier = []

    # Añade elementos al final de la lista frontera
    def add(self, node):
        self.frontier.append(node)

    # Valida si algún elemento en la frontera contiene algún estado particular
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    # Valida si la frontera está vacía
    def empty(self):
        return len(self.frontier) == 0

    # Elimina último elemento
    def remove(self):
        if self.empty():
            raise Exception("Frontera vacía")
        else:
            node = self.frontier[-1]  # Último elemento en la lista
            self.frontier = self.frontier[:-1]  # Remueve último elemento
            return node


# Versión alternativa, hereda de StackFrontier,
# pero funciona como Queue en vez de Stack.
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontera vacía")
        else:
            node = self.frontier[0]  # Retorna el primer elemento ingresado
            self.frontier = self.frontier[1:]  # Elimina el primer elemento
            return node


class Maze():
    def __init__(self, filename):

        # Lee archivo y establece el largo y ancho del laberinto
        with open(filename) as f:
            # Guarda todo el contenido del archivo como una cadena de texto.
            # El archivo representa el laberinto usando caracteres.
            contents = f.read()

        # Valida la existencia y cantidad del punto de partida y la meta
        if contents.count("A") != 1:
            raise Exception("El laberinto debe tener solo un punto de partida")
        if contents.count("B") != 1:
            raise Exception("El laberinto debe tener solo una meta")

        # Retorna la lista de líneas en el archivo
        contents = contents.splitlines()

        # Se establece la altura de acuerdo con el número de líneas
        self.height = len(contents)

        # Se establece el ancho respecto a la línea más larga
        self.width = max(len(line) for line in contents)

        # Mantiene control sobre las paredes del laberinto.
        # self.walls será una matriz de valores booleanos:
        # True  = hay pared
        # False = espacio libre
        self.walls = []

        # Recorre cada fila del laberinto
        for i in range(self.height):

            # Genera una fila para la matriz de paredes
            row = []

            # Recorre cada columna hasta el ancho máximo del laberinto
            for j in range(self.width):
                try:
                    # Si encuentra "A", guarda esa posición como punto de inicio.
                    # Además, marca la celda como transitable, por eso agrega False.
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)

                    # Si encuentra "B", guarda esa posición como meta.
                    # También se marca como celda transitable.
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)

                    # Si encuentra un espacio en blanco, significa que es un camino libre.
                    elif contents[i][j] == " ":
                        row.append(False)

                    # Cualquier otro carácter se considera una pared.
                    else:
                        row.append(True)

                # Algunas líneas pueden ser más cortas que la línea más larga.
                # Si se intenta acceder a una columna que no existe en esa línea,
                # se captura el error y se considera ese espacio como libre.
                except IndexError:
                    row.append(False)

            # Agrega la fila procesada a la matriz general de paredes.
            self.walls.append(row)

        # Aquí se guardará la solución cuando sea encontrada.
        # Inicialmente es None porque todavía no se ha resuelto el laberinto.
        self.solution = None

    def print(self):
        # Si ya existe una solución, se obtiene la lista de posiciones del camino.
        # self.solution normalmente tendrá la forma:
        # (acciones, celdas)
        # Por eso self.solution[1] representa las celdas del camino.
        solution = self.solution[1] if self.solution is not None else None

        print()

        # Recorre cada fila de la matriz de paredes
        for i, row in enumerate(self.walls):

            # Recorre cada columna dentro de la fila actual
            for j, col in enumerate(row):

                # Si col es True, significa que esa celda es una pared.
                if col:
                    print("█", end="")

                # Si la posición actual coincide con el punto de inicio,
                # imprime "A".
                elif (i, j) == self.start:
                    print("A", end="")

                # Si la posición actual coincide con la meta,
                # imprime "B".
                elif (i, j) == self.goal:
                    print("B", end="")

                # Si hay una solución y la celda actual forma parte del camino,
                # imprime "*" para visualizar la ruta encontrada.
                elif solution is not None and (i, j) in solution:
                    print("*", end="")

                # Si no es pared, inicio, meta ni parte de la solución,
                # imprime un espacio vacío.
                else:
                    print(" ", end="")

            # Salto de línea al terminar de imprimir una fila completa.
            print()

        print()