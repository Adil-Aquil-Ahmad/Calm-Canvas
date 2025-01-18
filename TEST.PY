from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.CCUsers
users = db.Users
user_scp = db.UserSCP 

user = users.find_one({'email': 'adilaquil2005@gmail.com'})
user_scp_data = user_scp.find_one({'email': 'adilaquil2005@gmail.com'})


profile_data = {
    'first_name': user['profile']['name'].get('first_name', ''),
    'middle_name': user['profile']['name'].get('middle_name', ''),
    'last_name': user['profile']['name'].get('last_name', ''),
    'age': user['profile'].get('age', ''),
    'height': user['profile'].get('height', ''),
    'weight': user['profile'].get('weight', ''),
}

self_care = {
    'email': user_scp_data.get('email', ''),
    'height': user['profile'].get('height', ''),
    'weight': user['profile'].get('weight', ''),
    'last_water_intake_time': user_scp_data.get('last_water_intake_time', ''),
    'last_face_wash_time': user_scp_data.get('last_face_wash_time', ''),
    'steps_walked_today': user_scp_data.get('steps_walked_today', ''),
}

print(self_care)