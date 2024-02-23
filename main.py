import pygame
import sys
import random
 
pygame.init()

screen_width = 800
screen_height = 800

current_square = 1
current_roll = 1

rolled = False

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
 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Food Detective")
 
background_image = pygame.image.load("assets/Background.png")

background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def draw_circle(square_number):
    x, y = locations[square_number]
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 10)

def roll_dice():
    return random.randint(1, 6)

def roll_button():
    global current_roll
    global rolled

    button_x = 700
    button_y = 20
    button_width = 80
    button_height = 80

    roll = pygame.image.load("assets/Roll" + str(current_roll) + ".png")
    roll = pygame.transform.scale(roll, (button_width, button_height))
    screen.blit(roll, (button_x, button_y))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button_x + button_width > mouse[0] > button_x and button_y + button_height > mouse[1] > button_y:
        if click[0] == 1 and not rolled:
            current_roll = roll_dice()
            rolled = True
        elif click[0] == 0 and rolled:
            rolled = False

def main():
    global current_square
    target_forward_square = 1
    target_reverse_square = 1
 
    while True:
        if rolled:
            target_forward_square = min(len(locations), current_square + current_roll)
            target_reverse_square = max(1, current_square - current_roll)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_square != target_reverse_square:
                    current_square = max(1, current_square - 1)  # Ensure current_square doesn't go below 1
                elif event.key == pygame.K_RIGHT and current_square != target_forward_square:
                    current_square = min(len(locations), current_square + 1)  # Ensure current_square doesn't exceed the number of squares
 
        screen.blit(background_image, [0, 0])

        draw_circle(current_square)
        roll_button()

        pygame.display.flip()
 
if __name__ == "__main__":
    main()
