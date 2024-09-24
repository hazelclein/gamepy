import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 40
FPS = 60
GRAVITY = 1

# Warna
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Pengaturan layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft-like Game")

# Kelas untuk blok
class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Kelas untuk pemain
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 100, BLOCK_SIZE, BLOCK_SIZE)
        self.speed_y = 0
        self.on_ground = False

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def jump(self):
        if self.on_ground:
            self.speed_y = -15

    def update(self):
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.speed_y = 0
        else:
            self.on_ground = False

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

# Kelas untuk dunia
class World:
    def __init__(self):
        self.blocks = [Block(x * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BROWN) for x in range(WIDTH // BLOCK_SIZE)]
        for x in range(5):
            self.blocks.append(Block(x * BLOCK_SIZE, HEIGHT - 2 * BLOCK_SIZE, GREEN))

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    def remove_block(self, pos):
        for block in self.blocks:
            if block.rect.collidepoint(pos):
                self.blocks.remove(block)
                break

    def add_block(self, pos):
        x, y = pos
        new_block = Block(x // BLOCK_SIZE * BLOCK_SIZE, y // BLOCK_SIZE * BLOCK_SIZE, BROWN)
        self.blocks.append(new_block)

def main():
    clock = pygame.time.Clock()
    player = Player()
    world = World()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_SPACE]:
            player.jump()
        if keys[pygame.K_e]:  # Menggali atau menempatkan blok
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:  # Klik kiri untuk menggali
                world.remove_block(pos)
            elif pygame.mouse.get_pressed()[2]:  # Klik kanan untuk menempatkan
                world.add_block(pos)

        player.move(dx)
        player.update()

        # Gambar semua elemen
        screen.fill(WHITE)
        world.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
      