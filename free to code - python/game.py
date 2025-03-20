import random
import time
import os
import sys
from typing import Dict, List, Tuple, Optional

class Entity:
    def __init__(self, name: str, health: int, damage: int):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
    
    def is_alive(self) -> bool:
        return self.health > 0

    def attack(self, target) -> str:
        damage = random.randint(self.damage - 2, self.damage + 2)
        if damage < 0:
            damage = 0
        target.health -= damage
        if target.health < 0:
            target.health = 0
        return f"{self.name} attacks {target.name} for {damage} damage!"

    def heal(self, amount: int) -> str:
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_heal = self.health - before
        return f"{self.name} heals for {actual_heal} health points!"


class Player(Entity):
    def __init__(self, name: str):
        super().__init__(name, health=30, damage=5)
        self.inventory = []
        self.position = (0, 0)  # Starting position
        self.gold = 0
        self.level = 1
        self.experience = 0
        self.exp_to_level = 20
    
    def add_item(self, item: str) -> str:
        self.inventory.append(item)
        return f"Added {item} to your inventory!"
    
    def use_item(self, item: str) -> Optional[str]:
        if item in self.inventory:
            self.inventory.remove(item)
            if item == "Health Potion":
                return self.heal(10)
            elif item == "Strength Potion":
                self.damage += 2
                return f"Your damage increased by 2! New damage: {self.damage}"
            elif item == "Magic Map":
                return "You can now see all rooms!"
        return None
    
    def gain_experience(self, amount: int) -> Optional[str]:
        self.experience += amount
        if self.experience >= self.exp_to_level:
            self.level_up()
            return f"You leveled up! You are now level {self.level}!"
        return None
    
    def level_up(self):
        self.level += 1
        self.max_health += 5
        self.health = self.max_health
        self.damage += 2
        self.experience -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)


