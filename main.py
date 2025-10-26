from fastapi import FastAPI,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
import requests
from PIL import Image
import io

Hugging_faces_url="https://sujith2121-civic-clip-fastapi.hf.space/classify"

app=FastAPI(title="CIVIC ISSUE CLASSIFIER PROXY")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ClassificationResponse(BaseModel):
    category:str=Field(default="Not found")
    department:str=Field(default="Not found")


@app.post("/predict",response_model=ClassificationResponse)
async def proxy_predict(image:UploadFile=File(...),description:str=Form(...)):
    image_bytes=await image.read()
    files={"image":(image.filename,image_bytes,image.content_type)}
    data={"description":description}
    resposne=requests.post(Hugging_faces_url,files=files,data=data)
    if resposne.ok:
        result=resposne.json()
        return {
            "category":result.get("category","Unknown"),
            "department":result.get("department","Unknown")

        }
    else:
        return{
            "category":"Error",
            "department":"Error"
        }