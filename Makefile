setup_example:
	cp -r ./wagtail_text_to_speech ./example
	cp example/web.example.env example/web.env
	cd example && docker-compose up
