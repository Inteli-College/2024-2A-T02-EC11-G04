import tensorflow as tf
import os
from PIL import Image, ImageDraw

# Diretório com seus arquivos .tfrecord
tfrecord_dir = "./Forest Analysis.v23i.tfrecord/valid"
output_dir = "./Images2"

# Função para parsear o dataset
def _parse_function(proto):
    feature_description = {
        'image/encoded': tf.io.FixedLenFeature([], tf.string),
        'image/filename': tf.io.FixedLenFeature([], tf.string),
        'image/object/bbox/xmin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/xmax': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymax': tf.io.VarLenFeature(tf.float32),
        'image/object/class/text': tf.io.VarLenFeature(tf.string),
    }
    return tf.io.parse_single_example(proto, feature_description)

def process_tfrecords(tfrecord_files):
    for tfrecord_file in tfrecord_files:
        raw_dataset = tf.data.TFRecordDataset(tfrecord_file)
        parsed_dataset = raw_dataset.map(_parse_function)

        for image_features in parsed_dataset:
            img = tf.image.decode_jpeg(image_features['image/encoded'].numpy())
            img = Image.fromarray(img.numpy())

            # Extraindo bounding boxes e labels
            xmin = image_features['image/object/bbox/xmin'].values.numpy()
            xmax = image_features['image/object/bbox/xmax'].values.numpy()
            ymin = image_features['image/object/bbox/ymin'].values.numpy()
            ymax = image_features['image/object/bbox/ymax'].values.numpy()
            classes = image_features['image/object/class/text'].values.numpy()

            # Convertendo coordenadas normalizadas para pixels
            width, height = img.size
            xmin = (xmin * width).astype(int)
            xmax = (xmax * width).astype(int)
            ymin = (ymin * height).astype(int)
            ymax = (ymax * height).astype(int)

            # Desenhando os bounding boxes na imagem
            draw = ImageDraw.Draw(img)
            for i in range(len(xmin)):
                draw.rectangle([xmin[i], ymin[i], xmax[i], ymax[i]], outline="red", width=2)
                draw.text((xmin[i], ymin[i]), classes[i].decode('utf-8'), fill="red")

            # Salvando a imagem com bounding boxes
            filename = image_features['image/filename'].numpy().decode('utf-8')
            img.save(os.path.join(output_dir, filename))

if __name__ == "__main__":
    tfrecord_files = [os.path.join(tfrecord_dir, file) for file in os.listdir(tfrecord_dir) if file.endswith('.tfrecord')]
    os.makedirs(output_dir, exist_ok=True)
    process_tfrecords(tfrecord_files)
    print("Processamento concluído.")
