
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
import hashlib
import requests
import base64
import uuid
from lxml import etree
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

#Pendiente
#Todo debe llevar dos digitos, desde BD
#TaxTotal puede haber varios, que son la suma de TaxSubtotal, TaxSubtotal puede haber varios.

#Header
#****Header

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
AuthorizationProviderDV = "4"               #DV Dian
URL                     = "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentKey=" #Cambiar cuando sea prod

#****UBLExtensions

#Signature

ID                          = Prefix + From #El From debería estar en un For, para ir aumentando el consecutivo

UUID                        = uuid.uuid4()

CanonicalizationMethod      = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
SignatureMethod             = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
TransformAlgorithm          = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
DigestMethodAlgorithm       = "http://www.w3.org/2001/04/xmlenc#sha256"
#Public cert generado con comando openssl en CERT/private_public_key.sh Y quitando encabezado y footer
PublicCert                  = """MIIG6jCCBdKgAwIBAgIIe5xIbRWLEQ0wDQYJKoZIhvcNAQELBQAwgcUxJjAkBgNV
BAMMHVNVQkNBIENBTUVSRklSTUEgQ09MT01CSUEgU0FTMRQwEgYDVQQFEws5MDEz
MTIxMTItNDFAMD4GA1UECww3Q2VydGlmaWNhZG9zIFBhcmEgRmlybWEgRWxlY3Ry
b25pY2EgQ2FtZXJmaXJtYSBDb2xvbWJpYTEgMB4GA1UECgwXQ0FNRVJGSVJNQSBD
T0xPTUJJQSBTQVMxFDASBgNVBAcMC0JPR09UQSBELkMuMQswCQYDVQQGEwJDTzAe
Fw0yNTA0MTUxNDMzNTNaFw0yNjA0MTUxNDMzNTJaMIGtMRkwFwYDVQQJDBBDYWxs
ZSAxNDUgMTNBIDU3MRMwEQYDVQQUEwozMjAzMjkxNjcwMRQwEgYDVQQDDAtCSUxB
SSBTLkEuUzETMBEGA1UEBRMKOTAxOTIzNzM5MzEcMBoGA1UECwwTRmFjdHVyYSBF
bGVjdHJvbmljYTEUMBIGA1UECgwLQklMQUkgUy5BLlMxDzANBgNVBAgMBkJvZ290
YTELMAkGA1UEBhMCQ08wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCk
1YCwwMJ288h8/wE8bDmUZRutDO8W+R61+17STSDlZUFKmFk5eEGorPkLXUAPIpL3
NVK8S5O6MikxCe424cSevtDBAMhvzHnrJQ52I0Xu2cTGVVAo4yvM2RrU590NhAH0
TlSQKGf1Wc/WsEQAH1zK4onuUEXqzxPmRqg5Sd2VJgtp8fSF1asLnrvtC/JCXwsZ
/8oet3w6+mQ5IqLFBIZEVMEG9ECpQgmeyEM5hgqm0r7bLUGXzzvWXlc0+xs/UJCC
DsiePH0BzJoWB8WMNi279pJj+BhRQNdYngV6g59sw8sqVezSlsBB+9MfhABSrQT4
TVcG8kdI8ZGxmJ9qJ145AgMBAAGjggLyMIIC7jAMBgNVHRMBAf8EAjAAMB8GA1Ud
IwQYMBaAFMCPn2uVGVZRNZ5UmMZ3l/0l2PbNMFsGCCsGAQUFBwEBBE8wTTBLBggr
BgEFBQcwAYY/aHR0cDovL3BraWNvbC5jYW1lcmZpcm1hY29sb21iaWEuY28vZWpi
Y2EvcHVibGljd2ViL3N0YXR1cy9vY3NwMBUGA1UdEQQOMAyICisGAQQBgYcuHgsw
JwYDVR0lBCAwHgYIKwYBBQUHAwIGCCsGAQUFBwMEBggrBgEFBQcDATCCAe8GA1Ud
HwEB/wSCAeMwggHfMIIB26CCAQmgggEFhoIBAWh0dHA6Ly9wa2ljb2wuY2FtZXJm
aXJtYWNvbG9tYmlhLmNvL2VqYmNhL3B1YmxpY3dlYi93ZWJkaXN0L2NlcnRkaXN0
P2NtZD1jcmwmaXNzdWVyPUNOJTNEU1VCQ0ErQ0FNRVJGSVJNQStDT0xPTUJJQStT
QVMlMkNTTiUzRDkwMTMxMjExMi00JTJDT1UlM0RDZXJ0aWZpY2Fkb3MrUGFyYStG
aXJtYStFbGVjdHJvbmljYStDYW1lcmZpcm1hK0NvbG9tYmlhJTJDTyUzRENBTUVS
RklSTUErQ09MT01CSUErU0FTJTJDTCUzREJPR09UQStELkMuJTJDQyUzRENPooHL
pIHIMIHFMSYwJAYDVQQDDB1TVUJDQSBDQU1FUkZJUk1BIENPTE9NQklBIFNBUzEL
MAkGA1UEBhMCQ08xFDASBgNVBAcMC0JPR09UQSBELkMuMSAwHgYDVQQKDBdDQU1F
UkZJUk1BIENPTE9NQklBIFNBUzFAMD4GA1UECww3Q2VydGlmaWNhZG9zIFBhcmEg
RmlybWEgRWxlY3Ryb25pY2EgQ2FtZXJmaXJtYSBDb2xvbWJpYTEUMBIGA1UEBRML
OTAxMzEyMTEyLTQwHQYDVR0OBBYEFMHkHAmKYrJTkXi+ypUSGLPYKw0YMA4GA1Ud
DwEB/wQEAwIF4DANBgkqhkiG9w0BAQsFAAOCAQEAqHaGevtkSZQaT220mIMUwn8J
DqMR9LxXj2CRIYWYr2NvpP68K7wN/+2CLdSqHR4/FC84NAAq7oANW+bEwQaTuuAJ
qVfW2TXsPC7M8t1sEb+MemYSbf/zGGXWYOv1KCJAZdqypO918x/hFZuS/uDKSbgD
7CLJBz7ERAhHoOc1yOUcRKTMVZbNwF29rugVIF//MbaLwKPG15V8uk/kFe0nsLQV
QDd8ZudAUVPe1pvDX3AzAfVgMYaYkXzIRsfRpctg4sl0rlTZR+FjLLrVhFAtzs36
LUx9umW2KeoaBr77lbgcPZnVyic0J7YWY9+gMrmPW/dRaaz1IogEMkb1kJyxPA=="""

