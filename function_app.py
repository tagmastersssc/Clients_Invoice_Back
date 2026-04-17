import json
import os
import secrets
import time
from http.cookies import SimpleCookie
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import azure.functions as func
import httpx
import jwt
from jwt import InvalidTokenError

from GenerateXML import GenerateXML
from OpenAIAPI import CreateFollowUpResponseAPI, CreateInitialResponseAPI
from TableStorage import GetMetrics
from models import RequestCreditNote, RequestDebitNote, RequestInvoice, RequestMetrics

app = func.FunctionApp()


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def normalize_samesite(value: str | None, default: str = "lax") -> str:
    normalized = (value or default).strip().lower()
    if normalized not in {"lax", "strict", "none"}:
        return default
    return normalized


MAIN_LOGIN_BACK_URL = (os.getenv("MAIN_LOGIN_BACK_URL", "http://localhost:8000") or "http://localhost:8000").strip().rstrip("/")
BILAI_TENANT_ID = (os.getenv("BILAI_TENANT_ID", "bilai-tenant-id") or "bilai-tenant-id").strip()
BILAI_TENANT_EXCHANGE_SECRET = os.getenv("BILAI_TENANT_EXCHANGE_SECRET", "").strip()
CLIENTS_FRONT_URL = (os.getenv("CLIENTS_FRONT_URL", "http://localhost:5174") or "http://localhost:5174").strip()
CLIENTS_SESSION_SECRET = os.getenv("CLIENTS_SESSION_SECRET", "dev-client-session-secret")
CLIENTS_SESSION_TTL_SECONDS = int(os.getenv("CLIENTS_SESSION_TTL_SECONDS", "28800"))
SESSION_COOKIE_NAME = (os.getenv("SESSION_COOKIE_NAME", "bilai_client_session") or "bilai_client_session").strip()
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN", "").strip()
SESSION_COOKIE_PATH = (os.getenv("SESSION_COOKIE_PATH", "/") or "/").strip() or "/"
SESSION_COOKIE_SAMESITE = normalize_samesite(os.getenv("SESSION_COOKIE_SAMESITE"), "lax")
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", False)
VITE_LOGIN_APP_URL = (os.getenv("VITE_LOGIN_APP_URL", "http://localhost:5173") or "http://localhost:5173").strip()
VITE_API_URL = (os.getenv("VITE_API_URL", "/api") or "/api").strip()
VITE_APP_TENANT_ID = (os.getenv("VITE_APP_TENANT_ID", BILAI_TENANT_ID) or BILAI_TENANT_ID).strip()
ALLOWED_ORIGINS = {
    value.strip().rstrip("/")
    for value in ([CLIENTS_FRONT_URL] + os.getenv("ALLOWED_ORIGINS", "").split(","))
    if value.strip()
}
RAW_API_BASE_URL = os.getenv("RAW_API_BASE_URL", "").strip()
RAW_API_KEY = os.getenv("RAW_API_KEY", "").strip()
RAW_API_KEY_IN_HEADER = env_bool("RAW_API_KEY_IN_HEADER", False)
RAW_API_KEY_HEADER_NAME = (os.getenv("RAW_API_KEY_HEADER_NAME", "x-functions-key") or "x-functions-key").strip()
try:
    RAW_API_TIMEOUT_SECONDS = float(os.getenv("RAW_API_TIMEOUT_SECONDS", "15"))
except ValueError:
    RAW_API_TIMEOUT_SECONDS = 15.0


def _request_origin(req: func.HttpRequest) -> str:
    forwarded_proto = req.headers.get("x-forwarded-proto", "").split(",")[0].strip()
    parsed = urlsplit(req.url)
    scheme = forwarded_proto or parsed.scheme or "http"
    return f"{scheme}://{parsed.netloc}"


def _is_secure_request(req: func.HttpRequest) -> bool:
    forwarded_proto = req.headers.get("x-forwarded-proto", "").split(",")[0].strip().lower()
    parsed = urlsplit(req.url)
    return forwarded_proto == "https" or parsed.scheme == "https"


def _append_path_to_url(base_url: str, path: str) -> str:
    parsed = urlsplit(base_url)
    normalized_path = f"{parsed.path.rstrip('/')}/{path.lstrip('/')}" if parsed.path else f"/{path.lstrip('/')}"
    return urlunsplit((parsed.scheme, parsed.netloc, normalized_path, "", ""))


