#!/bin/bash


#VsQkyWgLqSuZEJoC

#Obtener certificado publico
openssl pkcs12 -in "BILAI S.A.S.p12" -clcerts -nokeys -legacy -nodes | \
openssl x509 -out publicCert.pem

#Obtener IssuerName
openssl x509 -in publicCert.pem -noout -issuer

#Obtener SerialNumber
openssl x509 -in publicCert.pem -noout -serial

#Obtener certificado privado
openssl pkcs12 -in "BILAI S.A.S.p12" -nocerts -nodes -legacy  \
  | openssl pkey -out privateKey.pem

