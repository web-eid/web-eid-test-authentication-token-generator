"""
A Python script that generates arbitrary Web eID authentication tokens for
testing using pkcs11-tool.

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
import subprocess

# Leave empty to read from card or add as base64-encoded to use a modified certificate
USER_CERTIFICATE = ""
ALGORITHM = "ES384"
SLOT_INDEX = "00"
OBJECT_ID = "01"
PIN = "1234"
MECHANISM = "ECDSA"
HASH_ALGO = hashlib.sha384
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


def main():
    user_cert = base64.b64decode(USER_CERTIFICATE) if USER_CERTIFICATE else read_user_cert()
    encoded = encode(PAYLOAD, user_cert)
    print(encoded)


def read_user_cert():
    result = run_command("pkcs11-tool", "--read", "--slot-index", SLOT_INDEX, "--id", OBJECT_ID, "--type", "cert")
    return result.stdout


def encode(payload, user_cert):
    segments = []

    header = {
        "typ": "JWT",
        "alg": ALGORITHM,
        "x5c": [base64.b64encode(user_cert).decode("utf-8")],
    }

    json_header = json_encode(header)
    json_payload = json_encode(payload)

    segments.append(base64url_encode(json_header))
    segments.append(base64url_encode(json_payload))

    signing_input = b".".join(segments)
    signature = sign(signing_input)

    segments.append(base64url_encode(signature))

    encoded_string = b".".join(segments)

    return encoded_string.decode("utf-8")


def sign(signing_input):
    with open("signing-input", "wb") as signing_input_file:
        signing_input_file.write(HASH_ALGO(signing_input).digest())
    result = run_command(
        "pkcs11-tool",
        "--sign",
        "--slot-index",
        SLOT_INDEX,
        "--id",
        OBJECT_ID,
        "--pin",
        PIN,
        "--mechanism",
        MECHANISM,
        "--input-file",
        "signing-input",
    )
    return result.stdout


def run_command(*args):
    try:
        return subprocess.run(args, check=True, capture_output=True)
    except Exception as e:
        print(f"Command '{e.cmd}' failed, stderr: '{e.stderr}', stdout: '{e.stdout}'")
        raise


def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace(b"=", b"")


def json_encode(input):
    return json.dumps(input, separators=(",", ":")).encode("utf-8")


if __name__ == "__main__":
    main()
