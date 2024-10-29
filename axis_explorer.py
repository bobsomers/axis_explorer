import threading

from StreamDeck.DeviceManager import DeviceManager
import mido

from axis_explorer.music import Pitch
from axis_explorer.ndlr import NDLR
from axis_explorer.scenes import SceneManager


BRIGHTNESS = 100


def main():
    decks = DeviceManager().enumerate()
    print(f"Found {len(decks)} Stream Deck(s):")
    for deck in decks:
        print(f"  {deck.deck_type()} ({deck.id()})")

    midi_outputs = mido.get_output_names()
    print(f"\nFound {len(midi_outputs)} MIDI output device(s):")
    for midi_out in midi_outputs:
        print(f"  {midi_out}")
    ndlr_devices = [d for d in devices if "NDLR" in d]
    ndlr_device_1 = [d for d in ndlr_devices if " 1" in d]
    assert(len(ndlr_device_1) == 1)

    deck = decks[0]
    midi_device = ndlr_device_1
    ndlr = NDLR(midi_device, 15)

    deck.open()
    deck.reset()
    deck.set_brightness(BRIGHTNESS)

    scene_manager = SceneManager(deck, ndlr)
    scene_manager.render(deck)
    def callback(deck, key, state):
        scene_manager.key_change(deck, key, state)
    deck.set_key_callback(callback)

    print("\nRunning...")
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            pass


if __name__ == "__main__":
    main()
