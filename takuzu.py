# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 33:
# 99216 Filipa Magalhães
# 99275 Mário Santos

import sys
from sys import stdin
import numpy as np
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

    def __str__(self):
        return str(self.id)

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, matrix: np.ndarray, size: int, num_values_row: list,
     num_values_col: list):
        """O construtor especifica o estado inicial."""
        self.matrix = matrix
        self.size = size
        self.num_values_row = num_values_row    # lista de listas
        self.num_values_col = num_values_col    # lista de listas

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

        size = int(stdin.readline())
        matrix = [[0]*size for _ in range(size)]
        num_values_row = np.zeros([size, 3], dtype = int)
        num_values_col = np.zeros([size, 3], dtype = int)
        # num_values_row = np.zeros([size, 2], dtype = int)
        # num_values_col = np.zeros([size, 2], dtype = int)

        for i in range(size):
            j = 0
            line = stdin.readline()
            lineSize = len(line)
            for _ in range(lineSize):
            
                if line[_] in ['0', '1', '2']:
                    value = int(line[_])
                    matrix[i][j] = value
                    # else:
                    #     num_values_row[i][value] += 1
                    #     num_values_col[j][value] += 1
                    num_values_row[i][value] += 1
                    num_values_col[j][value] += 1
                    j += 1
            
        board = Board(matrix, size, num_values_row, num_values_col)
        return board


    def get_board(self, action):
        
        newBoard = Board(self.matrix, self.size, self.num_values_row, self.num_values_col)

        i, j, val = action[0], action[1], action[2]
        
        newMatrix = np.copy(self.matrix)
        newMatrix[i][j] = val

        newSize = np.copy(self.size)

        newValues_row = np.copy(self.num_values_row)
        newValues_row[i][val] += 1
        newValues_row[i][2] -= 1


        newValues_col = np.copy(self.num_values_col)
        newValues_col[j][val] += 1
        newValues_col[j][2] -= 1
        
        newBoard = Board(newMatrix, newSize, newValues_row, newValues_col)
        return newBoard

    # TODO: outros metodos da classe


