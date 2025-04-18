import os
from dotenv import load_dotenv
import os  
from openai import AzureOpenAI  

load_dotenv()

def generate_refined_model(img_url: str):  
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
    
    #Prepare the chat prompt 
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {"type": "text", 
                    "text": "You are a professional 3d modeler and an expert in THREEJS. You are going to be given an amateur's a THREEJS code, you must take it an make the model more detailed, and more accurate to what it is trying to represent based on comments and context clues. Keep the originally essence of the model but improve upon things like,   making sure shapes are connected properly, detail of objects and adding more complex shapes to accurately display things. Your response should just be the three js code in the same format as the threejs code sent in, ensure the code has no bugs or errors as well, and no import statements, 'THREE', 'OrbitControls', 'window', 'document', 'requestAnimationFrame' have all already been defined, and always make sure the code can be interacted with by the user\n"

                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": img_url
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
        max_tokens=10000,  
        temperature=1,  
        top_p=1,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )

    return completion.choices[0].message.content.strip()