"""
The event.py module should define various types of events. An event is something that happens at a location and requires the player to make choices or interact in some way.

Here's a basic structure for event.py:
Event instances would be the interactive elements within a location where players make decisions or face challenges.
"""


from enum import Enum
from statistics import Statistic  # Import necessary classes
from project_code.src.Character import Character

class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"

class Event:
    def __init__(self, parser, data=None):
        self.parser = parser
        self.data = data or {}
        # Initialize properties from data
        self.status = EventStatus.UNKNOWN

        # Define event-specific logic and attributes

    def execute(self, party):
        # Logic for executing the event
        pass

    def resolve_choice(self, party, character, chosen_skill):
        # Logic for resolving the player's choice in the event
        pass

    # list of event methods
    # NOTE: since we have these events already, idt we'll need to do anything else with the methods above this since each event has its own logic

class BlacksmithEvent(Event):

    def blacksmith_event(character: Character):
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

class CastleEvent(Event):

    def castle_event(character: Character):
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

class ForestEvent(Event):
    
    def forest_event(character: Character):
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

class DragonEvent(Event):

    def azure_dragon_encounter(character: Character):
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

        try:
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
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
