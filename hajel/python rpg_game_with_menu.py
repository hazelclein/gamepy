import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (255, 0, 0)
BULLET_COLOR = (255, 255, 0)
POWERUP_COLOR = (0, 255, 0)
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 5
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
POWERUP_SIZE = 30

# Pengaturan layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game with Menu and Pause")

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.health = 150
        self.experience = 0
        self.level = 1
        self.speed = PLAYER_SPEED

    def move(self, dx, dy):
        if 0 <= self.rect.x + dx <= WIDTH - PLAYER_SIZE:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= HEIGHT - PLAYER_SIZE:
            self.rect.y += dy

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.health += 20
        print(f"Level Up! Now at Level {self.level}, Health: {self.health}")

    def draw_health_bar(self):
        health_bar_length = 200
        health_ratio = self.health / 100
        pygame.draw.rect(screen, BLACK, (10, 10, health_bar_length, 20))  # Background bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, health_bar_length * health_ratio, 20))  # Health bar

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.health = 50

    def move_towards_player(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += ENEMY_SPEED
        elif self.rect.x > player_rect.x:
            self.rect.x -= ENEMY_SPEED
        if self.rect.y < player_rect.y:
            self.rect.y += ENEMY_SPEED
        elif self.rect.y > player_rect.y:
            self.rect.y -= ENEMY_SPEED

    def is_alive(self):
        return self.health > 0

class Boss:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
        self.health = 300

    def move_towards_player(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += ENEMY_SPEED // 2  # Boss bergerak lebih lambat
        elif self.rect.x > player_rect.x:
            self.rect.x -= ENEMY_SPEED // 2
        if self.rect.y < player_rect.y:
            self.rect.y += ENEMY_SPEED // 2
        elif self.rect.y > player_rect.y:
            self.rect.y -= ENEMY_SPEED // 2

    def is_alive(self):
        return self.health > 0

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE)
        self.direction = direction

    def move(self):
        if self.direction == 'left':
            self.rect.x -= BULLET_SPEED
        elif self.direction == 'right':
            self.rect.x += BULLET_SPEED
        elif self.direction == 'up':
            self.rect.y -= BULLET_SPEED
        elif self.direction == 'down':
            self.rect.y += BULLET_SPEED

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - POWERUP_SIZE), random.randint(0, HEIGHT - POWERUP_SIZE), POWERUP_SIZE, POWERUP_SIZE)
        self.type = random.choice(['health', 'speed'])

def draw_text(text, size, color, surface, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def game_over():
    while True:
        screen.fill(WHITE)
        draw_text("Game Over", 50, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press Q to Quit", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Main Menu", 50, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press S to Start", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press Q to Quit", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def level_selection():
    while True:
        screen.fill(WHITE)
        draw_text("Level Selection", 50, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press 1 for Level 1", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press 2 for Level 2", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Press Q to Quit", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop(level):
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy(random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)) for _ in range(5)]
    bullets = []
    power_ups = []
    boss = None
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:  # Kiri
                player.move(-player.speed, 0)
            if keys[pygame.K_d]:  # Kanan
                player.move(player.speed, 0)
            if keys[pygame.K_w]:  # Atas
                player.move(0, -player.speed)
            if keys[pygame.K_s]:  # Bawah
                player.move(0, player.speed)
            if keys[pygame.K_SPACE]:  # Menembak
                bullet_direction = 'up' if keys[pygame.K_w] else 'down' if keys[pygame.K_s] else 'left' if keys[pygame.K_a] else 'right' if keys[pygame.K_d] else None
                if bullet_direction:
                    bullet_x = player.rect.centerx
                    bullet_y = player.rect.centery
                    bullets.append(Bullet(bullet_x, bullet_y, bullet_direction))

            # Update posisi peluru
            for bullet in bullets[:]:
                bullet.move()
                if bullet.rect.x < 0 or bullet.rect.x > WIDTH or bullet.rect.y < 0 or bullet.rect.y > HEIGHT:
                    bullets.remove(bullet)

            # Gerakan musuh dan cek tumbukan
            for enemy in enemies[:]:
                enemy.move_towards_player(player.rect)

                if player.rect.colliderect(enemy.rect):
                    player.health -= 1
                    print(f"Player Health: {player.health}")
                    if player.health <= 0:
                        game_over()
                        return  # Restart game loop

            # Cek tumbukan peluru dengan musuh
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if enemy.is_alive() and bullet.rect.colliderect(enemy.rect):
                        enemy.health -= 50
                        bullets.remove(bullet)
                        if not enemy.is_alive():
                            player.gain_experience(50)
                        break

            # Menghasilkan power-up secara acak
            if random.random() < 0.01:  # 1% kemungkinan menghasilkan power-up
                power_ups.append(PowerUp())

            # Cek tumbukan power-up dengan pemain
            for power_up in power_ups[:]:
                if player.rect.colliderect(power_up.rect):
                    if power_up.type == 'health':
                        player.health += 20
                        print(f"Health Increased! Current Health: {player.health}")
                    elif power_up.type == 'speed':
                        player.speed += 2
                        print(f"Speed Increased! Current Speed: {player.speed}")
                    power_ups.remove(power_up)

            # Spawn Boss setelah mengalahkan semua musuh
            if not any(enemy.is_alive() for enemy in enemies) and boss is None:
                boss = Boss()
                print("Boss has appeared!")

            # Gerakan bos dan cek tumbukan
            if boss and boss.is_alive():
                boss.move_towards_player(player.rect)
                if player.rect.colliderect(boss.rect):
                    player.health -= 1
                    print(f"Player Health: {player.health}")
                    if player.health <= 0:
                        game_over()
                        return  # Restart game loop

                # Cek tumbukan peluru dengan bos
                for bullet in bullets[:]:
                    if boss.is_alive() and bullet.rect.colliderect(boss.rect):
                        boss.health -= 50
                        bullets.remove(bullet)
                        if not boss.is_alive():
                            print("Boss Defeated!")

            # Gambar semua elemen
            screen.fill(WHITE)
            pygame.draw.rect(screen, PLAYER_COLOR, player.rect)
            player.draw_health_bar()  # Gambar bar kesehatan
            for enemy in enemies:
                if enemy.is_alive():
                    pygame.draw.rect(screen, ENEMY_COLOR, enemy.rect)
            
            for bullet in bullets:
                pygame.draw.rect(screen, BULLET_COLOR, bullet.rect)

            if boss and boss.is_alive():
                pygame.draw.rect(screen, (255, 0, 255), boss.rect)  # Warna bos

            for power_up in power_ups:
                pygame.draw.rect(screen, POWERUP_COLOR, power_up.rect)

        else:
            draw_text("Paused", 50, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Press P to Resume", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2)
            draw_text("Press Q to Quit", 30, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        main_menu()
        level = level_selection()
        game_loop(level)

if __name__ == "__main__":
    main()
