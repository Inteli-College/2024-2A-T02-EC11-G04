import base64
import boto3
import io
from PIL import Image

def decode_and_upload(base64_image: str, bucket_name: str, s3_file_name: str):
    try:
        # Decodificando a imagem base64
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Salvando a imagem como PNG em um objeto BytesIO
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)  # Necessário para garantir que o ponteiro está no início do arquivo

        # Criando um cliente S3
        s3_client = boto3.client('s3')

        # Enviando a imagem para o S3
        s3_client.upload_fileobj(
            buffered,  # Arquivo a ser enviado
            bucket_name,  # Nome do bucket
            s3_file_name,  # Nome do arquivo no S3
            ExtraArgs={'ContentType': 'image/png'}  # Especifica o tipo de conteúdo
        )

        print(f"Imagem {s3_file_name} enviada com sucesso para o bucket {bucket_name}")

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

# Exemplo de uso
base64_image = "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"  # Substitua pela sua string base64
bucket_name = "bucket-greench"  # Substitua pelo nome do seu bucket S3
s3_file_name = "imagem.png"  # Nome do arquivo a ser salvo no S3

decode_and_upload(base64_image, bucket_name, s3_file_name)