import pygame as pg

CARD_RADIUS = 8
HIGHLIGHT_COLOR = (0x22, 0x22, 0x22)
HOVER_COLOR = (0xAA, 0xAA, 0xAA)


class CardSprite(pg.sprite.Sprite):
    def __init__(self, card):
        super().__init__()
        self.card = card
        self.image = pg.image.load(f'kaarten/{str(card)}.gif').convert_alpha()
        card_size = self.image.get_size()

        mask = pg.Surface(card_size, pg.SRCALPHA)
        pg.draw.rect(mask, (255, 255, 255), (0, 0, *card_size), border_radius=CARD_RADIUS)

        self.image.blit(mask, (0, 0), None, pg.BLEND_RGBA_MIN)
        self.rect = self.image.get_rect()

    def unfocus(self):
        self.image.set_alpha(int(0xFF * 0.3))

    def selected(self):
        self.add_border(HIGHLIGHT_COLOR)

    def hover(self):
        self.add_border(HOVER_COLOR)

    def add_border(self, color):
        pg.draw.rect(self.image, color, (0, 0, *self.rect.size), 3,
                     border_radius=CARD_RADIUS)


class GridAligner:
    def __init__(self, sprite_group):
        self.sprite_group = sprite_group
        self.position = (0, 0)
        self.margin = 0
        self.columns = 1
        self.size = (0, 0)

    def align(self):
        x, y = self.position
        self.size = (0, 0)

        for idx, sprite in enumerate(self.sprite_group):
            column_idx = idx % self.columns
            row_idx = idx // self.columns
            width, height = sprite.rect.size

            sprite.rect.x = x + column_idx * (width + self.margin)
            sprite.rect.y = y + row_idx * (height + self.margin)

            self.size = (max(self.size[0], sprite.rect.right - x),
                         max(self.size[1], sprite.rect.bottom - y))
