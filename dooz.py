# Example file showing a basic pygame "game loop"
import pygame
import numpy as np


def draw_board(screen, board):
    width = screen.get_width()
    height = screen.get_height()
    text_box = 40
    line_width = 2
    block_width = width // 3
    block_height = (height - text_box) // 3
    for i in range(3):
        for j in range(3):
            # pygame.draw.rect(screen, "black", (i * 100, j * 100, 100, 100), 1)
            pygame.draw.rect(
                screen,
                "black",
                (i * block_width, j * block_height, block_width, block_height),
                line_width,
            )
            if board[i, j] == 1:
                pygame.draw.line(
                    screen,
                    "red",
                    (i * block_width + line_width, j * block_height + line_width),
                    (
                        i * block_width + block_width - line_width,
                        j * block_height + block_height - line_width,
                    ),
                    line_width,
                )
                pygame.draw.line(
                    screen,
                    "red",
                    (
                        i * block_width + line_width,
                        j * block_height + block_height - line_width,
                    ),
                    (
                        i * block_width + block_width - line_width,
                        j * block_height + line_width,
                    ),
                    line_width,
                )
            elif board[i, j] == 2:
                pygame.draw.circle(
                    screen,
                    "blue",
                    (
                        i * block_width + block_width // 2,
                        j * block_height + block_height // 2,
                    ),
                    min(block_width, block_height) // 3,
                    line_width,
                )


def has_won(player, board):
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    for i in range(3):
        if np.all(board[:, i] == player) or np.all(board[i, :] == player):
            return True
    return False


WIDTH = 480
HEIGHT = 480


def main():
    # pygame setup
    pygame.init()
    pygame.display.set_caption("DOOZ")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    board = np.zeros((3, 3), dtype=int)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 36)
    text_gameover = font.render("Game Over!", True, pygame.Color("black"))
    text_owon = font.render("O is the winner!", True, pygame.Color("blue"))
    text_xwon = font.render("X is the winner!", True, pygame.Color("red"))
    text_invalid = font.render("Invalid Move!", True, pygame.Color("red"))
    text_info = font.render("Press R to reset", True, pygame.Color("black"))

    turn = 0  # 0 for x 1 for O
    should_quit = False
    warning_shown = False
    while not should_quit:
        width = screen.get_width()
        height = screen.get_height()
        info_box = width // 3, height - 40
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = True
                pos = event.pos
                x = pos[0] // (width // 3)
                y = pos[1] // ((height - 40) // 3)
                if board[x, y] == 0:
                    board[x, y] = turn + 1
                    turn = int(not turn)
                    warning_shown = False
                else:
                    warning_shown = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.fill(0)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        # RENDER YOUR GAME HERE
        line_width = 2
        draw_board(screen, board)
        # check for win
        if has_won(1, board):
            screen.blit(text_xwon, info_box)
            running = False
        elif has_won(2, board):
            screen.blit(text_owon, info_box)
            running = False

        if np.all(board) and not has_won(1, board) and not has_won(2, board):
            screen.blit(text_gameover, info_box)
            running = False
        if not running:
            screen.blit(text_info, (width // 3, height -20))
            running = True
        if warning_shown:
            screen.blit(text_invalid, info_box)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    raise SystemExit(main())
