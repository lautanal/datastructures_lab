import pygame
from ui import Ui


WIDTHMARGIN = 150
HEIGHTMARGIN = 100
NCOLS = 150
NROWS = 100
TEXTAREA = 250
TEXTHOR = False


def main():
    """User Interface start.
    """
    pygame.init()
    infoObject = pygame.display.Info()
    maxw = infoObject.current_w - WIDTHMARGIN
    maxh = infoObject.current_h - HEIGHTMARGIN
    ui = Ui(maxw, maxh, NROWS, NCOLS, TEXTAREA, TEXTHOR)
    ui.start()


if __name__ == "__main__":
    main()