def _runtime_config_payload() -> dict[str, str]:
    return {
        "VITE_API_URL": VITE_API_URL,
        "VITE_LOGIN_APP_URL": VITE_LOGIN_APP_URL,
        "VITE_APP_TENANT_ID": VITE_APP_TENANT_ID,
    }


def _runtime_config_js(payload: dict[str, str]) -> str:
    config_json = json.dumps(payload, ensure_ascii=False)
    return (
        "window.__BILAI_RUNTIME_CONFIG__ = "
        f"Object.assign({{}}, window.__BILAI_RUNTIME_CONFIG__ || {{}}, {config_json});"
    )


def _cors_headers(req: func.HttpRequest) -> dict[str, str]:
    origin = req.headers.get("Origin", "").strip().rstrip("/")
    if not origin or origin not in ALLOWED_ORIGINS:
        return {}
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
        "Vary": "Origin",
    }


def _preflight_response(req: func.HttpRequest, allow_methods: str) -> func.HttpResponse:
    headers = _cors_headers(req)
    requested_headers = req.headers.get("Access-Control-Request-Headers", "").strip()
    headers["Access-Control-Allow-Methods"] = allow_methods
    headers["Access-Control-Allow-Headers"] = requested_headers or "Content-Type, X-CSRF-Token"
    headers["Access-Control-Max-Age"] = "86400"
    return func.HttpResponse(status_code=204, headers=headers)


def _json_response(
    payload: Any,
    *,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
    req: func.HttpRequest | None = None,
) -> func.HttpResponse:
    response_headers = {}
    if req is not None:
        response_headers.update(_cors_headers(req))
    if headers:
        response_headers.update(headers)
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json",
        headers=response_headers or None,
    )


def _text_response(
    body: str,
    *,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
    req: func.HttpRequest | None = None,
) -> func.HttpResponse:
    response_headers = {}
    if req is not None:
        response_headers.update(_cors_headers(req))
    if headers:
        response_headers.update(headers)
    return func.HttpResponse(body, status_code=status_code, headers=response_headers or None)


def _with_cors(response: func.HttpResponse, req: func.HttpRequest) -> func.HttpResponse:
    response.headers.update(_cors_headers(req))
    return response


def _redirect(url: str, *, headers: dict[str, str] | None = None) -> func.HttpResponse:
    response_headers = {"Location": url}
    if headers:
        response_headers.update(headers)
    return func.HttpResponse(status_code=302, headers=response_headers)


def _redirect_with_fragment(url: str, fragment_params: dict[str, str], *, headers: dict[str, str] | None = None) -> func.HttpResponse:
    parsed = urlsplit(url)
    fragment = urlencode({key: value for key, value in fragment_params.items() if value})
    target = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, fragment))
    return _redirect(target, headers=headers)


def _get_cookie_value(req: func.HttpRequest, name: str) -> str:
    raw_cookie = req.headers.get("Cookie", "")
    if not raw_cookie:
        return ""

    jar = SimpleCookie()
    jar.load(raw_cookie)
    morsel = jar.get(name)
    return morsel.value.strip() if morsel else ""


def _get_bearer_token(req: func.HttpRequest) -> str:
    authorization = req.headers.get("Authorization", "").strip()
    if not authorization:
        return ""
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return ""
    return token.strip()


def _build_set_cookie_header(name: str, value: str, *, req: func.HttpRequest, max_age: int) -> str:
    parts = [
        f"{name}={value}",
        f"Max-Age={max_age}",
        f"Path={SESSION_COOKIE_PATH}",
        "HttpOnly",
        f"SameSite={SESSION_COOKIE_SAMESITE.capitalize()}",
    ]
    if SESSION_COOKIE_DOMAIN:
        parts.append(f"Domain={SESSION_COOKIE_DOMAIN}")
    if SESSION_COOKIE_SECURE or _is_secure_request(req):
        parts.append("Secure")
    return "; ".join(parts)


def _build_delete_cookie_header(name: str, *, req: func.HttpRequest) -> str:
    parts = [
        f"{name}=",
        "Max-Age=0",
        "Expires=Thu, 01 Jan 1970 00:00:00 GMT",
        f"Path={SESSION_COOKIE_PATH}",
        "HttpOnly",
        f"SameSite={SESSION_COOKIE_SAMESITE.capitalize()}",
    ]
    if SESSION_COOKIE_DOMAIN:
        parts.append(f"Domain={SESSION_COOKIE_DOMAIN}")
    if SESSION_COOKIE_SECURE or _is_secure_request(req):
        parts.append("Secure")
    return "; ".join(parts)


