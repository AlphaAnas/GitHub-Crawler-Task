from abc import ABC, abstractmethod
from typing import List
from src.domain.models import GitHubRepo

class IRepoStorage(ABC):
    @abstractmethod
    async def upsert_repos(self, repos: List[GitHubRepo]) -> None:
        pass

    @abstractmethod
    async def setup_schema(self) -> None:
        pass

class IGitHubSource(ABC):
    @abstractmethod
    async def fetch_repos(self, batch_size: int, total_count: int) -> List[GitHubRepo]:
        pass