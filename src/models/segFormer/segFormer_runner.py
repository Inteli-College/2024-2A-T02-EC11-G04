import json
import torch
from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
from PIL import Image
import numpy as np

def load_model(model_name, feature_extractor_name="nvidia/segformer-b0-finetuned-ade-512-512"):
    print("carregando o modelo...")
    # Load the model configuration
    with open(f'{model_name}_classes.json', 'r') as f:
        id2label = json.load(f)
    label2id = {v: k for k, v in id2label.items()}

    num_labels = len(id2label)

    # Initialize the feature extractor
    feature_extractor = SegformerFeatureExtractor.from_pretrained(feature_extractor_name)

    # Initialize the model with the correct number of labels
    model = SegformerForSemanticSegmentation.from_pretrained(
        feature_extractor_name,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    # Load the model weights
    model_path = f"{model_name}.pth"
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=True))
    model.eval()  # Set model to evaluation mode

    return model, feature_extractor



def upload_image(image_path):
    print("subindo a imagem para testes...")
    image = Image.open(image_path).convert('RGB')  # Ensure image is in RGB format

    # Prepare the image for inference
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits

    # Resize the logits to the original image size
    upsampled_logits = torch.nn.functional.interpolate(
        logits,
        size=image.size[::-1],  # (height, width)
        mode="bilinear",
        align_corners=False,
    )

    # Get the predicted segmentation map
    predicted_mask = upsampled_logits.argmax(dim=1).squeeze().cpu().numpy()

    # Define a color map for visualization
    color_map = {
        0: (0, 0, 0),  # Background color
        1: (255, 0, 0),  # Foreground color
    }

    # Function to convert the prediction to a visualizable image
    def prediction_to_vis(prediction):
        vis_shape = prediction.shape + (3,)
        vis = np.zeros(vis_shape, dtype=np.uint8)
        for i, c in color_map.items():
            vis[prediction == i] = c
        return Image.fromarray(vis)

    # Visualize the predicted mask
    vis_mask = prediction_to_vis(predicted_mask)

    # Resize vis_mask to match the original image size
    vis_mask = vis_mask.resize(image.size, Image.NEAREST)

    # Convert both images to RGBA mode
    vis_mask = vis_mask.convert("RGBA")
    image = image.convert("RGBA")

    # Blend images
    overlay_img = Image.blend(image, vis_mask, alpha=0.3)

    # Calculating the area of the mask (class 1 in this case)
    mask_area_pixels = np.sum(predicted_mask == 1)
    total_pixels = predicted_mask.size
    mask_percentage = (mask_area_pixels / total_pixels) * 100

    print(f"A área coberta pela máscara é {mask_area_pixels} pixels")
    print(f"Porcentagem da área coberta: {mask_percentage:.2f}%")

    print("retornando a imagem...")
    return overlay_img, mask_area_pixels, mask_percentage


if __name__ == "__main__":
    # Example usage
    model, feature_extractor = load_model(model_name="model_segformer")

    # Run the function to load the model and perform inference
    output_img, mask_area_pixels, mask_percentage = upload_image("Arvore.jpg")
    output_img.save("output_image.png")  # Salva a imagem no formato desejado, por exemplo, PNG

    print("Imagem salva como 'output_image.png'")