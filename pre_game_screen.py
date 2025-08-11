from label import Label
from button import Button

class PreGameScreen:
    """A class to represent the pre-game screen."""

    def __init__(self, game):
        """Initialize the pre-game screen."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.play_button = Button(self.game, "Play")

        self.score_label = Label(self.screen,
                                f"Score: {self.game.stats.score:,}",
                                (0, 0, 255),
                                self.play_button.rect.width,
                                self.play_button.rect.left,
                                self.play_button.rect.center[1] - 100)

        self.game_over_label = Label(self.screen,
                                     "Game Over",
                                     (255, 0, 0),
                                     self.play_button.rect.width,
                                     self.play_button.rect.left,
                                     self.score_label.rect.center[1] - 100)


    def draw(self):
        """Draw the pre-game screen."""
        if self.game.game_lost:
            self.score_label.set_text(f'Score: {self.game.stats.score:,}')
            self.game_over_label.draw()
            self.score_label.draw()
        self.play_button.draw()




