# Web eID test authentication token generator

A Python script that generates arbitrary Web eID authentication tokens for
testing using `pkcs11-tool`.

## Prerequisites

* Python 3.8+,
* OpenSC installed,
* connected electronic ID card that is supported by OpenSC,
* the script has only been tested on Ubuntu.

## Usage

The `authtoken-generator.py` script is only a quick rough helper and needs to
be manually amended for it to work. It can be configured by changing the values
of the global variables in the script.

1. Run `pkcs11-tool -M` to see which algorithms are supported by the ID card.
2. Run `pkcs11-tool -O` to see which objects (keys) are available on the ID card.
3. Change `PAYLOAD` as needed.
4. Change `HASH_ALGO`, `ALGORITHM` and `MECHANISM` to match the algorithm used in signing (step 1);
   use algorithm names from [RFC 7518, section 3](https://tools.ietf.org/html/rfc7518#section-3),
   e.g. *ES384* for `ALGORITHM`, copy-paste `MECHANISM` from step 1.
5. Change `OBJECT_ID` to match the ID of the signing key (step 2).
6. Change `PIN` to match the signing key PIN.
7. Run `python authtoken-generator.py`.

Optional:

* Change `SLOT_INDEX` to use the signing certificate.
* Set the `USER_CERTIFICATE` value to a base64-encoded certificate to use a custom certificate.
  Otherwise the certificate is read from the card by default.
