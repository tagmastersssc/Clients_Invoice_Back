
def PaymentMeans(
                    PaymentMeansID,
                    PaymentMeansCode,
                    PaymentDueDate
                ):
    return(
        f"""<cac:PaymentMeans>
      <cbc:ID>{PaymentMeansID}</cbc:ID>
      <cbc:PaymentMeansCode>{PaymentMeansCode}</cbc:PaymentMeansCode>
      <cbc:PaymentDueDate>{PaymentDueDate}</cbc:PaymentDueDate>
   </cac:PaymentMeans>""")