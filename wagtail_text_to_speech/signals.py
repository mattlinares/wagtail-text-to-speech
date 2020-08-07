#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from wagtail.documents.models import Document
from wagtail.core.signals import page_published

from wagtail_text_to_speech.providers import get_current_provider
# from wagtail_text_to_speech.utils import translate_description_result
from wagtail_text_to_speech import app_settings
from wagtail_text_to_speech.app_settings import get_setting



def create_audio_version(sender, instance, **kwargs):

    try:
        if instance.synthesized_article_audio_file and instance.synthesized_article_audio == False:
            instance.publish_synthesized_article_audio = False
            audio_document = Document.objects.get(id=instance.synthesized_article_audio_file_id)
            audio_document.delete()
            instance.synthesized_article_audio_file = None
            try:
                instance.save()
            except:
                pass
            return
        if instance.synthesized_article_audio == True and instance.synthesized_article_audio_file:
            return
        if instance.synthesized_article_audio == False:
            return
    except:
        pass

    provider = get_current_provider()()

    # Prepare Wagtail article text by cleaning all RichTextBlock text
    import re
    regex_clean_pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    authors = ''
    meta_text = ''
    for author in instance.author_list:
        authors += author['full_name'] + ', '
    excerpt = re.sub(regex_clean_pattern, '', instance.excerpt)
    meta_text += '<speak>' + instance.title + ' by ' + authors + excerpt + '<break time="2000ms" />'
    body_text = ''
    for block in instance.body:
        if block.block.name == 'rich_text':
            body_text += block.value['text'].source
    cleaned_body_text = re.sub(regex_clean_pattern, '', body_text)
    full_text = meta_text + cleaned_body_text + '</speak>'
    # Send text to speech generation API
    file_name = instance.title + ' – synthesized audio reading'
    result = provider.generate_speech(full_text, file_name)

    instance.synthesized_article_audio_file = result

    instance.save()

page_published.connect(create_audio_version)


# @receiver(
#     post_save,
#     sender=ArticlePageBaseMixin,
#     # dispatch_uid="wagtail_text_to_speech.signals.apply_image_alt",
# )
# def create_audio_version(sender, instance, **kwargs):
#     # Only run on articles with make audio option selected
#     # TODO And if audio has not already been created
#     # TODO Also allow new audio to be created – perhaps by allowing
#     # past audio to be deleted.
#     # if not kwargs["create_audio_version"] == True:
#     #     return

#     provider = get_current_provider()()
#     # image_url = instance.file.url


#     result = provider.describe(full_text)

#     # if get_setting("ALT_GENERATOR_TRANSLATE_TO_LOCAL_LANG"):
#     #     result = translate_description_result(result)

#     # if image_url[-4:] == instance.title[-4:]:
#     #     _apply_title(instance, result.description)

#     instance.save()


