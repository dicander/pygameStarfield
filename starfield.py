# Display a ride through perspective correct stars made out of pixels
# using pygame

import pygame
import random

# A class for a star. It has a position within a frustrum with coordinates between -1 and 1 (float)

class Star:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    
    def update(self, speed):
        self.z -= speed
        if self.z <= 0:
            self.z = 1
            self.x = random.uniform(-1, 1)
            self.y = random.uniform(-1, 1)



def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 800))
    pygame.display.set_caption('Starfield')
    # Make the window visible
    clock = pygame.time.Clock()
    # Create a list of stars
    stars = []
    for i in range(10000):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = random.uniform(0, 1)
        stars.append(Star(x, y, z))

    speed = 0.01
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        # Draw the stars, perspective correct
        for star in stars:
            # Perspective correct the stars
            x = star.x / star.z
            y = star.y / star.z
            # Scale the stars to the screen
            x = int(x * 1024) + 512
            y = int(y * 800) + 400
            # Draw the star
            # Calculate greyscale based on z
            greyscale = int((1-star.z)*255)
            pygame.draw.circle(screen, (greyscale, greyscale, greyscale), (x, y), 4-star.z*4)
            star.update(speed)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()