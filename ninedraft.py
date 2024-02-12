"""
Simple 2d world where the player can interact with the items in the world.
"""

__author__ = "Joel Foster"
__date__ = "31/05/2019"
__version__ = "1.2.0"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk
import random
from collections import namedtuple

import pymunk
from constants import *

from tkinter import messagebox
from block import Block, ResourceBlock, BREAK_TABLES, LeafBlock, TrickCandleFlameBlock
from grid import Stack, Grid, SelectableGrid, ItemGridView
from item import Item, SimpleItem, HandItem, BlockItem, MATERIAL_TOOL_TYPES, TOOL_DURABILITIES
from player import Player
from dropped_item import DroppedItem
from crafting import GridCrafter, CraftingWindow
from world import World
from core import positions_in_range
from game import GameView, WorldViewRouter
from mob import Bird, Mob
from new_blocks import HiveBlock
from new_items import FoodItem, ToolItem
from status_view import StatusView
from new_mobs import Bee, Sheep
from item_creation import create_block, create_item, load_simple_world

BLOCK_SIZE = 2 ** 5
GRID_WIDTH = 2 ** 5
GRID_HEIGHT = 2 ** 4

GameData = namedtuple('GameData', ['world', 'player'])

class Ninedraft:
    """High-level app class for Ninedraft, a 2d sandbox game"""

    def __init__(self, master):
        """Constructor

        Parameters:
            master (tk.Tk): tkinter root widget
        """

        self._master = master
        self._mouse_focus = True
        self._status_view = None

        # Launch game
        self.new_game()

        self._crafting_window = None
        self._master.bind("e",
                          lambda e: self.run_effect(('crafting', "basic")))

        self._view = GameView(master, self._world.get_pixel_size(), WorldViewRouter(BLOCK_COLOURS, ITEM_COLOURS))
        self._view.pack()

        # Mouse Movement
        self._master.bind("<Button-1>", self._left_click)
        self._master.bind("<Button-3>", self._right_click)
        self._master.bind("<Motion>", self._mouse_move)
        self._view.bind("<Leave>", self._leave)
        self._view.bind("<Enter>", self._enter)

        self._status_view = StatusView(master, self._player)
        self._status_view.pack(side=tk.TOP, fill=None)

        self._hot_bar_view = ItemGridView(master, self._hot_bar.get_size())
        self._hot_bar_view.pack(side=tk.TOP, fill=tk.X)

        # Player Movement
        self._master.bind("<space>", lambda e: self._jump())
        self._master.bind("a", lambda e: self._move(-1, 0))
        self._master.bind("<Left>", lambda e: self._move(-1, 0))
        self._master.bind("d", lambda e: self._move(1, 0))
        self._master.bind("<Right>", lambda e: self._move(1, 0))
        self._master.bind("s", lambda e: self._move(0, 1))
        self._master.bind("<Down>", lambda e: self._move(0, 1))

        # Hotbar Binds
        self._master.bind("1", lambda e: self._hot_bar.toggle_selection((0, 0)))
        self._master.bind("2", lambda e: self._hot_bar.toggle_selection((0, 1)))
        self._master.bind("3", lambda e: self._hot_bar.toggle_selection((0, 2)))
        self._master.bind("4", lambda e: self._hot_bar.toggle_selection((0, 3)))
        self._master.bind("5", lambda e: self._hot_bar.toggle_selection((0, 4)))
        self._master.bind("6", lambda e: self._hot_bar.toggle_selection((0, 5)))
        self._master.bind("7", lambda e: self._hot_bar.toggle_selection((0, 6)))
        self._master.bind("8", lambda e: self._hot_bar.toggle_selection((0, 7)))
        self._master.bind("9", lambda e: self._hot_bar.toggle_selection((0, 8)))
        self._master.bind("0", lambda e: self._hot_bar.toggle_selection((0, 9)))

        # MenuBar
        menubar = tk.Menu(master)
        self._master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label='New Game', command=self.new_game)
        filemenu.add_command(label='Exit', command=self.close)

        # Event handler for closing application by cross
        master.protocol("WM_DELETE_WINDOW", self.close)

        self._target_in_range = False
        self._target_position = 0, 0

        self.redraw()

        self.step()

    def redraw(self):
        """ Redraw all objects. """
        self._view.delete(tk.ALL)

        # physical things
        self._view.draw_physical(self._world.get_all_things())

        # target
        target_x, target_y = self._target_position
        target = self._world.get_block(target_x, target_y)
        cursor_position = self._world.grid_to_xy_centre(*self._world.xy_to_grid(target_x, target_y))

        # Show or hide target
        if not self._mouse_focus:
            self._view.hide_target()
        elif self._target_in_range and self._mouse_focus:
            self._view.show_target(self._player.get_position(), self._target_position)

        # Update Status View
        self._status_view.update_health()
        self._status_view.update_food()

        # hot bar
        self._hot_bar_view.render(self._hot_bar.items(), self._hot_bar.get_selected())

    def step(self):
        data = GameData(self._world, self._player)
        self._world.step(data)
        self.check_target()

        # Handle the player's death.
        if self._player.get_health() <= 0:
            self._world.remove_player(self._player)
            self.death()

        self.redraw()

        self._master.after(15, self.step)

    def _move(self, dx, dy):
        """ Change the player's velocity

            Parameters:
                dx(float): Change in x velocity
                dy(float): Change in y velocity
        """
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x + dx * 80, velocity.y + dy * 80))

    def _jump(self):
        """ Player Action: Jump """
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x * 0.5, velocity.y - 250))

    def mine_block(self, block, x, y):
        """ Event: Player mining block.

            Parameters:
                block(BLOCK()): Block
                x(float): x coordinate of block
                y(float): y coordinate of block
        """
        luck = random.random()

        active_item, effective_item = self.get_holding()

        if self._target_in_range:

            was_item_suitable, was_attack_successful = block.mine(effective_item, active_item, luck)

            effective_item.attack(was_attack_successful)

            if block.is_mined():
                if self._player.get_food() > 0:
                    self._player.change_food(change=-0.5)
                    # Handle if the food becomes negative
                    if self._player.get_food() < 0:
                        self._player.change_food(change=-(self._player.get_food()))
                else:
                    self._player.change_health(change=-1)

                drops = block.get_drops(luck, was_item_suitable)
                self._world.remove_thing(thing=block)

                if block.get_id() == 'hive':
                    for i in range(5):
                        self._world.add_mob(Bee("Bee", (9, 9)), x, y)

                if not drops:
                    return None

                x0, y0 = block.get_position()

                for i, (drop_category, drop_types) in enumerate(drops):
                    print(f'Dropped {drop_category}, {drop_types}')

                    if drop_category == "item":
                        physical = DroppedItem(create_item(*drop_types))

                        # this is so bleh
                        x = x0 - BLOCK_SIZE // 2 + 5 + (i % 3) * 11 + random.randint(0, 2)
                        y = y0 - BLOCK_SIZE // 2 + 5 + ((i // 3) % 3) * 11 + random.randint(0, 2)

                        self._world.add_item(physical, x, y)
                    elif drop_category == "block":
                        self._world.add_block(create_block(*drop_types), x, y)
                    else:
                        raise KeyError(f"Unknown drop category {drop_category}")
        else:
            return None

    def damage_mob(self, mob):
        """ Event: Attacking mob.

            Parameter:
                mob(Mob): Mob
        """

        luck = random.random()
        active_item, effective_item = self.get_holding()

        if self._target_in_range:

            # Handle if Mob is Sheep
            if mob.get_id() == 'Sheep':
                x, y = mob.get_position()
                physical = DroppedItem(create_item('wool'))
                self._world.add_item(physical, x, y)
                return None

            if active_item in ATTACK_STRENGTH:
                damage = -(ATTACK_STRENGTH[active_item])
            else:
                damage = -1
            mob.change_health(damage)
            print(f'Did {-(damage)} to {mob}')

            if mob.is_dead():
                drops = mob.get_drops(luck)

                x0, y0 = mob.get_position()
                if drops:
                    for i, (drop_category, drop_types) in enumerate(drops):
                        print(f'Dropped {drop_category}, {drop_types}')

                        if drop_category == "item":
                            physical = DroppedItem(create_item(*drop_types))

                            x = x0 - BLOCK_SIZE // 2 + 5 + (i % 3) * 11 + random.randint(0, 2)
                            y = y0 - BLOCK_SIZE // 2 + 5 + ((i // 3) % 3) * 11 + random.randint(0, 2)

                            self._world.add_item(physical, x, y)
                        else:
                            raise KeyError(f"Unknown drop category {drop_category}")
                self._world.remove_thing(mob)

    def get_holding(self):
        """(Tuple<str, str>) Return the current active item and effective item in hotbar. """
        active_stack = self._hot_bar.get_selected_value()
        active_item = active_stack.get_item() if active_stack else self._hands

        effective_item = active_item if active_item.can_attack() else self._hands

        return active_item, effective_item

    def check_target(self):
        """ Determine if cursor target in range. """
        # select target block, if possible
        active_item, effective_item = self.get_holding()

        pixel_range = active_item.get_attack_range() * self._world.get_cell_expanse()

        self._target_in_range = positions_in_range(self._player.get_position(),
                                                   self._target_position,
                                                   pixel_range)

    def _mouse_move(self, event):
        """ Event: Mouse movement
            Parameter:
                event(x, y): x and y coordinates of cursor position.
        """
        self._target_position = event.x, event.y
        self.check_target()

    def _left_click(self, event):
        """ Event: Left Click
            Parameter:
                event(x, y): x and y coordinates of left click.
        """
        # Invariant: (event.x, event.y) == self._target_position
        #  => Due to mouse move setting target position to cursor
        x, y = self._target_position
        print('left click')

        if self._target_in_range:
            block = self._world.get_block(x, y)
            mobs = self._world.get_mobs(x, y, 1)
            if block:
                self.mine_block(block, x, y)
            if mobs:
                for mob in mobs:
                    self.damage_mob(mob)

    def _trigger_crafting(self, craft_type):
        """ Trigger Crafting Window
            Parameter:
                craft_type(str): Crafting Window to Initialise"""
        print(f"Crafting with {craft_type}")
        if craft_type == 'basic':
            crafter = GridCrafter(CRAFTING_RECIPES_2x2)
        elif craft_type == 'crafting_table':
            crafter = GridCrafter(CRAFTING_RECIPES_3x3, 3, 3)
        elif craft_type == 'furnace':
            crafter = GridCrafter(FURNACE_RECIPES, 3, 1)
        self._crafting_window = CraftingWindow(self._master, 'Crafting Window', self._hot_bar, self._inventory, crafter)


    def run_effect(self, effect):
        """ Run an effect

            Parameters:
                effect(str): effect to be applied
        """
        if len(effect) == 2:
            if effect[0] == "crafting":
                craft_type = effect[1]

                if craft_type == "basic":
                    print("Can't craft much on a 2x2 grid :/")

                elif craft_type == "crafting_table":
                    print("Let's get our kraft® on! King of the brands")

                elif craft_type == "furnace":
                    print("Time for some cooking.")

                self._trigger_crafting(craft_type)
                return
            elif effect[0] in ("food", "health"):
                stat, strength = effect
                print(f"Gaining {strength} {stat}!")
                getattr(self._player, f"change_{stat}")(strength)
                return

        raise KeyError(f"No effect defined for {effect}")

    def _right_click(self, event):
        print("Right click")

        x, y = self._target_position
        target = self._world.get_thing(x, y)

        if target:
            # use this thing
            print(f'using {target}')
            effect = target.use()
            print(f'used {target} and got {effect}')

            if effect:
                self.run_effect(effect)

        else:
            # place active item
            selected = self._hot_bar.get_selected()

            if not selected:
                return

            stack = self._hot_bar[selected]
            drops = stack.get_item().place()

            stack.subtract(1)

            if stack.get_quantity() == 0:
                # remove from hotbar
                self._hot_bar[selected] = None

            if not drops:
                return

            # handling multiple drops would be somewhat finicky, so prevent it
            if len(drops) > 1:
                raise NotImplementedError("Cannot handle dropping more than 1 thing")

            drop_category, drop_types = drops[0]

            x, y = event.x, event.y

            if drop_category == "block":
                existing_block = self._world.get_block(x, y)

                if not existing_block:
                    self._world.add_block(create_block(drop_types[0]), x, y)
                else:
                    raise NotImplementedError(
                        "Automatically placing a block nearby if the target cell is full is not yet implemented")

            elif drop_category == "food":
                strength = stack.get_item().get_strength()
                # Update Player's Health
                if self._player.get_food() < self._player._max_food:
                    self._player.change_food(strength)
                elif self._player.get_health() < self._player._max_health:
                    self._player.change_health(strength)

            elif drop_category == "effect":
                self.run_effect(drop_types)

            else:
                raise KeyError(f"Unknown drop category {drop_category}")

    def close(self):
        """ Close the game """
        if tk.messagebox.askokcancel("Exit", "Are you sure you want to quit the game?"):
            self._master.destroy()

    def new_game(self):
        """ Launch a new game. """
        self._world = World((GRID_WIDTH, GRID_HEIGHT), BLOCK_SIZE)

        load_simple_world(self._world)

        self._player = Player()
        self._world.add_player(self._player, 250, 150)

        self._world.add_collision_handler("player", "item", on_begin=self._handle_player_collide_item)

        self._hot_bar = SelectableGrid(rows=1, columns=10)
        self._hot_bar.select((0, 0))

        starting_hotbar = [
            Stack(create_item("dirt"), 20),
            Stack(create_item("apple"), 4),
        ]

        for i, item in enumerate(starting_hotbar):
            self._hot_bar[0, i] = item

        self._hands = create_item('hands')

        starting_inventory = [
            ((1, 5), Stack(Item('dirt'), 10)),
            ((0, 2), Stack(Item('wood'), 10)),
        ]
        self._inventory = Grid(rows=3, columns=10)
        for position, stack in starting_inventory:
            self._inventory[position] = stack

        # Configure status view to 'new player'.
        if self._status_view:
            self._status_view._player = self._player
            self._status_view.update_food()
            self._status_view.update_health()

    def death(self):
        """ Event handler for player's death """
        if tk.messagebox.askokcancel("You have died!", "Would you like to start a new game?"):
            self.new_game()
        else:
            self._master.destroy()

    def _enter(self, event):
        """ Set the focus of the mouse when entering
            the application.
        """
        self._mouse_focus = True
        self.redraw()

    def _leave(self, event):
        """ Set the focus of the mouse when leaving
            the application.
        """
        self._mouse_focus = False
        self.redraw()

    def _activate_item(self, index):
        print(f"Activating {index}")

        self._hot_bar.toggle_selection((0, index))

    def _handle_player_collide_item(self, player: Player, dropped_item: DroppedItem, data,
                                    arbiter: pymunk.Arbiter):
        """Callback to handle collision between the player and a (dropped) item. If the player has sufficient space in
        their to pick up the item, the item will be removed from the game world.

        Parameters:
            player (Player): The player that was involved in the collision
            dropped_item (DroppedItem): The (dropped) item that the player collided with
            data (dict): data that was added with this collision handler (see data parameter in
                         World.add_collision_handler)
            arbiter (pymunk.Arbiter): Data about a collision
                                      (see http://www.pymunk.org/en/latest/pymunk.html#pymunk.Arbiter)
                                      NOTE: you probably won't need this
        Return:
             bool: False (always ignore this type of collision)
                   (more generally, collision callbacks return True iff the collision should be considered valid; i.e.
                   returning False makes the world ignore the collision)
        """

        item = dropped_item.get_item()

        if self._hot_bar.add_item(item):
            print(f"Added 1 {item!r} to the hotbar")
        elif self._inventory.add_item(item):
            print(f"Added 1 {item!r} to the inventory")
        else:
            print(f"Found 1 {item!r}, but both hotbar & inventory are full")
            return True

        self._world.remove_item(dropped_item)
        return False

