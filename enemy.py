from constants import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED
        #attributes
        #randomly select type
        #based on type, modify attributes