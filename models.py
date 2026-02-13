from pydantic import BaseModel

class CreditNote(BaseModel):                        #reduce el valor de una factura o anula una venta#Estos datos deberian venir de buscar en la base de datos
    InvoiceID:                                      str # Numero de factura referenciada
    ResponseCode:                                   str # 1	Devolución parcial de los bienes y/o no aceptación parcial del servicio 2	Anulación de factura electrónica 3	Rebaja  o descuento parcial o total 4	Ajuste de precio 5	Descuento comercial por pronto pago 6	Descuento comercial por volumen de ventas
    Description:                                    str
    CUFE:                                           str
    IssueDate:                                      str

class DebitNote(BaseModel):                         #reduce el valor de una factura o anula una venta#Estos datos deberian venir de buscar en la base de datos
    InvoiceID:                                      str # Numero de factura referenciada
    ResponseCode:                                   str #1	Intereses 2	Gastos por cobrar 3	Cambio del valor 4	Otros
    Description:                                    str
    CUFE:                                           str
    IssueDate:                                      str

class UBLExtensions(BaseModel):
    From:                                           str #"990000000"       #Rango desde, en página habilitacion de la Dian
    Prefix:                                         str #"SETP"            #Prefijo, en página habilitacion de la Dian
    PIN:                                            str #"12345"           #Pin, en página habilitacion de la Dian
    SoftwareID:                                     str #"7acba738-2ca7-452c-aeaf-cbc10ddf3614" #Id, en página habilitacion de la Dian
    InvoiceAuthorization:                           str #"18760000001"     #Numero resolucion DIAN
    StartDate:                                      str #"2019-01-19"      #Fecha desde, en página habilitacion de la Dian
    EndDate:                                        str #"2030-01-19"      #Fecha hasta, en página habilitacion de la Dian
    To:                                             str #"995000000"       #Rango hasta, en página habilitacion de la Dian
    ProviderID:                                     str #"901923739"       #Nit de la compañía que genera la factura
    ProviderIDDV:                                   str #"3"               #Digito de verificacion del NIT
    AuthorizationProviderID:                        str #"800197268"       #Nit Dian
    AuthorizationProviderDV:                        str #"4"               #DV Dian
    URL:                                            str #"https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentKey=" #Cambiar cuando sea prod //Pendiente revisar

class Signature(BaseModel):
    P12Path:                                        str #"CERT/BILAI S.A.S.p12"
    P12Password:                                    str #"VsQkyWgLqSuZEJoC"
    SignPolicyURL:                                  str #"https://facturaelectronica.dian.gov.co/politicadefirma/v2/politicadefirmav2.pdf"
    SignerRole:                                     str #"supplier"

class VersionXML(BaseModel):
    UBLVersionID:                                   str #"UBL 2.1"
    CustomizationID:                                str #"10" Tabla 13.1.5.1 - Invoice // 13.1.5.2 - CreditNote
    ProfileID:                                      str #"DIAN 2.1: Factura Electrónica de Venta" #Debe cambiar si es nota credito factura etc...
    ProfileExecutionID:                             str #"2" #1 Prod, 2 pruebas
    DocumentTypeCode:                               str #"01" #01	Factura electrónica de Venta, 02	Factura electrónica de venta -exportación, 03	Instrumento electrónico de transmisión – tipo 03, 04	Factura electrónica de Venta - tipo 04, 91	Nota Crédito, 92	Nota Débito, 96	Eventos (ApplicationResponse) Tabla 13.1.3
    DocumentCurrencyCode:                           str #"COP" Código de moneda de la transacción tabla 13.3.3
    LineCountNumeric:                               str #"1" #Número o cantidad de elementos InvoiceLine de la factura //Pendiente Calcular automáticamente

