# Clients_Invoice_Back

Backend dedicado por cliente para BilAI.

## Rol en la arquitectura

- Expone las APIs del tenant (`GenerateInvoice`, `GenerateCreditNote`, `GenerateDebitNote`, `Metrics`, etc.).
- Actúa como **BFF** del `Clients_Invoice_Front`.
- Recibe el `one-time code` desde `Main_Login_Back`.
- Crea la cookie `HttpOnly` local del tenant.

## Endpoints nuevos para el portal

- `GET /api/auth/session/bootstrap`
- `GET /api/session/me`
- `POST /api/session/logout`
- `GET /api/runtime-config`
- `GET /api/runtime-config.js`
- `GET /api/metrics`
- `POST /api/invoices`
- `POST /api/credit-notes`
- `POST /api/debit-notes`

## Variables locales

Usa `local.settings.example.json` como referencia y copia esos valores en tu `local.settings.json`.

Variables importantes:

- `MAIN_LOGIN_BACK_URL`: URL del broker SSO central.
- `BILAI_TENANT_ID`: slug lógico del cliente (`client1`, `client2`, etc.).
- `BILAI_TENANT_EXCHANGE_SECRET`: secreto compartido con `Main_Login_Back`.
- `CLIENTS_FRONT_URL`: dominio real del frontend del cliente.
- `ALLOWED_ORIGINS`: orígenes permitidos para CORS con credenciales.
- `CLIENTS_SESSION_SECRET`: secreto para firmar la sesión local del tenant.
- `RAW_API_BASE_URL`: déjalo vacío si esta misma Function App contiene la lógica de facturación y métricas. Úsalo solo si el BFF debe reenviar a otra API del mismo cliente.

## Flujo

1. `Main_Login_Back` autentica al usuario con SSO.
2. `Main_Login_Back` emite un código corto de un solo uso.
3. El navegador es redirigido a `Clients_Invoice_Back /api/auth/session/bootstrap`.
4. `Clients_Invoice_Back` intercambia ese código contra `Main_Login_Back`.
5. `Clients_Invoice_Back` crea la cookie de sesión del tenant y redirige al `Clients_Invoice_Front`.
