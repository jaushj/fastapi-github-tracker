from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")
