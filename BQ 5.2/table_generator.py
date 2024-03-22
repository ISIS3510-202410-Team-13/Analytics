import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Generate random data for the dataset
num_rows = 1000

# Generate UserIDs
user_ids = [fake.unique.uuid4() for _ in range(num_rows)]

# Generate UserType: Nuevo, Ocasional, Frecuente
user_types = ['Nuevo', 'Ocasional', 'Frecuente']
user_type = [random.choice(user_types) for _ in range(num_rows)]

# Generate UserSemester: Values between 1 and 10
user_semester = [random.randint(1, 10) for _ in range(num_rows)]

# Generate UserCareer: ISIS, IIND, MATE, IBIO, IELE, IMEC, IQUI, ICYA, LITE, PSIC, MEDI
user_careers = ["ISIS", "IIND", "MATE", "IBIO", "IELE", "IMEC", "IQUI", "ICYA", "LITE", "PSIC", "MEDI"]
user_career = [random.choice(user_careers) for _ in range(num_rows)]

# Generate MeetingDate
meeting_dates = [fake.date_this_year() for _ in range(num_rows)]

# Generate DayOfWeek
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_of_week = [random.choice(days_of_week) for _ in range(num_rows)]

# Generate MeetingDuration: Up to 4 hours
meeting_duration = [random.randint(15, 240) for _ in range(num_rows)]

# Generate MeetingBuilding: ML, SD, W, R, O, C, LL, B, RGD, AU
meeting_buildings = ["ML", "SD", "W", "R", "O", "C", "LL", "B", "RGD", "AU"]
meeting_building = [random.choice(meeting_buildings) for _ in range(num_rows)]

# Generate MeetingPurpose: Class, Leisure, Group Project, Other
meeting_purposes = ["Class", "Leisure", "Group Project", "Other"]
meeting_purpose = [random.choice(meeting_purposes) for _ in range(num_rows)]

# Generate OverallSatisfactionScore: Values between 1 and 5
overall_satisfaction_score = [random.randint(1, 5) for _ in range(num_rows)]

# Create the DataFrame
df = pd.DataFrame({
    'UserID': user_ids,
    'UserType': user_type,
    'UserSemester': user_semester,
    'UserCareer': user_career,
    'MeetingDate': meeting_dates,
    'DayOfWeek': day_of_week,
    'MeetingDuration': meeting_duration,
    'MeetingBuilding': meeting_building,
    'MeetingPurpose': meeting_purpose,
    'OverallSatisfactionScore': overall_satisfaction_score
})

# Display the DataFrame
print(df.head())

file_path = "./meeting_data.xlsx"
df.to_excel(file_path, index=False)