PrivateCertificate          = """MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCk1YCwwMJ288h8
/wE8bDmUZRutDO8W+R61+17STSDlZUFKmFk5eEGorPkLXUAPIpL3NVK8S5O6Mikx
Ce424cSevtDBAMhvzHnrJQ52I0Xu2cTGVVAo4yvM2RrU590NhAH0TlSQKGf1Wc/W
sEQAH1zK4onuUEXqzxPmRqg5Sd2VJgtp8fSF1asLnrvtC/JCXwsZ/8oet3w6+mQ5
IqLFBIZEVMEG9ECpQgmeyEM5hgqm0r7bLUGXzzvWXlc0+xs/UJCCDsiePH0BzJoW
B8WMNi279pJj+BhRQNdYngV6g59sw8sqVezSlsBB+9MfhABSrQT4TVcG8kdI8ZGx
mJ9qJ145AgMBAAECggEACbblG4WnI4hai7aIeOpbIMb7F2Foj3U/I7Qc2OgSxQvV
1tk26PXDz0N8EF9k8LKcI4jQ+qfs0BxrF3WUxHp2mNesfE0MT9dAZP6NS6K1WTS1
+ocsojxBNWFvyck6DehDW59olgmYY61XXAYnYjQQk/E/j8jLVhTxZ0p8WTDK2yKH
cszTpn/PfU47rGhONuWLpGsM5LRzJRJ+VC0m6rh2um2iZ/lTNoRXpo+qaP3r9dWX
kKfHKqGX4Q+g1VGC3x1MCPqGdtPwJD6r9h6jc1IJTU3dV5v1QRus8jeJz0uZjHwi
6GxZnlT65IXiQ7resARr4zKYrea6zrrqJq1hkCi8wQKBgQDPhDdXnor1p/Ds7ez6
xQvlEkmdz0QFt/s4yFhse4+f1Vs/O/2CI+KaT91JB7n/2cWTlarS2dameP6fKLCf
HnxxUwFnCmtRZoRZEfIqZ5QPThDvzHrF5vN41jCdMoVR7+gnDlQfLiRJc8dTRpp5
QM0Fw7R6zP/jZSst84da1v9JawKBgQDLWGbU43TxZEELX/9L9OjupiDFP3RtZZDd
y6eKmoS2GJMP8x7v8yl4xCVzk3H/T5mJc8o9KfvPg+bpI3dUowtgTjhC8iWL/fxP
VUA9REvOuZCD5jJyot7IsnzxDfHW0Hih5fjCiqoO4oPMM3SAnyMUH0agznQKPEOS
7zLege4r6wKBgDkC1QWAbCLjWcBt+V5HxmXPqWPurnx3uFA4UnqzU5kQz7nGrHYV
j8rfSCcpNUOCO9K5Gq5E5MDlmuZ1ElkU0hF8QXVimmtJo/CoioR14mp2AxcucUhv
k9JN3htB5vjE1V3thNTwI03+vfM2AXhwgiMkSjA2o9KAV+WO80/Uo1wzAoGAeObo
zS8oOtY27kJ3knvdevd/iIe/+8NlrNoHlZtlyLc3yUXuYRCc2dcVxXAnWXvEeDtG
RbOOqsVsJ7YUn1gJzYr0XKmItYGf4LN5bHQM9q7SQ/o8iHhaKc4mB1UZM3XkI66O
h2zWy97WKjV10XvM6Yvm/HmD+Qn3y4c5IZ7zM10CgYAJpWYCQ+IeEIpTu6WBE5+P
5l8jHPC3vx53hN/i+QTr+o9BB68XyhU+9JrL0vhznDLN9Fi4O0/Yynay1ZRJplBs
WIXDV9jIKx9ittM2VIsi+D+4qODcWlvWZZcbdAWqMghBlBzW9BINMgi4itHZuhQv
RUa1f6QohNBmayVZeR79SQ=="""

