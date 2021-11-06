import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork:
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
class Person:
    full_name: str
    birth_date: date
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime
    updated_at: datetime = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime
    updated_at: datetime = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
