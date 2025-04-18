from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
from PIL import Image
from io import BytesIO
from app.modelGen import generate_model
# Load API keys from environment variables

router = APIRouter()


def add_white_background(png_base64):
    image_data = base64.b64decode(png_base64)
    image = Image.open(BytesIO(image_data)).convert("RGBA")

    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.paste(image, (0, 0), image)

    # Save with white background
    output = BytesIO()
    background.convert("RGB").save(output, format="PNG")
    return base64.b64encode(output.getvalue()).decode("ascii")

class SketchRequest(BaseModel):
    image_data: str  # Base64-encoded image string from frontend



@router.post("/process-sketch")
async def process_sketch(sketch: SketchRequest):
    """ Process the sketch, refine it with Hugging Face, and generate 3D model using Replicate. """
    try:
        print("Received sketch data")


        img_data = sketch.image_data
        image_data = img_data.split(',')[1]
        white_background_base64 = add_white_background(image_data)
        with open("sketch_output_with_white.png", "wb") as f:
            f.write(base64.b64decode(white_background_base64))


        jsCode = generate_model(white_background_base64)
        
        return {"prompt": jsCode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))