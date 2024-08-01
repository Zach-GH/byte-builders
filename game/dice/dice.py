#!/usr/bin/env python3

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Dice Roller Illusion")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dice face positions
dice_faces = {
    1: [(3, 3)],
    2: [(1, 1), (5, 5)],
    3: [(1, 1), (3, 3), (5, 5)],
    4: [(1, 1), (1, 5), (5, 1), (5, 5)],
    5: [(1, 1), (1, 5), (3, 3), (5, 1), (5, 5)],
    6: [(1, 1), (1, 3), (1, 5), (5, 1), (5, 3), (5, 5)]
}

def draw_dice(x, y, size, number):
    """Draw a dice with the given number at position (x, y) with the given size."""
    shadow_offset = size // 10
    
    # Draw shadow
    pygame.draw.polygon(win, (50, 50, 50), [
        (x + shadow_offset, y + shadow_offset),
        (x + size + shadow_offset, y + shadow_offset),
        (x + size + shadow_offset, y + size + shadow_offset),
        (x + shadow_offset, y + size + shadow_offset)
    ])
    
    # Draw dice faces (front, top, side)
    front_face = [(x, y), (x + size, y), (x + size, y + size), (x, y + size)]
    top_face = [(x, y), (x + size, y), (x + size - shadow_offset, y - shadow_offset), (x - shadow_offset, y - shadow_offset)]
    side_face = [(x + size, y), (x + size, y + size), (x + size + shadow_offset, y + size + shadow_offset), (x + size + shadow_offset, y + shadow_offset)]
    
    pygame.draw.polygon(win, (200, 200, 200), top_face)  # Light shade
    pygame.draw.polygon(win, (100, 100, 100), side_face)  # Dark shade
    pygame.draw.polygon(win, WHITE, front_face)  # Main face
    
    for pos in dice_faces[number]:
        dot_x = x + (pos[0] * size) // 6
        dot_y = y + (pos[1] * size) // 6
        pygame.draw.circle(win, BLACK, (dot_x, dot_y), size // 12)

def main():
    clock = pygame.time.Clock()
    rolling = False
    dice_number = 1
    
    while True:
        win.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                rolling = True
        
        if rolling:
            dice_number = random.randint(1, 6)
            rolling = False
        
        draw_dice(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, dice_number)
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
