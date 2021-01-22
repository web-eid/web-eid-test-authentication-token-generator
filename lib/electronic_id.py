from abc import ABC, abstractmethod


class ElectronicID(ABC):
    @abstractmethod
    def get_user_cert(self):
        pass

    @abstractmethod
    def sign(self, signing_input: bytes) -> str:
        pass