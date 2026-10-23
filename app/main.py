# Karka AI & Tech Academy website · SiteSprint, Karka Infini AI 2026
# Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
"""Karka AI & Tech Academy: FastAPI web app."""

from __future__ import annotations

import csv
import hashlib
import hmac
import io
import os
import re
import secrets
import time
from collections import defaultdict, deque
from datetime import date
from pathlib import Path
from typing import Annotated
from urllib.parse import quote

import jinja2
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError, field_validator
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import data, storage
from .icons import icon

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Karka AI & Tech Academy", docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(GZipMiddleware, minimum_size=600)


# ---------------------------------------------------------------------------
# Static files with long-lived caching for fingerprinted URLs
# ---------------------------------------------------------------------------
class CachedStatic(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 200:
            versioned = b"v=" in scope.get("query_string", b"")
            response.headers["Cache-Control"] = (
                "public, max-age=31536000, immutable" if versioned else "public, max-age=3600"
            )
        return response


app.mount("/static", CachedStatic(directory=STATIC_DIR), name="static")

_asset_hashes: dict[str, str] = {}


def asset(path: str) -> str:
    """Return a cache-busting URL for a static file (content hash in the query string)."""
    if path not in _asset_hashes or os.getenv("DEV"):
        file = STATIC_DIR / path
        digest = hashlib.md5(file.read_bytes()).hexdigest()[:10] if file.exists() else "0"
        _asset_hashes[path] = digest
    return f"/static/{path}?v={_asset_hashes[path]}"


_WS = re.compile(r"[ \t\r\n\f]+")
_KEEP = re.compile(r"(<(textarea|pre)\b[^>]*>.*?</\2>)", re.S | re.I)


def minify_html(html: str) -> str:
    """Collapse whitespace runs to a single space so each page ships as one line.

    Browsers already treat any whitespace run as one space, so rendering is unchanged.
    <textarea>/<pre> contents are kept verbatim. Inline scripts must end statements
    with semicolons and avoid `//` comments.
    """
    parts = _KEEP.split(html)
    out = []
    for i in range(0, len(parts), 3):
        out.append(_WS.sub(" ", parts[i]))
        if i + 1 < len(parts):
            out.append(parts[i + 1])
    return "".join(out).strip()


class MinifiedTemplate(jinja2.Template):
    def render(self, *args, **kwargs):
        return minify_html(super().render(*args, **kwargs))


def _origin(request: Request) -> dict:
    """Absolute links (canonical, og:image, sitemap) follow whatever domain serves the site."""
    return {"origin": str(request.base_url).rstrip("/")}


templates = Jinja2Templates(directory=BASE_DIR / "templates", context_processors=[_origin])
templates.env.template_class = MinifiedTemplate
templates.env.globals.update(
    asset=asset,
    icon=icon,
    site=data.SITE,
    nav=data.NAV,
    year=date.today().year,
    courses=data.COURSES,
    program_choices=data.PROGRAM_CHOICES,
    audiences=data.AUDIENCES,
)
templates.env.filters["urlquote"] = lambda s: quote(str(s))


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    return response


# ---------------------------------------------------------------------------
# Leads
# ---------------------------------------------------------------------------
PHONE_RE = re.compile(r"^(?:\+?91|0)?([6-9]\d{9})$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class LeadIn(BaseModel):
    name: str
    phone: str
    email: str = ""
    program: str
    audience: str = ""
    message: str = ""
    source: str = ""
    company: str = ""  # honeypot: humans never see this field

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        v = " ".join(v.split())
        if not 2 <= len(v) <= 80:
            raise ValueError("Please enter your name.")
        return v

    @field_validator("phone")
    @classmethod
    def _phone(cls, v: str) -> str:
        m = PHONE_RE.match(re.sub(r"[\s\-()]", "", v))
        if not m:
            raise ValueError("Enter a valid 10-digit mobile number.")
        return f"+91{m.group(1)}"

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        v = v.strip()
        if v and (len(v) > 120 or not EMAIL_RE.match(v)):
            raise ValueError("That email doesn't look right.")
        return v

    @field_validator("program")
    @classmethod
    def _program(cls, v: str) -> str:
        v = v.strip()
        if v in data.COURSES:  # accept a slug too
            v = data.COURSES[v]["name"]
        if v not in data.PROGRAM_CHOICES:
            raise ValueError("Pick a program.")
        return v

    @field_validator("audience")
    @classmethod
    def _audience(cls, v: str) -> str:
        v = v.strip()
        if v and v not in data.AUDIENCES:
            raise ValueError("Pick one option.")
        return v

    @field_validator("message", "source")
    @classmethod
    def _trim(cls, v: str) -> str:
        return v.strip()[:1000]


_hits: dict[str, deque] = defaultdict(deque)
RATE_LIMIT, RATE_WINDOW = 6, 600  # 6 submissions per 10 minutes per IP


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    return fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "?")


def _rate_limited(request: Request, bucket: dict[str, deque] = _hits, limit: int = RATE_LIMIT) -> bool:
    now, q = time.monotonic(), bucket[_client_ip(request)]
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= limit:
        return True
    q.append(now)
    return False


def _errors(exc: ValidationError) -> dict[str, str]:
    out: dict[str, str] = {}
    for err in exc.errors():
        field = str(err["loc"][0]) if err["loc"] else "form"
        msg = err["msg"].removeprefix("Value error, ")
        out.setdefault(field, "This field is required." if err["type"] == "missing" else msg)
    return out


def _accept(lead: LeadIn) -> int | None:
    if lead.company:  # bot filled the honeypot: pretend success, store nothing
        return None
    return storage.save_lead(lead.model_dump(exclude={"company"}))


@app.post("/api/leads", status_code=201)
async def create_lead(request: Request):
    if _rate_limited(request):
        return JSONResponse({"ok": False, "errors": {"form": "Too many attempts. Please try again in a few minutes."}}, 429)
    try:
        payload = await request.json()
        lead = LeadIn.model_validate(payload if isinstance(payload, dict) else {})
    except ValidationError as exc:
        return JSONResponse({"ok": False, "errors": _errors(exc)}, 422)
    except ValueError:
        return JSONResponse({"ok": False, "errors": {"form": "Invalid request."}}, 400)
    lead_id = _accept(lead)
    return {"ok": True, "id": lead_id, "first_name": lead.name.split()[0]}


@app.post("/apply", response_class=HTMLResponse)
async def apply_submit(request: Request):
    """No-JS fallback for every lead form on the site."""
    form = dict(await request.form())
    values = {k: str(v) for k, v in form.items()}
    if _rate_limited(request):
        return templates.TemplateResponse(
            request, "apply.html", {"values": values, "errors": {"form": "Too many attempts. Please try again later."}}, 429
        )
    try:
        lead = LeadIn.model_validate(values)
    except ValidationError as exc:
        return templates.TemplateResponse(request, "apply.html", {"values": values, "errors": _errors(exc)}, 422)
    _accept(lead)
    return RedirectResponse(f"/thank-you?name={quote(lead.name.split()[0])}", status.HTTP_303_SEE_OTHER)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def _client_data() -> dict:
    """Small JSON payload the front-end needs (track finder, program names)."""
    return {
        "quiz": data.QUIZ,
        "pick": data.TRACK_PICK,
        "tracks": {t["id"]: {"name": t["name"], "tagline": t["tagline"]} for t in data.TRACKS},
        "courses": {s: {"name": c["name"], "featured": c["featured"], "duration": c.get("duration")} for s, c in data.COURSES.items()},
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "d": data,
            "client_data": _client_data(),
            "page_path": "/",
        },
    )


