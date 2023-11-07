from GUI import GUI
from HAL import HAL
import cv2

# Constantes del control PID (ajusta estos valores según sea necesario)
KP = 0.003  # Término proporcional
KI = 0  # Término integral
KD = 0 # Término derivativo

linear_velocity = 3

prev_error = 0
integral = 0

while True:
    # Obtener la vista desde el punto de vista del agente
    img = HAL.getImage()

    # Procesar la imagen para encontrar la línea roja
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))

    # Obtener los contornos de las líneas
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
  
          # Establecer las velocidades del agente
          HAL.setV(linear_velocity)  # Velocidad hacia adelante constante
          HAL.setW(angular_velocity)

        prev_error = error

    # Mostrar la vista del agente
    GUI.showImage(red_mask)

    # Actualizar el número de pasos
    print('cX: %.2f cY: %.2f' % (cX, cY))
