
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
        f'\
   <cac:InvoiceLine>\n\
      <cbc:ID>{InvoiceLineID}</cbc:ID>\n\
      <cbc:InvoicedQuantity unitCode="{unitCode}">{InvoicedQuantity}</cbc:InvoicedQuantity>\n\
      <cbc:LineExtensionAmount currencyID="{currencyID}">{LineExtensionAmount}</cbc:LineExtensionAmount>\n\
      <cac:AllowanceCharge>\n\
         <cbc:ID>{AllowanceChargeID}</cbc:ID>\n\
         <cbc:ChargeIndicator>{ChargeIndicator}</cbc:ChargeIndicator>\n\
         <cbc:AllowanceChargeReason>{AllowanceChargeReason}</cbc:AllowanceChargeReason>\n\
         <cbc:MultiplierFactorNumeric>{MultiplierFactorNumeric}</cbc:MultiplierFactorNumeric>\n\
         <cbc:Amount currencyID="{currencyID}">{Amount}</cbc:Amount>\n\
         <cbc:BaseAmount currencyID="{currencyID}">{BaseAmount}</cbc:BaseAmount>\n\
      </cac:AllowanceCharge>\n\
      {TaxTotal}\
      <cac:Item>\n\
         <cbc:Description>{ItemDescription}</cbc:Description>\n\
      </cac:Item>\n\
      <cac:Price>\n\
         <cbc:PriceAmount currencyID="{currencyID}">{PriceAmount}</cbc:PriceAmount>\n\
         <cbc:BaseQuantity unitCode="{BaseQuantityUnitCode}">{BaseQuantity}</cbc:BaseQuantity>\n\
      </cac:Price>\n\
   </cac:InvoiceLine>\n\
    ')