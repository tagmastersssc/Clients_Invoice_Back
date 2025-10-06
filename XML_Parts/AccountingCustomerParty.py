def AccountingCustomerParty(
                                CustomerAdditionalAccountID,
                                CustomerPartyName,
                                PartyIdentificationType,
                                PartyIdentification,
                                CustomerTaxSchemeID,
                                CustomerTaxSchemeName,
                                CustomerTaxLevelCode
                            ):
    return(
        f"""<cac:AccountingCustomerParty>
      <cbc:AdditionalAccountID>{CustomerAdditionalAccountID}</cbc:AdditionalAccountID>
      <cac:Party>
         <cac:PartyIdentification>
            <cbc:ID schemeName="{PartyIdentificationType}">{PartyIdentification}</cbc:ID>
         </cac:PartyIdentification>
         <cac:PartyName>
            <cbc:Name>{CustomerPartyName}</cbc:Name>
         </cac:PartyName>
         <cac:PartyTaxScheme>
            <cbc:RegistrationName>{CustomerPartyName}</cbc:RegistrationName>
            <cbc:CompanyID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="3" schemeName="{PartyIdentificationType}">{PartyIdentification}</cbc:CompanyID>
            <cbc:TaxLevelCode>{CustomerTaxLevelCode}</cbc:TaxLevelCode>
            <cac:TaxScheme>
               <cbc:ID>{CustomerTaxSchemeID}</cbc:ID>
               <cbc:Name>{CustomerTaxSchemeName}</cbc:Name>
            </cac:TaxScheme>
         </cac:PartyTaxScheme>
         <cac:PartyLegalEntity>
            <cbc:RegistrationName>{CustomerPartyName}</cbc:RegistrationName>
            <cbc:CompanyID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="3" schemeName="{PartyIdentificationType}">{PartyIdentification}</cbc:CompanyID>
         </cac:PartyLegalEntity>
      </cac:Party>
   </cac:AccountingCustomerParty>""")