from azure.data.tables import TableServiceClient, TableEntity
import os
from datetime import datetime

connection_string = os.environ.get("CUSTOMCONNSTR_StorageTable")
def TableStorage():
    return (connection_string)
# table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
# table_client = table_service.get_table_client("Documents")

# entity = {
#     "PartitionKey": "Invoice",
#     "RowKey": "INV-00001",
#     "DocumentType": "Invoice",
#     "CUFE": "C123456789",
#     "CustomerID": "900123456",
#     "IssueDate": "2025-10-24",
#     "Status": "Sent",
#     "XmlFileName": "invoices/INV-00001.xml",
#     "PdfFileName": "invoices/INV-00001.pdf",
#     "DianResponse": "Accepted",
#     "CreatedAt": datetime.utcnow().isoformat(),
#     "UpdatedAt": datetime.utcnow().isoformat()
# }

# table_client.create_entity(entity=entity)
# print("Factura almacenada en Table Storage ✅")


