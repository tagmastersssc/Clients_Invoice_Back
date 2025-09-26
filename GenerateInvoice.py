
import XML_Parts.Header
import XML_Parts.UBLExtensions
import XML_Parts.VersionXML
import XML_Parts.AccountingSupplierParty
import XML_Parts.AccountingCustomerParty
import XML_Parts.PaymentMeans
import XML_Parts.TaxTotal
import XML_Parts.LegalMonetaryTotal
import XML_Parts.InvoiceLine
import XML_Parts.Signature
import XML_Parts.GenerateSOAP
import hashlib
import requests
import base64
import zipfile
import os
import uuid
import xml.etree.ElementTree as ET
from lxml import etree
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from xml.dom import minidom


#Pendiente
#Todo debe llevar dos digitos, desde BD
#TaxTotal puede haber varios, que son la suma de TaxSubtotal, TaxSubtotal puede haber varios.

#Header
#****Header

#UBLExtensions
From                    = "990000001"       #Rango desde, en página habilitacion de la Dian
InvoiceNumber           = int(From) + 12
Prefix                  = "SETP"            #Prefijo, en página habilitacion de la Dian
PIN                     = "12345"           #Pin, en página habilitacion de la Dian
ID                      = Prefix + str(InvoiceNumber) #El From debería estar en un For, para ir aumentando el consecutivo
SoftwareID              = "7acba738-2ca7-452c-aeaf-cbc10ddf3614" #Id, en página habilitacion de la Dian
SoftwareSecurityCode    = SoftwareID + PIN + ID
SoftwareSecurityCode    = SoftwareSecurityCode.encode()
SoftwareSecurityCode    = hashlib.sha384(SoftwareSecurityCode).hexdigest()

InvoiceAuthorization    = "18760000001"     #Numero resolucion DIAN
StartDate               = "2019-01-19"      #Fecha desde, en página habilitacion de la Dian
EndDate                 = "2030-01-19"      #Fecha hasta, en página habilitacion de la Dian
To                      = "995000000"       #Rango hasta, en página habilitacion de la Dian
ProviderID              = "901923739"       #Nit de la compañía que genera la factura
ProviderIDDV            = "3"               #Digito de verificacion del NIT
AuthorizationProviderID = "800197268"       #Nit Dian
AuthorizationProviderDV = "4"               #DV Dian
URL                     = "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentKey=" #Cambiar cuando sea prod //Pendiente revisar

#****UBLExtensions

#Signature



p12_path = "CERT/BILAI S.A.S.p12"
password = b"VsQkyWgLqSuZEJoC"
with open(p12_path, "rb") as f:
    p12_data = f.read()
private_key, cert, additional_certs = pkcs12.load_key_and_certificates(
    p12_data, password
)
cert_der                    = cert.public_bytes(Encoding.DER)
digest                      = hashes.Hash(hashes.SHA256())
digest.update(cert_der)
digest_bytes                = digest.finalize()
DigestValuePublicCert       = base64.b64encode(digest_bytes).decode("utf-8")


PublicCertOneLine           = base64.b64encode(cert_der).decode()

CanonicalizationMethod      = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
SignatureMethod             = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
TransformAlgorithm          = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
DigestMethodAlgorithm       = "http://www.w3.org/2001/04/xmlenc#sha256"
DigestMethodAlgorithmPolicy = "http://www.w3.org/2001/04/xmlenc#sha256"
tz                          = timezone(timedelta(hours=-5))
now                         = datetime.now(tz)
SigningTimeFormatted        = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
SigningTimeFormatted        = SigningTimeFormatted[:-2] + ":" + SigningTimeFormatted[-2:]


IssuerName                  = cert.issuer.rfc4514_string()
IssuerName                  = IssuerName.replace("2.5.4.5=", "SERIALNUMBER=")

IssuerSerial                = cert.serial_number
SignPolicyURL               = "https://facturaelectronica.dian.gov.co/politicadefirma/v2/politicadefirmav2.pdf"
DownloadedSignPolicy        = requests.get(SignPolicyURL)
DownloadedSignPolicy.raise_for_status()
DigestValueSigPolicyHash    = base64.b64encode(hashlib.sha256(DownloadedSignPolicy.content).digest()).decode("utf-8")
SignerRole                  = "supplier"


