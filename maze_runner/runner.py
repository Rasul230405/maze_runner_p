"""
    This module implements runner class and all the functions related to runner
    Magic constants:
    'N' - North
    'S' - South
    'W' - West
    'E' - East

    Last edited: 08/11/2024
    Author: Rasul Abbaszada
"""

import matplotlib.patches as patches
# I think the best data type for runner is to define its own data type. why not?
class Runner:
    def __init__(self, x: int = 0, y: int = 0, orientation: str = "N"):
        self._x = x
        self._y = y
        self._orientation = orientation

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation

    @x.setter
    def x(self, x):
        self._x = x
    @y.setter
    def y(self, y):
        self._y = y

    def turn(self, direction: str) -> None:
        if direction == "Right":
            if self._orientation == "N":
                self._orientation = "E"
            elif self._orientation == "W":
                self._orientation = "N"
            elif self._orientation == "S":
                self._orientation = "W"
            else:
                self._orientation = "S"

        else:
            if self._orientation == "N":
                self._orientation = "W"
            elif self._orientation == "W":
                self._orientation = "S"
            elif self._orientation == "S":
                self._orientation = "E"
            else:
                self._orientation = "N"

    def forward(self) -> None:
        '''Forward by 1 coordinate.'''
        if self._orientation == "N":
            self._y += 1
        elif self._orientation == "S":
            self._y -= 1
        elif self._orientation == "W":
            self._x -= 1
        else:
            self._x += 1

    def get_position(self) -> tuple[int, int]:
        return (self._x, self._y)

    def plot(self, ax, color: str = "green"):
        width = 1
        height = 1
        rect = patches.Rectangle((self._x, self._y), width, height, facecolor=color)
        ax.add_patch(rect)

def create_runner(x: int = 0, y: int = 0, orientation: str = "N") -> Runner:
    return Runner(x, y, orientation)

# it would be best to implement this function within class, but anyway
def get_x(runner: Runner) -> int:
    return runner.x

def get_y(runner: Runner) -> int:
    return runner.y

def get_orientation(runner) -> str:
    return runner.orientation

def turn(runner: Runner, direction: str) -> Runner:
    runner.turn(direction)
    return runner

def forward(runner):
    runner.forward()
    return runner



