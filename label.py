import pygame.font

class Label:
    """A label for the game."""

    def __init__(self, screen, msg, bg_color, width, left_x, center_y):
        """Initialize label attributes."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the label.
        self.width, self.height = width, 50
        self.bg_color = bg_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)

        # Build the label's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = left_x
        self.rect.centery = center_y

        self.set_text(msg)

    def set_text(self, msg):
        """Turn msg into a rendered image and center text on the label."""
        self.msg_image = self.font.render(msg,
                                          True,
                                          self.text_color,
                                          self.bg_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the label."""
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)