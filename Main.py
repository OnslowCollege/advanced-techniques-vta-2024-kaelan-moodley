"""
Main.

Created by: Kaelan Moodley
Date: 28/05/2024

Enviromental Conservation Game.

"""

# Enter your code here

import random
from typing import List, Tuple

class Hero:
    def __init__(self, name: str, health: int, attack_power: int):
        """
        Initialize a Character object.

        Parameters:
        - The name of the character.
        - The health points of the character.
        - The attack power of the character.
        """
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self)-> int:
        """
        Simulate a character's attack.
        
        Returns:
        The damage delt by the charcters attack.
        """
        return random.randint(self.attack_power // 2, self.attack_power)
    
    def is_alive(self) -> bool:
        """
        Checks if the charcter is still alive.
        
        Returns:
        True if the charcter is alive, otherwise will return False.
        """
        return self.health > 0
    
class Player(Hero): 
    def __init__(self, name: str):
        """'
        
        """

class Enemy(Hero):
    def _init_(self, name: str, health: int, attack_power: int, reward: int):
        """
        Initialize an Enemy object.

        Parameters: 

        -The name of the enemy.
        -The health points of the enemy.
        -The attack power of the enemy.
        -The currency reward for defeating the enemy.

        """
        super().__init__(name, health, attack_power)
        self.reward = reward
        
    def main():
        """ The main function to run the game. """
