from enum import Enum, auto

class ErrorCorrectionLevel(Enum):
    L = 1
    M = 2
    Q = 3
    H = 4

class ModeIndicator(Enum):
    numeric_mode = 0
    alphanumeric_mode = 1
    byte_mode = 2
    kanji_mode = 3

class SizeLevel(Enum):
    small = auto()
    medium = auto()
    large = auto()

class Module(Enum):
    empty = auto()
    black = auto()
    white = auto()
    data_white = auto()
    data_black = auto()
    reserved_for_format_information = auto()
    reserved_for_version_information = auto()
