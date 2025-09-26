from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from cryptography.hazmat.primitives import hashes
import base64

# Cargar el .p12
with open("CERT/BILAI S.A.S.p12", "rb") as f:
    data = f.read()
priv, cert, others = pkcs12.load_key_and_certificates(data, b"VsQkyWgLqSuZEJoC")

# DER del certificado
cert_der = cert.public_bytes(Encoding.DER)

# X509Certificate (Base64 sin saltos)
print("<ds:X509Certificate>", base64.b64encode(cert_der).decode("utf-8"), "</ds:X509Certificate>")

# CertDigest (SHA256 sobre DER)
digest = hashes.Hash(hashes.SHA256()); digest.update(cert_der)
print("<ds:DigestValue>", base64.b64encode(digest.finalize()).decode("utf-8"), "</ds:DigestValue>")

# IssuerSerial
print("Issuer:", cert.issuer.rfc4514_string())  # va en <ds:X509IssuerName>
print("SerialNumber (decimal):", cert.serial_number)  # va en <ds:X509SerialNumber>
