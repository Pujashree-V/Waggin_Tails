#!/bin/bash
# generate RSA key pair for the test for any host along with
# certificate, public key and private key
echo -e "Algorithm: \c "
read algo
echo -e "Key size: \c "
read size
echo -e "key name: \c "
read keyName
if [ -z "$keyName" ]; then
    echo "\$keyName is empty hence generating with Host Name"
    keyName=$(hostname)
fi
echo -e "Generating key pair for $keyName"
openssl req -newkey $algo:$size -x509 -keyout $keyName-key.pem -out ftadev-cacert.pem -days 3650
openssl rsa -in $keyName-key.pem -out $keyName-prikey.pem
openssl rsa -in $keyName-key.pem -pubout -out $keyName-pubkey.pem
openssl req -key $keyName-prikey.pem -new -out $keyName-cert.csr -days 3650
openssl x509 -signkey $keyName-prikey.pem -in $keyName-cert.csr -req -days 365 -out $keyName-cert.crt

#from pkcs12 keystore output private key and public key
#openssl pkcs12 -in ftacbkeystore.p12 -nodes -nocerts -out ftacbprivate.key
#openssl pkcs12 -in keystore_name.p12 -nokeys -out public-cert-file