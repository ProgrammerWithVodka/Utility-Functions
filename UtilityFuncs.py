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