import os
from dotenv import load_dotenv
import os  
from openai import AzureOpenAI  
from app.prompt_gen import generate_refined_model

load_dotenv()

def generate_model(prompt: str):  
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
    
    # Prepare the chat prompt 
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {"type": "text", 
                "text": "You are a professional 3d modeler and an expert in THREEJS. Your job is to take image and to write THREEJS code which transforms that image into a beautiful and interactive 3D model. You never make a mistake and your response will only consist of executable THREEJS. You must guarantee that there are no bugs or errors in the code, do not try to create THREE.CurvedGeometry.\\\\n\\\\nThe images you get will be based on 2d sketches, they will specify that it is a 3d model as well as include details regarding\\\\n\\\\n1. Colour : Make sure the colours are as accurate as possible for each part of the model\\\\n2. Shape : Each part of the models shape will be specified and from that you must construct the accurate THREEJS code to ensure those shapes work, anything that is natural, bushes, shrubs etc should use a bunch of shapes to look as natural as possible and add more texture to the overall shape\\\\n3. Position : The positions of each piece of the model will also be said, make sure every shape is in the correct position.\\\\n\\\\nEXCEMPTIONS:\\\\n\\\\nIF an object is listed that is a real life object, you may take liberty with things like shape and proportion, while still trying to keep it close to the description in terms of colour.\\\\n\\\\nIf the position of something is not included for whatever reason please use logical thinking to ensure you place that piece in the right location. AN EXAMPLE : The prompt could say the house had a triangular roof but not where. IT would be okay for you to assume that the roof was on top of the house.\\\\n\\\\nNext if certain objects shapes are describe in a simple manner, you may make an attempt to add more detail to those shapes, in order to make them more life like and interesting, KEEP IT ACCURATE TO REAL LIFE THO. AN EXAMPLE : A bush may be described as a round object but In this case it would be okay to add more shapes to it to make it appear more bush like. Finally, Whenever you place a new shape or object specify what that is supposed to be within the context of the image in a comment above it, also specify where it should be\\\\n\\\\nPlease return only runnable THREEJS CODE IN YOUR response as this code will be ran immediately after you return it. DO NOT INCLUDE ANY IMPORTS ALSO 'THREE', 'OrbitControls', 'window', 'document', 'requestAnimationFrame' have all already been defined, and always make sure the code can be interacted with by the user\n"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "image": prompt
                    }
            ]
        }
    ]

    messages = chat_prompt  
    
# Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,
        messages=messages,
        max_tokens=5000,  
        temperature=1,  
        top_p=1,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )

    return generate_refined_model(completion.choices[0].message.content)


