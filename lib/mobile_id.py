from copy import deepcopy
import hashlib

from mobile_id import MobileIDClient

from lib.electronic_id import ElectronicID


class MobileIDElectronicID(ElectronicID):
    def __init__(
        self,
        service_name: str,
        service_uuid: str,
        user_phone_number: str,
        user_id_code: str,
        algorithm: str,
    ) -> None:
        super().__init__()
        self.client = MobileIDClient(live=True, name=service_name, uuid=service_uuid)
        self.user_phone_number = user_phone_number
        self.user_id_code = user_id_code
        self.algorithm = algorithm

    def get_user_cert(self) -> str:
        # We need to perform authentication with a dummy value to get the user cert
        result = self._sign_with_authkey(b"dummy-data")
        return result.cert

    def sign(self, signing_input: bytes) -> str:
        result = self._sign_with_authkey(signing_input)
        algo = result.signature_algorithm
        # SHA256WithECEncryption -> ES256
        jwt_algo = f"{algo[10]}S{algo[3:6]}"
        assert (
            jwt_algo == self.algorithm
        ), f"You have to pass algorithm='{jwt_algo}' argument to make Mobile-ID authentication work"
        return result.signature

    def _sign_with_authkey(self, data: bytes) -> "AuthenticationResult":
        client = deepcopy(self.client)
        client.nonce_hash = hashlib.sha256(data).digest()
        auth_start_response = client.start_authentication(
            phone_number=self.user_phone_number, national_id_number=self.user_id_code
        )
        print("Mobile-ID verification code:", auth_start_response.verification_code)
        return client.finalize_authentication(
            auth_start_response.session_id, auth_start_response.nonce_hash
        )
