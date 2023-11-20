from GUI import GUI
from HAL import HAL
import cv2

# Constantes del control PID (ajusta estos valores según sea necesario)
KP = 0.002  # Término proporcional
KI = 0  # Término integral
KD = 0.01 # Término derivativo

linear_velocity = 5

max_velocity = 6
min_velocity = 2.5
curve_speed_factor = 0.3


prev_error = 0
integral = 0

def calculate_speed_factor(curve_angle):
    # Diseña una función que ajuste la velocidad en función del ángulo de la curva
    # Puedes experimentar con diferentes funciones según tus necesidades
    # Por ejemplo, puedes devolver un valor más bajo para curvas más agresivas
    return max(0.5, 1 - 0.01 * abs(curve_angle))

while True:
    # Obtener la vista desde el punto de vista del agente
    img = HAL.getImage()

    # Procesar la imagen para encontrar la línea roja
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))

    # Obtener los contornos de las líneas
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)

    # Encontrar el centroide de la figura formada por los contornos
    if len(contours) > 0:
        M = cv2.moments(contours[0])
        if M["m00"] != 0:
            cX = M["m10"] / M["m00"]
            cY = M["m01"] / M["m00"]
        else:
            cX, cY = 0, 0

        # Calcular el error desde el centroide hasta el centro de la pantalla
        error = 320 - cX

        # Calcular los términos del control PID
        P = KP * error
        integral += error
        I = KI * integral
        derivative = error - prev_error
        D = KD * derivative

        
        if(cX > 0):
          # Calcular la velocidad angular del agente usando control PID
          angular_velocity = P + I + D
          
          # Calcula el ángulo de la curva
          ellipse = cv2.fitEllipse(max_contour)
          curve_angle = ellipse[2]

          # Ajusta la velocidad en función del ángulo de la curva
          speed_factor = calculate_speed_factor(curve_angle)
          # Calcula la velocidad considerando el límite inferior y la velocidad inicial
          linear_velocity = max(min_velocity, max_velocity * speed_factor * (1 - curve_speed_factor * abs(angular_velocity)))

          # Establecer las velocidades del agente
          HAL.setV(linear_velocity)  # Velocidad hacia adelante constante
          HAL.setW(angular_velocity)

        prev_error = error

    # Mostrar la vista del agente
    GUI.showImage(red_mask)

    # Actualizar el número de pasos
    print('cX: %.2f cY: %.2f linear_velocity: %.2f' % (cX, cY, linear_velocity))