class Monster(Entity):
    def __init__(self, level: int):
        monster_types = [
            ("Goblin", 10, 3),
            ("Skeleton", 15, 4),
            ("Orc", 20, 5),
            ("Troll", 25, 6),
            ("Dragon", 40, 8)
        ]
        
        # Choose monster based on level
        index = min(level // 2, len(monster_types) - 1)
        name, health, damage = monster_types[index]
        
        # Scale with level
        health += level * 2
        damage += level // 2
        
        super().__init__(name, health, damage)
        self.gold_value = random.randint(5, 10) * level


class Room:
    def __init__(self, description: str, position: Tuple[int, int]):
        self.description = description
        self.position = position
        self.items = []
        self.monster = None
        self.visited = False
        self.exits = {"north": False, "east": False, "south": False, "west": False}
    
    def add_item(self, item: str):
        self.items.append(item)
    
    def add_monster(self, monster: Monster):
        self.monster = monster
    
    def set_exits(self, north: bool, east: bool, south: bool, west: bool):
        self.exits = {"north": north, "east": east, "south": south, "west": west}
    
    def get_exits_description(self) -> str:
        available_exits = [direction for direction, available in self.exits.items() if available]
        if not available_exits:
            return "There are no exits!"
        
        return "Exits: " + ", ".join(available_exits)
    
    def describe(self) -> str:
        result = [f"\n{self.description}"]
        
        if self.monster and self.monster.is_alive():
            result.append(f"A {self.monster.name} is here! (Health: {self.monster.health}/{self.monster.max_health})")
        
        if self.items:
            result.append(f"You see: {', '.join(self.items)}")
        
        result.append(self.get_exits_description())
        return "\n".join(result)


class Game:
    def __init__(self):
        self.player = None
        self.dungeon = {}
        self.game_over = False
        self.has_won = False
        self.turn_count = 0
        self.magic_map = False
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        # Using ASCII characters instead of Unicode box-drawing characters
        banner = """
        +-------------------------------------------+
        |                                           |
        |   PYTHON DUNGEON ADVENTURE                |
        |                                           |
        +-------------------------------------------+
        """
        print(banner)
    
    def display_stats(self):
        stats = f"""
        {self.player.name} | Level: {self.player.level} | XP: {self.player.experience}/{self.player.exp_to_level}
        Health: {self.player.health}/{self.player.max_health} | Damage: {self.player.damage} | Gold: {self.player.gold}
        Position: {self.player.position} | Turns: {self.turn_count}
        Inventory: {', '.join(self.player.inventory) if self.player.inventory else 'Empty'}
        """
        print(stats)
    
    def start_game(self):
        self.clear_screen()
        self.display_banner()
        
        name = input("Enter your character's name: ")
        self.player = Player(name)
        
        self.generate_dungeon()
        
        self.play_game()
    
    def generate_dungeon(self):
        # Define room descriptions
        room_descriptions = [
            "A dimly lit chamber with cobwebs in the corners.",
            "A musty room with crumbling stone walls.",
            "A small cave with strange symbols etched into the floor.",
            "An ancient library with dusty, empty shelves.",
            "A damp corridor with water dripping from the ceiling.",
            "A former guard room with broken weapons scattered about.",
            "An eerie chamber with flickering magical lights.",
            "A room filled with strange alchemical equipment.",
            "A grand hall with tattered banners hanging from the walls.",
            "A small shrine to a forgotten deity."
        ]
        
        # Create a 3x3 dungeon
        for x in range(3):
            for y in range(3):
                description = random.choice(room_descriptions)
                room_descriptions.remove(description)  # Ensure unique descriptions
                
                room = Room(description, (x, y))
                
                # Set exits
                north = y > 0
                east = x < 2
                south = y < 2
                west = x > 0
                room.set_exits(north, east, south, west)
                
                # Add items randomly
                if random.random() < 0.3:
                    items = ["Health Potion", "Strength Potion", "Gold Coin", "Magic Map"]
                    room.add_item(random.choice(items))
                
                # Add monsters randomly, but not in the starting room
                if (x, y) != (0, 0) and random.random() < 0.7:
                    level = max(1, x + y)
                    room.add_monster(Monster(level))
                
                self.dungeon[(x, y)] = room
        
        # Place the victory item in the furthest room
        self.dungeon[(2, 2)].add_item("Ancient Artifact")
        self.dungeon[(2, 2)].add_monster(Monster(5))  # Boss monster
    
    def get_current_room(self) -> Room:
        return self.dungeon[self.player.position]
    
    def display_map(self):
        print("\nDungeon Map:")
        print("  +---+---+---+")
        for y in range(3):
            row = "  "
            for x in range(3):
                if (x, y) == self.player.position:
                    row += "| P "
                elif self.dungeon[(x, y)].visited or self.magic_map:
                    if self.dungeon[(x, y)].monster and self.dungeon[(x, y)].monster.is_alive():
                        row += "| M "
                    elif self.dungeon[(x, y)].items:
                        row += "| i "
                    else:
                        row += "|   "
                else:
                    row += "| ? "
            row += "|"
            print(row)
            print("  +---+---+---+")
        print("P = Player, M = Monster, i = Item, ? = Unexplored")
    
    def move_player(self, direction: str) -> str:
        current_room = self.get_current_room()
        
        if not current_room.exits[direction]:
            return "You can't go that way!"
        
        x, y = self.player.position
        if direction == "north":
            y -= 1
        elif direction == "east":
            x += 1
        elif direction == "south":
            y += 1
        elif direction == "west":
            x -= 1
        
        self.player.position = (x, y)
        new_room = self.get_current_room()
        new_room.visited = True
        
        return f"You move {direction}." + new_room.describe()
    
    def handle_combat(self) -> str:
        current_room = self.get_current_room()
        monster = current_room.monster
        
        if not monster or not monster.is_alive():
            return "There's no monster here to fight."
        
        result = []
        
        # Player attacks first
        result.append(self.player.attack(monster))
        
        # Check if monster is defeated
        if not monster.is_alive():
            gold_gained = monster.gold_value
            self.player.gold += gold_gained
            exp_gained = monster.gold_value * 2
            level_up_message = self.player.gain_experience(exp_gained)
            
            result.append(f"You defeated the {monster.name}!")
            result.append(f"You gained {gold_gained} gold and {exp_gained} experience!")
            
            if level_up_message:
                result.append(level_up_message)
            
            return "\n".join(result)
        
        # Monster counterattacks
        result.append(monster.attack(self.player))
        
        # Check if player is defeated
        if not self.player.is_alive():
            self.game_over = True
            result.append(f"You have been defeated by the {monster.name}!")
        
        return "\n".join(result)
    
    def handle_take(self, item_name: str) -> str:
        current_room = self.get_current_room()
        
        # Check if the specified item is in the room
        matching_items = [item for item in current_room.items if item.lower() == item_name.lower()]
        
        if not matching_items:
            return f"There is no {item_name} here."
        
        item = matching_items[0]
        current_room.items.remove(item)
        
        if item == "Gold Coin":
            self.player.gold += 10
            return "You picked up 10 gold coins!"
        elif item == "Ancient Artifact":
            self.player.add_item(item)
            self.has_won = True
            return "You found the Ancient Artifact! You can now escape the dungeon and win the game!"
        elif item == "Magic Map":
            self.magic_map = True
            return "You can now see the entire dungeon map!"
        else:
            return self.player.add_item(item)
    
    def handle_use(self, item_name: str) -> str:
        result = self.player.use_item(item_name)
        if result:
            return result
        return f"You don't have {item_name} in your inventory."
    
    def process_command(self, command: str) -> str:
        command = command.lower().strip()
        parts = command.split()
        
        if not parts:
            return "Please enter a command."
        
        action = parts[0]
        
        if action in ["n", "north", "e", "east", "s", "south", "w", "west"]:
            # Handle movement shortcuts
            if action in ["n", "north"]:
                return self.move_player("north")
            elif action in ["e", "east"]:
                return self.move_player("east")
            elif action in ["s", "south"]:
                return self.move_player("south")
            elif action in ["w", "west"]:
                return self.move_player("west")
        
        elif action == "look":
            return self.get_current_room().describe()
        
        elif action == "fight" or action == "attack":
            return self.handle_combat()
        
        elif action == "take" or action == "get":
            if len(parts) < 2:
                return "Take what?"
            return self.handle_take(" ".join(parts[1:]))
        
        elif action == "use":
            if len(parts) < 2:
                return "Use what?"
            return self.handle_use(" ".join(parts[1:]))
        
        elif action == "inventory" or action == "i":
            if not self.player.inventory:
                return "Your inventory is empty."
            return "Inventory: " + ", ".join(self.player.inventory)
        
        elif action == "map" or action == "m":
            self.display_map()
            return ""
        
        elif action == "help" or action == "h":
            return """
Commands:
- north/n, east/e, south/s, west/w: Move in that direction
- look: Examine your surroundings
- fight/attack: Attack a monster in the room
- take/get [item]: Pick up an item
- use [item]: Use an item from your inventory
- inventory/i: Check your inventory
- map/m: Display the dungeon map
- help/h: Show this help message
- quit/exit: End the game
"""
        
        elif action == "quit" or action == "exit":
            self.game_over = True
            return "Thanks for playing!"
        
        else:
            return "I don't understand that command. Type 'help' for a list of commands."
    
    def play_game(self):
        # Show initial room description
        current_room = self.get_current_room()
        current_room.visited = True
        
        while not self.game_over:
            self.clear_screen()
            self.display_banner()
            self.display_stats()
            self.display_map()
            
            if self.has_won and self.player.position == (0, 0):
                print("""
                +-------------------------------------------+
                |                                           |
                |   CONGRATULATIONS! YOU HAVE WON!          |
                |                                           |
                +-------------------------------------------+
                
                You've escaped the dungeon with the Ancient Artifact!
                """)
                self.game_over = True
                input("Press Enter to exit...")
                break
            
            if not self.player.is_alive():
                print("""
                +-------------------------------------------+
                |                                           |
                |   GAME OVER - YOU HAVE DIED               |
                |                                           |
                +-------------------------------------------+
                """)
                self.game_over = True
                input("Press Enter to exit...")
                break
            
            command = input("\nWhat do you want to do? ")
            result = self.process_command(command)
            
            print(result)
            time.sleep(1)
            self.turn_count += 1


if __name__ == "__main__":
    # Fix for Windows console
    if sys.platform == 'win32':
        try:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        except:
            # If that doesn't work, we'll use standard ASCII characters instead
            pass
            
    game = Game()
    game.start_game()