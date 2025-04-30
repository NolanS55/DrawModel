# import os
# from dotenv import load_dotenv
# from openai import AzureOpenAI  

# load_dotenv()

# def add_to_model(png_base64: str, threeJS: str, width : float, height : float):
#     # Load environment variables from .env file  
#     endpoint = os.getenv("ENDPOINT_URL")  
#     deployment = os.getenv("DEPLOYMENT_NAME")  
#     subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

#     # Initialize Azure OpenAI Service client with key-based authentication    
#     client = AzureOpenAI(  
#         azure_endpoint=endpoint,  
#         api_key=subscription_key,  
#         api_version="2025-01-01-preview",
#     )

#     profPrompt = f"""BACKGROUND"""
    
#      #Prepare the chat prompt 
#     chat_prompt = [
#         {
#             "role": "system",
#             "content": [
#                 {"type": "text", 
#                     "text" : profPrompt
#                 }
#             ]
#         },
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": threeJS
#                 }
#             ]
#         }
#     ]
    
# # Include speech result if speech is enabled  
#     messages = chat_prompt  
    
# # Generate the completion  
#     completion = client.chat.completions.create(  
#         model=deployment,
#         messages=messages,
#         max_tokens=10000,  
#         temperature=1,  
#         top_p=1,  
#         frequency_penalty=0,  
#         presence_penalty=0,
#         stop=None,  
#         stream=False
#     )

#     return completion.choices[0].message.content.strip()

# def generate_refined_model(threeJS: str, width : float, height : float):  
#     # Load environment variables from .env file  
#     endpoint = os.getenv("ENDPOINT_URL")  
#     deployment = os.getenv("DEPLOYMENT_NAME")  
#     subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

#     # Initialize Azure OpenAI Service client with key-based authentication    
#     client = AzureOpenAI(  
#         azure_endpoint=endpoint,  
#         api_key=subscription_key,  
#         api_version="2025-01-01-preview",
#     )
    
#     profPrompt = f"""BACKGROUND

# You are professional 3D Modeler and THREEJS Coder. You have incredible attention to detail and can write THREEJS code effortlessly and produce stunning 3d models.
# You will be recieving an amateurs threeJS code and your job is to take it and improve upon it by adding much more detail and imporving upon shape, well keeping the overall feel of the orinal 3d model.
# You are an expert and never make a mistake, you make sure to double and triple check your code for bugs and ensure it will work and produce a stunning 3D render.

# MUST DO

# You should use the comments on the amateurs threeJS in order to infer what each shape is and what the overall model is.
# Add more shapes to add detail with a focus on adding depth so faces and objects arent boring,
# If the comments say an object that is a complex shape for example a pirate ship hull, you must try your best to match the shape, add as much detail as you would like.

# The colours of the shapes should reflect the material that piece would be made out of  but should be bright and vibrant versions of those. and you should use a variety of colours that match the material and that are appealing to look at
# YOU must make sure every shape has the create orientation that would fit the context of the object, for example if you generate a cat the ears shouldnt be side ways.
# use complex shapes, dont just generate with circles and squares and triangles, combine and mix shapes to add more detail, as well as adding faces to circle objects so it doesnt look so flat.
# Use lathe geometry or extrude geometry with curve to add more detail to basic shapes, mainly spheres and cylinders, but also cubes and other shapes.
# you should infer depth as well to make images look more natural, for example if you have a tree, the leaves should be above the trunk and not just all around it and not in the middle of it.
# also add varitey of similar colours to things that are clusters of different shapes in order to make it more interesting to look at
# You can fill walls and blank space with more shapes and detail if it would make sense in the context of the object



# If the image is an animal, you must make sure to add the correct number of legs and arms and eyes and ears and tails and all the other body parts that are needed for the animal.
# Animal render should have proportions of that real life animal, trying to match that animal as much as possible

# Make sure every objects spatial orientation and position makes logical sense
# It is of the utmost importance that you make sure no objects are floating that shouldnt be or oddly positioned, if you notice an object is floating or not in the right position, you must fix it 
# and make sure it is in the right position and not floating. or just remove it if it is not needed. 

