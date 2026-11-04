from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "calculator" / "index.html"


class CalculatorPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_is_a_full_document(self):
        self.assertTrue(self.html.startswith("<!doctype html>"))
        self.assertIn('<meta name="viewport"', self.html)
        self.assertIn('href="https://andydiep.com/calculator/"', self.html)

    def test_has_the_calculator_and_booking_link(self):
        self.assertIn("How much profit is editing costing you?", self.html)
        self.assertIn('id="year"', self.html)
        self.assertIn('href="/#step-2"', self.html)

    def test_no_review_leftovers(self):
        for leftover in ("Review only", "email not connected", "PLACEHOLDER", "noindex"):
            self.assertNotIn(leftover, self.html)


if __name__ == "__main__":
    unittest.main()
