
def UBLExtensions(
                  Type,
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
                  ):
    DianExtensionsBefore   = f"""<sts:InvoiceSource>
                     <cbc:IdentificationCode listAgencyID="6" listAgencyName="United Nations Economic Commission for Europe" listSchemeURI="urn:oasis:names:specification:ubl:codelist:gc:CountryIdentificationCode-2.1">CO</cbc:IdentificationCode>
                  </sts:InvoiceSource>
                  <sts:SoftwareProvider>
                     <sts:ProviderID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="{ProviderIDDV}" schemeName="31">{ProviderID}</sts:ProviderID>
                     <sts:SoftwareID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">{SoftwareID}</sts:SoftwareID>
                  </sts:SoftwareProvider>
                  <sts:SoftwareSecurityCode schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">{SoftwareSecurityCode}</sts:SoftwareSecurityCode>
                  <sts:AuthorizationProvider>
                     <sts:AuthorizationProviderID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="{AuthorizationProviderDV}" schemeName="31">{AuthorizationProviderID}</sts:AuthorizationProviderID>
                  </sts:AuthorizationProvider>
                  <sts:QRCode>{URL}{CUFE}</sts:QRCode>
               </sts:DianExtensions>"""
    if (Type == "Invoice"):
      DianExtensionsAfter   = f"""<sts:DianExtensions>
                  <sts:InvoiceControl>
                     <sts:InvoiceAuthorization>{InvoiceAuthorization}</sts:InvoiceAuthorization>
                     <sts:AuthorizationPeriod>
                        <cbc:StartDate>{StartDate}</cbc:StartDate>
                        <cbc:EndDate>{EndDate}</cbc:EndDate>
                     </sts:AuthorizationPeriod>
                     <sts:AuthorizedInvoices>
                        <sts:Prefix>{Prefix}</sts:Prefix>
                        <sts:From>{From}</sts:From>
                        <sts:To>{To}</sts:To>
                     </sts:AuthorizedInvoices>
                  </sts:InvoiceControl>
                  {DianExtensionsBefore}"""
    else:
       DianExtensionsAfter   = f"""<sts:DianExtensions>
                  {DianExtensionsBefore}"""
    return(
        f"""<ext:UBLExtensions>
      <ext:UBLExtension>
         <ext:ExtensionContent>
            {DianExtensionsAfter}
         </ext:ExtensionContent>
      </ext:UBLExtension>
   <ext:UBLExtension><ext:ExtensionContent></ext:ExtensionContent></ext:UBLExtension></ext:UBLExtensions>""")