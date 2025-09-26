
def UBLExtensions(
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
    return(
        f'<ext:UBLExtensions>\n\
      <ext:UBLExtension>\n\
         <ext:ExtensionContent>\n\
            <sts:DianExtensions>\n\
               <sts:InvoiceControl>\n\
                  <sts:InvoiceAuthorization>{InvoiceAuthorization}</sts:InvoiceAuthorization>\n\
                  <sts:AuthorizationPeriod>\n\
                     <cbc:StartDate>{StartDate}</cbc:StartDate>\n\
                     <cbc:EndDate>{EndDate}</cbc:EndDate>\n\
                  </sts:AuthorizationPeriod>\n\
                  <sts:AuthorizedInvoices>\n\
                     <sts:Prefix>{Prefix}</sts:Prefix>\n\
                     <sts:From>{From}</sts:From>\n\
                     <sts:To>{To}</sts:To>\n\
                  </sts:AuthorizedInvoices>\n\
               </sts:InvoiceControl>\n\
               <sts:InvoiceSource>\n\
                  <cbc:IdentificationCode listAgencyID="6" listAgencyName="United Nations Economic Commission for Europe" listSchemeURI="urn:oasis:names:specification:ubl:codelist:gc:CountryIdentificationCode-2.1">CO</cbc:IdentificationCode>\n\
               </sts:InvoiceSource>\n\
               <sts:SoftwareProvider>\n\
                  <sts:ProviderID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="{ProviderIDDV}" schemeName="31">{ProviderID}</sts:ProviderID>\n\
                  <sts:SoftwareID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">{SoftwareID}</sts:SoftwareID>\n\
               </sts:SoftwareProvider>\n\
               <sts:SoftwareSecurityCode schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">{SoftwareSecurityCode}</sts:SoftwareSecurityCode>\n\
               <sts:AuthorizationProvider>\n\
                  <sts:AuthorizationProviderID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="{AuthorizationProviderDV}" schemeName="31">{AuthorizationProviderID}</sts:AuthorizationProviderID>\n\
               </sts:AuthorizationProvider>\n\
               <sts:QRCode>{URL}{CUFE}</sts:QRCode>\n\
            </sts:DianExtensions>\n\
         </ext:ExtensionContent>\n\
      </ext:UBLExtension>\n\
   <ext:UBLExtension><ext:ExtensionContent></ext:ExtensionContent></ext:UBLExtension></ext:UBLExtensions>\n\
    ')