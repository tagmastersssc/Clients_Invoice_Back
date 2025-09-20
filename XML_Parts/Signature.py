
def Signature(
                KeyInfo,
                SignedProperties,
                SignedInfo,
                SignatureValue
                ):
    return(
        f"""<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
{SignedInfo}
<ds:SignatureValue>
{SignatureValue}
</ds:SignatureValue>
{KeyInfo}
<ds:Object>
<xades:QualifyingProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Target="">
{SignedProperties}
</xades:QualifyingProperties>
</ds:Object>
</ds:Signature>"""
    )