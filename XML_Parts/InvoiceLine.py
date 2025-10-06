
def InvoiceLine(
                  InvoiceLineID,
                  InvoicedQuantity,
                  unitCode,
                  LineExtensionAmount,
                  currencyID,
                  AllowanceChargeID,
                  ChargeIndicator,
                  AllowanceChargeReason,
                  MultiplierFactorNumeric,
                  Amount,
                  BaseAmount,
                  TaxTotal,
                  ItemDescription,
                  PriceAmount,
                  BaseQuantity,
                  BaseQuantityUnitCode
               ):
    return(
        f"""<cac:InvoiceLine>
      <cbc:ID>{InvoiceLineID}</cbc:ID>
      <cbc:InvoicedQuantity unitCode="{unitCode}">{InvoicedQuantity}</cbc:InvoicedQuantity>
      <cbc:LineExtensionAmount currencyID="{currencyID}">{LineExtensionAmount}</cbc:LineExtensionAmount>
      {TaxTotal}\
      <cac:Item>
         <cbc:Description>{ItemDescription}</cbc:Description>
         <cac:StandardItemIdentification>
            <cbc:ID schemeID="999" schemeName="Estándar de adopción del contribuyente">2374860038</cbc:ID>
         </cac:StandardItemIdentification>
      </cac:Item>
      <cac:Price>
         <cbc:PriceAmount currencyID="{currencyID}">{PriceAmount}</cbc:PriceAmount>
         <cbc:BaseQuantity unitCode="{BaseQuantityUnitCode}">{BaseQuantity}</cbc:BaseQuantity>
      </cac:Price>
   </cac:InvoiceLine>""")


#StandardItemIdentification revisar

#Agregar en caso de descuento
# <cac:AllowanceCharge>
#          <cbc:ID>{AllowanceChargeID}</cbc:ID>
#          <cbc:ChargeIndicator>{ChargeIndicator}</cbc:ChargeIndicator>
#          <cbc:AllowanceChargeReason>{AllowanceChargeReason}</cbc:AllowanceChargeReason>
#          <cbc:MultiplierFactorNumeric>{MultiplierFactorNumeric}</cbc:MultiplierFactorNumeric>
#          <cbc:Amount currencyID="{currencyID}">{Amount}</cbc:Amount>
#          <cbc:BaseAmount currencyID="{currencyID}">{BaseAmount}</cbc:BaseAmount>
#       </cac:AllowanceCharge>