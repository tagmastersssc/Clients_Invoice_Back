
def Header(Type):
    if(Type     == "Invoice"):
        Header  = "Invoice"
        STS     = "dian:gov:co:facturaelectronica:Structures-2-1"
    elif(Type   == "CreditNote"):
        Header  = "CreditNote"
        STS     = "http://www.dian.gov.co/contratos/facturaelectronica/v1/Structures"
    elif(Type   == "DebitNote"):
        Header  = "DebitNote"
        STS     = "http://www.dian.gov.co/contratos/facturaelectronica/v1/Structures"
    return(
        f"""<{Header} xmlns="urn:oasis:names:specification:ubl:schema:xsd:{Header}-2"
  xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
  xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
  xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
  xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
  xmlns:sts="{STS}">""")