"""
To implement location.py and event.py, you'll want to design these modules in a way that they can be used 
dynamically within your game. This would typically involve defining various locations 
(like a village, castle, pub, etc.) and events (encounters or situations that the player's party can experience) 
in a manner that integrates well with the rest of your game structure.

location.py
The location.py module should define different types of locations. 
Each location can have its own unique properties and events associated with it. 
For instance, a village may have different events compared to a cave.
Location instances can be created in the Game class and assigned different events based on the game's storyline.
Here's a basic structure for location.py:
"""
import json
import random
from project_code.src.Event import Event

class Location:
    def __init__(self, name, description, parser, number_of_events=1):
        self.name = name
        self.description = description
        self.parser = parser
        self.events = [Event(self.parser) for _ in range(number_of_events)]

    def explore(self, character):
        print(f"{character.name} explores the {self.name}.")
        return random.choice(self.events)(character)

    def complete_quest(self, character, success):
        if success:
            character.add_experience(5)  # Arbitrary experience points
            print(f"Quest completed! {character.name} earned experience.")
        else:
            print("Quest failed. Restarting adventure...")  
