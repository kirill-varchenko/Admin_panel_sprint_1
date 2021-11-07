import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import date, datetime


class AbstractRow(ABC):
    pass


@dataclass
class Genre(AbstractRow):
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork(AbstractRow):
    title: str
    description: str
    creation_date: date
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person(AbstractRow):
    full_name: str
    birth_date: date
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork(AbstractRow):
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime
    updated_at: datetime = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork(AbstractRow):
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime
    updated_at: datetime = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
