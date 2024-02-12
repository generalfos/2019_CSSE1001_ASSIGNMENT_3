""" Item Subclasses """

__author__ = "Joel Foster"
__date__ = "22/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

from item import Item, TOOL_DURABILITIES
from constants import TOOL_RANGES

class FoodItem(Item):
    """ Food Item """
    def __init__(self, item_id, strength):
        super().__init__(item_id)
        self._strength = strength

    def get_strength(self):
        """ (int) Returns the strength of the food """
        return self._strength

    def can_attack(self) -> bool:
        """(bool) Returns False, since FoodItems cannot be used to attack"""
        return False

    def place(self):
        """Uses the selected item in the hotbar.

        Return:
            [tuple<str, tuple<str, ...>>]:
                    A list of EffectIDs resulting from placing this item. Each EffectID is a pair
                    of (effect_type, effect_sub_id) pair, where:
                      - effect_type is the type of the effect ('item', 'block', etc.)
                      - effect_sub_id is the unique identifier for an effect of a particular type
        """


        return [('food', self._id)]

class ToolItem(Item):
    """ Tool Item """
    def __init__(self, item_id):
        self._id = f'{item_id[1]}_{item_id[0]}'
        self._tool_type = item_id[0]
        self._max_durability = TOOL_DURABILITIES[item_id[1]]
        self._durability = TOOL_DURABILITIES[item_id[1]]
        self._max_stack_size = 1
        self._range = TOOL_RANGES[item_id[1]]

    def get_type(self):
        """(str) Returns tool type """
        return self._tool_type

    def get_durability(self):
        """(float) Returns tool durability """
        return self._durability

    def get_max_durability(self):
        """(float) Returns max tool durability """
        return self._max_durability

    def can_attack(self):
        """(float) Returns tool durability """
        if self._durability > 0:
            return True
        else:
            return False

    def attack(self, successful):
        """(float) Returns outcome of tool attack """
        if not successful:
            self._durability -= 1
