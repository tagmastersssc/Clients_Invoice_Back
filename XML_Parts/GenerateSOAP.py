
def GenerateSOAP(
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
                    ):
    return(
        f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:wcf="http://wcf.dian.colombia">
   <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"><wsu:Timestamp wsu:Id="TS-9821734F262768B5271758426395199294"><wsu:Created>{TimestampCreated}</wsu:Created><wsu:Expires>{TimestampExpires}</wsu:Expires></wsu:Timestamp><wsse:BinarySecurityToken EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" wsu:Id="X509-9821734F262768B5271758426395095289">{PublicCertOneLine}</wsse:BinarySecurityToken><ds:Signature Id="SIG-9821734F262768B5271758426395161293" xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"><ec:InclusiveNamespaces PrefixList="wsa soap wcf" xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#"/></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/><ds:Reference URI="#id-9821734F262768B5271758426395096292"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"><ec:InclusiveNamespaces PrefixList="soap wcf" xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#"/></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/><ds:DigestValue>{SOAPDigestValue}</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>{SOAPSignatureValue}</ds:SignatureValue><ds:KeyInfo Id="KI-9821734F262768B5271758426395095290"><wsse:SecurityTokenReference wsu:Id="STR-9821734F262768B5271758426395095291"><wsse:Reference URI="#X509-9821734F262768B5271758426395095289" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"/></wsse:SecurityTokenReference></ds:KeyInfo></ds:Signature></wsse:Security><wsa:Action>{SOAPAction}</wsa:Action><wsa:To wsu:Id="id-9821734F262768B5271758426395096292" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">{SOAPTo}</wsa:To></soap:Header>
   <soap:Body>
      <wcf:SendTestSetAsync>
         <!--Optional:-->
         <wcf:fileName>{DestinationZip}</wcf:fileName>
         <!--Optional:-->
         <wcf:contentFile>{ZipBase64}</wcf:contentFile>
         <!--Optional:-->
         <wcf:testSetId>{TestSetId}</wcf:testSetId>
      </wcf:SendTestSetAsync>
   </soap:Body>
</soap:Envelope>""")