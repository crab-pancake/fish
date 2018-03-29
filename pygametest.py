import sys, pygame

size = width, height = 600, 400
black = 255, 255, 255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("test.png")
ballrect = ball.get_rect()
speed=[1,1]

def gamerun():
    pygame.init()
    while True:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        #loop
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        #render
        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()

def main():
    gamerun()

if __name__ == "__main__":
    main()