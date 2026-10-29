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
