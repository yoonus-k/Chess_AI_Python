import copy, math, random

from const import *
from board import *


class AI:
    def __init__(self, engine="book", depth=2):
        self.engine = engine
        self.depth = depth
        self.book = Book()
        self.color = "black"
        self.game_moves = []
        self.explored = 0
        self.explored_without = 0

    # ----
    # BOOK
    # ----

    def book_move(self):
        move = self.book.next_move(self.game_moves, weighted=True)
        return move

    # -------
    # MINIMAX
    # -------

    def heatmap(self, piece, row, col):
        hmp = 0
        if piece.name == "pawn":
            if piece.color == "black":
                hmp = [
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
                    [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
                    [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
                    [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
                    [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
                    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
                    [9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00],
                ]
            elif piece.color == "white":
                hmp = [
                    [9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00],
                    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
                    [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
                    [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
                    [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
                    [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
                    [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                ]

        elif piece.name == "knight":
            hmp = [
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
                [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
                [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
                [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
                [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
                [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        elif piece.name == "bishop":
            hmp = [
                [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
                [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
                [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
                [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
                [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
                [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
                [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
                [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
            ]

        elif piece.name == "king":
            if piece.color == "black":
                hmp = [
                    [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
                    [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                ]

            elif piece.color == "white":
                hmp = [
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
                    [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
                ]

        else:
            hmp = [
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        eval = -hmp[row][col] if piece.color == "black" else hmp[row][col]
        return eval

    def threats(self, board, piece):
        eval = 0
        for move in piece.moves:
            attacked = board.squares[move.final.row][move.final.col]
            if attacked.has_piece():
                if attacked.piece.color != piece.color:
                    # checks
                    if attacked.piece.name == "king":
                        eval += attacked.piece.value / 10500

                    # threat
                    else:
                        eval += attacked.piece.value / 45

        return eval

    # heuristic evaluation function
    def static_eval(self, board):
        # var
        eval = 0

        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    # piece
                    piece = board.squares[row][col].piece
                    # white - black
                    eval += piece.value
                    # heatmap
                    eval += self.heatmap(piece, row, col)
                    # moves
                    if piece.name != "queen":
                        eval += 0.01 * len(piece.moves)
                    else:
                        eval += 0.003 * len(piece.moves)
                    # checks
                    eval += self.threats(board, piece)

        eval = round(eval, 5)
        return eval

    def get_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_team_piece(color):
                    board.calc_moves(square.piece, square.row, square.col)
                    moves += square.piece.moves

        return moves

    def minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0:
            return self.static_eval(board), None  # eval, move

        # white
        if maximizing:
            best_move = None
            max_eval = -math.inf
            moves = self.get_moves(board, "white")
            for move in moves:
                self.explored += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth - 1, False, alpha, beta)[
                    0
                ]  # eval, mov
                if eval > max_eval:
                    max_eval = eval
                    best_move = move or max_eval

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break

            if best_move is not None and not best_move:
                best_move = moves[0]

            return max_eval, best_move  # eval, move

        # black
        elif not maximizing:
            best_move = None
            min_eval = math.inf
            moves = self.get_moves(board, "black")
            for move in moves:
                self.explored += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth - 1, True, alpha, beta)[
                    0
                ]  # eval, move
                if eval < min_eval:
                    min_eval = eval
                    if (move is not None) and (min_eval is not None):
                        best_move = move or min_eval

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break

            if best_move is not None and not best_move:
                idx = random.randrange(0, len(moves))
                best_move = moves[idx]

            return min_eval, best_move  # eval, move

    def minimax_without(self, board, depth, maximizing):
        if depth == 0:
            return self.static_eval(board), None  # eval, move

        # white
        if maximizing:
            max_eval = -math.inf
            moves = self.get_moves(board, "white")
            for move in moves:
                self.explored_without += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax_without(temp_board, depth - 1, False)[
                    0
                ]  # eval, mov
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

            if not best_move:
                best_move = moves[0]

            return max_eval, best_move  # eval, move

        # black
        elif not maximizing:
            min_eval = math.inf
            moves = self.get_moves(board, "black")
            for move in moves:
                self.explored_without += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax_without(temp_board, depth - 1, True)[
                    0
                ]  # eval, move
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

            if not best_move:
                idx = random.randrange(0, len(moves))
                best_move = moves[idx]

            return min_eval, best_move  # eval, move

    # ---------
    # MAIN EVAL
    # ---------

    def eval(self, main_board):
        self.explored = 0
        self.explored_without = 0

        # add last move
        last_move = main_board.last_move
        self.game_moves.append(last_move)

        # book engine
        if self.engine == "book":
            move = self.book_move()

            # no more book moves ?
            if move is None:
                self.engine = "minimax"

        # minimax engine
        if self.engine == "minimax":
            # printing
            print("\nFinding best move...")

            # minimax initial call
            eval, move = self.minimax(
                main_board, self.depth, False, -math.inf, math.inf
            )  # eval, move
            # eval, move_without = self.minimax_without(main_board, self.depth, False)

            # printing
            print("\n- Initial eval:", self.static_eval(main_board))
            print("- Final eval:", eval)
            print("the best move is:", move.__str__)
            print("- Boards explored", self.explored)
            print("- Boards explored without", self.explored_without)
            if self.explored != 0:
                print(
                    "optimization:",
                    ((self.explored_without - self.explored) / self.explored) * 100,
                    "%",
                )
                print(
                    "Alpha Beta Pruning is almost ",
                    self.explored_without / self.explored,
                    " times faster !",
                )
            if eval >= 5000:
                print("* White MATE!")
            if eval <= -5000:
                print("* Black MATE!")

        # append
        self.game_moves.append(move)

        return move


###########################################################################
###########################################################################
# book class
class Book:
    def __init__(self):
        self.head = Node()
        self._create()

    def next_move(self, game_moves, weighted=True):
        for i, move in enumerate(game_moves):
            if i == 0:
                node = self.head

            for child in node.children:
                if move == child.value:
                    if len(game_moves) - 1 == i:
                        move = child.choose_child(
                            weighted
                        )  # weighted (from popular moves)
                        return move
                    else:
                        node = child

    # ------------
    # INIT METHODS
    # ------------

    def _create(self):
        # --------------------------
        # ROUND 1 - TODO: 16 missing
        # --------------------------
        self.head.add_children(
            Node(Move(Square(6, 4), Square(4, 4)), 1365473),  # e4
            Node(Move(Square(6, 3), Square(4, 3)), 1050119),  # d4
            Node(Move(Square(7, 6), Square(5, 5)), 299548),  # right knight
            Node(Move(Square(6, 2), Square(4, 2)), 211850),  # c4
        )

        # -------
        # ROUND 2
        # -------

        # e4 - 4 logs
        self.head.children[0].add_children(
            Node(Move(Square(1, 2), Square(3, 2)), 607220),
            Node(Move(Square(1, 4), Square(3, 4)), 296972),
            Node(Move(Square(1, 4), Square(2, 4)), 175686),
            Node(Move(Square(1, 2), Square(2, 2)), 106332),
        )

        #  d4 - 3 logs
        self.head.children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 624094),
            Node(Move(Square(1, 3), Square(3, 3)), 264257),
            Node(Move(Square(1, 4), Square(2, 4)), 47288),
        )

        # right knight - 2 logs
        self.head.children[2].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 139857),
            Node(Move(Square(1, 3), Square(3, 3)), 79598),
        )

        # c4 - 3 logs
        self.head.children[3].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 64235),
            Node(Move(Square(1, 4), Square(3, 4)), 45546),
        )

        # -------
        # ROUND 3
        # -------

        # 3.1.1
        self.head.children[0].children[0].add_children(
            Node(Move(Square(7, 6), Square(5, 5)), 483773),
            Node(Move(Square(7, 1), Square(5, 2)), 55647),
        )

        # 3.1.2
        self.head.children[0].children[1].add_children(
            Node(Move(Square(7, 6), Square(5, 5)), 262867),
        )

        # 3.1.3
        self.head.children[0].children[2].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 156673)
        )

        # 3.1.4
        self.head.children[0].children[3].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 83980)
        )

        # -----------------------------------------------------

        # 3.2.1
        self.head.children[1].children[0].add_children(
            Node(Move(Square(6, 2), Square(4, 2)), 430542),
            Node(Move(Square(7, 6), Square(5, 5)), 160061),
        )

        # 3.2.2
        self.head.children[1].children[1].add_children(
            Node(Move(Square(6, 2), Square(4, 2)), 191778),
            Node(Move(Square(7, 6), Square(5, 5)), 78389),
        )

        # 3.2.3
        self.head.children[1].children[2].add_children(
            Node(Move(Square(6, 4), Square(4, 4)), 155950)
        )

        # -----------------------------------------------------

        # 3.3.1
        self.head.children[2].children[0].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 158564),
            Node(Move(Square(6, 2), Square(4, 2)), 89892),
        )

        # 3.3.2
        self.head.children[2].children[1].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 77741),
            Node(Move(Square(6, 6), Square(5, 6)), 32694),
        )

        # -----------------------------------------------------

        # 3.4.1
        self.head.children[3].children[0].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 417701),
            Node(Move(Square(7, 6), Square(5, 5)), 88843),
        )

        # 3.4.2
        self.head.children[3].children[1].add_children(
            Node(Move(Square(7, 1), Square(5, 2)), 29415),
            Node(Move(Square(6, 6), Square(5, 6)), 15373),
        )

        # -------
        # ROUND 4
        # -------

        # 4.1.1.1
        self.head.children[0].children[0].children[0].add_children(
            Node(Move(Square(1, 3), Square(2, 3)), 196457),
            Node(Move(Square(0, 1), Square(2, 2)), 135043),
            Node(Move(Square(1, 4), Square(2, 4)), 127503),
        )

        # 4.1.1.2
        self.head.children[0].children[0].children[1].add_children(
            Node(Move(Square(0, 1), Square(2, 2)), 32756),
            Node(Move(Square(1, 4), Square(2, 4)), 8897),
        )

        # -----------------------------------------------------

        # 4.1.2.1
        self.head.children[0].children[1].children[0].add_children(
            Node(Move(Square(0, 1), Square(2, 2)), 226645),
        )

        # -----------------------------------------------------

        # 4.1.3.1
        self.head.children[0].children[2].children[0].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 153961),
        )

        # -----------------------------------------------------

        # 4.1.4.1
        self.head.children[0].children[3].children[0].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 80928),
        )

        # -----------------------------------------------------
        # -----------------------------------------------------

        # 4.2.1.1
        self.head.children[1].children[0].children[0].add_children(
            Node(Move(Square(1, 4), Square(2, 4)), 211046),
            Node(Move(Square(1, 6), Square(2, 6)), 154877),
            Node(Move(Square(1, 2), Square(3, 2)), 48947),
        )

        # 4.2.1.2
        self.head.children[1].children[0].children[1].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 70523),
            Node(Move(Square(1, 6), Square(2, 6)), 65729),
            Node(Move(Square(1, 4), Square(3, 4)), 58615),
        )

        # -----------------------------------------------------

        # 4.2.2.1
        self.head.children[1].children[1].children[0].add_children(
            Node(Move(Square(1, 2), Square(2, 2)), 92378),
            Node(Move(Square(1, 4), Square(2, 4)), 75340),
            Node(Move(Square(3, 3), Square(4, 2)), 23649),  # !CAPTURE
        )

        # 4.2.2.2
        self.head.children[1].children[1].children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 69781),
        )

        # ------------------------------------------------------

        # 4.2.3.1
        self.head.children[1].children[2].children[0].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 153961),
        )

        # -----------------------------------------------------
        # -----------------------------------------------------

        # 4.3.1.1
        self.head.children[2].children[0].children[0].add_children(
            Node(Move(Square(1, 3), Square(2, 3)), 196457),
            Node(Move(Square(0, 1), Square(2, 2)), 135043),
            Node(Move(Square(1, 4), Square(2, 4)), 127503),
        )

        # 4.3.1.2
        self.head.children[2].children[0].children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 23080),
            Node(Move(Square(0, 1), Square(2, 2)), 13414),
            Node(Move(Square(1, 6), Square(2, 6)), 23080),
        )

        # ------------------------------------------------------
        # -----------------------------------------------------

        # 4.4.1.1
        self.head.children[3].children[0].children[0].add_children(
            Node(Move(Square(1, 4), Square(2, 4)), 211046),
            Node(Move(Square(1, 6), Square(2, 6)), 154877),
            Node(Move(Square(1, 2), Square(3, 2)), 48947),
        )

        # 4.4.1.2
        self.head.children[3].children[0].children[1].add_children(
            Node(Move(Square(1, 6), Square(2, 6)), 33861),
            Node(Move(Square(1, 4), Square(2, 4)), 32507),
            Node(Move(Square(1, 2), Square(3, 2)), 23128),
        )

        # -----------------------------------------------------

        # 4.4.2.1
        self.head.children[3].children[1].children[0].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 7508),
            Node(Move(Square(0, 1), Square(2, 2)), 4443),
            Node(Move(Square(1, 6), Square(2, 6)), 2706),
        )

        # 4.4.2.2
        self.head.children[3].children[1].children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 7988),
            Node(Move(Square(0, 1), Square(2, 2)), 4463),
        )

        # -----------------------------------------------------
        # -----------------------------------------------------


###########################################################################
###########################################################################
# node class
class Node:
    def __init__(self, value=None, weight=0, prob=0):
        self.value = value
        self.weight = weight
        self.prob = prob
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        self.calc_prob()

    def add_children(self, *nodes):
        for node in nodes:
            self.add_child(node)

    def calc_prob(self):
        weights = 0
        for child in self.children:
            weights += child.weight

        for child in self.children:
            child.prob = (child.weight / weights) * 100

    def get_child(self, idx):
        return self.children[idx]

    def choose_child(self, weighted=True):
        if not weighted:
            return self.children[0]

        rnd = random.randint(1, 100)

        c = 0
        for child in self.children:
            if rnd <= child.prob + c:
                return child.value

            c += child.prob
