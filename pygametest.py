#!/usr/bin/env python
# I don't know what the above line means

import pygame

class Bubble:
    """A class for different boxes with text in them."""
    def __init__(self):
        self.bubble=pygame.Surface((400,70)) # This is the actual surface that will be blitted
        self.bubble.fill((30,30,30))

        self.bubble.fill(0,(5,5,390,60))

    def clear(self):
        # self.bubble.fill((30,30,30)) # Probably not necessary since this only refills the border
        self.bubble.fill((0,0,0),(5,5,390,60))

    def showtext(self,text):
        self.clear()
        sometext=Font.render(text, 1, (255, 255, 255)) # Surface of the rendered font
        self.bubble.blit(sometext,(10,10))

def showinv():
    ypos=150
    window.fill(0, (5,145,150,70))
    for item in fonted:
        r = window.blit(item, (10, ypos))
        ypos += Font.get_height()

inventory=["Chicken: 1","Dog: 2","Fish:3"]

def main():
    pygame.init()

    global window
    window=pygame.display.set_mode((500,300), pygame.RESIZABLE)
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    global Font
    Font=pygame.font.Font(None,20)

    a=Bubble()

    global fonted
    fonted=[Font.render(item,1,(200,200,200)) for item in inventory] # list of rendered Surfaces
    i=0
    running=1
    while running: # game loop
        # if not pygame.mixer.music.get_busy():
        #     pygame.mixer.music.load("darude.ogg")
        #     pygame.mixer.music.play()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running=0
            if e.type == pygame.KEYDOWN:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
                i+=1
                a.showtext("A key has been pressed down %s time(s)."%i)
            elif e.type == pygame.KEYUP:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if e.type == pygame.VIDEORESIZE:
                window=pygame.display.set_mode(e.size,pygame.RESIZABLE)
                thing=window.get_width(),window.get_height()
                a.showtext("The screen has been resized to %s,%s"%thing)
                global currentColour
                currentColour=(thing[1]%256,thing[0]%256,(thing[0]*thing[1])%256)
                window.fill(currentColour)
                pygame.display.set_caption("Pygame Test. Window size: %s,%s"%thing) # Works! yay

        showinv()
        window.blit(a.bubble,(0,0))
        pygame.display.flip()

    quit() # Only runs after the game gets quitted

    print("Finished.")

if __name__ == '__main__': main()