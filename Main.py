"""
Main.

Created by: Kaelan Moodley
Date: 28/05/2024

Enviromental Conservation Game.

"""

# Enter your code here

import random


class Hero:
    """Represents a basic character in the game."""

    def __init__(self, name: str, health: int, attack_power: int):
        """
        Initialize a Hero object.

        Parameters
        ----------
        name: str
            The name of the hero.
        health: int
            The health points of the hero.
        attack_power: int
            The attack power of the hero.

        """

        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self) -> int:
        """
        Simulate a hero's attack.

        Returns
        -------
        int
            The damage dealt by the hero's attack.

        """

        return random.randint(self.attack_power // 2, self.attack_power)

    def is_alive(self) -> bool:
        """
        Check if the hero is still alive.

        Returns
        -------
        bool
            True if the hero is alive, otherwise False.

        """

        return self.health > 0


class Player(Hero):
    """Represents the player in the game."""

    def __init__(self, name: str):
        """
        Initialize a Player object.

        Parameters
        ----------
        name: str
            The name of the player.

        """

        super().__init__(name, health=100, attack_power=20)
        self.dollars = 0
        self.inventory = {
            "health potion": 2,
            "damage potion": 0,
            "super sword": 0,
        }
        self.stats = {"battles_won": 0, "battles_lost": 0}

    def defend(self):
        """Simulate a player's defend action, which increases their health."""
        self.health = min(100, self.health + 15)
        print(f"{self.name} defends and regains 15 HP.")

    def use_potion(self, potion_type: str, enemy: "Enemy"):
        """
        Use a potion from the player's inventory.

        Parameters
        ----------
        potion_type: str
            The type of potion to use.
        enemy: Enemy
            The enemy to affect if using a damage potion.

        """

        if self.inventory.get(potion_type, 0) > 0:
            self.inventory[potion_type] -= 1
            if potion_type == "health potion":
                self.health = min(100, self.health + 25)
                print(f"{self.name} uses a health potion and regains 25 HP.")
            elif potion_type == "damage potion":
                damage = 20
                enemy.health -= damage
                print(
                    f"{self.name} uses a damage potion and deals"+
                    f" {damage} damage to {enemy.name}!"
                )
        else:
            print(f"{self.name} has no {potion_type} left!")

    def add_dollars(self, amount: int):
        """
        Add money to the player's total.

        Parameters
        ----------
        amount: int
            The amount of money to add.

        """

        self.dollars += amount
        print(
            f"{self.name} earned {amount} dollars. "+
            f"Total dollars: {self.dollars}"
        )

    def buy_item(self, item: str, cost: int):
        """
        Buy an item from the shop and add it to the player's inventory.

        Parameters
        ----------
        item: str
            The item to buy.
        cost: int
            The cost of the item.

        """

        if self.dollars >= cost:
            self.dollars -= cost
            if item in self.inventory:
                self.inventory[item] += 1
            else:
                self.inventory[item] = 1

            if item == "super sword":
                self.attack_power += 10
                print(
                    f"{self.name} bought a {item}. "+
                    "Attack power increased by 10. "+
                    f"Remaining dollars: {self.dollars}"
                )
            else:
                print(
                    f"{self.name} bought a {item}."+
                    f" Remaining dollars: {self.dollars}"
                )
        else:
            print(f"{self.name} does not have enough dollars to buy {item}.")

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
    """Represents an enemy in the game."""

    def __init__(self, name: str, health: int, attack_power: int, reward: int):
        """
        Initialize an Enemy object.

        Parameters
        ----------
        name: str
            The name of the enemy.
        health: int
            The health points of the enemy.
        attack_power: int
            The attack power of the enemy.
        reward: int
            The currency reward for defeating the enemy.

        """

        super().__init__(name, health, attack_power)
        self.reward = reward


def get_player_choice() -> str:
    """
    Get the player's choice of action.

    Returns
    -------
    str
        The player's chosen action.

    """

    while True:
        player_choice = input(
            "Choose your action (1. Attack, 2. Defend, 3. Use Health Potion,"+
            " 4. Use Damage Potion): "
        ).strip()
        if player_choice in ["1", "2", "3", "4"]:
            return player_choice
        print("Invalid choice! Please enter 1, 2, 3, or 4.")


def player_turn(player: Player, enemy: Enemy) -> bool:
    """
    Handle the player's turn.

    Parameters
    ----------
    player: Player
        The player object.
    enemy: Enemy
        The enemy object.

    Returns
    -------
    bool
        True if the enemy is defeated, False otherwise.

    """

    print(
        f"{player.name}'s HP: {player.health} | "+
        f"{enemy.name}'s HP: {enemy.health}"
    )
    player_choice = get_player_choice()
    if player_choice == "1":
        player_damage = player.attack()
        enemy.health -= player_damage
        print(
            f"{player.name} attacks {enemy.name}"+
            f" and deals {player_damage} damage!"
        )
        if enemy.health <= 0:
            print(
                f"{player.name} defeated {enemy.name} "+
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
                f"{player.name} defeated {enemy.name} "+
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
    player: Player
        The player object.
    enemy: Enemy
        The enemy object.

    Returns
    -------
    bool
        True if the player is defeated, False otherwise.

    """

    enemy_damage = enemy.attack()
    player.health -= enemy_damage
    print(
        f"{enemy.name} attacks {player.name} and deals {enemy_damage} damage!"
    )
    if player.health <= 0:
        print(f"{player.name} was defeated by {enemy.name}. Game over!")
        player.stats["battles_lost"] += 1
        return True
    return False


def battle(player: Player, enemy: Enemy) -> bool:
    """
    Simulate a battle between a player and an enemy.

    Parameters
    ----------
    player: Player
        The player object.
    enemy: Enemy
        The enemy object.

    Returns
    -------
    bool
        True if the player wins, False otherwise.

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
    player: Player
        The player object.

    """

    print("Welcome to the shop! Here are the items you can buy:")
    items = {
        "Potions": [
            {
                "name": "health potion",
                "cost": 20,
                "description": "Regains 25 HP",
            },
            {
                "name": "damage potion",
                "cost": 30,
                "description": "Deals 20 damage to the enemy",
            },
        ],
        "Weapons": [
            {
                "name": "sword",
                "cost": 50,
                "description": "Increases attack power by 5",
            },
            {
                "name": "super sword",
                "cost": 100,
                "description": "Increases attack power by 10",
            },
        ],
    }

    for category, category_items in items.items():
        print(f"\n{category}:")
        for idx, item in enumerate(category_items, start=1):
            print(
                f"  {idx}. {item['name'].capitalize()}:"+
                f" {item['cost']} dollars - {item['description']}"
            )

    while True:
        category_choice = (
            input(
                "\nEnter the category (Potions/Weapons) you want to buy from "+
                "or type 'exit' to leave: "
            )
            .strip()
            .capitalize()
        )
        if category_choice in items:
            item_choice = input(
                "Enter the number of the item you want to buy from "+
                f" {category_choice} or type 'back' to choose another"+
                " category: "
            ).strip()
            if item_choice.isdigit() and 1 <= int(item_choice) <= len(
                items[category_choice]
            ):
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


def main():
    """Run the game."""
    player_name = input("Enter your name: ").strip()
    player = Player(player_name)

    enemies_data = [
        ("Deforestation", 80, 12, 20),
        ("Pollution", 70, 14, 25),
        ("Climate Change", 90, 11, 30),
        ("Overfishing", 75, 13, 20),
        ("Plastic Pollution", 85, 14, 25),
    ]

    enemies = [
        Enemy(name, health, attack_power, reward)
        for name, health, attack_power, reward in enemies_data
    ]

    print("Welcome, eco-warrior! Your mission is to protect the environment.")
    print("You will face various adversaries harming the planet. Let's begin!")

    while player.is_alive():
        print("\nMenu:")
        print("1. Fight an enemy")
        print("2. Visit the shop")
        print("3. View stats")
        print("4. Exit game")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            for i, enemy in enumerate(enemies, start=1):
                print(
                    f"{i}. {enemy.name} (HP: {enemy.health}, Attack: {enemy.attack_power}, Reward: {enemy.reward} dollars)"
                )

            enemy_choice = int(input("Choose an enemy to fight: ").strip()) - 1
            if 0 <= enemy_choice < len(enemies):
                if not battle(player, enemies[enemy_choice]):
                    print("Game over!")
                    break
                enemies.pop(enemy_choice)
            else:
                print("Invalid choice. Please choose a valid enemy.")
        elif choice == "2":
            shop_categorized(player)
        elif choice == "3":
            player.show_stats()
        elif choice == "4":
            print("Thank you for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()

