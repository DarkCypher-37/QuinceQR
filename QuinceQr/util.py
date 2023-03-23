import numpy as np

from itertools import zip_longest, product

from enumerations import *
import lookup_tables


digits = "0123456789" # only digits
alphanumeric = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:" # digits, cap_alphabet, space, $, %, *, +, -, ., /, :

def get_char_id(char: str) -> int:
    """
    returns the id of an character in alphanumeric encoding

    """

    return alphanumeric.find(char)

def get_size_from_version(version: int) -> SizeLevel:
    """
    returns the SizeLevel of the QR-Code

    """

    if 1 <= version <= 9:
        return SizeLevel.small
    if 10 <= version <= 26:
        return SizeLevel.medium
    if 27 <= version <= 40:
        return SizeLevel.large
    raise ValueError(f"the specified version is not between 1 through 40 (inclusive): {version}")

def calculate_character_counter_indicater_pad(version: int, mode: ModeIndicator) -> int:
    """
    returns the length of the character_count_indicator pad

    Parameters
    ----------
    version: int
        the version of the QR-Code
    mode: ModeIndicator
        the mode for the data encoding

    Returns
    -------
    int
        length of the character_count_indicator pad
    """
    
    return lookup_tables.char_count_byte_length_for_version_and_mode[get_size_from_version(version)][mode]

def get_qr_code_version(character_length: int, mode: ModeIndicator, error_correction_level: ErrorCorrectionLevel, minimum_version:int=1) -> int:
    """ 
    get the minumum version (equivalent to the size of the qr code) for the specified mode and error correction level
    
    Parameters
    ----------
    character_length: int
        length of the data to be encodeded
    mode: ModeIndicator
        mode of the encoding used for the data
    error_correction_level: ErrorCorrectionLevel
        the Error Correction Level of the QR-Code
    minimum_version:int = 1
        a wished for minimum version, meaning that if the specified minimum_version is large enough, it will be returned

    Returns
    -------
    int
        the version of the QR-Code
    """
    
    for index, version in enumerate(lookup_tables.version_dict):
        length_in_version = version[error_correction_level][mode.value]
        if length_in_version >= character_length:
            return max(index+1, minimum_version)

    raise Exception("too much data, can't fit inside QR-Code")

def get_mode_indicator_bits(mode: ModeIndicator) -> str:
    """ 
    get the corresponding bits for the mode

    """
    
    return lookup_tables.mode_indicator_mapping[mode]

def get_total_number_codewords(version: int, error_correction_level: ErrorCorrectionLevel) -> int:
    """ 
    get the amount of total datacodewords in a QR-Code for any given version & error correction level
    
    Returns
    -------
    int
        Total Number of Data Codewords for this Version and EC Level
        error_correction_table[0]
    
    """
    
    error_correction_info = lookup_tables.error_correction_table[version, error_correction_level]
    return error_correction_info[0]

def get_blocks_per_group(version: int, error_correction_level: ErrorCorrectionLevel) -> tuple:
    """ 
    get the amount of blocks per group 
    
    Returns
    -------
    tuple
        (Number of Blocks in Group 1, Number of Blocks in Group 2)
        (error_correction_table[2], error_correction_table[4])
    
    """
    
    error_correction_info = lookup_tables.error_correction_table[version, error_correction_level]
    return (error_correction_info[2], error_correction_info[4])

def get_codewords_per_block(version: int, error_correction_level: ErrorCorrectionLevel) -> tuple:
    """ 
    get the amount of codewords per block of group 1 and group 2
    
    Returns
    -------
    tuple
        (Number of Data Codewords in Each of Group 1's Blocks, Number of Data Codewords in Each of Group 2's Blocks)
        (error_correction_table[3], error_correction_table[5])
    
    """
    
    error_correction_info = lookup_tables.error_correction_table[version, error_correction_level]
    return (error_correction_info[3], error_correction_info[5])

def get_error_correction_codewords_per_block(version: int, error_correction_level: ErrorCorrectionLevel) -> int:
    """ 
    get the amount of error correction codewords per block (is the same for both groups!)
    
    Returns
    -------
    int
        EC Codewords Per Block
        error_correction_table[1]
    
    """
    
    error_correction_info = lookup_tables.error_correction_table[version, error_correction_level]
    return error_correction_info[1]


def split_string_into_chunks(string: str, chunk_size: int = 8):
    """ 
    split a string into evenly sized chunks

    """
    return [string[index:(index+chunk_size)] for index in range(0, len(string), chunk_size)]

def interweave_codewords(codewords: list) -> list:
    # flatten, to make one array of blocks
    flattened = sum(codewords, [])
    # zip together all the blocks
    zipped = zip_longest(*flattened, fillvalue=None)
    # remove all 'None's and flatten again
    result = list(filter(lambda value: value is not None, sum(zipped, ())))
    return result

# with open('../resources/remainder_bits.pickle', 'rb') as file:
#     # Load the array from the file using pickle
#     remainder_bits_table = pickle.load(file)

def get_remainder_bits(version: int) -> int:
    if not 1 <= version <= 40:
        raise ValueError(f"the version needs to be in the range 1 through 40")
    return lookup_tables.remainder_bits_table[version-1]

