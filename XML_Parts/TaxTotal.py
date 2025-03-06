
def TaxTotal(
                TaxAmount,
                currencyID,
                TaxableAmount,
                TaxSubtotalTaxAmount,
                Percent,
                TaxSubtotalTaxSchemeID,
                TaxSubtotalTaxSchemeName
                ):
    return(
        f'\
   <cac:TaxTotal>\n\
      <cbc:TaxAmount currencyID="{currencyID}">{TaxAmount}</cbc:TaxAmount>\n\
      <cac:TaxSubtotal>\n\
         <cbc:TaxableAmount currencyID="{currencyID}">{TaxableAmount}</cbc:TaxableAmount>\n\
         <cbc:TaxAmount currencyID="{currencyID}">{TaxSubtotalTaxAmount}</cbc:TaxAmount>\n\
         <cac:TaxCategory>\n\
            <cbc:Percent>{Percent}</cbc:Percent>\n\
            <cac:TaxScheme>\n\
               <cbc:ID>{TaxSubtotalTaxSchemeID}</cbc:ID>\n\
               <cbc:Name>{TaxSubtotalTaxSchemeName}</cbc:Name>\n\
            </cac:TaxScheme>\n\
         </cac:TaxCategory>\n\
      </cac:TaxSubtotal>\n\
   </cac:TaxTotal>\n\
    ')