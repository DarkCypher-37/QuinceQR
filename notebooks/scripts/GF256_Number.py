import pickle

class GF256_Number:

    def __init__(self, alpha=None, integer=None) -> None:
        
        self.log_table = self.load_log_table()
        self.antilog_table = self.load_antilog_table()

        # TODO: proper commenting

        if alpha is None and integer is None:
            # Neither were specified
            raise ValueError("Neither the alpha-notation, nor the integer-notation were specified")
        
        elif alpha is None:
            # integer was specified
            if not 1 <= integer <= 255:
                raise ValueError(f"the specified integer is not in GF(256), must be in the range 1 <= integer <= 255, not: {integer}")
            
            self._integer = integer
            self._alpha = self._integer_to_alpha(integer)

        elif integer is None:
            # alpha was specified
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

    def load_log_table(self) -> list:
        filepath_log_table = "../resources/log_table.pickle"

        with open(filepath_log_table, 'rb') as file:
            log_table = pickle.load(file)

        return log_table
    
    def load_antilog_table(self) -> list:
        filepath_antilog_table = "../resources/antilog_table.pickle"

        with open(filepath_antilog_table, 'rb') as file:
            antilog_table = pickle.load(file)

        return antilog_table

    def _integer_to_alpha(self, integer: int) -> int:
        """ 
        antilog_table[integer] = alpha
        """
        alpha = self.antilog_table[integer]
        return alpha

    def _alpha_to_integer(self, alpha: int) -> int:
        """ 
        log_table[alpha] = integer
        """
        integer = self.log_table[alpha]
        return integer
    
    @staticmethod
    def gf256_multiply(a: "GF256_Number", b: "GF256_Number") -> "GF256_Number":
        # adding the exponents, as it is quivalent to multiplying
        # eg. a**n * a**m = a**(n+m)
        alpha = a.alpha + b.alpha
        return GF256_Number(alpha=alpha%255)

    @staticmethod
    def gf256_add(a: "GF256_Number", b: "GF256_Number") -> "GF256_Number":
        return GF256_Number(integer=a.integer ^ b.integer)