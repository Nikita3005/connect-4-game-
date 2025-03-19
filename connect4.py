import pygame
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 80  # Grid cell size
RADIUS = SQUARESIZE // 2 - 5
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE  # Extra row for the menu
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)  # Light Blue
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# Board initialization
board = np.zeros((ROW_COUNT, COLUMN_COUNT))
game_over = False
turn = 0

# Function to draw the board
def draw_board():
    screen.fill(WHITE)  # White background
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, LIGHT_BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    
    # Draw pieces
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (r * SQUARESIZE + SQUARESIZE // 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (r * SQUARESIZE + SQUARESIZE // 2)), RADIUS)
    pygame.display.update()

# Function to check if a column is valid
def is_valid_column(col):
    return board[ROW_COUNT - 1][col] == 0

# Function to get the lowest empty row in a column
def get_next_open_row(col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

# Function to drop a piece
def drop_piece(col, piece):
    row = get_next_open_row(col)
    if row is not None:
        board[row][col] = piece
        animate_drop(col, row, piece)
        return row
    return None

# Function to animate the drop
def animate_drop(col, final_row, piece):
    for r in range(ROW_COUNT - 1, final_row - 1, -1):
        draw_board()
        pygame.draw.circle(screen, RED if piece == 1 else YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (r * SQUARESIZE + SQUARESIZE // 2)), RADIUS)
        pygame.display.update()
        pygame.time.delay(50)

# Function to check for a win
def check_win(piece):
    # Check horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

# Function to display message
def display_message(text):
    font = pygame.font.Font(None, 40)
    label = font.render(text, True, (0, 0, 0))
    screen.fill(WHITE)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Function to get player names
def get_player_names():
    pygame.display.set_caption("Enter Player Names")
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    input_box1 = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 40)
    input_box2 = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 40)
    color = pygame.Color("black")

    player1_name = ""
    player2_name = ""
    active_box = 1

    running = True
    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, color, input_box1, 2)
        pygame.draw.rect(screen, color, input_box2, 2)

        text1 = font.render("Player 1: " + player1_name, True, (0, 0, 0))
        text2 = font.render("Player 2: " + player2_name, True, (0, 0, 0))
        screen.blit(text1, (input_box1.x + 5, input_box1.y + 5))
        screen.blit(text2, (input_box2.x + 5, input_box2.y + 5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active_box == 1:
                        active_box = 2
                    else:
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    if active_box == 1:
                        player1_name = player1_name[:-1]
                    else:
                        player2_name = player2_name[:-1]
                else:
                    if active_box == 1:
                        player1_name += event.unicode
                    else:
                        player2_name += event.unicode

    return player1_name, player2_name

# Get player names
player1, player2 = get_player_names()

# Main game loop
draw_board()
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = event.pos[0]
            col = x_pos // SQUARESIZE

            if is_valid_column(col):
                row = drop_piece(col, 1 if turn == 0 else 2)

                if check_win(1 if turn == 0 else 2):
                    display_message(f"{player1 if turn == 0 else player2} Wins!")
                    game_over = True
                    break

                turn = (turn + 1) % 2

    draw_board()
pygame.time.delay(3000)
pygame.quit()
