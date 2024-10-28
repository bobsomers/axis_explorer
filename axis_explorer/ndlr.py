import mido

from axis_explorer.music import Pitch, ScaleMode


class NDLR:
    def __init__(self, device: str, midi_channel: int):
        self.port = mido.open_output(device)
        self.channel = (midi_channel - 1) % 16
        self.key_msg = mido.Message("control_change",
                                    channel=self.channel,
                                    control=73,
                                    value=1)
        self.mode_msg = mido.Message("control_change",
                                     channel=self.channel,
                                     control=74,
                                     value=0)
        self.chord_degree_msg = mido.Message("control_change",
                                             channel=self.channel,
                                             control=26,
                                             value=1)

    def close(self):
        if not self.port.closed:
            self.port.close()

    def set_key(self, pitch: Pitch):
        msg = self.key_msg.copy(value=pitch.value)
        self.port.send(msg)

    def set_mode(self, mode: ScaleMode):
        msg = self.mode_msg.copy(value=mode.value)
        self.port.send(msg)

    def set_chord_degree(self, degree: int):
        degree = ((degree - 1) % 7) + 1
        msg = self.chord_degree_msg.copy(value=degree)
        self.port.send(msg)
