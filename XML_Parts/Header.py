
def Header(Type):
    if(Type     == "Invoice"):
        Header          = "Invoice"
        STS             = "dian:gov:co:facturaelectronica:Structures-2-1"
        HeaderFull      = ""
    elif(Type   == "CreditNote"):
        Header          = "CreditNote"
        STS             = "http://www.dian.gov.co/contratos/facturaelectronica/v1/Structures"
        HeaderFull      = """xmlns:xades="http://uri.etsi.org/01903/v1.3.2#"
                            xmlns:xades141="http://uri.etsi.org/01903/v1.4.1#"
                            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                            xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2 http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-CreditNote-2.1.xsd"
                            """
    elif(Type   == "DebitNote"):
        Header          = "DebitNote"
        STS             = "http://www.dian.gov.co/contratos/facturaelectronica/v1/Structures"
    return(
        f"""<{Header} xmlns="urn:oasis:names:specification:ubl:schema:xsd:{Header}-2"
  xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
  xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
  xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
  xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
  xmlns:sts="{STS}"
  {HeaderFull}>""")