def calc_qr_size(version: int) -> int:
    """ 
    calculate the width or height of the QR-Code when given a version

    """
    return (((version-1)*4)+21)

def place_pattern(matrix: np.ndarray, pattern: np.ndarray, upper_left_corner: tuple, overwrite=True) -> np.ndarray:
    """ 
    place a pattern from a small 2d array into a big 2d array at a certain position
    if overwrite is False, the matrix will not be change if something beside 'Module.empty' would be overwritten
    """

    mat = matrix.copy()

    # Check that the pattern fits within the bounds of the matrix
    if upper_left_corner[0] + len(pattern[0]) > len(mat[0]) or upper_left_corner[1] + len(pattern) > len(mat):
        raise ValueError(f"Pattern does not fit within matrix bounds: {upper_left_corner=}, {mat.shape=}, {pattern.shape=}")

    # Check that the upper_left_corner coordinates are valid
    if upper_left_corner[0] < 0 or upper_left_corner[1] < 0:
        raise ValueError("Upper left corner coordinates must be non-negative")

    end = upper_left_corner[0]+len(pattern[0]), upper_left_corner[1]+len(pattern)

    # only change the matrix if the 'overwrite' flag is set
    if not overwrite:
        area = mat[upper_left_corner[1]:end[1], upper_left_corner[0]:end[0]]
        if not np.all(area == np.full_like(pattern, fill_value=Module.empty)):
            return mat
        
    mat[upper_left_corner[1]:end[1], upper_left_corner[0]:end[0]] = pattern

    return mat

def calculate_finder_positions(version: int) -> tuple:
    """ 
    returns the top left corners of the finder positions, when given a version
    """
    # return (0, 0), ((((version-1)*4)+21) - 7, 0), (0, (((version-1)*4)+21) - 7)
    return (0, 0), (14 + 4*(version-1), 0), (0, 14 + 4*(version-1))

def shift_finder_pattern(upper_left_corner: tuple, offset: tuple) -> tuple:
    """ 
    shift the finder pattern to the new position within an 8x8 matrix
    """
    shifted_pattern = place_pattern(np.full((8, 8), fill_value=Module.white), lookup_tables.FINDER_PATTERN, offset)
    upper_left_corner = upper_left_corner[0]-offset[0], upper_left_corner[1]-offset[1]
    
    return shifted_pattern, upper_left_corner

def get_alignment_positions(version: int) -> list:
    """ 
    returns the top left corners of the alignment positions, when given a version
    """
    if not 2 <= version <= 40:
        raise ValueError(f"The QR-Code version must be in the range '2 <= version <= 40' not {version}")

    return list(product(lookup_tables.alignment_pattern_locations_table[version], repeat=2))

def make_timing_patterns(version: int) -> tuple:
    """ 
    returns horizontal and vertical timing patterns
    """
    size = calc_qr_size(version)
    length = int((size-16)/2)
    # interchanging black and white, but starts with black and ends with black
    horizontal = np.array([[Module.black, *[Module.white, Module.black]*length]])
    
    return horizontal, np.rot90(horizontal)

def get_version_information_string(version: int) -> str:
    """
    returns the version information string for any given version (must be above version 6!)
    """
    if 6 < version < 41:
        return lookup_tables.version_information_string[version]
    raise ValueError(f"version must be in range 6 < version < 41, not: {version=}")


def get_format_information_string(error_correction_level: ErrorCorrectionLevel, mask_pattern_num: int) -> str:
    if not 0 <= mask_pattern_num <= 7:
        raise ValueError(f"mask_pattern_num must be in range 0 <= mask_pattern_num <= 7, not: {mask_pattern_num=}")
    return lookup_tables.format_information_string[error_correction_level, mask_pattern_num]

masking_conditions = [
    lambda row, column: (row + column) % 2 == 0,
    lambda row, column: row % 2 == 0,
    lambda row, column: column % 3 == 0,
    lambda row, column: (row + column) % 3 == 0,
    lambda row, column: ( int(row / 2) + int(column / 3) ) % 2 == 0,
    lambda row, column: ((row * column) % 2) + ((row * column) % 3) == 0,
    lambda row, column: ( ((row * column) % 2) + ((row * column) % 3) ) % 2 == 0,
    lambda row, column: ( ((row + column) % 2) + ((row * column) % 3) ) % 2 == 0
]

evaluation_condition3_pattern = np.array([Module.white, Module.white, Module.white, Module.white, Module.black, Module.white, Module.black, Module.black, Module.black, Module.white, Module.black])

