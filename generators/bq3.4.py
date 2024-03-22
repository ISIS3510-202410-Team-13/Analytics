import pandas as pd
import numpy as np
from faker import Faker
fake = Faker()

# Crear datos falsos para la tabla
np.random.seed(0)  # Para reproducibilidad
num_rows = 100
user_ids = [fake.unique.uuid4() for _ in range(num_rows)]
session_ids = [fake.unique.uuid4() for _ in range(num_rows)]
dates = [fake.date_this_year() for _ in range(num_rows)]
start_times = [fake.time() for _ in range(num_rows)]
end_times = [fake.time() for _ in range(num_rows)]
sections = np.random.choice(['Calendario', 'Tareas', 'Notificaciones', 'Configuración'], num_rows)
events = np.random.choice(['Ver', 'Editar', 'Crear'], num_rows)
costumization = np.random.choice(['BackGround_image', 'ChangeColor_Box', 'user_Icon'], num_rows)

# Calcular duraciones de las sesiones y el tiempo en cada sección
durations = np.random.randint(5, 120, num_rows)  # Duración de sesión entre 5 y 120 minutos
time_in_section = np.random.randint(1, durations)  # Tiempo en la sección no puede ser mayor que la duración de la sesión
interactions = np.random.randint(1, 20, num_rows)  # Número de interacciones por sesión

# Crear el DataFrame
df = pd.DataFrame({
    'UserID': user_ids,
    'SessionID': session_ids,
    'Fecha': dates,
    'HoraInicio': start_times,
    'HoraFin': end_times,
    'DuracionSesion (minutos)': durations,
    'Seccion': sections,
    'TiempoEnSeccion (minutos)': time_in_section,
    'Interacciones': interactions,
    'Evento': events
})

df.to_excel("bq3.4", index=False)