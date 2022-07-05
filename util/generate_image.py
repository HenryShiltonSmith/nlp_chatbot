import io
import os
import asyncio
import tempfile
import names

from PIL import Image
from thispersondoesnotexist import get_online_person
from io import BytesIO

from util.gender_pred import predict_gender
from pathlib import Path

os.chdir(Path(__file__).parent)

async def generate():
    picture = await get_online_person()  # bytes representation of the image
    image = Image.open(io.BytesIO(picture))
    return image

def generateImage():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    age = "(0, 2)"
        
    while age == "(0, 2)" or age == "(4, 6)" or age == "(8, 12)" or age =="(15, 20)":   
        image = asyncio.run(generate())  # bytes representation of the image

        buf = BytesIO()
        image.save(buf, 'jpeg')

        buf.seek(0)
        image_bytes = buf.read()
        buf.close()    
            
        with tempfile.TemporaryFile(mode="wb",delete=False) as jpg:
            jpg.write(image_bytes)
            name = str(jpg.name)
            prediction_tupple  = predict_gender(name)
            
            pic = Image.open(jpg.name)
            name = str(names.get_first_name(gender=str(prediction_tupple[0]).lower()))
            file_name = name + ".jpg"
            pic.save(file_name)

        age = prediction_tupple[1]
        
        if str(age) == "(0, 2)" or str(age) == "(4, 6)" or str(age) == "(8, 12)" or str(age) == "(15, 20)":
            os.remove(file_name)
            age = "(0, 2)"
        else:
            return str(file_name), name