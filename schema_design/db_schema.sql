-- Создание отдельной схемы для контента:
CREATE SCHEMA IF NOT EXISTS content;

-- Жанры кинопроизведений:
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Кинопроизведения:
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Персоны:
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Жанры кинопроизведений:
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE cascade,
    genre_id uuid NOT NULL REFERENCES content.genre(id) ON DELETE cascade,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Индекс по кинопроизведению-жанру
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx
ON content.genre_film_work (film_work_id, genre_id);

-- Персоны кинопроизведений
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE cascade,
    person_id uuid NOT NULL REFERENCES content.person(id) ON DELETE cascade,
    role TEXT NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

-- Индекс по кинопроизведению-персоне-роли
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role_idx
ON content.person_film_work (film_work_id, person_id, role);

