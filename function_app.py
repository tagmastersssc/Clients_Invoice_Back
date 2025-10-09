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


@app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )