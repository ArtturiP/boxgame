import pygame
import random

pygame.init()  # initialize pygame

screen = pygame.display.set_mode((600, 480))    # screen size 600x480

font = pygame.font.SysFont("Arial", 24)     # font Arial and font-size 24

pygame.display.set_caption('Box Game')      # name of the game 'Box Game'

# when game is being played
def playGame():
    global counter  # shows the time elapsed for the player
    counter = 0
    counterfont = font.render(str(counter), True, (255, 255, 255))

    # timer
    time_delay = 1000
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    # coordinates for the targets
    randomxcoordinates = []
    randomycoordinates = []

    # colors of the targets
    targetcolors = []

    for i in range(10):
        randomx = random.randrange(0, 600)
        randomy = random.randrange(0, 480)
        targetcolor = (255, 255, 255)
        randomxcoordinates.append(randomx)
        randomycoordinates.append(randomy)
        targetcolors.append(targetcolor)

    # rectangle (and controls for it) for the player
    class Player(object):
        def __init__(self):
            self.rect = pygame.rect.Rect(0, 0, 40, 40)

        def handle_keys(self):
            key = pygame.key.get_pressed()
            dist = 1
            if key[pygame.K_LEFT]:
                self.rect.move_ip(-1, 0)
            if key[pygame.K_RIGHT]:
                self.rect.move_ip(1, 0)
            if key[pygame.K_UP]:
                self.rect.move_ip(0, -1)
            if key[pygame.K_DOWN]:
                self.rect.move_ip(0, 1)

        def draw(self, surface):
            pygame.draw.rect(screen, (250, 0, 0), self.rect)

    rects = []    # targets
    player = Player()
    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == timer_event:
                counter += 1    # timer number goes up 1 for every second
                counterfont = font.render(str(counter), True, (255, 255, 255))

        screen.fill((0, 0, 0))    # background

        # build the targets in the game
        for i in range(10):
            rect = pygame.draw.rect(screen, targetcolors[i], (randomxcoordinates[i], randomycoordinates[i], 20, 20))
            rects.append(rect)
            if player.rect.colliderect(rect):
                targetcolors[i] = (0, 0, 0)

        player.draw(screen)     # build the player in the game

        # time counter to show in the game
        pygame.draw.rect(screen, (0, 0, 0), (600-counterfont.get_width(), 0, counterfont.get_width(), counterfont.get_height()))
        screen.blit(counterfont, (600-counterfont.get_width(), 0))

        player.handle_keys()

        # timer stops and result screen shows when all targets have vanished
        result = all(element == (0, 0, 0) for element in targetcolors)
        if result:
            gameOver()
            pygame.time.set_timer(timer_event, 0)

        pygame.display.update()

        clock.tick(60)

# when game is over and showing results
def gameOver():
    congrats = font.render("Congratulations, you passed the game!", True, (255, 255, 255))
    info = font.render("Press R to play again or Press ESC to quit", True, (255, 255, 255))
    yourresult = font.render("Your time was " + str(counter) + " seconds.", True, (255, 255, 255))
    congrats_x = 150
    congrats_y = 150
    info_x = 150
    info_y = 150 + congrats.get_height()
    yourresult_x = 150
    yourresult_y = info_y + info.get_height()
    screen.blit(congrats, (congrats_x, congrats_y))
    screen.blit(info, (info_x, info_y))
    screen.blit(yourresult, (yourresult_x, yourresult_y))
    keys = pygame.key.get_pressed()     # actions for said buttons
    if keys[pygame.K_r]:
        playGame()
    if keys[pygame.K_ESCAPE]:
        exit()


playGame()      # play the game