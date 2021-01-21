from django.db import models


# Create your models here.
class Details:

    def __init__(self,
                 game_type="",
                 name="",
                 required_age="",
                 about_the_game="",
                 short_description="",
                 supported_languages="",
                 images="",
                 release_date="",
                 coming_soon=False,
                 developers="",
                 publishers="",
                 platforms="",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_type = game_type
        self.name = name
        self.required_age = required_age
        self.about_the_game = about_the_game
        self.short_description = short_description
        self.supported_languages = supported_languages
        self.images = images
        self.release_date = release_date
        self.coming_soon = coming_soon
        self.developers = developers
        self.publishers = publishers
        self.platforms = platforms


class Images:
    def __init__(self, header, screenhots, background, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = header
        self.screenhots = screenhots
        self.background = background
