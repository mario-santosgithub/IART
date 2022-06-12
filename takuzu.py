# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 33:
# 99216 Filipa Magalhães
# 99275 Mário Santos

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
    def __init__(self, matrix: list, size: int):
        """O construtor especifica o estado inicial."""
        self.matrix = matrix
        self.size = size
    
    def __str__(self):
        """Retorna a string equivalente à representação externa
            do tabuleiro."""
        string = ""
        for i in range(self.size):
            for j in range(self.size):
                string += str(self.matrix[i][j])
                string += "\t"
            string = string[:-1] + "\n"

        return string[:-1]
        #print(string, sep="")

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""

        return self.matrix[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
    
        if row < self.size - 1:
            low = self.matrix[row+1][col]
        else:
            low = None

        if row > 0:
            up = self.matrix[row-1][col]
        else:
            up = None

        return (low, up) 

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
    
        if col > 0:
            left = self.matrix[row][col-1]
        else:
            left = None

        if col < self.size - 1:
            right = self.matrix[row][col+1]
        else:
            right = None

        return (left, right)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

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
        
        board = Board(matrix, size)
        return board

    # TODO: outros metodos da classe


class Takuzu(Problem):
    
    def __init__(self, board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def actions(self, takuzuState): 
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        possible_actions = []

        size = len(self.board.matrix)
        for i in range(1, size+1):
            for j in range(1, size+1):
                # horizontais do tipo 0 2 0
                horizontal = takuzuState.board.adjacent_horizontal_numbers(i, j)
                if (horizontal[0] != 2) and (horizontal[0] == horizontal[1]) and is_empty(takuzuState, i, j):
                    num = abs(horizontal[0] - 1)
                    possible_actions += [(i, j, num)]

                #horizontais do tipo 2 0 0 2 (esquerda)
                if (horizontal[0] == 2 and takuzuState.board.get_number(i,j) == horizontal[1] and horizontal[1] != 2):
                    num = abs(horizontal[1] - 1)
                    possible_actions += [(i, j-1, num)]
                #horizontais do tipo 2 0 0 2 (direita)
                if (horizontal[1] == 2 and takuzuState.board.get_number(i,j) == horizontal[0] and horizontal[0] != 2):
                    num = abs(horizontal[0] - 1)
                    possible_actions += [(i, j+1, num)]

                # verticais do tipo 0 2 0
                vertical = takuzuState.board.adjacent_vertical_numbers(i, j)
                if (vertical[0] != 2) and (vertical[0] == vertical[1]) and (takuzuState.board.get_number(i,j) == 2):
                    num = abs(vertical[0] - 1)
                    possible_actions += [(i, j, num)]

                #verticais do tipo 2 0 0 2 (cima)
                if (vertical[1] == 2 and takuzuState.board.get_number(i,j) == vertical[0] and vertical[0] != 2):
                    num = abs(vertical[0] - 1)
                    possible_actions += [(i-1, j, num)]

                #verticais do tipo 2 0 0 2 (baixo)
                if (vertical[0] == 2 and takuzuState.board.get_number(i,j) == vertical[1] and vertical[1] != 2):
                    num = abs(vertical[1] - 1)
                    possible_actions += [(i+1, j, num)]
                    
        return possible_actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        state.board.matrix[action[0]][action[1]] = action[2]
        
        return state

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

    def is_empty(self, board: Board, row: int, col: int):
        """Verifica se certa posição está ainda por preencher (True)."""
        return board.get_number(row, col) == 2

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:

    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")
    
    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(initial_state.board.get_number(1, 2))

    result_state = problem.result(initial_state, (1, 2, 1))

    print(result_state.board.get_number(1, 2))

    #actions = takuzu.actions(takuzuState)

    #print(actions)

    #for i in range(0, 4):
    #    for j in range(0,4):
    #        print(i+1, j+1)
    #        print(board.adjacent_horizontal_numbers(i+1, j+1))



    
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
