# Karka AI & Tech Academy website · SiteSprint, Karka Infini AI 2026
# Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
"""AWS Lambda entry point: adapts the FastAPI (ASGI) app to Lambda Function URL events."""

import os

os.environ.setdefault("DATA_DIR", "/tmp")  # the only writable path on Lambda

from mangum import Mangum  # noqa: E402

from .main import app  # noqa: E402

handler = Mangum(app, lifespan="off")
