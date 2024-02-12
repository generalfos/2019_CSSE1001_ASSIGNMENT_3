""" List of constants and crafting recipes """

__author__ = "Joel Foster"
__date__ = "22/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

BLOCK_COLOURS = {
    'diamond': 'blue',
    'gold': 'gold',
    'iron': '#C0C0C0',
    'dirt': '#552015',
    'stone': 'grey',
    'wood': '#723f1c',
    'wool': 'white',
    'leaves': 'green',
    'crafting_table': 'pink',
    'furnace': 'black',
    'honey': 'yellow',
    'hive': 'yellow4',
    'charcoal': 'black',
}

ITEM_COLOURS = {
    'diamond': 'blue',
    'gold': 'gold',
    'iron': '#C0C0C0',
    'dirt': '#552015',
    'wool': 'white',
    'stone': 'grey',
    'wood': '#723f1c',
    'apple': '#ff0000',
    'cooked_apple': 'red',
    'leaves': 'green',
    'crafting_table': 'pink',
    'furnace': 'black',
    'cooked_apple': 'red4',
    'honey': 'yellow',
    'hive': 'yellow4',
    'charcoal': 'black',
}

TOOL_RANGES = {
    "wood": 2,
    "stone": 3,
    "iron": 5,
    "gold": 6,
    "diamond": 10
}

ATTACK_STRENGTH = {
    "hands": 2,
    "wooden_sword": 3,
    "stone_sword": 5,
    "gold_sword": 6,
    "diamond_sword": 8,
}

SHEEP_GRAVITY_FACTOR = 50
SHEEP_X_SCALE = 2.763
BEE_GRAVITY_FACTOR = 300
BEE_X_SCALE = 1.01

from grid import Stack
from item_creation import create_item
from item import SimpleItem, BlockItem

# 2x2 Crafting Recipes
CRAFTING_RECIPES_2x2 = [
    (
        (
            (None, 'wood'),
            (None, 'wood')
        ),
        Stack(create_item('stick'), 4)),
    (
        (
            ('wood', 'wood'),
            ('wood', 'wood')
        ),
        Stack(create_item('crafting_table'), 1)
    ),
    (
        (
            ('wool', 'wool'),
            ('wool', 'wool')
        ),
        Stack(create_item('wool'), 1)
    ),
    (
        (
            ('dirt', None),
            (None, None)
        ),
        Stack(create_item('dirt'), 1)
    ),
    (
        (
            ('iron', None),
            (None, None)
        ),
        Stack(create_item('diamond'), 1)
    ),
]

# 3x3 Crafting Recipes
CRAFTING_RECIPES_3x3 = {
    (
        (
            (None, None, None),
            (None, 'wood', None),
            (None, 'wood', None)
        ),
        Stack(create_item('stick'), 16)
    ),
    (
        (
            ('wood', 'wood', 'wood'),
            (None, 'stick', None),
            (None, 'stick', None)
        ),
        Stack(create_item('pickaxe', 'wood'), 1)
    ),
    (
        (
            ('wood', 'wood', None),
            ('wood', 'stick', None),
            (None, 'stick', None)
        ),
        Stack(create_item('axe', 'wood'), 1)
    ),
    (
        (
            (None, 'wood', None),
            (None, 'stick', None),
            (None, 'stick', None)
        ),
        Stack(create_item('shovel', 'wood'), 1)
    ),
    (
        (
            (None, 'stone', None),
            (None, 'stone', None),
            (None, 'stick', None)
        ),
        Stack(create_item('sword', 'wood'), 1)
    ),
    (
        (
            ('stone', 'stone', 'stone'),
            ('stone', None, 'stone'),
            ('stone', 'stone', 'stone')
        ),
        Stack(create_item('furnace'), 1)
    ),
    (
        (
            ('diamond', 'diamond', 'diamond'),
            (None, 'stick', None),
            (None, 'stick', None)
        ),
        Stack(create_item('pickaxe', 'diamond'), 1)
    ),
    (
        (
            ('iron', 'iron', 'iron'),
            (None, 'stick', None),
            (None, 'stick', None)
        ),
        Stack(create_item('pickaxe', 'iron'), 1)
    ),
    (
        (
            ('stone', 'stone', 'stone'),
            (None, 'stick', None),
            (None, 'stick', None)
        ),
        Stack(create_item('pickaxe', 'stone'), 1)
    ),

}

# Furnace Crafting Recipes
FURNACE_RECIPES = {
    (
        (
            ('apple',),
            (None,),
            ('wood',)
        ),
        Stack(create_item('cooked_apple'), 1)
    ),

    (
        (
            ('wood',),
            (None,),
            ('wood',)
        ),
        Stack(create_item('charcoal'), 16)
    ),

    (
        (
            ('diamond',),
            (None,),
            ('wood',)
        ),
        Stack(create_item('diamond'), 16)
    ),

    (
        (
            ('iron',),
            (None,),
            ('wood',)
        ),
        Stack(create_item('iron'), 16)
    ),

    (
        (
            ('gold',),
            (None,),
            ('wood',)
        ),
        Stack(create_item('gold'), 16)
    ),
}
