import cv2
import os
import time

# Diretório para salvar as capturas de tela
save_dir = "captures"
os.makedirs(save_dir, exist_ok=True)

# Tempo de captura (em segundos)
capture_interval = 5  # Captura a cada 5 segundos
last_capture_time = time.time()

# Abrir a webcam (use 0 para a webcam padrão, 1 para outra câmera, etc.)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Falha ao capturar imagem da webcam. Reiniciando...")
        cap = cv2.VideoCapture(0)
        continue
    
    # Verificar se já passou o intervalo de captura
    if time.time() - last_capture_time > capture_interval:
        # Salvar a imagem no diretório especificado
        filename = os.path.join(save_dir, f"capture_{time.strftime('%Y%m%d_%H%M%S')}.png")
        cv2.imwrite(filename, frame)
        print(f"Imagem salva em: {filename}")
        last_capture_time = time.time()  # Atualizar o tempo da última captura
    
    # Exibir a imagem ao vivo da webcam
    cv2.imshow('Webcam', frame)
    
    # Verificar se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a webcam e fechar as janelas abertas
cap.release()
cv2.destroyAllWindows()
