import pickle
from typing import Optional

class GF256_Number:
    """
    Represents a number in the Galois Field GF(256).
    
    Attributes:
        alpha (int): The alpha-notation value of the GF256 number.
        integer (int): The integer-notation value of the GF256 number.

        at least one of the alpha or the integer notation values have to be specified!

    '2**alpha = integer'
    """

    log_table = None
    antilog_table = None

    def __init__(self, alpha: Optional[int] = None, integer: Optional[int] = None) -> None:
        """
        Initializes a new GF256_Number

        """

        filepath_log_table = "resources/log_table.pickle"
        filepath_antilog_table = "resources/antilog_table.pickle"

        if GF256_Number.log_table is None:
            self._load_log_table(filepath_log_table)
        if GF256_Number.antilog_table is None:
            self._load_antilog_table(filepath_antilog_table)

        if alpha is None and integer is None:
            # Neither were specified
            raise ValueError("Neither the alpha-notation, nor the integer-notation were specified")
        
        elif alpha is None:
            # Integer was specified
            if not 1 <= integer <= 255:
                raise ValueError(f"the specified integer is not in GF(256), must be in the range 1 <= integer <= 255, not: {integer}")
            
            self._integer = integer
            self._alpha = self._integer_to_alpha(integer)

        elif integer is None:
            # Alpha was specified
            if not 0 <= alpha <= 255:
                raise ValueError(f"the specified alpha is not in GF(256), must be in the range 0 <= alpha <= 255, not: {alpha}")
            
            self._alpha = alpha
            self._integer = self._alpha_to_integer(alpha)

        elif not (alpha is None or integer is None):
            # Both arguments were specified
            if not 0 <= alpha <= 255:
                raise ValueError(f"the specified alpha is not in GF(256), must be in the range 0 <= alpha <= 255, not: {alpha}")
            elif not 1 <= integer <= 255:
                raise ValueError(f"the specified integer is not in GF(256), must be in the range 1 <= integer <= 255, not: {integer}")
            
            if alpha == self._integer_to_alpha(integer):
                self._alpha = alpha
                self._integer = integer
            else:
                raise ValueError("There was a mismatch between the specified alpha-notation and integer-notation of the number")

    def __str__(self) -> str:
        return f"integer: {self.integer}, alpha: {self.alpha}"
    
    def __repr__(self):
        return f"GF256({self.integer, self.alpha})"
 
    def __add__(self, other: "GF256_Number") -> "GF256_Number":
        if isinstance(other, GF256_Number):
            return GF256_Number.gf256_add(self, other)
        # elif isinstance(other, int):
        #     # this would treat other-integers as the integer part of GF256_Numbers
        #     return self + GF256_Number(integer=other)
        else:
            raise TypeError("GF256 addition is only defined for other GF256 elements")
    
    def __iadd__(self, other: "GF256_Number") -> "GF256_Number":
        result = GF256_Number.gf256_add(self, other)
        self._alpha = result.alpha
        self._integer = result.integer
        return self

    def __mul__(self, other: "GF256_Number") -> "GF256_Number":
        return GF256_Number.gf256_multiply(self, other)
    
    def __imul__(self, other: "GF256_Number") -> "GF256_Number":
        result = GF256_Number.gf256_multiply(self, other)
        self._alpha = result.alpha
        self._integer = result.integer
        return self

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: int):
        if not 0 <= alpha <= 255:
            raise ValueError(f"the specified alpha is not in GF(256), must be in the range 0 <= alpha <= 255, not: {alpha}")
        
        self._alpha = alpha
        self._integer = self._alpha_to_integer(alpha)

    @property
    def integer(self) -> int:
        return self._integer

    @integer.setter
    def integer(self, integer: int):
        if not 1 <= integer <= 255:
            raise ValueError(f"the specified integer is not in GF(256), must be in the range 1 <= integer <= 255, not: {integer}")
        
        self._integer = integer
        self._alpha = self._integer_to_alpha(integer)

    @classmethod
    def _load_log_table(cls, filepath_log_table) -> list:
        with open(filepath_log_table, 'rb') as file:
            log_table = pickle.load(file)
    
        cls.log_table = log_table

    @classmethod
    def _load_antilog_table(cls, filepath_antilog_table) -> list:
        with open(filepath_antilog_table, 'rb') as file:
            antilog_table = pickle.load(file)

        cls.antilog_table = antilog_table

    def _integer_to_alpha(self, integer: int) -> int:
        """ 
        converts from integer to alpha-notation
        antilog_table[integer] = alpha
        """
        alpha = GF256_Number.antilog_table[integer]
        return alpha

    def _alpha_to_integer(self, alpha: int) -> int:
        """ 
        converts from alpha to integer-notation
        log_table[alpha] = integer
        """
        integer = GF256_Number.log_table[alpha]
        return integer
    
    @staticmethod
    def gf256_multiply(a: "GF256_Number", b: "GF256_Number") -> "GF256_Number":
        """
        Multiplies two GF256 Numbers

        adding the exponents, as it is quivalent to multiplying
            eg. a**n * a**m = a**(n+m)
        """
        alpha = a.alpha + b.alpha
        return GF256_Number(alpha=alpha%255)

    @staticmethod
    def gf256_add(a: "GF256_Number", b: "GF256_Number") -> "GF256_Number":
        """
        Adds two GF256 NUmbers
        equivalent to bitwise XOR
        """
        print(f"{a=}, {b=}, {a.integer^b.integer=}")
        return GF256_Number(integer=a.integer ^ b.integer)

def main():
    g1 = GF256_Number(integer=5)
    g2 = GF256_Number(integer=6)

    # TODO: if g1 is equal to g2 and the two are added the result is integer=0, which is currently not allowed

    print(g1 + g2)
    print(g1 * g2)

if __name__ == "__main__":
    main()