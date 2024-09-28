from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from controllers import chatbotcontroller
from fastapi.responses import PlainTextResponse

router = APIRouter()

class Query(BaseModel):
  query : str
  
@router.post('/genrate_embedding')
async def genrate_embedding(file: UploadFile):
  return await chatbotcontroller.genrate_embedding(file)

@router.post('/chatbot', response_class=PlainTextResponse)
def chatbot(query: Query):
  return chatbotcontroller.chatbot(query)