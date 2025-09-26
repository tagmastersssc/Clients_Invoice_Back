
def Signature(
                KeyInfo,
                SignedProperties,
                SignedInfo,
                SignatureValue
                ):
    return(
        f"""<ds:Signature Id="xmldsig-f1a488a1-61f3-4856-b35b-b5d4211b75ee" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
{SignedInfo}
<ds:SignatureValue Id="xmldsig-f1a488a1-61f3-4856-b35b-b5d4211b75ee-sigvalue">{SignatureValue}</ds:SignatureValue>
{KeyInfo}
<ds:Object>
<xades:QualifyingProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Target="#xmldsig-f1a488a1-61f3-4856-b35b-b5d4211b75ee">
{SignedProperties}
</xades:QualifyingProperties>
</ds:Object>
</ds:Signature>"""
    )