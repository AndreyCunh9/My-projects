import pyautogui
import time

# Defina as coordenadas da posição que deseja clicar
x, y = 769, 400  # Altere para a posição desejada

try:
    while True:
        pyautogui.click(x, y)
        time.sleep(0.1)  # Intervalo entre cliques, ajuste conforme necessário
except KeyboardInterrupt:
    print("Script interrompido pelo usuário.")
