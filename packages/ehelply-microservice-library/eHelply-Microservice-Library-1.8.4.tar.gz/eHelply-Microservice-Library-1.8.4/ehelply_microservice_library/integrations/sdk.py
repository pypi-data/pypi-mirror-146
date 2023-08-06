from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.utils.cryptography import Encryption
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_bootstrapper.utils.environment import Environment
from ehelply_python_sdk.configuration import Configuration


class SDK(Integration):
    headers: dict
    base_url: str

    def __init__(self, service_gatekeeper_key: str) -> None:
        super().__init__("sdk")

        self.enc: Encryption = Encryption([service_gatekeeper_key.encode(Encryption.STRING_ENCODING)])

    def init(self):
        try:
            secret_token: str = State.config.m2m.auth.secret_key
            access_token: str = State.config.m2m.auth.access_key

            if len(secret_token) == 0 or len(access_token) == 0:
                State.logger.warning("SDK (M2M) credentials are not set. Check the m2m.yaml config")

            secret_token = self.enc.decrypt_str(secret_token.encode(Encryption.STRING_ENCODING))
            access_token = self.enc.decrypt_str(access_token.encode(Encryption.STRING_ENCODING))

            # Setup SDK
            SDK.make_sdk(access_token, secret_token)

        except:
            SDK.make_sdk("", "")
            State.logger.severe(
                "SDK (M2M) credentials are invalid. Ensure they are encrypted. Check the m2m.yaml config")

    @staticmethod
    def make_sdk(access_token: str, secret_token: str):
        host: str = "https://api.prod.ehelply.com"

        if Environment.is_dev() or Environment.is_test():
            host = "https://api.test.ehelply.com"

        SDK.base_url = host

        configuration = Configuration(
            host=host
        )

        SDK.headers = {
            "x_access_token": access_token,
            "x_secret_token": secret_token,
            "ehelply_project": "ehelply-cloud"
        }


