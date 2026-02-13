from lxml import etree

# cargar XSD
with open("UBL-CreditNote-2.1.xsd", "rb") as f:
    schema_root = etree.XML(f.read())

schema = etree.XMLSchema(schema_root)

# cargar XML
with open("CreditNote_c14n_Sig.xml", "rb") as f:
    xml_doc = etree.parse(f)

# validar
if schema.validate(xml_doc):
    print("XML válido contra XSD")
else:
    print("XML inválido")
    for error in schema.error_log:
        print(error.message)


