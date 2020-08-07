from django.conf import settings


DEFAULT_PROVIDER = "wagtail_text_to_speech.providers.polly.Polly"  # NOQA

ALT_GENERATOR_PROVIDER = getattr(settings, "ALT_GENERATOR_PROVIDER", DEFAULT_PROVIDER)


def get_setting(name):
    return getattr(settings, name, None) or globals()[name]