KeyInfo                     = f"""<ds:KeyInfo Id="{UUID}-KeyInfo" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
<ds:X509Data>
<ds:X509Certificate>
{PublicCert}
</ds:X509Certificate>
</ds:X509Data>
</ds:KeyInfo>"""

tz = timezone(timedelta(hours=-5))
now = datetime.now(tz)
SigningTimeFormatted = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + now.strftime("%z")
SigningTimeFormatted = SigningTimeFormatted[:-2] + ":" + SigningTimeFormatted[-2:]

DigestValuePublicCert           = base64.b64encode(hashlib.sha256(PublicCert.encode("utf-8")).digest()).decode("utf-8")

#Issuer Name generado con comando openssl en CERT/private_public_key.sh hay que ordenarlo despues del comando
IssuerName                  = "C=CO,L=BOGOTA D.C.,O=CAMERFIRMA COLOMBIA SAS,OU=Certificados Para Firma Electronica Camerfirma Colombia,CN=SUBCA CAMERFIRMA COLOMBIA SAS,serialNumber=901312112-4"
IssuerSerial                = "7B9C486D158B110D"
SignPolicyURL               = "https://facturaelectronica.dian.gov.co/politicadefirma/v2/politicadefirmav2.pdf"
DownloadedSignPolicy        = requests.get(SignPolicyURL)
DownloadedSignPolicy.raise_for_status()
DigestValueSigPolicyHash    = base64.b64encode(hashlib.sha256(DownloadedSignPolicy.content).digest()).decode("utf-8")
SignerRole                  = "supplier"

