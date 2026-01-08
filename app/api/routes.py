from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryUpdate,
    RepositoryResponse,
)
from app.services.github import fetch_repo, GitHubServiceError
from app.db import crud

router = APIRouter()

@router.post("/repositories", response_model=RepositoryResponse, status_code=201)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        data = await fetch_repo(payload.owner, payload.name)
        return await crud.create_repo(db, data)
    except GitHubServiceError:
        raise HTTPException(status_code=404, detail="GitHub repository not found")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Repository already exists")

@router.get("/repositories/{repo_id}", response_model=RepositoryResponse)
async def get_repository(repo_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = await crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo

@router.put("/repositories/{repo_id}", response_model=RepositoryResponse)
async def update_repository(
    repo_id: UUID,
    payload: RepositoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = await crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return await crud.update_repo(db, repo, payload.description)

@router.delete("/repositories/{repo_id}", status_code=204)
async def delete_repository(repo_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = await crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    await crud.delete_repo(db, repo)
