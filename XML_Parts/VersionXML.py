
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
                DocumentCurrencyCode,
                LineCountNumeric,
                InvoicePeriodStartDate,
                InvoicePeriodEndDate
                ):
    return(
        f"""<cbc:UBLVersionID>{UBLVersionID}</cbc:UBLVersionID>
   <cbc:CustomizationID>{CustomizationID}</cbc:CustomizationID>
   <cbc:ProfileID>{ProfileID}</cbc:ProfileID>
   <cbc:ProfileExecutionID>{ProfileExecutionID}</cbc:ProfileExecutionID>
   <cbc:ID>{ID}</cbc:ID>
   <cbc:UUID schemeID="2" schemeName="CUFE-SHA384">{CUFE}</cbc:UUID>
   <cbc:IssueDate>{IssueDate}</cbc:IssueDate>
   <cbc:IssueTime>{IssueTime}</cbc:IssueTime>
   <cbc:InvoiceTypeCode>{InvoiceTypeCode}</cbc:InvoiceTypeCode>
   <cbc:DocumentCurrencyCode>{DocumentCurrencyCode}</cbc:DocumentCurrencyCode>
   <cbc:LineCountNumeric>{LineCountNumeric}</cbc:LineCountNumeric>
   <cac:InvoicePeriod>
      <cbc:StartDate>{InvoicePeriodStartDate}</cbc:StartDate>
      <cbc:EndDate>{InvoicePeriodEndDate}</cbc:EndDate>
   </cac:InvoicePeriod>""")