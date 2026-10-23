#!/usr/bin/env bash
# Karka AI & Tech Academy · built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
# Build and deploy the site to AWS Lambda with a public Function URL.
# Safe to re-run: creates resources the first time, updates code/config afterwards.
#
#   ./deploy/deploy_lambda.sh                 # defaults below
#   AWS_REGION=ap-southeast-2 FUNCTION=karka-academy ./deploy/deploy_lambda.sh
set -euo pipefail

FUNCTION="${FUNCTION:-karka-academy}"
REGION="${AWS_REGION:-ap-southeast-2}"
ROLE_NAME="${ROLE_NAME:-${FUNCTION}-lambda-role}"
RUNTIME="python3.13"
ARCH="arm64"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$ROOT/deploy/.build"
ZIP="$ROOT/deploy/.build.zip"
PW_FILE="$ROOT/deploy/.admin-password"
export AWS_REGION="$REGION" AWS_PAGER=""
PY="python3"   # any Python 3 with pip; packages install into the build dir, not your env
for v in "$ROOT/.venv" "$ROOT/../.venv"; do [[ -x "$v/bin/python" ]] && { PY="$v/bin/python"; break; }; done
PY="${PYTHON:-$PY}"

say() { printf '\n\033[1;35m▸ %s\033[0m\n' "$*"; }

say "Account: $(aws sts get-caller-identity --query Account --output text) · region $REGION"

# ---------------------------------------------------------------- package
say "Building package (Linux $ARCH wheels for $RUNTIME)"
rm -rf "$BUILD" "$ZIP" && mkdir -p "$BUILD"
"$PY" -m pip install -q -r "$ROOT/requirements-lambda.txt" -t "$BUILD" \
  --platform manylinux2014_aarch64 --implementation cp --python-version 3.13 --only-binary=:all: --upgrade
rsync -a --exclude '__pycache__' --exclude '*.pyc' "$ROOT/app" "$BUILD/"
find "$BUILD" -name '__pycache__' -type d -prune -exec rm -rf {} +
(cd "$BUILD" && zip -qr9 "$ZIP" .)
echo "  $(du -h "$ZIP" | cut -f1) zip"

# ---------------------------------------------------------------- admin password
if [[ -z "${ADMIN_PASSWORD:-}" ]]; then
  [[ -f "$PW_FILE" ]] || openssl rand -base64 18 | tr -d '/+=' > "$PW_FILE"
  ADMIN_PASSWORD="$(cat "$PW_FILE")"
fi
ENV_JSON="{\"Variables\":{\"DATA_DIR\":\"/tmp\",\"ADMIN_PASSWORD\":\"$ADMIN_PASSWORD\"}}"

# ---------------------------------------------------------------- IAM role
if ! ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query Role.Arn --output text 2>/dev/null); then
  say "Creating IAM role $ROLE_NAME"
  ROLE_ARN=$(aws iam create-role --role-name "$ROLE_NAME" \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' \
    --query Role.Arn --output text)
  aws iam attach-role-policy --role-name "$ROLE_NAME" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  echo "  waiting for the role to propagate…"; sleep 12
fi

# ---------------------------------------------------------------- function
if aws lambda get-function --function-name "$FUNCTION" >/dev/null 2>&1; then
  say "Updating code"
  aws lambda update-function-code --function-name "$FUNCTION" --zip-file "fileb://$ZIP" >/dev/null
  aws lambda wait function-updated-v2 --function-name "$FUNCTION"
  say "Updating configuration"
  aws lambda update-function-configuration --function-name "$FUNCTION" \
    --runtime "$RUNTIME" --handler app.lambda_handler.handler --memory-size 1024 --timeout 15 \
    --environment "$ENV_JSON" >/dev/null
  aws lambda wait function-updated-v2 --function-name "$FUNCTION"
else
  say "Creating function $FUNCTION"
  for i in 1 2 3 4 5; do
    aws lambda create-function --function-name "$FUNCTION" --runtime "$RUNTIME" --architectures "$ARCH" \
      --role "$ROLE_ARN" --handler app.lambda_handler.handler --zip-file "fileb://$ZIP" \
      --memory-size 1024 --timeout 15 --environment "$ENV_JSON" >/dev/null && break
    echo "  role not ready yet, retrying ($i)…"; sleep 8
  done
  aws lambda wait function-active-v2 --function-name "$FUNCTION"
fi

# ---------------------------------------------------------------- public Function URL
if ! URL=$(aws lambda get-function-url-config --function-name "$FUNCTION" --query FunctionUrl --output text 2>/dev/null); then
  say "Creating public Function URL"
  URL=$(aws lambda create-function-url-config --function-name "$FUNCTION" --auth-type NONE --query FunctionUrl --output text)
fi
aws lambda add-permission --function-name "$FUNCTION" --statement-id public-url \
  --action lambda:InvokeFunctionUrl --principal '*' --function-url-auth-type NONE >/dev/null 2>&1 || true
aws lambda add-permission --function-name "$FUNCTION" --statement-id public-url-invoke \
  --action lambda:InvokeFunction --principal '*' --invoked-via-function-url >/dev/null 2>&1 || true

say "Smoke test"
for path in "" healthz; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "${URL}${path}")
  echo "  GET /${path}  →  $code"
done

say "Live at: $URL"
echo "  Lead inbox: ${URL}admin/leads  (user: admin, password in deploy/.admin-password)"
