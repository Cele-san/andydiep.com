from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CALENDLY_URL = "https://calendly.com/diepdigitalmedia-4upt/45-min-ai-editing-chat"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.anchors = []
        self._active_anchor = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._active_anchor = {
                "href": dict(attrs).get("href"),
                "parts": [],
            }

    def handle_endtag(self, tag):
        if tag == "a" and self._active_anchor is not None:
            self.anchors.append(
                (
                    " ".join(self._active_anchor["parts"]),
                    self._active_anchor["href"],
                )
            )
            self._active_anchor = None

    def handle_data(self, data):
        value = " ".join(data.split())
        if value:
            self.parts.append(value)
            if self._active_anchor is not None:
                self._active_anchor["parts"].append(value)


class CoachingCopyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        parser = TextExtractor()
        parser.feed(cls.html)
        cls.text = " ".join(parser.parts)
        cls.anchors = parser.anchors

    def test_page_leads_with_attendee_value(self):
        self.assertIn("Bring me the part of AI editing that's slowing you down", self.text)
        self.assertIn("free 45-minute coaching call", self.text)
        self.assertNotIn("I want to hear how you actually edit", self.text)

    def test_every_primary_cta_uses_the_coaching_label_and_existing_url(self):
        matching_ctas = [
            (text, href)
            for text, href in self.anchors
            if text.startswith("Book the free 45-min coaching call")
            and href == CALENDLY_URL
        ]
        self.assertEqual(len(matching_ctas), 3)

    def test_page_names_the_audience_and_concrete_outcome(self):
        self.assertIn("business owners, creators, YouTubers, and video editors", self.text)
        self.assertIn("work out the next AI-assisted step worth trying", self.text)
        self.assertIn("leave with a clearer next move", self.text)

    def test_booking_form_copy_matches_required_and_optional_fields(self):
        self.assertIn("The booking form requires your role and country", self.text)
        self.assertIn("Age range and workflow questions are optional", self.text)

    def test_evergreen_page_has_no_expiring_two_week_claim(self):
        self.assertNotIn("next two weeks", self.text.lower())
        self.assertNotIn("next couple of weeks", self.text.lower())


if __name__ == "__main__":
    unittest.main()