def _create_client_session_token(*, email: str, first_name: str, last_name: str, name: str, provider: str) -> str:
    now = int(time.time())
    payload = {
        "sub": email,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "name": name,
        "provider": provider,
        "tenant": BILAI_TENANT_ID,
        "csrf": secrets.token_urlsafe(24),
        "iat": now,
        "exp": now + CLIENTS_SESSION_TTL_SECONDS,
    }
    return jwt.encode(payload, CLIENTS_SESSION_SECRET, algorithm="HS256")


def _decode_client_session_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            CLIENTS_SESSION_SECRET,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "sub"]},
        )
    except InvalidTokenError as exc:
        raise PermissionError("Sesión inválida o expirada.") from exc

    tenant = str(payload.get("tenant") or "").strip()
    email = str(payload.get("email") or "").strip()
    if tenant != BILAI_TENANT_ID or "@" not in email:
        raise PermissionError("Sesión inválida.")
    return payload


def _require_portal_session(req: func.HttpRequest) -> dict:
    bearer_token = _get_bearer_token(req)
    if bearer_token:
        return _decode_client_session_token(bearer_token)

    cookie_token = _get_cookie_value(req, SESSION_COOKIE_NAME)
    if not cookie_token:
        raise PermissionError("Falta sesión autenticada.")
    return _decode_client_session_token(cookie_token)


def _serialize_session_user(payload: dict) -> dict[str, str]:
    return {
        "email": str(payload.get("email") or "").strip(),
        "firstName": str(payload.get("first_name") or "").strip(),
        "lastName": str(payload.get("last_name") or "").strip(),
        "name": str(payload.get("name") or "").strip(),
        "provider": str(payload.get("provider") or "").strip(),
        "tenant": str(payload.get("tenant") or "").strip(),
    }


def _require_csrf(req: func.HttpRequest, session: dict) -> None:
    if _get_bearer_token(req):
        return
    expected = str(session.get("csrf") or "").strip()
    provided = req.headers.get("X-CSRF-Token", "").strip()
    if not expected or not provided or not secrets.compare_digest(expected, provided):
        raise PermissionError("No se pudo validar la protección CSRF del portal.")


def _normalize_year_month(year_raw: str | None, month_raw: str | None) -> tuple[str, str]:
    now = time.localtime()
    year_value = year_raw.strip() if isinstance(year_raw, str) else ""
    month_value = month_raw.strip() if isinstance(month_raw, str) else ""

    year_int = now.tm_year if not year_value else int(year_value)
    month_int = now.tm_mon if not month_value else int(month_value)

    if year_int < 2000 or year_int > 2100:
        raise ValueError("El año debe estar entre 2000 y 2100.")
    if month_int < 1 or month_int > 12:
        raise ValueError("El mes debe estar entre 1 y 12.")

    return str(year_int), f"{month_int:02d}"


def _resolve_raw_api_base_url(req: func.HttpRequest) -> str:
    if RAW_API_BASE_URL:
        return RAW_API_BASE_URL.rstrip("/")
    return f"{_request_origin(req)}/api"


def _resolve_raw_api_headers() -> dict[str, str]:
    if RAW_API_KEY_IN_HEADER and RAW_API_KEY:
        return {RAW_API_KEY_HEADER_NAME: RAW_API_KEY}
    return {}


def _resolve_raw_api_query_auth() -> dict[str, str]:
    if RAW_API_KEY_IN_HEADER or not RAW_API_KEY:
        return {}
    return {"code": RAW_API_KEY}


def _request_raw_api(
    req: func.HttpRequest,
    method: str,
    endpoint_name: str,
    *,
    params: dict[str, str] | None = None,
    json_body: Any = None,
) -> httpx.Response:
    base_url = _resolve_raw_api_base_url(req)
    url = f"{base_url}/{endpoint_name.lstrip('/')}"
    query_params = dict(params or {})
    query_params.update(_resolve_raw_api_query_auth())
    response = httpx.request(
        method.upper(),
        url,
        params=query_params or None,
        json=json_body,
        headers=_resolve_raw_api_headers() or None,
        timeout=RAW_API_TIMEOUT_SECONDS,
    )
    return response


