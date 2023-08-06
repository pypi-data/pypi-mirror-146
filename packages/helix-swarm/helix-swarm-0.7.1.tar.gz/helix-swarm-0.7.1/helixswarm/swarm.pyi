import abc
from abc import ABC, abstractmethod
from helixswarm.endpoints.activities import Activities as Activities
from helixswarm.endpoints.changes import Changes as Changes
from helixswarm.endpoints.comments import Comments as Comments
from helixswarm.endpoints.groups import Groups as Groups
from helixswarm.endpoints.projects import Projects as Projects
from helixswarm.endpoints.reviews import Reviews as Reviews
from helixswarm.endpoints.servers import Servers as Servers
from helixswarm.endpoints.users import Users as Users
from helixswarm.endpoints.workflows import Workflows as Workflows
from helixswarm.exceptions import SwarmError as SwarmError, SwarmNotFoundError as SwarmNotFoundError, SwarmUnauthorizedError as SwarmUnauthorizedError
from helixswarm.helpers import minimal_version as minimal_version
from typing import Any, Callable, NamedTuple, Optional

class Response(NamedTuple):
    status: Any
    body: Any

class Swarm(ABC, metaclass=abc.ABCMeta):
    auth_update_callback: Any
    activities: Any
    changes: Any
    comments: Any
    groups: Any
    projects: Any
    reviews: Any
    servers: Any
    users: Any
    workflows: Any
    def __init__(self) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def request(self, callback: Callable, method: str, path: str, fcb: Optional[Callable] = ..., **kwargs: Any) -> dict: ...
    def get_version(self) -> dict: ...
    def check_auth(self, token: Optional[str] = ...) -> dict: ...
    def get_auth_methods(self) -> dict: ...
    def init_auth(self, method: str) -> dict: ...
    def check_session(self) -> dict: ...
    def init_session(self) -> dict: ...
    def destroy_session(self) -> dict: ...
    def login(self, saml: Optional[bool] = ...) -> dict: ...
    def logout(self) -> dict: ...
