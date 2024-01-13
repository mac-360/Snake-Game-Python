import pygame as game
import random

# Initialize Pygame and Mixer
game.init()
game.mixer.init()

# Load Sounds
beep_sound = game.mixer.Sound("beep.wav")
background_music = game.mixer.music.load("background_music.mp3")
game.mixer.music.play(-1)

# Global Variables
exit_game = False
pos_x = 600
pos_y = 250
velocity_x = 10
velocity_y = 0
GameWindow = game.display.set_mode((1000, 600))
snake_width = 15
snake_len = 15
clock = game.time.Clock()
WHITE = (255, 255, 255)
RED = (255, 0, 0)
Black = (0, 0, 0)
BLUE = (0, 0, 255)
FPS = 40
WindowWidth = 1000
WindowLength = 600
apple_pos_x = random.randint(40, WindowWidth - 40)
apple_pos_y = random.randint(40, WindowLength - 40)
snake_segments = [(pos_x, pos_y)]
difficulty = "MEDIUM"
NoofSmallApplesEaten = 0
BigAppleGenerated:bool=False
score:int=0
# Assuming you've defined YELLOW as (255, 255, 0) in your global constants
YELLOW = (255, 255, 0)
def InitializeGameCaption():
    game.display.set_caption("Snake Game")
    icon_surface = game.image.load('snake_icon.png') 
    game.display.set_icon(icon_surface)

def QuitWindow():
    global exit_game
    exit_game=True
    game.quit()
    quit()

def CheckWhichKeyAndUpdatePos(key):
    global velocity_x, velocity_y
    if key == game.K_DOWN and velocity_y != -10:
        velocity_x, velocity_y = 0, 10
    elif key == game.K_UP and velocity_y != 10:
        velocity_x, velocity_y = 0, -10
    elif key == game.K_RIGHT and velocity_x != -10:
        velocity_x, velocity_y = 10, 0
    elif key == game.K_LEFT and velocity_x != 10:
        velocity_x, velocity_y = -10, 0

def UpdateXandYPosition():
    global pos_x, pos_y, exit_game, snake_len
    pos_x += velocity_x
    pos_y += velocity_y
    snake_segments.append((pos_x, pos_y))
    if len(snake_segments) > snake_len:
        del snake_segments[0]
    if pos_x < 0 or pos_x >= WindowWidth or pos_y < 0 or pos_y >= WindowLength:
        exit_game = True

def DisplayGameOver():
    font = game.font.SysFont(None, 100)
    game_over_text = font.render("GAME OVER", True, RED)
    GameWindow.blit(game_over_text, (250, 250))
    game.display.update()
    game.time.delay(2000)
    QuitWindow()

def IsAppleEaten():
    global beep_sound, snake_len, NoofSmallApplesEaten,BigAppleGenerated,score
    if not BigAppleGenerated:
        if abs(pos_x - apple_pos_x) < 15 and abs(pos_y - apple_pos_y) < 15:
            if NoofSmallApplesEaten < 5:
                snake_len += 2
                score+=10
                beep_sound.play()
                NoofSmallApplesEaten += 1
                NewCoordinatesofApple()
                return True
    else:
        if abs(pos_x - apple_pos_x) < 25 and abs(pos_y - apple_pos_y) < 25:
            snake_len += 4
            score+=20
            BigAppleGenerated=False
            beep_sound.play()
            NoofSmallApplesEaten=0
            NewCoordinatesofApple()
            return True



def NewCoordinatesofApple():
    global apple_pos_x, apple_pos_y
    apple_pos_x = random.randint(40, WindowWidth - 40)
    apple_pos_y = random.randint(40, WindowLength - 40)

def CheckSelfCollision():
    head = (pos_x, pos_y)
    for segment in snake_segments[:-1]:
        if head == segment:
            return True
    return False

