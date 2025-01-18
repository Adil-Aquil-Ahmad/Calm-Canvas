from flask import render_template, request, redirect, url_for, flash, session
from Users import Users, UserProfile, load_users, hash_password, save_users
from CalmCanvas import SelfCare
import hashlib
from pymongo import MongoClient
import datetime

def initialise_routes(app):

    @app.route('/')
    def home():
        if 'username' in session:
            return redirect(url_for('my_profile'))
        else:
            return render_template('Login.html')

    @app.route('/analytics', methods=['GET', 'POST'])
    def analytics():
        print(session['email'])
        if 'username' not in session:
            flash("You need to log in first.", "danger")
            return redirect(url_for('login'))

        client = MongoClient("localhost", 27017)
        db = client.CCUsers
        users = db.Users
        user_scp = db.UserSCP 
        print(session['email'])
        user = users.find_one({'email': session['email']})
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('login'))

        profile_data = {
            'first_name': user['profile']['name'].get('first_name', ''),
            'middle_name': user['profile']['name'].get('middle_name', ''),
            'last_name': user['profile']['name'].get('last_name', ''),
            'age': user['profile'].get('age', ''),
            'height': user['profile'].get('height', ''),
            'weight': user['profile'].get('weight', ''),
        }

        user_scp_data = user_scp.find_one({'email': session['email']})
        if not user_scp_data:
            user_scp_data = {}

        self_care = {
            'email': user_scp_data.get('email', ''),
            'height': user['profile'].get('height', ''),
            'weight': user['profile'].get('weight', ''),
            'last_water_intake_time': user_scp_data.get('last_water_intake_time', ''),
            'last_face_wash_time': user_scp_data.get('last_face_wash_time', ''),
            'steps_walked_today': user_scp_data.get('steps_walked_today', ''),
}
        print(self_care)
        print(self_care['last_water_intake_time'])
        print(self_care['email'])
        print(self_care['last_face_wash_time'])
        print(self_care['steps_walked_today'])

        self_care_obj = SelfCare(
            email=self_care['email'], 
            height=profile_data['height'], 
            weight=profile_data['weight'], 
            last_water_intake_time=self_care['last_water_intake_time'], 
            last_face_wash_time=self_care['last_face_wash_time'], 
            steps_Walked_today=self_care['steps_walked_today']
        )


        bmi = self_care_obj.calculate_BMI()
        time_since_lwit = self_care_obj.time_since_lwit()
        time_since_lfwt = self_care_obj.time_since_LFWT()
        calories_burnt = self_care_obj.calculate_calories_burnt()

        if request.method == 'POST':
            new_water_time = request.form.get('last_water_intake_time')
            new_steps = request.form.get('steps_walked_today')

            user_scp.update_one(
                {'email': session['email']},
                {'$set': {
                    'last_water_intake_time': new_water_time,
                    'steps_walked_today': new_steps
                }}
            )
            flash("Self-care data updated successfully!", "success")
            return redirect(url_for('analytics'))

        return render_template(
            'Analytics.html', 
            profile=profile_data,
            bmi=bmi,
            time_since_lwit=time_since_lwit,
            time_since_lfwt=time_since_lfwt,
            calories_burnt=calories_burnt,
            steps_walked=self_care['steps_walked_today'],
            self_care=self_care
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'username' in session:
            flash("You are already signed in.", "danger")
            return redirect(url_for('my_profile'))

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            users = load_users()
            for user in users:
                if user['email'] == email and user['password'] == hash_password(password):
                    session['username'] = user["profile"]["name"]["first_name"]
                    session['email'] = user['email']
                    flash("Login successful!", "success")
                    return redirect(url_for('my_profile'))
            flash("Invalid email or password.", "danger")

        return render_template('Login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['Username']
            email = request.form['Email']
            password = request.form['Password']

            users = load_users()
            if any(user['email'] == email for user in users):
                flash("Email already registered.", "danger")
                return redirect(url_for('register'))

            save_users(username, email, hash_password(password))
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))

        return render_template('SignUp.html')

    @app.route('/my_profile', methods=['GET', 'POST'])
    def my_profile():
        if 'email' not in session:
            flash("You need to log in first.", "danger")
            return redirect(url_for('login'))

        client = MongoClient("localhost", 27017)
        db = client.CCUsers
        users = db.Users

        user = users.find_one({'email': session['email']})
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('login'))

        profile_data = {
            'first_name': user['profile']['name'].get('first_name', ''),
            'middle_name': user['profile']['name'].get('middle_name', ''),
            'last_name': user['profile']['name'].get('last_name', ''),
            'age': user['profile'].get('age', ''),
            'height': user['profile'].get('height', ''),
            'weight': user['profile'].get('weight', ''),
        }

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            middle_name = request.form.get('middle_name', '')
            last_name = request.form.get('last_name')
            age = int(request.form.get('age', 0))
            height = float(request.form.get('height', 0))
            weight = float(request.form.get('weight', 0))

            users.update_one(
                {'email': session['email']},
                {'$set': {
                    'profile.name.first_name': first_name,
                    'profile.name.middle_name': middle_name,
                    'profile.name.last_name': last_name,
                    'profile.age': age,
                    'profile.height': height,
                    'profile.weight': weight,
                }}
            )

            flash("Profile updated successfully!", "success")
            return redirect(url_for('my_profile'))

        return render_template(
            'Profile.html', 
            profile=profile_data
        )


