import asyncio
import os
from dotenv import load_dotenv
import argparse
from src.adapters.github_adapter import GraphQLGitHubAdapter
from src.adapters.postgres_adapter import PostgresAdapter


load_dotenv()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['setup', 'crawl'], required=True)
    args = parser.parse_args()

    db_url = os.getenv("DB_URL")
    # Clean Architecture: Main injects dependencies
    storage = PostgresAdapter(db_url)

    if args.mode == 'setup':
        print("Setting up database schema...")
        await storage.setup_schema()
        print("Schema created.")
        
    elif args.mode == 'crawl':
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN is missing")
            
        source = GraphQLGitHubAdapter(token)
        

        print("Starting crawl...")
        repos = await source.fetch_repos(batch_size=100, total_limit=1000) 
        
        print(f"Saving {len(repos)} repositories to DB...")
        await storage.upsert_repos(repos)
        print("Done.")

if __name__ == "__main__":
    asyncio.run(main())