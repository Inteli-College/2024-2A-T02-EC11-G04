import base64
import json
import os
import json
import torch
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
from PIL import Image
import numpy as np
import base64

from .logger import Logger

_logger=Logger(logger_name=__name__)._get_logger()


class ImageHandler:
    """Class for image compression"""

    def __init__(self, model_name, output_json="metadata.json", feature_extractor_name="nvidia/segformer-b0-finetuned-ade-512-512", device=None) -> None:
        _logger.info("Image handler initialized.")
        self.model_name = model_name
        self.output_json = output_json
        self.feature_extractor_name = feature_extractor_name
        
        # Definir o dispositivo (GPU se disponível, caso contrário CPU)
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Carregar o modelo e o feature extractor
        self.model, self.feature_extractor = self.load_model()

    def load_model(self):
        """
        Carregar o modelo Segformer e o feature extractor.
        """
        # Definir o diretório do script para ajudar a carregar arquivos corretamente
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Caminho para o arquivo JSON de classes
        json_path = os.path.join(script_dir, '../models', f'{self.model_name}_classes.json')

        # Carregar o mapeamento de classes
        with open(json_path, 'r') as f:
            id2label = json.load(f)

        label2id = {v: k for k, v in id2label.items()}
        num_labels = len(id2label)

        # Inicializar o feature extractor
        feature_extractor = SegformerImageProcessor.from_pretrained(self.feature_extractor_name)

        # Inicializar o modelo Segformer com as classes carregadas
        model = SegformerForSemanticSegmentation.from_pretrained(
            self.feature_extractor_name,
            num_labels=num_labels,
            id2label=id2label,
            label2id=label2id,
            ignore_mismatched_sizes=True,  # Ignorar tamanhos incompatíveis
        )

        # Caminho para o arquivo de pesos do modelo
        model_path = os.path.join(script_dir, '../models', f"{self.model_name}.pth")
        # Carregar os pesos do modelo treinado
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
        model.eval()  # Colocar o modelo no modo de avaliação

        _logger.info("Model loaded.")

        return model, feature_extractor

    def process_image_fr(self, image_path):
        """
        Processa a imagem e retorna a máscara de segmentação, área e percentual de cobertura.
        """
        # Carregar a imagem e convertê-la para RGB
        image = Image.open(image_path).convert('RGB')

        # Preparar a imagem para o modelo
        inputs = self.feature_extractor(images=image, return_tensors="pt").to(self.device)

        # Fazer a inferência no modelo
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        # Redimensionar o resultado para o tamanho original da imagem
        upsampled_logits = torch.nn.functional.interpolate(logits, size=image.size[::-1], mode="bilinear", align_corners=False)
        # Previsão final (máscara de segmentação)
        predicted_mask = upsampled_logits.argmax(dim=1).squeeze().cpu().numpy()

        # Geração da visualização da máscara
        vis_mask = self.prediction_to_vis(predicted_mask, image.size)

        # Área coberta pela máscara (classe 1)
        mask_area_pixels = np.sum(predicted_mask == 1)
        mask_percentage = (mask_area_pixels / predicted_mask.size) * 100

        # Salvar a imagem processada e metadados
        metadata = self.save_metadata(image_path, mask_area_pixels, mask_percentage, vis_mask)

        _logger.info("Image Processed.")

        return metadata

    def save_metadata(self, image_path, mask_area_pixels, mask_percentage, vis_mask):
        """
        Salva os metadados da imagem processada junto com a imagem original em Base64.
        """
        # Remover a extensão do nome da imagem
        image_name_without_extension = os.path.splitext(os.path.basename(image_path))[0]

        # Codificar a imagem original em Base64
        with open(image_path, "rb") as image_file:
            image = image_file.read()
            image_base64 = base64.b64encode(image).decode("utf-8")

        metadata = {
            "image_name": image_name_without_extension,  # Nome sem a extensão
            "mask_area_pixels": int(mask_area_pixels),   # Convertido para int
            "mask_percentage": float(mask_percentage),   # Convertido para float
            "image_base64": image_base64                 # Imagem original em Base64
        }

        # Definir o caminho do arquivo JSON para salvar os metadados no diretório de saída
        output_json_path = os.getenv('OUTPUT_DIRECTORY_2', 'test_json')

        # Salvar os metadados no arquivo JSON no diretório de saída
        with open(output_json_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        _logger.info("Metadata Saved. Path: %s", output_json_path)

        # Retornar os metadados como JSON, sem modificar a estrutura original da função
        return metadata


    def prediction_to_vis(self, prediction, image_size):
        """
        Gera uma visualização da máscara de segmentação.
        """
        # Mapa de cores para visualização (exemplo: classe 0 é preta, classe 1 é vermelha)
        color_map = {0: (0, 0, 0), 1: (255, 0, 0)}
        vis_shape = prediction.shape + (3,)
        vis = np.zeros(vis_shape, dtype=np.uint8)
        for label, color in color_map.items():
            vis[prediction == label] = color

        # Converte o array para uma imagem PIL e ajusta o tamanho da imagem original
        vis_mask = Image.fromarray(vis).resize(image_size, Image.NEAREST)

        _logger.info("Vis Generated.")

        return vis_mask.convert("RGBA")

    def process_image(self, file_path) -> str:
        """Process the image and extract the image in base64 format.

        Args:
            file_path (str): Path to the image file.

        Returns:
            base64: Compressed image in base64 format. 
        """
        metadata = self.process_image_fr(file_path)

        _logger.info("Image Processed.")

        return json.dumps(metadata)
