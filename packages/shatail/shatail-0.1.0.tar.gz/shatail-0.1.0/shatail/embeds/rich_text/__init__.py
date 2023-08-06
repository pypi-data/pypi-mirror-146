from shatail.embeds import format
from shatail.embeds.embeds import get_embed
from shatail.embeds.models import Embed
from shatail.rich_text import EmbedHandler

# Front-end conversion


class MediaEmbedHandler(EmbedHandler):
    identifier = "media"

    @staticmethod
    def get_model():
        return Embed

    @staticmethod
    def get_instance(attrs):
        return get_embed(attrs["url"])

    @staticmethod
    def expand_db_attributes(attrs):
        """
        Given a dict of attributes from the <embed> tag, return the real HTML
        representation for use on the front-end.
        """
        return format.embed_to_frontend_html(attrs["url"])
