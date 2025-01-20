import pygame
import random
import sys
import json
from operator import itemgetter



# Inicializálás
pygame.init()

# Képernyő méretek
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pálinkavadász")

# Játék sebesség
clock = pygame.time.Clock()
FPS = 60

# Képek betöltése
player_image = pygame.image.load("stickman.png")
bottle_image = pygame.image.load("palinka.png")
obstacle_image = pygame.image.load("pirosblock.jpg")

# Képek méretei
player_size = 50
bottle_size = 40
obstacle_size = 60

# Képek átméretezése
player_image = pygame.transform.scale(player_image, (player_size, player_size))
bottle_image = pygame.transform.scale(bottle_image, (bottle_size, bottle_size))
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size, obstacle_size))

# Leaderboard fájl
LEADERBOARD_FILE = "leaderboard.json"

# Leaderboard betöltése
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Leaderboard mentése
def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

# Leaderboard megjelenítése
def display_leaderboard():
    leaderboard = load_leaderboard()
    leaderboard = sorted(leaderboard, key=itemgetter("score"), reverse=True)[:5]

    screen.fill((173, 216, 230))  # Kék háttér
    font = pygame.font.SysFont("Arial", 40)
    title = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 3, 50))

    font = pygame.font.SysFont("Arial", 30)
    y_offset = 150
    for i, entry in enumerate(leaderboard):
        text = font.render(f"{i + 1}. {entry['name']} - {entry['score']} pont", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 4, y_offset))
        y_offset += 50

    font = pygame.font.SysFont("Arial", 25)
    instruction_text = font.render("Nyomj [I]-t az új játékhoz, vagy [N]-t a kilépéshez", True, (255, 255, 255))
    screen.blit(instruction_text, (WIDTH // 8, HEIGHT - 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    return True  # Új játék indítása
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

# Játékos név bevitele
def get_player_name():
    font = pygame.font.SysFont("Arial", 50)
    player_name = ""
    input_active = True

    while input_active:
        screen.fill((173, 216, 230))  # Kék háttér
        text = font.render("Add meg a neved:", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 4, HEIGHT // 3))
        name_display = font.render(player_name, True, (0, 0, 0))
        screen.blit(name_display, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

    return player_name

# Játék vége képernyő
def game_over_screen(score, player_name):
    screen.fill((0, 0, 0))  # Fekete háttér
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(f"Játék vége! Pontszám: {score}", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 4, HEIGHT // 3))

    sub_text = font.render("Nyomj [I]-t az új játékhoz, [N]-t a kilépéshez", True, (255, 255, 255))
    screen.blit(sub_text, (WIDTH // 8, HEIGHT // 2))
    pygame.display.flip()

    # Várakozás néhány másodpercig
    pygame.time.wait(3000)  # 3000 ms = 3 másodperc

    # Pontszám mentése a leaderboardba
    leaderboard = load_leaderboard()
    leaderboard.append({"name": player_name, "score": score})
    save_leaderboard(leaderboard)

    # Leaderboard megjelenítése
    if display_leaderboard():
        game_loop()

# Játék főciklusa
def game_loop():
    global score, obstacles, obstacle_speeds, obstacle_directions

    player_pos = [WIDTH // 2, HEIGHT - 100]
    bottle_pos = [random.randint(0, WIDTH - bottle_size), random.randint(0, HEIGHT // 2)]
    bottle_speed = [random.choice([-5, 5]), random.choice([-5, 5])]

    obstacles = []
    for _ in range(5):
        while True:
            obs_x = random.randint(0, WIDTH - obstacle_size)
            obs_y = random.randint(HEIGHT // 2, HEIGHT - obstacle_size)
            if abs(obs_x - player_pos[0]) > 100 and abs(obs_y - player_pos[1]) > 100:
                obstacles.append([obs_x, obs_y])
                break

    moving_obstacles = [0, 1, 2]
    obstacle_speeds = [[0, 4], [0, -4], [4, 0]]
    obstacle_directions = [1, 1, 1]

    running = True
    score = 0
    player_facing = "right"
    while running:
        screen.fill((173, 216, 230))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_pos[0] > 0:
            player_pos[0] -= 10
            player_facing = "left"
        if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += 10
            player_facing = "right"
        if keys[pygame.K_w] and player_pos[1] > 0:
            player_pos[1] -= 10
        if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += 10

        if player_facing == "right":
            player_img = pygame.transform.flip(player_image, True, False)
        else:
            player_img = player_image

        bottle_pos[0] += bottle_speed[0]
        bottle_pos[1] += bottle_speed[1]

        if bottle_pos[0] <= 0 or bottle_pos[0] >= WIDTH - bottle_size:
            bottle_speed[0] = -bottle_speed[0]
        if bottle_pos[1] <= 0 or bottle_pos[1] >= HEIGHT - bottle_size:
            bottle_speed[1] = -bottle_speed[1]

        for i in moving_obstacles:
            obstacles[i][0] += obstacle_speeds[i][0] * obstacle_directions[i]
            obstacles[i][1] += obstacle_speeds[i][1] * obstacle_directions[i]

            if obstacles[i][0] <= 0 or obstacles[i][0] >= WIDTH - obstacle_size:
                obstacle_directions[i] *= -1
            if obstacles[i][1] <= 0 or obstacles[i][1] >= HEIGHT - obstacle_size:
                obstacle_directions[i] *= -1

        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        bottle_rect = pygame.Rect(bottle_pos[0], bottle_pos[1], bottle_size, bottle_size)

        if player_rect.colliderect(bottle_rect):
            score += 1
            bottle_pos = [random.randint(0, WIDTH - bottle_size), random.randint(0, HEIGHT // 2)]

        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_size, obstacle_size)
            if player_rect.colliderect(obstacle_rect):
                running = False

        # Elemek kirajzolása
        screen.blit(player_img, (player_pos[0], player_pos[1]))
        screen.blit(bottle_image, (bottle_pos[0], bottle_pos[1]))
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # Pontszám megjelenítése
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Pontszám: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    game_over_screen(score, get_player_name())

# Program indítása
if __name__ == "__main__":
    game_loop()