def _parse_proxy_response(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text


def _handle_generate_invoice(data: dict, *, req: func.HttpRequest | None = None) -> func.HttpResponse:
    try:
        request_obj = RequestInvoice(**data)
        response_payload = GenerateXML(request_obj, "Invoice")
        return _text_response(str(response_payload), status_code=200, req=req)
    except Exception as exc:  # noqa: BLE001
        return _text_response(f"Error interno: {exc}", status_code=500, req=req)


def _handle_generate_credit_note(data: dict, *, req: func.HttpRequest | None = None) -> func.HttpResponse:
    try:
        request_obj = RequestCreditNote(**data)
        response_payload = GenerateXML(request_obj, "CreditNote")
        return _text_response(str(response_payload), status_code=200, req=req)
    except Exception as exc:  # noqa: BLE001
        return _text_response(f"Error interno: {exc}", status_code=500, req=req)


def _handle_generate_debit_note(data: dict, *, req: func.HttpRequest | None = None) -> func.HttpResponse:
    try:
        request_obj = RequestDebitNote(**data)
        response_payload = GenerateXML(request_obj, "DebitNote")
        return _text_response(str(response_payload), status_code=200, req=req)
    except Exception as exc:  # noqa: BLE001
        return _text_response(f"Error interno: {exc}", status_code=500, req=req)


def _handle_metrics_from_payload(data: dict, *, req: func.HttpRequest | None = None) -> func.HttpResponse:
    try:
        request_obj = RequestMetrics(**data)
        metrics = GetMetrics(request_obj)
        return _text_response(str(metrics), status_code=200, req=req)
    except Exception as exc:  # noqa: BLE001
        return _text_response(f"Error interno: {exc}", status_code=500, req=req)


@app.route(route="runtime-config", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def RuntimeConfig(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "GET, OPTIONS")
    return _json_response(_runtime_config_payload(), req=req)


@app.route(route="runtime-config.js", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def RuntimeConfigJs(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "GET, OPTIONS")
    return func.HttpResponse(
        _runtime_config_js(_runtime_config_payload()),
        status_code=200,
        mimetype="application/javascript",
        headers={"Cache-Control": "no-store", **_cors_headers(req)},
    )


@app.route(route="auth/session/bootstrap", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def BootstrapSession(req: func.HttpRequest) -> func.HttpResponse:
    code = (req.params.get("code") or "").strip()
    tenant = (req.params.get("tenant") or BILAI_TENANT_ID).strip()

    if not code:
        login_url = f"{VITE_LOGIN_APP_URL}?{urlencode({'error': 'Falta el código de acceso.', 'tenant': BILAI_TENANT_ID})}"
        return _redirect(login_url)

    if tenant != BILAI_TENANT_ID:
        login_url = f"{VITE_LOGIN_APP_URL}?{urlencode({'error': 'El tenant solicitado no coincide con este portal.', 'tenant': BILAI_TENANT_ID})}"
        return _redirect(login_url)

    try:
        exchange_response = httpx.post(
            f"{MAIN_LOGIN_BACK_URL}/api/auth/tenant/exchange",
            json={"code": code, "tenant": tenant},
            headers={"X-BilAI-Exchange-Secret": BILAI_TENANT_EXCHANGE_SECRET},
            timeout=15,
        )
    except httpx.HTTPError:
        login_url = f"{VITE_LOGIN_APP_URL}?{urlencode({'error': 'No fue posible validar el acceso con BilAI.', 'tenant': BILAI_TENANT_ID})}"
        return _redirect(login_url)

    if exchange_response.status_code >= 400:
        detail = _parse_proxy_response(exchange_response)
        message = detail.get("detail") if isinstance(detail, dict) else str(detail or "").strip()
        login_url = f"{VITE_LOGIN_APP_URL}?{urlencode({'error': message or 'No fue posible completar el acceso.', 'tenant': BILAI_TENANT_ID})}"
        return _redirect(login_url)

    payload = exchange_response.json()
    user = payload.get("user") if isinstance(payload, dict) else None
    if not isinstance(user, dict):
        login_url = f"{VITE_LOGIN_APP_URL}?{urlencode({'error': 'BilAI devolvió una respuesta inválida al iniciar sesión.', 'tenant': BILAI_TENANT_ID})}"
        return _redirect(login_url)

    session_token = _create_client_session_token(
        email=str(user.get("email") or "").strip(),
        first_name=str(user.get("firstName") or "").strip(),
        last_name=str(user.get("lastName") or "").strip(),
        name=str(user.get("name") or "").strip(),
        provider=str(user.get("provider") or "").strip(),
    )
    return _redirect_with_fragment(
        CLIENTS_FRONT_URL,
        {
            "token": session_token,
            "tenant": BILAI_TENANT_ID,
        },
    )


@app.route(route="session/me", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def GetSession(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "GET, OPTIONS")
    try:
        session = _require_portal_session(req)
    except PermissionError as exc:
        return _json_response({"detail": str(exc)}, status_code=401, req=req)
    return _json_response(
        {
            "authenticated": True,
            "user": _serialize_session_user(session),
            "csrfToken": str(session.get("csrf") or "").strip(),
        },
        req=req,
    )


@app.route(route="session/logout", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def LogoutSession(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "POST, OPTIONS")
    try:
        session = _require_portal_session(req)
        _require_csrf(req, session)
    except PermissionError as exc:
        return _json_response({"detail": str(exc)}, status_code=401, req=req)

    response_headers = dict(_cors_headers(req))
    if not _get_bearer_token(req):
        response_headers["Set-Cookie"] = _build_delete_cookie_header(SESSION_COOKIE_NAME, req=req)
    return func.HttpResponse(status_code=204, headers=response_headers or None)


@app.route(route="metrics", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def PortalMetrics(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "GET, OPTIONS")
    try:
        _require_portal_session(req)
    except PermissionError as exc:
        return _json_response({"detail": str(exc)}, status_code=401, req=req)

    year = req.params.get("year") or req.params.get("Year")
    month = req.params.get("month") or req.params.get("Month")
    try:
        year_value, month_value = _normalize_year_month(year, month)
    except ValueError as exc:
        return _json_response({"detail": str(exc)}, status_code=400, req=req)

    if not RAW_API_BASE_URL:
        try:
            metrics = GetMetrics(RequestMetrics(Year=year_value, Month=month_value))
        except Exception as exc:  # noqa: BLE001
            return _json_response({"detail": f"No fue posible consultar las métricas del tenant: {exc}"}, status_code=502, req=req)
        return _json_response({"year": year_value, "month": month_value, "metrics": metrics}, req=req)

    try:
        response = _request_raw_api(
            req,
            "GET",
            "Metrics",
            params={"Year": year_value, "Month": month_value},
            json_body={"Year": year_value, "Month": month_value},
        )
    except httpx.HTTPError:
        return _json_response({"detail": "No fue posible consultar las métricas del tenant."}, status_code=502, req=req)

    payload = _parse_proxy_response(response)
    if response.status_code >= 400:
        message = payload.get("detail") if isinstance(payload, dict) else str(payload or "").strip()
        return _json_response({"detail": message or "La API del tenant devolvió un error al consultar métricas."}, status_code=502, req=req)

    return _json_response({"year": year_value, "month": month_value, "metrics": payload}, req=req)


@app.route(route="invoices", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def PortalInvoices(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "POST, OPTIONS")
    try:
        session = _require_portal_session(req)
        _require_csrf(req, session)
    except PermissionError as exc:
        return _json_response({"detail": str(exc)}, status_code=401, req=req)

    try:
        data = req.get_json()
    except ValueError:
        return _json_response({"detail": "Invalid JSON body"}, status_code=400, req=req)

    if not RAW_API_BASE_URL:
        return _handle_generate_invoice(data, req=req)

    try:
        response = _request_raw_api(req, "POST", "GenerateInvoice", json_body=data)
    except httpx.HTTPError:
        return _json_response({"detail": "No fue posible registrar la factura en el backend del tenant."}, status_code=502, req=req)

    payload = _parse_proxy_response(response)
    if response.status_code >= 400:
        message = payload.get("detail") if isinstance(payload, dict) else str(payload or "").strip()
        return _json_response({"detail": message or "La API del tenant devolvió un error al registrar la factura."}, status_code=502, req=req)

    if isinstance(payload, (dict, list)):
        return _json_response(payload, req=req)
    return _text_response(str(payload), status_code=200, req=req)


@app.route(route="credit-notes", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def PortalCreditNotes(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "POST, OPTIONS")
    try:
        session = _require_portal_session(req)
        _require_csrf(req, session)
    except PermissionError as exc:
        return _json_response({"detail": str(exc)}, status_code=401, req=req)

    try:
        data = req.get_json()
    except ValueError:
        return _json_response({"detail": "Invalid JSON body"}, status_code=400, req=req)

    if not RAW_API_BASE_URL:
        return _handle_generate_credit_note(data, req=req)

    try:
        response = _request_raw_api(req, "POST", "GenerateCreditNote", json_body=data)
    except httpx.HTTPError:
        return _json_response({"detail": "No fue posible registrar la nota crédito en el backend del tenant."}, status_code=502, req=req)

    payload = _parse_proxy_response(response)
    if response.status_code >= 400:
        message = payload.get("detail") if isinstance(payload, dict) else str(payload or "").strip()
        return _json_response({"detail": message or "La API del tenant devolvió un error al registrar la nota crédito."}, status_code=502, req=req)

    if isinstance(payload, (dict, list)):
        return _json_response(payload, req=req)
    return _text_response(str(payload), status_code=200, req=req)


@app.route(route="debit-notes", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def PortalDebitNotes(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return _preflight_response(req, "POST, OPTIONS")
    try:
        session = _require_portal_session(req)
        _require_csrf(req, session)
    except PermissionError as exc:
        return _json_response({"detail": str(exc)}, status_code=401, req=req)

    try:
        data = req.get_json()
    except ValueError:
        return _json_response({"detail": "Invalid JSON body"}, status_code=400, req=req)

    if not RAW_API_BASE_URL:
        return _handle_generate_debit_note(data, req=req)

    try:
        response = _request_raw_api(req, "POST", "GenerateDebitNote", json_body=data)
    except httpx.HTTPError:
        return _json_response({"detail": "No fue posible registrar la nota débito en el backend del tenant."}, status_code=502, req=req)

    payload = _parse_proxy_response(response)
    if response.status_code >= 400:
        message = payload.get("detail") if isinstance(payload, dict) else str(payload or "").strip()
        return _json_response({"detail": message or "La API del tenant devolvió un error al registrar la nota débito."}, status_code=502, req=req)

    if isinstance(payload, (dict, list)):
        return _json_response(payload, req=req)
    return _text_response(str(payload), status_code=200, req=req)


@app.route(route="GenerateInvoice", methods=["POST"])
def GenerateInvoice(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        return _text_response("Invalid JSON body", status_code=400)
    return _handle_generate_invoice(data)


@app.route(route="GenerateCreditNote", methods=["POST"])
def GenerateCreditNote(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        return _text_response("Invalid JSON body", status_code=400)
    return _handle_generate_credit_note(data)


@app.route(route="GenerateDebitNote", methods=["POST"])
def GenerateDebitNote(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        return _text_response("Invalid JSON body", status_code=400)
    return _handle_generate_debit_note(data)


@app.route(route="Metrics", methods=["GET"])
def Metrics(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        data = {
            "Year": req.params.get("Year") or req.params.get("year") or "",
            "Month": req.params.get("Month") or req.params.get("month") or "",
        }
    return _handle_metrics_from_payload(data)


@app.route(route="CreateInitialResponse", methods=["POST"])
def CreateInitialResponse(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        return _text_response("Invalid JSON body", status_code=400)

    try:
        input_text = data.get("input_text")
        if not input_text:
            return _text_response("Missing 'input_text' in request body", status_code=400)
        response = CreateInitialResponseAPI(input_text)
        return func.HttpResponse(
            response.model_dump_json(indent=2),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        return _text_response(f"Error interno: {exc}", status_code=500)


@app.route(route="CreateFollowUpResponse", methods=["POST"])
def CreateFollowUpResponse(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        return _text_response("Invalid JSON body", status_code=400)

    try:
        previous_response_id = data.get("previous_response_id")
        input_messages = data.get("input_messages")
        if not previous_response_id or not input_messages:
            return _text_response("Missing 'previous_response_id' or 'input_messages' in request body", status_code=400)
        response = CreateFollowUpResponseAPI(previous_response_id, input_messages)
        return func.HttpResponse(
            response.model_dump_json(indent=2),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        return _text_response(f"Error interno: {exc}", status_code=500)
