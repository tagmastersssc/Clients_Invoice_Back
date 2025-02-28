
import XML_Parts.Header
import XML_Parts.UBLExtensions
import XML_Parts.VersionXML
import XML_Parts.AccountingSupplierParty

def Default():
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
xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2     http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd">\
    ')


# Header
# UBLExtensions
# Signature
# VersionXML
# AccountingSupplierParty
# AccountingCustomerParty
# PayTotalLegalMonetaryTotal
# TotalTributos
# InvoiceLine
# End


#Header
Header              = XML_Parts.Header.Header()

#UBLExtensions
InvoiceAuthorization    = "18760000001"     #Numero resolucion DIAN
StartDate               = "2019-01-19"      #Fecha desde, en página habilitacion de la Dian
EndDate                 = "2030-01-19"      #Fecha hasta, en página habilitacion de la Dian
Prefix                  = "SETP"            #Prefijo, en página habilitacion de la Dian
From                    = "990000000"       #Rango desde, en página habilitacion de la Dian
To                      = "995000000"       #Rango hasta, en página habilitacion de la Dian
ProviderID              = "800197268"       #Nit de la compañía que genera la factura
ProviderIDDV            = "4"               #Digito de verificacion del NIT
SoftwareID              = "56f2ae4e-9812-4fad-9255-08fcfcd5ccb0" #Id, en página habilitacion de la Dian
PIN                     = "00001"           #Pin, en página habilitacion de la Dian
SoftwareSecurityCode    = "a8d18e4e5aa00b44a0b1f9ef413ad8215116bd3ce91730d580eaed795c83b5a32fe6f0823abc71400b3d59eb542b7de8" #CAMBIAR, se debe generar con un hash incluyendo el PIN, según documentación
AuthorizationProviderID = "800197268"       #Nit Dian
#Pendiente QR

UBLExtensions       = XML_Parts.UBLExtensions.UBLExtensions(
                        InvoiceAuthorization,
                        StartDate,
                        EndDate,
                        Prefix,
                        From,
                        To,
                        ProviderID,
                        SoftwareID,
                        SoftwareSecurityCode,
                        AuthorizationProviderID
                        )


#Aqui debe ir el bloque de firma

# VersionXML
UBLVersionID                = "UBL 2.1"
CustomizationID             = "10" #09	AIU, 10	Estándar *, 11	Mandatos, 12	Transporte**, 14	Notariios, 15	Compra Divisas, 16	Venta Divisas Tabla 13.1.5.1
ProfileExecutionID          = "2" #1 Prod, 2 pruebas
ID                          = Prefix + From #El From debería estar en un For, para ir aumentando el consecutivo
CUFE                        = "941cf36af62dbbc06f105d2a80e9bfe683a90e84960eae4d351cc3afbe8f848c26c39bac4fbc80fa254824c6369ea694" #Es un hash de varios valores, pendiente 
IssueDate                   = "2019-06-20" #Esto se debe extraer desde una BD, temporal dejar quemado
IssueTime                   = "09:15:23-05:00"
InvoiceTypeCode             = "01" #01	Factura electrónica de Venta, 02	Factura electrónica de venta -exportación, 03	Instrumento electrónico de transmisión – tipo 03, 04	Factura electrónica de Venta - tipo 04, 91	Nota Crédito, 92	Nota Débito, 96	Eventos (ApplicationResponse) Tabla 13.1.3
Note                        = "SETP9900000022019-06-2009:15:23-05:0012600.06012424.01040.00030.0014024.07900508908900108281fc8eac422eba16e22ffd8c6f94b3f40a6e38162c2" #Temporal, no es necesario
DocumentCurrencyCode        = "COP"
LineCountNumeric            = "2" #Número o cantidad de elementos InvoiceLine de la factura
InvoicePeriodStartDate      = "2019-05-01" #Automatizar
InvoicePeriodEndDate        = "2019-05-30" #Automatizar
BillingReference            = "" #Solo para documento con nota credito sacar modelo de generica.xml

VersionXML          = XML_Parts.VersionXML.VersionXML(
                        UBLVersionID,
                        CustomizationID,
                        ProfileExecutionID,
                        ID,
                        CUFE,
                        IssueDate,
                        IssueTime,
                        InvoiceTypeCode,
                        Note,
                        DocumentCurrencyCode,
                        LineCountNumeric,
                        InvoicePeriodStartDate,
                        InvoicePeriodEndDate
                        )

