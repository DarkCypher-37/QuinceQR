import qrcode
import pickle
import numpy as np
import itertools
import matplotlib.pyplot as plt

from enum import Enum, auto
from typing import List, Callable, Any

from enumerations import ErrorCorrectionLevel, ModeIndicator, SizeLevel
import polynomial_division
import util


class QuinceQr:

    def __init__(self, data: str, error_correction_level: ErrorCorrectionLevel, version=None) -> None:
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

        Returns
        -------
        ModeIndicator
            the ModeIndicator for the mode of the data
        """

        self.data = data
        self.error_correction_level = error_correction_level
        
        encoded_data_bits = self._encoding_phase(version)
        data_codewords_in_groups, error_correction_codewords_in_groups = self._error_correction_phase(encoded_data_bits)
        bit_string = self._structuring_phase(data_codewords_in_groups, error_correction_codewords_in_groups)
        # TODO: continue here !!
        print(bit_string)
        


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
        # data_bytes = data.encode("UTF-8")                 # utf-8

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

    def _split_in_groups(self, codewords: list, num_of_blocks_per_group: list, num_of_codewords_per_block: list) -> list:
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

    def _all_codewords_to_bits(self, all_codewords: list) -> str:
        """
        formats all the codewords to bits again and adds remainder bits
        """

        num_remainder_bits = util.get_remainder_bits(self.version)
        bit_string = ''.join(format(byte, '08b') for byte in all_codewords) + '0'*num_remainder_bits
        return bit_string


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

    def layout_phase():
        ...

    def _make_qr_code():
        ...



    # to implement:
    # consider setter and getters for self.data ...
    def change_data():
        ...

    def make_image():
        ...


def main():
    # qr = QuinceQr("HELLO WORLD", ErrorCorrectionLevel.Q, version=5)
    qr = QuinceQr("asdafd sadf345435", ErrorCorrectionLevel.M)
    
    # version, out = make_groups("HELLO WORLD", ErrorCorrectionLevel.Q, version=5)
    
    # qr.data = "12434"
    # assert qr._get_mode() == ModeIndicator.numeric_mode
    # qr.data = "HELLO WORLD*+-123"
    # assert qr._get_mode() == ModeIndicator.alphanumeric_mode
    # qr.data = "324kjdsfSFJ!"
    # assert qr._get_mode() == ModeIndicator.byte_mode

    # qr.data = "Hello, world!"
    # assert qr._encode_byte_mode() == '01001000011001010110110001101100011011110010110000100000011101110110111101110010011011000110010000100001'



if __name__ == "__main__":
    main()