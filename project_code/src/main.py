# main.py
import json
import sys
from typing import List
import random
import os


class Statistic:
    def __init__(self, legacy_points: int):
        self.value = self._generate_starting_value(legacy_points)
        self.description = None
        self.min_value = 0
        self.max_value = 100

    def __str__(self):
        return f"{self.value}"

    def increase(self, amount):
        self.value += amount
        if self.value > self.max_value:
            self.value = self.max_value

    def decrease(self, amount):
        self.value -= amount
        if self.value < self.min_value:
            self.value = self.min_value

    def _generate_starting_value(self, legacy_points: int):
        """Generate a starting value for the statistic based on random number and user properties."""
        """This is just a placeholder for now. Perhaps some statistics will be based on user properties, and others 
        will be random."""
        return legacy_points / 100 + random.randint(1, 3)

class Strength(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Strength is a measure of physical power."

class Dexterity(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Dexterity is a measure of physical speed."

class Constitution(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Constitution is a measure of physical resistance."

class Vitality(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Vitality is a measure of physical health."

class Endurance(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Endurance is a measure of healing speed."

class Intelligence(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Intelligence is a measure of how fast one can solve problems."

class Wisdom(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Wisdom is a measure of effective decision making under pressure."

class Knowledge(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Knowledge is a measure of how much one knows."

class Willpower(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Willpower is a measure of how much resistance to natural urges one has."

class Spirit(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Spirit is a measure of how difficult it is to learn new skills."

class Capacity(Statistic):
    def __init__(self, legacy_points: int, capacity_type: str):
        super().__init__(legacy_points)
        self.capacity_type = capacity_type
        self.associated_ability = None
        self.description = f"{capacity_type} capacity is a measure of how much {capacity_type} a character can hold."

    def associate_ability(self, ability_name: str):
        """Associate a specific ability with this capacity."""
        self.associated_ability = ability_name

    def __str__(self):
        if self.associated_ability:
            return f"{self.capacity_type} Capacity for {self.associated_ability}: {self.value}"
        return f"{self.capacity_type} Capacity: {self.value}"


class Location:

    def __init__(self, parser, number_of_events: int = 1):
        self.parser = parser
        self.events = [Event(self.parser) for _ in range(number_of_events)]

    def add_event(self, event):
        #add an event to the location
        self.events.append(event)

    import json

    def create_custom_event_from_static_text_file(self, file_path):
        # load json file from path
        with open(file_path, "r") as file:
            data = json.load(file)

        return Event(self.parser, data)
    
    def to_json(self) -> dict:
        return {
            #convert attributes to JSON-compatible types
            "number_of_events": len(self.events)
        }
    
    @classmethod
    def from_json(cls, data: dict, parser) -> 'Location':
        return cls(
            parser=parser,
            number_of_events=data["number_of_events"]
        )


from enum import Enum

class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Event:

        def __init__(self, parser, data: dict = None):
            self.parser = parser
            # parse json file
            self.primary = data['primary_attribute']
            self.secondary = data['secondary_attribute']
            self.prompt_text = data['prompt_text']
            self.pass_ = data['pass']
            self.fail = data['fail']
            self.partial_pass = data['partial_pass']


            self.status = EventStatus.UNKNOWN
            self.fail = {
                "message": "You failed."
            }
            self.pass_ = {
                "message": "You passed."
            }
            self.partial_pass = {
                "message": "You partially passed."
            }
            self.prompt_text = "A dragon appears, what will you do?"

            self.primary: Statistic = Strength()
            self.secondary: Statistic = Dexterity()

        def execute(self, party):
            chosen_one = self.parser.select_party_member(party)
            chosen_skill = self.parser.select_skill(chosen_one)

            self.resolve_choice(party, chosen_one, chosen_skill)

        def set_status(self, status: EventStatus = EventStatus.UNKNOWN):
            self.status = status

        def resolve_choice(self, party, character, chosen_skill):
            # check if the skill attributes overlap with the event attributes
            # if they don't overlap, the character fails
            # if one overlap, the character partially passes
            # if they do overlap, the character passes
            if self.primary and self.secondary:
                if(self.primary in character.stats and self.secondary in character.stats and chosen_skill.primary == self.primary and chosen_skill.secondary == self.secondary):
                    self.set_status(EventStatus.PASS)
                elif (self.primary in character.stats or self.secondary in character.stats or chosen_skill.primary == self.primary or chosen_skill.secondary == self.secondary):
                    self.set_status(EventStatus.PARTIAL_PASS)
                else:
                    self.set_status(EventStatus.FAIL)
            else:
                self.set_status(EventStatus.FAIL)


class Character:

    def __init__(self, name: str = None):
        """
        Core Stats: Everyone has these ad some text
        - Strength: How much you can lift. How strong you are. How hard you punch, etc.
        - Dexterity: How quick your limbs can perform intricate tasks. How adept you are at avoiding blows you anticipate. Impacts speed.
        - Constitution: The bodies natural armor. Characters may have unique positive or negative constitutions that provide additional capabilities
        - vitality: A measure of how lively you feel. How many Hit Points you have. An indirect measure of age.
        - Endurance: How fast you recover from injuries. How quickly you recover from fatigue.
        - Intelligence: How smart you are. How quickly you can connect the dots to solve problems. How fast you can think.
        - Wisdom: How effectively you can make choices under pressure. Generally low in younger people.
        - Knowledge: How much you know? This is a raw score for all knowledge. Characters may have specific areas of expertise with a bonus or deficit in some areas.
        - Willpower: How quickly or effectively the character can overcome natural urges. How susceptible they are to mind control.
        - Spirit: Catchall for ability to perform otherworldly acts. High spirit is rare. Different skills have different resource pools they might use like mana, stamina, etc. These are unaffected by spirit. Instead spirit is a measure of how hard it is to learn new otherworldly skills and/or master general skills.
         """
        self.name = self._generate_name() if name is None else name
        self.living_status = True
        self.strength: Strength = Strength(self)
        self.dexterity: Dexterity = Dexterity(self)
        self.constitution: Constitution = Constitution(self)
        self.vitality: Vitality = Vitality(self)
        self.endurance: Endurance = Endurance(self)
        self.intelligence: Intelligence = Intelligence(self)
        self.wisdom: Wisdom = Wisdom(self)
        self.knowledge: Knowledge = Knowledge(self)
        self.willpower: Willpower = Willpower(self)
        self.spirit: Spirit = Spirit(self)
        self.capacities = []  # List to hold capacity instances
        self.stats = [
            self.name, 
            self.living_status, 
            self.strength, 
            self.dexterity, 
            self.constitution,
            self.vitality, 
            self.endurance, 
            self.intelligence,
            self.wisdom,
            self.knowledge,
            self.willpower,
            self.spirit,
            self.capacities
            ]

    """
        The add_capacity function in the Character 
        class is designed to manage different types of 
        "capacities" that a character might possess.
    """
    def add_capacity(self, capacity):
        """Add a capacity to the character."""
        self.capacities.append(capacity)

    def _generate_name(self):
        return "Bob"
    
    def to_json(self) -> dict:
        return {
            #convert attributes to JSON-compatible types
            "name": self.name, 
            "living_status": self.living_status, 
            "strength": self.strength, 
            "dexterity": self.dexterity, 
            "constitution": self.constitution,
            "vitality": self.vitality,
            "endurance": self.endurance,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "knowledge": self.knowledge,
            "willpower": self.willpower,
            "spirit": self.spirit,
            "capacities": self.capacities
        }
    
    @classmethod
    def from_json(cls, data: dict) -> 'Character':
        return cls(
            name=data["name"], 
            living_status=data["living_status"], 
            strength=data["strength"],
            dexterity=data["dexterity"],
            constitution=data["constitution"],
            vitality=data["vitality"],
            endurance=data["endurance"],
            intelligence=data["intelligence"],
            wisdom=data["wisdom"],
            knowledge=data["knowledge"],
            willpower=data["willpower"],
            spirit=data["spirit"],
            capacities=data["capacities"]
        )


class Game:

    def __init__(self, parser):
        self.parser = parser
        self.characters: List[Character] = []
        self.locations: List[Location] = []
        self.events: List[Event] = []
        self.party: List[Character] = []
        self.current_location = None
        self.current_event = None
        self.continue_playing = True

        self._initialize_game()

    def add_character(self, character: Character):
        """Add a character to the game."""
        self.characters.append(character)

    def add_location(self, location: Location):
        """Add a location to the game."""
        self.locations.append(location)

    def add_event(self, event: Event):
        """Add an event to the game."""
        self.events.append(event)

    def _initialize_game(self):
        """Initialize the game with characters, locations, and events based on the user's properties."""
        character_list = [Character() for _ in range(10)]
        location_list = [Location(self.parser) for _ in range(2)]

        for character in character_list:
            self.add_character(character)

        for location in location_list:
            self.add_location(location)

    def start_game(self):
        return self._main_game_loop()

    def _main_game_loop(self):
        """The main game loop."""
        while self.continue_playing:
            self.current_location = self.locations[0]
            self.current_event = self.current_location.getEvent()

            self.current_event.execute()

            if self.party is None:
                # award legacy points
                self.continue_playing = False
                return "Save and quit"
            else:
                continue
        if self.continue_playing is False:
            return True
        elif self.continue_playing == "Save and quit":
            return "Save and quit"
        else:
            return False


class User:

    def __init__(self, parser, username: str, password: str, legacy_points: int = 0):
        self.username = username
        self.password = password
        self.legacy_points = legacy_points
        self.current_game = self._get_retrieve_saved_game_state_or_create_new_game()

    def _get_retrieve_saved_game_state_or_create_new_game(self) -> Game:
        save_file = f'save_{self.username}.json'
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                game_state = json.load(file)
                return Game.load_from_json(game_state)  # Assuming Game has a method to load from a JSON
        else:
            return Game()

    def save_game(self):
        save_file = f'save_{self.username}.json'
        with open(save_file, 'w') as file:
            game_state = self.current_game.to_json()  # Assuming Game has a method to convert to JSON
            json.dump(game_state, file)


class UserInputParser:

    def __init__(self):
        self.style = "console"

    def parse(self, prompt) -> str:
        response: str = input(prompt)
        return response


import csv

class UserFactory:
    
    @staticmethod
    def create_user(parser: UserInputParser) -> User:
        #creates user instance
        username = parser.parse("Enter a username: ")
        password = parser.parse("Enter a password: ")
        user = User(username, password)

        #save user data to CSV file
        UserFactory.save_user_to_csv(user, "users.csv")

        return user
    
    def save_user_to_csv(user:User, filename: str):
        #convert user instance to dict
        user_data = user.to_dict()

        #write user data to CSV file
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = user_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            #write data
            writer.writerow(user_data)
    
    def get_user_by_username(username: str, filename: str) -> User | None:
        #read user data from CSV file and search for username
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    return User(row['username'], row['password'])
        return None


class InstanceCreator:

    def __init__(self, user_factory: UserFactory, parser: UserInputParser):
        self.user_factory = user_factory
        self.parser = parser

    def _new_user_or_login(self) -> User:
        response = self.parser.parse("Create a new username or login to an existing account?")
        if "login" in response:
            return self._load_user()
        else:
            return self.user_factory.create_user(self.parser)

    def get_user_info(self, response: str) -> User | None:
        if "yes" in response:
            return self._new_user_or_login()
        else:
            return None

    def _load_user(self) -> User:
        username = self.parser.parse("Enter your username: ")
        return self.user_factory.get_user_by_username(username)


def start_game():
    parser = UserInputParser()
    user_factory = UserFactory()
    instance_creator = InstanceCreator(user_factory, parser)

    response = parser.parse("Would you like to start a new game? (yes/no)")
    print(f"Response: {response}")
    user = instance_creator.get_user_info(response)
    if user is not None:
        game_instance = user.current_game
        if game_instance is not None:
            response = game_instance.start_game()
            if response == "Save and quit":
                user.save_game()
                print("Game saved. Goodbye!")
                sys.exit()
            elif response:
                print("Goodbye!")
                sys.exit()
    else:
        print("See you next time!")
        sys.exit()


if __name__ == '__main__':
    start_game()
