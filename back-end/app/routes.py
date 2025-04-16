from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import os  
import base64
from openai import AzureOpenAI  

# Load API keys from environment variables
load_dotenv()

router = APIRouter()

class SketchRequest(BaseModel):
    image_data: str  # Base64-encoded image string from frontend

def generate_prompt(img_url: str):  
    # Load environment variables from .env file  
    endpoint = os.getenv("ENDPOINT_URL")  
    deployment = os.getenv("DEPLOYMENT_NAME")  
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

    # Initialize Azure OpenAI Service client with key-based authentication    
    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2025-01-01-preview",
    )
    
    print(client)
    #Prepare the chat prompt 
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI tool that takes image descriptions and writes prompts that would allow AI to generate an image. In the description you should ignore like line colour, also the prompt should be for one cohesive image. The description will list out objects and we want to render that into one image with the prompt\n\npeople also might send images, if they do it is your job to then generate prompt for that image, you can ignore things like colour of the lines or the crummyness of the drawing and instead just focus on the details, their position and the object as a whole. If the image is just a black line drawing, you can assume colour, also if there is colours make sure you specify the colour of those objects\n\nthe prompt must also specify a white background"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": img_url
                }
            ]
        }
    ]
    
# Include speech result if speech is enabled  
    messages = chat_prompt  
    
# Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,
        messages=messages,
        max_tokens=800,  
        temperature=1,  
        top_p=1,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )

    print(completion.to_json())  

@router.post("/process-sketch")
async def process_sketch(sketch: SketchRequest):
    """ Process the sketch, refine it with Hugging Face, and generate 3D model using Replicate. """
    try:
        print("Received sketch data")


        img_data = sketch.image_data
        image_data = img_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # Now encode it back to base64, ready to send to Azure
        encoded_image = base64.b64encode(image_bytes).decode('ascii')

        generate_prompt(encoded_image)
        return "hi"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def image_to_base64(image: Image) -> str:
    """ Convert image to base64 string for API submission. """
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')