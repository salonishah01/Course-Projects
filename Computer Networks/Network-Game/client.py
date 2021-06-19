import pygame
from network import Network
from player import Player
import datetime

pygame.init()

# Width and height of the game window
width = 500 
height = 500

win = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("Client")
font = pygame.font.Font('freesansbold.ttf', 25)

# Input: x and y coordinates at 2 points
# Return: Euclidean distance
def distance(x1, y1, x2, y2):
    return (abs(x2-x1)**2 + abs(y2-y1)**2)**0.5

# Input: Player 1 and Player 2 objects with Player 2's index
# Return: None
# Description: Checks if given 2 players one is infected, and if that can affect the other one
def check(p1, p2, i):
    if distance(p1.x, p1.y, p2.x, p2.y) <= (p1.radius+p2.radius): # diameter
        if p2.infected: 
            if p1.far[i]: # Players were far before, but now came closer again
                p1.far[i] = False
                p1.health -= 1

            if p1.health <= 0:
                p1.health = 0
                p1.infected = True
        
    else: p1.far[i] = True

# Input: Message string, foreground and background color in hex and the position in (x,y)
# Return: None
# Description: Writes the given message string in the game window
def drawLeaderboard(score, fgColor, bgColor, pos):
    text = font.render(score, True, fgColor, bgColor)
    textRect = text.get_rect()
    textRect.center = pos
    win.blit(text, textRect)

# Input: game's window object and list of players object
# Return: None
# Description: Redraws window with updated health score and updated alive players
def redrawWindow(win,players):
    win.fill((255,255,255))

    for i, player in enumerate(players):
        player.draw(win)
        pScore = str(player.health)
        drawLeaderboard(pScore, (255, 255, 255), player.color, (100+(i*15),15)) # Scoreboard

        if player.color != (0,0,0): # Alive 
            drawLeaderboard("  ", (255, 255, 255), player.color, (400+(i*15),15))

    drawLeaderboard("Health:", (0,0,0), (255, 255, 255), (46, 15))
    drawLeaderboard("Alive:", (0,0,0), (255, 255, 255), (350, 15))

    pygame.display.update()

# Input: None
# Return: None
# Description: Instatiate a new player object(p1) and start sending p1's information to server
# This makes server send back the other players information. Use this and draw it in the current window
def main():
    run = True
    n = Network()
    p1 = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        # a = datetime.datetime.now()

        otherPlayers = n.send(p1)
        
        # b = datetime.datetime.now()
        # print(str((b-a).microseconds) + " microsec")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p1.move()

        for i, p2 in enumerate(otherPlayers):
            check(p1, p2, i)

        redrawWindow(win, [p1]+otherPlayers)

main()