#****Signature

# VersionXML
IssueDate                   = now.strftime("%Y-%m-%d")
IssueTime                   = now.strftime("%H:%M:%S%z")
IssueTime                   = IssueTime[:-2] + ":" + IssueTime[-2:]

UBLVersionID                = "UBL 2.1"
CustomizationID             = "10" #09	AIU, 10	Estándar *, 11	Mandatos, 12	Transporte**, 14	Notariios, 15	Compra Divisas, 16	Venta Divisas Tabla 13.1.5.1
ProfileID                   = "DIAN 2.1: Factura Electrónica de Venta" #Debe cambiar si es nota credito factura etc...
ProfileExecutionID          = "2" #1 Prod, 2 pruebas


InvoiceTypeCode             = "01" #01	Factura electrónica de Venta, 02	Factura electrónica de venta -exportación, 03	Instrumento electrónico de transmisión – tipo 03, 04	Factura electrónica de Venta - tipo 04, 91	Nota Crédito, 92	Nota Débito, 96	Eventos (ApplicationResponse) Tabla 13.1.3
Note                        = "SETP9900000022019-06-2009:15:23-05:0012600.06012424.01040.00030.0014024.07900508908900108281fc8eac422eba16e22ffd8c6f94b3f40a6e38162c2" #Temporal, no es necesario
DocumentCurrencyCode        = "COP"
LineCountNumeric            = "1" #Número o cantidad de elementos InvoiceLine de la factura
InvoicePeriodStartDate      = "2019-05-01" #Automatizar
InvoicePeriodEndDate        = "2019-05-30" #Automatizar
BillingReference            = "" #Solo para documento con nota credito sacar modelo de generica.xml

#****VersionXML          

#AccountingSupplierParty  Grupo de información que definen el obligado a facturar: Emisor de la factura

PhysicalLocationID                              = "11001" #Codigo municipio, tabla 13.4.3, pasar a SQL
PhysicalLocationCityName                        = "Bogotá, D.c. " #Nombre ciudad, tabla 13.4.3, pasar a SQL
PhysicalLocationCountrySubentity                = "Bogotá" # Departamento, tabla 13.4.2, pasar a SQL
PhysicalLocationCountrySubentityCode            = "11" #Codigo departamento, tabla 13.4.2, pasar a SQL
PhysicalLocationAddressLine                     = "Av. #97 - 13" #Informar la dirección, sin ciudad ni departamento
CountryIdentificationCode                       = "CO"
CountryName                                     = "Colombia"

TaxLevelCode                                    = ["O-47"] #Obligaciones o responsabilidades del contribuyente; incluye el régimen al que pertenece el emisor,  varios ej. O-13;O-15;//// tabla 13.2.6.1 O-13	Gran contribuyente, O-15	Autorretenedor, O-23	Agente de retención IVA, O-47	Régimen simple de tributación, R-99-PN	No aplica – Otros *
if len(TaxLevelCode) > 1:
    TaxLevelCode = ';'.join(TaxLevelCode) + ";"
else:
    TaxLevelCode = TaxLevelCode[0]

AdditionalAccountID                             = "1" # 1	Persona Jurídica y asimiladas, 2	Persona Natural y asimiladas Tabla 13.2.3
# IndustryClasificationCode                       = "5440" # Corresponde al código de actividad económica CIIU // al parecer la etiqueta es opcional, pendiente convertir en arreglo, pueden ser varios
PartyName                                       = "BILAI S.A.S" #Nombre comercial del emisor
RegistrationName                                = "BILAI S.A.S" #Nombre registrado en el RUT
RegistrationAddressID                           = PhysicalLocationID #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCityName                     = PhysicalLocationCityName #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountrySubentity             = PhysicalLocationCountrySubentity #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountrySubentityCode         = PhysicalLocationCountrySubentityCode #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressAddressLine                  = PhysicalLocationAddressLine #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountryIdentificationCode    = CountryIdentificationCode #Cambiar si la direccion fiscal del emisor es diferente
RegistrationAddressCountryName                  = CountryName #Cambiar si la direccion fiscal del emisor es diferente
TaxSchemeID                                     = "01" #Identificador del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *
MatriculaMercantil                              = "3930757" # https://www.rues.org.co/buscar/RM/ Nit al final
TaxSchemeName                                   = "IVA" #Nombre del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *
#Contact se eliminó etiqueta