class Takuzu(Problem):
    
    def __init__(self, board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))
        self.board = board

    def actions(self, state: TakuzuState): 
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        possible_actions = []
        state_board = state.board
        size = state.board.size

        free_positions = []

        for i in range(size):
            for j in range(size):
                if state.board.matrix[i][j] == 2:
                    free_positions += [(i, j)]

        max_num_value = size // 2
        #final_board_rows = state.board.matrix
        #final_board_cols = np.transpose(final_board_rows)

        for pos in free_positions:
            i, j = pos[0], pos[1]
            
        # ----- Completar linha/coluna: -----
            for val in range(2):
                if (size%2 == 0):
                    if (state_board.num_values_row[i][val] == max_num_value or
                        state_board.num_values_col[j][val] == max_num_value):
                        num = abs(val - 1)
                        return [(i, j, num)]
                else:
                    if (state_board.num_values_row[i][val] == max_num_value + 1 or
                        state_board.num_values_col[j][val] == max_num_value + 1):
                        num = abs(val - 1)
                        return [(i, j, num)]

        # ----- Horizontais: -----
            horizontal = state_board.adjacent_horizontal_numbers(i, j)
            #  -> tipo 0 2 0
            if (horizontal[0] == horizontal[1] != 2):
                num = abs(horizontal[0] - 1)
                return [(i, j, num)]

            #  -> tipo (2) 0 0 2 (esquerda)
            if (j+2 < size and state_board.matrix[i][j+1] == state_board.matrix[i][j+2] != 2):
                num = abs(state_board.matrix[i][j+1] - 1)
                return [(i, j, num)]
            #  -> tipo (2) 0 0 2 (direita)
            if (j >= 2 and state_board.matrix[i][j-2] == state_board.matrix[i][j-1] != 2):
                num = abs(state_board.matrix[i][j-1] - 1)
                return [(i, j, num)]
          
        # ----- Verticais: -----
            #  -> tipo 0 2 0
            vertical = state_board.adjacent_vertical_numbers(i, j)
            if (vertical[0] == vertical[1] != 2):
                num = abs(vertical[0] - 1)
                return [(i, j, num)]
            #  -> tipo (2) 0 0 2 (baixo)
            if (i+2 < size and state_board.matrix[i+1][j] == state_board.matrix[i+2][j] != 2):
                num = abs(state_board.matrix[i+1][j] - 1)
                return [(i, j, num)]
            #  -> tipo (2) 0 0 2 (cima)
            if (i >= 2 and state_board.matrix[i-2][j] == state_board.matrix[i-1][j] != 2):
                num = abs(state_board.matrix[i-1][j] - 1)
                return [(i, j, num)]

        # ----- Linhas/Colunas diferentes: -----
            # if (state_board.num_values_row[i][2] == 2):
            #     for row in range(size):
                    
            #         if (size%2 == 0):

            # if (state_board.num_values_col[j][2] == 2):

            possible_actions += [(i, j, 0), (i, j, 1)]
    
        return possible_actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board.get_board(action)

        return TakuzuState(board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        
        size = state.board.size
        
        # -> Alguma posição por preencher?
        for k in range(size):
            if (state.board.num_values_row[k][2] != 0 or
                state.board.num_values_col[k][2] != 0):
                return False

        final_board_rows = state.board.matrix
        final_board_cols = np.transpose(final_board_rows)

        # -> Máx. 2 números iguais adjacentes (vertical e horizontal)?
        # -> #0's = #1's por linha/coluna?
        #       Soma de todas as posições por linha/coluna == size // 2
        #       [Se N é ímpar, pode também ser == (size // 2) + 1]
        sum_values_each = size // 2

        for row in final_board_rows:
            total = np.sum(row)
            if (total == sum_values_each or (size % 2 != 0 and total == sum_values_each + 1)):
                for i in range(2, size):
                    if (row[i-2] == row[i-1] == row[i]):
                        return False
            else:
                return False
        
        for col in final_board_cols:
            total = np.sum(col)
            if (total == sum_values_each or (size % 2 != 0 and total == sum_values_each + 1)):
                for j in range(2, size):
                    if (col[j-2] == col[j-1] == col[j]):
                        return False
            else:
                return False
        
        # -> Linhas/colunas todas diferentes?
        if (len(np.unique(final_board_rows, axis=0)) != size or
            len(np.unique(final_board_cols, axis=0)) != size):
            return False
        
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    #print("Is goal?", problem.goal_test(goal_node.state))
    print(goal_node.state.board, sep="")



    # board = Board.parse_instance_from_stdin()
    # print("Initial:\n", board, sep="")

    # print("\n")

    # takuzu = Takuzu(board)
    # state = TakuzuState(board)
    # while(not takuzu.goal_test(state)):
        
    #     state = TakuzuState(board)
        
    #     actions = takuzu.actions(state)

    #     if len(actions) == 1:
    #         state = takuzu.result(state, actions[0])
    #     else:
    #         #dfs?
    #         pass
    #     print("\n")
    #     print(state.board)
    # print("Is goal?", takuzu.goal_test(state))
    # print("Solution:\n", state.board, sep="")

# EXEMPLO 1 ---------------------------
    # board = Board.parse_instance_from_stdin()
    # print("Initial:\n", board, sep="")
    # print(board.adjacent_vertical_numbers(3, 3))
    # print(board.adjacent_horizontal_numbers(3, 3))
    # print(board.adjacent_vertical_numbers(1, 1))
    # print(board.adjacent_horizontal_numbers(1, 1))

# EXEMPLO 2 ---------------------------
    # board = Board.parse_instance_from_stdin()
    # print("Initial:\n", board, sep="")
    # problem = Takuzu(board)
    # initial_state = TakuzuState(board)
    # print(initial_state.board.get_number(2, 2))
    # result_state = problem.result(initial_state, (2, 2, 1))
    # print(result_state.board.get_number(2, 2))

# EXEMPLO 3 ---------------------------
    # problem = Takuzu(board)
    # s0 = TakuzuState(board)
    # print("Initial:\n", s0.board, sep="")
    # s1 = problem.result(s0, (0, 0, 0))
    # s2 = problem.result(s1, (0, 2, 1))
    # s3 = problem.result(s2, (1, 0, 1))
    # s4 = problem.result(s3, (1, 1, 0))
    # s5 = problem.result(s4, (1, 3, 1))
    # s6 = problem.result(s5, (2, 0, 0))
    # s7 = problem.result(s6, (2, 2, 1))
    # s8 = problem.result(s7, (2, 3, 1))
    # s9 = problem.result(s8, (3, 2, 0))
    # print("Is goal?", problem.goal_test(s9))
    # print("Solution:\n", s9.board, sep="")
    
# EXEMPLO 4 ---------------------------
    #initial_state = TakuzuState(board)

    #print(initial_state.board.get_number(1, 2))
    #result_state = problem.result(initial_state, (1, 2, 1))
    #print(result_state.board.get_number(1, 2))

    #actions = problem.actions(initial_state)
    #print(actions)
    

    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
