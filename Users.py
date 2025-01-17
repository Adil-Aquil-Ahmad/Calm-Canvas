import hashlib
from pymongo import MongoClient

class Users:
    
    all = []

    def __init__(self, email: str, password: str, privilege: str = "user"):
        
        self.email = email
        self.password = password
        self.privilege = privilege

        Users.all.append(self)
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.email}, {self.password}, {self.privilege})"
    
    def __str__(self):
        return f"Email: {self.email}\nPassword: {self.password}\nPrivelege: {self.privilege}"

    @classmethod
    def instantiate_from_database(cls):
        client = MongoClient("localhost", 27017)
        db = client.CCUsers
        users = db.Users

        for user in users.find():
            Users(user["email"], user["password"], user["privilege"])



class UserProfile(Users):

    all = []

    def __init__(self, email, password, privilege, first_name: str, middle_name: str, last_name: str, age: int, height: float, weight: float):
        super().__init__(email, password, privilege)
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.height = height
        self.weight = weight

        UserProfile.all.append(self)
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.first_name, self.middle_name, self.last_name, self.age, self.height, self.weight})"
    
    def __str__(self):
        return f"Name: {self.first_name} {self.middle_name} {self.last_name} \nAge: {self.age} \nHeight: {self.height}cm \nWeight: {self.weight}kg"
    
    @classmethod
    def instantiate_from_database(cls):
        client = MongoClient("localhost", 27017)
        db = client.CCUsers
        users = db.Users

        for user in users.find():
            UserProfile(user["email"],
                        user["password"],
                        user["privilege"],
                        user["profile"]["name"]["first_name"], 
                        user["profile"]["name"]["middle_name"], 
                        user["profile"]["name"]["last_name"],
                        user["profile"]["age"],
                        user["profile"]["height"],
                        user["profile"]["weight"]
                        )


Users.instantiate_from_database()
UserProfile.instantiate_from_database()
print(Users.all)
print(UserProfile.all)
print(str(UserProfile.all[0]))


