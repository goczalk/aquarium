"""
File with classes of creatures
"""

import random
import math
import pygame
from render import load_png


""" CONSTANTS """
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


""" SCREEN """
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500


""" PLANCTON """
MIN_PL_RADIUS = 2
MAX_PL_RADIUS = 4
PLANCTON_FRESHNESS = 500


""" EGG """
EGG_FRESHNESS = 500

""" FISH """
MIN_FISH_SIZE = 13
MAX_FISH_SIZE = 18

FISH_YEAR = 200  # Number of units (frames) which has to pass to increase age

""" Enegry"""
MAX_ENERGY = 100
MIN_ENERGY = 1

# TODO
# MAX_ENERGY/2?
ENERGY_CHANGE_VELOCITY = MAX_ENERGY/2

# TODO
# 'slow' speed: 1 move = 1 energy point?
# 'fast' speed: 1 move = 2 energy point?
ENERGY_POINT = 0.025
ADDITIONAL_ENERGY_POINT = 0.025
MAX_HUNGRY_TIME = 0.3 * FISH_YEAR
MIN_ENERGY_HP_LOSE = 0.1 * MAX_ENERGY

""" Health points """
MAX_HP = 100
HP_FASTER_AGING = 0.2 * MAX_HP
HP_SLOWER_AGING = 0.8 * MAX_HP

SLOWER_FASTER_AGING_COUNTER = 10 # if so many times in row Energy is below/over ENERGY_FASTER_AGING/ENERGY_SLOWER_AGING
ADDITIONAL_FISH_YEAR = 0.1 * FISH_YEAR # health is decreasing (10%) faster or slower (such num is -/+ to counter)
                                       # it can be -/+ only 3 times in a row  as you can't inifnitly slower/faster aging

""" Regeneration """
HP_REGENERATION_POSSIBLE = 0.9 * MAX_HP
ENERGY_REGENERATION_POSSIBLE = 0.8 * MAX_ENERGY
REGENERATION_CYCLE = 20 # number of units fish has to wait for regeneration
ENERGY_REGENERATION_COST = 0.1 * MAX_ENERGY

""" Reproduction  """
LAYING_EGG_PROBABILITY = 1 # Probability of laying eggs is 1/(LAYING_EGG_PROBABILITY+1)
                           # if const is 3 -> probability is 25%
HP_REPRODUCTION_POSSIBLE = 0.25 * MAX_HP
ENERGY_REPRODUCTION_POSSIBLE = 0.5 * MAX_ENERGY
REPRODUCTION_POSSIBLE = 300 # Minimum number of time units between each reproduction
ENERGY_REPRODUCTION_COST = 0.2 * MAX_ENERGY
NEW_FISH_NUM = 1

""" Constants describing width and height of rectangle of energy/hp """
LABEL_HEIGHT = 5
LABEL_WIDTH = 30

""" Multiplier for increasing food value """
MULTIPLIER_FOR_FOOD = 5


class Plancton:
    """
    self.freshness - num of units that plancton is fresh
    self.radius - radius of plancton
    self.rect - Rectangle object
    self.screen - screen to display on
    self.xy - x, y position
    """
    
    def __init__(self):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        self.radius = random.randrange(MIN_PL_RADIUS, MAX_PL_RADIUS+1)
        self.xy = (x, y)
        self.rect = pygame.Rect(self.xy, (self.radius, self.radius))
        self.screen = pygame.display.get_surface()
        self.freshness = 0
    
    def is_fresh(self):
        """
        Returns true if plancton is fresh
        """
        self.freshness += 1
        return True if self.freshness < PLANCTON_FRESHNESS else False        

    def draw(self):
        pygame.draw.circle(self.screen, 0x339966, self.xy, self.radius)

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


