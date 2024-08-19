"""
Main.

Created by: Kaelan Moodley
Date: 28/05/2024

Enviromental Conservation Game.

You are an eco warrior fighting the various problems that the enviroment
faces. You have potions and weapons to aid in your battle.

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
            "damage potion": 1,
            "sword": 0,
            "excaliber": 0,
        }
        self.stats = {"battles_won": 0, "battles_lost": 0}

    def defend(self):
        """Simulate a player's defend action, which increases their health."""
        self.health = min(100, self.health + 8)
        print(f"{self.name} defends and regains 8 HP.")

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
                self.health = min(100, self.health + 15)
                print(f"{self.name} uses a health potion and regains 15 HP.")
            elif potion_type == "damage potion":
                damage = 25
                enemy.health -= damage
                print(
                    f"{self.name} uses a damage potion and deals"
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
            f"{self.name} earned {amount} dollars. "
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

            if item == "excaliber":
                self.attack_power += 10
                print(
                    f"{self.name} bought a {item}. "
                    "Attack power increased by 10. "
                    f"Remaining dollars: {self.dollars}"
                )
            else:
                print(
                    f"{self.name} bought a {item}."
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
        print("Inventory:")
        for item, quantity in self.inventory.items():
            print(f"  - {item}: {quantity}")
        print(f"Battles Won: {self.stats['battles_won']}")
        print(f"Battles Lost: {self.stats['battles_lost']}")


class Enemy(Hero):
    """Represents an enemy in the game."""

    def __init__(
        self, name: str, health: int, attack_power: int, reward: int, description: str
    ):
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
        description: str
            The description of the environmental issue the enemy represents.
        """
        super().__init__(name, health, attack_power)
        self.reward = reward
        self.description = description

    def show_description(self):
        """Displays the description of the enemy."""
        # Format the description with proper line breaks for readability
        formatted_description = self.description.replace(
            "/n", "\n"
        ).replace("  ", "")
        print(f"\n{self.name}: {formatted_description}\n")


def get_player_choice() -> str:
    """
    Get the player's choice of action.

    Returns
    -------
    str
        The player's chosen action.
    """
    while True:
        # Prompt the player to choose an action
        player_choice = input(
            "Choose your action (1. Attack, 2. Defend, 3. Use Health Potion,"
            + " 4. Use Damage Potion): "
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
    # Display the current health of both the player and the enemy
    print(
        f"{player.name}'s HP: {player.health} | "
        f"{enemy.name}'s HP: {enemy.health}"
    )
    # Get the player's action choice
    player_choice = get_player_choice()

    if player_choice == "1":
        # Player chooses to attack
        player_damage = player.attack()
        enemy.health -= player_damage
        print(
            f"{player.name} attacks {enemy.name}"
            f" and deals {player_damage} damage!"
        )
        if enemy.health <= 0:
            # Enemy is defeated
            print(
                f"{player.name} defeated {enemy.name} "
                f"and earned {enemy.reward} dollars!"
            )
            player.add_dollars(enemy.reward)
            player.stats["battles_won"] += 1
            return True

    elif player_choice == "2":
        # Player chooses to defend
        player.defend()

    elif player_choice == "3":
        # Player chooses to use a health potion
        player.use_potion("health potion", enemy)
        return True  # Skip enemy's turn

    elif player_choice == "4":
        # Player chooses to use a damage potion
        player.use_potion("damage potion", enemy)
        if enemy.health <= 0:
            # Enemy is defeated
            print(
                f"{player.name} defeated {enemy.name} "
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
    # Enemy attacks the player
    enemy_damage = enemy.attack()
    player.health -= enemy_damage
    print(
        f"{enemy.name} attacks {player.name} and deals {enemy_damage} damage!"
    )
    if player.health <= 0:
        # Player is defeated
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
    print(f"\nA wild {enemy.name} has appeared!")
    enemy.show_description()

    while True:
        if player_turn(player, enemy):
            return True
        if enemy_turn(player, enemy):
            return False


def main():
    """Run the main game loop."""
    player_name = input("Enter your hero's name: ")
    player = Player(player_name)

    # Define a list of enemies with environmental issues as descriptions
    enemies = [
        Enemy(
            "Pollution",
            50,
            10,
            10,
            "Pollution is contaminating the air, water, and land. It's"
            " a significant threat to ecosystems, wildlife, and human"
            " health. We must reduce waste, recycle, and limit emissions"
            " to fight pollution effectively.",
        ),
        Enemy(
            "Deforestation",
            60,
            12,
            12,
            "Deforestation is the clearing of forests on a massive scale,"
            " often resulting in damage to the quality of the land. It"
            " leads to habitat loss, decreased biodiversity, and"
            " contributes to climate change. Reforestation and"
            " sustainable land management are critical solutions.",
        ),
        Enemy(
            "Climate Change",
            80,
            15,
            15,
            "Climate change is causing more frequent and severe weather"
            " events, rising sea levels, and disruptions to natural"
            " ecosystems. It's driven by human activities, such as"
            " burning fossil fuels and deforestation. Urgent action"
            " is needed to reduce greenhouse gas emissions and"
            " transition to renewable energy sources.",
        ),
        Enemy(
            "Overfishing",
            50,
            10,
            10,
            "Overfishing is depleting fish populations at a rate faster"
            " than they can reproduce. This threatens marine ecosystems"
            " and food security. Sustainable fishing practices and"
            " marine conservation are essential to restore fish stocks.",
        ),
    ]

    # Run battles for each enemy
    for enemy in enemies:
        battle(player, enemy)
        if player.health <= 0:
            break

    print("\nGame over! Here are your final stats:")
    player.show_stats()


# Run the game
main()
