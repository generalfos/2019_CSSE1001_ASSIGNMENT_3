""" Status View Class """

__author__ = "Joel Foster"
__date__ = "22/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk

class StatusView(tk.Frame):
    """ Display information to the user about their status in the game. """

    def __init__(self, master, Player):
        self._player = Player
        super().__init__(master)

        heart_img = tk.PhotoImage(file='Heart.gif')
        heart = tk.Label(self, image=heart_img)
        heart.image = heart_img
        heart.pack(side=tk.LEFT)

        self._health = tk.Label(self, text='Health: 20')
        self._health.pack(side=tk.LEFT)

        self._food = tk.Label(self, text='Food: 20')
        self._food.pack(side=tk.LEFT)

        food_img = tk.PhotoImage(file='Food.gif')
        food = tk.Label(self, image=food_img)
        food.image = food_img
        food.pack(side=tk.LEFT)

    def update_health(self):
        health = round((self._player.get_health()) * 2) / 2
        self._health.config(text='Health: {0}'.format(health))

    def update_food(self):
        food = round((self._player.get_food()) * 2) / 2
        self._food.config(text='Food: {0}'.format(food))

    def set_health(self, health):
        self._health = health

    def set_food(self, food):
        self._food = food
