#!/usr/bin/env sh
export SSL_CERT="WH_cert.pem"
export SSL_PRIV="WH_pkey.pem"

if [ -n "${WH_HOST}" ]; then

  if [ ! -f WH_pkey.pem ] || [ ! -f WH_cert.pem ]; then
    openssl genrsa -out "$SSL_PRIV" 2048
    openssl req -new -x509 -subj "/C=RU/ST=Moscow/L=Moscow/O=opa/OU=Research team/emailAddress=root@example.com/CN=$WH_HOST" -days 3650 -key $SSL_PRIV -out $SSL_CERT
    echo "Generated ssl key for server mode, host=$WH_HOST"
  fi

fi
python main.py