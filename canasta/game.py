import pygame
import sys
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Game():
    def __init__(self):
        # Below Line - Calls pygame.init (needed for other modules such as pygame.font)...
        pygame.init()
        # Below Section - Sets up the pygame window size and assigns a title caption for the game window.
        self.screen = pygame.display
        self.screen_surface = pygame.display.set_mode((1920, 1020))
        pygame.display.set_caption("Canasta")
        # -------------------------------------
        self.background = pygame.Surface([1920, 1020])
        self.background.fill((0,40,0))
        # -------------------------------------
        # Below Line - Creates the card_group Sprite Group.
        self.card_group = pygame.sprite.LayeredDirty()
        self.card_group.clear(self.screen, self.background)
        self.card_rects = None
        # -------------------------------------
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        # -------------------------------------
        self.text = self.font.render('Happy Monday, Chelsi! Still Love you!', True, (0, 255, 0), (0, 0, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = [1010, 300]
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
game = Game()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Below Function - Called by main(). Handles screen background assignment, card_group draw updating, and the pygame.display updates.
def draw_window():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # -------------------------------------
    game.card_group.update()
    game.card_rects = game.card_group.draw(game.screen_surface)
    game.screen_surface.blit(game.text, game.textRect.center)
    game.screen.update(game.card_rects)
