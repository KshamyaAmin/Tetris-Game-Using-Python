
from settings import *
from tetris import Tetris, Text
import sys
import pathlib
import pygame as pg
class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images
    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)
    def update(self):
        # Only update if game not over
        if not self.tetris.game_over:
            self.tetris.update()
        self.clock.tick(FPS)
    def draw(self):
        if self.tetris.game_over:
            self.draw_game_over_screen()
        else:
            self.screen.fill(color=BG_COLOR)
            self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
            self.tetris.draw()
            self.text.draw()
            pg.display.flip()
    def draw_game_over_screen(self):
        self.screen.fill(BG_COLOR)
        font = pg.font.Font(FONT_PATH, 60)
        text_surf = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(text_surf, (WIN_W // 2 - text_surf.get_width() // 2, WIN_H // 3))
        font_small = pg.font.Font(FONT_PATH, 40)
        msg1 = font_small.render("Press N for New Game", True, (255, 255, 255))
        msg2 = font_small.render("Press E to Exit", True, (255, 255, 255))
        self.screen.blit(msg1, (WIN_W // 2 - msg1.get_width() // 2, WIN_H // 2))
        self.screen.blit(msg2, (WIN_W // 2 - msg2.get_width() // 2, WIN_H // 2 + 60))
        pg.display.flip()
    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            # If game over, only process new game or exit keys
            if self.tetris.game_over:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_n:
                        self.tetris.reset()
                    elif event.key == pg.K_e:
                        pg.quit()
                        sys.exit()
                continue
            if event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
if __name__ == '__main__':
    app = App()
    app.run()
