import cv2
import numpy as np
import glob
import os

def extract_bounding_boxes(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detectar bordas
    edges = cv2.Canny(gray, 50, 150)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append([x, y, x+w, y+h])
    
    return boxes

def process_images(image_dir, output_dir):
    image_paths = glob.glob(os.path.join(image_dir, "*.jpg"))
    for image_path in image_paths:
        boxes = extract_bounding_boxes(image_path)
        base_name = os.path.basename(image_path)
        txt_path = os.path.join(output_dir, os.path.splitext(base_name)[0] + '.txt')
        with open(txt_path, 'w') as f:
            for box in boxes:
                # Normalizando as coordenadas
                f.write(f'tree-top {box[0]} {box[1]} {box[2]} {box[3]}\n')

# Defina o diretório das imagens e o diretório de saída
image_dir = "./Images2"
output_dir = "./Annotations2"
os.makedirs(output_dir, exist_ok=True)

process_images(image_dir, output_dir)
