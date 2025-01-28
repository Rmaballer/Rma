import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

font = pygame.font.SysFont("comicsans", 40)

grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
grid[1][1] = 0

walls = [
    (5, 5), (5, 6), (5, 7), (6, 5), (7, 5),
    (3, 3), (3, 4), (3, 5), (4, 5), (4, 6)
]
for wall in walls:
    grid[wall[1]][wall[0]] = 2

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * GRID_SIZE, row * GRID_SIZE
            if grid[row][col] == 1:
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 6)
            elif grid[row][col] == 2:
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))

def draw_pacman():
    pygame.draw.circle(
        screen, YELLOW, 
        (pacman_x + GRID_SIZE // 2, pacman_y + GRID_SIZE // 2), 
        GRID_SIZE // 2 - 2
    )

def main():
    global pacman_x, pacman_y, direction
    pacman_x, pacman_y = GRID_SIZE * 1, GRID_SIZE * 1
    pacman_speed = GRID_SIZE
    direction = None

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"

        next_x, next_y = pacman_x, pacman_y
        if direction == "UP":
            next_y -= pacman_speed
        elif direction == "DOWN":
            next_y += pacman_speed
        elif direction == "LEFT":
            next_x -= pacman_speed
        elif direction == "RIGHT":
            next_x += pacman_speed

        if 0 <= next_x < WIDTH and 0 <= next_y < HEIGHT:
            col, row = next_x // GRID_SIZE, next_y // GRID_SIZE
            if grid[row][col] != 2:
                pacman_x, pacman_y = next_x, next_y

        col, row = pacman_x // GRID_SIZE, pacman_y // GRID_SIZE
        if grid[row][col] == 1:
            grid[row][col] = 0

        draw_grid()
        draw_pacman()

        if all(grid[row][col] != 1 for row in range(ROWS) for col in range(COLS)):
            win_text = font.render("You Win!", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

        pygame.display.update()
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    main()
