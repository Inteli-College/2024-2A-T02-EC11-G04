from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from rembg import remove
import json
import torch
from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
from PIL import Image
import numpy as np
from contextlib import asynccontextmanager

model = None
feature_extractor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model(model_name="model_segformer")
    yield


app = FastAPI(root_path="/service1", lifespan=lifespan)

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    global model
    global feature_extractor
    if file is None:
        raise HTTPException(status_code=400, detail='Image not Found')

    # Leia a imagem enviada
    image = Image.open(file.file).convert('RGB')

    # Converta a imagem para um formato que `rembg` possa processar
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Use rembg para remover o fundo
    input_bytes = img_byte_arr.read()

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

    # Salva a imagem processada em um buffer de bytes
    img_byte_arr = io.BytesIO()
    overlay_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png"), mask_area_pixels, mask_percentage

def load_model(model_name, feature_extractor_name="nvidia/segformer-b0-finetuned-ade-512-512"):
    global model
    global feature_extractor
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)