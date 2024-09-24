import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Pengaturan layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle dan Ball
paddle_width, paddle_height = 15, 100
ball_size = 15

# Posisi dan skor
player1_pos = [50, (HEIGHT - paddle_height) // 2]
player2_pos = [WIDTH - 50 - paddle_width, (HEIGHT - paddle_height) // 2]
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_velocity = [3, 3]
player1_score = 0
player2_score = 0
power_up_active = False
power_up_pos = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
power_up_type = ""
power_up_timer = 0
power_up_spawn_time = 1000  # Interval waktu untuk spawn power-up (ms)
last_power_up_spawn = pygame.time.get_ticks()
paused = False

# Font untuk menampilkan skor dan menu
font = pygame.font.Font(None, 36)

def draw_menu():
    screen.fill(BLACK)
    title_text = font.render("Pong Game", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    exit_text = font.render("Press ESC to Exit", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

def reset_game():
    global player1_pos, player2_pos, ball_pos, ball_velocity, player1_score, player2_score, power_up_active, power_up_pos, power_up_type
    player1_pos = [50, (HEIGHT - paddle_height) // 2]
    player2_pos = [WIDTH - 50 - paddle_width, (HEIGHT - paddle_height) // 2]
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_velocity = [3, 3]
    player1_score = 0
    player2_score = 0
    power_up_active = False
    power_up_type = ""
    spawn_power_up()

def spawn_power_up():
    global power_up_pos, power_up_type
    power_up_pos = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
    power_up_type = random.choice(['enlarge', 'speed', 'slow', 'normal'])

def draw_power_up():
    if power_up_type == 'enlarge':
        color = GREEN
    elif power_up_type == 'speed':
        color = BLUE
    elif power_up_type == 'slow':
        color = RED
    else:
        color = WHITE

    pygame.draw.rect(screen, color, (power_up_pos[0], power_up_pos[1], 10, 10))

# Game Loop
menu_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if menu_active:
        draw_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Mulai game saat ENTER ditekan
            menu_active = False
            reset_game()
        if keys[pygame.K_ESCAPE]:  # Keluar saat ESC ditekan
            pygame.quit()
            sys.exit()
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:  # Pause game saat P ditekan
            paused = not paused

        if not paused:
            if keys[pygame.K_w] and player1_pos[1] > 0:
                player1_pos[1] -= 5
            if keys[pygame.K_s] and player1_pos[1] < HEIGHT - paddle_height:
                player1_pos[1] += 5
            if keys[pygame.K_UP] and player2_pos[1] > 0:
                player2_pos[1] -= 5
            if keys[pygame.K_DOWN] and player2_pos[1] < HEIGHT - paddle_height:
                player2_pos[1] += 5

            # Pergerakan bola
            ball_pos[0] += ball_velocity[0]
            ball_pos[1] += ball_velocity[1]

            # Cek tabrakan dengan paddle
            if (ball_pos[0] <= player1_pos[0] + paddle_width and player1_pos[1] < ball_pos[1] < player1_pos[1] + paddle_height) or \
               (ball_pos[0] >= player2_pos[0] - ball_size and player2_pos[1] < ball_pos[1] < player2_pos[1] + paddle_height):
                ball_velocity[0] = -ball_velocity[0]
                ball_velocity[0] *= 1.6  # Tambahkan kecepatan saat mengenai paddle
                ball_velocity[1] *= 1.1

            # Cek tabrakan dengan dinding
            if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - ball_size:
                ball_velocity[1] = -ball_velocity[1]

            # Cek jika bola keluar
            if ball_pos[0] < 0:
                player2_score += 1  # Pemain 2 mendapatkan poin
                ball_pos = [WIDTH // 2, HEIGHT // 2]  # Reset bola ke tengah
                ball_velocity = [3, 3]  # Reset kecepatan bola
                spawn_power_up()  # Spawn power-up
            elif ball_pos[0] > WIDTH:
                player1_score += 1  # Pemain 1 mendapatkan poin
                ball_pos = [WIDTH // 2, HEIGHT // 2]
                ball_velocity = [3, 3]
                spawn_power_up()  # Spawn power-up

            # Cek jika pemain mendapatkan power-up
            if power_up_active and player1_pos[0] < power_up_pos[0] < player1_pos[0] + paddle_width and player1_pos[1] < power_up_pos[1] < player1_pos[1] + paddle_height:
                power_up_active = False
                if power_up_type == 'enlarge':
                    paddle_height += 20  # Memperbesar paddle pemain 1
                elif power_up_type == 'speed':
                    ball_velocity[0] *= 1.5  # Meningkatkan kecepatan bola
                elif power_up_type == 'slow':
                    ball_velocity[0] *= 0.5  # Mengurangi kecepatan bola

            if power_up_active and player2_pos[0] < power_up_pos[0] < player2_pos[0] + paddle_width and player2_pos[1] < power_up_pos[1] < player2_pos[1] + paddle_height:
                power_up_active = False
                if power_up_type == 'enlarge':
                    paddle_height += 20  # Memperbesar paddle pemain 2
                elif power_up_type == 'speed':
                    ball_velocity[0] *= 1.5  # Meningkatkan kecepatan bola
                elif power_up_type == 'slow':
                    ball_velocity[0] *= 0.5  # Mengurangi kecepatan bola

            # Spawn power-up lebih cepat
            current_time = pygame.time.get_ticks()
            if current_time - last_power_up_spawn > power_up_spawn_time:
                spawn_power_up()
                last_power_up_spawn = current_time

            # Menggambar
            screen.fill(BLACK)
            pygame.draw.rect(screen, WHITE, (player1_pos[0], player1_pos[1], paddle_width, paddle_height))
            pygame.draw.rect(screen, WHITE, (player2_pos[0], player2_pos[1], paddle_width, paddle_height))
            pygame.draw.ellipse(screen, WHITE, (ball_pos[0], ball_pos[1], ball_size, ball_size))

            # Menggambar power-up
            if not power_up_active:
                draw_power_up()
                power_up_active = True

            # Tampilkan skor
            score_text = font.render(f"{player1_score}  |  {player2_score}", True, WHITE)
            screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, 20))

        else:
            # Menampilkan pesan pause
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
