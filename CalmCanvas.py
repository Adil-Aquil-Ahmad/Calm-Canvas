from Users import Users, UserProfile
import datetime

class SelfCare():

    all = []
    
    def __init__(self, email: str, height: int, weight: float, last_water_intake_time: datetime, last_face_wash_time: datetime, steps_Walked_today: int):

        self.email = email
        self.height = height
        self.weight = weight
        self.LWIT = last_water_intake_time
        self.LFWT = last_face_wash_time
        self.SWT = steps_Walked_today


        SelfCare.all.append(self)

    
    def calculate_BMI(self):

        BMI = self.weight/((self.height/100)**2)
        return BMI
    
    def time_since_lwit(self):
        
        now = datetime.datetime.now()
        since = now - self.LWIT
        return since
    
    def time_since_LFWT(self):

        now = datetime.datetime.now()
        since = now - self.LWIT
        return since
    
    def calculate_calories_burnt(self):

        Calories_burnt = 0.03 * self.SWT
        return Calories_burnt
    

    