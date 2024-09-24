import curses
import random

# Inisialisasi layar
stdscr = curses.initscr()
curses.curs_set(0)  # Sembunyikan kursor
sh, sw = stdscr.getmaxyx()  # Dapatkan ukuran layar
w = curses.newwin(sh, sw, 0, 0)  # Buat jendela baru
w.keypad(1)  # Aktifkan input keypad
w.timeout(100)  # Timeout untuk pembaruan layar

# Inisialisasi snake dan makanan
snk_x = sw // 4
snk_y = sh // 2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]
food = [sh // 2, sw // 2]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)  # Tambahkan makanan

# Inisialisasi arah
key = 'd'  # Mulai bergerak ke kanan

while True:
    next_key = w.getch()  # Dapatkan input dari pengguna
    if next_key in [ord('w'), ord('a'), ord('s'), ord('d')]:
        key = next_key  # Update arah jika input valid

    # Hitung posisi kepala snake
    new_head = [snake[0][0], snake[0][1]]

    if key == ord('s'):  # Down
        new_head[0] += 1
    if key == ord('w'):  # Up
        new_head[0] -= 1
    if key == ord('a'):  # Left
        new_head[1] -= 1
    if key == ord('d'):  # Right
        new_head[1] += 1

    # Cek apakah snake memakan makanan
    snake.insert(0, new_head)
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh - 1),
                random.randint(1, sw - 1)
            ]
            food = nf if nf not in snake else None
        w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
    else:
        tail = snake.pop()  # Hapus ekor
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Cek apakah snake menabrak diri sendiri atau dinding
    if (snake[0][0] in [0, sh]) or (snake[0][1] in [0, sw]) or (snake[0] in snake[1:]):
        curses.endwin()
        quit()

    # Gambar snake
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
