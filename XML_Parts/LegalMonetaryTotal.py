
def LegalMonetaryTotal(
                        currencyID,
                        LineExtensionAmount,
                        TaxExclusiveAmount,
                        TaxInclusiveAmount,
                        PayableAmount

                     ):
    return(
        f"""<cac:LegalMonetaryTotal>
      <cbc:LineExtensionAmount currencyID="{currencyID}">{LineExtensionAmount}</cbc:LineExtensionAmount>
      <cbc:TaxExclusiveAmount currencyID="{currencyID}">{TaxExclusiveAmount}</cbc:TaxExclusiveAmount>
      <cbc:TaxInclusiveAmount currencyID="{currencyID}">{TaxInclusiveAmount}</cbc:TaxInclusiveAmount>
      <cbc:PayableAmount currencyID="{currencyID}">{PayableAmount}</cbc:PayableAmount>
   </cac:LegalMonetaryTotal>""")