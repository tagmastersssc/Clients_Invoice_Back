
def Signature(
                KeyInfo,
                SignedProperties,
                SignedInfo,
                SignatureValue,
                UUID
                ):
    return(
        f"""<ds:Signature Id="xmldsig-{UUID}" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
{SignedInfo}
<ds:SignatureValue Id="xmldsig-{UUID}-sigvalue">{SignatureValue}</ds:SignatureValue>
{KeyInfo}
<ds:Object>
<xades:QualifyingProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Target="#xmldsig-{UUID}">
{SignedProperties}
</xades:QualifyingProperties>
</ds:Object>
</ds:Signature>"""
    )