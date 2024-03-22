import pandas as pd
import numpy as np

np.random.seed(42)  
num_rows = 100
user_ids = np.arange(1, num_rows + 1)
user_types = np.random.choice(['Nuevo', 'Frecuente', 'Ocasional'], size=num_rows)

booking_attempt_dates = pd.date_range(start="2024-01-01", end="2024-03-31", freq='8H')[:num_rows]


buildings = ['ML', 'SD', 'O', 'W', 'RGD']
rooms = ['102', '202', '301', '302']
space_ids = [np.random.choice(buildings) + np.random.choice(rooms) for _ in range(num_rows)]

ease_of_use_scores = np.random.randint(1, 6, size=num_rows)  
availability_scores = np.random.randint(1, 6, size=num_rows)  
overall_satisfaction_scores = np.random.randint(1, 6, size=num_rows)  
feedback_comments = np.random.choice(['Todo bien', 'Necesita mejoras', 'Excelente', 'Frustrante', 'Confuso'], size=num_rows)

df_updated = pd.DataFrame({
    'UserID': user_ids,
    'UserType': user_types,
    'BookingAttemptDate': booking_attempt_dates,
    'SpaceID': space_ids,
    'EaseOfUseScore': ease_of_use_scores,
    'AvailabilityScore': availability_scores,
    'OverallSatisfactionScore': overall_satisfaction_scores,
    'FeedbackComments': feedback_comments
})