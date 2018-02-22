# Import a library of functions called 'pg'
import pygame as pg
import math
import time
import os

# Initialize the game engine
pg.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#Select Font
font = pg.font.SysFont('Calibri', 25, True, False)

PI = math.pi

#Height and width
HEIGHT = 800
WIDTH = 800
#Hald Height and width
HHEIGHT = HEIGHT / 2
HWIDTH = WIDTH / 2
CENTER = (HWIDTH, HHEIGHT)

ROOT3 = math.sqrt(3)
OFFSET = 6 * ROOT3
# Set the height and width of the screen
size = (HEIGHT, WIDTH)
screen = pg.display.set_mode(size)
screenRect = screen.get_rect()

#Calculate a centerRect for the rotation lines
CRECTW = 250
CRECTH = 250
CRECTL = HWIDTH - CRECTW / 2
CRECTT = HHEIGHT - CRECTH  / 2
centerRect = pg.Rect(CRECTL, CRECTT, CRECTW, CRECTH)

# Calculate the points to make arrows
LEN = 10
#Red Arrow
REDPT = (HWIDTH - CRECTW / 2, HHEIGHT)
REDLEFT = (REDPT[0] - LEN, REDPT[1] - LEN)
REDRIGHT = (REDPT[0] + LEN, REDPT[1] - LEN)
#Green Arrow
GREENPT = (HWIDTH - 2 + CRECTW / 2, HHEIGHT) # Not sure why this needs the extra -2
GREENLEFT = (GREENPT[0] - LEN, GREENPT[1] - LEN)
GREENRIGHT = (GREENPT[0] + LEN, GREENPT[1] - LEN)

centerRect = pg.Rect(CRECTL, CRECTT, CRECTW, CRECTH)


pg.display.set_caption("Titan Rover Viz")



# Loop until the user clicks the close button.
done = False
clock = pg.time.Clock()


class Viewer:
    def __init__(self):
        self.roseSurf = pg.image.load(os.path.join('rviewer/data', 'rose_out.png')).convert_alpha()
        self.roseRect = self.roseSurf.get_rect(center=screenRect.center)
        self.clock = pg.time.Clock()

    def convertAngle(self, targetHeading):
        return (90 - targetHeading) % 360
    
    def flashArrivalMsg(self, point, arrivalTime):
        flashFont = pg.font.SysFont('Calibri', 50, True, False)
        arrivalText = flashFont.render("ARRIVED!", True, BLACK)
        pointText = flashFont.render("Waypoint: " + str(point), True, BLACK)
        timeText = flashFont.render("Time: " + str(arrivalTime), True, BLACK)
        for i in range(6):
            screen.fill(RED)
            screen.blit(arrivalText, [10, 0])
            screen.blit(pointText, [10, 60])
            screen.blit(timeText, [10, 120])
            pg.display.flip()
            time.sleep(0.25)

            screen.fill(WHITE)
            screen.blit(arrivalText, [10, 0])
            screen.blit(pointText, [10, 60])
            screen.blit(timeText, [10, 120])
            pg.display.flip()
            time.sleep(0.25)
        time.sleep(1)

        # This limits the while loop to a max of 60 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(60)


    #refresh the screen
    def refreshScreen(self, motor1, motor2, currentHeading, targetDistance, targetHeading, shouldCW):
        for event in pg.event.get():  # User did something
            if event.type == pg.QUIT:  # If user clicked close
                pg.quit()
                exit()
        # Clear the screen and set the screen background
        screen.fill(BLACK)

        # Draw rower icon and facing line
        pg.draw.polygon(screen, WHITE, [[HWIDTH - 6, HHEIGHT + OFFSET], [HWIDTH, HHEIGHT - OFFSET], [HWIDTH + 6, HHEIGHT + OFFSET]], 1)
        pg.draw.line(screen, WHITE, (CENTER[0], CENTER[1]-OFFSET), (HWIDTH,0))

        #draw compass rose, ideally this will be correct for the given targetHeadingle (inverted)
        newSurf = pg.transform.rotate(self.roseSurf, currentHeading)
        newRect = newSurf.get_rect(center=screenRect.center)
        screen.blit(newSurf, newRect)
        currentHeading = (currentHeading + 5 ) % 360

        if shouldCW == None:
            None
        elif shouldCW == True:
            #Green Arc with arrow
            pg.draw.arc(screen, GREEN, centerRect, 0, PI / 2, 2)
            pg.draw.line(screen, GREEN, GREENPT, GREENLEFT, 2)
            pg.draw.line(screen, GREEN, GREENPT, GREENRIGHT, 2)
        else:
            #Red Arc with arrow
            pg.draw.arc(screen, RED, centerRect, PI / 2, PI, 2)
            pg.draw.line(screen, RED, REDPT, REDLEFT, 2)
            pg.draw.line(screen, RED, REDPT, REDRIGHT, 2)

        #Draw line + dot at desired point
        targetHeading = self.convertAngle(targetHeading)
        ptx = targetDistance * math.cos(math.radians(targetHeading))
        pty = targetDistance * math.sin(math.radians(targetHeading))
        pt = (int(HWIDTH - ptx), int(HHEIGHT-pty))
        pg.draw.line(screen, BLUE, CENTER, pt, 2)
        pg.draw.circle(screen, BLUE, pt, 10, 0)

        #Put Text
        motor1Text = font.render("Motor 1: " + str(motor1), True, WHITE)
        motor2Text = font.render("Motor 2: " + str(motor2), True, WHITE)
        screen.blit(motor1Text, [5, HEIGHT - 50])
        screen.blit(motor2Text, [5, HEIGHT - 25])
            # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pg.display.flip()

        # This limits the while loop to a max of 60 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(60)

    def __del__(self):
        # Be IDLE friendly
        pg.quit()


