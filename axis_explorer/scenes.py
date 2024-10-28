from abc import ABC, abstractmethod
from pathlib import Path
import os
import threading

from PIL import Image, ImageColor, ImageDraw, ImageFont
from StreamDeck.Devices.StreamDeckXL import StreamDeckXL
from StreamDeck.ImageHelpers import PILHelper

from axis_explorer.music import Axis, Pitch, pitch_str, ScaleMode, mode_suffix_str
from axis_explorer.ndlr import NDLR

class Scene(ABC):
    def render(self, deck):
        for key in range(deck.key_count()):
            self.render_key(deck, key, False)

    @abstractmethod
    def render_key(self, deck: StreamDeckXL, key: int, pressed: bool):
        pass

    @abstractmethod
    def key_change(self, deck: StreamDeckXL, key: int, pressed: bool):
        pass


class AxisScene(Scene):
    def __init__(self, ndlr: NDLR, root: Pitch):
        self.ndlr = ndlr
        self.axis = Axis(root)

        self.FONT_FILE = Path(os.path.dirname(os.path.abspath(__file__))) / "Rajdhani-Bold.ttf"
        self.big_font = ImageFont.truetype(self.FONT_FILE, 40)
        self.mid_font = ImageFont.truetype(self.FONT_FILE, 30)
        self.small_font = ImageFont.truetype(self.FONT_FILE, 20)

        tonic_pri = self.axis.tonic_primary()
        tonic_sec = self.axis.tonic_secondary()
        subdom_pri = self.axis.subdominant_primary()
        subdom_sec = self.axis.subdominant_secondary()
        dom_pri = self.axis.dominant_primary()
        dom_sec = self.axis.dominant_secondary()

        self.keys = [
            # Row 1
            ("blue", tonic_pri[0], "Primary", ScaleMode.Ionian),
            ("blue", tonic_pri[0], "Primary", ScaleMode.Aeolian),
            ("darkorange", subdom_pri[0], "Primary", ScaleMode.Ionian),
            ("darkorange", subdom_pri[0], "Primary", ScaleMode.Aeolian),
            ("green", dom_pri[0], "Primary", ScaleMode.Ionian),
            ("green", dom_pri[0], "Primary", ScaleMode.Aeolian),
            ("purple", None, None, ScaleMode.Ionian),
            ("purple", None, None, ScaleMode.Dorian),

            # Row 2
            ("blue", tonic_pri[1], "Prim TSub", ScaleMode.Ionian),
            ("blue", tonic_pri[1], "Prim TSub", ScaleMode.Aeolian),
            ("darkorange", subdom_pri[1], "Prim TSub", ScaleMode.Ionian),
            ("darkorange", subdom_pri[1], "Prim TSub", ScaleMode.Aeolian),
            ("green", dom_pri[1], "Prim TSub", ScaleMode.Ionian),
            ("green", dom_pri[1], "Prim TSub", ScaleMode.Aeolian),
            ("purple", None, None, ScaleMode.Phrygian),
            ("purple", None, None, ScaleMode.Lydian),

            # Row 3
            ("blue", tonic_sec[0], "Secondary", ScaleMode.Ionian),
            ("blue", tonic_sec[0], "Secondary", ScaleMode.Aeolian),
            ("darkorange", subdom_sec[0], "Secondary", ScaleMode.Ionian),
            ("darkorange", subdom_sec[0], "Secondary", ScaleMode.Aeolian),
            ("green", dom_sec[0], "Secondary", ScaleMode.Ionian),
            ("green", dom_sec[0], "Secondary", ScaleMode.Aeolian),
            ("purple", None, None, ScaleMode.Mixolydian),
            ("purple", None, None, ScaleMode.Aeolian),

            # Row 4
            ("blue", tonic_sec[1], "Scnd TSub", ScaleMode.Ionian),
            ("blue", tonic_sec[1], "Scnd TSub", ScaleMode.Aeolian),
            ("darkorange", subdom_sec[1], "Scnd TSub", ScaleMode.Ionian),
            ("darkorange", subdom_sec[1], "Scnd TSub", ScaleMode.Aeolian),
            ("green", dom_sec[1], "Scnd TSub", ScaleMode.Ionian),
            ("green", dom_sec[1], "Scnd TSub", ScaleMode.Aeolian),
            ("purple", None, None, ScaleMode.Locrian),
            ("black", None, None, None),
        ]

    def render_key(self, deck: StreamDeckXL, key: int, pressed: bool):
        self._set_key_image(deck, key)

    def key_change(self, deck: StreamDeckXL, key: int, pressed: bool):
        if not pressed:
            return

        _, axis_pitch, axis_quality, scale_mode = self.keys[key]

        if axis_pitch is None and axis_quality is None and scale_mode is None:
            # TODO: Return to root note selection scene
            pass
        elif axis_pitch is None and scale_mode is not None:
            self.ndlr.set_key(self.axis.circle.root)
            self.ndlr.set_mode(scale_mode)
        elif axis_pitch is not None and scale_mode is not None:
            self.ndlr.set_key(axis_pitch)
            self.ndlr.set_mode(scale_mode)
            self.ndlr.set_chord_degree(1)

    def _set_key_image(self, deck: StreamDeckXL, key: int):
        bgcolor, axis_pitch, axis_quality, scale_mode = self.keys[key]

        image = Image.new("RGB", deck.key_image_format()["size"], ImageColor.getrgb(bgcolor))
        draw = ImageDraw.Draw(image)

        if axis_pitch is not None and scale_mode is not None:
            draw.text((image.width / 2, image.height * 2 / 5),
                      text=f"{pitch_str(axis_pitch)}{mode_suffix_str(scale_mode)}",
                      font=self.big_font,
                      anchor="mm",
                      fill="white")
            draw.text((image.width / 2, image.height * 5 / 7),
                      text=axis_quality,
                      font=self.small_font,
                      anchor="mm",
                      fill="white")
        elif scale_mode is not None:
            draw.text((image.width / 2, image.height * 2 / 5),
                      text=f"{self.axis.circle.root.name}",
                      font=self.big_font,
                      anchor="mm",
                      fill="white")
            draw.text((image.width / 2, image.height * 5 / 7),
                      text=f"{scale_mode.name}",
                      font=self.small_font,
                      anchor="mm",
                      fill="white")
        else:
            draw.text((image.width / 2, image.height / 2),
                      text="Root\nNote",
                      font=self.mid_font,
                      anchor="mm",
                      fill="white")

        deck.set_key_image(key, PILHelper.to_native_key_format(deck, image))
