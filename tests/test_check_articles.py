"""The validator must pass the pilot and reject each way an article can go wrong (stdlib unittest)."""
import re
import shutil
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import check_articles as ca  # noqa: E402

PILOT = (REPO / "articles" / "sd-01-001.md").read_text(encoding="utf-8")


def strip_marks(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c)).replace("đ", "d")


MUTATIONS = {
    "no image": (lambda t: re.sub(r"(?m)^!\[.*\]\(.*\)$", "", t), "images must be exactly"),
    "wrong image url": (lambda t: t.replace("assets.bytebytego.com/diagrams/0337", "assets.bytebytego.com/diagrams/9999"), "images must be exactly"),
    "short alt": (lambda t: re.sub(r"!\[[^\]]*\]", "![hinh]", t), "alt text"),
    "no glossary entries": (lambda t: re.sub(r"(?m)^- \*\*(Polling|SSE|WebSocket|Yêu cầu|Máy chủ)[^\n]*\n", "", t), "glossary"),
    "code fence": (lambda t: t + "\n```\nx\n```\n", "forbidden text"),
    "todo left behind": (lambda t: t + "\nTODO(coder)\n", "forbidden text"),
    "external link": (lambda t: t + "\nxem https://example.com/x\n", "host that is not allowed"),
    "github link elsewhere": (lambda t: t + "\nxem https://github.com/other/repo\n", "outside ByteByteGoHq"),
    "section removed": (lambda t: re.sub(r"(?s)## ❓ Thử trả lời.*?(?=## 🎨)", "", t), "sections must be exactly"),
    "sections out of order": (lambda t: t.replace("## ⚖️ Khi nào", "## 📖 Từ khó, giải nghĩa X\n- a\n\n## ⚖️ Khi nào", 1), "sections must be exactly"),
    "required term gone": (lambda t: t.replace("WebSocket", "WS"), "required term missing"),
    "no emoji": (lambda t: "".join(c for c in t if not ca.is_emoji(c)), "emoji"),
    "not vietnamese": (lambda t: strip_marks(t), "Vietnamese"),
    "licence missing": (lambda t: t.replace("CC BY-NC-ND 4.0", "CC"), "licence name"),
    "credit missing": (lambda t: t.replace("ByteByteGo", "nguon"), "ByteByteGo credit"),
    "pinned link missing": (lambda t: t.replace("b28380a4710c5ec9638ec037d4168e288f334cba/data", "main/data"), "pinned source link"),
    "bad status": (lambda t: t.replace("status: draft", "status: shipped"), "status must be"),
    "id differs from file": (lambda t: t.replace("id: sd-01-001", "id: sd-01-002"), "must equal the file name"),
    "hook missing": (lambda t: re.sub(r"(?m)^hook:.*\n", "", t), "'hook'"),
    "hook too long": (lambda t: re.sub(r"(?m)^hook:.*$", "hook: " + "x" * 200, t), "hook must be"),
    "answer left open": (lambda t: t.replace("<details>", "<details open>"), "closed <details>"),
    "image prompt too short": (lambda t: re.sub(r"(?m)^Prompt: .*$", "Prompt: a cat", t), "Prompt"),
    "too short": (lambda t: t[: t.index("## 🏠")] + t[t.index("## 🔗") :], "sections must be exactly"),
    "no title": (lambda t: t.replace("# 📡 ", "", 1).replace("Làm sao trình duyệt biết có tin mới?\n\n>", "x\n\n>", 1), "title"),
}


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "catalog").mkdir()
        (self.root / "articles").mkdir()
        shutil.copy(REPO / "catalog" / "api-web-development.json", self.root / "catalog")
        self.catalog = ca.load_catalog(self.root)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def errors_for(self, text: str) -> list[str]:
        path = self.root / "articles" / "sd-01-001.md"
        path.write_text(text, encoding="utf-8")
        return ca.check_article(path, self.catalog)

    def test_pilot_is_clean(self):
        self.assertEqual(self.errors_for(PILOT), [])

    def test_each_mutation_is_rejected(self):
        for name, (mutate, expected) in MUTATIONS.items():
            with self.subTest(name):
                mutated = mutate(PILOT)
                self.assertNotEqual(mutated, PILOT, "the mutation did not change the article")
                errors = self.errors_for(mutated)
                self.assertTrue(any(expected in e for e in errors), f"{expected!r} not in {errors}")

    def test_missing_file_and_unknown_id_fail(self):
        self.assertEqual(ca.check_article(self.root / "articles" / "sd-01-002.md", self.catalog), ["file is missing"])
        path = self.root / "articles" / "sd-99-999.md"
        path.write_text(PILOT, encoding="utf-8")
        self.assertTrue(any("not in the catalog" in e for e in ca.check_article(path, self.catalog)))

    def test_binary_image_in_repo_fails_the_run(self):
        (self.root / "articles" / "sd-01-001.md").write_text(PILOT, encoding="utf-8")
        self.assertEqual(ca.main(["--all", "--root", str(self.root)]), 0)
        (self.root / "articles" / "copied.png").write_bytes(b"x")
        self.assertEqual(ca.main(["--all", "--root", str(self.root)]), 1)

    def test_ids_requires_the_file_to_exist(self):
        self.assertEqual(ca.main(["--ids", "sd-01-002", "--root", str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()
