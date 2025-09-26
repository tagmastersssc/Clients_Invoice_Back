
def VersionXML(
                UBLVersionID,
                CustomizationID,
                ProfileID,
                ProfileExecutionID,
                ID,
                CUFE,
                IssueDate,
                IssueTime,
                InvoiceTypeCode,
                Note,
                DocumentCurrencyCode,
                LineCountNumeric,
                InvoicePeriodStartDate,
                InvoicePeriodEndDate
                ):
    return(
        f'\
   <cbc:UBLVersionID>{UBLVersionID}</cbc:UBLVersionID>\n\
   <cbc:CustomizationID>{CustomizationID}</cbc:CustomizationID>\n\
   <cbc:ProfileID>{ProfileID}</cbc:ProfileID>\n\
   <cbc:ProfileExecutionID>{ProfileExecutionID}</cbc:ProfileExecutionID>\n\
   <cbc:ID>{ID}</cbc:ID>\n\
   <cbc:UUID schemeID="2" schemeName="CUFE-SHA384">{CUFE}</cbc:UUID>\n\
   <cbc:IssueDate>{IssueDate}</cbc:IssueDate>\n\
   <cbc:IssueTime>{IssueTime}</cbc:IssueTime>\n\
   <cbc:InvoiceTypeCode>{InvoiceTypeCode}</cbc:InvoiceTypeCode>\n\
   <cbc:Note>{Note}</cbc:Note>\n\
   <cbc:DocumentCurrencyCode>{DocumentCurrencyCode}</cbc:DocumentCurrencyCode>\n\
   <cbc:LineCountNumeric>{LineCountNumeric}</cbc:LineCountNumeric>\n\
   <cac:InvoicePeriod>\n\
      <cbc:StartDate>{InvoicePeriodStartDate}</cbc:StartDate>\n\
      <cbc:EndDate>{InvoicePeriodEndDate}</cbc:EndDate>\n\
   </cac:InvoicePeriod>\n\
    ')