# Web eID test authentication token generator

A Python script that generates arbitrary Web eID authentication tokens for
testing using either `pkcs11-tool` or Estonian Mobile-ID.

## Prerequisites

* Python 3.8+,
* When using `pkcs11-tool` mode,
  * OpenSC installed,
  * electronic ID card connected that is supported by OpenSC.

The script has only been tested on Ubuntu Linux.

## Usage

The `authtoken-generator.py` script is only a quick rough helper and needs to
be manually amended for it to work. It can be configured by changing the values
of the global variables in the script.

### Usage in `pkcs11-tool` mode

1. Run `pkcs11-tool -M` to see which algorithms are supported by the ID card.
2. Run `pkcs11-tool -O` to see which objects (keys) are available on the ID card.
3. Edit `python authtoken-generator.py`:
   1. Change `PAYLOAD` as needed.
   2. Change `HASH_ALGO`, `ALGORITHM` and `MECHANISM` to match the algorithm used in signing (step 1);
      use algorithm names from [RFC 7518, section 3](https://tools.ietf.org/html/rfc7518#section-3),
      e.g. *ES384* for `ALGORITHM`, copy-paste `MECHANISM` from step 1.
   3. Change `OBJECT_ID` to match the ID of the signing key (step 2).
   4. Change `PIN` to match the signing key PIN.
   5. Make sure `EID` is initialized with `PKCS11ElectronicID`.
4. Run `python authtoken-generator.py`.

Optional:

* Change `SLOT_INDEX` to use the signing certificate.
* Set the `USER_CERTIFICATE` value to a base64-encoded certificate to use a custom certificate.
  Otherwise the certificate is read from the card by default.

### Usage in Mobile-ID mode

1. Create and activate virtual environment, install the Mobile-ID service client library:
   ```py
   python -m venv venv
   . venv/bin/activate # . venv/Scripts/activate in Windows
   pip install git+https://github.com/web-eid/mobile-id-rest-python-client
   ```
2. Edit `python authtoken-generator.py`:
   1. Make sure `EID` is initialized with `MobileIDElectronicID` in `python authtoken-generator.py`.
   2. Pass the following arguments to `MobileIDElectronicID` constructor:
      1. `service_name`: Mobile-ID service name, e.g. 'MyCompany',
      2. `service_uuid`: Mobile-ID service UUID, e.g. '09c14dbb-f882-4a53-9a68-335940150f01',
      3. `user_phone_number`: Phone number of the person who authenticates, e.g. '51234567',
      4. `user_id_code`: ID code of the person who authenticates, e.g. '38001085718'.
3. Run `python authtoken-generator.py`.
