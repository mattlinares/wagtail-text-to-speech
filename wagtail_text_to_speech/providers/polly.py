# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from django.conf import settings

from wagtail.documents.models import Document

from wagtail_text_to_speech import app_settings
from wagtail_text_to_speech.providers import AbstractProvider, DescriptionResult


class Polly(AbstractProvider):
    def __init__(self, *args, **kwargs):
        # session = boto3.Session(
        #     aws_access_key_id=os.environ.get('AWS_POLLY_ACCESS_KEY', None),
        #     aws_secret_access_key=os.environ.get('AWS_POLLY_SECRET_KEY', None),
        #     region_name="eu-west-2"
        # )
        # polly = session.client("polly")
        pass

    def generate_speech(self, text, title):
        session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_POLLY_ACCESS_KEY', None),
            aws_secret_access_key=os.environ.get('AWS_POLLY_SECRET_KEY', None),
            region_name="eu-west-1"
        )
        polly = session.client("polly")
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                                VoiceId="Amy", Engine="neural", TextType='ssml')
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)
        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join(settings.MEDIA_ROOT, "speech.mp3")
                    try:
                        with open(output, "wb") as file:
                            file.write(stream.read())
                        # Save mp3 as Wagtail document
                        audio_document = Document.objects.create(title=title, file=output)
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
                        sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        return audio_document
