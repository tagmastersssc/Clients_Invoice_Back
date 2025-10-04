
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
import warnings
import calendar
from lxml import etree
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from models import Request

#Quitar warning de P12
warnings.filterwarnings("ignore",category=UserWarning,message="PKCS#12 bundle could not be parsed as DER")
####

def GenerateXML(Request: Request,Type):

    #UBLExtensions
    InvoiceNumber                                   = int(Request.UBLExtensions.From) + 8
    ID                                              = Request.UBLExtensions.Prefix + str(InvoiceNumber) #El From debería estar en un For, para ir aumentando el consecutivo
    SoftwareSecurityCode                            = Request.UBLExtensions.SoftwareID + Request.UBLExtensions.PIN + ID
    SoftwareSecurityCode                            = SoftwareSecurityCode.encode()
    SoftwareSecurityCode                            = hashlib.sha384(SoftwareSecurityCode).hexdigest()
    #****UBLExtensions

    #Signature
    with open(Request.Signature.P12Path, "rb") as f:
        P12Data = f.read()
    PrivateKey, Cert , AdditionalCerts              = pkcs12.load_key_and_certificates(
        P12Data, Request.Signature.P12Password.encode()
                                                    )
    CertDer                                         = Cert.public_bytes(Encoding.DER)
    Digest                                          = hashes.Hash(hashes.SHA256())
    Digest.update(CertDer)
    DigestBytes                                     = Digest.finalize()
    DigestValuePublicCert                           = base64.b64encode(DigestBytes).decode("utf-8")
    PublicCertOneLine                               = base64.b64encode(CertDer).decode()
    CanonicalizationMethod                          = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
    SignatureMethod                                 = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
    TransformAlgorithm                              = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
    DigestMethodAlgorithm                           = "http://www.w3.org/2001/04/xmlenc#sha256"
    DigestMethodAlgorithmPolicy                     = "http://www.w3.org/2001/04/xmlenc#sha256"
    TimeZone                                        = timezone(timedelta(hours=-5))
    Now                                             = datetime.now(TimeZone)
    SigningTimeFormatted                            = Now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + Now.strftime("%z")
    SigningTimeFormatted                            = SigningTimeFormatted[:-2] + ":" + SigningTimeFormatted[-2:]
    IssuerName                                      = Cert.issuer.rfc4514_string()
    IssuerName                                      = IssuerName.replace("2.5.4.5=", "SERIALNUMBER=")
    IssuerSerial                                    = Cert.serial_number
    DownloadedSignPolicy                            = requests.get(Request.Signature.SignPolicyURL)
    DownloadedSignPolicy.raise_for_status()
    DigestValueSigPolicyHash                        = base64.b64encode(hashlib.sha256(DownloadedSignPolicy.content).digest()).decode("utf-8")
    #****Signature

    #VersionXML
    IssueDate                                       = Now.strftime("%Y-%m-%d")
    IssueTime                                       = Now.strftime("%H:%M:%S%z")
    IssueTime                                       = IssueTime[:-2] + ":" + IssueTime[-2:]
    InvoicePeriodStartDate                          = Now.replace(day=1).strftime("%Y-%m-%d")
    LastDay                                         = calendar.monthrange(Now.year, Now.month)[1]
    InvoicePeriodEndDate                            = Now.replace(day=LastDay).strftime("%Y-%m-%d")
    #****VersionXML
    
    #AccountingSupplierParty  Grupo de información que definen el obligado a facturar: Emisor de la factura
    RegistrationAddressID                           = Request.AccountingSupplierParty.PhysicalLocationID #Cambiar si la direccion fiscal del emisor es diferente
    RegistrationAddressCityName                     = Request.AccountingSupplierParty.PhysicalLocationCityName #Cambiar si la direccion fiscal del emisor es diferente
    RegistrationAddressCountrySubentity             = Request.AccountingSupplierParty.PhysicalLocationCountrySubentity #Cambiar si la direccion fiscal del emisor es diferente
    RegistrationAddressCountrySubentityCode         = Request.AccountingSupplierParty.PhysicalLocationCountrySubentityCode #Cambiar si la direccion fiscal del emisor es diferente
    RegistrationAddressAddressLine                  = Request.AccountingSupplierParty.PhysicalLocationAddressLine #Cambiar si la direccion fiscal del emisor es diferente
    RegistrationAddressCountryIdentificationCode    = Request.AccountingSupplierParty.CountryIdentificationCode #Cambiar si la direccion fiscal del emisor es diferente
    RegistrationAddressCountryName                  = Request.AccountingSupplierParty.CountryName #Cambiar si la direccion fiscal del emisor es diferente
    #****AccountingSupplierParty

    if(Type         == "Invoice"):
        CloseTag                                        = "</Invoice>"
        CUFE                                            = ID + IssueDate + IssueTime + Request.LegalMonetaryTotal.LineExtensionAmount + Request.CUFE.CodImp1 + Request.CUFE.ValImp1 + Request.CUFE.CodImp2 + Request.CUFE.ValImp2 + Request.CUFE.CodImp3 + Request.CUFE.ValImp3 + Request.LegalMonetaryTotal.PayableAmount + Request.UBLExtensions.ProviderID + Request.AccountingCustomerParty.PartyIdentification + Request.CUFE.ClTec + Request.VersionXML.ProfileExecutionID
        CUFE                                            = CUFE.encode()
        CUFE                                            = hashlib.sha384(CUFE).hexdigest()
    elif(Type       == "CreditNote"):
        CloseTag                                        = "</CreditNote>"
        CUFE                                            = Request.CreditNote.CUFE
    elif(Type       == "DebitNote"):
        CloseTag                                        = "</DebitNote>"
        CUFE                                            = Request.CreditNote.CUFE
        


    Header                                          = XML_Parts.Header.Header(Type)

    UBLExtensions                                   = XML_Parts.UBLExtensions.UBLExtensions(
                                                        Type,
                                                        Request.UBLExtensions.InvoiceAuthorization,
                                                        Request.UBLExtensions.StartDate,
                                                        Request.UBLExtensions.EndDate,
                                                        Request.UBLExtensions.Prefix,
                                                        Request.UBLExtensions.From,
                                                        Request.UBLExtensions.To,
                                                        Request.UBLExtensions.ProviderID,
                                                        Request.UBLExtensions.ProviderIDDV,
                                                        Request.UBLExtensions.SoftwareID,
                                                        SoftwareSecurityCode,
                                                        Request.UBLExtensions.AuthorizationProviderID,
                                                        Request.UBLExtensions.AuthorizationProviderDV,
                                                        CUFE,
                                                        Request.UBLExtensions.URL
                                                    )   

    VersionXML                                      = XML_Parts.VersionXML.VersionXML(
                                                        Request.VersionXML.UBLVersionID,
                                                        Request.VersionXML.CustomizationID,
                                                        Request.VersionXML.ProfileID,
                                                        Request.VersionXML.ProfileExecutionID,
                                                        ID,
                                                        CUFE,
                                                        IssueDate,
                                                        IssueTime,
                                                        Request.VersionXML.InvoiceTypeCode,
                                                        Request.VersionXML.DocumentCurrencyCode,
                                                        Request.VersionXML.LineCountNumeric,
                                                        InvoicePeriodStartDate,
                                                        InvoicePeriodEndDate
                                                    )

    AccountingSupplierParty                         = XML_Parts.AccountingSupplierParty.AccountingSupplierParty(
                                                        Request.AccountingSupplierParty.AdditionalAccountID,
                                                        Request.AccountingSupplierParty.PartyName,
                                                        Request.AccountingSupplierParty.PhysicalLocationID,
                                                        Request.AccountingSupplierParty.PhysicalLocationCityName,
                                                        Request.AccountingSupplierParty.PhysicalLocationCountrySubentity,
                                                        Request.AccountingSupplierParty.PhysicalLocationCountrySubentityCode,
                                                        Request.AccountingSupplierParty.PhysicalLocationAddressLine,
                                                        Request.AccountingSupplierParty.CountryIdentificationCode,
                                                        Request.AccountingSupplierParty.CountryName,
                                                        Request.AccountingSupplierParty.RegistrationName,
                                                        Request.UBLExtensions.ProviderID,
                                                        Request.UBLExtensions.ProviderIDDV,
                                                        Request.AccountingSupplierParty.TaxLevelCode,
                                                        RegistrationAddressID,
                                                        RegistrationAddressCityName,
                                                        RegistrationAddressCountrySubentity,
                                                        RegistrationAddressCountrySubentityCode,
                                                        RegistrationAddressAddressLine,
                                                        RegistrationAddressCountryIdentificationCode,
                                                        RegistrationAddressCountryName,
                                                        Request.AccountingSupplierParty.TaxSchemeID,
                                                        Request.AccountingSupplierParty.TaxSchemeName,
                                                        Request.UBLExtensions.Prefix,
                                                        Request.AccountingSupplierParty.MatriculaMercantil
                                                    )

    AccountingCustomerParty                         = XML_Parts.AccountingCustomerParty.AccountingCustomerParty(
                                                        Request.AccountingCustomerParty.CustomerAdditionalAccountID,
                                                        Request.AccountingCustomerParty.CustomerPartyName,
                                                        Request.AccountingCustomerParty.PartyIdentificationType,
                                                        Request.AccountingCustomerParty.PartyIdentification,
                                                        Request.AccountingCustomerParty.CustomerTaxSchemeID,
                                                        Request.AccountingCustomerParty.CustomerTaxSchemeName,
                                                        Request.AccountingCustomerParty.CustomerTaxLevelCode
                                                    )

    PaymentMeans                                    = XML_Parts.PaymentMeans.PaymentMeans(
                                                        Request.PaymentMeans.PaymentMeansID,
                                                        Request.PaymentMeans.PaymentMeansCode,
                                                        Request.PaymentMeans.PaymentDueDate
                                                    )

    TaxTotal                                        = XML_Parts.TaxTotal.TaxTotal(
                                                        Request.TaxTotal.TaxAmount,
                                                        Request.VersionXML.DocumentCurrencyCode,
                                                        Request.TaxTotal.TaxableAmount,
                                                        Request.TaxTotal.TaxSubtotalTaxAmount,
                                                        Request.TaxTotal.Percent,
                                                        Request.TaxTotal.TaxSubtotalTaxSchemeID,
                                                        Request.TaxTotal.TaxSubtotalTaxSchemeName
                                                    )

    LegalMonetaryTotal                              = XML_Parts.LegalMonetaryTotal.LegalMonetaryTotal(
                                                        Request.VersionXML.DocumentCurrencyCode,
                                                        Request.LegalMonetaryTotal.LineExtensionAmount,
                                                        Request.LegalMonetaryTotal.TaxExclusiveAmount,
                                                        Request.LegalMonetaryTotal.TaxInclusiveAmount,
                                                        Request.LegalMonetaryTotal.PayableAmount
                                                    )

    TaxTotalInvoiceLine                             = XML_Parts.TaxTotal.TaxTotal(
                                                        Request.TaxTotalInvoiceLine.InvoiceLineTaxAmount,
                                                        Request.VersionXML.DocumentCurrencyCode,
                                                        Request.TaxTotalInvoiceLine.InvoiceLineTaxableAmount,
                                                        Request.TaxTotalInvoiceLine.InvoiceLineTaxSubtotalTaxAmount,
                                                        Request.TaxTotalInvoiceLine.InvoiceLinePercent,
                                                        Request.TaxTotalInvoiceLine.InvoiceLineTaxSubtotalTaxSchemeID,
                                                        Request.TaxTotalInvoiceLine.InvoiceLineTaxSubtotalTaxSchemeName
                                                    )

    InvoiceLine                                     = XML_Parts.InvoiceLine.InvoiceLine(
                                                        Request.InvoiceLine.InvoiceLineID,
                                                        Request.InvoiceLine.InvoicedQuantity,
                                                        Request.InvoiceLine.UnitCode,
                                                        Request.InvoiceLine.InvoiceLineLineExtensionAmount,
                                                        Request.VersionXML.DocumentCurrencyCode,
                                                        Request.InvoiceLine.AllowanceChargeID,
                                                        Request.InvoiceLine.ChargeIndicator,
                                                        Request.InvoiceLine.AllowanceChargeReason,
                                                        Request.InvoiceLine.MultiplierFactorNumeric,
                                                        Request.InvoiceLine.Amount,
                                                        Request.InvoiceLine.BaseAmount,
                                                        TaxTotalInvoiceLine,
                                                        Request.InvoiceLine.ItemDescription,
                                                        Request.InvoiceLine.PriceAmount,
                                                        Request.InvoiceLine.BaseQuantity,
                                                        Request.InvoiceLine.BaseQuantityUnitCode
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
            CloseTag 
        )
    XML = CreateXml()

    #Canonicalizar XML full, y generar el digest value full
    parser                                          = etree.XMLParser(remove_blank_text=True)
    doc                                             = etree.fromstring(XML.encode("utf-8"), parser)
    CanonicalXml                             = etree.tostring(doc, method="c14n", exclusive=False)

    DigestValueAllC14nInvoice                       = base64.b64encode(hashlib.sha256(CanonicalXml).digest()).decode("utf-8")

    #Insertar bloque Signature con valores incorrectos
    DigestValueKeyInfo                              = ""
    DigestValueSignedProperties                     = ""
    SignatureValue                                  = ""
    UUID                                            = str(uuid.uuid4())

    KeyInfo                                         = f"""<ds:KeyInfo Id="xmldsig-{UUID}-keyinfo" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:xades="http://uri.etsi.org/01903/v1.3.2#"><ds:X509Data><ds:X509Certificate>{PublicCertOneLine}</ds:X509Certificate></ds:X509Data></ds:KeyInfo>"""

    SignedProperties                                = f"""<xades:SignedProperties Id="xmldsig-{UUID}-signedprops"><xades:SignedSignatureProperties><xades:SigningTime>{SigningTimeFormatted}</xades:SigningTime><xades:SigningCertificate><xades:Cert><xades:CertDigest><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValuePublicCert}</ds:DigestValue></xades:CertDigest><xades:IssuerSerial><ds:X509IssuerName>{IssuerName}</ds:X509IssuerName><ds:X509SerialNumber>{IssuerSerial}</ds:X509SerialNumber></xades:IssuerSerial></xades:Cert></xades:SigningCertificate><xades:SignaturePolicyIdentifier><xades:SignaturePolicyId><xades:SigPolicyId><xades:Identifier>{Request.Signature.SignPolicyURL}</xades:Identifier><xades:Description>Política de firma para facturas electrónicas de la República de Colombia.</xades:Description></xades:SigPolicyId><xades:SigPolicyHash><ds:DigestMethod Algorithm="{DigestMethodAlgorithmPolicy}"/><ds:DigestValue>{DigestValueSigPolicyHash}</ds:DigestValue></xades:SigPolicyHash></xades:SignaturePolicyId></xades:SignaturePolicyIdentifier><xades:SignerRole><xades:ClaimedRoles><xades:ClaimedRole>{Request.Signature.SignerRole}</xades:ClaimedRole></xades:ClaimedRoles></xades:SignerRole></xades:SignedSignatureProperties></xades:SignedProperties>"""

    SignedInfo                                      = f"""<ds:SignedInfo><ds:CanonicalizationMethod Algorithm="{CanonicalizationMethod}"/><ds:SignatureMethod Algorithm="{SignatureMethod}"/><ds:Reference Id="xmldsig-{UUID}-ref0" URI=""><ds:Transforms><ds:Transform Algorithm="{TransformAlgorithm}"/></ds:Transforms><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValueAllC14nInvoice}</ds:DigestValue></ds:Reference><ds:Reference URI="#xmldsig-{UUID}-keyinfo"><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValueKeyInfo}</ds:DigestValue></ds:Reference><ds:Reference Type="http://uri.etsi.org/01903#SignedProperties" URI="#xmldsig-{UUID}-signedprops"><ds:DigestMethod Algorithm="{DigestMethodAlgorithm}"/><ds:DigestValue>{DigestValueSignedProperties}</ds:DigestValue></ds:Reference></ds:SignedInfo>"""

    Signature                                       = XML_Parts.Signature.Signature(
                                                        KeyInfo,
                                                        SignedProperties,
                                                        SignedInfo,
                                                        SignatureValue,
                                                        UUID
                                                    )

    Signature                                       = etree.fromstring(Signature.encode("utf-8"), parser)
    CanonicalXmlTree                         = etree.fromstring(CanonicalXml,parser)

    Signature                                       = etree.tostring(
                                                        Signature,
                                                        method="c14n",
                                                        exclusive=False,
                                                        with_comments=False,
                                                        inclusive_ns_prefixes=None
                                                    )

    #Añade bloque signature

    ns                                              = {"ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"}
    InvoiceExtensionContents                        = CanonicalXmlTree.findall(".//ext:ExtensionContent", namespaces=ns)
    SecondExtensionContent                          = InvoiceExtensionContents[1]
    SecondExtensionContent.append(etree.fromstring(Signature))
    #Calcular DigestValue KeyInfo y remplazar en factura

    ns                                              = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
    keyinfo_node                                    = CanonicalXmlTree.find(".//ds:KeyInfo", namespaces=ns)

    CanonicalKeyInfo                                = etree.tostring(
                                                        keyinfo_node,
                                                        method="c14n",
                                                        exclusive=False,
                                                        with_comments=False,
                                                        inclusive_ns_prefixes=None
                                                    )

    DigestValueKeyInfo                              = base64.b64encode(hashlib.sha256(CanonicalKeyInfo).digest()).decode("utf-8")
    KeyInfoReferenceNode                            = CanonicalXmlTree.xpath(f".//ds:Reference[@URI='#xmldsig-{UUID}-keyinfo']", namespaces=ns)
    DigestNode                                      = KeyInfoReferenceNode[0].find("ds:DigestValue", namespaces=ns)
    DigestNode.text                                 = DigestValueKeyInfo

    #Calcular DigestValue SignedProperties y remplazar en factura

    ns                                              = {"xades": "http://uri.etsi.org/01903/v1.3.2#"}
    SignedPropertiesNode                            = CanonicalXmlTree.find(".//xades:SignedProperties", namespaces=ns)
    CanonicalSignedProperties                       = etree.tostring(
                                                        SignedPropertiesNode,
                                                        method="c14n",
                                                        exclusive=False,
                                                        with_comments=False,
                                                        inclusive_ns_prefixes=None
                                                    )
    DigestValueSignedProperties                     = base64.b64encode(hashlib.sha256(CanonicalSignedProperties).digest()).decode("utf-8")
    ns                                              = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
    SignedPropertiesReferenceNode                   = CanonicalXmlTree.xpath(f".//ds:Reference[@URI='#xmldsig-{UUID}-signedprops']", namespaces=ns)
    DigestNode                                      = SignedPropertiesReferenceNode[0].find("ds:DigestValue", namespaces=ns)
    DigestNode.text                                 = DigestValueSignedProperties

    #Canonicalizar SignedInfo

    SignedInfoNode                                  = CanonicalXmlTree.find(".//ds:SignedInfo", namespaces=ns)
    SignedInfoCanonicalXml                          = etree.tostring(
                                                        SignedInfoNode,
                                                        method="c14n",
                                                        exclusive=False,
                                                        with_comments=False,
                                                        inclusive_ns_prefixes=None
                                                    )

    #Firmar

    SignedInfoSignature                             = PrivateKey.sign(
                                                        SignedInfoCanonicalXml,
                                                        padding.PKCS1v15(),
                                                        hashes.SHA256()
                                                    )
    SignatureValue                                  = base64.b64encode(SignedInfoSignature).decode("utf-8")

    #Cambiar SignatureValue en factura
    SignatureValueNode                              = CanonicalXmlTree.find(".//ds:SignatureValue", namespaces=ns)
    SignatureValueNode.text                         = SignatureValue

    #Buscar nodo signature 
    SignatureNode                                   = CanonicalXmlTree.find(".//ds:Signature", namespaces=ns)
    XMLStr                                          = etree.tostring(SignatureNode, encoding="utf-8")
    CleanSignatureNode                              = etree.fromstring(XMLStr, parser)

    SignatureStr                                    = etree.tostring(CleanSignatureNode, encoding="utf-8").decode("utf-8")

    CanonicalXmlTree                         = etree.tostring(CanonicalXmlTree, encoding="utf-8").decode("utf-8")

    SignedInvoice                                   = CanonicalXmlTree.replace(
                                                        "<ext:ExtensionContent></ext:ExtensionContent>", 
                                                        f"<ext:ExtensionContent>{SignatureStr}</ext:ExtensionContent>"
                                                    )
    SignedInvoice                                   = SignedInvoice.replace(
                                                        f'<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" xmlns:sts="dian:gov:co:facturaelectronica:Structures-2-1" Id="xmldsig-{UUID}">', 
                                                        f'<ds:Signature Id="xmldsig-{UUID}">'
                                                    )

    with open(f"{Type}_c14n_Sig.xml", "w", encoding="utf-8") as f:
        f.write(SignedInvoice)

    #Comprimir XML en Zip
    FileToZip                                       = f"{Type}_c14n_Sig.xml"
    DestinationZip                                  = f"{Type}_c14n_Sig.zip"

    with zipfile.ZipFile(DestinationZip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(FileToZip, os.path.basename(FileToZip))

    with open(DestinationZip, "rb") as f:
        ZipBase64 = base64.b64encode(f.read()).decode("utf-8")

    SOAPNow                                         = datetime.now(timezone.utc)
    TimestampCreated                                = SOAPNow.strftime("%Y-%m-%dT%H:%M:%SZ")
    TimestampExpires                                = (SOAPNow + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    SOAPTo                                          = "https://vpfe-hab.dian.gov.co/WcfDianCustomerServices.svc"
    ToTag                                           = f"""<wsa:To xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:wcf="http://wcf.dian.colombia" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="id-9821734F262768B5271758426395096292">{SOAPTo}</wsa:To>"""
    SOAPDigestValue                                 =  base64.b64encode(hashlib.sha256(ToTag.encode("utf-8")).digest()).decode("utf-8")
    SOAPSignedInfo                                  = f"""<ds:SignedInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:wcf="http://wcf.dian.colombia" xmlns:wsa="http://www.w3.org/2005/08/addressing"><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"><ec:InclusiveNamespaces xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" PrefixList="wsa soap wcf"></ec:InclusiveNamespaces></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"></ds:SignatureMethod><ds:Reference URI="#id-9821734F262768B5271758426395096292"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"><ec:InclusiveNamespaces xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" PrefixList="soap wcf"></ec:InclusiveNamespaces></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></ds:DigestMethod><ds:DigestValue>{SOAPDigestValue}</ds:DigestValue></ds:Reference></ds:SignedInfo>"""
    SOAPSignedInfoSignature                         = PrivateKey.sign(
                                                        SOAPSignedInfo.encode("utf-8"),
                                                        padding.PKCS1v15(),
                                                        hashes.SHA256()
                                                    )
    SOAPSignatureValue                              = base64.b64encode(SOAPSignedInfoSignature).decode("utf-8")
    SOAPAction                                      = "http://wcf.dian.colombia/IWcfDianCustomerServices/SendBillSync" #Produccion debe ser diferente #Actualmente está SendBillSync, para ver la respuesta inmediata, para habilitar el set de pruebas, debe ser SendTestSetAsync
    TestSetId                                       = "47c11080-2700-4010-afc4-19b8d95cbf6a" #Produccion no lo debe tener //SET DE PRUEBAS

    GenerateSOAP                                    = XML_Parts.GenerateSOAP.GenerateSOAP(
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

    SOAPCanonicalXml                                = etree.tostring(etree.fromstring(GenerateSOAP.encode("utf-8")), method="c14n", exclusive=False)

    SOAPheaders                                     = {
                                                        "Content-Type": f'application/soap+xml;charset=UTF-8;action="{SOAPAction}"'
                                                    }
    if(Type=="Invoice"): #Pendiente
        response                                        = requests.post(SOAPTo, data=SOAPCanonicalXml.decode("utf-8"), headers=SOAPheaders)
        print("Código de respuesta:", response.status_code)
        print(response.text)


    return


    ###### // LEGACY
    #Pendiente
    #Todo debe llevar dos digitos, desde BD
    #TaxTotal puede haber varios, que son la suma de TaxSubtotal, TaxSubtotal puede haber varios.
    # VersionXML
    # BillingReference            = "" #Solo para documento con nota credito sacar modelo de generica.xml
    #****VersionXML          
    #AccountingSupplierParty  Grupo de información que definen el obligado a facturar: Emisor de la factura
    # IndustryClasificationCode                       = "5440" # Corresponde al código de actividad económica CIIU // al parecer la etiqueta es opcional, pendiente convertir en arreglo, pueden ser varios
    #Contact se eliminó etiqueta
    #****AccountingSupplierParty 
    #AccountingCustomerParty Grupo con información que definen el Adquiriente
    #Elimino bloque PhysicalLocation, documentacion lo marca opcional
    #Elimino bloque TaxLevelCode documentacion manda opcional
    #Elimino bloque RegistrationAddress documentacion manda opcional
    #Elimino bloque CorporateRegistrationScheme
    #Elimino bloque Contact
    #****AccountingCustomerParty 
    #Elimino bloque TaxRepresentativeParty documentacion manda opcional
    #Elimino bloque Delivery documentacion manda opcional
    #Elimino bloque DeliveryTerms documentacion manda opcional
    #PaymentMeans //// Formas de pago , pendiente agregar varios, documentación indica 1..N
    #Elimino bloque PaymentID, documentacion manda opcional
    #****PaymentMeans 
    #Elimino bloque PrepaidPayment, documentacion manda opcional
    #TaxTotal Grupo de campos para información totales relacionadas con un tributo
    #Despues del POC revisar, pueden haber varios taxtotal, cada uno con varios taxsubtotal, se debe calcular automatico todo lo de adentro
    #****TaxTotal
    #LegalMonetaryTotal   //// Grupo de campos para información relacionadas con los valores totales aplicables a la factura
    #AllowanceTotalAmount Descuento Total: Suma de todos los descuentos aplicados a nivel de la factura
    #ChargeTotalAmount Cargo Total: Suma de todos los cargos aplicados a nivel de la factura
    #PrePaidAmount Anticipo Total: Suma de todos los pagos anticipados
    #****LegalMonetaryTotal
    #InvoiceLine    ////   Grupo de campos para información relacionadas con una línea de factura Cuando se deba facturar un producto y un servicio, se deberán informar en Items(InvoiceLine) por seprado.
    #Solo para POC se manda base, después deben generarse varias lineas con todos los prpductos
    #schemeID Obligatorio cuando se informe el tipo de operación “11”: Valida los posibles valores en el numera . 13.3.12
    # Note Información Adicional: Texto libre para añadir información adicional al artículo.
    #Elimino FreeOfChargeIndicator no aparece en la documentación
    #Elimino Bloque Delivery no aparece en la documentación
    #AllowanceCharge Grupo de campos para información relacionadas con un cargo o un descuento //Pueden ser varios
    #Item Grupo de información que describen las características del artículo o servicio
    #Elimino bloque SellersItemIdentification , documentacion manda opcional
    #Elimino bloque AdditionalItemIdentification , documentacion manda opcional
    #Price Grupo de información que describen los precios del artículo o servicio
    #****InvoiceLine