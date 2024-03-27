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
