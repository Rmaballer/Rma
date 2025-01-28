import pygame
import random

pygame.init()

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (0, 0, 139)

colors = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont('comicsans', 30)

class Tetrimino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, surface):
        for i, row in enumerate(self.shape):
            for j, value in enumerate(row):
                if value:
                    pygame.draw.rect(surface, self.color, (self.x * BLOCK_SIZE + j * BLOCK_SIZE, self.y * BLOCK_SIZE + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_grid(surface):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for i in range(ROWS):
        pygame.draw.line(surface, WHITE, (0, i * BLOCK_SIZE), (WIDTH, i * BLOCK_SIZE))
    for i in range(COLS):
        pygame.draw.line(surface, WHITE, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, HEIGHT))


def clear_lines():
    global grid
    for i in range(ROWS - 1, -1, -1):
        if all(grid[i][j] != (0, 0, 0) for j in range(COLS)):
            del grid[i]
            grid = [[(0, 0, 0)] * COLS] + grid
            return True
    return False


def draw_text(text, x, y):
    label = font.render(text, 1, WHITE)
    screen.blit(label, (x, y))


def main():
    clock = pygame.time.Clock()
    running = True
    score = 0
    current_tetrimino = Tetrimino(random.choice(SHAPES), random.choice(colors))

    while running:
        screen.fill((0, 0, 0))

        draw_grid(screen)
        current_tetrimino.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_tetrimino.move(-1, 0)
            if not valid_move(current_tetrimino):
                current_tetrimino.move(1, 0)

        if keys[pygame.K_RIGHT]:
            current_tetrimino.move(1, 0)
            if not valid_move(current_tetrimino):
                current_tetrimino.move(-1, 0)

        if keys[pygame.K_DOWN]:
            current_tetrimino.move(0, 1)
            if not valid_move(current_tetrimino):
                current_tetrimino.move(0, -1)

        if keys[pygame.K_UP]:
            current_tetrimino.rotate()
            if not valid_move(current_tetrimino):
                current_tetrimino.rotate()
                current_tetrimino.rotate()
                current_tetrimino.rotate()

        current_tetrimino.move(0, 1)
        if not valid_move(current_tetrimino):
            current_tetrimino.move(0, -1)
            place_tetrimino(current_tetrimino)
            clear_lines()
            current_tetrimino = Tetrimino(random.choice(SHAPES), random.choice(colors))
            if not valid_move(current_tetrimino):
                running = False

        draw_text(f"Score: {score}", 10, 10)
        pygame.display.update()

        clock.tick(5)


def valid_move(tetrimino):
    for i, row in enumerate(tetrimino.shape):
        for j, value in enumerate(row):
            if value:
                if tetrimino.x + j < 0 or tetrimino.x + j >= COLS or tetrimino.y + i >= ROWS:
                    return False
                if grid[tetrimino.y + i][tetrimino.x + j] != (0, 0, 0):
                    return False
    return True


def place_tetrimino(tetrimino):
    for i, row in enumerate(tetrimino.shape):
        for j, value in enumerate(row):
            if value:
                grid[tetrimino.y + i][tetrimino.x + j] = tetrimino.color


if __name__ == "__main__":
    main()
    pygame.quit()