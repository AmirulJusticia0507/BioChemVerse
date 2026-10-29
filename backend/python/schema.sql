-- Skema awal BioChemVerse
-- Dijalankan otomatis saat aplikasi start (idempoten — semua IF NOT EXISTS).

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Pengguna platform (dasar untuk autentikasi JWT)
CREATE TABLE IF NOT EXISTS users (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username      varchar(64) UNIQUE NOT NULL,
    email         varchar(255) UNIQUE NOT NULL,
    password_hash text NOT NULL,
    role          varchar(32) NOT NULL DEFAULT 'student',
    created_at    timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now()
);

-- Token pemulihan kata sandi hanya disimpan sebagai hash dan berlaku singkat.
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    token_hash text PRIMARY KEY,
    user_id    uuid NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    expires_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_user ON password_reset_tokens (user_id);

-- Progres belajar per modul (ChemSphere / ForensiLab / AnatomiMed)
CREATE TABLE IF NOT EXISTS user_progress (
    id         bigserial PRIMARY KEY,
    user_id    uuid NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    module     varchar(32) NOT NULL,
    score      integer NOT NULL DEFAULT 0,
    completed  boolean NOT NULL DEFAULT false,
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (user_id, module)
);

CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress (user_id);

-- Data referensi kimia (impor dari proyek ChemSphere — lihat scripts/import-chemsphere-data.mjs)

CREATE TABLE IF NOT EXISTS categories (
    slug text PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE IF NOT EXISTS elements (
    atomic_number integer PRIMARY KEY,
    symbol        varchar(10) UNIQUE NOT NULL,
    name          varchar(100) NOT NULL,
    name_latin    varchar(100),
    atomic_mass   numeric(10, 4) NOT NULL,
    category_slug text REFERENCES categories (slug),
    period        smallint,
    group_no      smallint,
    description   text,
    uses          text,
    hazard        text,
    properties    jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_elements_category ON elements (category_slug);

CREATE TABLE IF NOT EXISTS polyatomic_ions (
    name        varchar(100) PRIMARY KEY,
    formula     varchar(50) NOT NULL,
    charge      varchar(20),
    description text
);

-- Kuis unsur: riwayat percobaan per pengguna
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id           bigserial PRIMARY KEY,
    user_id      uuid NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    topic        varchar(32) NOT NULL,
    total        integer NOT NULL,
    correct      integer NOT NULL,
    score        integer NOT NULL,
    duration_sec integer,
    created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user ON quiz_attempts (user_id, created_at DESC);

-- Bookmark unsur per pengguna
CREATE TABLE IF NOT EXISTS bookmarks (
    id             bigserial PRIMARY KEY,
    user_id        uuid NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    atomic_number  integer NOT NULL REFERENCES elements (atomic_number) ON DELETE CASCADE,
    note           varchar(255),
    created_at     timestamptz NOT NULL DEFAULT now(),
    UNIQUE (user_id, atomic_number)
);
