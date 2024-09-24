import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# Pengaturan layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

class Tetrimino:
    shapes = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 0, 0], [1, 1, 1]],  # L
        [[0, 0, 1], [1, 1, 1]]   # J
    ]

    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetrimino.color, ((tetrimino.x + x) * GRID_SIZE, (tetrimino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_board(board):
    for y in range(ROWS):
        for x in range(COLS):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision(board, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (x + tetrimino.x < 0 or
                    x + tetrimino.x >= COLS or
                    y + tetrimino.y >= ROWS or
                    board[y + tetrimino.y][x + tetrimino.x]):
                    return True
    return False

def merge_board(board, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + tetrimino.y][x + tetrimino.x] = tetrimino.color

def clear_lines(board):
    lines_cleared = 0
    for y in range(ROWS):
        if all(board[y]):
            del board[y]
            board.insert(0, [None] * COLS)
            lines_cleared += 1
    return lines_cleared

def main():
    clock = pygame.time.Clock()
    board = [[None] * COLS for _ in range(ROWS)]
    score = 0
    level = 1
    speed = 500  # Kecepatan dalam milidetik
    tetrimino = Tetrimino()
    fall_time = 0

    while True:
        screen.fill(WHITE)
        draw_grid()
        draw_board(board)
        draw_tetrimino(tetrimino)

        fall_time += clock.get_time()
        if fall_time >= speed:
            tetrimino.y += 1
            if check_collision(board, tetrimino):
                tetrimino.y -= 1
                merge_board(board, tetrimino)
                score += clear_lines(board) * 100
                tetrimino = Tetrimino()
                if check_collision(board, tetrimino):
                    print(f"Game Over! Your score: {score}")
                    pygame.quit()
                    return
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrimino.x -= 1
                    if check_collision(board, tetrimino):
                        tetrimino.x += 1
                if event.key == pygame.K_RIGHT:
                    tetrimino.x += 1
                    if check_collision(board, tetrimino):
                        tetrimino.x -= 1
                if event.key == pygame.K_DOWN:
                    tetrimino.y += 1
                    if check_collision(board, tetrimino):
                        tetrimino.y -= 1
                if event.key == pygame.K_UP:
                    tetrimino.rotate()
                    if check_collision(board, tetrimino):
                        tetrimino.rotate()  # Kembali ke bentuk semula jika tumbukan

        # Menampilkan skor
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
