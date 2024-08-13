import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageDraw
import pygame
import os
class ImageChangeHandler(FileSystemEventHandler):
    def __init__(self, image_path, display_function):
        self.image_path = image_path
        self.display_function = display_function

    def on_modified(self, event):
        print(event.src_path)
        if event.src_path == self.image_path:
            print(f"Image {self.image_path} has been modified.")
            self.display_function()

def display_image(screen, image_path, window_size):
    # Load the image
    try:
        image = pygame.image.load(image_path)
        
        # Scale the image to fit the window
        image = pygame.transform.scale(image, window_size)

        # Blit the image onto the screen
        screen.blit(image, (0, 0))
        pygame.display.flip()
    except:
        print("invalid read")

def main():
    image_path = "./clock.png"
    window_size = (640, 320)
    
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('LED Matrix Image Display')

    # Display the initial image
    display_image(screen, image_path, window_size)

    # Set up the file system event handler
    event_handler = ImageChangeHandler(image_path, lambda: display_image(screen, image_path, window_size))

    # Set up the observer
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()


    try:
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Sleep for a short time to reduce CPU usage
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
