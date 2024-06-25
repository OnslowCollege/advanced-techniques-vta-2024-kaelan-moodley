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
    """E."""

    def __init__(self, name: str, health: int, attack_power: int):
        """
        Initialize a Character object.

        Parameters
        ----------
        - name: The name of the character.
        - health: The health points of the character.
        - attack_power: The attack power of the character.
        
        """
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self)-> int:
        """
        Simulate a character's attack.
        
        Returns
        -------
        The damage delt by the charcters attack.

        """
        return random.randint(self.attack_power // 2, self.attack_power)
    
    def is_alive(self) -> bool:
        """
        Check if the charcter is still alive.
        
        Returns
        -------
        True if the charcter is alive, otherwise will return False.

        """
        return self.health > 0
    
class Player(Hero): 
    """E."""

    def __init__(self, name: str):
        """
        Initialize a player object.

        Parameters
        ----------
        - name: The name of the player.

        """
        super().__init__(name, health=100, attack_power=20)
        self.dollars = 0
        self.inventory = {
            "health potion": 2, "damage potion": 0, "super sword": 0
            }

    def defend(self):
        """Simulate a player's defend action, which increases their health."""
        self.health = min(100, self.health + 15)
        print(f"{self.name} defends and regains 15 HP.")

    def use_potion(self, potion_type: str, enemy: 'Enemy'):
        """
        Use a potion from the player's inventory.

        Parameters
        ----------
        - potion_type: The type of potion to use.
        - enemy: The enemy to affect if using a damage potion.

        """
        if self.inventory.get(potion_type, 0) > 0:
            self.inventory[potion_type] -= 1
            if potion_type == "health potion":
                self.health = min(100, self.health + 25)
                print(f"{self.name} uses a basic potion and regains 25 HP.")
            elif potion_type == "damage potion":
                damage = 20
                enemy.health -= damage
                print(f"{self.name} uses a damage potion and deals {damage} damage to {enemy.name}!")
        else:
            print(f"{self.name} has no {potion_type} left!")   

    def add_dollars(self, amount: int):
        """
        Add money to the player's total.

        Parameters
        ----------
        - amount: The amount of money to add.

        """      
        self.dollars += amount
        print(f"{self.name} earned {amount} dollars. Total dollars: {self.dollars}")

    def show_stats(self):
        """Display the player's stats."""
        
        print(f"\n{self.name}'s Stats:")
        print(f"Health: {self.health}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Dollars: {self.dollars}")
        print(f"Inventory: {self.inventory}")
        print(f"Battles Won: {self.stats['battles_won']}")
        print(f"Battles Lost: {self.stats['battles_lost']}")


class Enemy(Hero): 
    """E."""

    def _init_(self, name: str, health: int, attack_power: int, reward: int):
        """
        Initialize an Enemy object.

        Parameters
        ----------
        - name: The name of the enemy.
        - health: The health points of the enemy.
        - attack_power: The attack power of the enemy.
        - reward: The currency reward for defeating the enemy.

        """
        super().__init__(name, health, attack_power)
        self.reward = reward

def get_player_choice() -> str:
    """
    Get the player's choice of action.

    Returns
    -------
    - str: The player's chosen action.

    """
    while True:
        player_choice = input("Choose your action (1. Attack, 2. Defend, 3." +
                        "Use Health Potion, 4. Use Damage Potion): ").strip()
        if player_choice in ["1", "2", "3", "4"]:
            return player_choice
        print("Invalid choice! Please enter 1, 2, 3, or 4.")

        

def shop(player: Player):
    """
    Display the shop menu and allow the player to buy items.

    Parameters
    ----------
    - player (Player): The player object.

    """
    print("Welcome to the shop! Here are the items you can buy:")
    items = {
        "health potion": 20,
        "damage potion": 30,
        "sword": 50,
        "super sword": 100
    }

    for item, cost in items.items():
        print(f"{item.capitalize()}: {cost} dollars")

    choice = input("Enter the name of the item you want to buy or type 'exit' to leave: ").strip().lower()
    if choice in items:
        player.buy_item(choice, items[choice])
    elif choice == "exit":
        return
    else:
        print("Invalid choice. Please try again.")