class Fish(pygame.sprite.Sprite):
    """
    self.angle - int for angle
    self.colour - colour of the fish depending on its gender
    self.energy - current energy
    self.FONT - font for energy label
    self.gender - "male" or "female", chosen randomly on init
    self.hp - current healt points
    self.image - loaded image
    self.is_ill - boolean if has disease
    self.moves_fast - boolean, true when fish is moving fast
    self.rect - Rectangle object
    self.size - radius of the circle
    self.screen - screen to display on
    self.velocity - int for velocity
    
    # counters
    self.adding_additional_fish_year_counter_faster- counter to count that additional years to fish year are only added 3 times in a row
    self.adding_additional_fish_year_counter_slower- counter to count that additional years to fish year are only substracted 3 times in a row
    self.faster_aging_counter - counter of energies in row for faster aging 
    self.hp_time_counter - counter of frames for fish aging
    self.reproduction_counter - counter of frames until last reproduction (laying or fertilizing)
    self.regeneration_counter - counter of frames when fish is regenerating
    self.slower_aging_counter - counter of energies in row for slower aging
    """
    
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        
        # initilize font
        self.FONT = pygame.font.SysFont("monospace", 15)

        # self.image, self.rect = load_png('ball.png')
        self.randomize_gender()
        self.randomize_size()
        xy = self._init_position()
        
        self.rect = pygame.Rect(xy, (self.size, self.size))

        self.energy = MAX_ENERGY
        self.hp = MAX_HP
        self.age = 1
        self.set_colour()
        self.is_ill = False

        self.choose_point_to_chase()
        #inna nazwa niz vetor?
        self.randomize_vector()
        self.screen = pygame.display.get_surface()

        self._init_counters()
        # self.rect = pygame.draw.circle(screen, 663399, (10, 10), 15)
        # self.area = screen.get_rect()

    def _init_counters(self):
        self.age_time_counter = 0
        self.faster_aging_counter = 0
        self.slower_aging_counter = 0
        self.adding_additional_fish_year_counter_slower = 0
        self.adding_additional_fish_year_counter_faster = 0
        self.hp_time_counter = 0
        self.regeneration_counter = 0
        self.reproduction_counter = 0
        
    def _init_position(self):
        self.x = 300
        self.y = 300
        # self.x = random.randrange(SCREEN_WIDTH - self.size)
        # self.y = random.randrange(SCREEN_HEIGHT - self.size)
        #self.rect = self.rect.move(x, y)
        return (self.x, self.y)

    def randomize_gender(self):
        x = random.randrange(0, 2)
        if x == 0:
            self.gender = "female"
        else:
            self.gender = "male"
    
    def set_colour(self):
        if self.gender == "female" :
            self.colour = 0xcc0066
        else:
            self.colour = 0x333399

    def get_colour(self):
        if self.is_ill:
            return BLACK
        else:
            return self.colour

    def randomize_size(self):
        self.size = random.randrange(MIN_FISH_SIZE, MAX_FISH_SIZE+1)

    def fish_on_chasing_point(self):
        if abs(self.x - self.point_x) <= 5 and abs(self.y - self.point_y) <= 5:
            return True
        else:
            return False

    #narazie losowe punkty!
    def choose_point_to_chase(self):
        self.point_x = random.randrange(SCREEN_WIDTH - self.size)
        self.point_y = random.randrange(SCREEN_HEIGHT - self.size)
        # self.point_x = 100
        # self.point_y = 100

        #????
        dx = self.point_x - self.x
        dy = self.point_y - self.y
        #
        # if abs(dx) < 5 or dx == 0:
        #     dx = 1
        # if abs(dy) < 5:
        #     dy = 0

        print("dx" + str(dx) + "; dy: " + str(dy))
        print("point x" + str(self.point_x) + "; point y: " + str(self.point_y))
        print("x" + str(self.x) + "; y: " + str(self.y))

        self.angle_difference = math.atan2(dy, dx)

        print("diff:" + str(self.angle_difference))

    def randomize_vector(self):
        # random angle
        # self.angle = random.uniform(0, 2 * math.p3,14/6i)
        self.angle = 0
        self.change_speed()
        
    def change_speed(self):
        if self.energy >= ENERGY_CHANGE_VELOCITY:
            self.velocity = 2
            self.moves_fast = True
        elif self.energy < ENERGY_CHANGE_VELOCITY:
            self.velocity = 1
            # if self.energy <= MIN_ENERGY:
            #     self.velocity = 1
            self.moves_fast = False

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
        self.update()
        self.draw_energy_indicators()
        self.draw_hp_indicators()
        pygame.draw.circle(self.screen, self.get_colour(), (self.rect.x, self.rect.y), self.size)
        self.draw_age()

        # narysuj punkt!
        self.xy_point = (self.point_x, self.point_y)
        pygame.draw.circle(self.screen, 0x1112255, self.xy_point, 10)

    def update(self):
        """
        Updates velocity, energy, health. Draws energy and healt indicator.
        """
        # check if dead
        if self.hp > 0:

            if self.fish_on_chasing_point():
                print("HAAAAALO")
                self.choose_point_to_chase()

            self.change_angle_to_chase()
            self.rect = self.calc_new_pos()
            self.x = self.rect.x
            self.y = self.rect.y

            # TODO
            # stuck on the edges horizontal 
            # TODO
            # refactor code
            if self.x > (1000 - self.rect.width):
                self.x = 1000 - self.rect.width
                self.randomize_vector()
            elif self.x < 0:
                self.x = 0
                self.randomize_vector()
            if self.y > (500 - self.rect.height):
                self.y = 500 - self.rect.height
                self.randomize_vector()
            elif self.y < 0:
                self.y = 0
                self.randomize_vector()
            self.rect.x = self.x
            self.rect.y = self.y
            
            self.decrease_energy()
            self.change_speed_or_regenerate()
            self.decrease_hp()
            self.aging()
    
    def decrease_energy(self):
        """
        When fish is moving faster it uses up more energy.
        """
        if self.energy <= MIN_ENERGY:
            self.energy = MIN_ENERGY
            return
        self.energy -= ENERGY_POINT
        if self.moves_fast:
            self.energy -= ADDITIONAL_ENERGY_POINT

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

    def lay_eggs(self):
        """
        Returns egg object if laid or None.
        Probability of laying happening: LAYING_EGG_PROBABILITY
        """
        self.reproduction_counter += 1
        if self.gender == "female":
            if(self.reproduction_counter >= REPRODUCTION_POSSIBLE):
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
            if(self.reproduction_counter >= REPRODUCTION_POSSIBLE):
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
        x, y, width, height = self.rect
        x = x - self.size
        y = y - self.size
        y_label = y - height/0.6

        # draw rect with energy
        energy_ratio = self.energy/MAX_ENERGY
        label_width = LABEL_WIDTH * energy_ratio
        Rgb = 255
        if energy_ratio > 0.5:
            Rgb = 255 - 255 * energy_ratio
        y_rect = y - height
        if y <= height/0.8:
            y_label = y + height*1.8
            y_rect = y + height*2.4

        self.screen.blit(energy_num_label, (x, y_label))
        pygame.draw.rect(self.screen, (Rgb, 200, 0), (x, y_rect, label_width, LABEL_HEIGHT))

    def draw_hp_indicators(self):
        # render text
        hp_num_label = self.FONT.render("HP" + str(self.hp), 1, BLACK)
        x, y, width, height = self.rect
        x = x - self.size
        y = y - self.size
        y_label = y - height/1.2

        # draw rect with hp
        hp_ratio = self.hp/MAX_HP
        label_width = LABEL_WIDTH * hp_ratio
        Rgb = 255
        if hp_ratio > 0.5:
            Rgb = 255 - 255 * hp_ratio
        y_rect = y - height/5
        if y <= height/0.8:
            y_rect = y + height*3.2
            y_label = y + height*2.5

        self.screen.blit(hp_num_label, (x, y_label))
        pygame.draw.rect(self.screen, (Rgb, 200, 0), (x, y_rect, label_width, LABEL_HEIGHT))

    def draw_age(self):
        age_label = self.FONT.render(str(self.age), 1, WHITE)
        x, y, width, height = self.rect
        x = x - self.size / 2
        y = y - self.size / 2
        self.screen.blit(age_label, (x, y))

    def change_angle_to_chase(self):
        # dx = self.point_x - self.x
        # dy = self.point_y - self.y
        #
        # if abs(dx) < 5 or dx == 0:
        #     dx = 1
        # if abs(dy) < 5:
        #     dy = 0
        # division = dy/dx
        #
        # angle_difference = math.asin(division)
        # # 0.1??? const???
        # print ("moj" + str(self.angle))
        # print("diff:" + str(self.angle_difference))

        # when angle_difference will be < 0, negative value will be added => decrease angle

        # if abs(self.angle - self.angle_difference) > 0.001:
        if self.age_time_counter >= FISH_YEAR/3:
            self.angle = self.angle_difference
            # print("tu")
            # print ("moj" + str(self.angle))
            # print("diff:" + str(self.angle_difference))
            # self.angle += 0.01 * self.angle_difference
            # self.angle /= 2 * math.pi

    def calc_new_pos(self):
        dx = self.velocity * math.cos(self.angle) # * dt
        dy = self.velocity * math.sin(self.angle)
        
        # if velocity == 0, dx and dy could be == 0 which would stop the fish
        if 0 < dx < 1:
            dx = math.ceil(dx)
        elif -1 < dx < 0:
            dx = math.floor(dx)
        if 0 < dy < 1:
            dy = math.ceil(dy)
        elif -1 < dy < 0:
            dy = math.floor(dy)

        return self.rect.move(dx, dy)
    
    def increase_energy(self, value):
        self.energy += MULTIPLIER_FOR_FOOD * value
        if self.energy > MAX_ENERGY:
            self.energy = MAX_ENERGY

    def catch_disease(self):
        self.is_ill = True
