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
        self.name = name  # Name of the hero
        self.health = health  # Health points of the hero
        self.attack_power = attack_power  # Attack power of the hero

    def attack(self) -> int:
        """
        Simulate a hero's attack.

        Returns
        -------
        int
            The damage dealt by the hero's attack.

        """
        return random.randint(self.attack_power // 2, self.attack_power)  
    # Random damage within attack power range

    def is_alive(self) -> bool:
        """
        Check if the hero is still alive.

        Returns
        -------
        bool
            True if the hero is alive, otherwise False.

        """
        return self.health > 0  # Hero is alive if health is greater than 0


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
        # Initialize with default health and attack power
        self.dollars = 0  # Player's money
        self.inventory = {
            "health potion": 2,  # Number of health potions
            "damage potion": 1,  # Number of damage potions
            "sword": 0,  # Number of swords
            "excaliber": 0,  # Number of excalibers
        }
        self.stats = {"battles_won": 0, "battles_lost": 0} 
        # Track battles won and lost

    def defend(self):
        """Simulate a player's defend action, which increases their health."""
        self.health = min(100, self.health + 8)  # Regain up to 100 HP
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
            # Check if potion is available
            self.inventory[potion_type] -= 1
            if potion_type == "health potion":
                self.health = min(100, self.health + 15)  # Regain up to 100 HP
                print(f"{self.name} uses a health potion and regains 15 HP.")
            elif potion_type == "damage potion":
                damage = 25
                enemy.health -= damage  # Inflict damage on the enemy
                print(
                    f"{self.name} uses a damage potion and deals" +
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
        self.dollars += amount  # Increase the player's money
        print(
            f"{self.name} earned {amount} dollars. " +
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
        if self.dollars >= cost:  # Check if the player has enough money
            self.dollars -= cost
            if item in self.inventory:
                self.inventory[item] += 1  # Add item to inventory
            else:
                self.inventory[item] = 1

            if item == "excaliber":
                self.attack_power += 10  # Increase attack power
                print(
                    f"{self.name} bought a {item}. " +
                    "Attack power increased by 10. " +
                    f"Remaining dollars: {self.dollars}"
                )
            else:
                print(
                    f"{self.name} bought a {item}." +
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

    def __init__(self, name: str, health: int, attack_power: int, reward: int,
                description: str):
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
        # Initialize with given parameters
        self.reward = reward  # Reward for defeating the enemy
        self.description = description  # Description of the enemy

    def show_description(self):
        """Displays the description of the enemy."""  # noqa: D401
        print(f"{self.name}: {self.description}")


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
            "Choose your action (1. Attack, 2. Defend, 3. Use Health Potion," +
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
        f"{player.name}'s HP: {player.health} | " +
        f"{enemy.name}'s HP: {enemy.health}"
    )
    player_choice = get_player_choice()
    if player_choice == "1":
        player_damage = player.attack()
        enemy.health -= player_damage  # Apply damage to the enemy
        print(
            f"{player.name} attacks {enemy.name}" +
            f" and deals {player_damage} damage!"
        )
        if enemy.health <= 0:
            print(
                f"{player.name} defeated {enemy.name} " +
                f"and earned {enemy.reward} dollars!"
            )
            player.add_dollars(enemy.reward)  # Add reward to player's dollars
            player.stats["battles_won"] += 1  # Increment battles won
            return True
    elif player_choice == "2":
        player.defend()  # Player defends and regains health
    elif player_choice == "3":
        player.use_potion("health potion", enemy)  # Use health potion
        return True  # Skip enemy's turn
    elif player_choice == "4":
        player.use_potion("damage potion", enemy)  # Use damage potion
        if enemy.health <= 0:
            print(
                f"{player.name} defeated {enemy.name} " +
                f"and earned {enemy.reward} dollars!"
            )
            player.add_dollars(enemy.reward)  # Add reward to player's dollars
            player.stats["battles_won"] += 1  # Increment battles won
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
    player.health -= enemy_damage  # Apply damage to the player
    print(
        f"{enemy.name} attacks {player.name} and deals {enemy_damage} damage!"
    )
    if player.health <= 0:
        print(f"{player.name} was defeated by {enemy.name}. Game over!")
        player.stats["battles_lost"] += 1  # Increment battles lost
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
    print(f"The terrible {enemy.name} appears!")
    enemy.show_description()  # Show the enemy's description
    while player.is_alive() and enemy.is_alive():
        if player_turn(player, enemy):
            return True
        if player_turn(player, enemy):
            continue  # Skip the enemy's turn if the player used a potion
        if enemy_turn(player, enemy):
            return False
    return player.is_alive()  # Player wins if still alive


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
                "description": "Regains 15 HP",
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
                "name": "excaliber",
                "cost": 100,
                "description": "Increases attack power by 10",
            },
        ],
    }

    for category, category_items in items.items():
        print(f"\n{category}:")
        for idx, item in enumerate(category_items, start=1):
            print(
                f"  {idx}. {item['name'].capitalize()}:" +
                f" {item['cost']} dollars - {item['description']}"
            )

    while True:
        category_choice = (
            input(
                "\nEnter the category (Potions/Weapons) you want to buy from "
                + "or type 'exit' to leave: "
            )
            .strip()
            .capitalize()
        )
        if category_choice in items:
            item_choice = input(
                "Enter the number of the item you want to buy from " +
                f" {category_choice} or type 'back' to choose another" +
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
    while True:
        player_name = input("Enter your name: ").strip()
        if player_name.isalpha():
            break
        print("Invalid name. Please enter a name with only " +
            " alphabetic characters.")

    player = Player(player_name)
    enemies_data = [
        ("Deforestation", 110, 12, 100, "The loss of trees and other " +
        " vegetation (Deforestation) can cause climate change, " +
        " desertification, soil erosion, fewer crops, flooding, increased " +
        " greenhouse gasses in the atmosphere, and a host of problems for " +
        " Indigenous people."),
        ("Pollution", 120, 14, 35, "Public health concerns related to high " +
        " air pollution exposures include cancer, cardiovascular disease, " +
        " respiratory diseases, diabetes mellitus, obesity, and " +
        " reproductive, neurological, and immune system disorders. " +
        " Research on air pollution and health effects continually advances."),
        ("Climate Change", 130, 15, 40, "Climate change impacts:/nRising " +
        " Temperatures: Increased heat, more illnesses, wildfires, and " +
        " rapid Arctic warming./nSevere Storms: Intense storms, extreme " +
        " rainfall, and flooding./nIncreased Drought: Worsened water " +
        " shortages, affecting food production./nWarming Oceans: Rising " +
        " sea levels and ocean acidity, harming marine life./nSpecies " +
        " Loss: Accelerated extinction, one million species at risk./nFood " +
        " Insecurity: Harm to fisheries, crops, and livestock, leading to " +
        " hunger./nHealth Risks: Pollution, disease, and malnutrition " +
        " causing millions of deaths./nPoverty and Displacement: " +
        " Increased poverty and displacement due to climate impacts."),
        ("Overfishing", 140, 20, 45, "Overfishing and destructive fishing " +
        " not only devastates fish populations and wildlife, breaks down " +
        " the food web and degrades habitats. It undermines the ocean's " +
        " ability to perform critical ecosystem services such as storing " +
        " carbon that is needed for climate mitigation."),
        ("Plastic Pollution", 150, 25, 75, "This pollution (plastic " +
        " pollution)chokes marine wildlife, damages soil and poisons " +
        " groundwater, and can cause serious health impacts. Is pollution " +
        " the only problem with plastic? No, it also contributes to the " +
        " climate crisis. The production of plastic is one of the most " +
        " energy-intensive manufacturing processes in the world."),
    ]

    enemies = [
        Enemy(name, health, attack_power, reward, description)
        for name, health, attack_power, reward, description in enemies_data
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
                    f"{i}. {enemy.name} (HP: {enemy.health}, " +
                    f"Attack: {enemy.attack_power}, Reward: " +
                    f" {enemy.reward} dollars)"
                )

            enemy_choice = input("Choose an enemy to fight: ").strip()
            try:
                enemy_choice = int(enemy_choice) - 1
                if 0 <= enemy_choice < len(enemies):
                    if not battle(player, enemies[enemy_choice]):
                        print("Game over!")
                        break
                    enemies.pop(enemy_choice)  # Remove defeated enemy
                else:
                    print("Invalid choice. Please choose a valid enemy.")

            except ValueError:
                print("Invalid choice, please enter a valid choice.")

        elif choice == "2":
            shop_categorized(player)  # Show shop menu
        elif choice == "3":
            player.show_stats()  # Show player stats
        elif choice == "4":
            print("Thank you for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":

    main()  # Start the game
