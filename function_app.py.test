import azure.functions as func
from openai import OpenAI

OPENAI_API_KEY = "sk-proj-CplCfI2z9RrpAzElcuDOT3BlbkFJEuqQHYafNQLI7DPUlKbo"
client = OpenAI(api_key=OPENAI_API_KEY)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    message = req.params.get('message')
    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asistente de compras"},
                {"role": "user", "content": "Context: " + "context" + "\n\n Query: " + str(message)}
            ]
        )
    return func.HttpResponse(
            completion.choices[0].message.content,
            status_code=200
    )