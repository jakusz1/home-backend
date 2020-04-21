from enum import Enum, auto, IntEnum

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class DenonKey(str, AutoName):
    MD_TRACK_DOWN = auto()
    MD_TRACK_UP = auto()
    MD_REV = auto()
    MD_FFWD = auto()
    MD_REC = auto()
    MD_PAUSE = auto()
    MD_STOP = auto()
    MD_PLAY = auto()
    CD_TRACK_DOWN = auto()
    CD_TRACK_UP = auto()
    CD_REV = auto()
    CD_FFWD = auto()
    CD_DISC_SKIP = auto()
    CD_PAUSE = auto()
    CD_STOP = auto()
    CD_PLAY = auto()
    TUNER_PRESET_UP = auto()
    TUNER_PRESET_DOWN = auto()
    DECK_REV = auto()
    DECK_FFWD = auto()
    DECK_PLAY = auto()
    DECK_PLAY_REV = auto()
    DECK_A_B = auto()
    DECK_REC = auto()
    DECK_PAUSE = auto()
    DECK_STOP = auto()
    KEY_VOLUMEUP = auto()
    KEY_VOLUMEDOWN = auto()
    AMP_PHONO = auto()
    AMP_TAPE = auto()
    AMP_MD = auto()
    AMP_CD = auto()
    AMP_TUNER = auto()
    AMP_AUX = auto()
    AMP_MUTE = auto()
    AMP_POWER = auto()


class DenonInput(str, AutoName):
    AMP_PHONO = auto()
    AMP_TAPE = auto()
    AMP_MD = auto()
    AMP_CD = auto()
    AMP_TUNER = auto()
    AMP_AUX = auto()
