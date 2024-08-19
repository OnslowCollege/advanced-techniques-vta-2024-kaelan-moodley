import random

class Hero:
    """Represents a basic character in the game."""

    def __init__(self, name: str, health: int, attack_power: int):
        """Initialize a Hero object with name, health, and attack power."""
        self.name = name  # Name of the hero
        self.health = health  # Health points of the hero
        self.attack_power = attack_power  # Attack power of the hero

    def attack(self) -> int:
        """Simulate an attack and return the damage dealt."""
        return random.randint(self.attack_power // 2, self.attack_power)  # Damage is random between half and full attack power

    def is_alive(self) -> bool:
        """Check if the hero is still alive (health > 0)."""
        return self.health > 0

class Player(Hero):
    """Represents the player character, a subclass of Hero."""

    def __init__(self, name: str):
        """Initialize a Player with specific health, attack power, inventory, and stats."""
        super().__init__(name, health=100, attack_power=20)  # Initialize with default health and attack power
        self.dollars = 0  # Initialize player's currency
        self.inventory = {  # Initialize player's inventory with items
            "health potion": 2,
            "damage potion": 1,
            "sword": 0,
            "excaliber": 0,
        }
        self.stats = {"battles_won": 0, "battles_lost": 0}  # Initialize player's battle stats

    def defend(self):
        """Player defends to regain health."""
        self.health = min(100, self.health + 8)  # Increase health by 8, but not above 100
        print(f"{self.name} defends and regains 8 HP.")

    def use_potion(self, potion_type: str, enemy: "Enemy"):
        """Use a potion from the inventory."""
        if self.inventory.get(potion_type, 0) > 0:  # Check if the potion is available
            self.inventory[potion_type] -= 1  # Decrease potion count
            if potion_type == "health potion":
                self.health = min(100, self.health + 15)  # Heal the player by 15 HP
                print(f"{self.name} uses a health potion and regains 15 HP.")
            elif potion_type == "damage potion":
                damage = 25  # Fixed damage value for damage potion
                enemy.health -= damage  # Decrease enemy's health
                print(f"{self.name} uses a damage potion and deals {damage} damage to {enemy.name}!")
        else:
            print(f"{self.name} has no {potion_type} left!")  # Inform the player if the potion is not available

    def add_dollars(self, amount: int):
        """Add a specified amount of dollars to the player's total."""
        self.dollars += amount  # Increase the player's money
        print(f"{self.name} earned {amount} dollars. Total dollars: {self.dollars}")

    def buy_item(self, item: str, cost: int):
        """Buy an item from the shop and add it to the inventory."""
        if self.dollars >= cost:  # Check if the player has enough dollars
            self.dollars -= cost  # Deduct the cost
            if item in self.inventory:
                self.inventory[item] += 1  # Add to existing item in inventory
            else:
                self.inventory[item] = 1  # Add new item to inventory
            if item == "excaliber":
                self.attack_power += 10  # Increase attack power if Excaliber is bought
                print(f"{self.name} bought a {item}. Attack power increased by 10. Remaining dollars: {self.dollars}")
            else:
                print(f"{self.name} bought a {item}. Remaining dollars: {self.dollars}")
        else:
            print(f"{self.name} does not have enough dollars to buy {item}.")  # Inform player of insufficient funds

    def show_stats(self):
        """Display the player's stats and inventory."""
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
    """Represents an enemy character, a subclass of Hero."""

    def __init__(self, name: str, health: int, attack_power: int, reward: int, description: str):
        """Initialize an Enemy with specific health, attack power, reward, and description."""
        super().__init__(name, health, attack_power)  # Initialize with given health and attack power
        self.reward = reward  # Dollars rewarded to player upon defeating this enemy
        self.description = description  # Description of the enemy

    def show_description(self):
        """Display the enemy's description."""
        print(f"{self.name}: {self.description}")

def get_player_choice() -> str:
    """Get and return the player's choice of action."""
    while True:  # Loop until a valid choice is made
        player_choice = input("Choose your action (1. Attack, 2. Defend, 3. Use Health Potion, 4. Use Damage Potion): ").strip()
        if player_choice in ["1", "2", "3", "4"]:
            return player_choice  # Return the valid choice
        print("Invalid choice! Please enter 1, 2, 3, or 4.")  # Prompt again if choice is invalid

def player_turn(player: Player, enemy: Enemy) -> bool:
    """Handle the player's turn and return True if the enemy is defeated."""
    print(f"{player.name}'s HP: {player.health} | {enemy.name}'s HP: {enemy.health}")  # Display health of both player and enemy
    player_choice = get_player_choice()  # Get the player's action choice
    if player_choice == "1":  # Attack
        player_damage = player.attack()  # Calculate damage
        enemy.health -= player_damage  # Decrease enemy's health
        print(f"{player.name} attacks {enemy.name} and deals {player_damage} damage!")
        if enemy.health <= 0:  # Check if enemy is defeated
            print(f"{player.name} defeated {enemy.name} and earned {enemy.reward} dollars!")
            player.add_dollars(enemy.reward)  # Reward player
            player.stats["battles_won"] += 1  # Increase win count
            return True
    elif player_choice == "2":  # Defend
        player.defend()
    elif player_choice == "3":  # Use Health Potion
        player.use_potion("health potion", enemy)
        return True  # Skip enemy's turn
    elif player_choice == "4":  # Use Damage Potion
        player.use_potion("damage potion", enemy)
        if enemy.health <= 0:  # Check if enemy is defeated by potion
            print(f"{player.name} defeated {enemy.name} and earned {enemy.reward} dollars!")
            player.add_dollars(enemy.reward)  # Reward player
            player.stats["battles_won"] += 1  # Increase win count
            return True

    return False  # Continue battle if enemy is still alive

def enemy_turn(player: Player, enemy: Enemy):
    """Handle the enemy's turn."""
    if enemy.is_alive():  # Check if enemy is still alive
        enemy_damage = enemy.attack()  # Calculate damage
        player.health -= enemy_damage  # Decrease player's health
        print(f"{enemy.name} attacks {player.name} and deals {enemy_damage} damage!")
        if player.health <= 0:  # Check if player is defeated
            print(f"{player.name} was defeated by {enemy.name}.")
            player.stats["battles_lost"] += 1  # Increase loss count

def battle(player: Player, enemy: Enemy):
    """Simulate a battle between the player and an enemy."""
    print(f"\nA wild {enemy.name} appears!\n")  # Announce enemy appearance
    enemy.show_description()  # Show enemy's description

    while player.is_alive() and enemy.is_alive():  # Continue battle while both are alive
        if player_turn(player, enemy):  # Player's turn, check if enemy is defeated
            break
        enemy_turn(player, enemy)  # Enemy's turn if still alive

    if not player.is_alive():  # Check if player is defeated
        print(f"{player.name} has been defeated in battle.")
    else:
        print(f"{player.name} emerges victorious!")

def game():
    """Main function to run the game."""
    print("Welcome to the Environmental Hero Game!")
    player_name = input("Enter your hero's name: ").strip()  # Get player's name
    player = Player(player_name)  # Create player object

    # List of enemies to battle
    enemies = [
        Enemy(
            name="Smog Monster",
            health=40,
            attack_power=12,
            reward=10,
            description="A vile creature born from pollution in the air."
        ),
        Enemy(
            name="Deforestation Giant",
            health=60,
            attack_power=15,
            reward=20,
            description="A giant that destroys forests and wildlife habitats."
        ),
        Enemy(
            name="Oil Spill Serpent",
            health=70,
            attack_power=18,
            reward=30,
            description="A slithering serpent leaving toxic oil spills in its wake."
        ),
        Enemy(
            name="Plastic Kraken",
            health=90,
            attack_power=20,
            reward=40,
            description="A massive sea creature composed entirely of discarded plastics."
        ),
    ]

    for enemy in enemies:  # Loop through each enemy
        battle(player, enemy)  # Start battle
        if not player.is_alive():  # Check if player is defeated
            print("Game Over.")
            break

    if player.is_alive():  # If player is still alive after all battles
        print("Congratulations! You've defeated all the environmental threats!")
        player.show_stats()  # Show final stats

if __name__ == "__main__":
    game()
