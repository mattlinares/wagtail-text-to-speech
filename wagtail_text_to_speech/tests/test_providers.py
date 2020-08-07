from django.test import TestCase

from wagtail_text_to_speech.providers import get_current_provider
from wagtail_text_to_speech.providers.cognitive import Cognitive


class ProviderdRetrivalTest(TestCase):
    def test_generate(self):
        provider = get_current_provider()

        self.assertTrue(isinstance(provider(), Cognitive))
