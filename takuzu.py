# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self):
        """O construtor especifica o estado inicial."""
        self.matrix = []
        self.size = 0
        pass



    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO

        return self.matrix[row-1][col-1]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        # TODO
        if row < self.size:
            low = self.matrix[row][col-1]
        else:
            low = None

        if row > 1:
            up = self.matrix[row-2][col-1]
        else:
            up = None

        return (low, up)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        if col > 1:
            left = self.matrix[row-1][col-2]
        else:
            left = None

        if col < self.size:
            right = self.matrix[row-1][col]
        else:
            right = None

        return (left, right)

    def printboard(self):

        string = ""
        for i in range(self.size):
            for j in range(self.size):
                string += str(self.matrix[i][j])
                string += "\t"
            string = string[:-1] + "\n"
        print(string, sep="")

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        # TODO
        size = int(stdin.readline()[0])
        matrix = [[0]*size for _ in range(size)]

        for i in range(size):
            j = 0
            line = stdin.readline()
            lineSize = len(line)

            for _ in range(lineSize):
            
                if line[_] in ['0', '1', '2']:
                    matrix[i][j] = int(line[_])
                    j += 1
        
        return matrix

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board()
    board.matrix = board.parse_instance_from_stdin()
    board.size = len(board.matrix)

    board.printboard()
    
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
