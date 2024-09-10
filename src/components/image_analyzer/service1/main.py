from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from rembg import remove

app = FastAPI(root_path="/service1")

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    if file is None:
        raise HTTPException(status_code=400, detail='Image not Found')

    # Leia a imagem enviada
    image = Image.open(file.file)

    # Converta a imagem para um formato que `rembg` possa processar
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Use rembg para remover o fundo
    input_bytes = img_byte_arr.read()
    output_bytes = remove(input_bytes)

    # Converta o resultado de volta para uma imagem
    output_img = Image.open(io.BytesIO(output_bytes))

    # Salva a imagem processada em um buffer de bytes
    img_byte_arr = io.BytesIO()
    output_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)