class ClientError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PageNotFound(ClientError):
    pass


class NonAuthorizedRequest(ClientError):
    pass


class ProxyRequestError(ClientError):
    pass


class ChallengeRequired(ClientError):
    pass


class Response429(ClientError):
    pass
