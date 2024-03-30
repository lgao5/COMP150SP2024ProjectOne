import random
import sys
import csv


class Statistic:
    def __init__(self, name, legacy_points):
        self.name = name
        self.value = random.randint(1, 10) + legacy_points // 10

    def __str__(self):
        return f"{self.name}: {self.value}"

class Character:
    def __init__(self, name, level=1, experience=0, stats=None):
        legacy_points = random.randint(0, 50)
        self.name = name
        self.level = level
        self.experience = experience
        self.attempted_quests = set()
        self.successful_quests = set()

        if stats:
            self.stats = stats
        else:
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
    def has_completed_all_quests(self):
        return len(self.successful_quests) == 3
class Location:
    def __init__(self, name, description, events):
        # Enhanced descriptions for each location
        self.name = name
        self.description = description
        self.events = events

    # Add more narrative elements in each location's exploration
    def explore(self, character):
        print(f"{character.name} treads cautiously into the {self.name}. {self.description}")
        return random.choice(self.events)(character)
    def complete_quest(self, character, success):
        if success:
            character.add_experience(5)  # Arbitrary experience points
            print(f"Quest completed! {character.name} earned experience.")
        else:
            print("Quest failed. Restarting adventure...")
def azure_dragon_encounter(character):
    print("The air grows cold and the ground trembles as you step into the lair of the Azure Dragon.")
    print("You have entered the Dungeon of the Azure Dragon!")
    weapons = ["Halberd", "Heavy Crossbow", "Divine Rapier", "Recurve Bow", "Spellcaster"]
    weapon_descriptions = {
        "Halberd": "A massive blade on a long pole, excellent for keeping dragons at bay.",
        "Heavy Crossbow": "A powerful ranged weapon, perfect for piercing dragon scales.",
        "Divine Rapier": "A sword of light, deadly to all evil creatures.",
        "Recurve Bow": "A bow with intricate designs, its arrows swift and true.",
        "Spellcaster": "Harness the arcane, casting spells of destruction and protection."
    }
    dragon_hits = 0

    print("Choose your weapon to fight the Azure Dragon:")
    for i, weapon in enumerate(weapons, start=1):
        print(f"{i}. {weapon}: {weapon_descriptions[weapon]}")
    
    weapon_choice = int(input("Select a weapon (1-5): "))
    if 1 <= weapon_choice <= 5:
        chosen_weapon = weapons[weapon_choice - 1]
        print(f"You have chosen the {chosen_weapon}. The battle begins!")

        while dragon_hits < 2:
            combat_action = input(f"Choose an action with your {chosen_weapon}: [strike/block]: ").lower()
            if combat_action == "strike":
                dragon_hits += 1
                print(f"You strike the Azure Dragon with your {chosen_weapon}! It reels from the hit.")
            elif combat_action == "block":
                print(f"You skillfully block the Azure Dragon's attack with your {chosen_weapon}.")
            else:
                print("In your hesitation, the dragon gains the upper hand!")

            if dragon_hits == 2:
                victory_description = {
                    "Halberd": "With a mighty thrust of your Halberd, the dragon collapses, defeated by your valor.",
                    "Heavy Crossbow": "Your final bolt finds its mark in the dragon's heart, ending its reign of terror.",
                    "Divine Rapier": "Light from your Divine Rapier pierces the dragon, banishing its dark essence.",
                    "Recurve Bow": "Your last arrow soars, striking true and felling the mighty beast.",
                    "Spellcaster": "A burst of magical energy envelops the dragon, sealing its fate."
                }
                print(victory_description[chosen_weapon])
                print(f"Congratulations {character.name}, you have defeated the Azure Dragon!")
                break
    else:
        print("Invalid choice. The dragon attacks and you are unprepared! The battle is lost.")

def blacksmith_event(character):
    print(f"Entering the blacksmith's forge, {character.name} is greeted by the heat of blazing fires and the sound of hammering.")
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
    print(f"As {character.name} approaches the majestic castle, the air fills with the sense of ancient power and intrigue.")
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
    print(f"The Mysterious Forest stands before {character.name}, its depths whispering secrets and untold dangers.")
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
    def load_characters(filename):
        characters = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stats = {
                    "Strength": Statistic("Strength", int(row["Strength"])),
                    "Dexterity": Statistic("Dexterity", int(row["Dexterity"])),
                    "Constitution": Statistic("Constitution", int(row["Constitution"])),
                    "Vitality": Statistic("Vitality", int(row["Vitality"])),
                    "Endurance": Statistic("Endurance", int(row["Endurance"])),
                    "Intelligence": Statistic("Intelligence", int(row["Intelligence"])),
                    "Wisdom": Statistic("Wisdom", int(row["Wisdom"])),
                    "Knowledge": Statistic("Knowledge", int(row["Knowledge"])),
                    "Willpower": Statistic("Willpower", int(row["Willpower"])),
                    "Spirit": Statistic("Spirit", int(row["Spirit"])),
                }
                character = Character(
                    name=row["Name"],
                    level=int(row["Level"]),
                    experience=int(row["Experience"]),
                    stats=stats
                )
                characters.append(character)
        return characters
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


def start_game():
    print("Welcome to the Towns Explorer game, a world of mystery and adventure!")
    print("In this land, heroes embark on quests to prove their valor and skill.")
    print("Are you ready to carve your name into the legends of the realm?")

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
            characters.append(Character(player_name))
            print(f"\nCharacter created: {characters[-1]}")  # Display the character's stats

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
                if player.has_completed_all_quests():
                    final_choice = input("You have been offered a one time opportunity, do you wish to enter the Dungeon of the Azure Dragon? (yes/no): ").lower()
                    if final_choice == "yes":
                        azure_dragon_encounter(player)
                        continue  # after the encounter
            # existing exploration logic...

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