#****AccountingSupplierParty 

#AccountingCustomerParty Grupo con información que definen el Adquiriente

CustomerAdditionalAccountID                             = "2" # 1	Persona Jurídica y asimiladas, 2	Persona Natural y asimiladas Tabla 13.2.3 Nota: Se debe informar el código “2” cuando se trate del consumidor final
CustomerPartyName                                       = "Sergio Gonzalez"
PartyIdentificationType                                 = "13" #tipo de identificación Tabla 13.2.1 si es nit agregar DV y agregar a XML, pendiente
PartyIdentification                                     = "1014262008" # Si es nit, hay que agregar el digito de verificacion
#Elimino bloque PhysicalLocation, documentacion lo marca opcional
#Elimino bloque TaxLevelCode documentacion manda opcional
#Elimino bloque RegistrationAddress documentacion manda opcional
CustomerTaxSchemeID                                     = "ZZ" #Identificador del tributo del adquiriente tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *   ////Consumidor final ZZ
CustomerTaxSchemeName                                   = "No aplica" #Nombre del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica * ////Consumidor final No aplica
CustomerTaxLevelCode                                    = "R-99-PN" #Obligaciones o responsabilidades del contribuyente; incluye el régimen al que pertenece el emisor,  varios ej. O-13;O-15;//// tabla 13.2.6.1 O-13	Gran contribuyente, O-15	Autorretenedor, O-23	Agente de retención IVA, O-47	Régimen simple de tributación, R-99-PN	No aplica – Otros *
#Elimino bloque CorporateRegistrationScheme
#Elimino bloque Contact

#****AccountingCustomerParty 

#Elimino bloque TaxRepresentativeParty documentacion manda opcional
#Elimino bloque Delivery documentacion manda opcional
#Elimino bloque DeliveryTerms documentacion manda opcional

#PaymentMeans //// Formas de pago , pendiente agregar varios, documentación indica 1..N

PaymentMeansID                  = "1" #Formas de pago tabla 13.3.4.1 // 1	Contado 2	Crédito
PaymentMeansCode                = "91" #Código correspondiente al medio de pago tabla 13.3.4.2
PaymentDueDate                  = "2019-06-30" #Fecha de vencimiento de la factura, Obligatorio si es venta a crédito
#Elimino bloque PaymentID, documentacion manda opcional

#****PaymentMeans 

#Elimino bloque PrepaidPayment, documentacion manda opcional

#TaxTotal Grupo de campos para información totales relacionadas con un tributo

#Despues del POC revisar, pueden haber varios taxtotal, cada uno con varios taxsubtotal, se debe calcular automatico todo lo de adentro

TaxAmount                       = "215.55" #Valor del tributo //// Suma de todos los elementos ../cac:TaxTotal/TaxSubtotal/cbc :TaxAmount
currencyID                      = "COP" #Código de moneda de la transacción tabla 13.3.3
TaxableAmount                   = "1134.45" #Base Imponible sobre la que se calcula el valor del tributo
TaxSubtotalTaxAmount            = "215.55" #Valor del tributo: producto del porcentaje aplicado sobre la base imponible
Percent                         = "19.00" #Tarifa del tributo tabla 13.3.11
TaxSubtotalTaxSchemeID          = "01" #Identificador del tributo
TaxSubtotalTaxSchemeName        = "IVA" #Nombre del tributo

#****TaxTotal

#LegalMonetaryTotal   //// Grupo de campos para información relacionadas con los valores totales aplicables a la factura

