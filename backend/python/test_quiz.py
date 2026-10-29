"""Uji pembangkit soal kuis (murni, tanpa database).

Jalankan: python -m unittest test_quiz -v
"""

from __future__ import annotations

import random
import unittest

import quiz

ELEMENTS = [
    {
        "atomic_number": number,
        "symbol": symbol,
        "name": name,
        "period": period,
        "group_no": group,
        "category_name": category,
    }
    for number, symbol, name, period, group, category in [
        (1, "H", "Hidrogen", 1, 1, "Nonlogam"),
        (2, "He", "Helium", 1, 18, "Gas Mulia"),
        (3, "Li", "Litium", 2, 1, "Logam Alkali"),
        (4, "Be", "Berilium", 2, 2, "Logam Alkali Tanah"),
        (5, "B", "Boron", 2, 13, "Metaloid"),
        (6, "C", "Karbon", 2, 14, "Nonlogam"),
        (7, "N", "Nitrogen", 2, 15, "Nonlogam"),
        (8, "O", "Oksigen", 2, 16, "Nonlogam"),
        (26, "Fe", "Besi", 4, 8, "Logam Transisi"),
        (79, "Au", "Emas", 6, 11, "Logam Transisi"),
    ]
]


class BuildQuizTests(unittest.TestCase):
    def test_campuran_membuat_soal_berurutan_tanpa_kunci_di_opsi_ganda(self):
        result = quiz.build_quiz(ELEMENTS, "campuran", 8, random.Random(42))
        self.assertEqual(result["topic"], "campuran")
        self.assertEqual(len(result["questions"]), 8)
        for index, item in enumerate(result["questions"]):
            self.assertEqual(item["id"], str(index))
            self.assertIn(item["answer"], item["options"])
            self.assertEqual(len(set(item["options"])), len(item["options"]))
            self.assertEqual(len(item["options"]), 4)

    def test_simbol_memakai_nama_unsur_untuk_pertanyaan(self):
        result = quiz.build_quiz(ELEMENTS, "simbol", 10, random.Random(1))
        for item in result["questions"]:
            self.assertTrue(item["question"].startswith("Apa simbol kimia untuk "))
            self.assertTrue(item["answer"])

    def test_nomor_atom_jawabannya_string_angka(self):
        result = quiz.build_quiz(ELEMENTS, "nomor-atom", 10, random.Random(7))
        for item in result["questions"]:
            self.assertTrue(item["answer"].isdigit())

    def test_kategori_hanya_memakai_kategori_yang_ada(self):
        categories = {element["category_name"] for element in ELEMENTS}
        result = quiz.build_quiz(ELEMENTS, "kategori", 10, random.Random(3))
        for item in result["questions"]:
            for option in item["options"]:
                self.assertIn(option, categories)

    def test_golongan_periode_memakai_format_posisi(self):
        result = quiz.build_quiz(ELEMENTS, "golongan-periode", 10, random.Random(5))
        for item in result["questions"]:
            self.assertRegex(item["answer"], r"^Golongan \d+, periode \d+$")

    def test_jumlah_soal_dibatasi_max_dan_minimal_satu(self):
        self.assertEqual(len(quiz.build_quiz(ELEMENTS, "simbol", 99)["questions"]), len(ELEMENTS))
        self.assertEqual(len(quiz.build_quiz(ELEMENTS, "simbol", 0)["questions"]), 1)

    def test_tanpa_duplikat_unsur_dalam_satu_set(self):
        result = quiz.build_quiz(ELEMENTS, "simbol", 10, random.Random(11))
        questions = [item["question"] for item in result["questions"]]
        self.assertEqual(len(questions), len(set(questions)))

    def test_seed_sama_menghasilkan_soal_sama(self):
        first = quiz.build_quiz(ELEMENTS, "kategori", 5, random.Random(99))
        second = quiz.build_quiz(ELEMENTS, "kategori", 5, random.Random(99))
        self.assertEqual(first, second)

    def test_topik_dikenal(self):
        self.assertIn("campuran", quiz.QUIZ_TOPICS)
        self.assertGreaterEqual(len(quiz.QUIZ_TOPICS), 5)


if __name__ == "__main__":
    unittest.main()
