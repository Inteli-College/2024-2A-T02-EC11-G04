import cv2
import time
import os

class CaptureHandler:
    def __init__(self, camera_index=0, output_directory=None):
        self.camera_index = camera_index
        self.output_directory = output_directory or os.getenv('OUTPUT_DIRECTORY', 'images')

        # Cria o diretório se não existir
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def generate_image_name(self):
        """
        Gera um nome de arquivo para a imagem com o formato 'IMG_YYYYMMDD-HHMMSS.jpg'.
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_name = f"IMG_{timestamp}.jpg"
        return image_name

    def capture_image(self, width=640, height=480):
        """
        Captura uma imagem da câmera USB de forma síncrona e salva no diretório especificado.
        """
        # Acessa a câmera USB
        cap = cv2.VideoCapture(self.camera_index)
        
        # Verifica se a câmera foi aberta corretamente
        if not cap.isOpened():
            print("Erro: Não foi possível acessar a câmera.")
            return None

        # Define a resolução da imagem
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Captura a imagem
        ret, frame = cap.read()

        if ret:
            # Gerar o nome da imagem com timestamp
            image_name = self.generate_image_name()
            output_path = os.path.join(self.output_directory, image_name)

            try:
                # Salvar a imagem no diretório especificado
                cv2.imwrite(output_path, frame)
                print(f"Imagem salva em: {output_path}")
            except Exception as e:
                print(f"Erro ao salvar a imagem: {e}")
                return None
            finally:
                # Libera a câmera após captura
                cap.release()
                cv2.destroyAllWindows()

            return output_path
        else:
            print("Erro: Falha ao capturar a imagem.")
            cap.release()
            cv2.destroyAllWindows()
            return None