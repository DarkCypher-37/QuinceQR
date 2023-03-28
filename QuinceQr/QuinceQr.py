import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from typing import Callable

from enumerations import *
from lookup_tables import ALIGNMENT_PATTERN
import polynomial_division
import util

__all__ = ["QrCode", "ErrorCorrectionLevel"]

class QrCode:

    def __init__(self, data: str, error_correction_level: ErrorCorrectionLevel, version: int = 1, force_mask: int = None) -> None:
        """
        makes a QR-Code

        Parameters
        ----------
        data : str
            the text of the QR-Code
        error_correction_level: ErrorCorrectionLevel
            diffrent Levels specify how much redundant data there will be:
                ErrorCorrectionLevel.L =  7% \n
                ErrorCorrectionLevel.M = 15% \n
                ErrorCorrectionLevel.Q = 25% \n
                ErrorCorrectionLevel.H = 30% \n
        force_mask: int
            the number of the mask to be applied, when None the best will be used

        Returns
        -------
        ModeIndicator
            the ModeIndicator for the mode of the data
        """

        self.data = data
        self.error_correction_level = error_correction_level
        
        self.qr_code_matrix = self._make_qr_code(version, force_mask=force_mask)
        


    def _get_mode(self) -> ModeIndicator:
        """
        returns the mode for the specified data
        will only return numeric, alphanumeric or byte mode, as kanji is not implemented

        Parameters
        ----------
        data : str
            the text of the QR-Code

        Returns
        -------
        ModeIndicator
            the ModeIndicator for the mode of the data
        """

        if set(self.data).issubset(util.digits): # or use re.match
            return ModeIndicator.numeric_mode
        elif set(self.data).issubset(util.alphanumeric):
            return ModeIndicator.alphanumeric_mode
        else:
            return ModeIndicator.byte_mode
    

    def _make_character_counter_indicater(self, mode: ModeIndicator):
        """
        returns the character_count_indicator of the QR-Code

        Parameters
        ----------
        version: int
            the version of the QR-Code

        Returns
        -------
        SizeLevel
            the size level of the QR-Code
        """
        pad = util.calculate_character_counter_indicater_pad(self.version, mode)        # get the amount of padding needed
        return format(len(self.data), f">0{pad}b")                                      # pad the binary to the length specified

    def _encode_alphanumeric_mode(self) -> str:
        """
        encode text in alphanumeric mode

        Parameters
        ----------

        Returns
        -------
        str
            the encoded data
        """

        encoded_data = ""
        pairs = [self.data[i:i+2] for i in range(0, len(self.data), 2)]
        
        for pair in pairs:
            if len(pair) == 1:
                val = util.get_char_id(pair)
                encoded_data += format(val, ">06b")
                break
            
            val1 = util.get_char_id(pair[0])
            val2 = util.get_char_id(pair[1])
            pair_val = (45*val1)+val2

            encoded_data += format(pair_val, ">011b")
        return encoded_data

    def _encode_numeric_mode(self) -> str:
        """
        encode text in numeric mode

        Parameters
        ----------

        Returns
        -------
        str
            the encoded data
        """

        encoded_data = ""
        pairs = [self.data[i:i+3] for i in range(0, len(self.data), 3)]

        for pair in pairs:
            if len(pair) == 1 or pair[0:2] == "00":
                encoded_data += format(int(pair), ">04b")
            elif len(pair) == 2 or pair[0] == "0":
                encoded_data += format(int(pair), ">07b")
            elif len(pair) == 3:
                encoded_data += format(int(pair), ">010b")
        return encoded_data

    def _encode_byte_mode(self) -> str:
        """
        encode text in byte mode

        Parameters
        ----------

        Returns
        -------
        str
            the encoded data
        """
        data_bytes = self.data.encode("ISO 8859-1")         # iso 8859 latin-1 (Western europe)
        # data_bytes = self.data.encode("UTF-8")            # utf-8 (not supported by all readers and does not produce good results for larger QR-Codes)

        encoded_data = "".join(format(byte, "0>8b") for byte in data_bytes)
        return encoded_data

    def _encode_kanji_mode(self) -> str:
        raise NotImplementedError

    def _encode_text(self, mode):
        """
        encode text in the given mode

        Parameters
        ----------
        data: str
            the data to be encoded

        Returns
        -------
        str
            the encoded data
        """
        if mode == ModeIndicator.numeric_mode:
            return self._encode_numeric_mode()
        elif mode == ModeIndicator.alphanumeric_mode:
            return self._encode_alphanumeric_mode()
        elif mode == ModeIndicator.byte_mode:
            return self._encode_byte_mode()
        elif mode == ModeIndicator.kanji_mode:
            return self._encode_kanji_mode()
        raise TypeError(f"mode not found: {mode}")
        
    def _add_terminator(self, bit_string: str, total_data_bits_required: int) -> str:
        """ 
        returns the encoded_data_bits with the terminator appended (just a bunch of zeroes)

        """

        length_difference = total_data_bits_required - len(bit_string)
        terminator_length = min(4, length_difference)
        return bit_string + "0" * terminator_length
    
    def _add_padding(self, bit_string: str) -> str:
        """ 
        returns the encoded_data_bits with padding (just a bunch of zeroes)

        """

        pad_length = 8-len(bit_string)%8
        return  bit_string + "0" * pad_length

    def _fill_with_pad_bytes(self, total_bit_string: str, total_data_bits_required: int) -> str:
        """ 
        fill the encoded_data_bits with the pad_bytes, (alternating '11101100' and '00010001')

        """

        pad_byte1, pad_byte2 = "11101100", "00010001"

        while len(total_bit_string) < total_data_bits_required:
            total_bit_string += pad_byte1
            pad_byte1, pad_byte2 = pad_byte2, pad_byte1

        return total_bit_string

    def _encoded_data_to_bits(self, mode: ModeIndicator, encoded_data: str) -> str:
        character_count_indicator = self._make_character_counter_indicater(mode)

        encoded_data_bits = util.get_mode_indicator_bits(mode) + character_count_indicator + encoded_data
        total_number_bits_required = util.get_total_number_codewords(self.version, self.error_correction_level)*8

        encoded_data_bits = self._add_terminator(encoded_data_bits, total_number_bits_required)
        encoded_data_bits = self._add_padding(encoded_data_bits)
        encoded_data_bits = self._fill_with_pad_bytes(encoded_data_bits, total_number_bits_required)

        return encoded_data_bits

    def _split_in_groups(self, codewords: list, num_of_blocks_per_group: tuple, num_of_codewords_per_block: tuple) -> list:
        """
        Sorts a list of codewords into the appropriate groups and blocks

        
        The codewords need to be sorted into 2 Groups, each containing x and y blocks respectivly
        In Group 1 each Block contains n codewords, in Group 2 each block contains m codewords

        The codewords need to be sorted into 2 Groups, each containing 'num_of_blocks_per_group[0]' and 'num_of_blocks_per_group[1]' blocks respectivly
        In Group 1 each Block contains 'num_of_codewords_per_block[0]' codewords, in Group 2 each block contains 'num_of_codewords_per_block[1]' codewords
        
        Group 1                 | Group 2
        Block 1 ... Block x     | Block 1 ... Block y
        n or m number of codewords per block

        
        Returns
        -------
        list
            codewords sorted into groups
        """

        groups = []
        for group_index in range(2):
            group_offset = group_index*num_of_blocks_per_group[0]*num_of_codewords_per_block[0]
            group = []

            for block_index in range(num_of_blocks_per_group[group_index]):
                block_offset = block_index*num_of_codewords_per_block[group_index]
                
                block = [codewords[group_offset + block_offset + codeword_index_in_block] for codeword_index_in_block in range(num_of_codewords_per_block[group_index])]
                group.append(block)
            groups.append(group)

        return groups

    def _make_error_correction_codewords(self, data_codewords_in_groups: list, generator_polynomial: list) -> list:
        """
        make the error correction codewords
        """

        error_correction_codewords_in_groups = []

        # convert data_codewords from binary to integers
        for group_index, group in enumerate(data_codewords_in_groups):
            for block_index, block in enumerate(group):
                data_codewords_in_groups[group_index][block_index] = [int(codeword, 2) for codeword in block]

        # make the error_correction_codewords and arange them into groups and blocks
        for group in data_codewords_in_groups:
            error_correction_codewords_single_group = []
            for block in group:
                error_correction_codewords_single_block = polynomial_division.divide_polynomials(block, generator_polynomial)
                error_correction_codewords_single_group.append(error_correction_codewords_single_block)
            error_correction_codewords_in_groups.append(error_correction_codewords_single_group)

        return error_correction_codewords_in_groups

    def _all_codewords_to_bits(self, all_codewords: list) -> str:
        """
        formats all the codewords to bits again and adds remainder bits
        """

        num_remainder_bits = util.get_remainder_bits(self.version)
        bit_string = ''.join(format(byte, '08b') for byte in all_codewords) + '0'*num_remainder_bits
        return bit_string

    def _place_finder_patterns(self, matrix: np.ndarray) -> np.ndarray:
        """
        place the finder patterns in the QR-Code
        """
        mat = matrix.copy()

        finder_pattern_seperator_offsets = [(0, 0), (1, 0), (0, 1)]
        for position, offset in zip(util.calculate_finder_positions(self.version), finder_pattern_seperator_offsets):
            mat = util.place_pattern(mat, *util.shift_finder_pattern(position, offset), overwrite=False)
        return mat

    def _place_alignment_patterns(self, matrix: np.ndarray) -> np.ndarray:
        """
        place the alignment patterns in the QR-Code
        """
        mat = matrix.copy()
        
        for alignment_position in util.get_alignment_positions(self.version):
            upper_left_corner = alignment_position[0]-2, alignment_position[1]-2
            mat = util.place_pattern(mat, ALIGNMENT_PATTERN, upper_left_corner, overwrite=False)
        return mat

    def _place_timing_patterns(self, matrix) -> np.ndarray:
        """
        place the timing patterns in the QR-Code
        """
        
        horizontal, vertical = util.make_timing_patterns(self.version)
        mat = util.place_pattern(matrix, horizontal, (8, 6))
        mat = util.place_pattern(mat, vertical, (6, 8))
        return mat
    
    def _place_dark_module(self, matrix: np.ndarray) -> np.ndarray:
        """
        place the dark module in the QR-Code
        """
        
        mat = matrix.copy()
        coords = (8, ((4 * self.version) + 9))
        mat[coords[::-1]] = Module.black
        return mat

    def _reserve_format_information_area(self, matrix: np.ndarray) -> np.ndarray:
        """
        reserve the area for format information in the QR-Code
        """

        def top_left():
            x = 8
            for y in range(0, 6):
                mat[y, x] = Module.reserved_for_format_information

            y = 8
            for x in range(0, 6):
                mat[y, x] = Module.reserved_for_format_information

            coords = [(8, 8), (7, 8), (8, 7)]
            for coord in coords:
                mat[coord] = Module.reserved_for_format_information

        def top_right():
            y = 8
            for x in range(size-8, size):
                mat[y, x] = Module.reserved_for_format_information
        
        def bottom_left():
            x = 8
            for y in range(size-7, size):
                mat[y, x] = Module.reserved_for_format_information
        
        mat = matrix.copy()
        size = util.calc_qr_size(self.version)

        top_left()
        top_right()
        bottom_left()
        return mat

    def _reserve_version_information_area(self, matrix: np.ndarray) -> np.ndarray:
        """
        reserve the area for version information in the QR-Code (for version 7 and above)
        """

        size = util.calc_qr_size(self.version)

        # top right
        pattern = np.full((3, 6), fill_value=Module.reserved_for_version_information)
        upper_left_corner = (0, size-11)
        mat = util.place_pattern(matrix, pattern, upper_left_corner)

        # bottom left
        pattern = np.full((6, 3), fill_value=Module.reserved_for_version_information)
        upper_left_corner = (size-11, 0)
        mat = util.place_pattern(mat, pattern, upper_left_corner)
        
        return mat

    def _place_function_patterns(self, matrix: np.ndarray) -> np.ndarray:
        """
        place all the required function patterns in the QR-Code
        """

        mat = self._place_finder_patterns(matrix)

        if self.version >= 2:
            mat = self._place_alignment_patterns(mat)

        mat = self._place_timing_patterns(mat)
        mat = self._place_dark_module(mat)
        mat = self._reserve_format_information_area(mat)

        if self.version >= 7:
            mat = self._reserve_version_information_area(mat)

        return mat
    
    def _fill_qr_code(self, bit_string: str, matrix: np.ndarray) -> np.ndarray:
        """
        fill the QR-Code with the bits/modules
        """

        def data_bytes_iterator(data):
            # temp = 0
            for bit in data:
                # temp += 1
                yield Module.data_black if bit == '1' else Module.data_white

            raise Exception("you should never have come here, but now that you are here ...")
            # print("you should never have come here, but now that you are here ...") # TODO
            # print(f"{temp=}")
            # # raise ...
            # while True:
            #     yield Module.black

        bits = data_bytes_iterator(bit_string)

        mat = np.rot90(matrix)

        y = 0
        direction = -1 # start with placing modules from right to left
        while y < len(mat)-1:
            # skip the timing pattern, we should arrive here after a full completion of 2 rows ...
            if y == util.calc_qr_size(self.version)-7:
                # print(f"skipping a row:") # TODO: remove
                # pp_mat([mat[y]])
                y +=1

            for x in range(len(mat[0]))[::direction]:
                # only fill in data, if the area is not already filled, otherwise skip ...
                if mat[y, x] == Module.empty:
                    mat[y, x] = next(bits)
                if mat[y+1, x] == Module.empty:
                    mat[y+1, x] = next(bits)

            y+=2
            direction *= -1 # reverse the module placing direction

        return np.rot90(mat, k=-1)
    
    def _place_version_information_string(self, matrix: np.ndarray) -> np.ndarray:
        """
        place the version information string into the QR-Code, for versions above 6
        there are potetial conflicts with the order of Module placement in the bottom left, as one source used a wrong (?) order! (But this algorithm should be inline with the QR-Code standard)
        """

        if not 6 < self.version < 41:
            raise ValueError(f"version must be in range 6 < version < 41, not {self.version}")

        def version_information_string_generator(version_information_string: str):
            for bit in version_information_string:
                yield Module.white if bit == '0' else Module.black
            raise Exception("outside of bounds!!!")

        mat = matrix.copy()
        size = util.calc_qr_size(self.version)
        version_information_string = util.get_version_information_string(self.version)

        # top_right
        data = version_information_string_generator(version_information_string)
        for row_index in reversed(range(0, 6)):
            for index in reversed(range(size-11, size-8)):
                mat[row_index, index] = next(data)

        # bottom_left orig (this is apparently incorrect !!)
        # data = version_information_string_generator(version_information_string)
        # for index in range(0, 6):
        #     for row_index in range(size-11, size-8):
        #         mat[row_index, index] = next(data)

        # bottom_left reversed on x and y (this seems to be the correct way!!)
        data = version_information_string_generator(version_information_string)
        for index in reversed(range(0, 6)):
            for row_index in reversed(range(size-11, size-8)):
                mat[row_index, index] = next(data)
        
        return mat
    
    def _apply_mask(self, matrix: np.ndarray, pattern_formula: Callable[[int, int], bool]):
        """
        applies a given mask on the QR-Code
        """

        mat = matrix.copy()

        for (row_index, index), value in np.ndenumerate(mat):
            if pattern_formula(row_index, index):
                # toggle the module
                if value == Module.data_black:
                    mat[row_index, index] = Module.data_white
                elif value == Module.data_white:
                    mat[row_index, index] = Module.data_black
                # if value == 1.:                         # TODO REMOVE
                #     mat[row_index, index] = 0           # TODO REMOVE

        return mat
    
    def _evaluation_condition_1(self, matrix: np.ndarray) -> int:
        """ 
        returns the penalty for evaluation condition #1 (chains of same colored modules)
        """

        penalty = 0

        # horizontal
        for row_index in range(len(matrix)):
            last_module = None
            consecutive_chain_len = 1
            for index in range(len(matrix[0])):
                current_module = matrix[row_index, index]
                if last_module is None:
                    last_module = current_module
                elif last_module == current_module:
                    consecutive_chain_len += 1
                else:
                    if consecutive_chain_len >= 5:
                        penalty += consecutive_chain_len -2

                    last_module = current_module
                    consecutive_chain_len = 1

            if consecutive_chain_len >= 5:
                penalty += consecutive_chain_len -2

        # vertical
        for index in range(len(matrix)):
            last_module = None
            consecutive_chain_len = 1
            for row_index in range(len(matrix[0])):
                current_module = matrix[row_index, index]
                if last_module is None:
                    last_module = current_module
                elif last_module == current_module:
                    consecutive_chain_len += 1
                else:
                    if consecutive_chain_len >= 5:
                        penalty += consecutive_chain_len -2

                    last_module = current_module
                    consecutive_chain_len = 1

            if consecutive_chain_len >= 5:
                penalty += consecutive_chain_len -2

        return penalty
    
    def _evaluation_squares_patterns_ratio(self, matrix: np.ndarray) -> int:
        """ 
        returns the penaly for evaluation condition #2 (squares), #3 (patterns) and #4 (ratio)
        """

        mat = matrix.copy()

        penalty = 0

        num_total_modules = np.product(mat.shape)
        num_black_modules = 0

        for (row_index, index), value in np.ndenumerate(mat):

            if value == Module.black:
                num_black_modules += 1

            square = mat[row_index:row_index+2, index:index+2]
            if square.shape == (2, 2) and square[0, 0] == square[0, 1] == square[1, 0] == square[1, 1]:
            # if not(index+2 > len(mat[0]) or row_index+2 > len(mat)):
                penalty += 3
                # print(f"hit: {row_index, index=}")
            
            row = mat[row_index, index:index+11]
            if row.shape == (11,) and np.array_equal(row, util.evaluation_condition3_pattern):
                # print(f"WooW! {row_index, index=}")
                penalty += 40
                
            col = mat[row_index:row_index+11, index]
            if col.shape == (11,) and np.array_equal(col, util.evaluation_condition3_pattern):
                # print(f"here! {row_index, index=}")
                penalty += 40

        floor_div_res = int((num_black_modules/num_total_modules*100) // 5)
        ratio_penalty = int(min(abs(floor_div_res*5 - 50)/5, abs(floor_div_res*5 - 45)/5) * 10)

        return penalty + ratio_penalty
    
    def _calculate_penalty(self, matrix: np.ndarray) -> int:
        return self._evaluation_condition_1(matrix) + self._evaluation_squares_patterns_ratio(matrix)

    def _apply_best_mask(self, matrix: np.ndarray) -> tuple:
        """
        tries to figure out the mask with the least amount of bad patterns (lowest penalty)
        (currently broken; but applying any mask will provide a working QR-Code ...)
        """

        penalties = []
        matrices = []

        for index, mask_pattern in enumerate(util.masking_conditions):
            mat = self._apply_mask(matrix, mask_pattern)
            penalty = self._calculate_penalty(mat)
            penalties.append(penalty)
            matrices.append(mat)
            # print(f"{index, penalty}")
        
        index = np.argmin(penalties)

        # print(f"{penalties=}")  # TODO: remove
        # print(f"{index=}")      # TODO: remove
        
        return matrices[index], index
    
    def _place_format_information_string(self, matrix: np.ndarray, mask_pattern_num: int) -> np.ndarray:
        """
        places the format information string into the QR-Code
        """

        format_information_string = util.get_format_information_string(self.error_correction_level, mask_pattern_num)
        mat = matrix.copy()

        def format_information_string_generator(format_information_string: str):
            for bit in format_information_string:
                yield Module.white if bit == '0' else Module.black
            raise Exception("outside of bounds!!!")

        data = format_information_string_generator(format_information_string)

        index = 8
        for row_index in reversed(range(len(mat))):
            if mat[row_index, index] == Module.reserved_for_format_information:
                mat[row_index, index] = next(data)
        
        data = format_information_string_generator(format_information_string)
        
        row_index = 8
        for index in range(len(mat)):
            if mat[row_index, index] == Module.reserved_for_format_information:
                mat[row_index, index] = next(data)

        return mat

    def _unify_blacks_and_whites(self, matrix: np.ndarray) -> np.ndarray:
        """
        consolidata Module.data_black and Module.data_white into just Module.black and Module.white
        """

        mat = matrix.copy()
        mat = np.where(mat == Module.data_black, Module.black, mat) # type:ignore
        mat = np.where(mat == Module.data_white, Module.white, mat) # type:ignore
        return mat

    def _encoding_phase(self, requested_minimum_version) -> str:
        """
        the encoding phase of QR-Code generation
        """

        mode = self._get_mode()

        if requested_minimum_version is None:
            self.version = util.get_qr_code_version(len(self.data), mode, self.error_correction_level)
        else:
            self.version = util.get_qr_code_version(len(self.data), mode, self.error_correction_level, requested_minimum_version)

        encoded_data = self._encode_text(mode)
        encoded_data_bits = self._encoded_data_to_bits(mode, encoded_data)

        return encoded_data_bits

    def _error_correction_phase(self, encoded_data_bits: str) -> tuple:
        """
        the error correction phase of QR-Code generation
        """
        
        codewords = util.split_string_into_chunks(encoded_data_bits, 8)
        assert all(len(codeword) == 8 for codeword in codewords) # TODO: remove
        
        num_of_blocks_per_group = util.get_blocks_per_group(self.version, self.error_correction_level)
        num_of_codewords_per_block = util.get_codewords_per_block(self.version, self.error_correction_level)
        data_codewords_in_groups = self._split_in_groups(codewords, num_of_blocks_per_group, num_of_codewords_per_block)

        num_of_error_correction_codewords = util.get_error_correction_codewords_per_block(self.version, self.error_correction_level)
        generator_polynomial = polynomial_division.make_generator_polynomial(num_of_error_correction_codewords)
        
        error_correction_codewords_in_groups = self._make_error_correction_codewords(data_codewords_in_groups, generator_polynomial)

        return data_codewords_in_groups, error_correction_codewords_in_groups

    def _structuring_phase(self, data_codewords_in_groups: list, error_correction_codewords_in_groups: list) -> str:
        """
        the structuring phase of QR-Code generation
        """
        
        num_of_blocks_per_group = util.get_blocks_per_group(self.version, self.error_correction_level)

        # interweave if there is more than one block
        # => interweave if there are just blocks in group 1
        if sum(num_of_blocks_per_group) > 1:
            all_codewords = util.interweave_codewords(data_codewords_in_groups) + util.interweave_codewords(error_correction_codewords_in_groups)
        else:
            # else just use 1 block:
            all_codewords = data_codewords_in_groups[0][0] + error_correction_codewords_in_groups[0][0]

        bit_string = self._all_codewords_to_bits(all_codewords)
        return bit_string

    def _layout_phase(self, bit_string: str, force_mask: int = None, border_size: int = 3) -> np.ndarray:
        """
        layout the matrix for the QR-Code and place all the Modules within the matrix

        Parameters
        ----------
        bit-string: str
            the string of bits to be placed in the matrix
        force_mask: int = None
            when provided, forces a certain mask to be used. (needs to be in range 0..7 (both inclusive))
        border_size: int = 3
            when provided, makes a white perimeter around the QR-Code (mesured in Modules from one side to the QR-Code)
        
        """

        size = util.calc_qr_size(self.version)
        matrix = np.full((size, size), Module.empty)

        matrix = self._place_function_patterns(matrix)
        
        matrix = self._fill_qr_code(bit_string, matrix)

        if self.version >= 7:
            matrix = self._place_version_information_string(matrix)

        if force_mask is None:
            # FIXME: this method seems to be faulty ...
            matrix, mask_pattern_num = self._apply_best_mask(matrix)
        else:
            mask_pattern = util.masking_conditions[force_mask]
            matrix = self._apply_mask(matrix, mask_pattern)

            mask_pattern_num = force_mask

        matrix = self._place_format_information_string(matrix, mask_pattern_num)
        matrix = self._unify_blacks_and_whites(matrix)

        matrix = util.place_pattern(np.full((matrix.shape[0]+border_size*2, matrix.shape[1]+border_size*2), fill_value=Module.white), pattern=matrix, upper_left_corner=(3, 3))

        return matrix

    def _make_qr_code(self, requested_minimum_version: int, force_mask: int = None):
        """
        compute the QR-Code
        """

        encoded_data_bits = self._encoding_phase(requested_minimum_version)
        data_codewords_in_groups, error_correction_codewords_in_groups = self._error_correction_phase(encoded_data_bits)
        bit_string = self._structuring_phase(data_codewords_in_groups, error_correction_codewords_in_groups)
        matrix = self._layout_phase(bit_string, force_mask=force_mask)

        return matrix


    # to implement:
    # consider setter and getters for self.data ...
    def change_data(self):
        ...

    def make_image(self, image_size: tuple = 600):
        """
        make the QR-Code data matrix into an pillow image
        """

        rgb_matrix = np.empty((*self.qr_code_matrix.shape, 3), dtype=np.uint8)

        for (row_index, col_index), value in np.ndenumerate(self.qr_code_matrix):
            rgb_matrix[row_index, col_index] = np.array([0, 0, 0]) if value == Module.black else np.array([255, 255, 255])

        img = Image.fromarray(rgb_matrix)
        img = img.resize((image_size, image_size), resample=Image.NEAREST)
        # img = img.resize((image_size, image_size), resample=Image.NEAREST)
        
        return img


def main():
    # qr = QuinceQr("HELLO WORLD", ErrorCorrectionLevel.Q, version=7)
    # text = """Herbert Tremenheere Hewett (25 May 1864 – 4 March 1921) was an English amateur first-class cricketer who played for Somerset, captaining the county from 1889 to 1893, as well as Oxford University and the Marylebone Cricket Club. A battling left-handed opening batsman, Hewett could post a large score in a short time against even the best bowlers. Capable of hitting the ball powerfully, he combined an excellent eye with an unorthodox style to be regarded at his peak as one of England's finest batsmen. """
    # text = "Die Nutzdatencodierung und die QR Code-Speichercodierung haben an also sich nichts miteinander zu tun. Die verschiedenen QR Code-Speichercodierungen NUMERIC, ALHPANUMERIC, KANJI und 8-BIT existieren nur, weil je nach Input die Daten aufgrund verschiedener Codewortlängen effektiver gepackt werden. D.h. bei NUMERIC kann man eine längere Zahl bzw. mehr numerische Zeichen im QR Code speichern, als wenn man die gleiche Zahl mit der 8-BIT-Codierung im QR Code speichern will"
    # text = "(25 May 1864 – 4 March 1921)"
    # qr = QuinceQr(text, ErrorCorrectionLevel.Q, version=30)
    # print(qr.version)
    # qr = QuinceQr("HELLO WORLD", ErrorCorrectionLevel.Q, version=5)
    # qr = QuinceQr("asdafd sadf345435", ErrorCorrectionLevel.M)
    # qr = QrCode("HELLO WORLD", ErrorCorrectionLevel.Q, force_mask=7)
    qr = QrCode("HELLO WORLD", ErrorCorrectionLevel.Q)
    
    img = qr.make_image()
    img.show()


if __name__ == "__main__":
    main()