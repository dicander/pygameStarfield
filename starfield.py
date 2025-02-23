# Display a ride through perspective correct stars made out of pixels
# using pygame

import pygame
import random

N_STARS = 10000
WIDTH = 1600
HEIGHT = 800
MID_X = WIDTH // 2
MID_Y = HEIGHT // 2


# A class for a star. It has a position within a frustrum with coordinates between -1 and 1 (float)

class Star:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.randomize_color()
    
    def randomize_color(self):
        self.color = tuple(random.randint(200,255) for _ in range(3))
        # Now randomize to that I uniformly get 1 or 2 randomly picked components of the color tuple
        # set to 0
        zerotoone = random.random()
        if zerotoone < 0.4:
            chosen_index = random.randint(0,2)
            self.color = list(self.color)
            self.color[chosen_index] = 0
            self.color = tuple(self.color)
        elif zerotoone < 0.8:
            # now select one to keep
            chosen_index = random.randint(0,2)
            self.color = list(self.color)
            kept_color = self.color[chosen_index]
            self.color = [0,0,0]
            self.color[chosen_index] = kept_color

    def restart_from_back(self):
        self.z = 1
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.randomize_color()
#        self.color = tuple(random.randint(200,255) for _ in range(3))

    def update(self, speed):
        self.z -= speed
        if self.z <= 0:
            return self.restart_from_back()


def is_inside_viewport_of_current_resolution(x, y, z):
    x = x / z
    y = y / z
    x = int(x * WIDTH) + MID_X
    y = int(y * WIDTH) + MID_Y
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    return True



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Starfield')
    # Make the window visible
    clock = pygame.time.Clock()
    # Create a list of stars
    stars = []
    for i in range(N_STARS):
        x, y, z = 14, 14, 14
        while not is_inside_viewport_of_current_resolution(x, y, z):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            z = random.uniform(0, 1)
        # while this is outside of the viewport, move it towards the center of the screen, 0, 0
        stars.append(Star(x, y, z))
    speed = 0.01



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return

        screen.fill((0, 0, 0))
        # Draw the stars, perspective correct
        for star in stars:
            # Perspective correct the stars
            x = star.x / star.z
            y = star.y / star.z
            # Scale the stars to the screen
            x = int(x * WIDTH) + MID_X
            y = int(y * WIDTH) + MID_Y
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                star.restart_from_back()
                continue
            # Draw the star
            # Calculate greyscale based on z
            scale_factor = (1 - star.z)
            pygame.draw.circle(screen, (int(scale_factor*star.color[0]),
                                        int(scale_factor*star.color[1]), 
                                        int(scale_factor*star.color[2]))
                             , (x, y), 4-star.z*4)

            star.update(speed)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()