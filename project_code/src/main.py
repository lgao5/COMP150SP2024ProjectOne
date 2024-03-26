import random
import sys
import csv

# Simplified Statistic Class
class Statistic:
    def __init__(self, name, legacy_points):
        self.name = name
        self.value = random.randint(1, 10) + legacy_points // 10

    def __str__(self):
        return f"{self.name}: {self.value}"

class Character:
    def __init__(self, name):
        legacy_points = random.randint(0, 50)
        self.name = name
        self.level = 1
        self.experience = 0
        self.attempted_quests = set()
        self.successful_quests = set()
        self.stats = {
            "Strength": Statistic("Strength", legacy_points),
            "Dexterity": Statistic("Dexterity", legacy_points),
            "Constitution": Statistic("Constitution", legacy_points),
            "Vitality": Statistic("Vitality", legacy_points),
            "Endurance": Statistic("Endurance", legacy_points),
            "Intelligence": Statistic("Intelligence", legacy_points),
            "Wisdom": Statistic("Wisdom", legacy_points),
            "Knowledge": Statistic("Knowledge", legacy_points),
            "Willpower": Statistic("Willpower", legacy_points),
            "Spirit": Statistic("Spirit", legacy_points)
        }
        self.capacity = {
            "Mana": random.randint(10, 20),
            "Stamina": random.randint(10, 20),
            "Psy": random.randint(10, 20)
        }

    def __str__(self):
        stats_info = ', '.join(str(stat) for stat in self.stats.values())
        return f"Character: {self.name}, Stats: {stats_info}, Level: {self.level}, Experience: {self.experience}"
        capacity_info = ', '.join(f"{key}: {value}" for key, value in self.capacity.items())
        return f"{super().__str__()}, Capacity: {capacity_info}"
    def add_experience(self, amount):
        self.experience += amount
        if self.experience >= 10:  # Arbitrary value for leveling up
            self.experience -= 10
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f"{self.name} has reached level {self.level}!")
    def rest(self):
        for stat in self.stats.values():
            stat.value += random.randint(1, 3)
        print(f"{self.name} has rested and gained strength.")
    def reduce_stats(self, stats_to_reduce):
        for stat_name, reduction in stats_to_reduce.items():
            if stat_name in self.stats:
                self.stats[stat_name].value = max(self.stats[stat_name].value - reduction, 0)  # Prevent stats from going below 0

class Location:
    def __init__(self, name, description, events):
        self.name = name
        self.description = description
        self.events = events

    def explore(self, character):
        print(f"{character.name} explores the {self.name}.")
        return random.choice(self.events)(character)

    def complete_quest(self, character, success):
        if success:
            character.add_experience(5)  # Arbitrary experience points
            print(f"Quest completed! {character.name} earned experience.")
        else:
            print("Quest failed. Restarting adventure...")

def blacksmith_event(character):
    if character.capacity["Stamina"] < 13:
        print(f"{character.name} does not have enough Stamina to help in the blacksmith.")
        return False

    required_stats = {"Strength": 5, "Endurance": 5, "Vitality": 5}
    success = all(character.stats[stat].value > requirement for stat, requirement in required_stats.items())
    if success:
        print("You help the blacksmith and earn a strong sword!")
        character.reduce_stats(required_stats)
        character.capacity["Stamina"] -= 3  # Reduce capacity
    else:
        print("You watch the blacksmith work and learn about sword making.")
    return success

def castle_event(character):
    if character.capacity["Psy"] < 14:
        print(f"{character.name} does not have enough Psy to counsel the king.")
        return False

    required_stats = {"Wisdom": 5, "Intelligence": 5, "Knowledge": 5}
    success = all(character.stats[stat].value > requirement for stat, requirement in required_stats.items())
    if success:
        print("You provide wise counsel to the king and are rewarded!")
        character.reduce_stats(required_stats)
        character.capacity["Psy"] -= 5  # Reduce capacity
    else:
        print("You wander the castle and marvel at its grandeur.")
    return success

def forest_event(character):
    if character.capacity["Mana"] < 15:
        print(f"{character.name} does not have enough Mana to navigate the forest.")
        return False

    required_stats = {"Dexterity": 5, "Spirit": 5, "Willpower": 5}
    success = all(character.stats[stat].value > requirement for stat, requirement in required_stats.items())
    if success:
        print("You navigate the forest adeptly, finding hidden treasures!")
        character.reduce_stats(required_stats)
        character.capacity["Mana"] -= 4  # Reduce capacity
    else:
        print("You get lost but manage to find your way back after an adventure.")
    return success

