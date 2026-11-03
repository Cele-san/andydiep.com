from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CALENDLY_URL = "https://calendly.com/diepdigitalmedia-4upt/45-min-ai-editing-chat"


class LandingPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")

    def test_is_a_full_document(self):
        self.assertTrue(self.html.startswith("<!doctype html>"))
        self.assertIn('<meta name="viewport"', self.html)

    def test_has_the_offer_and_booking(self):
        self.assertIn("10x your content without hiring another editor.", self.html)
        self.assertIn("The 10x Content System", self.html)
        self.assertIn(CALENDLY_URL, self.html)
        self.assertIn("calendly-inline-widget", self.html)

    def test_no_review_leftovers(self):
        for leftover in ("REVIEW DRAFT", "review draft", "PLACEHOLDER", "noindex", "Leave a note"):
            self.assertNotIn(leftover, self.html)

    def test_carles_last_initial_only(self):
        self.assertIn("Carles A.", self.html)


if __name__ == "__main__":
    unittest.main()
