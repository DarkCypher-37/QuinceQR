import pickle

# Galois Field
MODULO = 0b100011101

def GF_256_log_antilog_table_generator():
    """ 
    2^n = x
    alpha^n = x
    log_table[n] = x
    antilog_table[x] = n
    the log_table takes the exponent 'n' and returns the integer 'x'
    the antilog_table takes the Integer 'x' and returns the exponent 'n'
    """
    log_table = [2**0]
    antilog_table = [None] * 256

    for power in range(1, 256):
        res = log_table[power-1]*2
        if res >= 256:
            res ^= MODULO

        log_table.append(res)
        # print(f"{power}\t{res}")

    for index, value in enumerate(log_table[:-1]):
        antilog_table[value] = index
    
    return log_table, antilog_table

log_table, antilog_table = GF_256_log_antilog_table_generator()

# verifying
print(log_table[:50] == [1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140])
print(antilog_table[:50] == [None, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181])


# saving
filepath_log_table = "resources/log_table.pickle"
filepath_antilog_table = "resources/antilog_table.pickle"

with open(filepath_log_table, 'wb') as file:
    pickle.dump(log_table, file, protocol=pickle.HIGHEST_PROTOCOL)

with open(filepath_antilog_table, 'wb') as file:
    pickle.dump(antilog_table, file, protocol=pickle.HIGHEST_PROTOCOL)

# loading
filepath_log_table = "resources/log_table.pickle"
filepath_antilog_table = "resources/antilog_table.pickle"

with open(filepath_log_table, 'rb') as file:
    log_table = pickle.load(file)

with open(filepath_antilog_table, 'rb') as file:
    antilog_table = pickle.load(file)

# verifying
print(log_table[:50] == [1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140])
print(antilog_table[:50] == [None, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181])