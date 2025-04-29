from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import bcrypt
import os
from PIL import Image
from io import BytesIO
from app.modelGen import generate_model, add_to_model
# Load API keys from environment variables

router = APIRouter()
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client['DrawServers']
users_collection = db['users']

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class SketchRequest(BaseModel):
    image_data: str
    width : float
    height : float  # Base64-encoded image string from frontend

class SketchAddRequest(BaseModel):
    image_data: str
    threejs_code: str
    width : float
    height : float  # Base64-encoded image string from frontend

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def add_white_background(png_base64):
    # add white background to the image so image is readable by AI
    image_data = base64.b64decode(png_base64)
    image = Image.open(BytesIO(image_data)).convert("RGBA")

    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.paste(image, (0, 0), image)

    # Save with white background
    output = BytesIO()
    background.convert("RGB").save(output, format="PNG")
    return base64.b64encode(output.getvalue()).decode("ascii")


@router.post("/add-to-scene")
async def add_to_scene(sketch: SketchAddRequest):
    """ Add the sketch to the scene. """
    try:
        print("Received sketch data: ", sketch.width, sketch.height)

        # Decode the base64 image data
        img_data = sketch.image_data
        image_data = img_data.split(',')[1]
        white_background_base64 = add_white_background(image_data)

        threeJSCode = sketch.threejs_code

        print("Added white background to the image")

        # Process the image with Hugging Face and Replicate
        jsCode = add_to_model(white_background_base64, threeJSCode, sketch.width, sketch.height)
        
        return {"prompt": jsCode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint for processing the sketch
@router.post("/process-sketch")
async def process_sketch(sketch: SketchRequest):
    """ Process the sketch, refine it with Hugging Face, and generate 3D model using Replicate. """
    try:
        print("Received sketch data: ", sketch.width, sketch.height)


        img_data = sketch.image_data
        image_data = img_data.split(',')[1]
        white_background_base64 = add_white_background(image_data)

        print("Added white background to the image")


        jsCode = generate_model(white_background_base64, sketch.width, sketch.height)
        
        return {"prompt": jsCode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    hashed_pw = hash_password(user.password)
    user_doc = {"email": user.email, "password": hashed_pw}
    result = await users_collection.insert_one(user_doc)

    return {"message": "User registered successfully.", "user_id": str(result.inserted_id)}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    if not verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {"message": "Login successful!"}