LineExtensionAmount             = "1134.45" # Total Valor Bruto antes de tributos: Total valor bruto, suma de los valores brutos de las líneas de la factura.
TaxExclusiveAmount              = "1134.45" # Total Valor Base Imponible : Base imponible para el cálculo de los tributos
TaxInclusiveAmount              = "1350.00" #Total de Valor Bruto más tributos
#AllowanceTotalAmount Descuento Total: Suma de todos los descuentos aplicados a nivel de la factura
#ChargeTotalAmount Cargo Total: Suma de todos los cargos aplicados a nivel de la factura
#PrePaidAmount Anticipo Total: Suma de todos los pagos anticipados
PayableAmount                   = "1350.00" #Valor de la Factura: Valor total de ítems (incluyendo cargos y descuentos a nivel de ítems)+valor tributos + valor cargos – valor descuentos.

#****LegalMonetaryTotal

#InvoiceLine    ////   Grupo de campos para información relacionadas con una línea de factura Cuando se deba facturar un producto y un servicio, se deberán informar en Items(InvoiceLine) por seprado.

#Solo para POC se manda base, después deben generarse varias lineas con todos los prpductos

InvoiceLineID                               = "1" #Número de Línea debe ser incremental
#schemeID Obligatorio cuando se informe el tipo de operación “11”: Valida los posibles valores en el numera . 13.3.12
# Note Información Adicional: Texto libre para añadir información adicional al artículo.
InvoicedQuantity                            = "1.00" #Cantidad del producto o servicio ////Revisar si debe ser solo 1, 
unitCode                                    = "ZZ" #Identificación de la unidad de medida tabla 13.3.6
InvoiceLineLineExtensionAmount              = "1134.45" #Valor total de la línea. //// El Valor Total de la línea es igual al producto de Cantidad x Precio Unidad menos Descuentos más Recargos que apliquen para la línea.
#Elimino FreeOfChargeIndicator no aparece en la documentación
#Elimino Bloque Delivery no aparece en la documentación
#AllowanceCharge Grupo de campos para información relacionadas con un cargo o un descuento //Pueden ser varios
AllowanceChargeID                           = "1"
ChargeIndicator                             = "false" #Indica que el elemento es un Cargo y no un descuento //// Cargo es true, es un Débito aumenta el valor de la item. Descuento es false, un Crédito descuenta el valor del ítem El elemento solamente puede identificar una de las informaciones.
AllowanceChargeReason                       = "Descuento por cliente frecuente" #Texto libre para informar de la razón del descuento.
MultiplierFactorNumeric                     = "33.33" #Porcentaje que aplicar. 
Amount                                      = "6299.94" #Valor total del cargo o descuento
BaseAmount                                  = "18900.00" #Valor Base para calcular el descuento el cargo
#TaxTotal Grupo de campos para información relacionadas con un tributo aplicable a esta línea de la factura
InvoiceLineTaxAmount                        = "215.55" #Valor del tributo //// Suma de todos los elementos ../cac:TaxTotal/TaxSubtotal/cbc :TaxAmount
InvoiceLinecurrencyID                       = "COP" #Código de moneda de la transacción tabla 13.3.3
InvoiceLineTaxableAmount                    = "1134.45" #Base Imponible sobre la que se calcula el valor del tributo
InvoiceLineTaxSubtotalTaxAmount             = "215.55" #Valor del tributo: producto del porcentaje aplicado sobre la base imponible
InvoiceLinePercent                          = "19.00" #Tarifa del tributo tabla 13.3.11
InvoiceLineTaxSubtotalTaxSchemeID           = "01" #Identificador del tributo
InvoiceLineTaxSubtotalTaxSchemeName         = "IVA" #Nombre del tributo
#****TaxTotalInvoiceLine
#Item Grupo de información que describen las características del artículo o servicio
ItemDescription                             = "AV OASYS -2.25 (8.4) LENTE DE CONTATO" #Descripción del artículo o servicio a que se refiere esta línea de la factura
#Elimino bloque SellersItemIdentification , documentacion manda opcional
#Elimino bloque AdditionalItemIdentification , documentacion manda opcional
#Price Grupo de información que describen los precios del artículo o servicio
PriceAmount                                 = "1134.45" #Valor del artículo o servicio
BaseQuantity                                = "1.00" #La cantidad real sobre la cual el precio aplica
BaseQuantityUnitCode                        = "ZZ" #Identificación de la unidad de medida tabla 13.3.6

