""" Block Subclasses """

__author__ = "Joel Foster"
__date__ = "22/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

from block import Block, ResourceBlock, BREAK_TABLES

class HiveBlock(Block):
    """ Hive Block """
    def __init__(self, hitpoints=20):
        super().__init__()
        self._hitpoints = self._max_hitpoints = hitpoints

    def get_drops(self, luck, correct_item_used):
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

class CraftingTableBlock(ResourceBlock):
    """ Crafting Table Block"""
    def __init__(self, block_id, break_table=BREAK_TABLES, hitpoints=20):
        super().__init__(block_id, break_table)
        self._hitpoints = self._max_hitpoints = hitpoints
        self._break_table = break_table[block_id]
        self._block_id = block_id

    def get_drops(self, luck, correct_item_used):
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
        return [('item', (self._block_id,))]

    def use(self):
        return ['crafting', 'crafting_table']

class Furnace(ResourceBlock):
    """ Furnace Block """
    def __init__(self, block_id, break_table=BREAK_TABLES, hitpoints=20):
        super().__init__(block_id, break_table)
        self._hitpoints = self._max_hitpoints = hitpoints
        self._break_table = break_table[block_id]
        self._block_id = block_id

    def get_drops(self, luck, correct_item_used):
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
        return [('item', (self._block_id,))]

    def use(self):
        """ Return(tuple(str, str)): Use effect."""
        return ['crafting', 'furnace']
