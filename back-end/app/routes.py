from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import base64
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import replicate

# Load API keys from environment variables
load_dotenv()
HUGGING_FACE_TOKEN = os.getenv('HUG_KEY')
REPLICATE_API_KEY = os.getenv('REPLICATE_KEY')

router = APIRouter()

class SketchRequest(BaseModel):
    image_data: str  # Base64-encoded image string from frontend

@router.post("/process-sketch")
async def process_sketch(sketch: SketchRequest):
    """ Process the sketch, refine it with Hugging Face, and generate 3D model using Replicate. """
    try:
        # Step 1: Decode the sketch image
        img_data = sketch.image_data
        img_bytes = base64.b64decode(img_data.split(",")[1])
        img = Image.open(BytesIO(img_bytes))

        print(img)
        # Step 2: Refine the image using Hugging Face's ControlNet model
        #refined_image_url = await refine_image(img)

        # Step 3: Generate 3D model from refined image using Replicate
        model_data = await generate_3d_model("dinosaur in the woods")
        return model_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def refine_image(image: Image):
    """ Refine the image using Hugging Face's ControlNet model. """
    try:
        headers = {
            'Authorization': f'Bearer {HUGGING_FACE_TOKEN}',
            'Content-Type': 'application/json'
        }
        data = {
            'inputs': image_to_base64(image)
        }
        print(f"Sending data to Hugging Face: {data}")  # Debug the data
        response = requests.post('https://api-inference.huggingface.co/models/lllyasviel/ControlNet-scribble', headers=headers, json=data)
        
        if response.status_code != 200:
            raise ValueError(f"Failed request to Hugging Face. Status code: {response.status_code} Response: {response.text}")

        response.raise_for_status()  # Will raise an error if response is not 2xx
        
        refined_image_url = response.json().get('url')
        if not refined_image_url:
            raise ValueError("Refined image URL not returned from Hugging Face.")
        
        return refined_image_url
    except Exception as e:
        print(f"Error in refine_image: {e}")
        raise HTTPException(status_code=500, detail=f"Error refining image: {str(e)}")

async def generate_3d_model(image_url: str):
    """ Send the refined image to Replicate to generate a 3D model. """
    try:
        print(f"Preparing to send request to Replicate with image_url: {image_url}")
        
        # Setup Replicate client with your API key
        client = replicate.Client(api_token=REPLICATE_API_KEY)
        
        # Example model: "stability-ai/stable-diffusion-3d" (or any 3D model of your choice)
        model = client.models.get("stability-ai/stable-diffusion-3d")
        
        # Print model details for debugging
        print(f"Loaded model: {model}")
        
        # Generate the 3D model based on the refined image URL
        print(f"Sending request to Replicate with the following prompt: {image_url}")
        output = model.predict(prompt=image_url)
        
        # Debug the response from Replicate
        print(f"Received response from Replicate: {output}")
        
        if not output:
            raise ValueError("No output returned from Replicate.")
        
        # Assuming 'image' key contains the 3D model URL or data
        if 'image' not in output:
            raise ValueError("No 'image' field in Replicate response. Response: {output}")

        # If successful, return the 3D model URL
        return {"3D_model_url": output['image']}  # Adjust according to the actual response format

    except Exception as e:
        # Capture detailed error information
        print(f"Error in generate_3d_model: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating 3D model: {str(e)}")

def image_to_base64(image: Image) -> str:
    """ Convert image to base64 string for API submission. """
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')