SignedProperties            = f"""<xades:SignedProperties Id="xmldsig-{UUID}-signedprops" xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
<xades:SignedSignatureProperties>
<xades:SigningTime>{SigningTimeFormatted}</xades:SigningTime>
<xades:SigningCertificate>
<xades:Cert>
<xades:CertDigest>
<ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/>
<ds:DigestValue>{DigestValuePublicCert}</ds:DigestValue>
</xades:CertDigest>
<xades:IssuerSerial>
<ds:X509IssuerName>{IssuerName}</ds:X509IssuerName>
<ds:X509SerialNumber>{IssuerSerial}</ds:X509SerialNumber>
</xades:IssuerSerial>
</xades:Cert>
</xades:SigningCertificate>
<xades:SignaturePolicyIdentifier>
<xades:SignaturePolicyId>
<xades:SigPolicyId>
<xades:Identifier>{SignPolicyURL}</xades:Identifier>
</xades:SigPolicyId>
<xades:SigPolicyHash>
<ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/>
<ds:DigestValue>{DigestValueSigPolicyHash}</ds:DigestValue>
</xades:SigPolicyHash>
</xades:SignaturePolicyId>
</xades:SignaturePolicyIdentifier>
<xades:SignerRole>
<xades:ClaimedRoles>
<xades:ClaimedRole>{SignerRole}</xades:ClaimedRole>
</xades:ClaimedRoles>
</xades:SignerRole>
</xades:SignedSignatureProperties>
</xades:SignedProperties>"""



#****Signature

# VersionXML
UBLVersionID                = "UBL 2.1"
CustomizationID             = "10" #09	AIU, 10	Estándar *, 11	Mandatos, 12	Transporte**, 14	Notariios, 15	Compra Divisas, 16	Venta Divisas Tabla 13.1.5.1
ProfileExecutionID          = "2" #1 Prod, 2 pruebas
IssueDate                   = now.strftime("%Y-%m-%d")
IssueTime                   = now.strftime("%H:%M:%S%z")
IssueTime                   = IssueTime[:-2] + ":" + IssueTime[-2:]
InvoiceTypeCode             = "01" #01	Factura electrónica de Venta, 02	Factura electrónica de venta -exportación, 03	Instrumento electrónico de transmisión – tipo 03, 04	Factura electrónica de Venta - tipo 04, 91	Nota Crédito, 92	Nota Débito, 96	Eventos (ApplicationResponse) Tabla 13.1.3
Note                        = "SETP9900000022019-06-2009:15:23-05:0012600.06012424.01040.00030.0014024.07900508908900108281fc8eac422eba16e22ffd8c6f94b3f40a6e38162c2" #Temporal, no es necesario
DocumentCurrencyCode        = "COP"
LineCountNumeric            = "2" #Número o cantidad de elementos InvoiceLine de la factura
InvoicePeriodStartDate      = "2019-05-01" #Automatizar
InvoicePeriodEndDate        = "2019-05-30" #Automatizar
BillingReference            = "" #Solo para documento con nota credito sacar modelo de generica.xml

#****VersionXML          

#AccountingSupplierParty  Grupo de información que definen el obligado a facturar: Emisor de la factura
AdditionalAccountID                             = "1" # 1	Persona Jurídica y asimiladas, 2	Persona Natural y asimiladas Tabla 13.2.3
# IndustryClasificationCode                       = "5440" # Corresponde al código de actividad económica CIIU // al parecer la etiqueta es opcional, pendiente convertir en arreglo, pueden ser varios
PartyName                                       = "Nombre Tienda" #Nombre comercial del emisor
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
#CorporateRegistrationScheme se eliminó etiqueta
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
#Elimino bloque CorporateRegistrationScheme
#Elimino bloque Contact

#****AccountingCustomerParty 

#Elimino bloque TaxRepresentativeParty documentacion manda opcional
#Elimino bloque Delivery documentacion manda opcional
#Elimino bloque DeliveryTerms documentacion manda opcional

