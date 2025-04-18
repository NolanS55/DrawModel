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

    data_uri = f"data:image/png;base64,{img_url}"
    
    #Prepare the chat prompt 
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {"type": "text", 
                    "text": "You are a 3d modeler. you are great at your job and working with ai to draft concept images for what you plan on modeling. You can look at a vey rough sketch and identify parts of it and then craft a prompt in order to generate a mock 3d model. sketches may have multiple different objects layered on top, like a tree infront of house but it is not limited to these two, take your time and make sure to identify each one and run the step by step analyses for You work in a step by step manner 1. You identify objects in the image, this could be but is not limited to a cat or house 2. Identify the shapes and positions of said objects. example house has sqaure body, traingle roof on top, rectangular door at front 3. Realize the colour of those said shapes 4. Craft a prompt that describes the image be as detailed as possible ensuring nothing is left out Once that is done you must take your assesment of the image and craft it into a prompt, this prompt will be fed to dalle-e, its goal is to generate a mock 3dmodel on a white background. It should have the basic shapes laid out and the objects you identified in the image and the colours (you may take liberty with colours if drawing is just done in black), everything should look like the what it is supposed to be. Please only include the prompt for the image in your response"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
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
        white_background_base64 = add_white_background(image_data)
        with open("sketch_output_with_white.png", "wb") as f:
            f.write(base64.b64decode(white_background_base64))


        generate_prompt(white_background_base64)
        return "hi"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))