from typing import Generic, TypeVar, List

from pydantic import BaseModel

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
