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
                print(f"{self.name} uses a damage potion and deals {damage} " +
                    f"damage to {enemy.name}!")
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
        print(f"{self.name} earned {amount} dollars." +
            f" Total dollars: {self.dollars}")

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

def player_turn(player: Player, enemy: Enemy) -> bool:
    """
    Handle the player's turn.

    Parameters
    ----------
    - player (Player): The player object.
    - enemy (Enemy): The enemy object.

    Returns
    -------
    - bool: True if the enemy is defeated, False otherwise.

    """

    print(
        f"{player.name}'s HP: {player.health} |" + 
        f" {enemy.name}'s HP: {enemy.health}"
    )
    player_choice = get_player_choice()
    if player_choice == "1":
        player_damage = player.attack()
        enemy.health -= player_damage
        print(
            f"{player.name} attacks {enemy.name} and" +
            " deals {player_damage} damage!"
        )
        if enemy.health <= 0:
            print(
                f"{player.name} defeated {enemy.name} " +
                f"and earned {enemy.reward} dollars!"
            )
            player.add_dollars(enemy.reward)
            player.stats["battles_won"] += 1
            return True
    elif player_choice == "2":
        player.defend()
    elif player_choice == "3":
        player.use_potion("health potion", enemy)
    elif player_choice == "4":
        player.use_potion("damage potion", enemy)
        if enemy.health <= 0:
            print(
                f"{player.name} defeated {enemy.name} " +
                f"and earned {enemy.reward} dollars!"
            )
            player.add_dollars(enemy.reward)
            player.stats["battles_won"] += 1
            return True
    return False

def enemy_turn(player: Player, enemy: Enemy) -> bool:
    """
    Handle the enemy's turn.

    Parameters
    ----------
    - player (Player): The player object.
    - enemy (Enemy): The enemy object.

    Returns
    -------
    - bool: True if the player is defeated, False otherwise.

    """
    enemy_damage = enemy.attack()
    player.health -= enemy_damage
    print(f"{enemy.name} attacks {player.name} and deals" +
        f" {enemy_damage} damage!")
    if player.health <= 0:
        print(f"{player.name} was defeated by {enemy.name}. Game over!")
        player.stats['battles_lost'] += 1
        return True
    return False

def battle(player: Player, enemy: Enemy) -> bool:
    """
    Simulate a battle between a player and an enemy.

    Parameters
    ----------
    - player (Player): The player object.
    - enemy (Enemy): The enemy object.

    Returns
    -------
    - bool: True if the player wins, False otherwise.
    
    """
    print(f"A wild {enemy.name} appears!")
    while player.is_alive() and enemy.is_alive():
        if player_turn(player, enemy):
            return True
        if enemy_turn(player, enemy):
            return False
    return player.is_alive()



def shop_categorized(player: Player):

    """
    Display the shop menu with categorized items. Allows player to purchase.

    Parameters
    ----------
    - player (Player): The player object.

    """
    print("Welcome to the shop! Here are the items you can buy:")
    items = {
        "Potions": [
            {"name": "health potion", 
            "cost": 20, "description":
            "Regains 25 HP"},
            {"name": "damage potion", 
            "cost": 30,
            "description": "Deals 20 damage to the enemy"}
        ],
        "Weapons": [
            {"name": "sword",
            "cost": 50, 
            "description": "Increases attack power by 5"},
            {"name": "super sword",
            "cost": 100,
            "description": "Increases attack power by 10"}
        ]
    }

    for category, category_items in items.items():
        print(f"\n{category}:")
        for idx, item in enumerate(category_items, start=1):
            print(f"  {idx}. {item['name'].capitalize()}: "+ 
                f" {item['cost']} dollars - {item['description']}")

    while True:
        category_choice = input("\nEnter the category (Potions/Weapons)"+
        " you want to buy from or type 'exit' to leave: ").strip().capitalize()
        if category_choice in items:
            item_choice = input("Enter the number of the item you want to"+
                    f" buy from {category_choice} or type 'back' to "+
                    " choose another category: ").strip()
            if item_choice.isdigit() and 1 <= int(item_choice) \
                <= len(items[category_choice]):
                selected_item = items[category_choice][int(item_choice) - 1]
                player.buy_item(selected_item["name"], selected_item["cost"])
            elif item_choice.lower() == "back":
                continue
            else:
                print("Invalid choice. Please try again.")
        elif category_choice == "Exit":
            break
        else:
            print("Invalid category. Please try again.")
            