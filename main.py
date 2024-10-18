import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")

# Create a grid
grid = [[random.randint(1, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
selected_candy = None

def handle_click(row, col):
    global selected_candy
    if selected_candy is None:
        selected_candy = (row, col)
    else:
        # Swap candies
        row1, col1 = selected_candy
        grid[row][col], grid[row1][col1] = grid[row1][col1], grid[row][col]
        selected_candy = None

def detect_match():
    match = set()
    
    # Horizontal matches
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                match.add((row, col))
                match.add((row, col + 1))
                match.add((row, col + 2))
    
    # Vertical matches
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                match.add((row, col))
                match.add((row + 1, col))
                match.add((row + 2, col))
    
    return match

def fill_empty_spaces():
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] == 0:  # If the cell is empty
                for r in range(row, 0, -1):
                    grid[r][col] = grid[r - 1][col]  # Move down candies
                grid[0][col] = random.randint(1, 3)  # Fill with a new candy

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] // CELL_SIZE
            row = event.pos[1] // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                handle_click(row, col)

    # Clear screen
    screen.fill(WHITE)

    # Draw candies
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            candy_type = grid[row][col]
            candy_color = (255, 0, 0) if candy_type == 1 else (0, 255, 0) if candy_type == 2 else (0, 0, 255)
            pygame.draw.rect(screen, candy_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Delete match candies
    matches = detect_match()
    if matches:
        for row, col in matches:
            grid[row][col] = 0
        fill_empty_spaces()  # Fill in the empty spaces after clearing matches

    # Update display
    pygame.display.flip()

pygame.quit()
