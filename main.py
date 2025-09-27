from fastapi import FastAPI
from GenerateXML import GenerateXML
from models import Request
import uvicorn

app = FastAPI()


@app.post("/GenerateInvoice")
def generate_invoice(Request: Request):
    
    GenerateXML(Request)
    mensaje = f"{Request.UBLExtensions.From}"

    return {
        "mensaje": mensaje,
        "datos_recibidos": Request.dict()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)