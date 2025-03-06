
import XML_Parts.Header
import XML_Parts.UBLExtensions
import XML_Parts.VersionXML
import XML_Parts.AccountingSupplierParty
import XML_Parts.AccountingCustomerParty
import XML_Parts.PaymentMeans
import XML_Parts.TaxTotal
import XML_Parts.LegalMonetaryTotal
import XML_Parts.InvoiceLine

import hashlib

#Pendiente
#Todo debe llevar dos digitos, desde BD

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
#Pendiente QR

#****UBLExtensions

#Aqui debe ir el bloque de signature
#Signature

ID                          = Prefix + From #El From debería estar en un For, para ir aumentando el consecutivo

#****Signature

# VersionXML
UBLVersionID                = "UBL 2.1"
CustomizationID             = "10" #09	AIU, 10	Estándar *, 11	Mandatos, 12	Transporte**, 14	Notariios, 15	Compra Divisas, 16	Venta Divisas Tabla 13.1.5.1
ProfileExecutionID          = "2" #1 Prod, 2 pruebas
IssueDate                   = "2019-06-20" #Esto se debe extraer desde una BD, temporal dejar quemado
IssueTime                   = "09:15:23-05:00"
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


#Construcción CUFE
CUFE                        = ID + IssueDate + IssueTime + LineExtensionAmount + CodImp1 + ValImp1 + CodImp2 + ValImp2 + CodImp3 + ValImp3 + 
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
                                    SoftwareID,
                                    SoftwareSecurityCode,
                                    AuthorizationProviderID
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


#Mostrar archivo
f = open("Invoice.xml", "r")
print(f.read())


