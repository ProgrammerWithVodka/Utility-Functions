# This function is for pygame. It takes a list of surfaces and combines them into one surface
# horizontally. This is useful for when you want to combine multiple text surfaces with different 
#colors and fonts into a single surface.
def combine_surfaces(surfaces):
    # New surface's width and height.
    new_width = 0
    new_height = 0
    # The points at which each surface will be blitted onto the new one.
    blit_points = [0]

    for idx, surface in enumerate(surfaces):
        # Adds the width of each iterated surface to the total new width.
        new_width += surface.get_width()
        # Takes largest height of all surfaces.
        if new_height < surface.get_height():
            new_height = surface.get_height()
        # Adds the blit point for this surface.
        blit_points.append(sum(blit_points[:idx + 1]) + surface.get_width())

    # Creates new surface.
    new_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA, 32)
    # Blits onto new surface.
    for idx in range(len(surfaces)):
        new_surface.blit(surfaces[idx], (blit_points[idx], 0))

    return new_surface
	
	
	
# This a universal randomizer function that takes decay and initial chance. It starts counting from 0
# until the rolled value is less than the success percent chance. That success chance is given in
# initial_chance and decreases every time the while loop runs by the decay. This means that getting
# a higher count becomes less and less probable as the loop runs. 
def decreasing_chance_randomizer(decay, initial_chance):
    # Real_chance is used to save the full decimal version of the chance for calculations.
    real_chance = initial_chance
    chance = initial_chance
    # Highest value to roll up to. Increases once the chance goes into decimals in order to remove the decimal.
    highest = 100
    roll = random.randint(1, highest)
    # The amount of times the while loop runs.
    count = 0

    # Loops until the chance fails.
    while roll <= chance:
        count += 1

        real_chance *= decay
        chance = round(real_chance, 2)
        # Checks for decimal and continuously multiplies by 10 to remove decimal.
        while chance != int(chance):
            chance *= 10
            real_chance *= 10
            highest *= 10

        roll = random.randint(1, highest)

    return count
	
	
	
# A field in which you can type text. It uses pygame.
class Field:
    def __init__(self, pos, length):
        # Draw pos of field
        self.pos = pos
        # Is the type field selected
        self.selected = False
        # Length of the type field
        self.length = length
        # The text in the type field
        self.text = ""
        # A surface that will contain the rendered text
        self.rendered_text = None
        # The position where the cursor is
        self.cursor_index = -1
        self.cursor_pos = 0
        # Counter used for the cursor blinking
        self.blink_count = 0
        # Position of text
        self.text_pos = 10

        # The surface that everything will be blitted on
        self.surface = pygame.Surface((length, 60), pygame.SRCALPHA, 32)
        self.text_surface = pygame.Surface((length - 6, 60), pygame.SRCALPHA, 32)
        # Glass type field image
        self.image = pygame.transform.scale(Constants.field_image, (length, 60))

    def draw_handler(self, screen):
        if self.selected:
            self.blink_count += 1

        self.surface.fill((255, 255, 255, 0))
        self.text_surface.fill((255, 255, 255, 0))

        # Draws text
        self.rendered_text = Constants.impact_font.render(self.text, True, (0, 255, 0))
        self.text_surface.blit(self.rendered_text, (self.text_pos, -2))
        self.surface.blit(self.text_surface, (3, 0))

        # Finds cursor position based on index
        self.cursor_pos = Constants.impact_font.render(self.text[:self.cursor_index + 1], True, (0, 0, 0)).get_width()

        # Draws glass typing field image
        self.surface.blit(self.image, (0, 0))

        # Draws cursor
        if self.blink_count % 40 < 20 and self.selected:
            pygame.draw.line(self.surface, (200, 0, 0), ((self.text_pos - 1) + self.cursor_pos, 10),
                             ((self.text_pos - 1) + self.cursor_pos, 50), 2)

        # Determines if a shift of text is needed
        if (self.text_pos - 1) + self.cursor_pos < 0:
            self.text_pos += (0 - ((self.text_pos - 1) + self.cursor_pos)) + 10
        elif (self.text_pos - 1) + self.cursor_pos > self.length:
            self.text_pos += (self.length - ((self.text_pos - 1) + self.cursor_pos)) - 10

        screen.blit(self.surface, self.pos)

    def event_handler(self, event):
        # Checks to see if the box was clicked which causes it to become selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pos[0] < event.pos[0] < self.pos[0] + self.length and self.pos[1] < event.pos[1] < self.pos[1] + 60:
                self.selected = True
            else:
                self.selected = False
        # Key presses
        elif self.selected:
            if event.unicode == " " and event.key == pygame.K_SPACE:
                self.text = self.text[:self.cursor_index + 1] + " " + self.text[self.cursor_index + 1:]
                # Shifts cursor to right
                self.cursor_index += 1
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_index > -1:
                    self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]
                    # Shifts cursor left
                    self.cursor_index -= 1

            # Checks if arrows were pressed and shifts cursor accordingly
            elif event.key == pygame.K_LEFT and self.cursor_index > -1:
                self.cursor_index -= 1
            elif event.key == pygame.K_RIGHT and self.cursor_index < len(self.text) - 1:
                self.cursor_index += 1

            elif len(event.unicode) > 0:
                self.text = self.text[:self.cursor_index + 1] + event.unicode + self.text[self.cursor_index + 1:]
                # Shifts cursor to right
                self.cursor_index += 1