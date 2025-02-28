
def UBLExtensions(
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
                    ):
    return(
        f'\
   <ext:UBLExtensions>\n\
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
                  <sts:ProviderID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="4" schemeName="31">{ProviderID}</sts:ProviderID>\n\
                  <sts:SoftwareID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">{SoftwareID}</sts:SoftwareID>\n\
               </sts:SoftwareProvider>\n\
               <sts:SoftwareSecurityCode schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">{SoftwareSecurityCode}</sts:SoftwareSecurityCode>\n\
               <sts:AuthorizationProvider>\n\
                  <sts:AuthorizationProviderID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="4" schemeName="31">{AuthorizationProviderID}</sts:AuthorizationProviderID>\n\
               </sts:AuthorizationProvider>\n\
               <sts:QRCode>NroFactura=SETP990000002\n\
								NitFacturador=800197268\n\
								NitAdquiriente=900108281\n\
								FechaFactura=2019-06-20\n\
								ValorTotalFactura=14024.07\n\
								CUFE=941cf36af62dbbc06f105d2a80e9bfe683a90e84960eae4d351cc3afbe8f848c26c39bac4fbc80fa254824c6369ea694\n\
								URL=https://catalogo-vpfe-hab.dian.gov.co/Document/FindDocument?documentKey=941cf36af62dbbc06f105d2a80e9bfe683a90e84960eae4d351cc3afbe8f848c26c39bac4fbc80fa254824c6369ea694&amp;partitionKey=co|06|94&amp;emissionDate=20190620</sts:QRCode>\n\
            </sts:DianExtensions>\n\
         </ext:ExtensionContent>\n\
      </ext:UBLExtension>\n\
   \n\
    ')