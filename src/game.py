import pygame

from ai import *
from const import *
from config import *
from board import *


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.config = Config()
        self.dragger = Dragger()
        self.next_player = "white"
        self.gamemode = "ai"
        self.selected_piece = None
        self.hovered_square = None

    # ------------
    # DRAW METHODS
    # ------------

    # draw a text called CPCS-331 in the middle of the screen
    def show_title(self, surface):
        # text
        text = self.config.font.render("CPCS-331", 1, "#00FF00")
        # text rect
        text_rect = text.get_rect(center=(WIDTH / 5.5, HEIGHT // 2.5))

        # increment the size of the text
        text = pygame.transform.scale(text, (600, 200))

        # Make the text transparent
        text.set_alpha(191)

        # draw
        surface.blit(text, text_rect)

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # tiles
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # draw
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # coordinates
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    surface.blit(lbl, (5, 5 + row * SQSIZE))

                # col coordinates
                if row == 7:
                    # coordinates
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # coordinates
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    surface.blit(lbl, (col * SQSIZE + SQSIZE - 20, HEIGHT - 20))

        if self.board.last_move:
            self.show_last_move(surface)

        if self.selected_piece:
            self.show_moves(surface)

    # draw the pieces on the board
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece  # get the piece object
                    # for dragger
                    if piece is not self.selected_piece:  # if the piece is not selected
                        piece.set_texture()  # set the texture
                        texture = piece.texture  # get the texture
                        img = pygame.image.load(texture)  # load the texture
                        img_center = (  # get the center of the texture
                            col * SQSIZE + SQSIZE // 2,
                            row * SQSIZE + SQSIZE // 2,
                        )
                        piece.texture_rect = img.get_rect(
                            center=img_center
                        )  # get the rect of the texture
                        surface.blit(
                            img, piece.texture_rect
                        )  # blit the texture to the screen

    def show_moves(self, surface):
        if self.selected_piece:
            theme = self.config.theme

            for move in self.selected_piece.moves:
                # color
                color = (
                    theme.moves.light
                    if (move.final.row + move.final.col) % 2 == 0
                    else theme.moves.dark
                )
                # rect
                rect = (
                    move.final.col * SQSIZE,
                    move.final.row * SQSIZE,
                    SQSIZE,
                    SQSIZE,
                )
                # draw
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            theme = self.config.theme

            initial = self.board.last_move.initial
            final = self.board.last_move.final

            # color
            for pos in [initial, final]:
                # color
                color = (
                    theme.trace.light
                    if (pos.col + pos.row) % 2 == 0
                    else theme.trace.dark
                )
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # draw
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            # color
            color = (180, 180, 180)
            # rect
            rect = (
                self.hovered_square.col * SQSIZE,
                self.hovered_square.row * SQSIZE,
                SQSIZE,
                SQSIZE,
            )
            # draw
            pygame.draw.rect(surface, color, rect, 3)

    # -------------
    # OTHER METHODS
    # -------------

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def next_turn(self):
        self.next_player = "black" if self.next_player == "white" else "white"

    def change_gamemode(self):
        self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def select_piece(self, piece):
        self.selected_piece = piece

    def unselect_piece(self):
        self.selected_piece = None

    def reset(self):
        self.__init__()


###########################################################################
###########################################################################
# Dragger class
class Dragger:
    """
    Responsable of dragging the pieces through screen
    """

    def __init__(self):
        self.dragging = False
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # -------------
    # CLASS METHODS
    # -------------

    # --- DRAW METHODS ---

    def update_blit(self, surface):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # image
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)

    # --- OTHER METHODS ---

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
