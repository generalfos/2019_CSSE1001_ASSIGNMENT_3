""" Handle object and world creation """

from constants import BLOCK_COLOURS, ITEM_COLOURS
from item import Item, SimpleItem, HandItem, BlockItem, MATERIAL_TOOL_TYPES, TOOL_DURABILITIES
from new_items import FoodItem, ToolItem
from block import Block, ResourceBlock, BREAK_TABLES, LeafBlock, TrickCandleFlameBlock
from new_blocks import CraftingTableBlock, Furnace
from mob import Bird, Mob
from new_mobs import Bee, Sheep

import random

def create_block(*block_id):
    """(Block) Creates a block (this function can be thought of as a block factory)

    Parameters:
        block_id (*tuple): N-length tuple to uniquely identify the block,
        often comprised of strings, but not necessarily (arguments are grouped
        into a single tuple)

    Examples:
        >>> create_block("leaf")
        LeafBlock()
        >>> create_block("stone")
        ResourceBlock('stone')
        >>> create_block("mayhem", 1)
        TrickCandleFlameBlock(1)
    """
    if len(block_id) == 1:
        block_id = block_id[0]
        if block_id == "leaf":
            return LeafBlock()
        elif block_id in ["crafting_table"]:
            return CraftingTableBlock('crafting_table')
        elif block_id in ["furnace"]:
            return Furnace('furnace')
        elif block_id in BREAK_TABLES:
            return ResourceBlock(block_id, BREAK_TABLES[block_id])

    elif block_id[0] == 'mayhem':
        return TrickCandleFlameBlock(block_id[1])

    raise KeyError(f"No block defined for {block_id}")


def create_item(*item_id):
    """(Item) Creates an item (this function can be thought of as a item factory)

    Parameters:
        item_id (*tuple): N-length tuple to uniquely identify the item,
        often comprised of strings, but not necessarily (arguments are grouped
        into a single tuple)

    Examples:
        >>> create_item("dirt")
        BlockItem('dirt')
        >>> create_item("hands")
        HandItem('hands')
        >>> create_item("pickaxe", "stone")  # *without* Task 2.1.2 implemented
        Traceback (most recent call last):
        ...
        NotImplementedError: "Tool creation is not yet handled"
        >>> create_item("pickaxe", "stone")  # *with* Task 2.1.2 implemented
        ToolItem('stone_pickaxe')
    """
    # Tool Items
    if len(item_id) == 2:

        if item_id[0] in MATERIAL_TOOL_TYPES and item_id[1] in TOOL_DURABILITIES:
            return ToolItem(item_id)

    # Other Items
    elif len(item_id) == 1:

        item_type = item_id[0]

        if item_type == "hands":
            return HandItem("hands")

        elif item_type in ["dirt", "wood", "stone", "wool", "crafting_table", "honey", "hive", "diamond",
                           "iron", "gold", "furnace", "charcoal"]:
            return BlockItem(item_type)

        elif item_type in ["apple", "cooked_apple"]:
            return FoodItem(item_type, 2)

        elif item_type in ["stick"]:
            return SimpleItem(item_type)

    raise KeyError(f"No item defined for {item_id}")


def load_simple_world(world):
    """Loads blocks and mobs into a world

    Parameters:
        world (World): The game world to load with blocks
    """
    block_weights = [
        (84, 'dirt'),
        (20, 'stone'),
        (5, 'diamond'),
        (15, 'iron'),
        (6, 'gold')
    ]

    cells = {}

    ground = []

    width, height = world.get_grid_size()

    for x in range(width):
        for y in range(height):
            if x < 22:
                if y <= 8:
                    continue
            else:
                if x + y < 30:
                    continue

            ground.append((x, y))

    weights, blocks = zip(*block_weights)
    kinds = random.choices(blocks, weights=weights, k=len(ground))

    for cell, block_id in zip(ground, kinds):
        cells[cell] = create_block(block_id)

    trunks = [(3, 8), (3, 7), (3, 6), (3, 5)]

    for trunk in trunks:
        cells[trunk] = create_block('wood')

    leaves = [(4, 3), (3, 3), (2, 3), (4, 2), (3, 2), (2, 2), (4, 4), (3, 4), (2, 4)]

    for leaf in leaves:
        cells[leaf] = create_block('leaf')

    cells[(3, 2)] = create_block('honey')
    cells[(4, 5)] = create_block('hive')

    for cell, block in cells.items():
        # cell -> box
        i, j = cell

        world.add_block_to_grid(block, i, j)

    world.add_block_to_grid(create_block("mayhem", 0), 14, 8)

    world.add_mob(Bird("friendly_bird", (12, 12)), 400, 100)

    world.add_mob(Sheep("Sheep", (20, 20)), 200, 100)