def DisplayApple():
    global NoofSmallApplesEaten,BigAppleGenerated,apple_pos_x,apple_pos_y
    
    if NoofSmallApplesEaten < 5:
        image = game.image.load('Smallapple.png')
        scaled_width = int(0.05 * image.get_width())
        scaled_height = int(0.05 * image.get_height())
        image = game.transform.scale(image, (scaled_width, scaled_height))
        image.set_colorkey(Black)
        # Blit the image onto the GameWindow
        GameWindow.blit(image, (apple_pos_x, apple_pos_y)) 
        

    else:
        BigAppleGenerated=True
        image = game.image.load('Bigapple.png')
        scaled_width = int(0.07 * image.get_width())
        scaled_height = int(0.07 * image.get_height())
        image = game.transform.scale(image, (scaled_width, scaled_height))
        image.set_colorkey(Black)
        # Blit the image onto the GameWindow
        GameWindow.blit(image, (apple_pos_x, apple_pos_y)) 

def DisplaySnake():
    image = game.image.load('snakeBody.png')
    scaled_width = int(0.15 * image.get_width())
    scaled_height = int(0.15 * image.get_height())
    image = game.transform.scale(image, (scaled_width, scaled_height))
    
    for segment in snake_segments[::]:
        # Blit snake body image onto GameWindow at the specified segment position
        GameWindow.blit(image, (segment[0], segment[1]))

def DisplayDifficultyScreen():
    global difficulty
    while True:
        GameWindow.fill(Black)
        font = game.font.SysFont(None, 55)
        easy_text = font.render("EASY", True, WHITE)
        medium_text = font.render("MEDIUM", True, WHITE)
        hard_text = font.render("HARD", True, WHITE)
        
        GameWindow.blit(easy_text, (420, 205))
        GameWindow.blit(medium_text, (400, 280))
        GameWindow.blit(hard_text, (410, 355))

        for event in game.event.get():
            if event.type == game.QUIT:
                QuitWindow()
            if event.type == game.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 420 <= x <= 580 and 205 <= y <= 255:
                    difficulty = "EASY"
                    velocity_x = 5
                    velocity_y = 0
                    return
                elif 400 <= x <= 600 and 280 <= y <= 330:
                    difficulty = "MEDIUM"
                    velocity_x = 10
                    velocity_y = 0
                    return
                elif 410 <= x <= 590 and 355 <= y <= 405:
                    difficulty = "HARD"
                    velocity_x = 15
                    velocity_y = 0
                    return
        game.display.update()