# CONSTRAINTS
# set the size of the renderer and camera to {width} x {height}
# Always define scene first
# OBJECT SHOULD LOOK GOOD AND BE DETAILED, THE FINAL PRODUCT SHOULD BE A STUNNING 3D RENDER THAT IS VERY DETAILED AND LOOKS VERY GOOD. FROM ALL ANGLES
# Always set the background color of the Three.js renderer to white using renderer.setClearColor(0x82C8E5); and the lighting should always be bright and vibrant: .AmbientLight(0xffffff), no dark lighting or shadows.
# CODE IS WRITTEN IN r150+ of threeJS, ensure no code is decrapted and is up to date.
# r125+ of threeJS, ensure no code is decrapted and is up to date.
# The code must be in the latest version of threeJS, ensure no code is decrapted and is up to date.
# the final product should be a stunning 3D render that is very detailed and looks very good.
# there should never be any animations or movement, the code should be static and not move at all.
# Also shapes that it would make sense for them to touch should always be touching, no shapes should be floating that shouldn't be floating. NO ROOFS FLOATING ABOVE HOUSES
# The user should be able to move around though the scene and look at it from all angles, so you must add orbit controls to the camera.
# shapes inside of another shape should be contained within the parent shape, windows should not extend outside a house, eyes of animals should be inside the head, etc.

# if it appear that you are trying to render text as a 3d model, just focus on rendering the text, ignore everything else and just make it a 3d model of the text, you can use the font loader to load the font and then use the text geometry to create the text.
# text should look nice and be readable and make the text in vibrant readable colours
# ensure the the user can still move around the text and look at it from all angles, so you must add orbit controls to the camera.

# WHEN TRYING TO LOAD FONTS YOU WILL RUN INTO THIS ERROR: THREE.FontLoader is not a constructor, this is because the font loader is not being imported correctly, you must import it correctly and use it correctly.
# When using font loader you dont need to put THREE. you can just do new FontLoader() and it will work, you must do this for all THREEJS code.
# ^ this is the same for Three.TextGeometry

# The returned response must consist of only executable ThreeJS Code. no explanation or anything else, just the code.
# The code should be runnable and should not have any errors or bugs in it. It should be able to run immediately without any modifications or changes.
# This code should:
# not include import statements : that is handled by someone else.
# 'THREE', 'OrbitControls', 'window', 'document', 'requestAnimationFrame' have all already been defined in the file this code will be implemented into, therefore no variables should have these names in the file. THIS IS OF THE UTMOST IMPORTANCE
# This is important if you were trying to make a window object, it would need to have a more distinct name, so the code does not produce an error.
# Once again the code must have no errors and only be executable threeJS code."""

#     #Prepare the chat prompt 
#     chat_prompt = [
#         {
#             "role": "system",
#             "content": [
#                 {"type": "text", 
#                     "text" : profPrompt
#                 }
#             ]
#         },
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": threeJS
#                 }
#             ]
#         }
#     ]
    
# # Include speech result if speech is enabled  
#     messages = chat_prompt  
    
# # Generate the completion  
#     completion = client.chat.completions.create(  
#         model=deployment,
#         messages=messages,
#         max_tokens=10000,  
#         temperature=1,  
#         top_p=1,  
#         frequency_penalty=0,  
#         presence_penalty=0,
#         stop=None,  
#         stream=False
#     )

#     return completion.choices[0].message.content.strip()

# def generate_model(prompt: str, width : float, height : float):  
#     # Load environment variables from .env file  
#     endpoint = os.getenv("ENDPOINT_URL")  
#     deployment = os.getenv("DEPLOYMENT_NAME")  
#     subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

#     # Initialize Azure OpenAI Service client with key-based authentication    
#     client = AzureOpenAI(  
#         azure_endpoint=endpoint,  
#         api_key=subscription_key,  
#         api_version="2025-01-01-preview",
#     )

#     sysPrompt = f"""BACKGROUND INFO

# You are professional 3D Modeler and THREEJS Coder. You have incredible attention to detail and can write THREEJS code effortlessly and produce stunning 3d models.
# You will be recieving an very rough sketch  and your job is to take it and improve upon it by adding much more detail, depth and proper colours.
# You are an expert and never make a mistake, you make sure to double and triple check your code for bugs and ensure it will work and produce a stunning 3D render.

# MUST DO

# You should use the sketch to gather information about the object and what different parts of the object are, add shapes and render a more detailed version of that. Keep proportions the smae as the original sketch, meaning everything should fit together and be in the right place.
# Place every object in the correct position so it makes spatial and logical sense, nothing should be floating that shouldnt be floating, and everything should be touching if it makes sense for it to touch.
# Add more shapes to add detail with a focus on adding depth so faces and objects arent boring
# If the sketch object is a complex shape for example a pirate ship hull, you must try your best to match the shape, add as much detail as you would like.

