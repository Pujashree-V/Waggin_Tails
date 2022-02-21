#!/bin/bash
#validate the server certificate for the given hostname
echo -e "Server hostname: \c "
read server
if true | openssl s_client -connect $server:443 2>/dev/null | \
  openssl x509 -noout -checkend 0; then
  echo "Certificate is not expired"
else
  echo "Certificate is expired"
fi