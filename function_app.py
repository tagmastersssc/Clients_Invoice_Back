
import os
import azure.functions as func
from models import RequestInvoice, RequestCreditNote, RequestDebitNote, RequestMetrics
from GenerateXML import GenerateXML
from TableStorage import GetMetricsTable
from OpenAIAPI import CreateInitialResponseAPI, CreateFollowUpResponseAPI


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

@app.route(route="CreateInitialResponse")
def CreateInitialResponse(req: func.HttpRequest) -> func.HttpResponse:
    try:
        Data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        input_text = Data.get("input_text")
        if not input_text:
            return func.HttpResponse(
                "Missing 'input_text' in request body",
                status_code=400
            )
        response = CreateInitialResponseAPI(input_text)
        return func.HttpResponse(
            response.model_dump_json(indent=2),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )

@app.route(route="CreateFollowUpResponse")
def CreateFollowUpResponse(req: func.HttpRequest) -> func.HttpResponse:
    try:
        Data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    try:
        previous_response_id = Data.get("previous_response_id")
        input_messages = Data.get("input_messages")
        if not previous_response_id or not input_messages:
            return func.HttpResponse(
                "Missing 'previous_response_id' or 'input_messages' in request body",
                status_code=400
            )
        response = CreateFollowUpResponseAPI(previous_response_id, input_messages)
        return func.HttpResponse(
            response.model_dump_json(indent=2),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            f"Error interno: {e}",
            status_code=500
        )