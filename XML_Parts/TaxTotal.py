
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
        f"""<cac:TaxTotal>
      <cbc:TaxAmount currencyID="{currencyID}">{TaxAmount}</cbc:TaxAmount>
      <cac:TaxSubtotal>
         <cbc:TaxableAmount currencyID="{currencyID}">{TaxableAmount}</cbc:TaxableAmount>
         <cbc:TaxAmount currencyID="{currencyID}">{TaxSubtotalTaxAmount}</cbc:TaxAmount>
         <cac:TaxCategory>
            <cbc:Percent>{Percent}</cbc:Percent>
            <cac:TaxScheme>
               <cbc:ID>{TaxSubtotalTaxSchemeID}</cbc:ID>
               <cbc:Name>{TaxSubtotalTaxSchemeName}</cbc:Name>
            </cac:TaxScheme>
         </cac:TaxCategory>
      </cac:TaxSubtotal>
   </cac:TaxTotal>""")