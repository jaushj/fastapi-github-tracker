from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Repository

async def create_repo(db: AsyncSession, data: dict):
    repo = Repository(**data)
    db.add(repo)
    await db.commit()
    await db.refresh(repo)
    return repo

async def get_repo(db: AsyncSession, repo_id):
    result = await db.execute(
        select(Repository).where(Repository.id == repo_id)
    )
    return result.scalar_one_or_none()

async def update_repo(db: AsyncSession, repo, description: str):
    repo.description = description
    await db.commit()
    await db.refresh(repo)
    return repo

async def delete_repo(db: AsyncSession, repo):
    await db.delete(repo)
    await db.commit()
