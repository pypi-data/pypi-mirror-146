import os
from _typeshed import NoneType
from typing import Any, TypeVar, Generator, AsyncGenerator

_None = TypeVar('_None', NoneType, NoneType)
_Generator = TypeVar('_Generator', Generator, AsyncGenerator)

class AnimePicture:
    content: Any
    def __init__(self, data: bytes) -> None: ...
    def save(self, directory: str | os.PathLike[str] | None = ..., filename: str = ...) -> _None: ...

async def AsyncGetAnimePictures(stop: int | None = ..., *, headless: bool | None = ..., delay: int | None = ...) -> _Generator: ...
def GetAnimePictures(stop: int | None = ..., *, headless: bool | None = ..., delay: int | None = ...) -> _Generator: ...
