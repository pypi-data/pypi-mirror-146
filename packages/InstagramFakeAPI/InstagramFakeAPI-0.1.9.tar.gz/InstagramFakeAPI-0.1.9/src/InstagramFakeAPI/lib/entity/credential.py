class Credential:

    def __init__(self, ua: str, bloks: str, cap: str):
        self.__account = {}

        self.__settings = {}
        self.__authorization = {}

        self.__device = None
        self.__connection_type_header = None

        self.__capabilities = cap
        self.__bloks_version_id = bloks
        self.__user_agent_str = ua

        self.__mid = ''

    #
    #   Full settings
    #

    @property
    def settings(self):
        return {
            'account': self.__account,
            'device': self.__device,
            'auth': self.__authorization
        }

    @settings.setter
    def settings(self, last_login: dict):
        self.__settings = last_login
        self.__device = self.__settings.get('device', None)
        self.__account = self.__settings.get('account', None)
        self.__authorization = self.__settings.get('auth', None)

    #
    #   Authorization data
    #

    @property
    def authorization(self) -> dict:
        return self.__authorization

    @authorization.setter
    def authorization(self, value: dict):
        self.__authorization = value

    #
    #   Device
    #

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, device: dict):
        self.__device = device

    @property
    def user_agent(self):
        return self.__user_agent_str.format(**self.__device)

    #
    #   Constants
    #

    @property
    def bloks_version_id(self) -> str:
        return self.__bloks_version_id

    @property
    def capabilities(self):
        return self.__capabilities

    @property
    def connection_type_header(self):
        return self.__connection_type_header

    #
    #   Language
    #

    @property
    def language(self):
        return self.account.get('language', 'en_US')

    #
    #   Headers settings
    #

    @property
    def claim(self) -> str:
        return self.__authorization.get('x-ig-set-www-claim', '') if self.__authorization.get(
            'x-ig-set-www-claim', '') != '0' else ''

    @property
    def bearer(self) -> str:
        return self.__authorization.get('ig-set-authorization', '')

    @property
    def u_rur(self) -> str:
        return self.__authorization.get('ig-set-ig-u-rur', '')

    @property
    def mid(self) -> str:
        return self.__authorization.get('x-mid', self.__mid)

    @mid.setter
    def mid(self, value: str):
        self.__mid = value

    #
    #   Account data dict
    #

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, account: dict):
        self.__account = account if account else {}

    #
    # Account details properties
    #

    @property
    def username(self) -> str:
        return self.__account.get('username')

    @property
    def password(self) -> str:
        return self.__account.get('password')

    @property
    def proxy(self) -> str:
        return self.__account.get('proxy','')

    @property
    def email(self) -> str:
        return self.__account.get('email_login')

    @property
    def email_password(self) -> str:
        return self.__account.get('email_pass')

    @property
    def email_host(self) -> str:
        return self.__account.get('email_host')

    @property
    def email_port(self) -> int:
        return int(self.__account.get('email_port'))
