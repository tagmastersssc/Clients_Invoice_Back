import azure.functions as func
from models import Request
from GenerateXML import GenerateXML


app = func.FunctionApp()

@app.route(route="GenerateInvoice")
def GenerateInvoice(req: func.HttpRequest) -> func.HttpResponse:
    try:
        Data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        RequestObj = Request(**Data)
        GenerateXML(RequestObj, "Invoice")
        return func.HttpResponse(
            str(Data),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )
    

@app.route(route="GenerateCreditNote")
def GenerateCreditNote(req: func.HttpRequest) -> func.HttpResponse:
    try:
        Data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        RequestObj = Request(**Data)
        GenerateXML(RequestObj, "CreditNote")
        return func.HttpResponse(
            str(Data),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )