# flake8: noqa
# mypy: ignore-errors
# pylint: disable=unused-import, invalid-name, unused-argument, too-few-public-methods

from collections.abc import Callable
from enum import Enum
from typing import List, Optional, TypedDict, Union

##### BEGIN OF LSP SPECS


class ChecksPluginApi:
    def register(
        self,
        provider: "ChecksProvider",
        config: Optional["ChecksApiConfig"] = None,
    ) -> None:
        pass

    def announceUpdate(self) -> None:
        pass

    def updateResult(self, run: "CheckRun", result: "CheckResult") -> None:
        pass


class ChecksApiConfig(TypedDict):
    fetchPollingIntervalSeconds: float


class ChangeData(TypedDict):
    changeNumber: float
    patchsetNumber: float
    patchsetSha: str
    repo: str
    commitMessage: str | None
    changeInfo: "ChangeInfo"


class ChecksProvider:
    def fetch(self, change: ChangeData) -> "Promise[FetchResponse]":
        pass


class FetchResponse(TypedDict):
    responseCode: "ResponseCode"
    errorMessage: str | None
    loginCallback: Callable[[], None] | None
    actions: list["Action"] | None
    summaryMessage: str | None
    links: list["Link"] | None
    runs: list["CheckRun"] | None


class ResponseCode(str, Enum):
    OK = "OK"
    ERROR = "ERROR"
    NOT_LOGGED_IN = "NOT_LOGGED_IN"


class CheckRun(TypedDict):
    change: float | None
    patchset: float | None
    attempt: float | None
    externalId: str | None
    checkName: str
    checkDescription: str | None
    checkLink: str | None
    status: "RunStatus"
    statusDescription: str | None
    statusLink: str | None
    labelName: str | None
    actions: list["Action"] | None
    scheduledTimestamp: Optional["Date"]
    startedTimestamp: Optional["Date"]
    finishedTimestamp: Optional["Date"]
    results: list["CheckResult"] | None


class Action(TypedDict):
    name: str
    tooltip: str | None
    primary: bool | None
    summary: bool | None
    disabled: bool | None
    callback: "ActionCallback"


ActionCallback = Callable[
    [float, float, Union[float, None], Union[str, None], Union[str, None], str],
    Union["Promise[ActionResult]", None],
]


class ActionResult(TypedDict):
    message: str | None
    shouldReload: bool | None
    errorMessage: str | None


class RunStatus(str, Enum):
    RUNNABLE = "RUNNABLE"
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"


class CheckResult(TypedDict):
    externalId: str | None
    category: "Category"
    summary: str
    message: str | None
    tags: list["Tag"] | None
    links: list["Link"] | None
    codePointers: list["CodePointer"] | None
    actions: list[Action] | None


class Category(str, Enum):
    SUCCESS = "SUCCESS"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Tag(TypedDict):
    name: str
    tooltip: str | None
    color: Optional["TagColor"]


class TagColor(str, Enum):
    GRAY = "gray"
    YELLOW = "yellow"
    PINK = "pink"
    PURPLE = "purple"
    CYAN = "cyan"
    BROWN = "brown"


class Link(TypedDict):
    url: str
    tooltip: str | None
    primary: bool
    icon: "LinkIcon"


class CodePointer(TypedDict):
    path: str
    range: "CommentRange"


class LinkIcon(str, Enum):
    EXTERNAL = "external"
    IMAGE = "image"
    HISTORY = "history"
    DOWNLOAD = "download"
    DOWNLOAD_MOBILE = "download_mobile"
    HELP_PAGE = "help_page"
    REPORT_BUG = "report_bug"
    CODE = "code"
    FILE_PRESENT = "file_present"


##### END OF LSP SPECS