class AccountingSupplierParty(BaseModel):
    PhysicalLocationID:                             str #"11001" #Codigo municipio, tabla 13.4.3, pasar a SQL
    PhysicalLocationCityName:                       str #"Bogotá, D.c. " #Nombre ciudad, tabla 13.4.3, pasar a SQL
    PhysicalLocationCountrySubentity:               str #"Bogotá" # Departamento, tabla 13.4.2, pasar a SQL
    PhysicalLocationCountrySubentityCode:           str #"11" #Codigo departamento, tabla 13.4.2, pasar a SQL
    PhysicalLocationAddressLine:                    str #"Av. #97 - 13" #Informar la dirección, sin ciudad ni departamento
    CountryIdentificationCode:                      str #"CO"
    CountryName:                                    str #"Colombia"
    TaxLevelCode:                                   str #"O-47" #Obligaciones o responsabilidades del contribuyente; incluye el régimen al que pertenece el emisor,  varios ej. O-13;O-15;//// tabla 13.2.6.1 O-13	Gran contribuyente, O-15	Autorretenedor, O-23	Agente de retención IVA, O-47	Régimen simple de tributación, R-99-PN	No aplica – Otros *
    AdditionalAccountID:                            str #1	Persona Jurídica y asimiladas, 2	Persona Natural y asimiladas Tabla 13.2.3
    PartyName:                                      str #"BILAI S.A.S" #Nombre comercial del emisor
    RegistrationName:                               str #"BILAI S.A.S" #Nombre registrado en el RUT
    TaxSchemeID:                                    str #"01" #Identificador del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *
    MatriculaMercantil:                             str #"3930757" # https://www.rues.org.co/buscar/RM/ Nit al final
    TaxSchemeName:                                  str #"IVA" #Nombre del tributo tabla 13.2.6.2 //// 01	IVA 04	INC ZA	IVA e INC ZZ 	No aplica *
    ElectronicMail:                                 str #Correo electronico

class AccountingCustomerParty(BaseModel):
    CustomerAdditionalAccountID:                    str #"2" # 1	Persona Jurídica y asimiladas, 2	Persona Natural y asimiladas Tabla 13.2.3 Nota: Se debe informar el código “2” cuando se trate del consumidor final
    CustomerPartyName:                              str #"Sergio Gonzalez"
    PartyIdentificationType:                        str #"13" #tipo de identificación Tabla 13.2.1 si es nit agregar DV y agregar a XML, pendiente
    PartyIdentification:                            str #"1014262008" # Si es nit, hay que agregar el digito de verificacion
    CustomerTaxSchemeID:                            str #"ZZ"
    CustomerTaxSchemeName:                          str #"No aplica"
    CustomerTaxLevelCode:                           str #"R-99-PN"
    ElectronicMail:                                 str #Correo electronico

class PaymentMeans(BaseModel):
    PaymentMeansID:                                 str #"1" #Formas de pago tabla 13.3.4.1 // 1	Contado 2	Crédito
    PaymentMeansCode:                               str #"91" #Código correspondiente al medio de pago tabla 13.3.4.2
    PaymentDueDate:                                 str #"2019-06-30" #Fecha de vencimiento de la factura, Obligatorio si es venta a crédito

class TaxTotal(BaseModel):
    TaxAmount:                                      str #"215.55" #Valor del tributo //// Suma de todos los elementos ../cac:TaxTotal/TaxSubtotal/cbc :TaxAmount
    TaxableAmount:                                  str #"1134.45" #Base Imponible sobre la que se calcula el valor del tributo
    TaxSubtotalTaxAmount:                           str #"215.55" #Valor del tributo: producto del porcentaje aplicado sobre la base imponible
    Percent:                                        str #"19.00" #Tarifa del tributo tabla 13.3.11
    TaxSubtotalTaxSchemeID:                         str #"01" #Identificador del tributo
    TaxSubtotalTaxSchemeName:                       str #"IVA" #Nombre del tributo

class LegalMonetaryTotal(BaseModel):
    LineExtensionAmount:                            str #"1134.45" # Total Valor Bruto antes de tributos: Total valor bruto, suma de los valores brutos de las líneas de la factura.
    TaxExclusiveAmount:                             str #"1134.45" # Total Valor Base Imponible : Base imponible para el cálculo de los tributos
    TaxInclusiveAmount:                             str #"1350.00" #Total de Valor Bruto más tributos
    PayableAmount:                                  str #"1350.00" #Valor de la Factura: Valor total de ítems (incluyendo cargos y descuentos a nivel de ítems)+valor tributos + valor cargos – valor descuentos.

