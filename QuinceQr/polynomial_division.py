from itertools import zip_longest

from GF256_Number import GF256_Number



def multiply_terms(term1, term2):
    """
    multiply two terms of the generator polynomial
    
    """
    result = []

    for coefficient1, exponent1 in term1:
        for coefficient2, exponent2 in term2:
            result.append((coefficient1*coefficient2, exponent1+exponent2))

    return result

def combine(term):
    """
    combine the generator polynomial
    
    """
    result = [None]*len(term)

    for coefficient, exponent in term:
        if result[exponent] is None:
            result[exponent] = coefficient
        else:
            result[exponent] += coefficient
            result.pop()
    return [(coefficient, exponent) for exponent, coefficient in reversed(list(enumerate(result)))]

def make_generator_polynomial(error_correction_codewords: int) -> list:
    """ 
    make the generator polynomial for the given amount of error correction codewords
    
    Returns
    -------
    list
        an array with the coefficients of generator polynomial
    
    """

    term = lambda n: [(GF256_Number(alpha=0), 1), (GF256_Number(alpha=n), 0)]

    result = term(0)
    for n in range(1, error_correction_codewords):
        result = combine(multiply_terms(result, term(n)))

    return [coefficient for coefficient, exponent in result]

def polynomial_long_division_gf256(message_polynomial: list, generator_polynomial: list) -> list:
    """
    perform the polynomial division
    """

    def polynomial_long_division_gf256_step(message_polynomial: list, generator_polynomial: list) -> list:
        # Multiply the generator_polynomial by the lead term of the messenger_polynomial
        lead_coefficient_message = message_polynomial[0]
        result = [coefficent*lead_coefficient_message for coefficent in generator_polynomial]
        
        # XOR the result with the messenger Polynomial (fill with integer=0)
        coefficient_pairs = zip_longest(message_polynomial, result, fillvalue=GF256_Number(integer=0))
        result = [message_coefficient + result_1a_coefficient for message_coefficient, result_1a_coefficient in coefficient_pairs]

        # discard leading zero
        result = result[1:]
        return result

    result = message_polynomial
    for _ in range(len(message_polynomial)):
        result = polynomial_long_division_gf256_step(message_polynomial=result, generator_polynomial=generator_polynomial)
    
    return result


def divide_polynomials(block: list, generator_polynomial: list) -> list:
    message_polynomial = [GF256_Number(integer=codeword) for codeword in block]
    error_correction_codewords_single_block = polynomial_long_division_gf256(message_polynomial, generator_polynomial)
    error_correction_codewords_single_block = [codeword.integer for codeword in error_correction_codewords_single_block] # convert to integers
    return error_correction_codewords_single_block


def main():
    # multiply_terms(...)
    # combine(...) 
    # make_generator_polynomial(...)
    assert [coefficient.integer for coefficient in make_generator_polynomial(7)] == [1, 127, 122, 154, 164, 11, 68, 117]

    # polynomial_long_division_gf256(...)
    # ...

    # divide_polynomials(...)
    assert divide_polynomials([32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236], make_generator_polynomial(18)) == [141, 200, 113, 155, 101, 253, 211, 137, 230, 12, 37, 93, 52, 6, 180, 144, 233, 213]
    assert divide_polynomials([236, 17, 236, 17, 236, 17, 236, 17, 236, 17, 236, 17, 236, 17, 236, 17], make_generator_polynomial(18)) == [253, 208, 208, 222, 148, 37, 141, 130, 227, 48, 182, 241, 103, 253, 37, 13, 171, 16]


if __name__ == "__main__":
    main()