def DisplayMenu():
    menu_running = True

    while menu_running:
        GameWindow.fill(Black)  # Fill the window with black color
        
        DisplayMainSnakeImg()
        
        font = game.font.SysFont('comicsansms', 50)  
        continue_text = font.render("Continue to Game", True, YELLOW) 
        high_scores_text = font.render("Display High Scores", True, YELLOW)
        
    
        continue_rect = continue_text.get_rect(center=(WindowWidth // 2, 225))
        high_scores_rect = high_scores_text.get_rect(center=(WindowWidth // 2, 325))
        
        
        GameWindow.blit(continue_text, continue_rect)
        GameWindow.blit(high_scores_text, high_scores_rect)

        
        game.display.update()

        for event in game.event.get():
            if event.type == game.QUIT:
                QuitWindow()
            
            elif event.type == game.MOUSEBUTTONDOWN:
                x, y = event.pos

                if continue_rect.collidepoint(x, y):

                    menu_running = False
                    return "Continue"

                
                elif high_scores_rect.collidepoint(x, y):
                    menu_running = False
                    return "DisplayScores"





       
                
def GameLoopFunction():
    global exit_game
    NewCoordinatesofApple()
    DisplayDifficultyScreen()

    while not exit_game:
        GameWindow.fill(Black)
        clock.tick(FPS)
        for event in game.event.get():
            if event.type == game.QUIT:
                QuitWindow()
            if event.type == game.KEYDOWN:
                CheckWhichKeyAndUpdatePos(event.key)
        UpdateXandYPosition()
        if CheckSelfCollision():
            print("Self collision detected!")
            exit_game = True
            DisplayGameOver()
            game.display.update()
            break

        if IsAppleEaten():
            NewCoordinatesofApple()
        DisplayApple()
        DisplaySnake()
        DisplayScore()
        game.display.update()

def DisplayScore():
    font = game.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    GameWindow.blit(score_text, (10, 10))


     
def FileHandling(filename:str):
    global score 

    try:
        with open(filename, 'r') as filerdr:
            scores = filerdr.read()
            scoreslist = [int(score_str) for score_str in scores.split()]  
            scoreslist.append(score)  
            scoreslist.sort(reverse=True) 

        if len(scoreslist) > 3:
            scoreslist.pop()  

        with open(filename, 'w') as filewriter:
            for s in scoreslist:
                filewriter.write(str(s) + ' ')

    except FileNotFoundError:
        print(f"FileNotFoundError: Unable to find the file '{filename}'")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    

def DisplayFile(filename: str):
    try:
        with open(filename, 'r') as filerdr:
            scores = filerdr.read()
            scoreslist = [int(score_str) for score_str in scores.split()]  
            
            scoreslist.sort(reverse=True)
            
            GameWindow.fill(Black)  
            
            vibrant_color = (255, 165, 0)  
            font = game.font.SysFont(None, 36)
            
            
            total_text_height = len(scoreslist) * 40
            y_position = (WindowLength - total_text_height) // 2
            
            for idx, score in enumerate(scoreslist, start=1):
                score_text = font.render(f"{idx}. {score}", True, vibrant_color)
                
                
                text_width, _ = font.size(f"{idx}. {score}")
                x_position = (WindowWidth - text_width) // 2
                
                GameWindow.blit(score_text, (x_position, y_position))
                y_position += 40  
                
                
                game.display.update()
                for event in game.event.get():
                    if event.type == game.QUIT:
                        QuitWindow()
                        return
            
            game.time.delay(5000)  
            
    except FileNotFoundError:
        print(f"Error: Unable to find the file '{filename}'")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def DisplayMainSnakeImg():
    global GameWindow, WindowWidth, WindowLength
    
    image = game.image.load('Snake_Main.png')
    
    # Scale the image to 70% of its original size
    scaled_width = int(0.70 * image.get_width())
    scaled_height = int(0.70 * image.get_height())
    image = game.transform.scale(image, (scaled_width, scaled_height))
    
    
    image.set_colorkey(Black)
    
    # Set the position of the image to the bottom right corner
    x_position = WindowWidth - scaled_width - 10  # 10 pixels from the right edge
    y_position = WindowLength - scaled_height - 10  # 10 pixels from the bottom edge
    
    # Blit the image onto the GameWindow
    GameWindow.blit(image, (x_position, y_position))
    
    
   
def DisplayStartofGame():
    global GameWindow, WindowWidth, WindowLength
    
    # Load the image
    image = game.image.load('Snake_Intro-bicubic.jpg')
    scaled_width = int(0.85 * image.get_width())
    scaled_height = int(0.85 * image.get_height())
    image = game.transform.scale(image, (scaled_width, scaled_height))
    
    
    image.set_colorkey(Black)
    # Blit the image onto the GameWindow
    GameWindow.blit(image, (0, 0)) 
    

    game.display.update()
    
    game.time.delay(1500)



def GameMain():
    InitializeGameCaption()
    DisplayStartofGame()
    user_choice = DisplayMenu()
    
    if user_choice == "Continue":
        GameLoopFunction()
        FileHandling('Scores.txt')
        
        DisplayGameOver()
    elif user_choice == "DisplayScores":
        DisplayFile('Scores.txt')
        GameMain()



def Main():
    GameMain()

Main()