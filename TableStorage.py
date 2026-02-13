from azure.data.tables import TableServiceClient, TableEntity
import os

connection_string = os.environ.get("CUSTOMCONNSTR_StorageTable")

table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client("Documents")


def AddDocument(Data):
#Construir desde GenerateXML el JSON que recibe esta funcion, aqui tener una funcion para agregar, otra para actualizar

    table_client.create_entity(entity=Data)
    print("Factura almacenada en Table Storage ✅")

    return (connection_string)



