import hashlib
from pymongo import MongoClient
import datetime

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
        self.username = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.height = height
        self.weight = weight

        UserProfile.all.append(self)
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.username, self.middle_name, self.last_name, self.age, self.height, self.weight})"
    
    def __str__(self):
        return f"Name: {self.username} {self.middle_name} {self.last_name} \nAge: {self.age} \nHeight: {self.height}cm \nWeight: {self.weight}kg"
    
    @classmethod
    def instantiate_from_database(cls):
        client = MongoClient("localhost", 27017)
        db = client.CCUsers
        users = db.Users

        for user in users.find():
            profile = user.get("profile", {})
            name = profile.get("name", {})
            UserProfile(
                user["email"],
                user["password"],
                user["privilege"],
                name.get("first_name", ""),
                name.get("middle_name", ""),
                name.get("last_name", ""),
                profile.get("age", 0),
                profile.get("height", 0.0),
                profile.get("weight", 0.0),
            )

def load_users():
    client = MongoClient("localhost", 27017)
    db = client.CCUsers
    users = db.Users
    CC_Users = []

    for user in users.find():
        CC_Users.append(user)

    return CC_Users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_users(username, email, password):
    client = MongoClient("localhost", 27017)
    db = client.CCUsers
    users = db.Users
    userscp = db.UserSCP
    users.insert_one({'email': email, 'password': password, 'privilege': 'user', 'profile': {'name': {'first_name': username}}})
    userscp.insert_one({'email': email, 'last_water_intake_time': datetime.datetime.now(), 'last_face_wash_time': datetime.datetime.now(), 'steps_walked_today': 0})


Users.instantiate_from_database()
UserProfile.instantiate_from_database()
print(Users.all)
print(Users.all[0])
print(UserProfile.all)
print(str(UserProfile.all[0]))