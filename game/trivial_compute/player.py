"""
Zachary Meisner
player.py

Add module docstring here
"""

from settings import pg, CELL_SIZE, GRID_COLS, GRID_ROWS

class Player:
    def __init__(self, start_pos, color, name):
        self.pos = start_pos
        self.color = color
        self.name = name
        self.size = CELL_SIZE

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
        if direction == 'LEFT':
            pos = (self.pos[0], max(self.pos[1] - 1, 0))
        elif direction == 'RIGHT':
            pos = (self.pos[0], min(self.pos[1] + 1, GRID_COLS - 1))
        elif direction == 'UP':
            pos = (max(self.pos[0] - 1, 0), self.pos[1])
        elif direction == 'DOWN':
            pos = (min(self.pos[0] + 1, GRID_ROWS - 1), self.pos[1])
        
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
            self.render_text_to_circle(screen, self.name, 30, pg.Color("black"),
                                       (x, y))
        elif self.color == (0, 255, 0): # green
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 + 25
            x = self.pos[1] * self.size + center_x + self.size / 2 - 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name, 30, pg.Color("black"),
                                       (x, y))
        elif self.color == (255, 0, 0): # red
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 - 25
            x = self.pos[1] * self.size + center_x + self.size / 2 - 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name, 30, pg.Color("white"),
                                       (x, y))
        elif self.color == (0, 0, 255): # blue
            # position of the player
            y = self.pos[0] * self.size + center_y + self.size / 2 + 25
            x = self.pos[1] * self.size + center_x + self.size / 2 + 25
            # Draw player
            pg.draw.circle(screen, self.color, (x, y), radius)
            pg.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)
            # Draw player name
            self.render_text_to_circle(screen, self.name, 30, pg.Color("white"),
                                       (x, y))

    def get_position(self):
        return self.pos
