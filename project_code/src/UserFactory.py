# UserFactory.py
from project_code.src.UserInputParser import UserInputParser
from project_code.src.User import User


class UserFactory:

    #store a list of all users
    list_of_users = {}
    
    @staticmethod
    def create_user(parser: UserInputParser) -> User:
        #creates user instance
        username = parser.parse("Enter a username: ")
        password = parser.parse("Enter a password: ")

        #adds user instance to list of users
        UserFactory.list_of_users[username] = User(username, password)
        return User(username, password)
    
    def get_user_by_username(username: str) -> User | None:
        return UserFactory.list_of_users.get(username)
