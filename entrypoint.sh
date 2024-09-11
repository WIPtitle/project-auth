#!/bin/sh

cd /app

pip install --upgrade pip

apt-get update && apt-get install -y libpq-dev git
pip install --no-cache-dir -r requirements.txt

CREDENTIALS_FILE=${AUTH_SECRET_KEY_FILE}
echo "Searching secret key in ${AUTH_SECRET_KEY_FILE}"

if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "No secret key found, generating new key..."
    SECRET_KEY=$(openssl rand -base64 32)

    cat <<EOF > "$CREDENTIALS_FILE"
{
  "SECRET_KEY": "SECRET_KEY"
}
EOF
fi

uvicorn app.main:app --host 0.0.0.0 --port 8000
