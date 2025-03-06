def AccountingCustomerParty(
                                CustomerAdditionalAccountID,
                                CustomerPartyName,
                                PartyIdentificationType,
                                PartyIdentification,
                                CustomerTaxSchemeID,
                                CustomerTaxSchemeName
                            ):
    return(
        f'\
   <cac:AccountingCustomerParty>\n\
      <cbc:AdditionalAccountID>{CustomerAdditionalAccountID}</cbc:AdditionalAccountID>\n\
      <cac:Party>\n\
         <cac:PartyIdentification>\n\
            <cbc:ID schemeName="{PartyIdentificationType}">{PartyIdentification}</cbc:ID>\n\
         </cac:PartyIdentification>\n\
         <cac:PartyName>\n\
            <cbc:Name>{CustomerPartyName}</cbc:Name>\n\
         </cac:PartyName>\n\
         <cac:PartyTaxScheme>\n\
            <cbc:RegistrationName>{CustomerPartyName}</cbc:RegistrationName>\n\
            <cbc:CompanyID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="3" schemeName="{PartyIdentificationType}">{PartyIdentification}</cbc:CompanyID>\n\
            <cac:TaxScheme>\n\
               <cbc:ID>{CustomerTaxSchemeID}</cbc:ID>\n\
               <cbc:Name>{CustomerTaxSchemeName}</cbc:Name>\n\
            </cac:TaxScheme>\n\
         </cac:PartyTaxScheme>\n\
         <cac:PartyLegalEntity>\n\
            <cbc:RegistrationName>{CustomerPartyName}</cbc:RegistrationName>\n\
            <cbc:CompanyID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="3" schemeName="{PartyIdentificationType}">{PartyIdentification}</cbc:CompanyID>\n\
         </cac:PartyLegalEntity>\n\
      </cac:Party>\n\
   </cac:AccountingCustomerParty>\n\
    ')