def main():
    # get_size_from_version(...)
    # ...

    # calculate_character_counter_indicater_pad(...)
    assert calculate_character_counter_indicater_pad(1, ModeIndicator.alphanumeric_mode) == 9
    assert calculate_character_counter_indicater_pad(20, ModeIndicator.byte_mode) == 16

    # get_qr_code_version(...)
    assert get_qr_code_version(20, ModeIndicator.alphanumeric_mode, ErrorCorrectionLevel.M, minimum_version=10) == 10
    assert get_qr_code_version(2000, ModeIndicator.alphanumeric_mode, ErrorCorrectionLevel.L) == 27
    assert get_qr_code_version(2000, ModeIndicator.numeric_mode, ErrorCorrectionLevel.Q, minimum_version=26) == 28
    assert get_qr_code_version(2000, ModeIndicator.byte_mode, ErrorCorrectionLevel.L) == 33
    assert get_qr_code_version(7089, ModeIndicator.numeric_mode, ErrorCorrectionLevel.L) == 40 # biggest numeric possible

    # get_mode_indicator_bits(...)
    # print(get_mode_indicator_bits(ModeIndicator.alphanumeric_mode))

    # get_total_number_codewords(...)
    assert get_total_number_codewords(1, ErrorCorrectionLevel.Q) == 13
    assert get_total_number_codewords(40, ErrorCorrectionLevel.H) == 1276

    # get_blocks_per_group(...)
    assert get_blocks_per_group(1, ErrorCorrectionLevel.Q) == (1, 0)
    assert get_blocks_per_group(5, ErrorCorrectionLevel.Q) == (2, 2)
    assert get_blocks_per_group(40, ErrorCorrectionLevel.L) == (19, 6)
    assert get_blocks_per_group(33, ErrorCorrectionLevel.M) == (14, 21)

    # get_codewords_per_block(...)
    assert get_codewords_per_block(1, ErrorCorrectionLevel.Q) == (13, 0)
    assert get_codewords_per_block(5, ErrorCorrectionLevel.Q) == (15, 16)
    assert get_codewords_per_block(40, ErrorCorrectionLevel.L) == (118, 119)
    assert get_codewords_per_block(33, ErrorCorrectionLevel.M) == (46, 47)

    # get_error_correction_codewords_per_block(...)
    assert get_error_correction_codewords_per_block(1, ErrorCorrectionLevel.M) == 10
    assert get_error_correction_codewords_per_block(40, ErrorCorrectionLevel.H) == 30

    # split_string_into_chunks(...)
    # ...

    # multiply_terms(...)
    # combine(...) 
    # make_generator_polynomial(...)
    # print([coefficient.integer for coefficient in make_generator_polynomial(7)])
    # should print: [1, 127, 122, 154, 164, 11, 68, 117]

    # poly_div(...)
    # ...

    # polynomial_long_division_gf256(...)
    # ...

    # interweave_codewords(...)
    test_codewords = [
        [
            [
                [67, 85, 70, 134, 87, 38, 85, 194, 119, 50, 6, 18, 6, 103, 38],
                [246, 246, 66, 7, 118, 134, 242, 7, 38, 86, 22, 198, 199, 146, 6]
            ],
            [
                [182, 230, 247, 119, 50, 7, 118, 134, 87, 38, 82, 6, 134, 151, 50, 7],
                [70,247,118,86,194,6,151,50,16,236,17,236,17,236,17,236]
            ]
        ],
        [
            [
                [213, 199, 11, 45, 115, 247, 241, 223, 229, 248, 154, 117, 154, 111, 86, 161, 111, 39],
                [87, 204, 96, 60, 202, 182, 124, 157, 200, 134, 27, 129, 209, 17, 163, 163, 120, 133]
            ],
            [
                [148, 116, 177, 212, 76, 133, 75, 242, 238, 76, 195, 230, 189, 10, 108, 240, 192, 141],
                [235, 159, 5, 173, 24, 147, 59, 33, 106, 40, 255, 172, 82, 2, 131, 32, 178, 236]
            ]
        ]
    ]


    fin = [67, 246, 182, 70, 85, 246, 230, 247, 70, 66, 247, 118, 134, 7, 119, 86, 87, 118, 50, 194, 38, 134, 7, 6, 85, 242, 118, 151, 194, 7, 134, 50, 119, 38, 87, 16, 50, 86, 38, 236, 6, 22, 82, 17, 18, 198, 6, 236, 6, 199, 134, 17, 103, 146, 151, 236, 38, 6, 50, 17, 7, 236]
    fin_err = [213, 87, 148, 235, 199, 204, 116, 159, 11, 96, 177, 5, 45, 60, 212, 173, 115, 202, 76, 24, 247, 182, 133, 147, 241, 124, 75, 59, 223, 157, 242, 33, 229, 200, 238, 106, 248, 134, 76, 40, 154, 27, 195, 255, 117, 129, 230, 172, 154, 209, 189, 82, 111, 17, 10, 2, 86, 163, 108, 131, 161, 163, 240, 32, 111, 120, 192, 178, 39, 133, 141, 236]

    assert interweave_codewords(test_codewords[0]) == fin
    assert interweave_codewords(test_codewords[1]) == fin_err

    # get_remainder_bits(...)
    assert get_remainder_bits(40) == 0
    assert get_remainder_bits(1) == 0

    # calculate_finder_positions(...)
    assert calculate_finder_positions(17) == ((0, 0), (78, 0), (0, 78))

    # get_alignment_positions(...)
    assert get_alignment_positions(2) == get_alignment_positions(2)


if __name__ == "__main__":
    main()