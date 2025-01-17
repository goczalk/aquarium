"""
File with classes of creatures
"""

import random
import math
import pygame

# from render import load_png

""" CONSTANTS """
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = 0x808080
SANDY = 0xfffcbb

""" SCREEN """
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

""" PLANCTON """
MIN_PL_RADIUS = 2
MAX_PL_RADIUS = 4
PLANCTON_FRESHNESS = 500

""" EGG """
EGG_FRESHNESS = 500

""" SHELTER """
SHELTER_MIN_DIMEN = 20
SHELTER_MAX_DIMEN = 80

""" FISH """
INIT_MIN_FISH_SIZE = 8
INIT_MAX_FISH_SIZE = 10
GROWING_UP_SPEED_MIN = 1
GROWING_UP_SPEED_MAX = 3

FISH_YEAR = 200  # Number of units (frames) which has to pass to increase age

# fish vision cannot be more or equal to SCREEN_WIDTH/4 -> then fish would see each other from both sides
# if aquarium would be infinite in width

""" Moving """
VISION_MULTIPLIER = 10
MAX_FISH_VISION = SCREEN_WIDTH / 5

ANGLE_CHANGE_MULTIPLIER = 0.01
MIN_SPEED = 1
MAX_SPEED = 2
CHASING_SPEED = 3

""" Energy"""
MAX_ENERGY = 100
MIN_ENERGY = 1

# TODO
# MAX_ENERGY/2?
ENERGY_CHANGE_VELOCITY = 0.3 * MAX_ENERGY

ENERGY_POINT = 0.002
MAX_HUNGRY_TIME = 0.3 * FISH_YEAR
MIN_ENERGY_HP_LOSE = 0.1 * MAX_ENERGY

""" Health points """
MAX_HP = 100
HP_FASTER_AGING = 0.2 * MAX_HP
HP_SLOWER_AGING = 0.8 * MAX_HP

SLOWER_FASTER_AGING_COUNTER = 10  # if so many times in row Energy is below/over ENERGY_FASTER_AGING/ENERGY_SLOWER_AGING
ADDITIONAL_FISH_YEAR = 0.1 * FISH_YEAR  # health is decreasing (10%) faster or slower (such num is -/+ to counter)
# it can be -/+ only 3 times in a row  as you can't inifnitly slower/faster aging

""" Regeneration """
HP_REGENERATION_POSSIBLE = 0.9 * MAX_HP
ENERGY_REGENERATION_POSSIBLE = 0.8 * MAX_ENERGY
REGENERATION_CYCLE = 40  # number of units fish has to wait for regeneration
ENERGY_REGENERATION_COST = 0.1 * MAX_ENERGY

""" Reproduction  """
LAYING_EGG_PROBABILITY = 1  # Probability of laying eggs is 1/(LAYING_EGG_PROBABILITY+1)
# if const is 3 -> probability is 25%
HP_REPRODUCTION_POSSIBLE = 0.25 * MAX_HP
ENERGY_REPRODUCTION_POSSIBLE = 0.3 * MAX_ENERGY
REPRODUCTION_POSSIBLE = 300  # Minimum number of time units between each reproduction
ENERGY_REPRODUCTION_COST = 0.2 * MAX_ENERGY

""" Constants describing width and height of rectangle of energy/hp """
LABEL_HEIGHT = 5
LABEL_WIDTH = 30

""" Multiplier for increasing food value """
MULTIPLIER_FOR_FOOD = 4


class Plancton:
    """
    self.freshness - num of units that plancton is fresh
    self.radius - radius of plancton
    self.rect - Rectangle object
    self.screen - screen to display on
    self.x - x position
    self.y - y position
    """

    def __init__(self):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        self.radius = random.randrange(MIN_PL_RADIUS, MAX_PL_RADIUS + 1)
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), (self.radius, self.radius))
        self.screen = pygame.display.get_surface()
        self.freshness = 0
        self.colour = 0x339966

    def is_fresh(self):
        """
        Returns true if plancton is fresh
        """
        self.freshness += 1
        return True if self.freshness < PLANCTON_FRESHNESS else False

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius)


