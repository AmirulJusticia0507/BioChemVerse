"""Pembuat soal kuis tabel periodik (adaptasi dari ChemSphere quizController).

Soal dibangkitkan di server agar kunci jawaban tidak pernah dikirim ke klien.
Semua fungsi di sini murni (kecuali parameter `rng`) sehingga mudah diuji.
"""

from __future__ import annotations

import random

QUIZ_TOPICS = ["simbol", "nomor-atom", "kategori", "golongan-periode", "campuran"]
MIN_ELEMENTS = 8
MAX_QUESTIONS = 30


def _distractors(answer: str, count: int, pool: list[str], rng: random.Random) -> list[str]:
    """Ambil `count` pilihan lain yang unik dari pool (bukan `answer`)."""
    unique = sorted({value for value in pool if value != answer})
    rng.shuffle(unique)
    return unique[:count]


def _position(element: dict) -> str:
    return f"Golongan {element['group_no']}, periode {element['period']}"


def build_quiz(
    elements: list[dict], topic: str, count: int, rng: random.Random | None = None
) -> dict:
    """Bangkitkan satu set soal.

    `elements` berisi dict dengan kunci: atomic_number, symbol, name, period,
    group_no, category_name.
    """
    rng = rng or random.Random()
    count = max(1, min(int(count), MAX_QUESTIONS))

    symbol_pool = [el["symbol"] for el in elements]
    category_pool = sorted({el["category_name"] for el in elements if el.get("category_name")})
    position_pool = [_position(el) for el in elements]

    picked = rng.sample(elements, min(count, len(elements)))
    questions = []

    for index, element in enumerate(picked):
        kind = topic
        if topic == "campuran":
            kind = rng.choice(["simbol", "nomor-atom", "kategori", "golongan-periode"])

        if kind == "simbol":
            answer = element["symbol"]
            question = f"Apa simbol kimia untuk {element['name']}?"
            pool = symbol_pool
        elif kind == "nomor-atom":
            answer = str(element["atomic_number"])
            question = f"Berapa nomor atom {element['name']} ({element['symbol']})?"
            pool = [str(el["atomic_number"]) for el in elements]
        elif kind == "kategori":
            answer = element.get("category_name") or "Tidak diketahui"
            question = f"Unsur {element['name']} ({element['symbol']}) termasuk kategori apa?"
            pool = category_pool
        else:  # golongan-periode
            answer = _position(element)
            question = f"Di golongan dan periode mana {element['name']} ({element['symbol']}) berada?"
            pool = position_pool

        options = [answer, *_distractors(answer, 3, pool, rng)]
        rng.shuffle(options)
        questions.append(
            {"id": str(index), "question": question, "options": options, "answer": answer}
        )

    return {"topic": topic, "questions": questions}
