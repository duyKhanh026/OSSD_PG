import pygame as py

# define constants
WIDTH = 500
HEIGHT = 500
FPS = 60

# define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# initialize pygame and create screen
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
# for setting FPS
clock = py.time.Clock()

rot = 0
rot_speed = 2

# define a surface (RECTANGLE)
image_orig = py.Surface((100, 150))
# for making transparent background while rotating an image
image_orig.set_colorkey(BLACK)
# fill the rectangle / surface with green color
image_orig.fill(GREEN)
# creating a copy of original image for smooth rotation
image = image_orig.copy()
image.set_colorkey(BLACK)
# define rect for placing the rectangle at the desired position
rect = image.get_rect()
rect.center = (WIDTH // 2, HEIGHT // 2)
# keep rotating the rectangle until running is set to False
running = True
jumping = False
jump_height = 100
jump_speed = 5
gravity = 1

while running:
    # set FPS
    clock.tick(FPS)
    # clear the screen every time before drawing new objects
    screen.fill(BLACK)
    # check for the exit
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_e and not jumping:  # Only jump if not already jumping
                jumping = True

    if jumping:
        # Move rectangle upward
        rect.y -= jump_speed
        jump_height -= jump_speed

        # If jump height reaches 0, start falling
        if jump_height <= 0:
            jumping = False

    else:
        # Apply gravity
        rect.y += gravity

        # Reset jump height for next jump
        jump_height = 100

    # making a copy of the old center of the rectangle
    old_center = rect.center
    # defining angle of the rotation
    rot = (rot + rot_speed) % 360
    # rotating the original image
    new_image = py.transform.rotate(image_orig, rot)
    rect = new_image.get_rect()
    # set the rotated rectangle to the old center
    rect.center = old_center
    # drawing the rotated rectangle to the screen
    screen.blit(new_image, rect)
    # flipping the display after drawing everything
    py.display.flip()

py.quit()