class SaveUser:
    @staticmethod
    def save_characters(characters, filename="characters_save.csv"):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Level", "Experience", "Strength", "Dexterity", "Constitution", "Vitality", "Endurance", "Intelligence", "Wisdom", "Knowledge", "Willpower", "Spirit"])
            for character in characters:
                stats = character.stats
                writer.writerow([
                    character.name, 
                    character.level, 
                    character.experience,
                    stats["Strength"].value, 
                    stats["Dexterity"].value, 
                    stats["Constitution"].value,
                    stats["Vitality"].value, 
                    stats["Endurance"].value, 
                    stats["Intelligence"].value,
                    stats["Wisdom"].value, 
                    stats["Knowledge"].value, 
                    stats["Willpower"].value, 
                    stats["Spirit"].value
                ])

    @staticmethod
    def load_characters(filename="characters_save.csv"):
        characters = []
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader) #skip header row
                for row in reader:
                    name, level, experience, strength, dexterity, constitution, vitality, endurance, intelligence, wisdom, knowledge, willpower, spirit = row
                    # Create Character instance using the data from the CSV
                    character = Character(name)
                    character.level = int(level)
                    character.experience = int(experience)
                    character.stats["Strength"].value = int(strength)
                    character.stats["Dexterity"].value = int(dexterity)
                    character.stats["Constitution"].value = int(constitution)
                    character.stats["Vitality"].value = int(vitality)
                    character.stats["Endurance"].value = int(endurance)
                    character.stats["Intelligence"].value = int(intelligence)
                    character.stats["Wisdom"].value = int(wisdom)
                    character.stats["Knowledge"].value = int(knowledge)
                    character.stats["Willpower"].value = int(willpower)
                    character.stats["Spirit"].value = int(spirit)
                    characters.append(character)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        return characters

def start_game():
    print("Welcome to the Towns Explorer game!")
    load_choice = input("Do you want to load a saved game? (yes/no): ").lower()
    characters = []

    if load_choice == 'yes':
        file_path = input("Enter the path of the saved game file: ")
        try: 
            characters = SaveUser.load_characters(file_path)
            print("Game loaded successfully.")
        except FileNotFoundError:
            print("No saved game file found at the given path. Starting a new game.")
            load_choice = 'no'
    if load_choice != 'yes':
        num_players = int(input("Enter the number of characters (up to 10): "))
        num_players = min(num_players, 10)  # Limit the number of players to 10

        for _ in range(num_players):
            player_name = input("Enter your character's name: ")
            new_character = Character(player_name)
            characters.append(new_character)
            print("\nCharacter created:")
            print(new_character)  # Display the character's stats

    locations = [
        Location("Blacksmith", "a place where weapons are made", [blacksmith_event]),
        Location("Castle", "the residence of the king", [castle_event]),
        Location("Mysterious Forest", "a forest full of secrets", [forest_event]),
    ]

    while characters:
        for player in characters[:]:
            print(f"\n{player.name}'s turn.")
            action = input("Choose an action: [explore, rest, buy capacity, save, quit]: ")

            if action == "explore":
                available_locations = [loc for loc in locations if loc.name not in player.successful_quests and loc.name not in player.attempted_quests]
                if not available_locations:
                    print("You've attempted all available adventures. Maybe rest or quit?")
                    continue

                location = random.choice(available_locations)
                success = location.explore(player)
                location.complete_quest(player, success)

                player.attempted_quests.add(location.name)
                if success:
                    player.successful_quests.add(location.name)

            elif action == "rest":
                player.rest()  # Call the new rest method
                player.attempted_quests.clear()
                print(f"{player.name} feels refreshed and ready for new adventures.")
                print(player)  # Optionally display the updated stats


            elif action == "quit":
                print(f"{player.name} is leaving the game.")
                characters.remove(player)  # Remove the character from the game
                if not characters:
                    print("All players have left. Thank you for playing!")
                break  # End this player's turn
            elif action == "save":
                SaveUser.save_characters(characters)
                print("Game progress saved.")
            elif action == "buy capacity":
                capacity_choice = input("Which capacity would you like to buy for 5 constitution (Mana, Stamina, Psy)? ").capitalize()
                if capacity_choice in ["Mana", "Stamina", "Psy"]:
                    if player.stats["Constitution"].value >= 5:
                        player.stats["Constitution"].value -= 5
                        player.capacity[capacity_choice] += 2
                        print(f"{capacity_choice} capacity increased! New capacities: {player.capacity}")
                    else:
                        print("Not enough Constitution to buy capacity.")
                else:
                    print("Invalid capacity type.")


if __name__ == "__main__":
    start_game()