@app.get("/courses/{slug}", response_class=HTMLResponse)
async def course_detail(request: Request, slug: str):
    course = data.COURSES.get(slug)
    if not course:
        raise HTTPException(404)
    if not course["featured"]:
        return RedirectResponse(f"/apply?program={slug}", status.HTTP_307_TEMPORARY_REDIRECT)
    related = [c for c in data.FEATURED if c["slug"] != slug][:3]
    return templates.TemplateResponse(
        request,
        "course.html",
        {"d": data, "course": course, "related": related, "page_path": f"/courses/{slug}"},
    )


@app.get("/apply", response_class=HTMLResponse)
async def apply_page(request: Request, program: str = ""):
    course = data.COURSES.get(program)
    values = {"program": course["name"] if course else ""}
    return templates.TemplateResponse(request, "apply.html", {"values": values, "errors": {}, "page_path": "/apply"})


@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request, name: str = ""):
    return templates.TemplateResponse(request, "thank_you.html", {"name": name[:40]})


@app.get("/api/courses")
async def api_courses():
    return {"tracks": data.TRACKS, "courses": data.COURSES}


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots(request: Request):
    return f"User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: {_origin(request)['origin']}/sitemap.xml\n"


@app.get("/sitemap.xml")
async def sitemap(request: Request):
    paths = ["/", "/apply"] + [f"/courses/{c['slug']}" for c in data.FEATURED]
    today = date.today().isoformat()
    origin = _origin(request)["origin"]
    urls = "".join(f"<url><loc>{origin}{p}</loc><lastmod>{today}</lastmod></url>" for p in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, media_type="application/xml")


