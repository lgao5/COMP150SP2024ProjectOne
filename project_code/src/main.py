import random
import sys

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
        self.stats = {
            "Strength": Statistic("Strength", legacy_points),
            "Dexterity": Statistic("Dexterity", legacy_points),
            "Intelligence": Statistic("Intelligence", legacy_points),
            "Wisdom": Statistic("Wisdom", legacy_points)
        }

    def __str__(self):
        stats_info = ', '.join(str(stat) for stat in self.stats.values())
        return f"Character: {self.name}, Stats: {stats_info}, Level: {self.level}, Experience: {self.experience}"

    def add_experience(self, amount):
        self.experience += amount
        if self.experience >= 10:  # Arbitrary value for leveling up
            self.experience -= 10
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f"{self.name} has reached level {self.level}!")

def level_up(self):
    self.level += 1
    print(f"{self.name} has reached level {self.level}!")

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
    success = character.stats["Strength"].value > 7
    if success:
        print("You help the blacksmith and earn a strong sword!")
    else:
        print("You watch the blacksmith work and learn about sword making.")
    return success

def castle_event(character):
    success = character.stats["Wisdom"].value > 7
    if success:
        print("You provide wise counsel to the king and are rewarded!")
    else:
        print("You wander the castle and marvel at its grandeur.")
    return success

def forest_event(character):
    success = character.stats["Dexterity"].value > 7
    if success:
        print("You navigate the forest adeptly, finding hidden treasures!")
    else:
        print("You get lost but manage to find your way back after an adventure.")
    return success

def start_game():
    print("Welcome to the simplified D&D game!")

    player_name = input("Enter your character's name: ")
    player = Character(player_name)
    print(player)

    locations = [
        Location("Blacksmith", "a place where weapons are made", [blacksmith_event]),
        Location("Castle", "the residence of the king", [castle_event]),
        Location("Mysterious Forest", "a forest full of secrets", [forest_event]),
    ]
    attempted_quests = set()
    successful_quests = set()

    while True:
        action = input("Choose an action: [explore, rest, quit]: ")
        if action == "explore":
            # Allow locations that have never been attempted or failed
            available_locations = [loc for loc in locations if loc.name not in successful_quests and loc.name not in attempted_quests]
            if not available_locations:
                print("You've attempted all available adventures. Maybe rest or quit?")
                continue

            location = random.choice(available_locations)
            success = location.explore(player)
            location.complete_quest(player, success)

            # Add to attempted quests and successful quests if completed
            attempted_quests.add(location.name)
            if success:
                successful_quests.add(location.name)

        elif action == "rest":
            print(f"{player.name} takes a moment to rest and gather strength.")
            # Clear only the attempted quests, not the successful ones
            attempted_quests.clear()
            print("You feel refreshed and ready for new adventures!")

        elif action == "quit":
            print("Thank you for playing!")
            break  # Ends the game session

if __name__ == "__main__":
    start_game()
