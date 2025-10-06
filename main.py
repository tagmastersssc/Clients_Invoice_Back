from fastapi import FastAPI
from GenerateXML import GenerateXML
from models import Request
import uvicorn

app = FastAPI()


@app.post("/GenerateInvoice")
def GenerateInvoice(Request: Request):
    

    GenerateXML(Request,"Invoice")
    mensaje = f"{Request.UBLExtensions.From}"

    return {
        "mensaje": mensaje,
        "datos_recibidos": Request.dict()
    }

@app.post("/GenerateCreditNote")
def GenerateCreditNote(Request: Request):
    

    GenerateXML(Request,"CreditNote")
    mensaje = f"{Request.UBLExtensions.From}"

    return {
        "mensaje": mensaje,
        "datos_recibidos": Request.dict()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)