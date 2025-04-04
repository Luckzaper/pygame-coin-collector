import pygame
import random
import os
import sys

# Initialize pygame modules
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for audio playback

# Constants for game configuration
SCREEN_WIDTH = 1000            # Width of the game window
SCREEN_HEIGHT = 800            # Height of the game window
PLAYER_WIDTH = 50              # Width of the player character
PLAYER_HEIGHT = 50             # Height of the player character
ENEMY_SIZE = 60                # Size of the enemy character
COIN_SIZE = 40                 # Size of the coin
FPS = 144                      # Frames per second (game speed)
INITIAL_LIVES = 3              # Starting number of lives
COIN_SCORE = 10                # Points awarded per coin collected
ENEMY_SPEED = 3                # Speed at which enemies move
WIN_SCORE = 150                # Score needed to win the game

# Function to load images with optional resizing and error handling
def load_image(filename, size=None):
    try:
        # Load image from the 'images' directory
        image = pygame.image.load(os.path.join("images", filename))
        if size:
            # Resize the image if a size is provided
            image = pygame.transform.scale(image, size)
        return image
    except:
        # If the image cannot be loaded, print an error and create a placeholder
        print(f"Could not load image: {filename}")
        surface = pygame.Surface(size if size else (50, 50))
        surface.fill((255, 0, 0))  # Fill the placeholder with red color
        return surface

# Try to load sound effects and background music
try:
    game_start_sound = pygame.mixer.Sound("game_start.wav")
    coin_collect_sound = pygame.mixer.Sound("coin_collect.wav")
    background_music = "background_music.wav"
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    game_won_sound = pygame.mixer.Sound("anime-wow-sound-effect.mp3")  # Load the win sound effect
except Exception as e:
    # If there's an error loading sounds, print it and exit the game
    print(f"Error loading sounds: {e}")
    pygame.quit()
    sys.exit(1)

# Initialize game state variables
score = 0              # Player's starting score
lives = INITIAL_LIVES  # Player's starting lives
game_over = False      # Flag to check if the game is over
game_won = False       # Flag to check if the player has won

# Set up the game window with specified width and height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coin Collector Game")  # Set the window title

# Load game assets (images)
try:
    background_image = load_image("mainBackground.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_image = load_image("player.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
    enemy_image = load_image("enemy.png", (ENEMY_SIZE, ENEMY_SIZE))
    coin_image = load_image("game_coin.png", (COIN_SIZE, COIN_SIZE))
    heart_image = load_image("heart.png", (30, 30))  # For displaying lives
except Exception as e:
    # If there's an error loading assets, print it and exit the game
    print(f"Error loading assets: {e}")
    pygame.quit()
    sys.exit(1)

# Create a clock object to manage the game's frame rate
timer = pygame.time.Clock()

# Define a Button class for creating interactive buttons in menus
class Button:
    def __init__(self, text, pos, size=(200, 60)):
        self.text = text
        self.pos = pos                  # Position (x, y) on the screen
        self.size = size                # Width and height of the button
        self.font = pygame.font.Font(None, 36)  # Font for button text
        self.color = (255, 223, 0)      # Button color (golden)
        self.rect = pygame.Rect(pos, size)  # Rectangle representing the button area

    def draw(self):
        # Draw the button rectangle with rounded corners
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        # Draw the button border
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3, border_radius=8)
        # Render the button text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        # Center the text on the button
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Draw the text onto the screen
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        # Check if the button was clicked based on mouse position
        return self.rect.collidepoint(mouse_pos)

# Function to display the instructions screen
def show_instructions():
    font = pygame.font.Font(None, 36)
    instructions = [
        "Instructions:",
        "1. Use arrow keys to move the player.",
        "2. Collect coins to increase your score.",
        "3. Avoid enemies; colliding with them reduces your lives.",
        "4. Game Over if you lose all lives.",
        "5. Win by reaching the target score!",
        "",
        "Press any key to return to the main menu..."
    ]

    # Clear the screen with black color
    screen.fill((0, 0, 0))
    # Render each line of instructions
    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + i * 40))
        screen.blit(text, text_rect)

    pygame.display.flip()  # Update the display

    # Wait for user input to return to the main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle the window close event
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Any key press will return to the main menu
                waiting = False

# Function to display the main menu
def show_main_menu():
    # Load and play menu background music
    pygame.mixer.music.load("menu-53679.mp3")
    pygame.mixer.music.play(-1)  # Play indefinitely

    # Set up the title text
    title_font = pygame.font.Font(None, 74)
    title_text = title_font.render("Main Menu", True, (34, 177, 76))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    # Create buttons for the menu options
    start_button = Button("Start", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 90))
    instructions_button = Button("Instructions", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    credits_button = Button("Credits", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
    exit_button = Button("Exit", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120))

    while True:
        # Fill the screen with a background color (light blue)
        screen.fill((173, 216, 230))
        # Draw the title text
        screen.blit(title_text, title_rect)

        # Draw the buttons onto the screen
        start_button.draw()
        instructions_button.draw()
        credits_button.draw()
        exit_button.draw()

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle the window close event
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position when clicked
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    # Start the game
                    pygame.mixer.music.stop()  # Stop menu music
                    game_start_sound.play()    # Play game start sound
                    return "start"
                elif instructions_button.is_clicked(mouse_pos):
                    # Show instructions
                    show_instructions()
                elif credits_button.is_clicked(mouse_pos):
                    # Show credits screen
                    return "credits"
                elif exit_button.is_clicked(mouse_pos):
                    # Exit the game
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Exit the game if ESC key is pressed
                    pygame.quit()
                    sys.exit()

# Function to display the credits screen
def show_credits():
    font = pygame.font.Font(None, 36)
    credits = [
        "Credits:",
        "Luckas Olimpio - Team Lead & Coder",
        "Abdul Rahman - Coder",
        "Kyle Whiddon - Audio",
        "Maurelly Rodriguez - Graphics",
        "",
        "Press any key to return to the main menu..."
    ]

    # Clear the screen with black color
    screen.fill((0, 0, 0))
    # Render each line of credits
    for i, line in enumerate(credits):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + i * 40))
        screen.blit(text, text_rect)

    pygame.display.flip()  # Update the display

    # Wait for user input to return to the main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle the window close event
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Any key press will return to the main menu
                waiting = False

