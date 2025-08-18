import pygame, sys
import numpy as np
import random

# Initialize pygame
pygame.init()

# Window size
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# Game board size (fixed at 600x600)
WIDTH = WINDOW_HEIGHT // 2
HEIGHT = WIDTH

# Offsets to center the game board in the window
X_OFFSET = (WINDOW_WIDTH - WIDTH) // 2
Y_OFFSET = ((WINDOW_HEIGHT - HEIGHT) // 2) + 125

# Board config
LINE_WIDTH = 15
WIN_LINE_WIDTH = 25
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
BACKSPACE_COLOR = (38, 180, 166)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill((BG_COLOR))
pygame.draw.rect(screen, BG_COLOR, (X_OFFSET, Y_OFFSET, WIDTH, HEIGHT))  # Game area

# Load Images
SINGLE_PLAYER_IMG = pygame.image.load('SinglePlayer Button.png').convert_alpha()
MULTI_PLAYER_IMG = pygame.image.load('Multiplayer.png').convert_alpha()

# Game board data
board = np.zeros((BOARD_ROWS, BOARD_COLS))


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Checks mouseover and clicked condition
        if self.rect.collidepoint(pos):
            # This is checking to see if you left clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


def draw_lines():
    # Horizontal
    for i in range(1, BOARD_ROWS):
        y = Y_OFFSET + i * SQUARE_SIZE
        pygame.draw.line(screen, LINE_COLOR, (X_OFFSET, y), (X_OFFSET + WIDTH, y), LINE_WIDTH)
    # Vertical
    for i in range(1, BOARD_COLS):
        x = X_OFFSET + i * SQUARE_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, Y_OFFSET), (x, Y_OFFSET + HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            center_x = X_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = Y_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                start1 = (X_OFFSET + col * SQUARE_SIZE + SPACE, Y_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end1 = (X_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE - SPACE, Y_OFFSET + row * SQUARE_SIZE + SPACE)
                start2 = (X_OFFSET + col * SQUARE_SIZE + SPACE, Y_OFFSET + row * SQUARE_SIZE + SPACE)
                end2 = (X_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        Y_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)


def console():
    # Draws the top console
    pygame.draw.rect(screen, (51, 51, 51), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 4))

    # Draws the left Square
    pygame.draw.rect(screen, (90, 90, 90),
                     ((WINDOW_WIDTH // 4), WINDOW_HEIGHT // 32, (WINDOW_WIDTH // 4) + 10, WINDOW_HEIGHT // 6))
    pygame.draw.rect(screen, (100, 100, 100), ((WINDOW_WIDTH // 4) + 5, (WINDOW_HEIGHT // 32) + 5, (WINDOW_WIDTH // 4),
                                               (WINDOW_HEIGHT // 6) - 10))

    # Draws the right Square
    pygame.draw.rect(screen, (90, 90, 90),
                     ((WINDOW_WIDTH // 2), WINDOW_HEIGHT // 32, (WINDOW_WIDTH // 4) + 10, WINDOW_HEIGHT // 6))
    pygame.draw.rect(screen, (100, 100, 100),
                     ((WINDOW_WIDTH // 2) + 5, (WINDOW_HEIGHT // 32) + 5, (WINDOW_WIDTH // 4),
                      (WINDOW_HEIGHT // 6) - 10))

    # Draws the X
    start1 = ((X_OFFSET + 0 * SQUARE_SIZE + SPACE) + 5, (0 * SQUARE_SIZE + SQUARE_SIZE - SPACE) + 27)
    end1 = ((X_OFFSET + 0 * SQUARE_SIZE + SQUARE_SIZE - SPACE) + 5, (0 * SQUARE_SIZE + SPACE) + 27)
    start2 = ((X_OFFSET + 0 * SQUARE_SIZE + SPACE) + 5, (0 * SQUARE_SIZE + SPACE) + 27)
    end2 = ((X_OFFSET + 0 * SQUARE_SIZE + SQUARE_SIZE - SPACE) + 5, (0 * SQUARE_SIZE + SQUARE_SIZE - SPACE) + 27)
    pygame.draw.line(screen, CIRCLE_COLOR, start1, end1, CROSS_WIDTH)
    pygame.draw.line(screen, CIRCLE_COLOR, start2, end2, CROSS_WIDTH)

    # Draws the O
    pygame.draw.circle(screen, CIRCLE_COLOR, (WINDOW_WIDTH // 2 + WINDOW_WIDTH // 8, WINDOW_HEIGHT // 8 - 15),
                       CIRCLE_RADIUS, CIRCLE_WIDTH)


def player_tracker(player):
    if player == 1:
        pygame.draw.rect(screen, (100, 100, 100),
                         ((WINDOW_WIDTH // 4) + 5, (WINDOW_HEIGHT // 6) + 12, (WINDOW_WIDTH // 4) - 6, 10))
        pygame.draw.rect(screen, BG_COLOR,
                         ((WINDOW_WIDTH // 2) + 5, (WINDOW_HEIGHT // 6) + 12, (WINDOW_WIDTH // 4) - 1, 10))
    else:
        pygame.draw.rect(screen, (100, 100, 100),
                         ((WINDOW_WIDTH // 2) + 5, (WINDOW_HEIGHT // 6) + 12, (WINDOW_WIDTH // 4) - 1, 10))
        pygame.draw.rect(screen, BG_COLOR,
                         ((WINDOW_WIDTH // 4) + 5, (WINDOW_HEIGHT // 6) + 12, (WINDOW_WIDTH // 4) - 6, 10))


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_filled():
    return not np.any(board == 0)


def ai():
    # These nested for loop is to try and win by simulating each move
    # We use the nested for loop to loop through each row and then each column in that row
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):

            # If the square is currently available then we temporarily place the ai there
            if available_square(row, col):

                # Placing the temporary
                board[row][col] = 2

                # After temporarily placing the ai there we will then check if this move causes a win
                winning = is_winning_move(2)

                # We then reset the square so it doesn't activate an unwanted move or lose or win
                board[row][col] = 0

                if winning:
                    return (row, col)

    # This nested for loop is used to check and attempt to block the oppenent from winning
    # We use the nested for loop to loop through each row and then each column in that row
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):

            # If the square is currently available then we temporarily place the oppenent there to check if they will win
            if available_square(row, col):

                # Placing the temporary
                board[row][col] = 1

                # After temporarily placing the opponent there we will then check if this move causes a win
                block = is_winning_move(1)

                # We then reset the square so it doesn't activate an unwanted move or lose or win
                board[row][col] = 0
                if block:
                    return (row, col)


    # If there is no blocking or wining move required we check to see if the center of the board is taken or not
    # We do this because the center of the board is the most powerful spot on the board
    if available_square(1, 1):
        return (1, 1)

    # If there is no blocking or wining move required and if the center is already taken then we look for the next most
    # valuable squares which is any of the corners
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)
    for row, col in corners:
        if available_square(row, col):
            return (row, col)

    # If there is no blocking or wining move required and if the center and corners are already taken then we go for the
    # Next best things which is the side squares
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    random.shuffle(sides)
    for row, col in sides:
        if available_square(row, col):
            return (row, col)

    # Then if there is no possible moves anymore either a loss or draw then we return no coords
    return None


def is_winning_move(player):
    # Check verticals
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check horizontals
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Check descending diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    # Check ascending diagonal
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    # No win found
    return False



def check_win(player):
    # vertical win check
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            draw_vertical_winning_line(col, player)
            return True

    # horizontal win check
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            draw_horizontal_winning_line(row, player)
            return True

    # asc diagonal win check
    if all(board[i][2 - i] == player for i in range(BOARD_ROWS)):
        draw_asc_diagonal(player)
        return True

    # desc diagonal win check
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        draw_desc_diagonal(player)
        return True

    return False


def animated_horizontal_line(row, player):
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR
    y = Y_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2
    start_x = X_OFFSET + 10
    end_x = X_OFFSET + WIDTH - 8
    step = 25
    for x in range(start_x, end_x, step):
        pygame.draw.line(screen, color, (start_x, y), (x + 1, y), WIN_LINE_WIDTH)
        pygame.display.update()
        pygame.time.delay(7)


def animated_vertical_line(col, player):
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    x = X_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2
    start_y = Y_OFFSET + 10
    end_y = Y_OFFSET + HEIGHT - 8
    step = 25
    for y in range(start_y, end_y, step):
        pygame.draw.line(screen, color, (x, start_y), (x, y + 1), WIN_LINE_WIDTH)
        pygame.display.update()
        pygame.time.delay(7)


def animated_asc_line(player):
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR
    step = 25
    start_x = X_OFFSET + 15
    end_x = X_OFFSET + WIDTH - 15
    start_y = Y_OFFSET + HEIGHT - 15
    end_y = Y_OFFSET + 15
    dx = (end_x - start_x) / step
    dy = (end_y - start_y) / step
    for i in range(1, step + 1):
        x = start_x + dx * i
        y = start_y + dy * i
        pygame.draw.line(screen, color, (start_x, start_y), (x, y), WIN_LINE_WIDTH)
        pygame.display.update()
        pygame.time.delay(7)


def animated_desc_line(player):
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR
    step = 25
    start_x = X_OFFSET + 15
    end_x = X_OFFSET + WIDTH - 15
    start_y = Y_OFFSET + 15
    end_y = Y_OFFSET + HEIGHT - 15
    dx = (end_x - start_x) / step
    dy = (end_y - start_y) / step
    for i in range(1, step + 1):
        x = start_x + dx * i
        y = start_y + dy * i
        pygame.draw.line(screen, color, (start_x, start_y), (x, y), WIN_LINE_WIDTH)
        pygame.display.update()
        pygame.time.delay(7)


def draw_vertical_winning_line(col, player):
    pygame.time.delay(160)
    animated_vertical_line(col, player)


def draw_horizontal_winning_line(row, player):
    pygame.time.delay(160)
    animated_horizontal_line(row, player)


def draw_asc_diagonal(player):
    pygame.time.delay(160)
    animated_asc_line(player)


def draw_desc_diagonal(player):
    pygame.time.delay(160)
    animated_desc_line(player)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_text():
    pygame.draw.rect(screen, BG_COLOR, ((WINDOW_WIDTH // 2) - (WINDOW_WIDTH // 16), (WINDOW_HEIGHT // 4) + 10, 200, 50))


def disp_text(player):
    if player == 1:
        reset_text()
        player_tracker(player)
        draw_text("O's Turn", text_font, (0, 0, 0), (WINDOW_WIDTH // 2) - (WINDOW_WIDTH // 16),
                  (WINDOW_HEIGHT // 4) + 10)
    elif player == 2:
        reset_text()
        player_tracker(player)
        draw_text("X's Turn", text_font, (0, 0, 0), (WINDOW_WIDTH // 2) - (WINDOW_WIDTH // 16),
                  (WINDOW_HEIGHT // 4) + 10)


def restart():
    screen.fill((BG_COLOR))
    pygame.draw.rect(screen, BG_COLOR, (X_OFFSET, Y_OFFSET, WIDTH, HEIGHT))
    draw_lines()
    console()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


text_font = pygame.font.SysFont('Arial', WINDOW_WIDTH // 25)

player = random.randint(1, 2)
SELECTION_SCREEN = True
SINGLE = False
MULTI = False
game_started = False
game_over = False

single_button = Button(WINDOW_WIDTH // 2 - 100 * 2, WINDOW_HEIGHT // 8, SINGLE_PLAYER_IMG, 2)
multiplayer_button = Button(WINDOW_WIDTH // 2 - 100 * 2, WINDOW_HEIGHT // 2, MULTI_PLAYER_IMG, 2)

# Main loop
while True:

    if SELECTION_SCREEN:
        if single_button.draw():
            SINGLE = True
            MULTI = False
            player = 1
            SELECTION_SCREEN = False
            restart()
            game_started = False


        elif multiplayer_button.draw():
            SINGLE = False
            MULTI = True
            SELECTION_SCREEN = False
            player = random.randint(1, 2)
            restart()
            game_started = False




    else:
        if MULTI and not game_started:
            draw_lines()
            console()
            disp_text(player)
            player_tracker(player)
            game_started = True


        elif SINGLE and not game_started:
            draw_lines()
            console()
            disp_text(player)
            player_tracker(player)
            game_started = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and game_over == False:
            mouseX, mouseY = event.pos
            if (X_OFFSET <= mouseX < X_OFFSET + WIDTH) and (Y_OFFSET <= mouseY < Y_OFFSET + HEIGHT):
                clicked_col = (mouseX - X_OFFSET) // SQUARE_SIZE
                clicked_row = (mouseY - Y_OFFSET) // SQUARE_SIZE
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()
                    pygame.display.update()
                    if check_win(player):
                        game_over = True
                    else:
                        player = player % 2 + 1
                        player_tracker(player)
                        disp_text(player)

                    if SINGLE and not game_over and player == 2:
                        pygame.time.delay(500)
                        ai_move = ai()
                        if ai_move:
                            mark_square(ai_move[0], ai_move[1], player)
                            draw_figures()
                            pygame.display.update()
                            if check_win(player):
                                game_over = True
                            else:
                                player = player % 2 + 1
                                player_tracker(player)
                                disp_text(player)
                    elif SINGLE and not game_over and player == 1:
                        disp_text(player)

        if game_over == True:
            console()
            reset_text()
            if player == 2:
                draw_text("X Is The Winner", text_font, (0, 0, 0), (WINDOW_WIDTH // 2) - (WINDOW_WIDTH // 8),
                          (WINDOW_HEIGHT // 4) + 10)
            else:
                draw_text("O Is the Winner", text_font, (0, 0, 0), (WINDOW_WIDTH // 2) - (WINDOW_WIDTH // 8),
                          (WINDOW_HEIGHT // 4) + 10)

        if is_board_filled() and not game_over:
            console()
            reset_text()
            draw_text("Draw", text_font, (0, 0, 0), (WINDOW_WIDTH // 2) - 35, (WINDOW_HEIGHT // 4) + 10)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not SINGLE:
            restart()
            game_over = False
            player = random.randint(1, 2)
            player_tracker(player)
            disp_text(player)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and SINGLE:
            restart()
            game_over = False
            player = 1
            player_tracker(player)
            disp_text(player)

    pygame.display.update()
