import pygame as pg
from lib import logic, ui
from typing import Optional, Tuple, Set
import math


class Game:
    # Game constants
    BOOT_SIZE = (100, 100)
    BG_COLOR = (0xD0, 0xD0, 0xD0)
    TEXT_COLOR = (0x22, 0x22, 0x22)
    BUTTON_COLOR = (0x24, 0xA0, 0xED)
    BUTTON_PRESSED_COLOR = (0x11, 0x83, 0xCA)
    CARD_MARGIN = 16
    WINDOW_MARGIN = 32

    # Game state variables
    game_logic: Optional[logic.Set] = None
    user_points: int
    computer_points: int
    start_ticks: Optional[int]
    user_selection: Set[logic.Card]
    found_set: Optional[Tuple[logic.Card, logic.Card, logic.Card]]
    mouse_position: Tuple[int, int]
    is_user_found: bool
    is_no_sets: bool
    is_mouse_down: bool

    # Variable label texts
    info_text: str
    set_found_text: str

    def __init__(self, search_time):
        self.search_time = search_time

        # Setup UI
        pg.init()
        self.screen = pg.display.set_mode(Game.BOOT_SIZE)
        self.font = pg.font.Font(None, 30)
        self.card_sprites = pg.sprite.Group()
        self.card_aligner = ui.GridAligner(self.card_sprites)

        # Setup aligner config
        self.card_aligner.margin = Game.CARD_MARGIN
        self.card_aligner.columns = 4
        self.card_aligner.position = (Game.WINDOW_MARGIN, Game.WINDOW_MARGIN)

    def start(self):
        while True:
            # Handle game events (quitting and mouse interaction)
            self.handle_events()

            # Setup state if started first time
            if self.game_logic is None:
                # Initialize game state
                self.setup_state()
                self.start_ticks = pg.time.get_ticks()

            # Sets up card UI and aligns in 3x4 grid
            self.setup_cards()

            # Enables card hovering and clicking while searching
            if self.found_set is None:
                self.handle_card_interaction()

            # Checks user selection for Sets or processes computer move if time's up
            self.handle_moves()

            # Calculate layout values
            content_size = [dim + 2 * Game.WINDOW_MARGIN for dim in self.card_aligner.size]
            content_size[1] += (self.font.get_height() + Game.WINDOW_MARGIN) * 2
            text_y = self.card_aligner.size[1] + 2 * Game.WINDOW_MARGIN

            # Resize screen if necessary
            if self.screen.get_size() == Game.BOOT_SIZE:
                self.screen = pg.display.set_mode(content_size)

            # Drawing
            self.screen.fill(Game.BG_COLOR)
            info_label = self.font.render(self.info_text, True, Game.TEXT_COLOR)
            score_label = self.font.render(f'{self.user_points} - {self.computer_points} '
                                           f'(you - computer)', True, Game.TEXT_COLOR)
            self.card_sprites.draw(self.screen)
            self.screen.blit(info_label, (Game.WINDOW_MARGIN, text_y))
            self.screen.blit(score_label, (Game.WINDOW_MARGIN, text_y + Game.WINDOW_MARGIN +
                                           self.font.get_height()))

            # Draws button and handles interactions
            self.handle_button_interaction(text_y)

            # Show display update
            pg.display.update()

    def setup_state(self):
        self.game_logic = logic.Set()

        # Track score
        self.user_points = 0
        self.computer_points = 0

        self.start_ticks = None  # Ticks at the start of the current search
        self.user_selection = set()  # Holds cards selected by the user
        self.found_set = None  # Holds the found Set, if any, either by user or computer
        self.mouse_position = (0, 0)  # Mouse position coordinates for hit testing

        self.is_user_found = False  # Is the found Set found by the user? False if computer found.
        self.is_no_sets = False  # Set True whenever there is no Set
        self.is_mouse_down = False  # Set True when mouse is down

    def setup_cards(self):
        # Remove old card sprites
        self.card_sprites.remove(self.card_sprites.sprites())

        # Add all card sprites (with appropriate styling)
        for card in self.game_logic.table:
            card_sprite = ui.CardSprite(card)

            if self.found_set is None:
                if card in self.user_selection:
                    card_sprite.selected()
            elif card not in self.found_set:
                card_sprite.unfocus()

            self.card_sprites.add(card_sprite)

        # Align card sprites
        self.card_aligner.align()

    def handle_card_interaction(self):
        for card_sprite in self.card_sprites:
            # Check if cursor is over card sprite
            if card_sprite.rect.collidepoint(*self.mouse_position):
                card = card_sprite.card

                if card not in self.user_selection:
                    card_sprite.hover()

                    if self.is_mouse_down:
                        self.user_selection.add(card)
                elif self.is_mouse_down:
                    self.user_selection.remove(card)

    def handle_moves(self):
        if len(self.user_selection) == 3:
            # Validate user selection
            if self.game_logic.is_set(*self.user_selection):
                self.is_user_found = True
            else:
                self.user_selection = set()

        if self.is_user_found:
            if self.found_set is None:
                # User found a Set!
                self.found_set = tuple(self.user_selection)
                self.info_text = 'Great! You found a Set.'
                self.user_points += 1
        else:
            time_remaining = self.search_time - (pg.time.get_ticks() - self.start_ticks)

            if time_remaining >= 0:
                # Instruct the user to search Sets
                self.info_text = f'Click on three cards that form a Set. ' \
                                 f'{math.ceil(time_remaining / 1000)}s left!'
            else:
                if self.found_set is None:
                    # Setup computer generated Sets
                    set_generator = self.game_logic.set_generator()

                    # Try to yield the first found Set
                    try:
                        self.found_set = next(set_generator)
                        self.set_found_text = 'Computer gets a point.'
                        self.computer_points += 1
                    except StopIteration:
                        # No Set can be found in the current table
                        self.set_found_text = 'There were no Sets.'
                        self.is_no_sets = True

                        # If there are no more cards to be added, the game is over
                        if len(self.game_logic.deck) == 0:
                            self.set_found_text = 'Game is over.'

                    self.info_text = f'Time\'s up. {self.set_found_text}'

    def handle_button_interaction(self, button_y):
        if self.found_set or self.is_no_sets:
            button_text = 'New Game' if self.is_no_sets and len(self.game_logic.deck) == 0 \
                else 'Continue'     # Choose appropriate button text

            button_label = self.font.render(button_text, True, Game.BUTTON_COLOR)
            button_x = self.screen.get_width() - Game.WINDOW_MARGIN - button_label.get_width()
            is_hover = button_label.get_rect().collidepoint(self.mouse_position[0] - button_x,
                                                            self.mouse_position[1] - button_y)

            if is_hover:
                button_label = self.font.render(button_text, True, Game.BUTTON_PRESSED_COLOR)

                if self.is_mouse_down:
                    game_over = False

                    # Remove Set if there is one, otherwise remove first three cards from table
                    if self.found_set:
                        self.game_logic.remove_from_table(self.found_set)
                    else:
                        self.game_logic.remove_from_table(self.game_logic.table[:3])

                        # If there are no more cards to be added, the game is over
                        if len(self.game_logic.deck) == 0:
                            game_over = True

                    # Prepare state for next round
                    self.user_selection = set()
                    self.found_set = None
                    self.is_user_found = False
                    self.is_no_sets = False
                    self.game_logic.fill_table()

                    if game_over:
                        # Resets the game and start time
                        self.setup_state()
                        self.start_ticks = pg.time.get_ticks()
                    else:
                        # Set start time for next round
                        self.start_ticks = pg.time.get_ticks()

            # Actually draw button to screen
            self.screen.blit(button_label, (button_x, button_y))

    def handle_events(self):
        self.is_mouse_down = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                print('Bye, see you next time!\n')
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.is_mouse_down = True

        self.mouse_position = pg.mouse.get_pos()