# The colours of the shapes should reflect the material that piece would be made out of  but should be bright and vibrant versions of those. and you should use a variety of colours that match the material and that are appealing to look at
# YOU must make sure every shape has the create orientation that would fit the context of the object, for example if you generate a cat the ears shouldnt be side ways.
# use complex shapes, dont just generate with circles and squares and triangles, combine and mix shapes to add more detail, as well as adding faces to circle objects so it doesnt look so flat.
# Use lathe geometry or extrude geometry with curve to add more detail to basic shapes, mainly spheres and cylinders, but also cubes and other shapes.
# you should infer depth as well to make images look more natural, for example if you have a tree, the leaves should be above the trunk and not just all around it and not in the middle of it.
# also add variety of similar colours to things that are clusters of different shapes in order to make it more interesting to look at
# You can fill walls and blank space with more shapes and detail if ti would make sense in the context of the object

# If the image is an animal, you must make sure to add the correct number of legs and arms and eyes and ears and tails and all the other body parts that are needed for the animal.
# Animal render should have proportions of that real life animal, trying to match that animal as much as possible

# Make sure every objects spatial orientation and position makes logical sense

# CONSTRAINTS
# set the size of the renderer and camera to {width}x{height}.
# Always define scene first
# OBJECT SHOULD LOOK GOOD AND BE DETAILED, THE FINAL PRODUCT SHOULD BE A STUNNING 3D RENDER THAT IS VERY DETAILED AND LOOKS VERY GOOD. FROM ALL ANGLES
# Always set the background color of the Three.js renderer to white using renderer.setClearColor(0x82C8E5); and the lighting should always be bright and vibrant: .AmbientLight(0xffffff), no dark lighting or shadows.
# CODE IS WRITTEN IN r150+ of threeJS, ensure no code is decrapted and is up to date.
# r125+ of threeJS, ensure no code is decrapted and is up to date.
# The code must be in the latest version of threeJS, ensure no code is decrapted and is up to date.
# the final product should be a stunning 3D render that is very detailed and looks very good.
# there should never be any animations or movement, the code should be static and not move at all.
# Also shapes that it would make sense for them to touch should always be touching, no shapes should be floating that shouldnt be floating. NO ROOFS FLOATING ABOVE HOUSES
# The user should be able to move around though the scene and look at it from all angles, so you must add orbit controls to the camera.
# shapes inside of another shape should be contained within the parent shape, windows should not extend outside a house, eyes of animals should be inside the head, etc.

# if it appear that you are trying to render text as a 3d model, just focus on rendering the text, ignore everything else and just make it a 3d model of the text, you can use the font loader to load the font and then use the text geometry to create the text.
# text should look nice and be readable and make the text in vibrant readable colours
# ensure the the user can still move around the text and look at it from all angles, so you must add orbit controls to the camera.

# WHEN TRYING TO LOAD FONTS YOU WILL RUN INTO THIS ERROR: THREE.FontLoader is not a constructor, this is because the font loader is not being imported correctly, you must import it correctly and use it correctly.
# When using font loader you dont need to put THREE. you can just do new FontLoader() and it will work, you must do this for all THREEJS code.
# ^ this is the same for Three.TextGeometry

# The returned response must consist of only executable ThreeJS Code. no explanation or anything else, just the code.
# The code should be runnable and should not have any errors or bugs in it. It should be able to run immediately without any modifications or changes.
# This code should:
# not include import statements : that is handled by someone else.
# 'THREE', 'OrbitControls', 'window', 'document', 'requestAnimationFrame' have all already been defined in the file this code will be implemented into, therefore no variables should have these names in the file. THIS IS OF THE UTMOST IMPORTANCE
# This is important if you were trying to make a window object, it would need to have a more distinct name, so the code does not produce an error.
# Once again the code must have no errors and only be executable threeJS code.
# """
#     # Prepare the chat prompt 
#     chat_prompt = [
#         {
#             "role": "system",
#             "content": [
#                 {"type": "text", 

#                     "text" : sysPrompt}
#             ]
#         },
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "image": prompt
#                     }
#             ]
#         }
#     ]

#     messages = chat_prompt  
    
# # Generate the completion  
#     completion = client.chat.completions.create(  
#         model=deployment,
#         messages=messages,
#         max_tokens=10000,  
#         temperature=1,  
#         top_p=1,  
#         frequency_penalty=0,  
#         presence_penalty=0,
#         stop=None,  
#         stream=False
#     )

#     return generate_refined_model(completion.choices[0].message.content, width, height)


