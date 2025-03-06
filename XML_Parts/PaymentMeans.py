
def PaymentMeans(
                    PaymentMeansID,
                    PaymentMeansCode,
                    PaymentDueDate
                ):
    return(
        f'\
   <cac:PaymentMeans>\n\
      <cbc:ID>{PaymentMeansID}</cbc:ID>\n\
      <cbc:PaymentMeansCode>{PaymentMeansCode}</cbc:PaymentMeansCode>\n\
      <cbc:PaymentDueDate>{PaymentDueDate}</cbc:PaymentDueDate>\n\
   </cac:PaymentMeans>\n\
    ')