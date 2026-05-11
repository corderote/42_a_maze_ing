import random

class Maze:
    def __init__(self, width, height, seed, perfect):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect

        # 1. Configurar la semilla AQUÍ adentro
        if seed is not None:
            random.seed(seed)
        
        # 2. Crear la rejilla inicial: todas las celdas cerradas (valor 15)
        # Es una lista de listas: self.grid[y][x]
        self.grid = [[15 for _ in width] for _ in height]

        # 3. Lista para saber qué celdas hemos visitado (importante para el algoritmo)
        self.visited = [[False for _ in range(width)] for _ in range(height)]

        # Definir las herramientas de "Excavación"

        # Mapeo: Dirección -> (Cambio en X, Cambio en Y, Bit de la pared)
        # Según el sujeto: N=1, E=2, S=4, W=8
        DIRECTIONS = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }
        
        # Para saber qué pared abrir en la celda de destino
        OPPOSITE = {1: 4, 2: 8, 4: 1, 8: 2} # N-S, E-W
        