class Egg:
    """
    self.freshness - num of units that egg is living
    self.radius - radius of egg
    self.rect - Rectangle object
    self.screen - screen to display on
    self.xy - x, y position
    """

    def __init__(self, x, y):
        self.radius = 1
        self.xy = (x, y)
        self.rect = pygame.Rect(self.xy, (self.radius, self.radius))
        self.screen = pygame.display.get_surface()
        self.freshness = 0

    def is_fresh(self):
        """
        Returns true if egg is fresh
        """
        self.freshness += 1
        return True if self.freshness < EGG_FRESHNESS else False

    def draw(self):
        pygame.draw.circle(self.screen, 0xff9933, self.xy, self.radius)


class Shelter:
    """
    self.rect - Rectangle object
    self.screen - screen to display on
    """
    def __init__(self):
        width = random.randrange(SHELTER_MIN_DIMEN, SHELTER_MAX_DIMEN)
        height = random.randrange(SHELTER_MIN_DIMEN, SHELTER_MAX_DIMEN)
        x = random.randrange(SCREEN_WIDTH - width)
        y = random.randrange(SCREEN_HEIGHT - height)
        self.rect = pygame.Rect(x, y, width, height)
        self.screen = pygame.display.get_surface()

    def draw(self):
        pygame.draw.rect(self.screen, SANDY, self.rect, 5)

