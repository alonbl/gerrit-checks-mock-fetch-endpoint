import typing


class FetchEndpoint(typing.TypedDict):
    accountId: int
    emailAddresses: list[str]
    project: str
    changeId: str
    revision: int
