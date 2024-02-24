import pygame
import sys
import random
 
pygame.init()

screen_width = 800
screen_height = 800

current_square = 1
current_roll = 1

rolled = False

at_target_square = False

can_move = False

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

def pop_up_message(message):
    font = pygame.font.Font(None, 36)
    lines = message.split('\n')  # Split the message into lines
    
    # Calculate the starting y position so the block of text is centered
    block_height = len(lines) * font.get_height()
    y_start = screen_height // 2 - block_height // 2
    
    screen.fill((0, 0, 0))  # Fill the screen with black before displaying the message

    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, y_start + i * font.get_height()))
        screen.blit(text, text_rect)
    
    pygame.display.flip()
    # Event loop to wait for ESC key press or mouse button click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Close popup when ESC is pressed
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # Close popup on mouse click
            
def get_clue_from_file(file_name):
    with open(file_name, "r") as file:
        return file.read()

def clear_text_file(file_name):
    with open(file_name, "w") as file:
        file.write("")

def write_clue_to_file(file_name, clue):
    with open(file_name, "a") as file:
        file.write("\n\n" + clue)

def add_new_clue(clue):
    write_clue_to_file("known clues.txt", clue)

def roll_button():
    global current_roll
    global rolled
    global at_target_square
    global can_move

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
        if click[0] == 1 and not rolled and (at_target_square or not can_move):
            can_move = True
            current_roll = roll_dice()
            rolled = True
            at_target_square = False
            print(current_roll)
        elif click[0] == 0 and rolled and not at_target_square:
            rolled = False

def see_clues():
    button_width = 80
    button_height = 80
    button_x = 20
    button_y = screen_height - button_height - 20

    button_image = pygame.image.load("assets/clue button.png")
    button_image = pygame.transform.scale(button_image, (button_width, button_height))
    screen.blit(button_image, (button_x, button_y))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button_x + button_width > mouse[0] > button_x and button_y + button_height > mouse[1] > button_y:
        if click[0] == 1:
            clues_file = "known clues.txt"
            with open(clues_file, "r") as file:
                clues = file.read()
            pop_up_message(clues)

def main():
    global current_square
    global at_target_square

    target_forward_square = 1
    target_reverse_square = 1
    clue = 1

    clear_text_file("known clues.txt")
 
    while True:
        if rolled:
            target_forward_square = min(len(locations), current_square + current_roll)
            target_reverse_square = max(1, current_square - current_roll)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_square != target_reverse_square and not at_target_square:
                    current_square = max(1, current_square - 1)  # Ensure current_square doesn't go below 1
                elif event.key == pygame.K_RIGHT and current_square != target_forward_square and not at_target_square:
                    current_square = min(len(locations), current_square + 1)  # Ensure current_square doesn't exceed the number of squares
                elif target_forward_square == current_square or target_reverse_square == current_square:
                    at_target_square = True
                    pop_up_message(get_clue_from_file("assets/clues/generic/test" + str(clue) + ".txt"))
                    add_new_clue(get_clue_from_file("assets/clues/generic/test" + str(clue) + ".txt"))
                    clue += 1
 
        screen.blit(background_image, [0, 0])

        draw_circle(current_square)
        roll_button()
        see_clues()

        pygame.display.flip()
 
if __name__ == "__main__":
    main()
