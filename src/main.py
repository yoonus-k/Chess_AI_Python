import sys, pygame, os

from const import *
from game import *
from board import *


class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.game = Game()

    def mainloop(self):

        while True:
            screen = self.screen
            game = self.game
            board = self.game.board
            ai = self.game.ai
            dragger = self.game.dragger

            if not game.selected_piece:
                def show():
                    game.show_bg(screen)
                    game.show_pieces(screen)
                    game.show_title(screen)
                show()
            game.show_hover(screen)

            if (
                dragger.dragging
            ):  # this is to fix the bug of the piece not showing when dragging
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    pos = event.pos
                    clicked_row = (
                        dragger.mouseY // SQSIZE
                    )  # get the row of the clicked square
                    clicked_col = (
                        dragger.mouseX // SQSIZE
                    )  # get the col of the clicked square

                    if board.squares[clicked_row][
                        clicked_col
                    ].has_piece():  # if the clicked square has a piece
                        piece = board.squares[clicked_row][
                            clicked_col
                        ].piece  # get the piece object from the clicked square
                        # valid piece ?
                        if (
                            piece.color == game.next_player
                        ):  # if the piece color is the same as the next player
                            game.select_piece(piece)  # select the piece
                            board.calc_moves(
                                piece, clicked_row, clicked_col, bool=True
                            )  # calculate the moves of the piece
                            dragger.drag_piece(piece)  # drag the piece
                            dragger.save_initial(pos)  # save the initial pos
                            # show
                            game.show_bg(screen)  # show the background
                            game.show_pieces(screen)  # show the pieces

                # mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # released pos
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # new move object
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move -> move ?
                        if board.valid_move(dragger.piece, move):
                            # capture
                            captured = board.squares[released_row][
                                released_col
                            ].has_piece()
                            # move
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)  # set en passant

                            game.sound_effect(captured)
                            # draw
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)


                            # next -> AI
                            game.next_turn()

                            # if the turn is black , check if the game is over

                            # --------------
                            # >>>>> AI >>>>>
                            # --------------

                            if game.gamemode == "ai":
                                # update
                                game.unselect_piece()
                                game.show_pieces(screen)
                                pygame.display.update()
                                # optimal move
                                move = ai.eval(board)

                                initial = move.initial
                                final = move.final
                                # piece
                                piece = board.squares[initial.row][initial.col].piece
                                # capture
                                captured = board.squares[final.row][
                                    final.col
                                ].has_piece()
                                # move
                                board.move(piece, move)
                                game.sound_effect(captured)
                                # draw
                                game.show_bg(screen)
                                game.show_pieces(screen)
                                # next -> AI
                                game.next_turn()

                    game.unselect_piece()
                    dragger.undrag_piece()

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    motion_row = pos[1] // SQSIZE
                    motion_col = pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # key press
                elif event.type == pygame.KEYDOWN:
                    # gamemode
                    if event.key == pygame.K_a:
                        game.change_gamemode()

                    if event.key == pygame.K_2:
                        ai.depth = 2

                    if event.key == pygame.K_3:
                        ai.depth = 3

                    if event.key == pygame.K_4:
                        ai.depth = 4

                    # theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # reset
                    if event.key == pygame.K_r:
                        game.reset()

                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        ai = self.game.ai
                        dragger = self.game.dragger

                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


class InstructionScene:
    def __init__(self, screen):
        self.screen = screen

    def display_instructions(self):
        self.screen.fill((255, 255, 255))  # Fill the instruction screen with white color
        font = pygame.font.Font(None, 36)
        text1 = font.render("Instructions:", True, (0, 0, 0))
        text2 = font.render("1. Change game mode with key 'a' (pvp or AI).", True, (0, 0, 0))
        text3 = font.render("2. Change AI depth with keys '3' or '4'.", True, (0, 0, 0))
        text4 = font.render("3. Restart the game with key 'r'.", True, (0, 0, 0))
        text5 = font.render("Press ESC to return to the main screen.", True, (0, 0, 0))
        self.screen.blit(text1, (50, 50))
        self.screen.blit(text2, (50, 100))
        self.screen.blit(text3, (50, 150))
        self.screen.blit(text4, (50, 200))
        self.screen.blit(text5, (50, 250))
        pygame.display.flip()  # Update the display

    # Mainloop for the instruction scene
    def mainloop(self):
        while True:
            for event in pygame.event.get():
                # Check if the user closed the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check if the user pressed the ESC key
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Exit the instruction mainloop and return to the main menu

            # Display the instructions
            self.display_instructions()
            pygame.display.update()


class Main:
    def __init__(self):
        pygame.init()
        # Set up the main screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess_AI CPCS-331 Project")

        # Set up the icon
        icon = pygame.image.load(os.path.join("../assets/images", "icon.png"))
        pygame.display.set_icon(icon)

        # Initialize scenes
        self.game_scene = GameScene(self.screen)
        self.instruction_scene = InstructionScene(self.screen)

        # Initial scene is the instruction scene
        self.current_scene = self.instruction_scene


    def mainloop(self):
        while True:
            self.current_scene.mainloop()

            if isinstance(self.current_scene, GameScene):
                # Switch to the instruction scene when ESC key is pressed
                self.current_scene = self.instruction_scene
                print("Switched to instruction scene")
            # Check if the scene is the instruction scene
            elif isinstance(self.current_scene, InstructionScene):
                # Switch to the game scene when ESC key is pressed
                self.current_scene = self.game_scene
                print("Switched to game scene")


if __name__ == "__main__":
    m = Main()
    m.mainloop()
