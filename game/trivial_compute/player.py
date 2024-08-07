"""
Zachary Meisner
player.py

Add module docstring here
"""

from settings import pg, CELL_SIZE, GRID_COLS, GRID_ROWS

class Player:
    def __init__(self, start_pos, color, name, id):
        self.pos = start_pos
        self.past_pos = start_pos
        self.color = color
        self.name = name
        self.size = CELL_SIZE
        self.id = id
        self.configured = False
        
    def render_text_to_circle(self, screen, text, font_size, text_color,
                              center):
        font = pg.font.Font(None, font_size)
        lines = text.split("\n")
        total_height = sum(font.render(line, True, text_color).get_height()
                           for line in lines)
        y_offset = center[1] - total_height / 2

        for line in lines:
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(
                center=(center[0], y_offset + text_surface.get_height() / 2))
            screen.blit(text_surface, text_rect.topleft)
            y_offset += text_surface.get_height()

    def move(self, direction):
        self.past_pos = self.pos

        if direction == 'LEFT':
            pos = (self.pos[0], max(self.pos[1] - 1, 0))
            if self.past_pos == (8, 0) and self.pos == (8, 0):
                pos = (max(self.pos[0] - 1, 0), self.pos[1])
                direction = 'UP'
            elif self.past_pos == (0, 0) and self.pos == (0, 0):
                pos = (min(self.pos[0] + 1, GRID_ROWS - 1), self.pos[1])
                direction = 'DOWN'

        elif direction == 'RIGHT':
            pos = (self.pos[0], min(self.pos[1] + 1, GRID_COLS - 1))
            if self.past_pos == (8, 8) and self.pos == (8, 8):
                pos = (max(self.pos[0] - 1, 0), self.pos[1])
                direction = 'UP'
            elif self.past_pos == (0, 8) and self.pos == (0, 8):
                pos = (min(self.pos[0] + 1, GRID_ROWS - 1), self.pos[1])
                direction = 'DOWN'

        elif direction == 'UP':
            pos = (max(self.pos[0] - 1, 0), self.pos[1])
            if self.past_pos == (0, 8) and self.pos == (0, 8):
                pos = (self.pos[0], max(self.pos[1] - 1, 0))
                direction = 'LEFT'
            elif self.past_pos == (0, 0) and self.pos == (0, 0):
                pos = (self.pos[0], min(self.pos[1] + 1, GRID_COLS - 1))
                direction = 'RIGHT'

        elif direction == 'DOWN':
            pos = (min(self.pos[0] + 1, GRID_ROWS - 1), self.pos[1])
            if self.past_pos == (8, 8) and self.pos == (8, 8):
                pos = (self.pos[0], max(self.pos[1] - 1, 0))
                direction = 'LEFT'
            elif self.past_pos == (8, 0) and self.pos == (8, 0):
                pos = (self.pos[0], min(self.pos[1] + 1, GRID_COLS - 1))
                direction = 'RIGHT'
        else:
            print("Don't have a valid direction to move")

        if ( # top left and top right
            pos == (1, 1) or pos == (1, 2)
            or pos == (1, 3) or pos == (1, 5)
            or pos == (1, 6) or pos == (1, 7)
            or pos == (2, 1) or pos == (2, 2)
            or pos == (2, 3) or pos == (2, 5)
            or pos == (2, 6) or pos == (2, 7)
            or pos == (3, 1) or pos == (3, 2)
            or pos == (3, 3) or pos == (3, 5)
            or pos == (3, 6) or pos == (3, 7)
            # bottom left or bottom right
            or pos == (5, 1) or pos == (5, 2)
            or pos == (5, 3) or pos == (5, 5)
            or pos == (5, 6) or pos == (5, 7)
            or pos == (6, 1) or pos == (6, 2)
            or pos == (6, 3) or pos == (6, 5)
            or pos == (6, 6) or pos == (6, 7)
            or pos == (7, 1) or pos == (7, 2)
            or pos == (7, 3) or pos == (7, 5)
            or pos == (7, 6) or pos == (7, 7)):
            print("Player can't move here!", pos)
        else:
            self.pos = pos
            if self.pos == (4, 4):
                direction = 'CHOOSE_UP_DOWN_LEFT_RIGHT'
            elif self.pos == (0, 4):
                direction = 'CHOOSE_DOWN_LEFT_RIGHT'
            elif self.pos == (8, 4):
                direction = 'CHOOSE_UP_LEFT_RIGHT'
            elif self.pos == (4, 0):
                direction = 'CHOOSE_UP_DOWN_RIGHT'
            elif self.pos == (4, 8):
                direction = 'CHOOSE_UP_DOWN_LEFT'
            print("Pos is", pos)
            return direction

    def draw(self, screen, center_x, center_y):

        radius = self.size / 4 # size of the player

        if self.color == (255, 255, 0): # yellow
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 - 25
            x = self.pos[1] * self.size + center_x + self.size / 2 + 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name[0], 30, pg.Color("black"),
                                       (x, y))
        elif self.color == (0, 255, 0): # green
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 + 25
            x = self.pos[1] * self.size + center_x + self.size / 2 - 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name[0], 30, pg.Color("black"),
                                       (x, y))
        elif self.color == (255, 0, 0): # red
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 - 25
            x = self.pos[1] * self.size + center_x + self.size / 2 - 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name[0], 30, pg.Color("white"),
                                       (x, y))
        elif self.color == (0, 0, 255): # blue
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 + 25
            x = self.pos[1] * self.size + center_x + self.size / 2 + 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name[0], 30, pg.Color("white"),
                                       (x, y))

    def get_position(self):
        return self.pos

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_configured(self):
        return self.configured

    def set_configured(self):
        self.configured = True

    def get_color(self):
        return self.color