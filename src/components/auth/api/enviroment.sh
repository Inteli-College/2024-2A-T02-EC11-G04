#!/bin/bash

# Generate custom secret
secret_generator() {
    python -c 'import secrets; print(secrets.token_urlsafe(64))'
}

# Create .env and add a base variables
(
    echo '# API dependency variables'
    echo SECRET=$(secret_generator)
    echo ALGORITHM=HS256
    echo POSTGRES_DSN=postgresql+psycopg2://youruser:youpassword@yourhost:5432/yourdatabase
    echo
    echo '# Postgres stuff'
    echo POSTGRES_USER=youruser
    echo POSTGRES_PASSWORD=youpassword
    echo POSTGRES_HOST=yourhost
    echo POSTGRES_PORT=5432
    echo POSTGRES_DATABASE=yourdatabase
) > example.env

echo "ROOT | Example enviroment file and variables created successfully"
