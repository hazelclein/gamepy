import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 800
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Pengaturan layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catur")

# Gambar papan catur
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Kelas untuk bidak catur
class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.type = piece_type
        self.rect = None

    def draw(self, screen):
        piece_color = (255, 255, 255) if self.color == "white" else (0, 0, 0)
        center = (self.rect.x + SQUARE_SIZE // 2, self.rect.y + SQUARE_SIZE // 2)
        if self.type == "pawn":
            pygame.draw.circle(screen, piece_color, center, SQUARE_SIZE // 4)
        elif self.type == "rook":
            pygame.draw.rect(screen, piece_color, (center[0] - 10, center[1] - 10, 20, 20))
        elif self.type == "knight":
            pygame.draw.polygon(screen, piece_color, [(center[0], center[1]-15), (center[0]+10, center[1]), (center[0]-10, center[1])])
        elif self.type == "bishop":
            pygame.draw.polygon(screen, piece_color, [(center[0], center[1]-15), (center[0]-10, center[1]+10), (center[0]+10, center[1]+10)])
        elif self.type == "queen":
            pygame.draw.rect(screen, piece_color, (center[0] - 15, center[1] - 15, 30, 30))
        elif self.type == "king":
            pygame.draw.rect(screen, piece_color, (center[0] - 10, center[1] - 10, 20, 20))

# Buat bidak catur
def create_pieces():
    pieces = []
    piece_types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

    for i, piece_type in enumerate(piece_types):
        pieces.append(Piece("white", piece_type))
        pieces[i].rect = pygame.Rect(i * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE)

    for i, piece_type in enumerate(piece_types):
        pieces.append(Piece("black", piece_type))
        pieces[i + len(piece_types)].rect = pygame.Rect(i * SQUARE_SIZE, 7 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

    for col in range(COLS):
        pieces.append(Piece("white", "pawn"))
        pieces[-1].rect = pygame.Rect(col * SQUARE_SIZE, 1 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pieces.append(Piece("black", "pawn"))
        pieces[-1].rect = pygame.Rect(col * SQUARE_SIZE, 6 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

    return pieces

def valid_move(piece, start_pos, end_pos):
    # Validasi langkah dasar (hanya untuk contoh, tidak mencakup semua aturan)
    dx = abs(end_pos[0] - start_pos[0])
    dy = abs(end_pos[1] - start_pos[1])

    if piece.type == "pawn":
        return (dy == 1 and dx == 0) or (dy == 1 and dx == 1 and piece.color == "black") or (dy == 1 and dx == 1 and piece.color == "white")
    elif piece.type == "rook":
        return (dx == 0 or dy == 0)
    elif piece.type == "knight":
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
    elif piece.type == "bishop":
        return dx == dy
    elif piece.type == "queen":
        return (dx == 0 or dy == 0 or dx == dy)
    elif piece.type == "king":
        return (dx <= 1 and dy <= 1)

def main():
    clock = pygame.time.Clock()
    pieces = create_pieces()
    selected_piece = None
    turn = "white"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // SQUARE_SIZE
                row = mouse_pos[1] // SQUARE_SIZE
                if selected_piece is None:
                    for piece in pieces:
                        if piece.rect.collidepoint(mouse_pos) and piece.color == turn:
                            selected_piece = piece
                            break
                else:
                    if valid_move(selected_piece, (selected_piece.rect.x // SQUARE_SIZE, selected_piece.rect.y // SQUARE_SIZE), (col, row)):
                        selected_piece.rect.topleft = (col * SQUARE_SIZE, row * SQUARE_SIZE)
                        turn = "black" if turn == "white" else "white"  # Ganti giliran
                    selected_piece = None

        draw_board()
        for piece in pieces:
            piece.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