class InvoiceLine(BaseModel):
    InvoiceLineID:                                  str #"1" #Número de Línea debe ser incremental
    InvoicedQuantity:                               str #"1.00" #Cantidad del producto o servicio ////Revisar si debe ser solo 1
    UnitCode:                                       str #"ZZ" #Identificación de la unidad de medida tabla 13.3.6
    InvoiceLineLineExtensionAmount:                 str #"1134.45" #Valor total de la línea. //// El Valor Total de la línea es igual al producto de Cantidad x Precio Unidad menos Descuentos más Recargos que apliquen para la línea.
    AllowanceChargeID:                              str
    ChargeIndicator:                                str #"false" #Indica que el elemento es un Cargo y no un descuento //// Cargo es true, es un Débito aumenta el valor de la item. Descuento es false, un Crédito descuenta el valor del ítem El elemento solamente puede identificar una de las informaciones.
    AllowanceChargeReason:                          str #"Descuento por cliente frecuente" #Texto libre para informar de la razón del descuento.
    MultiplierFactorNumeric:                        str #"33.33" #Porcentaje que aplicar.
    Amount:                                         str #"6299.94" #Valor total del cargo o descuento
    BaseAmount:                                     str #"18900.00" #Valor Base para calcular el descuento el cargo
    ItemDescription:                                str #"AV OASYS -2.25 (8.4) LENTE DE CONTATO" #Descripción del artículo o servicio a que se refiere esta línea de la factura
    PriceAmount:                                    str #"1134.45" #Valor del artículo o servicio
    BaseQuantity:                                   str #"1.00" #La cantidad real sobre la cual el precio aplica
    BaseQuantityUnitCode:                           str #"ZZ" #Identificación de la unidad de medida tabla 13.3.6

class TaxTotalInvoiceLine(BaseModel):
    InvoiceLineTaxAmount:                           str #"215.55" #Valor del tributo //// Suma de todos los elementos ../cac:TaxTotal/TaxSubtotal/cbc :TaxAmount
    InvoiceLineTaxableAmount:                       str #"1134.45" #Base Imponible sobre la que se calcula el valor del tributo
    InvoiceLineTaxSubtotalTaxAmount:                str #"215.55" #Valor del tributo: producto del porcentaje aplicado sobre la base imponible
    InvoiceLinePercent:                             str #"19.00" #Tarifa del tributo tabla 13.3.11
    InvoiceLineTaxSubtotalTaxSchemeID:              str #"01" #Identificador del tributo
    InvoiceLineTaxSubtotalTaxSchemeName:            str #"IVA" #Nombre del tributo

class CUFE(BaseModel):
    CodImp1:                                        str #"01" #01 Este valor es fijo.
    ValImp1:                                        str #"215.55" #Valor impuesto 01 - IVA    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
    CodImp2:                                        str #"04" #04 Este valor es fijo.
    ValImp2:                                        str #"0.00" #Valor impuesto 04 - Impuesto Nacional al Consumo    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
    CodImp3:                                        str #"03" #03 Este valor es fijo.
    ValImp3:                                        str #"0.00" #Valor impuesto 03 - ICA    // Revisar, se deben sumar todos los impuestos de algún lado, seguramente de TaxSubtotal
    ClTec:                                          str #"fc8eac422eba16e22ffd8c6f94b3f40a6e38162c" #Extraer de página de la DIAN // Llave tecnica TechnicalKey

class Request(BaseModel):
    CreditNote:                 CreditNote
    DebitNote:                  DebitNote
    UBLExtensions:              UBLExtensions 
    Signature:                  Signature
    VersionXML:                 VersionXML
    AccountingSupplierParty:    AccountingSupplierParty
    AccountingCustomerParty:    AccountingCustomerParty
    PaymentMeans:               PaymentMeans
    TaxTotal:                   TaxTotal
    LegalMonetaryTotal:         LegalMonetaryTotal
    InvoiceLine:                InvoiceLine
    TaxTotalInvoiceLine:        TaxTotalInvoiceLine
    CUFE:                       CUFE