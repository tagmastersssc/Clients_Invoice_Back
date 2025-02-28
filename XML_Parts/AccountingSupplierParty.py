
def AccountingSupplierParty(
                              AdditionalAccountID,
                              IndustryClasificationCode,
                              PartyName,
                              PhysicalLocationID,
                              PhysicalLocationCityName,
                              PhysicalLocationCountrySubentity,
                              PhysicalLocationCountrySubentityCode,
                              PhysicalLocationAddressLine,
                              CountryIdentificationCode,
                              CountryName,
                              RegistrationName,
                              ProviderID,
                              ProviderIDDV,
                              TaxLevelCode,
                              RegistrationAddressID,
                              RegistrationAddressCityName,
                              RegistrationAddressCountrySubentity,
                              RegistrationAddressCountrySubentityCode,
                              RegistrationAddressAddressLine,
                              RegistrationAddressCountryIdentificationCode,
                              RegistrationAddressCountryName,
                              TaxSchemeID,
                              TaxSchemeName
                              ):
    return(
        f'\
   <cac:AccountingSupplierParty>\n\
      <cbc:AdditionalAccountID>{AdditionalAccountID}</cbc:AdditionalAccountID>\n\
      <cac:Party>\n\
         <cbc:IndustryClasificationCode>{IndustryClasificationCode}</cbc:IndustryClasificationCode>\n\
         {PartyName}\n\
         <cac:PhysicalLocation>\n\
            <cac:Address>\n\
               <cbc:ID>{PhysicalLocationID}</cbc:ID>\n\
               <cbc:CityName>{PhysicalLocationCityName}</cbc:CityName>\n\
               <cbc:CountrySubentity>{PhysicalLocationCountrySubentity}</cbc:CountrySubentity>\n\
               <cbc:CountrySubentityCode>{PhysicalLocationCountrySubentityCode}</cbc:CountrySubentityCode>\n\
               <cac:AddressLine>\n\
                  <cbc:Line>{PhysicalLocationAddressLine}</cbc:Line>\n\
               </cac:AddressLine>\n\
               <cac:Country>\n\
                  <cbc:IdentificationCode>{CountryIdentificationCode}</cbc:IdentificationCode>\n\
                  <cbc:Name languageID="es">{CountryName}</cbc:Name>\n\
               </cac:Country>\n\
            </cac:Address>\n\
         </cac:PhysicalLocation>\n\
         <cac:PartyTaxScheme>\n\
            <cbc:RegistrationName>{RegistrationName}</cbc:RegistrationName>\n\
            <cbc:CompanyID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="{ProviderIDDV}" schemeName="31">{ProviderID}</cbc:CompanyID>\n\
            <cbc:TaxLevelCode listName="05">{TaxLevelCode}</cbc:TaxLevelCode>\n\
            <cac:RegistrationAddress>\n\
               <cbc:ID>{RegistrationAddressID}</cbc:ID>\n\
               <cbc:CityName>{RegistrationAddressCityName}</cbc:CityName>\n\
               <cbc:CountrySubentity>{RegistrationAddressCountrySubentity}</cbc:CountrySubentity>\n\
               <cbc:CountrySubentityCode>{RegistrationAddressCountrySubentityCode}</cbc:CountrySubentityCode>\n\
               <cac:AddressLine>\n\
                  <cbc:Line>{RegistrationAddressAddressLine}</cbc:Line>\n\
               </cac:AddressLine>\n\
               <cac:Country>\n\
                  <cbc:IdentificationCode>{RegistrationAddressCountryIdentificationCode}</cbc:IdentificationCode>\n\
                  <cbc:Name languageID="es">{RegistrationAddressCountryName}</cbc:Name>\n\
               </cac:Country>\n\
            </cac:RegistrationAddress>\n\
            <cac:TaxScheme>\n\
               <cbc:ID>{TaxSchemeID}</cbc:ID>\n\
               <cbc:Name>{TaxSchemeName}</cbc:Name>\n\
            </cac:TaxScheme>\n\
         </cac:PartyTaxScheme>\n\
         <cac:PartyLegalEntity>\n\
            <cbc:RegistrationName>{RegistrationName}</cbc:RegistrationName>\n\
            <cbc:CompanyID schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="{ProviderIDDV}" schemeName="31">{ProviderID}</cbc:CompanyID>\n\
            <cac:CorporateRegistrationScheme>\n\
               <cbc:ID>SETP</cbc:ID>\n\
               <cbc:Name>10181</cbc:Name>\n\
            </cac:CorporateRegistrationScheme>\n\
         </cac:PartyLegalEntity>\n\
         <cac:Contact>\n\
            <cbc:Name>Eric Valencia</cbc:Name>\n\
            <cbc:Telephone>6111111</cbc:Telephone>\n\
            <cbc:ElectronicMail>eric.valencia@ket.co</cbc:ElectronicMail>\n\
            <cbc:Note>Test descripcion contacto</cbc:Note>\n\
         </cac:Contact>\n\
      </cac:Party>\n\
   </cac:AccountingSupplierParty>\
    ')