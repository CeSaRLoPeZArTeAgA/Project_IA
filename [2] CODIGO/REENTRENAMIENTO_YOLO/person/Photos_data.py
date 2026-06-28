import os
import cv2
import time
from datetime import datetime

# Obtener el directorio actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Carpeta donde se guardarán las fotos
data_dir = os.path.join(script_dir, "data_own")
os.makedirs(data_dir, exist_ok=True)

# Buscar el siguiente índice disponible para no sobrescribir fotos anteriores
existing_files = [
    f for f in os.listdir(data_dir)
    if f.startswith("foto_") and f.endswith(".jpg")
]

indices = []
for f in existing_files:
    try:
        numero = int(f.split("_")[1])
        indices.append(numero)
    except:
        pass

next_index = max(indices) + 1 if indices else 1

# Activar cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Configuración
intervalo = 2          # segundos
duracion_total = 60   # segundos
cantidad_fotos = duracion_total // intervalo

print("Iniciando captura de fotos...")
print(f"Se guardarán aproximadamente {cantidad_fotos} fotos en: {data_dir}")
print("Presiona 'q' para salir antes de tiempo.")

inicio = time.time()
siguiente_captura = inicio

contador = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo leer el frame de la cámara.")
        break

    # Mostrar cámara en vivo
    cv2.imshow("Camara - Presiona 'q' para Salir", frame)

    tiempo_actual = time.time()

    # Capturar cada 2 segundos
    if tiempo_actual >= siguiente_captura and contador < cantidad_fotos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"foto_{next_index:04d}_{timestamp}.jpg"
        filepath = os.path.join(data_dir, filename)

        cv2.imwrite(filepath, frame)

        print(f"Foto guardada: {filename}")

        next_index += 1
        contador += 1
        siguiente_captura += intervalo

    # Terminar después de 1 minuto
    if tiempo_actual - inicio >= duracion_total:
        print("Captura finalizada.")
        break

    # Salir manualmente con q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Captura interrumpida por el usuario.")
        break

cap.release()
cv2.destroyAllWindows()