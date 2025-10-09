import azure.functions as func
from models import Request
from GenerateXML import GenerateXML


app = func.FunctionApp()

@app.route(route="GenerateInvoice")
def GenerateInvoice(req: func.HttpRequest) -> func.HttpResponse:
    Data = req.get_json()
    RequestObj = Request(**Data)
    GenerateXML(RequestObj,"Invoice")
    return func.HttpResponse(
            str(Data),
            status_code=200
    )

@app.route(route="GenerateCreditNote")
def GenerateCreditNote(req: func.HttpRequest) -> func.HttpResponse:
    Data = req.get_json()
    RequestObj = Request(**Data)
    GenerateXML(RequestObj,"CreditNote")
    return func.HttpResponse(
            str(Data),
            status_code=200
    )