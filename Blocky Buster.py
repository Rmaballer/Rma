import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
BLOCK_SIZE = WIDTH // COLS

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0)
]
IMPOSTER_OFFSET = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find the Imposters")

font = pygame.font.SysFont("comicsans", 40)

grid = []
imposter_positions = []
found_imposters = []

def generate_grid():
    global grid, imposter_positions
    grid = []
    imposter_positions = []
    base_color = random.choice(COLORS)
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            grid[row].append(base_color)
    while len(imposter_positions) < 4:
        pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if pos not in imposter_positions:
            imposter_positions.append(pos)
            row, col = pos
            grid[row][col] = (
                min(base_color[0] + IMPOSTER_OFFSET, 255),
                min(base_color[1] + IMPOSTER_OFFSET, 255),
                min(base_color[2] + IMPOSTER_OFFSET, 255),
            )

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            pygame.draw.rect(
                screen, 
                color, 
                (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                screen, 
                (0, 0, 0), 
                (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                1
            )

def main():
    global found_imposters
    clock = pygame.time.Clock()
    generate_grid()
    running = True
    lost = False

    while running:
        screen.fill((255, 255, 255))
        draw_grid()
        text = font.render(f"Found: {len(found_imposters)}/4", True, (0, 0, 0))
        screen.blit(text, (10, HEIGHT - 50))
        if len(found_imposters) == 4:
            win_text = font.render("You Win!", True, (0, 255, 0))
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False
        if lost:
            lose_text = font.render("You Lose!", True, (255, 0, 0))
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - lose_text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    col, row = x // BLOCK_SIZE, y // BLOCK_SIZE
                    if (row, col) in imposter_positions and (row, col) not in found_imposters:
                        found_imposters.append((row, col))
                        grid[row][col] = (255, 255, 255)
                    elif (row, col) not in imposter_positions:
                        lost = True
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
