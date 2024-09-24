import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 0.5

# Pengaturan layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0

    def jump(self):
        self.velocity = -10

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y > HEIGHT:
            self.y = HEIGHT
        if self.y < 0:
            self.y = 0

    def draw(self, screen):
        pygame.draw.ellipse(screen, GREEN, (self.x, self.y, 34, 24))

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(200, 400)
        self.gap = 180

    def update(self):
        self.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, 50, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + self.gap, 50, HEIGHT - self.height - self.gap))

def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Flappy Bird Clone", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    exit_text = font.render("Press ESC to Exit", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

def game_loop():
    bird = Bird()
    pipes = []
    score = 0
    clock = pygame.time.Clock()
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not paused:
                    bird.jump()
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            bird.update()

            # Menambahkan pipa baru
            if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.update()
                # Menghitung skor saat burung melewati pipa
                if pipe.x + 50 < bird.x < pipe.x + 55:
                    score += 1

            pipes = [pipe for pipe in pipes if pipe.x > -50]

            # Cek tumbukan
            if bird.y >= HEIGHT or any(pipe.x < bird.x + 34 < pipe.x + 50 and (bird.y < pipe.height or bird.y + 24 > pipe.height + pipe.gap) for pipe in pipes):
                return score

            # Menggambar
            screen.fill(BLACK)
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)

            # Tampilkan skor
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        else:
            font = pygame.font.Font(None, 36)
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

# Game loop utama
while True:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                score = game_loop()
                print(f"Game Over! Your score: {score}")
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
