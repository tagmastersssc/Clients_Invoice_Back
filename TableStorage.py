from azure.data.tables import TableServiceClient
import os

connection_string = "DefaultEndpointsProtocol=https;AccountName=TU_CUENTA;AccountKey=TU_KEY;EndpointSuffix=core.windows.net"

service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = service.get_table_client(table_name="Facturas")




os.environ.get("CUSTOMCONNSTR_StorageTable")