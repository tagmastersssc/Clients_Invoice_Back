from azure.data.tables import TableServiceClient
import os
import calendar

connection_string = os.environ.get("CUSTOMCONNSTR_StorageTable")

table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client("Documents")


def AddDocument(Data):
#Construir desde GenerateXML el JSON que recibe esta funcion, aqui tener una funcion para agregar, otra para actualizar

    table_client.create_entity(entity=Data)
    print("Factura almacenada en Table Storage ✅")

    return (connection_string)

def GetMetricsTable(Data):

    _, num_days = calendar.monthrange(int(Data.Year), int(Data.Month))

    TotalInvoices           = sum(1 for _ in table_client.query_entities(f"PartitionKey eq 'Invoice' and Timestamp ge datetime'{Data.Year}-{Data.Month}-01T00:00:00Z' and Timestamp le datetime'{Data.Year}-{Data.Month}-{num_days}T23:59:59Z'"))
    TotalCreditNotes        = sum(1 for _ in table_client.query_entities(f"PartitionKey eq 'CreditNote' and Timestamp ge datetime'{Data.Year}-{Data.Month}-01T00:00:00Z' and Timestamp le datetime'{Data.Year}-{Data.Month}-{num_days}T23:59:59Z'"))
    TotalDebitNotes         = sum(1 for _ in table_client.query_entities(f"PartitionKey eq 'DebitNote' and Timestamp ge datetime'{Data.Year}-{Data.Month}-01T00:00:00Z' and Timestamp le datetime'{Data.Year}-{Data.Month}-{num_days}T23:59:59Z'"))
    TotalValueInvoices      = sum(float(entity["PayableAmount"]) for entity in table_client.query_entities(f"PartitionKey eq 'Invoice' and Timestamp ge datetime'{Data.Year}-{Data.Month}-01T00:00:00Z' and Timestamp le datetime'{Data.Year}-{Data.Month}-{num_days}T23:59:59Z'"))
    TotalValueCreditNotes   = sum(float(entity["PayableAmount"]) for entity in table_client.query_entities(f"PartitionKey eq 'CreditNote' and Timestamp ge datetime'{Data.Year}-{Data.Month}-01T00:00:00Z' and Timestamp le datetime'{Data.Year}-{Data.Month}-{num_days}T23:59:59Z'"))
    TotalValueDebitNotes    = sum(float(entity["PayableAmount"]) for entity in table_client.query_entities(f"PartitionKey eq 'DebitNote' and Timestamp ge datetime'{Data.Year}-{Data.Month}-01T00:00:00Z' and Timestamp le datetime'{Data.Year}-{Data.Month}-{num_days}T23:59:59Z'"))

    Metrics = {
        "TotalInvoices": TotalInvoices,
        "TotalCreditNotes": TotalCreditNotes,
        "TotalDebitNotes": TotalDebitNotes,
        "TotalValueInvoices": TotalValueInvoices,
        "TotalValueCreditNotes": TotalValueCreditNotes,
        "TotalValueDebitNotes": TotalValueDebitNotes
    }

    return (Metrics)

