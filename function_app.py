import azure.functions as func
from models import RequestInvoice, RequestCreditNote, RequestDebitNote, RequestMetrics
from GenerateXML import GenerateXML
from TableStorage import GetMetricsTable


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
        RequestObj = RequestInvoice(**Data)
        GenerateXMLResponse = GenerateXML(RequestObj, "Invoice")
        return func.HttpResponse(
            str(GenerateXMLResponse),
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
        RequestObj = RequestCreditNote(**Data)
        GenerateXMLResponse = GenerateXML(RequestObj, "CreditNote")
        return func.HttpResponse(
            str(GenerateXMLResponse),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )

@app.route(route="GenerateDebitNote")
def GenerateDebitNote(req: func.HttpRequest) -> func.HttpResponse:
    try:
        Data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        RequestObj = RequestDebitNote(**Data)
        GenerateXMLResponse = GenerateXML(RequestObj, "DebitNote")
        return func.HttpResponse(
            str(GenerateXMLResponse),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )
    
@app.route(route="GetMetrics")
def GetMetrics(req: func.HttpRequest) -> func.HttpResponse:
    try:
        Data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        RequestObj = RequestMetrics(**Data)
        Metrics = GetMetricsTable(RequestObj)
        return func.HttpResponse(
            str(Metrics),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )