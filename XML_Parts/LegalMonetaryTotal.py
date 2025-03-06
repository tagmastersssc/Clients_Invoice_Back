
def LegalMonetaryTotal(
                        currencyID,
                        LineExtensionAmount,
                        TaxExclusiveAmount,
                        TaxInclusiveAmount,
                        PayableAmount

                     ):
    return(
        f'\
   <cac:LegalMonetaryTotal>\n\
      <cbc:LineExtensionAmount currencyID="{currencyID}">{LineExtensionAmount}</cbc:LineExtensionAmount>\n\
      <cbc:TaxExclusiveAmount currencyID="{currencyID}">{TaxExclusiveAmount}</cbc:TaxExclusiveAmount>\n\
      <cbc:TaxInclusiveAmount currencyID="{currencyID}">{TaxInclusiveAmount}</cbc:TaxInclusiveAmount>\n\
      <cbc:PayableAmount currencyID="{currencyID}">{PayableAmount}</cbc:PayableAmount>\n\
   </cac:LegalMonetaryTotal>\n\
    ')