#PaymentMeans //// Formas de pago , pendiente agregar varios, documentación indica 1..N

PaymentMeansID                  = "2" #Formas de pago tabla 13.3.4.1 // 1	Contado 2	Crédito
PaymentMeansCode                = "41" #Código correspondiente al medio de pago tabla 13.3.4.2
PaymentDueDate                  = "2019-06-30" #Fecha de vencimiento de la factura, Obligatorio si es venta a crédito
#Elimino bloque PaymentID, documentacion manda opcional

#****PaymentMeans 

#Elimino bloque PrepaidPayment, documentacion manda opcional

#TaxTotal Grupo de campos para información totales relacionadas con un tributo
#Despues del POC revisar, pueden haber varios taxtotal, cada uno con varios taxsubtotal, se debe calcular automatico todo lo de adentro

TaxAmount                       = "0.00" #Valor del tributo //// Suma de todos los elementos ../cac:TaxTotal/TaxSubtotal/cbc :TaxAmount
currencyID                      = "COP" #Código de moneda de la transacción tabla 13.3.3
TaxableAmount                   = "0.00" #Base Imponible sobre la que se calcula el valor del tributo
TaxSubtotalTaxAmount            = "0.00" #Valor del tributo: producto del porcentaje aplicado sobre la base imponible
Percent                         = "0.00" #Tarifa del tributo tabla 13.3.11
TaxSubtotalTaxSchemeID          = "03" #Identificador del tributo
TaxSubtotalTaxSchemeName        = "ICA" #Nombre del tributo

#****TaxTotal

#LegalMonetaryTotal   //// Grupo de campos para información relacionadas con los valores totales aplicables a la factura

LineExtensionAmount             = "12600.06" # Total Valor Bruto antes de tributos: Total valor bruto, suma de los valores brutos de las líneas de la factura.
TaxExclusiveAmount              = "12787.56" # Total Valor Base Imponible : Base imponible para el cálculo de los tributos
TaxInclusiveAmount              = "15024.07" #Total de Valor Bruto más tributos
#AllowanceTotalAmount Descuento Total: Suma de todos los descuentos aplicados a nivel de la factura
#ChargeTotalAmount Cargo Total: Suma de todos los cargos aplicados a nivel de la factura
#PrePaidAmount Anticipo Total: Suma de todos los pagos anticipados
PayableAmount                   = "15024.07" #Valor de la Factura: Valor total de ítems (incluyendo cargos y descuentos a nivel de ítems)+valor tributos + valor cargos – valor descuentos.

#****LegalMonetaryTotal

#InvoiceLine    ////   Grupo de campos para información relacionadas con una línea de factura Cuando se deba facturar un producto y un servicio, se deberán informar en Items(InvoiceLine) por seprado.
#Solo para POC se manda base, después deben generarse varias lineas con todos los prpductos

InvoiceLineID                               = "1" #Número de Línea debe ser incremental
#schemeID Obligatorio cuando se informe el tipo de operación “11”: Valida los posibles valores en el numera . 13.3.12
# Note Información Adicional: Texto libre para añadir información adicional al artículo.
InvoicedQuantity                            = "1.000000" #Cantidad del producto o servicio ////Revisar si debe ser solo 1, 
unitCode                                    = "EA" #Identificación de la unidad de medida tabla 13.3.6
InvoiceLineLineExtensionAmount              = "12600.06" #Valor total de la línea. //// El Valor Total de la línea es igual al producto de Cantidad x Precio Unidad menos Descuentos más Recargos que apliquen para la línea.
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
InvoiceLineTaxAmount                        = "2394.01" #Valor del tributo //// Suma de todos los elementos ../cac:TaxTotal/TaxSubtotal/cbc :TaxAmount
InvoiceLinecurrencyID                       = "COP" #Código de moneda de la transacción tabla 13.3.3
InvoiceLineTaxableAmount                    = "12600.06" #Base Imponible sobre la que se calcula el valor del tributo
InvoiceLineTaxSubtotalTaxAmount             = "2394.01" #Valor del tributo: producto del porcentaje aplicado sobre la base imponible
InvoiceLinePercent                          = "19.00" #Tarifa del tributo tabla 13.3.11
InvoiceLineTaxSubtotalTaxSchemeID           = "03" #Identificador del tributo
InvoiceLineTaxSubtotalTaxSchemeName         = "ICA" #Nombre del tributo
#****TaxTotalInvoiceLine
#Item Grupo de información que describen las características del artículo o servicio
ItemDescription                             = "AV OASYS -2.25 (8.4) LENTE DE CONTATO" #Descripción del artículo o servicio a que se refiere esta línea de la factura
#Elimino bloque SellersItemIdentification , documentacion manda opcional
#Elimino bloque AdditionalItemIdentification , documentacion manda opcional
#Price Grupo de información que describen los precios del artículo o servicio
PriceAmount                                 = "18900.00" #Valor del artículo o servicio
BaseQuantity                                = "1.000000" #La cantidad real sobre la cual el precio aplica
BaseQuantityUnitCode                        = "EA" #Identificación de la unidad de medida tabla 13.3.6

