# Class/Slot.py
import random

class Slot (object):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
        self.assets = 8
        self.rates = [0.1] * (self.assets - 1) + [0.1]  # 0.1 pour les nombres de 0 à 8, 0.5 pour le nombre 9
        self.board = self.createBoard()

    def createBoard(self):
        board = []
        numbers = list(range(self.assets))

        for _ in range(9):
            row = []
            for _ in range(9):
                num = random.choices(numbers, weights=self.rates, k=1)[0]
                row.append(num)
            board.append(row)
        return board
    
    def checkWin(self):
        def dfs(x, y, visited, current_cluster):
            """ Effectue une recherche en profondeur à partir de la position (x, y). """
            if (x, y) in visited or x < 0 or y < 0 or x >= 9 or y >= 9:
                return
            visited.add((x, y))
            current_cluster.append((x, y))

            number = self.board[x][y]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 9 and 0 <= ny < 9 and self.board[nx][ny] == number:
                    dfs(nx, ny, visited, current_cluster)
        clusters = []
        visited = set()
        for i in range(9):
            for j in range(9):
                if (i, j) not in visited:
                    current_cluster = []
                    dfs(i, j, visited, current_cluster)
                    if len(current_cluster) >= 5:
                        clusters.append(current_cluster)
        return clusters
    
    def removeClusters(self):
        """
        Enlève les nombres au niveau des clusters.
        """
        clusters = self.checkWin()
        for cluster in clusters:
            for x, y in cluster:
                self.board[x][y] = None
    
    def boardDown(self):
        """
        Enlève les nombres au niveau des clusters puis fait descendre les nombres dans le tableau.
        """
        for y in range(9):
            column = [self.board[x][y] for x in range(9) if self.board[x][y] is not None]
            none_count = 9 - len(column)
            for x in range(9):
                if x < none_count:
                    self.board[x][y] = None
                else:
                    self.board[x][y] = column[x - none_count]
    
    def refillBoard(self):
        """
        Remplit le tableau avec des nombres aléatoires.
        """
        for x in range(9):
            for y in range(9):
                if self.board[x][y] is None:
                    self.board[x][y] = random.choices(list(range(self.assets)), weights=self.rates, k=1)[0]

    def __str__(self):
        return f"{self.name} {self.type} {self.value} Board: {self.board}"

    def __repr__(self):
        return f"Slot(name={self.name}, type={self.type}, value={self.value}, board={self.board})"

    def __eq__(self, other):
        if not isinstance(other, Slot):
            return NotImplemented
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __ne__(self, other):
        return not self.__eq__(other)
