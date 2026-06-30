import sys
from constants import NORTH, EAST, SOUTH, WEST, MOVE


class MazeSolver:
    def __init__(self, maze_file: str):
        self.maze_file = maze_file
        self.grid = {}        # Matriz en memoria: {(x, y): valor_muros}
        self.width = 0
        self.height = 0
        self.start = (0, 0)
        self.exit = (0, 0)

        self.load_maze_from_file()

    def load_maze_from_file(self) -> None:
        """
        Lee el archivo de texto del laberinto puro y lo carga en memoria.
        """
        try:
            with open(self.maze_file, 'r') as f:
                # Leemos todas las líneas eliminando espacios en blanco y saltos de línea vacíos
                lines = [line.strip() for line in f.readlines() if line.strip()]

            # Las dos últimas líneas son la entrada y la salida
            matrix_lines = lines[:-2]
            start_line = lines[-2]
            exit_line = lines[-1]

            # Calculamos las dimensiones directamente del texto del laberinto
            self.height = len(matrix_lines)
            self.width = len(matrix_lines[0]) if self.height > 0 else 0

            # Reconstruimos la cuadrícula cargando los valores hexadecimales
            for y, line in enumerate(matrix_lines):
                for x, char in enumerate(line):
                    # int(char, 16) convierte el carácter 'A'-'F' o '0'-'9' a su entero decimal (0-15)
                    self.grid[(x, y)] = int(char, 16)
            
            # Parseamos la entrada y salida (limpiando posibles comas o espacios)
            start_clean = start_line.replace(',', ' ').split()
            exit_clean = exit_line.replace(',', ' ').split()

            self.start = (int(start_clean[0]), int(start_clean[1]))
            self.exit = (int(exit_clean[0]), int(exit_clean[1]))

            print(f"📖 Laberinto cargado con éxito de '{self.maze_file}'")
            print(f"   Dimensiones detectadas: {self.width}x{self.height}")
            print(f"   Punto de Entrada: {self.start} | Punto de Salida: {self.exit}")

        except Exception as e:
            print(f"❌ Error al leer el archivo del laberinto: {e}")
            sys.exit(1)

    def solve(self) -> list:
        """
        Encuentra el camino más corto desde la entrada hasta la salida usando BFS.
        Devuelve una lista de tuplas con las coordenadas del camino.
        """
        # La lista de direcciones a revisar, usando tus constantes
        directions_to_check = [NORTH, EAST, SOUTH, WEST]

        # La cola de exploración guarda: (posición_actual, camino_recorrido_hasta_aquí)
        queue = [(self.start, [self.start])]

        # Conjunto para no volver a pisar celdas ya visitadas por el BFS
        visited = {self.start}

        while queue:
            current_pos, path = queue.pop(0)
            x, y = current_pos

            # ¡Si llegamos a la salida, hemos terminado! Devolvemos el camino óptimo
            if current_pos == self.exit:
                return path

            # Miramos qué muros tiene la celda actual en la matriz
            walls = self.grid[(x, y)]

            # Revisamos las 4 direcciones posibles usando tus constantes
            for direction in directions_to_check:
                # Si el bit de la pared está en 0, significa que el camino está ABIERTO
                if not (walls & direction):
                    # Usamos tu diccionario MOVE para calcular la posición del vecino
                    dx, dy = MOVE[direction]
                    nx, ny = x + dx, y + dy
                    neighbor = (nx, ny)

                    # Si el vecino no ha sido visitado y existe en el mapa, avanzamos
                    if neighbor not in visited and (nx, ny) in self.grid:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

        print("❌ No se encontró ningún camino para resolver el laberinto.")
        return []

    def rewrite_output_file_coord(self, best_path: list) -> None:
        """
        Añade las coordenadas del camino de resolución (best_path)
        al final del archivo de texto del laberinto.
        """
        if not best_path:
            print("No path to print")
            return
        try:
            with open(self.maze_file, "a") as f:
                f.write("\n")
                for x, y in best_path:
                    f.write(f"({x}, {y})")
        except IOError as e:
            print(f"❌ Error writing output file: {e}")

    def write_hex_path(self, best_path: list) -> None:
        """
        Añade los valores hexadecimales del camino óptimo en una sola línea
        al final del archivo del laberinto.
        """
        if not best_path:
            print("No path to print")
            return
        try:
            hex_chars = []
            for pos in best_path:
                wall_value = self.grid[pos]
                hex_c = f"{wall_value:X}"
                hex_chars.append(hex_c)
            solution = "".join(hex_chars)
            with open(self.maze_file, "a") as f:
                f.write("\n")
                f.write(solution)
        except IOError as e:
            print(f"❌ Error al escribir la solución en el archivo: {e}")
        except Exception as e:
            print(f"General error in write_hex_path: {e}")

    def append_solution_path(self, best_path: list) -> None:
        """
        Añade al final del archivo la secuencia de pasos
        (N, E, S, W) que forman el camino más corto.
        """
        if not best_path:
            print("No path to print")
            return
        try:
            with open(self.maze_file, "a") as f:
                solution_path = ""

                for i in range(len(best_path) - 1):
                    x, y = best_path[i]
                    x_next, y_next = best_path[i + 1]

                    dx = x_next - x
                    dy = y_next - y

                    if dx == 1:
                        solution_path += "E"
                    elif dx == -1:
                        solution_path += "W"
                    elif dy == 1:
                        solution_path += "S"
                    elif dy == -1:
                        solution_path += "N"
                f.write("\n")
                f.write(solution_path)
        except IOError as e:
            print(f"❌ Error al escribir la solución en el archivo: {e}")
        except Exception as e:
            print(f"General error in write_hex_path: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python solver.py <archivo_laberinto.txt>")
        sys.exit(1)

    solver = MazeSolver(sys.argv[1])

    # ¡Calculamos la solución!
    camino_optimo = solver.solve()

    if camino_optimo:
        print(f"🎉 ¡Laberinto resuelto en {len(camino_optimo)} pasos!")
        print("El camino es:", camino_optimo)
