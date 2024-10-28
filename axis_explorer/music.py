from enum import Enum


# Deliberately in circle of fifths order to make things easier, and values
# chosen to make to NDLR CC values.
class Pitch(Enum):
    C = 1
    G = 2
    D = 3
    A = 4
    E = 5
    B = 6
    Fs = 7
    Db = 8
    Ab = 9
    Eb = 10
    Bb = 11
    F = 12


def pitch_str(p: Pitch) -> str:
    name = p.name
    if len(name) == 2 and name[1] == "s":
        return f"{name[0]}#"
    return name


# Values chosen deliberately to map to NDLR CC values.
class ScaleMode(Enum):
    Ionian = 1
    Dorian = 2
    Phrygian = 3
    Lydian = 4
    Mixolydian = 5
    Aeolian = 6
    Locrian = 7


def mode_suffix_str(m: ScaleMode) -> str:
    if m == ScaleMode.Aeolian:
        return "m"
    return ""


class CircleOfFifths:
    def __init__(self, root: Pitch):
        self.root = root

    def forward(self, number: int) -> Pitch:
        return Pitch(((self.root.value - 1 + number) % 12) + 1)

    def backward(self, number: int) -> Pitch:
        return Pitch(((self.root.value - 1 - number) % 12) + 1)


def tritone_sub(pitch: Pitch) -> Pitch:
    return CircleOfFifths(pitch).forward(6)


class Axis:
    def __init__(self, root: Pitch):
        self.circle = CircleOfFifths(root)

    def tonic_primary(self) -> tuple[Pitch, Pitch]:
        primary = self.circle.root
        return (primary, tritone_sub(primary))

    def tonic_secondary(self) -> tuple[Pitch, Pitch]:
        secondary = self.circle.forward(3)
        return (secondary, tritone_sub(secondary))

    def subdominant_primary(self) -> tuple[Pitch, Pitch]:
        primary = self.circle.backward(1)
        return (primary, tritone_sub(primary))

    def subdominant_secondary(self) -> tuple[Pitch, Pitch]:
        secondary = self.circle.forward(2)
        return (secondary, tritone_sub(secondary))

    def dominant_primary(self) -> tuple[Pitch, Pitch]:
        primary = self.circle.forward(1)
        return (primary, tritone_sub(primary))

    def dominant_secondary(self) -> tuple[Pitch, Pitch]:
        secondary = self.circle.forward(4)
        return (secondary, tritone_sub(secondary))

    def __str__(self) -> str:
        def names(notes: tuple[Pitch, Pitch]) -> str:
            one, two = notes
            return f"({one.name}, {two.name})"

        return "".join([
            f"Axis(root={self.circle.root.name}, ",
            f"tonic_primary={names(self.tonic_primary())}, ",
            f"tonic_secondary={names(self.tonic_secondary())}, ",
            f"subdominant_primary={names(self.subdominant_primary())}, ",
            f"subdominant_secondary={names(self.subdominant_secondary())}, ",
            f"dominant_primary={names(self.dominant_primary())}, ",
            f"dominant_secondary={names(self.dominant_secondary())})",
        ])
