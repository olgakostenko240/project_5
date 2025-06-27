from rest_framework.serializers import ValidationError

class YouTubeValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = "http://youtube.com"

        if value.get("link_to_video"):
            if url not in value.get("link_to_video"):
                raise ValidationError("Необходима ссылка на youtube.")
        return None
