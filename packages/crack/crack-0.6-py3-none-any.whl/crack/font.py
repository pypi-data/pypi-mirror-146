# -*- coding: utf-8 -*-
# @author: leesoar

"""something."""

from hashlib import md5

from fontTools.ttLib import TTFont

__all__ = ["Font"]


class Font(TTFont):
    __StepError = type("StepError", (Exception, ), {})

    def __init__(self, file):
        self.file = file
        if self.__is_url():
            self.__fetch_font_from_web()
        super().__init__(self.file)

    def __is_url(self):
        return self.file.startswith(("http://", "https://"))

    def __fetch_font_from_web(self):
        import io
        import requests
        self.file = io.BytesIO(requests.get(self.file).content)

    def __get_coords_digest(self, name, font=None):
        font = font or self
        if not name.startswith("uni"):
            name = name.encode("unicode_escape").upper().replace(b"\U", b"uni").decode()
        try:
            return md5(str(font["glyf"][name].coordinates).encode()).hexdigest()
        except (KeyError, AttributeError):
            return

    def mapping(self, real_names, cur_names=None, *, start=0, end=None):
        """Map correctly

        Make a correct mapping relationship.

        Args:
            real_names: you can also understand that it is correct names, like [1, 2]
            cur_names: from font file, like ["\u21b3", "\u9a3d"] or ["uni21B3", "uni9A3D"]
            start: start index
            end: end index
        """
        cur_names = cur_names or self.getGlyphNames()[start:end]
        self.__mapping = dict(zip(map(lambda x: self.__get_coords_digest(x), cur_names), real_names))

    def decode(self, content) -> str:
        """Decode content

        Get correct glyph results.

        Args:
            content: strings with wrong glyph name

        Return:
            correct content
        """
        if not hasattr(self, f"_{self.__class__.__name__}__mapping"):
            raise self.__StepError("call 'mapping' first.")
        if not hasattr(self, f"_{self.__class__.__name__}__need_trans_font"):
            raise self.__StepError("call 'load' first.")
        return "".join(str(self.__mapping.get(self.__get_coords_digest(char, self.__need_trans_font), char)) for char in content)

    def load(self, font: TTFont):
        """Load font

        Load the font what you need to decode.

        Args:
            font: type => 'Font' or 'TTFont'
        """
        self.__need_trans_font = font
