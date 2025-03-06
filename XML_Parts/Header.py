
def Header():
    return(
        f'\
<?xml version="1.0" encoding="UTF-8" standalone="no"?> \n\
<Invoice \n\
xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" \n\
xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" \n\
xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" \n\
xmlns:ds="http://www.w3.org/2000/09/xmldsig#" \n\
xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" \n\
xmlns:sts="dian:gov:co:facturaelectronica:Structures-2-1" \n\
xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" \n\
xmlns:xades141="http://uri.etsi.org/01903/v1.4.1#" \n\
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n\
xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2     http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd">\n\
    ')