# Karka AI & Tech Academy website · SiteSprint, Karka Infini AI 2026
# Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
import importlib
import re

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    from app import main, storage

    importlib.reload(storage)
    importlib.reload(main)
    main._hits.clear()
    return TestClient(main.app)


VALID = {"name": "Priya S", "phone": "98765 43210", "email": "priya@example.com",
         "program": "MERN Fullstack Development", "audience": "Graduate", "message": "Hi"}


def test_home_renders_key_sections(client):
    r = client.get("/")
    assert r.status_code == 200
    html = r.text
    for marker in ['id="pap"', 'id="tracks"', 'id="internship"', 'id="placements"', 'id="faq"', 'id="apply"',
                   "Subashini M", "DigitKode", "Pay after you", "FAQPage", 'id="karka-data"']:
        assert marker in html, marker
    css_url = re.search(r'href="(/static/css/main\.css\?v=[0-9a-f]+)"', html).group(1)
    assert "immutable" in client.get(css_url).headers["cache-control"]


def test_brand_assets_render(client):
    html = client.get("/").text
    assert "img/karka-logo-light.webp" in html and "img/mascot-640.webp" in html
    assert 'fetchpriority="high"' in html          # hero mascot loads first
    assert 'alt="amazon"' in html and ">DigitKode<" in html   # logo + text-wordmark partners
    for path in ["img/logos/amazon.webp", "img/icon-32.png", "img/mascot-320.webp"]:
        assert client.get(f"/static/{path}").status_code == 200
    assert client.get("/favicon.ico", follow_redirects=False).headers["location"] == "/static/img/icon-48.png"


def test_html_is_single_line_and_keeps_textarea(client):
    html = client.get("/").text
    assert "\n" not in html and "  " not in html
    r = client.post("/apply", data={**VALID, "phone": "1", "message": "line one\n\n  line two"})
    assert "line one\n\n  line two</textarea>" in r.text


def test_video_testimonials(client):
    html = client.get("/").text
    assert html.count('class="rl"') == 5 and "Prabin Raj" in html and 'preload="none"' in html
    r = client.get(re.search(r'src="(/static/video/gabriel\.mp4\?v=[0-9a-f]+)"', html).group(1), headers={"Range": "bytes=0-1023"})
    assert r.status_code == 206 and len(r.content) == 1024


def test_footer_map_and_credit(client):
    html = client.get("/").text
    assert 'class="ftr__map"' in html and "google.com/maps/embed" in html and 'loading="lazy"' in html
    assert "Athokpam Yaraba Luwang" in html and "linkedin.com/in/yaraba-athokpam-856538343" in html


def test_absolute_urls_follow_serving_domain(client):
    html = client.get("/", headers={"host": "demo.example.com"}).text
    assert 'og:image" content="http://demo.example.com/static/img/og.jpg"' in html
    assert 'rel="canonical" href="http://demo.example.com/"' in html
    assert "http://demo.example.com/courses/mern-fullstack" in client.get("/sitemap.xml", headers={"host": "demo.example.com"}).text


def test_course_pages(client):
    assert client.get("/courses/mern-fullstack").status_code == 200
    assert '"@type": "Course"' in client.get("/courses/ui-ux-design").text
    r = client.get("/courses/tally", follow_redirects=False)
    assert r.status_code == 307 and r.headers["location"] == "/apply?program=tally"
    assert client.get("/courses/nope").status_code == 404


def test_apply_page_preselects_program(client):
    r = client.get("/apply?program=ai-data-science")
    assert r.status_code == 200
    assert '<option value="AI &amp; Data Science" selected>' in r.text


def test_api_lead_success_and_storage(client):
    from app import storage

    r = client.post("/api/leads", json=VALID)
    assert r.status_code == 201, r.text
    assert r.json() == {"ok": True, "id": 1, "first_name": "Priya"}
    lead = storage.list_leads()[0]
    assert lead["phone"] == "+919876543210" and lead["program"] == "MERN Fullstack Development"


