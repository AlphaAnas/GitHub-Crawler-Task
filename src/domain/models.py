from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class GitHubRepo:
    id: int  
    name: str
    owner: str
    stars: int
    url: str
    crawled_at: datetime