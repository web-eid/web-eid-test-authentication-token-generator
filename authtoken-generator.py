"""
A Python script that generates arbitrary Web eID authentication tokens for
testing using either pkcs11-tool or Mobile-ID.

Copyright (c) 2020 The Web eID Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import base64
import hashlib
import json
from lib.pkcs11_tool import PKCS11ElectronicID

# Leave empty to read from card or add as base64-encoded to use a modified certificate
USER_CERT = ""
ALGORITHM = "ES256"
SLOT_INDEX = "00"
OBJECT_ID = "01"
PIN = "1234"
MECHANISM = "ECDSA"
HASH_ALGO = hashlib.sha256
PAYLOAD = {
    "aud": [
        "https://ria.ee",
        "urn:cert:sha-256:6f0df244e4a856b94b3b3b47582a0a51a32d674dbc7107211ed23d4bec6d9c72",
    ],
    "exp": "1586871169",
    "iat": "1586870869",
    "iss": "web-eid app v0.9.0-1-ge6e89fa",
    "nonce": "12345678123456781234567812345678",
    "sub": "JÕEORG,JAAK-KRISTJAN,38001085718",
}

EID = PKCS11ElectronicID(
    slot_index=SLOT_INDEX,
    object_id=OBJECT_ID,
    pin=PIN,
    mechanism=MECHANISM,
    hash_algo=HASH_ALGO,
)

# Or, in case you need to use Mobile-ID:
# from lib.mobile_id import MobileIDElectronicID
# EID = MobileIDElectronicID(
#     service_name="Mobile-ID service name",
#     service_uuid="Mobile-ID service UUID, e.g. '09c14dbb-f882-4a53-9a68-335940150f01'",
#     user_phone_number="Phone number of the person who authenticates, e.g. '51234567'",
#     user_id_code="ID code of the person who authenticates, e.g. '38001085718'",
#     algorithm=ALGORITHM,
# )


def main():
    user_cert = base64.b64decode(USER_CERT) if USER_CERT else EID.get_user_cert()
    signing_input = prepare_jwt_header_and_body(PAYLOAD, ALGORITHM, user_cert)
    signature = EID.sign(signing_input)
    jwt = append_signature(signing_input, signature)
    print(jwt)


def prepare_jwt_header_and_body(payload, algorithm, user_cert):
    header = {
        "typ": "JWT",
        "alg": algorithm,
        "x5c": [base64.b64encode(user_cert).decode("utf-8")],
    }

    json_header = json_encode(header)
    json_payload = json_encode(payload)

    signing_input = join(base64url_encode(json_header), base64url_encode(json_payload))
    return signing_input


def append_signature(signing_input, signature):
    jwt_bytes = join(signing_input, base64url_encode(signature))
    return jwt_bytes.decode("utf-8")


def join(segment1, segment2):
    return b".".join([segment1, segment2])


def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace(b"=", b"")


def json_encode(input):
    return json.dumps(input, separators=(",", ":")).encode("utf-8")


if __name__ == "__main__":
    main()
