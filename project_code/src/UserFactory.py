# UserFactory.py
from project_code.src.UserInputParser import UserInputParser
from project_code.src.User import User
from project_code.src.Statistic import *
from project_code.src.Character import Character
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
