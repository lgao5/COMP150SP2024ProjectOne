# UserFactory.py
from project_code.src.UserInputParser import UserInputParser
from project_code.src.User import User
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
