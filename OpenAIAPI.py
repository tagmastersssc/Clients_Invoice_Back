import os
from openai import OpenAI

api_key = os.environ.get("APPSETTING_OPENAI_KEY")
base_url = os.environ.get("APPSETTING_OPENAI_ENDPOINT")
model_name = os.environ.get("APPSETTING_OPENAI_DEPLOYMENT_MODEL_NAME")

client = OpenAI(  
  base_url = base_url,
  api_key= api_key
)

def CreateInitialResponseAPI(input_text):
    response = client.responses.create(
        model=model_name,
        input=input_text
    )
    return response

def CreateFollowUpResponseAPI(previous_response_id, input_messages):
    response = client.responses.create(
        model=model_name,
        previous_response_id=previous_response_id,
        input=input_messages
    )
    return response
