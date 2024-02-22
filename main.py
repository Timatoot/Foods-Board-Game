import pygame
import sys

# Initialize Pygame
pygame.init()

screen_width = 800
screen_height = 800

current_square = 1

locations = {
    1: (113, 58),
    2: (113, 161),
    3: (227, 161),
    4: (340, 161),
    5: (453, 161),
    6: (566, 161),
    7: (682, 161),
    8: (682, 266),
    9: (682, 383),
    10: (565, 383),
    11: (452, 383),
    12: (339, 383),
    13: (226, 383),
    14: (113, 383),
    15: (113, 499),
    16: (113, 619),
    17: (226, 619),
    18: (339, 619),
    19: (454, 619),
    20: (566, 619),
    21: (682, 619),
    22: (682, 722)
}

# square 1: 113, 58
# square 2: 113, 161
# square 3: 227, 161
# square 4: 340, 161
# square 5: 453, 161
# square 6: 566, 161
# square 7: 682, 161
# square 8: 682, 266
# square 9: 682, 383
# square 10: 565, 383
# square 11: 452, 383
# square 12: 339, 383
# square 13: 226, 383
# square 14: 113, 383
# square 15: 113, 499
# square 16: 113, 619
# square 17: 226, 619
# square 18: 339, 619
# square 19: 454, 619
# square 20: 566, 619
# square 21: 682, 619
# square 22: 682, 722

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Pygame Project")

# Load the background image
background_image = pygame.image.load("Background.png")

background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def draw_circle(square_number):
    x, y = locations[square_number]
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 10)

def main():
    global current_square
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move left
                    current_square = max(1, current_square - 1)  # Ensure current_square doesn't go below 1
                elif event.key == pygame.K_RIGHT:
                    # Move right
                    current_square = min(len(locations), current_square + 1)  # Ensure current_square doesn't exceed the number of squares


        # Draw the background image
        screen.blit(background_image, [0, 0])

        draw_circle(current_square)

        # Update the display
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