#AccountingSupplierParty
AdditionalAccountID             = "1" # 1	Persona Jurídica y asimiladas, 2	Persona Natural y asimiladas Tabla 13.2.3
IndustryClasificationCode       = "5440" # Corresponde al código de actividad económica CIIU
PartyName                       = ["Nombre Tienda","Establecimiento Principal","DIAN"] #Revisar, de acuerdo a nombre comercial y demás nombres
PartyNameFull                   = ""
for x in PartyName:
    PartyNameXML    =   f"\
         <cac:PartyName>\n\
            <cbc:Name>{x}</cbc:Name>\n\
         </cac:PartyName>\n"
    if x == PartyName[0]:
        PartyNameXML    =   f"<cac:PartyName>\n\
            <cbc:Name>{x}</cbc:Name>\n\
         </cac:PartyName>\n"
    PartyNameFull = PartyNameFull + PartyNameXML
PartyNameFull = PartyNameFull[:PartyNameFull.rfind('\n')]

PhysicalLocationID                              = "11001" #Codigo municipio, tabla 13.4.3, pasar a SQL
PhysicalLocationCityName                        = "Bogotá, D.c. " #Nombre ciudad, tabla 13.4.3, pasar a SQL
PhysicalLocationCountrySubentity                = "Bogotá" # Departamento, tabla 13.4.2, pasar a SQL
PhysicalLocationCountrySubentityCode            = "11" #Codigo departamento, tabla 13.4.2, pasar a SQL
PhysicalLocationAddressLine                     = "Av. #97 - 13" #Informar la dirección, sin ciudad ni departamento
CountryIdentificationCode                       = "CO" 
CountryName                                     = "Colombia"
RegistrationName                                = "DIAN" #Nombre registrado en el RUT
TaxLevelCode                                    = ["O-13","0-15"] #Obligaciones o responsabilidades del contribuyente; incluye el régimen al que pertenece el emisor,  varios ej. O-13;O-15;//// tabla 13.2.6.1 O-13	Gran contribuyente, O-15	Autorretenedor, O-23	Agente de retención IVA, O-47	Régimen simple de tributación, R-99-PN	No aplica – Otros *
TaxLevelCode                                    = ';'.join(TaxLevelCode) + ";"
RegistrationAddressID                           = PhysicalLocationID #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCityName                     = PhysicalLocationCityName #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountrySubentity             = PhysicalLocationCountrySubentity #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountrySubentityCode         = PhysicalLocationCountrySubentityCode #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressAddressLine                  = PhysicalLocationAddressLine #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountryIdentificationCode    = CountryIdentificationCode #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountryName                  = CountryName #Cambiar si la direccion fiscal del emisor es diferente
TaxSchemeID                                     = "01" #Identificador del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *
TaxSchemeName                                   = "IVA" #Nombre del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *

AccountingSupplierParty = XML_Parts.AccountingSupplierParty.AccountingSupplierParty(
                            AdditionalAccountID,
                            IndustryClasificationCode,
                            PartyNameFull,
                            PhysicalLocationID,
                            PhysicalLocationCityName,
                            PhysicalLocationCountrySubentity,
                            PhysicalLocationCountrySubentityCode,
                            PhysicalLocationAddressLine,
                            CountryIdentificationCode,
                            CountryName,
                            RegistrationName,
                            ProviderID,
                            ProviderIDDV,
                            TaxLevelCode,
                            RegistrationAddressID,
                            RegistrationAddressCityName,
                            RegistrationAddressCountrySubentity,
                            RegistrationAddressCountrySubentityCode,
                            RegistrationAddressAddressLine,
                            RegistrationAddressCountryIdentificationCode,
                            RegistrationAddressCountryName,
                            TaxSchemeID,
                            TaxSchemeName
                            )



def CreateXml():
    return(
        Header +
        UBLExtensions +
        VersionXML +
        AccountingSupplierParty
    )
XML = CreateXml()

#Crear factura en XML
f = open("Invoice.xml", "w")
f.write(XML)
f.close()


#Mostrar archivo
f = open("Invoice.xml", "r")
print(f.read())


