import threading

from PIL import Image, ImageColor, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper


BRIGHTNESS = 30
FONT = "Rajdhani-Bold.ttf"


#def print_deck_info(index, deck):
#    key_image_format = deck.key_image_format()
#    touchscreen_image_format = deck.touchscreen_image_format()
#
#    flip_description = {
#        (False, False): "not mirrored",
#        (True, False): "mirrored horizontally",
#        (False, True): "mirrored veritically",
#        (True, True): "mirrored horizontally/vertically",
#    }
#
#    print(f"Deck {index} - {deck.deck_type()}")
#    print(f" - ID: {deck.id()}")
#    print(f" - Serial: {deck.get_serial_number()}")
#    print(f" - Firmware Version: {deck.get_firmware_version()}")
#    print(f" - Key Count: {deck.key_count()}, {deck.key_layout()[0]}x{deck.key_layout()[1]}")
#
#    if deck.is_visual():
#        print(f" - Key Image Size: {key_image_format['size'][0]}x{key_image_format['size'][1]}")
#        print(f" - Format: {key_image_format['format']}")
#        print(f" - Rotation: {key_image_format['rotation']}")
#        print(f" - Flip: {flip_description[key_image_format['flip']]}")
#
#        if deck.is_touch():
#            print(f" - Touch Image Size: {touchscreen_image_format['size'][0]}x{touchscreen_image_format['size'][1]}")
#            print(f" - Format: {touchscreen_image_format['format']}")
#            print(f" - Rotation: {touchscreen_image_format['rotation']}")
#            print(f" - Flip: {flip_description[touchscreen_image_format['flip']]}")


def render_key_image(deck, label):
    image = Image.new("RGB", deck.key_image_format()["size"], ImageColor.getrgb("blue"))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, 30)
    draw.text((image.width / 2, image.height / 2), text=label, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_key_format(deck, image)


def update_key_image(deck, key, state):
    label = "Pressed!" if state else f"Key {key}"
    image = render_key_image(deck, label)
    with deck:
        deck.set_key_image(key, image)


def key_change_callback(deck, key, state):
    print(type(deck))
    print(type(key))
    print(f"Deck {deck.id()}, Key {key} = {state}", flush=True)


def main():
    decks = DeviceManager().enumerate()
    print(f"Found {len(decks)} Stream Decks.")
    for index, deck in enumerate(decks):
        deck.open()
        deck.reset()
        deck.set_brightness(BRIGHTNESS)
        print(f"Opened {deck.deck_type()} ({deck.id()})")

        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        deck.set_key_callback(key_change_callback)

        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass


if __name__ == "__main__":
    main()