#****InvoiceLine

CodImp1                                     = "01" #01 Este valor es fijo.
ValImp1                                     = "215.55" #Valor impuesto 01 - IVA    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
CodImp2                                     = "04" #04 Este valor es fijo.
ValImp2                                     = "0.00" #Valor impuesto 04 - Impuesto Nacional al Consumo    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
CodImp3                                     = "03" #03 Este valor es fijo.
ValImp3                                     = "0.00" #Valor impuesto 03 - ICA    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
ClTec                                       = "fc8eac422eba16e22ffd8c6f94b3f40a6e38162c" #Extraer de página de la DIAN // Llave tecnica TechnicalKey

#Construcción CUFE
CUFE                            = ID + IssueDate + IssueTime + LineExtensionAmount + CodImp1 + ValImp1 + CodImp2 + ValImp2 + CodImp3 + ValImp3 + PayableAmount + ProviderID + PartyIdentification + ClTec + ProfileExecutionID
CUFE                            = CUFE.encode()
CUFE                            = hashlib.sha384(CUFE).hexdigest()

Header                          = XML_Parts.Header.Header()

UBLExtensions                   = XML_Parts.UBLExtensions.UBLExtensions(
                                    InvoiceAuthorization,
                                    StartDate,
                                    EndDate,
                                    Prefix,
                                    From,
                                    To,
                                    ProviderID,
                                    ProviderIDDV,
                                    SoftwareID,
                                    SoftwareSecurityCode,
                                    AuthorizationProviderID,
                                    AuthorizationProviderDV,
                                    CUFE,
                                    URL
                                )   

