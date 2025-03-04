from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os 
from dotenv import load_dotenv

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

load_dotenv()
key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

def request_content_safety(text: str):
    request = AnalyzeTextOptions(text=text)
    try:
        return client.analyze_text(request)
    except:
        raise HTTPException(status_code=404, detail="API request failed")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    text: str

class ContentResponse(BaseModel):
    hate: float = 0.0
    self_harm: float = 0.0
    sexual: float = 0.0
    violence: float = 0.0

@app.post("/check", response_model=ContentResponse)
async def check_content(request: ContentRequest):
    result = request_content_safety(request.text)

    hate_result = next(item for item in result.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in result.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in result.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in result.categories_analysis if item.category == TextCategory.VIOLENCE)
    
    response = ContentResponse()
    if hate_result:
        response.hate = hate_result.severity
    if self_harm_result:
        response.self_harm = self_harm_result.severity
    if sexual_result:
        response.sexual = sexual_result.severity
    if violence_result:
        response.violence = violence_result.severity

    return response
