import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 1204
SCREEN_HEIGHT = 806
BLOCK_SIZE = 30  # Size of each block in the Tetris game
COLS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 60  # Frames per second
TOTAL_BLOCKS = 0  # Counter for the number of blocks

# Define colors
COLORS = [
    (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0),
    (255, 165, 0), (0, 0, 255), (255, 0, 0), (128, 0, 128),
    (255, 105, 180), (0, 128, 0), (255, 20, 147), (255, 69, 0),
    (138, 43, 226), (34, 139, 34), (255, 228, 225), (255, 140, 0),
    (218, 165, 32), (255, 255, 255), (128, 128, 128), (240, 230, 140)
]

# Define the Tetris shapes and their rotations
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define the font for the score display
font = pygame.font.SysFont('Arial', 24)

# Define a function to draw the grid
def draw_grid():
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))

# Define a function to draw a block
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Define a class to represent the falling block
class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def drop(self):
        self.y += 1

    def is_valid_position(self, grid):
        for iy, row in enumerate(self.shape):
            for ix, cell in enumerate(row):
                if cell:
                    if ix + self.x < 0 or ix + self.x >= COLS or iy + self.y >= ROWS or grid[iy + self.y][ix + self.x]:
                        return False
        return True

    def place_on_grid(self, grid):
        global TOTAL_BLOCKS
        for iy, row in enumerate(self.shape):
            for ix, cell in enumerate(row):
                if cell:
                    grid[iy + self.y][ix + self.x] = self.color
                    TOTAL_BLOCKS += 1

# Define a function to clear full rows
def clear_rows(grid):
    global TOTAL_BLOCKS
    for y in range(ROWS):
        if all(grid[y]):
            grid.pop(y)
            grid.insert(0, [None] * COLS)
            TOTAL_BLOCKS -= COLS

# Define a function to generate a new block
def generate_block():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return Block(shape, color)

# Function to display "Game Over" and ask if the player wants to play again
def ask_to_play_again():
    font = pygame.font.SysFont('Arial', 40)
    text = font.render("Game Over! Do you want to play again? (Y/N)", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Start a new game
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

    return False

# Main game loop
def main():
    global TOTAL_BLOCKS

    clock = pygame.time.Clock()
    grid = [[None] * COLS for _ in range(ROWS)]
    current_block = generate_block()
    game_over = False
    drop_speed = 1000  # Start the drop speed at 1 second (1000 ms)
    last_drop_time = pygame.time.get_ticks()

    while not game_over:
        screen.fill((0, 0, 0))  # Clear the screen
        draw_grid()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_block.x -= 1
                    if not current_block.is_valid_position(grid):
                        current_block.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_block.x += 1
                    if not current_block.is_valid_position(grid):
                        current_block.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_block.drop()
                    if not current_block.is_valid_position(grid):
                        current_block.y -= 1
                        current_block.place_on_grid(grid)
                        current_block = generate_block()
                        clear_rows(grid)
                elif event.key == pygame.K_UP:
                    current_block.rotate()
                    if not current_block.is_valid_position(grid):
                        current_block.rotate()
                        current_block.rotate()
                        current_block.rotate()

        # Slow down block drop as time progresses
        if pygame.time.get_ticks() - last_drop_time >= drop_speed:
            current_block.drop()
            if not current_block.is_valid_position(grid):
                current_block.y -= 1
                current_block.place_on_grid(grid)
                current_block = generate_block()
                clear_rows(grid)
            last_drop_time = pygame.time.get_ticks()

        # Draw the blocks on the grid
        for y in range(ROWS):
            for x in range(COLS):
                if grid[y][x]:
                    draw_block(x, y, grid[y][x])

        # Draw the current falling block
        for iy, row in enumerate(current_block.shape):
            for ix, cell in enumerate(row):
                if cell:
                    draw_block(current_block.x + ix, current_block.y + iy, current_block.color)

        # Draw the total block counter
        score_text = font.render(f'Total Blocks: {TOTAL_BLOCKS}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

        # If the game is over, prompt to play again
        if game_over:
            ask_to_play_again()

# Run the game
if __name__ == "__main__":
    main()
