import io
from PIL import Image

from infrastructure.types.enums import IconType


class BaseLogoService:

    def get_icon_stream(self, icon_type: IconType):
        if icon_type == IconType.icon:
            image_path = self.get_icon()
        else:
            image_path = self.get_side_bar_icon()
        logo_stream = io.BytesIO()
        logo = Image.open(image_path)
        logo.save(logo_stream, format=logo.format)
        return logo_stream.getvalue()

    def get_icon(self):
        return ""

    def get_side_bar_icon(self):
        return ""
