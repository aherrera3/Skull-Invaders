import pygame

class Button():
    # constructor of the class
    def __init__(self, x, y, image, scale):
        width, height = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))   # to scale the button images
        self.rect = self.image.get_rect()    # give the rectangule surrounding the image
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        action = False
        # gets the mouse position
        mousePos = pygame.mouse.get_pos()
        
        # checks the mouseover and clicked conditions
        if self.rect.collidepoint(mousePos):   # if pos is hovered in the rectangule image
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:     # if a mouse click is made. [0] is left click, [1] is middle click and [2] right click
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:     # to release the keystroke
                self.clicked = False

        # draw button on screen        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action