VersionXML                      = XML_Parts.VersionXML.VersionXML(
                                    UBLVersionID,
                                    CustomizationID,
                                    ProfileID,
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

AccountingSupplierParty         = XML_Parts.AccountingSupplierParty.AccountingSupplierParty(
                                    AdditionalAccountID,
                                    PartyName,
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
                                    TaxSchemeName,
                                    Prefix,
                                    MatriculaMercantil
                                )

AccountingCustomerParty         = XML_Parts.AccountingCustomerParty.AccountingCustomerParty(
                                    CustomerAdditionalAccountID,
                                    CustomerPartyName,
                                    PartyIdentificationType,
                                    PartyIdentification,
                                    CustomerTaxSchemeID,
                                    CustomerTaxSchemeName,
                                    CustomerTaxLevelCode
                                )

PaymentMeans                    = XML_Parts.PaymentMeans.PaymentMeans(
                                    PaymentMeansID,
                                    PaymentMeansCode,
                                    PaymentDueDate
                                )

TaxTotal                        = XML_Parts.TaxTotal.TaxTotal(
                                    TaxAmount,
                                    currencyID,
                                    TaxableAmount,
                                    TaxSubtotalTaxAmount,
                                    Percent,
                                    TaxSubtotalTaxSchemeID,
                                    TaxSubtotalTaxSchemeName
                                )

LegalMonetaryTotal              = XML_Parts.LegalMonetaryTotal.LegalMonetaryTotal(
                                    currencyID,
                                    LineExtensionAmount,
                                    TaxExclusiveAmount,
                                    TaxInclusiveAmount,
                                    PayableAmount
                                )

TaxTotalInvoiceLine             = XML_Parts.TaxTotal.TaxTotal(
                                    InvoiceLineTaxAmount,
                                    InvoiceLinecurrencyID,
                                    InvoiceLineTaxableAmount,
                                    InvoiceLineTaxSubtotalTaxAmount,
                                    InvoiceLinePercent,
                                    InvoiceLineTaxSubtotalTaxSchemeID,
                                    InvoiceLineTaxSubtotalTaxSchemeName
                                )

InvoiceLine                     = XML_Parts.InvoiceLine.InvoiceLine(
                                    InvoiceLineID,
                                    InvoicedQuantity,
                                    unitCode,
                                    InvoiceLineLineExtensionAmount,
                                    currencyID,
                                    AllowanceChargeID,
                                    ChargeIndicator,
                                    AllowanceChargeReason,
                                    MultiplierFactorNumeric,
                                    Amount,
                                    BaseAmount,
                                    TaxTotalInvoiceLine,
                                    ItemDescription,
                                    PriceAmount,
                                    BaseQuantity,
                                    BaseQuantityUnitCode
                                )

def CreateXml():
    return(
        Header +
        UBLExtensions +
        VersionXML +
        AccountingSupplierParty +
        AccountingCustomerParty +
        PaymentMeans +
        TaxTotal +
        LegalMonetaryTotal +
        InvoiceLine +
"</Invoice>" #Corregir
    )
XML = CreateXml()

#Crear factura en XML
f = open("Invoice.xml", "w")
f.write(XML)
f.close()

#Canonicalizar XML full, y generar el digest value full
parser = etree.XMLParser(remove_blank_text=True)
doc = etree.fromstring(XML.encode("utf-8"), parser)
InvoiceCanonicalXml         = etree.tostring(doc, method="c14n", exclusive=False)
with open("Invoice_c14n.xml", "wb") as f:
    f.write(InvoiceCanonicalXml)

DigestValueAllC14nInvoice   =  base64.b64encode(hashlib.sha256(InvoiceCanonicalXml).digest()).decode("utf-8")

#Insertar bloque Signature con valores incorrectos
DigestValueKeyInfo              =  ""
DigestValueSignedProperties     =  ""
SignatureValue                  =  ""
UUID                            = str(uuid.uuid4())

KeyInfo                         = f"""<ds:KeyInfo Id="xmldsig-{UUID}-keyinfo" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:xades="http://uri.etsi.org/01903/v1.3.2#"><ds:X509Data><ds:X509Certificate>{PublicCertOneLine}</ds:X509Certificate></ds:X509Data></ds:KeyInfo>"""

SignedProperties                = f"""<xades:SignedProperties Id="xmldsig-{UUID}-signedprops"><xades:SignedSignatureProperties><xades:SigningTime>{SigningTimeFormatted}</xades:SigningTime><xades:SigningCertificate><xades:Cert><xades:CertDigest><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValuePublicCert}</ds:DigestValue></xades:CertDigest><xades:IssuerSerial><ds:X509IssuerName>{IssuerName}</ds:X509IssuerName><ds:X509SerialNumber>{IssuerSerial}</ds:X509SerialNumber></xades:IssuerSerial></xades:Cert></xades:SigningCertificate><xades:SignaturePolicyIdentifier><xades:SignaturePolicyId><xades:SigPolicyId><xades:Identifier>{SignPolicyURL}</xades:Identifier><xades:Description>Política de firma para facturas electrónicas de la República de Colombia.</xades:Description></xades:SigPolicyId><xades:SigPolicyHash><ds:DigestMethod Algorithm="{DigestMethodAlgorithmPolicy}"/><ds:DigestValue>{DigestValueSigPolicyHash}</ds:DigestValue></xades:SigPolicyHash></xades:SignaturePolicyId></xades:SignaturePolicyIdentifier><xades:SignerRole><xades:ClaimedRoles><xades:ClaimedRole>{SignerRole}</xades:ClaimedRole></xades:ClaimedRoles></xades:SignerRole></xades:SignedSignatureProperties></xades:SignedProperties>"""

SignedInfo                      = f"""<ds:SignedInfo><ds:CanonicalizationMethod Algorithm="{CanonicalizationMethod}"/><ds:SignatureMethod Algorithm="{SignatureMethod}"/><ds:Reference Id="xmldsig-{UUID}-ref0" URI=""><ds:Transforms><ds:Transform Algorithm="{TransformAlgorithm}"/></ds:Transforms><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValueAllC14nInvoice}</ds:DigestValue></ds:Reference><ds:Reference URI="#xmldsig-{UUID}-keyinfo"><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValueKeyInfo}</ds:DigestValue></ds:Reference><ds:Reference Type="http://uri.etsi.org/01903#SignedProperties" URI="#xmldsig-{UUID}-signedprops"><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValueSignedProperties}</ds:DigestValue></ds:Reference></ds:SignedInfo>"""

Signature                       = XML_Parts.Signature.Signature(
                                    KeyInfo,
                                    SignedProperties,
                                    SignedInfo,
                                    SignatureValue,
                                    UUID
                                )

Signature = etree.fromstring(Signature.encode("utf-8"), parser)
InvoiceCanonicalXmlTree = etree.fromstring(InvoiceCanonicalXml)

Signature = etree.tostring(
    Signature,
    method="c14n",
    exclusive=False,
    with_comments=False,
    inclusive_ns_prefixes=None
)

# #Añade bloque signature

ns = {"ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"}
InvoiceExtensionContents = InvoiceCanonicalXmlTree.findall(".//ext:ExtensionContent", namespaces=ns)
SecondExtensionContent = InvoiceExtensionContents[1]
SecondExtensionContent.append(etree.fromstring(Signature))


SignatureCanonicalXmlTree = etree.fromstring(Signature)
#Calcular DigestValue KeyInfo y remplazar en factura

ns = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
keyinfo_node = InvoiceCanonicalXmlTree.find(".//ds:KeyInfo", namespaces=ns)

CanonicalKeyInfo = etree.tostring(
    keyinfo_node,
    method="c14n",
    exclusive=False,
    with_comments=False,
    inclusive_ns_prefixes=None
)

DigestValueKeyInfo          = base64.b64encode(hashlib.sha256(CanonicalKeyInfo).digest()).decode("utf-8")
KeyInfoReferenceNode        = InvoiceCanonicalXmlTree.xpath(f".//ds:Reference[@URI='#xmldsig-{UUID}-keyinfo']", namespaces=ns)
DigestNode                  = KeyInfoReferenceNode[0].find("ds:DigestValue", namespaces=ns)
DigestNode.text             = DigestValueKeyInfo

#Calcular DigestValue SignedProperties y remplazar en factura

ns = {"xades": "http://uri.etsi.org/01903/v1.3.2#"}
SignedPropertiesNode = InvoiceCanonicalXmlTree.find(".//xades:SignedProperties", namespaces=ns)
CanonicalSignedProperties = etree.tostring(
    SignedPropertiesNode,
    method="c14n",
    exclusive=False,
    with_comments=False,
    inclusive_ns_prefixes=None
)
DigestValueSignedProperties         = base64.b64encode(hashlib.sha256(CanonicalSignedProperties).digest()).decode("utf-8")
ns = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
SignedPropertiesReferenceNode       = InvoiceCanonicalXmlTree.xpath(f".//ds:Reference[@URI='#xmldsig-{UUID}-signedprops']", namespaces=ns)
DigestNode                          = SignedPropertiesReferenceNode[0].find("ds:DigestValue", namespaces=ns)
DigestNode.text                     = DigestValueSignedProperties


#Canonicalizar SignedInfo

ns = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
SignedInfoNode = InvoiceCanonicalXmlTree.find(".//ds:SignedInfo", namespaces=ns)
SignedInfoCanonicalXml = etree.tostring(
    SignedInfoNode,
    method="c14n",
    exclusive=False,
    with_comments=False,
    inclusive_ns_prefixes=None
)



#Firmar

SignedInfoSignature = private_key.sign(
    SignedInfoCanonicalXml,
    padding.PKCS1v15(),
    hashes.SHA256()
)
SignatureValue = base64.b64encode(SignedInfoSignature).decode("utf-8")

#Cambiar SignatureValue en factura
ns = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
SignatureValueNode                  = InvoiceCanonicalXmlTree.find(".//ds:SignatureValue", namespaces=ns)
SignatureValueNode.text             = SignatureValue

#Buscar nodo signature 
signature_node = InvoiceCanonicalXmlTree.find(".//ds:Signature", namespaces=ns)
xml_str = etree.tostring(signature_node, encoding="utf-8")
clean_node = etree.fromstring(xml_str, parser)


signature_str_ = etree.tostring(clean_node, encoding="utf-8").decode("utf-8")

with open("Invoice_c14n.xml", "r", encoding="utf-8") as f:
    contenido = f.read()

# print(signature_str_)
signed_invoice = contenido.replace(
            "<ext:ExtensionContent></ext:ExtensionContent>", 
            f"<ext:ExtensionContent>{signature_str_}</ext:ExtensionContent>"
        )
signed_invoice = signed_invoice.replace(
            f'<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" xmlns:sts="dian:gov:co:facturaelectronica:Structures-2-1" Id="xmldsig-{UUID}">', 
            f'<ds:Signature Id="xmldsig-{UUID}">'
        )

# NewXmlString = etree.tostring(signed_invoice, encoding="utf-8")

with open("Invoice_c14n_Sig.xml", "w", encoding="utf-8") as f:
    f.write(signed_invoice)

#Mostrarlo bonito ///Eliminar

dom = minidom.parseString(signed_invoice)
pretty_xml = dom.toprettyxml()
with open("invoice_c14n_pretty.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)
#####

#Comprimir XML en Zip
FileToZip = "Invoice_c14n_Sig.xml"
DestinationZip = "Invoice_c14n_Sig.zip"

with zipfile.ZipFile(DestinationZip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(FileToZip, os.path.basename(FileToZip))

with open(DestinationZip, "rb") as f:
    ZipBase64 = base64.b64encode(f.read()).decode("utf-8")

SOAPNow                     = datetime.now(timezone.utc)
TimestampCreated            = SOAPNow.strftime("%Y-%m-%dT%H:%M:%SZ")
TimestampExpires            = (SOAPNow + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
SOAPTo                      = "https://vpfe-hab.dian.gov.co/WcfDianCustomerServices.svc"
ToTag                       = f"""<wsa:To xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:wcf="http://wcf.dian.colombia" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="id-9821734F262768B5271758426395096292">{SOAPTo}</wsa:To>"""
SOAPDigestValue             =  base64.b64encode(hashlib.sha256(ToTag.encode("utf-8")).digest()).decode("utf-8")
SOAPSignedInfo              = f"""<ds:SignedInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:wcf="http://wcf.dian.colombia" xmlns:wsa="http://www.w3.org/2005/08/addressing"><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"><ec:InclusiveNamespaces xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" PrefixList="wsa soap wcf"></ec:InclusiveNamespaces></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"></ds:SignatureMethod><ds:Reference URI="#id-9821734F262768B5271758426395096292"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"><ec:InclusiveNamespaces xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" PrefixList="soap wcf"></ec:InclusiveNamespaces></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></ds:DigestMethod><ds:DigestValue>{SOAPDigestValue}</ds:DigestValue></ds:Reference></ds:SignedInfo>"""
SOAPSignedInfoSignature = private_key.sign(
    SOAPSignedInfo.encode("utf-8"),
    padding.PKCS1v15(),
    hashes.SHA256()
)
SOAPSignatureValue          = base64.b64encode(SOAPSignedInfoSignature).decode("utf-8")
SOAPAction                  = "http://wcf.dian.colombia/IWcfDianCustomerServices/SendBillSync" #Produccion debe ser diferente
TestSetId                   = "47c11080-2700-4010-afc4-19b8d95cbf6a" #Produccion no lo debe tener //SET DE PRUEBAS


GenerateSOAP                       = XML_Parts.GenerateSOAP.GenerateSOAP(
                                    PublicCertOneLine,
                                    TimestampCreated,
                                    TimestampExpires,
                                    SOAPDigestValue,
                                    SOAPSignatureValue,
                                    SOAPAction,
                                    SOAPTo,
                                    DestinationZip,
                                    ZipBase64,
                                    TestSetId
                                    )

SOAPCanonicalXml = etree.tostring(etree.fromstring(GenerateSOAP.encode("utf-8")), method="c14n", exclusive=False)

SOAPheaders = {
    "Content-Type": f'application/soap+xml;charset=UTF-8;action="{SOAPAction}"'
}

response = requests.post(SOAPTo, data=SOAPCanonicalXml.decode("utf-8"), headers=SOAPheaders)
print("Código de respuesta:", response.status_code)
print(response.text)