#****InvoiceLine

CodImp1                                     = "01" #01 Este valor es fijo.
ValImp1                                     = "0.00" #Valor impuesto 01 - IVA    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
CodImp2                                     = "04" #04 Este valor es fijo.
ValImp2                                     = "0.00" #Valor impuesto 04 - Impuesto Nacional al Consumo    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
CodImp3                                     = "03" #03 Este valor es fijo.
ValImp3                                     = "0.00" #Valor impuesto 03 - ICA    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
ClTec                                       = "" #Extraer de página de la DIAN // Clave tecnica // pendiente

#Construcción CUFE
CUFE                        = ID + IssueDate + IssueTime + LineExtensionAmount + CodImp1 + ValImp1 + CodImp2 + ValImp2 + CodImp3 + ValImp3 + PayableAmount + ProviderID + PartyIdentification + ClTec + ProfileExecutionID
CUFE                        = CUFE.encode()
CUFE                        = hashlib.sha384(CUFE).hexdigest()

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
                                    ID,
                                    PartyIdentification,
                                    IssueDate,
                                    PayableAmount,
                                    CUFE,
                                    URL
                                )   

VersionXML                      = XML_Parts.VersionXML.VersionXML(
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
                                    TaxSchemeName
                                )

AccountingCustomerParty         = XML_Parts.AccountingCustomerParty.AccountingCustomerParty(
                                    CustomerAdditionalAccountID,
                                    CustomerPartyName,
                                    PartyIdentificationType,
                                    PartyIdentification,
                                    CustomerTaxSchemeID,
                                    CustomerTaxSchemeName
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

#Canonicalizar XML full, generar en Invoice_c14n.xml y generar el digest value full

InvoiceCanonicalXml = etree.tostring(etree.parse("Invoice.xml").getroot(), method="c14n", exclusive=False)

with open("Invoice_c14n.xml", "wb") as f: #Esto se puede eliminar
    f.write(InvoiceCanonicalXml)

DigestValueAllC14nInvoice =  base64.b64encode(hashlib.sha256(InvoiceCanonicalXml).digest()).decode("utf-8")

#Canonicalizar KeyInfo, generar digest value de keyinfo

f = open("KeyInfo.xml", "w")
f.write(KeyInfo)
f.close()

KeyInfoCanonicalXml = etree.tostring(etree.parse("KeyInfo.xml").getroot(), method="c14n", exclusive=False)

with open("KeyInfo_c14n.xml", "wb") as f: #Esto se puede eliminar
    f.write(KeyInfoCanonicalXml)

DigestValueKeyInfo =  base64.b64encode(hashlib.sha256(KeyInfoCanonicalXml).digest()).decode("utf-8")

#Canonicalizar SignedProperties, generar digest value de SignedProperties

f = open("SignedProperties.xml", "w")
f.write(SignedProperties)
f.close()

SignedPropertiesCanonicalXml = etree.tostring(etree.parse("SignedProperties.xml").getroot(), method="c14n", exclusive=False)

with open("SignedProperties_c14n.xml", "wb") as f: #Esto se puede eliminar
    f.write(SignedPropertiesCanonicalXml)

DigestValueSignedProperties =  base64.b64encode(hashlib.sha256(SignedPropertiesCanonicalXml).digest()).decode("utf-8")

SignedInfo                  = f"""<ds:SignedInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
<ds:CanonicalizationMethod Algorithm="{CanonicalizationMethod}"/>
<ds:SignatureMethod Algorithm="{SignatureMethod}"/>
<ds:Reference URI="">
<ds:Transforms>
<ds:Transform Algorithm="{TransformAlgorithm}"/>
</ds:Transforms>
<ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/>
<ds:DigestValue>{DigestValueAllC14nInvoice}</ds:DigestValue>
</ds:Reference>
<ds:Reference URI="#{UUID}-KeyInfo">
<ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/>
<ds:DigestValue>{DigestValueKeyInfo}</ds:DigestValue>
</ds:Reference>
<ds:Reference Type="http://uri.etsi.org/01903#SignedProperties" URI="#xmldsig-{UUID}-signedprops">
<ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/>
<ds:DigestValue>{DigestValueSignedProperties}</ds:DigestValue>
</ds:Reference>
</ds:SignedInfo>"""

#Canonicalizar SignedInfo, generar digest value de SignedInfo

f = open("SignedInfo.xml", "w")
f.write(SignedInfo)
f.close()

SignedInfoCanonicalXml = etree.tostring(etree.parse("SignedInfo.xml").getroot(), method="c14n", exclusive=False)

with open("SignedInfo_c14n.xml", "wb") as f: #Esto se puede eliminar
    f.write(SignedInfoCanonicalXml)

#Firmar

DerDataPrivKey = base64.b64decode(PrivateCertificate)
private_key = serialization.load_der_private_key(
    DerDataPrivKey,
    password=None,
)
SignedInfoSignature = private_key.sign(
    SignedInfoCanonicalXml,
    padding.PKCS1v15(),
    hashes.SHA256()
)
SignatureValue = base64.b64encode(SignedInfoSignature).decode("utf-8")

Signature                       = XML_Parts.Signature.Signature(
                                    KeyInfo,
                                    SignedProperties,
                                    SignedInfo,
                                    SignatureValue
                                )

#Añade bloque signature a factura incial
InvoiceCanonicalXmlTree = etree.fromstring(InvoiceCanonicalXml)
ns = {"ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"}
InvoiceExtensionContents = InvoiceCanonicalXmlTree.findall(".//ext:ExtensionContent", namespaces=ns)
SecondExtensionContent = InvoiceExtensionContents[1]
FragmentSignature = etree.fromstring(Signature)
SecondExtensionContent.append(FragmentSignature)
NewXmlString = etree.tostring(InvoiceCanonicalXmlTree, method="c14n", exclusive=False)

with open("Invoice_c14n.xml", "wb") as f: #Esto se puede eliminar
    f.write(NewXmlString)

#Mostrarlo bonito ///Eliminar
from xml.dom import minidom
dom = minidom.parseString(NewXmlString)
pretty_xml = dom.toprettyxml()
with open("invoice_c14n_pretty.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)
#####






#Mostrar archivo
# f = open("Invoice.xml", "r")
# print(f.read())


#Validate XML
# xsd_main_path = "./Caja-de-herramientas-FE-V1-9/XSD/maindoc/UBL-Invoice-2.1.xsd"

# with open(xsd_main_path, "rb") as f:
#     xsd_doc = etree.parse(f, base_url=xsd_main_path)

# schema = etree.XMLSchema(xsd_doc)

# xml_tree = etree.parse("./Generica.xml")

# if schema.validate(xml_tree):
#     print("✅ XML válido contra el XSD de UBL")
# else:
#     print("❌ XML NO válido")
#     for e in schema.error_log:
#         print(f"Línea {e.line}: {e.message}")