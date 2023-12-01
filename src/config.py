import os, pygame

from board import Sound


class Config:
    def __init__(self):
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.move_sound = Sound(os.path.join("assets/sounds/move.wav"))
        self.capture_sound = Sound(os.path.join("assets/sounds/capture.wav"))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    # ------------
    # INIT METHODS
    # ------------

    def _add_themes(self):
        green = Theme(
            (234, 235, 200),
            (119, 154, 88),
            (244, 247, 116),
            (172, 195, 51),
            "#C86464",
            "#C84646",
        )
        brown = Theme(
            (235, 209, 166),
            (165, 117, 80),
            (245, 234, 100),
            (209, 185, 59),
            "#C86464",
            "#C84646",
        )
        blue = Theme(
            (229, 228, 200),
            (60, 95, 135),
            (123, 187, 227),
            (43, 119, 191),
            "#C86464",
            "#C84646",
        )
        gray = Theme(
            (120, 119, 118),
            (86, 85, 84),
            (99, 126, 143),
            (82, 108, 128),
            "#C86464",
            "#C84646",
        )

        self.themes = [
            green,
            brown,
            blue,
            gray,
        ]


###########################################################################
###########################################################################
# Theme class
class Theme:
    """
    Stores the game themes data
    """

    def __init__(
        self, light_bg, dark_bg, light_trace, dark_trace, light_moves, dark_moves
    ):
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)


###########################################################################
###########################################################################
# Color class
class Color:
    """
    Stores color data (light and dark)
    """

    def __init__(self, light, dark):
        self.light = light
        self.dark = dark
