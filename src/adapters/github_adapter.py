import aiohttp
import asyncio
from datetime import datetime
from src.ports.interfaces import IGitHubSource
from src.domain.models import GitHubRepo

class GraphQLGitHubAdapter(IGitHubSource):
    def __init__(self, token: str):
        self.token = token
        self.url = "https://api.github.com/graphql"
        self.headers = {"Authorization": f"Bearer {token}"}

    async def fetch_repos(self, batch_size: int, total_limit: int) -> list[GitHubRepo]:
        repos = []
        cursor = None
        # so search for all the repos with more than 100 stars, sorted by recently updated and get first 100
        query_template = """
        query($cursor: String) {
          search(query: "stars:>100 sort:updated", type: REPOSITORY, first: 100, after: $cursor) {
            pageInfo { endCursor hasNextPage }
            nodes {
              ... on Repository {
                databaseId name owner { login } stargazerCount url
              }
            }
          }
        }
        """

        async with aiohttp.ClientSession() as session: # Reuse session for multiple requests
            while len(repos) < total_limit:
                payload = {"query": query_template, "variables": {"cursor": cursor}}
                
                async with session.post(self.url, json=payload, headers=self.headers) as resp:
                    if resp.status == 429: # Rate Limit handling 
                        print("Rate limited. Sleeping...")
                        await asyncio.sleep(60) 
                        continue
                        
                    data = await resp.json()
                    results = data.get("data", {}).get("search", {})
                    
                    if not results.get("nodes"):
                        break

                    for node in results["nodes"]:
                        if not node: continue
                        repos.append(GitHubRepo(
                            id=node["databaseId"],
                            name=node["name"],
                            owner=node["owner"]["login"],
                            stars=node["stargazerCount"],
                            url=node["url"],
                            crawled_at=datetime.utcnow()
                        ))

                    cursor = results["pageInfo"]["endCursor"]
                    print(f"Fetched {len(repos)} repositories...")
                    
                    if not results["pageInfo"]["hasNextPage"]:
                        break
                        
        return repos[:total_limit]