@app.get("/manifest.webmanifest")
async def manifest():
    return JSONResponse(
        {
            "name": data.SITE["name"],
            "short_name": "Karka",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#1a0620",
            "theme_color": "#2b0a33",
            "icons": [
                {"src": "/static/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "/static/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
            ],
        },
        media_type="application/manifest+json",
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse("/static/img/icon-48.png", status.HTTP_301_MOVED_PERMANENTLY)


# ---------------------------------------------------------------------------
# Admin: lightweight lead inbox (enabled only when ADMIN_PASSWORD is set)
#
# Browsers sign in through /admin/login and get a signed, HttpOnly session cookie.
# (HTTP Basic's browser pop-up can't be used behind Lambda Function URLs, which
# rename the WWW-Authenticate header.) Basic auth still works for scripts/curl.
# ---------------------------------------------------------------------------
security = HTTPBasic(auto_error=False)
ADMIN_COOKIE = "karka_admin"
ADMIN_TTL = 12 * 3600
_login_hits: dict[str, deque] = defaultdict(deque)


class AdminLoginRequired(Exception):
    """Raised when a browser needs to sign in; redirects to the login page."""


def _admin_password() -> str:
    password = os.getenv("ADMIN_PASSWORD")
    if not password:
        raise HTTPException(404)
    return password


def _session_token(expires: int, password: str) -> str:
    # Keyed with the password, so changing ADMIN_PASSWORD signs everyone out.
    mac = hmac.new(password.encode(), f"karka-admin:{expires}".encode(), hashlib.sha256).hexdigest()
    return f"{expires}.{mac}"


def _valid_session(token: str | None, password: str) -> bool:
    try:
        expires = int((token or "").split(".", 1)[0])
    except ValueError:
        return False
    return expires > time.time() and secrets.compare_digest(token, _session_token(expires, password))


def _safe_next(path: str) -> str:
    return path if path.startswith("/admin/") and not path.startswith("/admin/log") else "/admin/leads"


def require_admin(request: Request, creds: Annotated[HTTPBasicCredentials | None, Depends(security)]) -> None:
    password = _admin_password()
    if _valid_session(request.cookies.get(ADMIN_COOKIE), password):
        return
    if creds is not None and secrets.compare_digest(creds.username, os.getenv("ADMIN_USER", "admin")) \
            and secrets.compare_digest(creds.password, password):
        return
    raise AdminLoginRequired(request.url.path)


@app.exception_handler(AdminLoginRequired)
async def admin_login_redirect(request: Request, exc: AdminLoginRequired):
    return RedirectResponse(f"/admin/login?next={quote(exc.args[0])}", status.HTTP_303_SEE_OTHER)


@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request, next: str = "/admin/leads"):
    password = _admin_password()
    if _valid_session(request.cookies.get(ADMIN_COOKIE), password):
        return RedirectResponse(_safe_next(next), status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "admin_login.html", {"next": _safe_next(next), "error": ""})


@app.post("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    password = _admin_password()
    form = await request.form()
    target = _safe_next(str(form.get("next", "")))
    if _rate_limited(request, _login_hits, limit=8):
        return templates.TemplateResponse(request, "admin_login.html",
                                          {"next": target, "error": "Too many attempts. Try again in a few minutes."}, 429)
    if not secrets.compare_digest(str(form.get("password", "")), password):
        return templates.TemplateResponse(request, "admin_login.html", {"next": target, "error": "Wrong password."}, 401)
    expires = int(time.time()) + ADMIN_TTL
    response = RedirectResponse(target, status.HTTP_303_SEE_OTHER)
    response.set_cookie(ADMIN_COOKIE, _session_token(expires, password), max_age=ADMIN_TTL, path="/admin",
                        httponly=True, samesite="strict", secure=request.url.scheme == "https")
    return response


@app.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse("/admin/login", status.HTTP_303_SEE_OTHER)
    response.delete_cookie(ADMIN_COOKIE, path="/admin")
    return response


@app.get("/admin/leads", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_leads(request: Request):
    return templates.TemplateResponse(request, "admin.html", {"leads": storage.list_leads()})


@app.get("/admin/leads.csv", dependencies=[Depends(require_admin)])
async def admin_leads_csv():
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=storage.FIELDS)
    writer.writeheader()
    writer.writerows(storage.list_leads(limit=100_000))
    return Response(buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=karka-leads.csv"})


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------
@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and not request.url.path.startswith(("/api", "/static")):
        return templates.TemplateResponse(request, "404.html", {}, 404)
    return JSONResponse({"detail": exc.detail}, exc.status_code, headers=getattr(exc, "headers", None))
