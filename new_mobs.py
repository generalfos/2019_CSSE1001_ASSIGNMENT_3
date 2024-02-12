""" Several Mob Classes """

__author__ = "Joel Foster"
__date__ = "22/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

from mob import Mob, MOB_DEFAULT_TEMPO
from constants import BEE_X_SCALE, BEE_GRAVITY_FACTOR, SHEEP_X_SCALE, SHEEP_GRAVITY_FACTOR
import random, cmath, math

class Bee(Mob):
    """ Bee Mob """
    def __init__(self, mob_id, size, tempo=MOB_DEFAULT_TEMPO, max_health=1):
        super().__init__(mob_id, size)
        self._id = mob_id
        self._tempo = tempo
        self._size = size
        self._steps = 0
        self._health = self._max_health = max_health

    def step(self, time_delta, game_data, world, player):
        """Advance this bee by one time step."""

        if self._steps % 2 == 0:

            distances = []

            velocity_x, velocity_y = self.get_velocity()
            x, y = self.get_position()

            all_things = world.get_all_things()
            honey_blocks = []

            # Find all honey blocks
            for thing in all_things:
                if thing.get_id() == 'honey':
                    block_x, block_y = thing.get_position()
                    distance_to_bee = math.sqrt( (x - block_x)**2 + (y - block_y)**2)
                    honey_blocks.append((block_x, block_y))
                    distances.append(distance_to_bee)

            # Find the closest honey distance
            if len(distances) > 0:
                minimum_distance = min(distances)
            else:
                minimum_distance = 251

            # If honey block is in range set bee target to the honey block
            if minimum_distance < 250:
                min_distance_index = distances.index(minimum_distance)
                closest_x, closest_y = honey_blocks[min_distance_index]
                dx, dy = closest_x - x, closest_y - y
                velocity = velocity_x + dx, velocity_y + dy

            # Elif if player exists, set bee target to player
            elif player:
                player_x, player_y = player.get_position()
                random_factor = random.randrange(1, 2)
                dx, dy = random_factor * (player_x - x), random_factor * (player_y - y)
                velocity = velocity_x + dx, velocity_y + dy
                distance_to_player = math.sqrt((-player_x + x) ** 2 + (y - player_y) ** 2)
                if distance_to_player < 20:
                    player.change_health(change=-1)

            # Else, randomise bee movement.
            else:
                health_percentage = self._health / self._max_health
                z = cmath.rect(self._tempo * health_percentage, random.uniform(0, 2 * cmath.pi))
                dx, dy = z.real * BEE_X_SCALE, z.imag
                velocity = x + dx, y + dy - BEE_GRAVITY_FACTOR

            self.set_velocity(velocity)

        super().step(time_delta, game_data)

    def get_drops(self, luck):
        """
        Returns the things this block drops

        Parameters:
            luck (float): The player's current luck factor, a random number between [0, 1)
            correct_item_used (bool): Whether the item used to mine was correct (most
                                      often this is taken from the break table)

        Return:
            list<
                tuple<
                    str,
                    tuple<str, ...>
                >
            >: A list of effects dropped by this block. See core.py for more information

        Pre-conditions:
            0 <= luck < 1
        """
        return None

    def use(self):
        """
        Returns none as a bee cannot be used.
        """
        return None

class Sheep(Mob):
    """ Sheep Mob """
    def __init__(self, mob_id, size, tempo=MOB_DEFAULT_TEMPO, max_health=20):
        super().__init__(mob_id, size)
        self._id = mob_id
        self._size = size
        self._steps = 0
        self._tempo = tempo
        self._health = self._max_health = max_health

    def step(self, time_delta, game_data):
        """Advance this sheep by one time step."""
        # Every 20 steps; could track time_delta instead to be more precise
        if self._steps % 20 == 0:
            # a random point on a movement circle (radius=tempo), scaled by the percentage
            # of health remaining
            health_percentage = self._health / self._max_health
            z = cmath.rect(self._tempo * health_percentage, random.uniform(0, 2 * cmath.pi))

            # stretch that random point onto an ellipse that is wider on the x-axis
            dx, dy = z.real * SHEEP_X_SCALE, z.imag

            x, y = self.get_velocity()
            velocity = x + dx, y + dy - SHEEP_GRAVITY_FACTOR

            self.set_velocity(velocity)

        super().step(time_delta, game_data)

    def get_drops(self, luck):
        """
        Returns the things this block drops

        Parameters:
            luck (float): The player's current luck factor, a random number between [0, 1)

        Return:
            list<
                tuple<
                    str,
                    tuple<str, ...>
                >
            >: A list of effects dropped by this block. See core.py for more information

        Pre-conditions:
            0 <= luck < 1
        """
        return [('item', ('wool',))] * round(3 * luck)

    def use(self):
        """
        Returns none as a sheep cannot be used.
        """
        return None
