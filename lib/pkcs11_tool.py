import subprocess

from lib.electronic_id import ElectronicID


class PKCS11ElectronicID(ElectronicID):
    def __init__(
        self,
        slot_index: str,
        object_id: str,
        pin: str,
        mechanism: str,
        hash_algo,
    ) -> None:
        super().__init__()
        self.slot_index = slot_index
        self.object_id = object_id
        self.pin = pin
        self.mechanism = mechanism
        self.hash_algo = hash_algo

    def get_user_cert(self) -> str:
        result = run_command(
            "pkcs11-tool",
            "--read",
            "--slot-index",
            self.slot_index,
            "--id",
            self.object_id,
            "--type",
            "cert",
        )
        return result.stdout

    def sign(self, signing_input: bytes) -> str:
        with open(SIGNING_INPUT_FILENAME, "wb") as signing_input_file:
            signing_input_file.write(self.hash_algo(signing_input).digest())
        result = run_command(
            "pkcs11-tool",
            "--sign",
            "--slot-index",
            self.slot_index,
            "--id",
            self.object_id,
            "--pin",
            self.pin,
            "--mechanism",
            self.mechanism,
            "--input-file",
            SIGNING_INPUT_FILENAME,
        )
        return result.stdout


SIGNING_INPUT_FILENAME = "signing-input"


def run_command(*args):
    try:
        return subprocess.run(args, check=True, capture_output=True)
    except Exception as e:
        print(f"Command '{e.cmd}' failed, stderr: '{e.stderr}', stdout: '{e.stdout}'")
        raise
