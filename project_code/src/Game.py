from typing import List
import random

from project_code.src.Character import Character
from project_code.src.Event import Event
from project_code.src.Location import Location
from project_code.src.Event import BlacksmithEvent
from project_code.src.Event import CastleEvent
from project_code.src.Event import ForestEvent
from project_code.src.UserFactory import UserFactory


class Game:

    def __init__(self):
        self.characters: List[Character] = []
        self.locations: List[Location] = []
        self.events: List[Event] = []
        self.party: List[Character] = []
        self.current_location = None
        self.current_event = None
        self._initialize_game()
        self.continue_playing = True

    def add_character(self, character: Character):
        """Add a character to the game."""
        self.characters.append(character)

    def add_location(self, location: Location):
        """Add a location to the game."""
        self.locations.append(location)

    #dw about this for now
    def add_event(self, event: Event):
        """Add an event to the game."""
        self.events.append(event)

    def load_events(self):
        blacksmith_event = BlacksmithEvent()
        castle_event = CastleEvent()
        forest_event = ForestEvent()
        

    def _initialize_game(self):
        """Initialize the game with characters, locations, and events based on the user's properties."""
        pass

    def start_game(self):
        return self._main_game_loop()

    def _main_game_loop(self):
        print("Welcome to the Towns Explorer game!")
    
        load_choice = input("Do you want to load a saved game? (yes/no): ").lower()
        characters = []

        if load_choice == 'yes':
            file_path = input("Enter the path of the saved game file: ")
            try:
                characters = UserFactory.load_characters(file_path)
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

        #self.load_events()   tbh idk if this method is needed
        locations = [
            Location("Blacksmith", "a place where weapons are made", [self.blacksmith_event]),
            Location("Castle", "the residence of the king", [self.castle_event]),
            Location("Mysterious Forest", "a forest full of secrets", [self.forest_event]),
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
                    UserFactory.save_characters(characters)
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








