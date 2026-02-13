
def VersionXML(
                Type,
                UBLVersionID,
                CustomizationID,
                ProfileID,
                ProfileExecutionID,
                ID,
                UUIDschemeName,
                CUFE,
                IssueDate,
                IssueTime,
                DocumentTypeCode,
                DocumentCurrencyCode,
                LineCountNumeric,
                InvoicePeriodStartDate,
                InvoicePeriodEndDate,
                InvoiceID,
                ResponseCode,
                Description,
                DocumentCUFE,
                DocumentIssueDate
                ):
    if (Type == "Invoice"):
      DocumentTypeCodeBlock      = f"<cbc:InvoiceTypeCode>{DocumentTypeCode}</cbc:InvoiceTypeCode>"
      DiscrepancyResponseBlock   = ""
      BillingReferenceBlock      = ""
    elif (Type == "CreditNote"):
      DocumentTypeCodeBlock      = f"<cbc:CreditNoteTypeCode>{DocumentTypeCode}</cbc:CreditNoteTypeCode>"
      DiscrepancyResponseBlock   = f"""<cac:DiscrepancyResponse>
      <cbc:ReferenceID>{InvoiceID}</cbc:ReferenceID>
      <cbc:ResponseCode>{ResponseCode}</cbc:ResponseCode>
      <cbc:Description>{Description}</cbc:Description>
   </cac:DiscrepancyResponse>"""
      BillingReferenceBlock      = f"""<cac:BillingReference>
      <cac:InvoiceDocumentReference>
         <cbc:ID>{InvoiceID}</cbc:ID>
         <cbc:UUID schemeName="CUFE-SHA384">{DocumentCUFE}</cbc:UUID>
         <cbc:IssueDate>{DocumentIssueDate}</cbc:IssueDate>
      </cac:InvoiceDocumentReference>
   </cac:BillingReference>"""
    elif (Type == "DebitNote"):
      DocumentTypeCodeBlock      = f""
      DiscrepancyResponseBlock   = f"""<cac:DiscrepancyResponse>
      <cbc:ReferenceID>{InvoiceID}</cbc:ReferenceID>
      <cbc:ResponseCode>{ResponseCode}</cbc:ResponseCode>
      <cbc:Description>{Description}</cbc:Description>
   </cac:DiscrepancyResponse>"""
      BillingReferenceBlock      = f"""<cac:BillingReference>
      <cac:InvoiceDocumentReference>
         <cbc:ID>{InvoiceID}</cbc:ID>
         <cbc:UUID schemeName="CUFE-SHA384">{DocumentCUFE}</cbc:UUID>
         <cbc:IssueDate>{DocumentIssueDate}</cbc:IssueDate>
      </cac:InvoiceDocumentReference>
   </cac:BillingReference>"""
      


    return(
        f"""<cbc:UBLVersionID>{UBLVersionID}</cbc:UBLVersionID>
   <cbc:CustomizationID>{CustomizationID}</cbc:CustomizationID>
   <cbc:ProfileID>{ProfileID}</cbc:ProfileID>
   <cbc:ProfileExecutionID>{ProfileExecutionID}</cbc:ProfileExecutionID>
   <cbc:ID>{ID}</cbc:ID>
   <cbc:UUID schemeID="{ProfileExecutionID}" schemeName="{UUIDschemeName}-SHA384">{CUFE}</cbc:UUID>
   <cbc:IssueDate>{IssueDate}</cbc:IssueDate>
   <cbc:IssueTime>{IssueTime}</cbc:IssueTime>
   {DocumentTypeCodeBlock}
   <cbc:DocumentCurrencyCode>{DocumentCurrencyCode}</cbc:DocumentCurrencyCode>
   <cbc:LineCountNumeric>{LineCountNumeric}</cbc:LineCountNumeric>
   <cac:InvoicePeriod>
      <cbc:StartDate>{InvoicePeriodStartDate}</cbc:StartDate>
      <cbc:EndDate>{InvoicePeriodEndDate}</cbc:EndDate>
   </cac:InvoicePeriod>{DiscrepancyResponseBlock}{BillingReferenceBlock}""")