class Fish(pygame.sprite.Sprite):
    """
    self.angle - int for angle
    self.angle_difference - difference counted to chased point
    self.chased_fish - fish which our fish want to chase
    self.colour - colour of the fish depending on its gender
    self.energy - current energy
    self.escape_from_fish - fish from which we should escape
    self.FONT - font for energy label
    self.gender - "male" or "female", chosen randomly on init
    self.growing_up_speed - speed with which fish is growing
    self.hp - current healt points
    self.image - loaded image
    self.in_shelter - boolean if fish is in shelter
    self.is_ill - boolean if has disease
    self.is_predator - boolean if is predator
    self.is_RL - boolean, True if is Reinforcement Learning fish
    self.moves_fast - boolean, true when fish is moving fast
    self.point_x - x of point to chase
    self.point_y - y of point to chase
    self.rect - Rectangle object
    self.RL_finished_chasing - boolean to determine if RL fish is on chasing point
    self.size - radius of the circle
    self.screen - screen to display on
    self.velocity - int for velocity
    self.x, self.y - current posistion
    
    # counters
    self.adding_additional_fish_year_counter_faster- counter to count that additional years to fish year are only added 3 times in a row
    self.adding_additional_fish_year_counter_slower- counter to count that additional years to fish year are only substracted 3 times in a row
    self.age_time_counter - counter to accumulate unit of passed time
    self.dx_accumulator - accumulator needed when fish is moving in very slow angle
    self.dy_accumulator - accumulator needed when fish is moving in very slow angle
    self.faster_aging_counter - counter of energies in row for faster aging
    self.hp_time_counter - counter of frames for fish aging
    self.reproduction_counter - counter of frames until last reproduction (laying or fertilizing)
    self.regeneration_counter - counter of frames when fish is regenerating
    self.size_accumulator - accumulator for size
    self.slower_aging_counter - counter of energies in row for slower aging
    """

    def __init__(self, rl=False, energy_point=None, multiplier_for_food=None):
        """
        :param rl: for reinforcement learning fish, it has different params when initilised and
            not randomly chosen point to chase
        :param energy_point: for configuration tests, changing global
        :param multiplier_for_food: for configuration tests, changing global
        """
        # pygame.sprite.Sprite.__init__(self)

        # initilize font
        self.FONT = pygame.font.SysFont("monospace", 15)

        # self.image, self.rect = load_png('ball.png')

        if rl:
            self.is_RL = True
            self.gender = "female"
            self.colour = 0xFF6E4A
            self.size = 9
            self.growing_up_speed = 2
            self.is_predator = False
            self.RL_finished_chasing = False
        else:
            self.is_RL = False
            self.randomize_gender()
            self.set_colour()
            self.randomize_size()
            self.randomize_growing_up_speed()
            self.randomize_predatory()

        xy = self._init_position()

        self.rect = pygame.Rect(xy, (self.size, self.size))

        self.energy = MAX_ENERGY
        self.hp = MAX_HP
        self.age = 1
        self.is_ill = False

        self.in_shelter = False
        self.chased_fish = None
        self.escape_from_fish = None
        self.init_vector()
        self.choose_random_point_to_chase()
        self.screen = pygame.display.get_surface()

        self._init_counters()

        #### for configuration tests
        if energy_point:
            global ENERGY_POINT
            ENERGY_POINT = energy_point
        if multiplier_for_food:
            global MULTIPLIER_FOR_FOOD
            MULTIPLIER_FOR_FOOD = multiplier_for_food

    def _init_counters(self):
        self.age_time_counter = 0
        self.faster_aging_counter = 0
        self.slower_aging_counter = 0
        self.adding_additional_fish_year_counter_slower = 0
        self.adding_additional_fish_year_counter_faster = 0
        self.hp_time_counter = 0
        self.regeneration_counter = 0
        self.reproduction_counter = 0
        self.dx_accumulator = 0
        self.dy_accumulator = 0
        self.size_accumulator = 0

    def _init_position(self):
        self.x = random.randrange(SCREEN_WIDTH - self.size)
        self.y = random.randrange(SCREEN_HEIGHT - self.size)
        return (self.x, self.y)

    def randomize_gender(self):
        x = random.randrange(0, 2)
        if x == 0:
            self.gender = "female"
        else:
            self.gender = "male"

    def randomize_predatory(self):
        x = random.randrange(0, 3)
        if x == 0:
            self.is_predator = True
        else:
            self.is_predator = False

    def set_colour(self):
        if self.gender == "female":
            self.colour = 0xcc0066
        else:
            self.colour = 0x333399

    def get_colour(self):
        if self.is_ill:
            return BLACK
        else:
            return self.colour

    def randomize_size(self):
        self.size = random.randrange(INIT_MIN_FISH_SIZE, INIT_MAX_FISH_SIZE + 1)

    def randomize_growing_up_speed(self):
        self.growing_up_speed = random.randrange(GROWING_UP_SPEED_MIN, GROWING_UP_SPEED_MAX + 1)

    def fish_on_chasing_point(self):
        if abs(self.x - self.point_x) <= 10 and abs(self.y - self.point_y) <= 10:
            return True
        else:
            return False

    def set_chased_fish(self, fish):
        self.chased_fish = fish

    def set_escape_from_fish(self, fish):
        self.escape_from_fish = fish

    def choose_random_point_to_chase(self):
        self.point_x = random.randrange(SCREEN_WIDTH - self.size)
        self.point_y = random.randrange(SCREEN_HEIGHT - self.size)

    def calculate_angle_diff(self):
        self.check_if_escape_and_chased_fish_visible()

        if self.escape_from_fish is not None:
            self.set_chasing_speed()
            dx = self.x - self.escape_from_fish.x
            dy = self.y - self.escape_from_fish.y

            if dx > 0:
                chased_point_x = self.x + dx
            else:
                chased_point_x = self.escape_from_fish.x * (-1)

            if dy > 0:
                chased_point_y = self.y + dy
            else:
                chased_point_y = self.escape_from_fish.y * (-1)

        elif self.chased_fish is not None:
            self.set_chasing_speed()
            chased_point_x = self.chased_fish.x
            chased_point_y = self.chased_fish.y
        else:
            chased_point_x = self.point_x
            chased_point_y = self.point_y

        dx = chased_point_x - self.x
        # zeby zamienic na kartezjanski uklad -> zeby odpowiadal katowi
        dy = (chased_point_y - self.y) * -1

        self.angle_difference = math.atan2(dy, dx)
        if self.angle_difference < 0:
            self.angle_difference += 2 * math.pi

    def check_if_escape_and_chased_fish_visible(self):
        if not is_still_visible_by(self.chased_fish, self):
            self.chased_fish = None
        if not is_still_visible_by(self.escape_from_fish, self):
            self.escape_from_fish = None

    def init_vector(self):
        # angle is same as in cartesian, +30deg (byt in radians) rotate to te left from OX, -30deg/330 rotates right
        self.angle = random.uniform(0, 2 * math.pi)
        self.change_speed()

    def change_speed(self):
        if self.energy >= ENERGY_CHANGE_VELOCITY:
            self.velocity = MAX_SPEED
        elif self.energy < ENERGY_CHANGE_VELOCITY:
            self.velocity = MIN_SPEED

    def set_chasing_speed(self):
        """
        When fish is chasing another fish it uses as much energy as it can.
        """
        if self.energy > MIN_ENERGY and self.energy > CHASING_SPEED * ENERGY_POINT:
            self.velocity = CHASING_SPEED

    def change_speed_or_regenerate(self):
        if self.hp <= HP_REGENERATION_POSSIBLE and self.energy >= ENERGY_REGENERATION_POSSIBLE:
            self.regeneration_counter += 1
            # fish is not moving when regenerating
            self.velocity = 0
            if self.regeneration_counter >= REGENERATION_CYCLE:
                self.hp += 1
                if self.hp > MAX_HP:
                    self.hp = MAX_HP
                self.energy -= ENERGY_REGENERATION_COST
        else:
            self.regeneration_counter = 0
            self.change_speed()

    def draw(self):
        # check if dead
        if self.hp > 0:
            self.update()
            self.draw_energy_indicators()
            self.draw_hp_indicators()
        self.draw_circles_and_age()

    def draw_circles_and_age(self):
        pygame.draw.circle(self.screen, self.get_colour(), (self.rect.x, self.rect.y), self.size)
        if self.is_predator:
            pygame.draw.circle(self.screen, GREY, (self.rect.x, self.rect.y), int(self.size * 0.6))
        self.draw_age()
        # self.area = screen.get_rect()

    def update(self):
        """
        Updates velocity, energy, health. Draws energy and health indicator.
        """
        if self.fish_on_chasing_point():
            if self.is_RL:
                self.RL_finished_chasing = True
            else:
                self.choose_random_point_to_chase()

        self.change_angle_to_chase()
        self.calc_new_pos()

        # TODO
        # stuck on the edges horizontal
        # TODO
        # refactor code
        if self.x > (1000 - self.rect.width):
            self.x = 1000 - self.rect.width
            self.init_vector()
        elif self.x < 0:
            self.x = 0
            self.init_vector()
        if self.y > (500 - self.rect.height):
            self.y = 500 - self.rect.height
            self.init_vector()
        elif self.y < 0:
            self.y = 0
            self.init_vector()
        self.rect.x = self.x
        self.rect.y = self.y

        self.decrease_energy()
        self.change_speed_or_regenerate()
        self.decrease_hp()
        self.aging()

    def decrease_energy(self):
        """
        When fish is moving faster, it uses up more energy.
        When fish is bigger, it uses up more energy.
        """
        if self.energy <= MIN_ENERGY:
            self.energy = MIN_ENERGY
            return
        self.energy -= self.velocity * ENERGY_POINT * self.size

    def decrease_hp(self):
        """
        Hp is decreasing when fish is hungry (does not have enough energy) or is sick for particular amount of time.
        It loses hp, one when hungry and one when sick. If both are True, it loses double hp.
        """
        if self.energy < MIN_ENERGY_HP_LOSE or self.is_ill:
            self.hp_time_counter += 1
            if self.hp_time_counter >= MAX_HUNGRY_TIME:
                if self.energy < MIN_ENERGY_HP_LOSE:
                    self.hp -= 1
                if self.is_ill:
                    self.hp -= 1

                self.hp_time_counter = 0
        else:
            self.hp_time_counter = 0

    def aging(self):
        """
        Age is increasing as fish is aging (time is passing).
        One frame, so one update, is one unit of time.
        Slower and faster aging according to hp.
        If in row HP is below/over HP_FASTER_AGING/HP_SLOWER_AGING
        health is decreasing 10% faster or slower
        It can be -/+ only 3 in a row times as you can't inifnitly slower/faster aging
        """
        self.age_time_counter += 1

        if self.energy >= HP_SLOWER_AGING:
            self.slower_aging_counter += 1
        else:
            self.slower_aging_counter = 0
            self.adding_additional_fish_year_counter_slower = 0

        if self.energy <= HP_FASTER_AGING:
            self.faster_aging_counter += 1
        else:
            self.faster_aging_counter = 0
            self.adding_additional_fish_year_counter_faster = 0

        # It can be -/+ only 3 times in a row as you can't inifnitly slower/faster aging
        if self.adding_additional_fish_year_counter_slower <= 3:
            # it is disposable boost up/down
            if self.slower_aging_counter >= SLOWER_FASTER_AGING_COUNTER:
                self.age_time_counter = self.age_time_counter - ADDITIONAL_FISH_YEAR
                self.adding_additional_fish_year_counter_slower += 1
                self.slower_aging_counter = 0

        if self.adding_additional_fish_year_counter_faster <= 3:
            if self.faster_aging_counter >= SLOWER_FASTER_AGING_COUNTER:
                self.age_time_counter = self.age_time_counter + ADDITIONAL_FISH_YEAR
                self.adding_additional_fish_year_counter_faster += 1
                self.faster_aging_counter = 0

        if self.age_time_counter >= FISH_YEAR:
            self.age += 1
            self.age_time_counter = 0
            self.grow_up()

    def grow_up(self):
        self.size_accumulator += self.growing_up_speed / self.age

        if self.size_accumulator >= 1:
            self.size += 1
            self.size_accumulator -= 1
            self.rect = pygame.Rect((self.rect.x, self.rect.y), (self.size, self.size))

    def lay_eggs(self):
        """
        Returns egg object if laid or None.
        Probability of laying happening: LAYING_EGG_PROBABILITY
        """
        self.reproduction_counter += 1
        if self.gender == "female":
            if (self.reproduction_counter >= REPRODUCTION_POSSIBLE):
                if self.hp >= HP_REPRODUCTION_POSSIBLE and self.energy >= ENERGY_REPRODUCTION_POSSIBLE:
                    q = random.randrange(0, LAYING_EGG_PROBABILITY)
                    if q == 0:
                        self.energy -= ENERGY_REPRODUCTION_COST
                        self.reproduction_counter = 0
                        self.draw_energy_indicators()
                        return Egg(self.rect.x, self.rect.y)

    def fertilize_eggs(self):
        """
        Probability of fertilizing happening: LAYING_EGG_PROBABILITY
        Returns True if successful, and False otherwise
        """
        self.reproduction_counter += 1
        if self.gender == "male":
            if self.reproduction_counter >= REPRODUCTION_POSSIBLE:
                if self.hp >= HP_REPRODUCTION_POSSIBLE and self.energy >= ENERGY_REPRODUCTION_POSSIBLE:
                    q = random.randrange(0, LAYING_EGG_PROBABILITY)
                    if q == 0:
                        self.energy -= ENERGY_REPRODUCTION_COST
                        self.reproduction_counter = 0
                        self.draw_energy_indicators()
                        return True
        return False

    def draw_energy_indicators(self):
        # render text
        energy_num_label = self.FONT.render("E" + str(math.floor(self.energy)), 1, BLACK)
        x, y, _, _ = self.rect
        x = x - self.size

        if y - self.size < 40:
            y = y + self.size / 2 + 1
            y_label = y + 6
            y_rect = y + 19
        else:
            y = y - self.size / 2 - 1
            y_label = y - 42
            y_rect = y - 27

        # draw rect with energy
        energy_ratio = self.energy / MAX_ENERGY
        label_width = LABEL_WIDTH * energy_ratio
        Rgb = 255
        if energy_ratio > 0.5:
            Rgb = 255 - 255 * energy_ratio

        self.screen.blit(energy_num_label, (x, y_label))
        pygame.draw.rect(self.screen, (Rgb, 200, 0), (x, y_rect, label_width, LABEL_HEIGHT))

    def draw_hp_indicators(self):
        # render text
        hp_num_label = self.FONT.render("HP" + str(self.hp), 1, BLACK)
        x, y, _, _ = self.rect
        x = x - self.size

        if y - self.size < 40:
            y = y + self.size / 2 + 1
            y_label = y + 24
            y_rect = y + 37
        else:
            y = y - self.size / 2 - 1
            y_label = y - 23
            y_rect = y - 10

        # draw rect with hp
        hp_ratio = self.hp / MAX_HP
        label_width = LABEL_WIDTH * hp_ratio
        Rgb = 255
        if hp_ratio > 0.5:
            Rgb = 255 - 255 * hp_ratio

        self.screen.blit(hp_num_label, (x, y_label))
        pygame.draw.rect(self.screen, (Rgb, 200, 0), (x, y_rect, label_width, LABEL_HEIGHT))

    def draw_age(self):
        age_label = self.FONT.render(str(self.age), 1, WHITE)
        x, y, width, height = self.rect
        x = x - self.size / 2
        y = y - self.size / 2
        self.screen.blit(age_label, (x, y))

    def change_angle_to_chase(self):
        self.calculate_angle_diff()
        if self.angle < self.angle_difference:
            self.angle += ANGLE_CHANGE_MULTIPLIER * self.angle_difference

    def calc_new_pos(self):
        dx = self.velocity * round(math.cos(self.angle), 3)  # * dt
        dy = -self.velocity * round(math.sin(self.angle), 3)

        # accumulators will always be positive
        # get piece after decimal point
        self.dx_accumulator += abs(dx) % 1
        self.dy_accumulator += abs(dy) % 1

        if self.dx_accumulator >= 1:
            # depending on actucal sing of dx, add or subtract
            to_add = math.floor(self.dx_accumulator)
            if dx > 0:
                dx += to_add
            else:
                dx -= to_add
            self.dx_accumulator -= 1

        if self.dy_accumulator >= 1:
            to_add = math.floor(self.dy_accumulator)
            if dy > 0:
                dy += to_add
            else:
                dy -= to_add
            self.dy_accumulator -= 1

        self.rect = self.rect.move(dx, dy)
        self.x = self.rect.x
        self.y = self.rect.y

    def increase_energy(self, value):
        self.energy += MULTIPLIER_FOR_FOOD * value
        if self.energy > MAX_ENERGY:
            self.energy = MAX_ENERGY

    def catch_disease(self):
        self.is_ill = True


""" GENERAL FUNCTIONS """


def is_in_vision(fish, dist):
    if dist <= MAX_FISH_VISION and dist <= fish.size * VISION_MULTIPLIER:
        return True
    return False


def calculate_distance(first, second):
    dist = math.sqrt((first.x - second.x) * (first.x - second.x) +
                     (first.y - second.y) * (first.y - second.y))
    return dist


def is_still_visible_by(fish_to_see, fish):
    if fish_to_see is None:
        return False
    dist = calculate_distance(fish, fish_to_see)
    return is_in_vision(fish_to_see, dist)
