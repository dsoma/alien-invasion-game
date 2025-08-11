import pygame
from label import Label

class BottomBar:
    """A class to represent the bottom bar of the game."""

    def __init__(self, game):
        """Initialize the bottom bar."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.screen_rect.width
        self.height = 100
        self.color = (0, 0, 0)
        self.MARGIN = 50

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottom = self.screen_rect.bottom

        # Label showing the level.
        level_label_color = (0, 135, 0)
        level_label_left_x = self.MARGIN
        level_label_center_y = self.rect.center[1]
        self.level_label = Label(self.screen,
                                 f'Level: {self.game.stats.level}',
                                 level_label_color,
                                 level_label_left_x,
                                 level_label_center_y)

        # Label showing the score.
        score_label_color = (0, 0, 135)
        score_label_left_x = level_label_left_x + self.level_label.width + self.MARGIN
        score_label_center_y = self.rect.center[1]
        self.score_label = Label(self.screen,
                                 f'Score: {self.game.stats.score}',
                                 score_label_color,
                                 score_label_left_x,
                                 score_label_center_y)

        # Label showing the high score.
        high_score_label_color = (0, 135, 135)
        high_score_label_left_x = score_label_left_x + self.score_label.width + self.MARGIN
        high_score_label_center_y = self.rect.center[1]
        self.high_score_label = Label(self.screen,
                                      f'High Score: {self.game.stats.high_score}',
                                      high_score_label_color,
                                      high_score_label_left_x,
                                      high_score_label_center_y)


        # Label showing the ships left.
        ships_left_label_color = (135, 0, 0)
        ships_left_label_left_x = high_score_label_left_x + self.high_score_label.width + self.MARGIN
        ships_left_label_center_y = self.rect.center[1]
        self.ships_left_label = Label(self.screen,
                                      f'Ships Left: {self.game.stats.ships_left}',
                                      ships_left_label_color,
                                      ships_left_label_left_x,
                                      ships_left_label_center_y)

    def draw(self):
        """Draw the bottom bar."""
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.level_label.draw()
        self.score_label.draw()
        self.high_score_label.draw()
        self.ships_left_label.draw()


    def update(self):
        """Update the bottom bar."""
        self.level_label.set_text(f'Level: {self.game.stats.level}')
        self.score_label.set_text(f'Score: {self.game.stats.score}')
        self.high_score_label.set_text(f'High Score: {self.game.stats.high_score}')
        self.ships_left_label.set_text(f'Ships Left: {self.game.stats.ships_left}')
