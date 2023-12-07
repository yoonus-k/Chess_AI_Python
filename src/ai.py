# This file is for the AI class and the Book class to calculate the best move for the AI player. (Black)
# import copy, math, random
import copy, math, random

from const import *
from board import *
import time


###########################################################################
###########################################################################
# AI class
class AI:
    def __init__(self, engine="book", depth=2):
        # var
        self.engine = engine
        self.depth = depth
        self.book = Book()
        self.color = "black"
        self.game_moves = []
        self.explored = 0
        self.explored_without_pruning = 0
        self.pruned_nodes = 0

    # book moves to accelerate the game performance

    def book_move(self):
        move = self.book.next_move(self.game_moves, weighted=True)
        return move

    # heuristic evaluation function , heatmap to evaluate the position of the piece
    # this heatmap is from the stockfish engine , it is a 8x8 matrix
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

    # heuristic evaluation function , threats to evaluate the value of the piece if it is attacking the opponent's piece
    def threats(self, board, piece):
        eval = 0
        for move in piece.moves:
            attacked = board.squares[move.final.row][move.final.col]
            if attacked.has_piece():  # if the square is not empty
                if attacked.piece.color != piece.color:
                    # checks
                    if attacked.piece.name == "king":
                        eval += (
                            attacked.piece.value / 10500
                        )  # decrease the value of the king to make the AI more aggressive

                    # threat
                    else:
                        eval += (
                            attacked.piece.value / 45
                        )  # increase the value of the piece to make the AI more aggressive

        return eval

    # heuristic evaluation function, this function is used in the minimax algorithm at the leaf nodes
    def static_eval(self, board):
        # var
        eval = 0

        # loop through the board
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():  # if the square is not empty
                    # get the piece
                    piece = board.squares[row][col].piece
                    # value of the piece
                    eval += piece.value
                    # add the heatmap value
                    eval += self.heatmap(piece, row, col)
                    # if the piece is not a queen , add the number of moves
                    if piece.name != "queen":
                        eval += 0.01 * len(piece.moves)
                    else:
                        eval += 0.003 * len(piece.moves)
                    # checks
                    eval += self.threats(board, piece)

        eval = round(eval, 5)
        return eval

    # get all the moves of the AI player
    def get_moves(self, board, color):
        moves = []
        # loop through the board
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_team_piece(color):
                    board.calc_moves(
                        square.piece, square.row, square.col
                    )  # calculate the moves of the piece
                    moves += square.piece.moves  # add the moves to the list

        return moves  # return the list of moves

    # minimax algorithm with alpha beta pruning
    def minimax(self, board, depth, maximizing, alpha, beta):
        # base case
        if depth == 0:
            return (
                self.static_eval(board),
                None,
            )  # return the evaluation of the board and the move

        # if the turn is white , maximize
        if maximizing:
            max_eval = -math.inf  # initialize the max evaluation
            best_move = None  # initialize the best move
            moves = self.get_moves(
                board, "white"
            )  # get all the moves of the white pieces
            for move in moves:  # loop through the moves
                self.explored += 1  # increment the number of explored boards
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth - 1, False, alpha, beta)[
                    0
                ]  # recursive call , eval, move
                if (
                    eval > max_eval
                ):  # if the evaluation is greater than the max evaluation, update the max evaluation and the best move
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, max_eval)  # update alpha
                if (
                    beta <= alpha
                ):  # if beta is less than or equal to alpha , break and prune
                    self.pruned_nodes += 1
                    break

            if (
                not best_move
            ):  # if the best move is not none and not best move , choose a random move
                best_move = moves[0]

            return max_eval, best_move

        # if the turn is black , minimize
        elif not maximizing:
            # initialize the min evaluation
            min_eval = math.inf  # initialize the min evaluation
            best_move = None

            moves = self.get_moves(
                board, "black"
            )  # get all the moves of the black pieces
            for move in moves:  # loop through the moves
                self.explored += 1  # increment the number of explored boards
                piece = board.squares[move.initial.row][
                    move.initial.col
                ].piece  # get the piece
                temp_board = copy.deepcopy(board)  # copy the board
                temp_board.move(piece, move)  # move the piece
                piece.moved = False  # set the moved attribute to false
                eval = self.minimax(temp_board, depth - 1, True, alpha, beta)[
                    0
                ]  # recursive call , eval, move
                if (
                    eval < min_eval
                ):  # if the evaluation is less than the min evaluation, update the min evaluation and the best move
                    min_eval = eval
                    best_move = move

                beta = min(beta, min_eval)  # update beta
                if (
                    beta <= alpha
                ):  # if beta is less than or equal to alpha , break and prune
                    self.pruned_nodes += 1
                    break

            if (
                not best_move
            ):  # if the best move is not none and not best move , choose a random move
                best_move = moves[0]

            return min_eval, best_move  # eval, move

    def minimax_without_pruning(self, board, depth, maximizing):
        # base case
        if depth == 0:
            return (
                self.static_eval(board),
                None,
            )  # return the evaluation of the board and the move

        # if the turn is white , maximize
        if maximizing:
            max_eval = -math.inf  # initialize the max evaluation
            moves = self.get_moves(
                board, "white"
            )  # get all the moves of the white pieces
            for move in moves:  # loop through the moves
                self.explored_without_pruning += (
                    1  # increment the number of explored boards
                )
                piece = board.squares[move.initial.row][
                    move.initial.col
                ].piece  # get the piece
                temp_board = copy.deepcopy(board)  # copy the board
                temp_board.move(piece, move)  # move the piece
                piece.moved = False  # set the moved attribute to false
                eval = self.minimax_without_pruning(temp_board, depth - 1, False)[
                    0
                ]  #  recursive call , eval, move
                if (
                    eval > max_eval
                ):  # if the evaluation is greater than the max evaluation, update the max evaluation and the best move
                    max_eval = eval
                    best_move = move

            if (
                not best_move
            ):  # if the best move is not none and not best move , choose a random move
                best_move = moves[0]

            return max_eval, best_move

        # if the turn is black , minimize
        elif not maximizing:
            # initialize the min evaluation
            min_eval = math.inf
            moves = self.get_moves(
                board, "black"
            )  # get all the moves of the black pieces
            for move in moves:  # loop through the moves
                self.explored_without_pruning += (
                    1  # increment the number of explored boards
                )
                piece = board.squares[move.initial.row][
                    move.initial.col
                ].piece  # get the piece
                temp_board = copy.deepcopy(board)  # copy the board
                temp_board.move(piece, move)  # move the piece
                piece.moved = False  # set the moved attribute to false
                eval = self.minimax_without_pruning(temp_board, depth - 1, True)[
                    0
                ]  # recursive call , eval, move
                if (
                    eval < min_eval
                ):  # if the evaluation is less than the min evaluation, update the min evaluation and the best move
                    min_eval = eval
                    best_move = move

            if (
                not best_move
            ):  # if the best move is not none and not best move , choose a random move
                best_move = moves[0]

            return min_eval, best_move

    # this function is used to test the performance of the alpha beta pruning
    def eval(self, main_board):
        # inictialize the number of explored boards and the number of explored boards without pruning to 0
        self.explored = 0
        self.explored_without_pruning = 0

        # get the last move to append it to the game moves
        last_move = main_board.last_move
        self.game_moves.append(last_move)

        # check if the engine is book to get the book move and append it to the game moves
        # if there is no more book moves , change the engine to minimax
        if self.engine == "book":
            move = self.book_move()

            # no more book moves ?
            if move is None:
                self.engine = "minimax"

        # if the engine is minimax , get the best move using the minimax algorithm
        if self.engine == "minimax":
            # print the number of explored boards
            print("Finding the best move using Minimax algorithm ...")
            # printing
            print("\n- Initial evalation for the static:", self.static_eval(main_board))

            # minimax initial call without pruning
            time_1 = time.time()
            print(
                "\n#############################################\nMinimax without pruning ..."
            )
            eval, move_without_pruning = self.minimax_without_pruning(
                main_board, self.depth, False
            )
            time_2 = time.time()
            print("- Final eval:", eval)
            print(
                "the best move is:",
                "(",
                Square.get_alphacol(move_without_pruning.initial.col),
                8 - move_without_pruning.initial.row,
                ")",
                "->",
                "(",
                Square.get_alphacol(move_without_pruning.final.col),
                8 - move_without_pruning.final.row,
                ").",
            )
            print("- Boards explored", self.explored_without_pruning)
            minimax_without_pruning_time = time_2 - time_1
            print("time taken:", minimax_without_pruning_time, "seconds")
            print("\n#####################")

            # minimax initial call with pruning
            print("Minimax with pruning Alpha Beta ...")
            time_1 = time.time()
            eval, move = self.minimax(
                main_board, self.depth, False, -math.inf, math.inf
            )
            time_2 = time.time()
            print("- Final eval:", eval)
            print(
                "the best move is:",
                "(",
                Square.get_alphacol(move.initial.col),
                8 - move.initial.row,
                ")",
                "->",
                "(",
                Square.get_alphacol(move.final.col),
                8 - move.final.row,
                ").",
            )
            print("- Boards explored: ", self.explored)
            print("- Pruned nodes: ", self.explored_without_pruning - self.explored)
            minimax_with_pruning_time = time_2 - time_1
            print("time taken:", minimax_with_pruning_time, "seconds")

            print("\n#####################")

            if self.explored != 0:
                print(
                    "optimization:",
                    ((self.explored_without_pruning - self.explored) / self.explored)
                    * 100,
                    "%",
                )
                print(
                    "Alpha Beta Pruning is almost ",
                    self.explored_without_pruning / self.explored,
                    " times faster !",
                )
                print(
                    "time saved:",
                    minimax_without_pruning_time - minimax_with_pruning_time,
                    " seconds",
                )
                print("\n############################################# ")
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
