from typing import List
import random


from project_code.src.Character import Character
from project_code.src.Event import Event, BlacksmithEvent, CastleEvent, ForestEvent, DragonEvent
from project_code.src.Location import Location
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
        self.events.extend([BlacksmithEvent(), CastleEvent(), ForestEvent(), DragonEvent()])
        

    def _initialize_game(self):
        """Initialize the game with characters, locations, and events based on the user's properties."""
        pass

    def start_game(self):
        return self._main_game_loop()

    def _main_game_loop(self):
        print("Welcome to the Towns Explorer game, a world of mystery and adventure!")
        print("In this land, heroes embark on quests to prove their valor and skill.")
        print("Are you ready to carve your name into the legends of the realm?")

        while True:
            try:
                load_choice = input("Do you want to load a saved game? (yes/no): ").lower()
                if load_choice not in ["yes", "no"]:
                    raise ValueError("Please enter 'yes' or 'no'.")
                break
            except ValueError as e:
                print(e)

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
            while True:
                try:
                    num_players = int(input("Enter the number of characters (up to 10): "))
                    if not 1 <= num_players <= 10:
                        raise ValueError("Please enter a number between 1 and 10.")
                    break
                except ValueError as e:
                    print(e)

            for _ in range(num_players):
                player_name = input("Enter your character's name: ")
                characters.append(Character(player_name))
                print(f"\nCharacter created: {characters[-1]}")  # Display the character's stats

        self.load_events()
        locations = [
            Location("Blacksmith", "a place where weapons are made", [self.events[0]]),
            Location("Castle", "the residence of the king", [self.events[1]]),
            Location("Mysterious Forest", "a forest full of secrets", [self.events[2]]),
        ]
        azure_dragon_encounter = self.events[3]

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

                elif action == "rest":
                    player.rest()
                    player.attempted_quests.clear()
                    print(f"{player.name} feels refreshed and ready for new adventures.")
                    print(player)

                elif action == "quit":
                    print(f"{player.name} is leaving the game.")
                    characters.remove(player)
                    if not characters:
                        print("All players have left. Thank you for playing!")
                    break

                elif action == "save":
                    UserFactory.save_characters(characters)
                    print("Game progress saved.")

                elif action == "buy capacity":
                    try:
                        capacity_choice = input("Which capacity would you like to buy for 5 constitution (Mana, Stamina, Psy)? ").capitalize()
                        if capacity_choice not in ["Mana", "Stamina", "Psy"]:
                            raise ValueError("Invalid capacity type. Please choose 'Mana', 'Stamina', or 'Psy'.")
                        if player.stats["Constitution"].value >= 5:
                            player.stats["Constitution"].value -= 5
                            player.capacity[capacity_choice] += 2
                            print(f"{capacity_choice} capacity increased! New capacities: {player.capacity}")
                        else:
                            print("Not enough Constitution to buy capacity.")
                    except ValueError as e:
                        print(e)

if __name__ == "__main__":
    game1 = Game()
    game1._main_game_loop()







