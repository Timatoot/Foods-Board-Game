import pygame
import sys
import random
import textwrap
 
pygame.init()

screen_width = 800
screen_height = 800

game_name = "Food Detective"

current_square = 1
current_roll = 1
rolls_remaining = 10

got_clue = False

rolled = False

at_target_square = False

can_move = False

categories = [
    [2, 6, 10, 14, 18],
    [3, 7, 11, 15, 19],
    [4, 8, 12, 16, 20],
    [5, 9, 13, 17, 21]
]

used_clues = [
    [],
    [],
    [],
    []
]

culpritChoices = ["Alex", "James", "Mylie", "Jennifer"]
foodBorneIllnessChoices = ["Salmonella", "E. Coli", "Listeria", "Norovirus"]
causeOfIllnessChoices = ["Mayonnaise", "Undercooked Chicken", "Jam", "Pizza"]
howItWasCausedChoices = ["Contamination", "Improper Storage", "Cross Contamination", "Improper Cooking"]

solution = ["Alex", "Salmonella", "Mayonnaise", "Contamination"]  # Culprit, Food Borne Illness, Cause of Illness, How it was caused

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
    21: (682, 619)
}

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Food Detective")

background_image = pygame.image.load("assets/Background.png")

background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def find_category_index(my_list, target):
    for i, row in enumerate(my_list):
        if target in row:
            return i
        
def add_used_clue(category, clue):
    used_clues[category].append(clue)

def check_clue_used(category, clue):
    return clue in used_clues[category]

def get_random_clue(category):
    random_clue = random.randint(1, 15)

    if check_clue_used(category, random_clue):
        return get_random_clue(category)
    else:
        add_used_clue(category, random_clue)
        return random_clue

def draw_circle(square_number):
    x, y = locations[square_number]
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 10)

def roll_dice():
    return random.randint(1, 6)

def pop_up_message(message):
    font = pygame.font.Font(None, 36)
    
    # Adjust the wrap width based on your font size and screen width
    # This is a rough estimation; you might need to fine-tune it
    char_width = font.size("a")[0]  # Estimate the width of a single character
    max_chars_per_line = screen_width // char_width
    
    # First, split the original message by explicit line breaks
    original_lines = message.split('\n')
    
    # Then wrap each line if it's too long to fit the screen
    wrapped_lines = []
    for line in original_lines:
        wrapped_lines.extend(textwrap.wrap(line, max_chars_per_line))
    
    # Calculate the starting y position so the block of text is centered
    block_height = len(wrapped_lines) * font.get_height()
    y_start = screen_height // 2 - block_height // 2
    
    screen.fill((0, 0, 0))  # Clear the screen with black
    
    # Render each line, adjusting the y position for each
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width // 2, y_start + i * font.get_height()))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()
    
    # Wait for a user action to close the message
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to close
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # Click to close
            
def get_text_from_file(file_name):
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

def check_current_category(categoryNumber):
    match categoryNumber:
        case 0:
            return "scene"
        case 1:
            return "witness"
        case 2:
            return "generic"
        case 3:
            return "weapon"
        case _:
            return

def roll_button():
    global current_roll
    global rolled
    global at_target_square
    global can_move
    global got_clue
    global rolls_remaining

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
            got_clue = False
            rolls_remaining -= 1
            print(current_roll)
        elif click[0] == 0 and rolled and not at_target_square:
            rolled = False

def display_remaining_rolls():
    font = pygame.font.Font(None, 36)
    text = font.render("Rolls remaining: " + str(rolls_remaining), True, (255, 255, 255))
    screen.blit(text, (450, 20))

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

def begin_game(name):
    pop_up_message("Welcome to " + name + 
                   "\n\nYou have 10 rolls to move around the board and collect clues." + 
                   "\n\nPress the left and right arrow keys to move." + 
                   "\n\nPress the roll button to roll the dice." + 
                   "\n\nPress the clue button to see your collected clues." + 
                   "\n\nClick anywhere to continue.")
    
    pop_up_message(get_text_from_file("intro.txt"))

            
def end_game_message():
    pop_up_message("Your time is up, detective. Now it's time to solve the case. Check your clues and see if you cracked the case. Click anywhere to continue")

    pop_up_message("Now it's time to figure out the details of the case. You must select the culprit, the Food Borne Illness and what caused the illness. Good Luck, and don't guess wrong, or the case may remain unsolved... \n\nClick to continue to the guessing stage.")

def guessing_stage(buttonsArray):
    global current_guessing_stage

    button_width = 150
    button_height = 50
    button_x = 325
    button_y = 350
    button_spacing = 100

    buttons = buttonsArray

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(buttons):
                    button_rect = pygame.Rect(button_x, button_y + i * button_spacing, button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        answer.append(buttons[i])
                        current_guessing_stage += 1
                        match current_guessing_stage:
                            case 0:
                                buttons = culpritChoices
                            case 1:
                                buttons = foodBorneIllnessChoices
                            case 2:
                                buttons = causeOfIllnessChoices
                            case 3:
                                buttons = howItWasCausedChoices
                            case 4:
                                if answer == solution:
                                    pop_up_message("Congratulations! You solved the case!")
                                else:
                                    pop_up_message("You guessed wrong! The case remains unsolved.")
                                pygame.quit()
                                sys.exit()
                            case _:
                                pass
                    
        screen.fill((0, 0, 0))

        for i, button in enumerate(buttons):
            button_rect = pygame.Rect(button_x, button_y + i * button_spacing, button_width, button_height)
            pygame.draw.rect(screen, (255, 0, 0), button_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(button, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()

def main():
    global current_square
    global at_target_square
    global got_clue
    global answer
    global current_guessing_stage

    target_forward_square = 1
    target_reverse_square = 1

    current_guessing_stage = 0

    answer = []

    clear_text_file("known clues.txt")

    begin_game(game_name)

    display_remaining_rolls() 

    while rolls_remaining > 0:
        if rolled:
            target_forward_square = min(len(locations), current_square + current_roll)
            target_reverse_square = max(2, current_square - current_roll)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_square != target_reverse_square and not at_target_square:
                    current_square = max(2, current_square - 1)  # Ensure current_square doesn't go below 2
                elif event.key == pygame.K_RIGHT and current_square != target_forward_square and not at_target_square:
                    current_square = min(len(locations), current_square + 1)  # Ensure current_square doesn't exceed the number of squares
                elif target_forward_square == current_square or target_reverse_square == current_square:
                    at_target_square = True
                    if (target_forward_square != 1 or target_reverse_square != 1) and not got_clue:
                        current_category = check_current_category(find_category_index(categories, current_square))
                        current_clue = get_random_clue(find_category_index(categories, current_square))
                        pop_up_message(get_text_from_file("assets/clues/"+ current_category +"/Clue" + str(current_clue) + ".txt"))
                        add_new_clue(get_text_from_file("assets/clues/"+ current_category +"/Clue" + str(current_clue) + ".txt"))
                        got_clue = True
    

        screen.blit(background_image, [0, 0])

        draw_circle(current_square)
        roll_button()
        see_clues()
        display_remaining_rolls()

        pygame.display.flip()

    end_game_message()
    guessing_stage(culpritChoices)
 
if __name__ == "__main__":
    main()