# Function to display the game over or game won screen
def show_game_over(won):
    pygame.mixer.music.stop()  # Stop any background music
    if won:
        game_won_sound.play()  # Play the win sound effect
    else:
        game_over_sound.play()  # Play the game over sound

    font = pygame.font.Font(None, 74)
    text = "You Won!" if won else "Game Over"
    # Render the message text
    message = font.render(text, True, (255, 255, 255))
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    # Create buttons for 'Restart' and 'Main Menu'
    restart_button = Button("Restart", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    menu_button = Button("Main Menu", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))

    while True:
        # Clear the screen with black color
        screen.fill((0, 0, 0))
        # Draw the message
        screen.blit(message, message_rect)
        # Draw the buttons
        restart_button.draw()
        menu_button.draw()

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle the window close event
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position when clicked
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.is_clicked(mouse_pos):
                    # Restart the game
                    return "restart"
                elif menu_button.is_clicked(mouse_pos):
                    # Return to main menu
                    return "menu"

# Function to create a new enemy at a random vertical position
def spawn_enemy():
    x = SCREEN_WIDTH  # Start at the right edge of the screen
    y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)  # Random y position within screen bounds
    return pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)  # Return a rectangle representing the enemy

# Function to create a new coin at a random position
def spawn_coin():
    x = random.randint(0, SCREEN_WIDTH - COIN_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)
    return pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)  # Return a rectangle representing the coin

# Main game loop function
def game_loop():
    global score, lives, game_won, game_over
    # Reset game state variables
    score, lives, game_over, game_won = 0, INITIAL_LIVES, False, False

    # Start background music for the game
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # Play indefinitely

    # Create the player rectangle centered on the screen
    player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = [spawn_enemy() for _ in range(3)]  # List of enemies
    coins = [spawn_coin() for _ in range(5)]     # List of coins

    enemy_spawn_interval = 2000  # Time interval to spawn new enemies (in milliseconds)
    last_spawn_time = pygame.time.get_ticks()  # Record the last time an enemy was spawned

    while not game_over and not game_won:
        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Handle player movement based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-5, 0)  # Move left
        if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.move_ip(5, 0)   # Move right
        if keys[pygame.K_UP] and player.top > 0:
            player.move_ip(0, -5)  # Move up
        if keys[pygame.K_DOWN] and player.bottom < SCREEN_HEIGHT:
            player.move_ip(0, 5)   # Move down

        # Draw the player, enemies, and coins onto the screen
        screen.blit(player_image, player.topleft)
        for enemy in enemies:
            screen.blit(enemy_image, enemy.topleft)
        for coin in coins:
            screen.blit(coin_image, coin.topleft)

        # Move enemies from right to left across the screen
        for enemy in enemies:
            enemy.move_ip(-ENEMY_SPEED, 0)  # Move enemy to the left

            if enemy.right < 0:
                # If enemy goes off the screen, remove and respawn it
                enemies.remove(enemy)
                enemies.append(spawn_enemy())

            if player.colliderect(enemy):
                # If the player collides with an enemy
                lives -= 1  # Decrease lives
                enemies.remove(enemy)
                enemies.append(spawn_enemy())  # Respawn the enemy
                if lives <= 0:
                    # If no lives left, game over
                    game_over = True

        # Check if it's time to spawn a new enemy
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > enemy_spawn_interval:
            enemies.append(spawn_enemy())
            last_spawn_time = current_time  # Reset the spawn timer

        # Check for collisions with coins
        for coin in coins[:]:  # Iterate over a copy of the list
            if player.colliderect(coin):
                score += COIN_SCORE  # Increase score
                coin_collect_sound.play()  # Play coin collection sound
                coins.remove(coin)
                coins.append(spawn_coin())  # Respawn the coin
                if score >= WIN_SCORE:
                    # If score reaches win condition, set game_won to True
                    game_won = True

        # Render the score on the screen
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Display the player's remaining lives as hearts
        for i in range(lives):
            screen.blit(heart_image, (10 + i * 35, 50))

        pygame.display.flip()  # Update the display

        # Handle events such as quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        timer.tick(FPS)  # Maintain the game frame rate

    # After the game loop ends, show the game over or game won screen
    result = show_game_over(game_won)
    if result == "restart":
        # Restart the game loop if the player chooses to restart
        game_loop()
    elif result == "menu":
        # Return to the main menu
        return

# Main function to start the game
def main():
    while True:
        # Show the main menu and get the player's selection
        menu_selection = show_main_menu()
        if menu_selection == "start":
            # Start the game loop
            game_loop()
        elif menu_selection == "credits":
            # Show the credits screen
            show_credits()
        elif menu_selection == "exit":
            # Exit the game
            break

    pygame.quit()  # Quit pygame when the game loop ends

# Entry point of the program
if __name__ == "__main__":
    main()
