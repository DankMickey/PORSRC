from heuristic import *
from diagonal_movement import *
from grid import *
from node import *
from util import *


BORDERLESS_GRID = """
xxx
xxx
"""
BORDER_GRID = """
+---+
|   |
|   |
+---+
"""
WALKED_GRID = """
+---+
|s# |
|xe |
+---+
"""


def t_str():
    """
    test printing the grid
    """
    grid = Grid(height=2, width=3)
    assert grid.grid_str(border=False, empty_chr='x') == BORDERLESS_GRID[1:-1]
    assert grid.grid_str(border=True) == BORDER_GRID[1:-1]
    grid.nodes[0][1].walkable = False
    start = grid.nodes[0][0]
    end = grid.nodes[1][1]
    path = [(0, 1)]
    assert grid.grid_str(path, start, end) == WALKED_GRID[1:-1]

class NAI:

    def __init__(self, tagto):
        self.AIworld = AIWorld(tagto)
        self._characters = {}
        self.name = ''

    def getworld(self):
        """
        :return: the Artificial Intelligence world
        """
        return self.AIworld
        
    def getname(self):
        return self.name

    def getcharactercount(self):
        """
        :return: number of intelligent characters in the world
        """
        return len(self._characters)

    def getcharacters(self):
        """
        :return: dictionary of the characters
        """
        return self._characters

    def isinworld(self, name):
        return name in self._characters

    def addcharacter(self, name, nodepath, mass, movt_force, max_force):
        """
        Add a character to the AI
        :param name: variable name in strings
        :param nodepath: Actor object
        :param mass: Mass
        :param movt_force: Movement Force
        :param max_force: Maximum Force
        :return:
        """
        self.name = str(name)
        #self.nodepath = nodepath
        self.AIchar = AICharacter(self.name, nodepath, mass, movt_force, max_force)

        self.AIworld.addAiChar(self.AIchar)
        self._characters[name] = self.AIchar

    def follow(self, name, target):
        """
        Follow the target
        :param name: the pursuer
        :param target: duh, the target
        :return:
        """
        if not self.isinworld(name):
            print("Character is not in the world, yet")
            return
            
        self._characters[name].getAiBehaviors().pursue(target)
        #self.nodepath.loop('walk')
        
    def evade(self, name, target):
        """
        Evade the target
        :param name: the pursuer
        :param target: duh, the target
        :return:
        """
        if not self.isinworld(name):
            print("Character is not in the world, yet")
            return

        self._characters[name].getAiBehaviors().evade(target)
        
    def removeFollow(self, name, target):
        """
        Remove the target
        :param name: the pursuer
        :param target: duh, the target
        :return:
        """
        self._characters[name].getAiBehaviors().removeAi('pursue')
        #self.nodepath.loop('idle')
        
        

    def patrol(self, name):
        if not self.isinworld(name):
            print("Character is not in the world, yet")
            return

        self._characters[name].getAiBehaviors().wander(5, 0, 10, 1.0)
