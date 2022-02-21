#!/bin/bash
# look at the contents of the certificate
# verify the certificate
echo -e "Give csr file name: \c "
read csrFile
printf "Certificate Contents...\n\n" 
openssl req -text -noout -verify -in $csrFile.csr
# verify the certificate
printf "Certificate Verification...\n\n"
openssl x509 -text -noout -in $csrFile.crt
# get the month date and year from the public key for validation
read crtdate < <(openssl x509 -text -noout -in $csrFile.crt | grep "Not After")

read month day year < <(date "+%m %d %Y")