def test_api_lead_accepts_slug_for_program(client):
    r = client.post("/api/leads", json={**VALID, "program": "ui-ux-design"})
    assert r.status_code == 201


def test_api_lead_validation_errors(client):
    r = client.post("/api/leads", json={**VALID, "phone": "12345", "email": "nope", "program": "Cooking"})
    assert r.status_code == 422
    errs = r.json()["errors"]
    assert set(errs) == {"phone", "email", "program"}
    r = client.post("/api/leads", json={})
    assert r.status_code == 422 and "name" in r.json()["errors"]


def test_honeypot_is_not_stored(client):
    from app import storage

    r = client.post("/api/leads", json={**VALID, "company": "spam inc"})
    assert r.status_code == 201
    assert storage.list_leads() == []


def test_rate_limit(client):
    for _ in range(6):
        assert client.post("/api/leads", json=VALID).status_code == 201
    assert client.post("/api/leads", json=VALID).status_code == 429


def test_form_post_fallback(client):
    r = client.post("/apply", data=VALID, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/thank-you?name=Priya")
    r = client.post("/apply", data={**VALID, "phone": "1"})
    assert r.status_code == 422 and "Enter a valid 10-digit mobile number." in r.text


def test_seo_endpoints(client):
    assert "Sitemap:" in client.get("/robots.txt").text
    sm = client.get("/sitemap.xml")
    assert sm.headers["content-type"].startswith("application/xml") and "/courses/mern-fullstack" in sm.text
    assert client.get("/manifest.webmanifest").json()["short_name"] == "Karka"
    assert client.get("/healthz").json() == {"ok": True}


def test_404_page(client):
    r = client.get("/does-not-exist")
    assert r.status_code == 404 and "got placed" in r.text


def test_admin_disabled_without_password(client, monkeypatch):
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    assert client.get("/admin/leads").status_code == 404


def test_admin_login_flow(client, monkeypatch):
    monkeypatch.setenv("ADMIN_PASSWORD", "s3cret")
    client.post("/api/leads", json=VALID)
    r = client.get("/admin/leads", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/admin/login?next=/admin/leads"
    assert client.post("/admin/login", data={"password": "nope"}).status_code == 401
    r = client.post("/admin/login", data={"password": "s3cret", "next": "/admin/leads"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/admin/leads"
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie and "path=/admin" in cookie
    assert "Priya S" in client.get("/admin/leads").text          # session cookie carried
    assert "Priya S" in client.get("/admin/leads.csv").text
    client.get("/admin/logout")
    assert client.get("/admin/leads", follow_redirects=False).status_code == 303


def test_admin_login_blocks_open_redirect_and_bruteforce(client, monkeypatch):
    monkeypatch.setenv("ADMIN_PASSWORD", "s3cret")
    r = client.post("/admin/login", data={"password": "s3cret", "next": "https://evil.example"}, follow_redirects=False)
    assert r.headers["location"] == "/admin/leads"
    client.cookies.clear()
    codes = [client.post("/admin/login", data={"password": "x"}).status_code for _ in range(9)]
    assert codes[-1] == 429


def test_admin_requires_auth(client, monkeypatch):
    monkeypatch.setenv("ADMIN_PASSWORD", "s3cret")
    assert client.get("/admin/leads", follow_redirects=False).status_code == 303
    client.post("/api/leads", json=VALID)
    r = client.get("/admin/leads", auth=("admin", "s3cret"))
    assert r.status_code == 200 and "Priya S" in r.text
    csv = client.get("/admin/leads.csv", auth=("admin", "s3cret"))
    assert csv.status_code == 200 and "Priya S" in csv.text


def test_security_headers_and_gzip(client):
    r = client.get("/", headers={"Accept-Encoding": "gzip"})
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers.get("content-encoding") == "gzip"
