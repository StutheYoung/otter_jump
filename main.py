import pygame
import sys

# initialize pygame
pygame.init()

# display set up
screen = pygame.display.set_mode((800, 600))
GROUND_Y = 550
ground_scroll_x = 0
pygame.display.set_caption("Otter Jump!")

#score keeping
score = 0
font = pygame.font.SysFont(None, 40)

# player block
class Block(pygame.sprite.Sprite):


    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.image.load("otter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = 100
        # sets position of player to be on ground
        self.rect.y = GROUND_Y - height
       
        # for jumping
        self.vertical_velocity = 0
        self.gravity = .11
        self.jump_strength = -10
        self.on_ground = True

    # updates position
    def update(self):
        self.vertical_velocity += self.gravity
        self.rect.y += self.vertical_velocity

        # check if its on the floor
        if self.rect.y >= GROUND_Y - self.height:
            self.rect.y = GROUND_Y - self.height
            self.vertical_velocity = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vertical_velocity = self.jump_strength
            self.on_ground = False



obstacle_speed = 2

# things that kill player
class Obstacle(pygame.sprite.Sprite):


    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([50, 100])
        self.image.fill((0, 255, 0))  
        # image is a rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_Y - self.rect.height
        self.passed = False
    #move left
    def update(self):
        self.rect.x -= obstacle_speed  
        if self.rect.right < 0:
            self.kill()

block = Block((250, 0, 0), 100, 100)
sprite_group = pygame.sprite.Group()
sprite_group.add(block)  # group for player
obstacles = pygame.sprite.Group()  # group for obstacles

frame_count = 0 

def end_screen(final_score):
    font_big = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 40)

    game_over_text = font_big.render("Game Over", True, (255, 0, 0))
    score_text = font_small.render(f"Final Score: {final_score}", True, (255, 255, 255))
    instruction_text = font_small.render("Press Q to Quit", True, (255, 255, 255))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (250, 200))
        screen.blit(score_text, (300, 300))
        screen.blit(instruction_text, (150, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                 



def run_game():
    global frame_count
    global score
    global obstacle_speed
    frame_count = 0
    score = 0
    running = True
    while running:
        # adds frame counts so new obstacles are added
        frame_count += 1
        if frame_count % 600  == 0:
            new_obstacle = Obstacle(800)
            obstacles.add(new_obstacle)

        # increase game speed
        if frame_count % 800 == 0:
            obstacle_speed += 0.05  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # stop progressing if something kills game
                screen.fill((0, 0, 0))
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    block.jump()  # jumps on spacebar

        # black screen and ground         
        screen.fill((0, 0, 0)) 
        pygame.draw.rect(screen, (100, 100, 100), (ground_scroll_x, GROUND_Y, 800, 50))
        pygame.draw.rect(screen, (100, 100, 100), (ground_scroll_x + 800, GROUND_Y, 800, 50))

        # showing sprites
        sprite_group.update()
        sprite_group.draw(screen)

        obstacles.update()
        obstacles.draw(screen)

        #updating score
        for obs in obstacles:
            if not obs.passed and obs.rect.right < block.rect.left:
                obs.passed = True
                score += 1

        # Show score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))


        # collisions
        if pygame.sprite.spritecollideany(block, obstacles):
            end_screen(score)
            running = False
        #refresh
        pygame.display.flip()


#start screen
def start_screen():
    wait = True
    big_font = pygame.font.SysFont(0,60)
    title = big_font.render('Welcome to Otter Jump', True, (255,255,255))
    instruction = big_font.render('Press any key to start', True, (255,255,255))
    while wait:
        screen.fill((0, 0, 0))
        screen.blit(title, (200, 200))
        screen.blit(instruction, (200, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                wait = False
                run_game()
    
    






start_screen()

