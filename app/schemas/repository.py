from pydantic import BaseModel, Field
from uuid import UUID

class RepositoryCreate(BaseModel):
    owner: str = Field(min_length=1)
    name: str = Field(min_length=1)

class RepositoryUpdate(BaseModel):
    description: str = Field(min_length=1)

class RepositoryResponse(BaseModel):
    id: UUID
    owner: str
    name: str
    description: str | None
    stars: int = Field(ge=0)
    forks: int = Field(ge=0)
    url: str

    class Config:
        from_attributes = True
