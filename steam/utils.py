from steam.models import Details, Images


def getDetailsModelFromJson(details_json, appid):
    details = details_json['details'][appid]
    success = details['success']
    if success:
        data = details['data']
        game_details = Details()

        game_details.game_type = data['type']
        game_details.name = data['name']
        game_details.required_age = data['required_age']
        game_details.about_the_game = data['about_the_game']
        game_details.short_description = data['short_description']
        game_details.supported_languages = data['supported_languages']
        game_details.developers = data['developers']
        game_details.publishers = data['publishers']
        game_details.platforms = data['platforms']
        game_details.release_date = data['release_date']['date']
        game_details.coming_soon = data['release_date']['coming_soon']

        images = Images(
            data['header_image'],
            data['screenshots'],
            data['background']
        )

        game_details.images = images

        return data
    return None


def isValidDetails(details_json, appid):
    return details_json[appid]['success']
