import asyncpg
from typing import List
from src.ports.interfaces import IRepoStorage
from src.domain.models import GitHubRepo

class PostgresAdapter(IRepoStorage):
    def __init__(self, db_url: str):
        self.db_url = db_url

    async def setup_schema(self):
        conn = await asyncpg.connect(self.db_url)
        # Using BIGINT for ID and UPSERT strategy for efficiency 
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS github_repos (
                id BIGINT PRIMARY KEY,
                name TEXT NOT NULL,
                owner TEXT NOT NULL,
                stars INTEGER NOT NULL,
                url TEXT,
                crawled_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await conn.close()

    async def upsert_repos(self, repos: List[GitHubRepo]):
        conn = await asyncpg.connect(self.db_url)
        # Efficient bulk insert/update
        values = [(r.id, r.name, r.owner, r.stars, r.url, r.crawled_at) for r in repos]
        
        await conn.executemany("""
            INSERT INTO github_repos (id, name, owner, stars, url, crawled_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (id) DO UPDATE 
            SET stars = EXCLUDED.stars, 
                crawled_at = EXCLUDED.crawled_at,
                updated_at = CURRENT_TIMESTAMP;
        """, values)
        await conn.close()