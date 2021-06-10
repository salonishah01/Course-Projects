import pygame

class Player():
    def __init__(self, x, y, radius, color, health, infected, noOfPlayers):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.radius = radius
        self.color = color
        
        self.health = health 
        self.far = [True] * noOfPlayers
        self.infected = infected
        self.vel = 4


    # Input: window object
    # Return: None
    # Description: Draw circle on the pygame window
    def draw(self, win):
        if self.infected:
            self.color = (0,0,0)
        pygame.draw.circle(win, self.color, self.center, self.radius)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if 0 < self.x-self.vel < 500:
                self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            if 0 < self.x+self.vel < 500:
                self.x += self.vel

        if keys[pygame.K_UP]:
            if 0 < self.y-self.vel < 500:
                self.y -= self.vel

        if keys[pygame.K_DOWN]:
            if 0 < self.y+self.vel < 500:    
                self.y += self.vel

        self.update()

    def update(self):
        self.center = (self.x, self.y)