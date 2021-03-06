"""Implements the hashids algorithm in python. For more information, visit
http://www.hashids.org/. Compatible with Python 2.6, 2.7 and 3"""

import warnings
from functools import wraps
from math import ceil
import numpy as np

__version__ = '1.2.0'

RATIO_SEPARATORS = 3.5
RATIO_GUARDS = 12

try:
    StrType = basestring
except NameError:
    StrType = str

def _is_str(candidate):
    """Returns whether a value is a string."""
    return isinstance(candidate, StrType)


def _is_uint(number):
    """Returns whether a value is an unsigned integer."""
    try:
        return number == int(number) and number >= 0
    except ValueError:
        return False


def _split(string, splitters):
    """Splits a string into parts at multiple characters"""
    part = ''
    for character in string:
        if character in splitters:
            yield part
            part = ''
        else:
            part += character
    yield part


def _hash(number, alphabet):
    """Hashes `number` using the given `alphabet` sequence."""
    hashed = ''
    len_alphabet = len(alphabet)
    while True:
        hashed = alphabet[number % len_alphabet] + hashed
        number //= len_alphabet
        if not number:
            return hashed


def _unhash(hashed, alphabet):
    """Restores a number tuple from hashed using the given `alphabet` index."""
    number = 0
    len_alphabet = len(alphabet)
    for character in hashed:
        position = alphabet.index(character)
        number *= len_alphabet
        number += position
    return number


def _reorder(string, salt):
    """Reorders `string` according to `salt`."""
    len_salt = len(salt)

    if len_salt != 0:
        string = list(string)
        index, integer_sum = 0, 0
        for i in range(len(string) - 1, 0, -1):
            integer = ord(salt[index])
            integer_sum += integer
            j = (integer + index + integer_sum) % i
            string[i], string[j] = string[j], string[i]
            index = (index + 1) % len_salt
        string = ''.join(string)

    return string


def _index_from_ratio(dividend, divisor):
    """Returns the ceiled ratio of two numbers as int."""
    return int(ceil(float(dividend) / divisor))


def _ensure_length(encoded, min_length, alphabet, guards, values_hash):
    """Ensures the minimal hash length"""
    len_guards = len(guards)
    guard_index = (values_hash + ord(encoded[0])) % len_guards
    encoded = guards[guard_index] + encoded

    if len(encoded) < min_length:
        guard_index = (values_hash + ord(encoded[2])) % len_guards
        encoded += guards[guard_index]

    split_at = len(alphabet) // 2
    while len(encoded) < min_length:
        alphabet = _reorder(alphabet, alphabet)
        encoded = alphabet[split_at:] + encoded + alphabet[:split_at]
        excess = len(encoded) - min_length
        if excess > 0:
            from_index = excess // 2
            encoded = encoded[from_index:from_index+min_length]

    return encoded

def _decode(hashid, salt, alphabet, separators, guards):
    """Helper method that restores the values encoded in a hashid without
    argument checks."""
    parts = tuple(_split(hashid, guards))
    hashid = parts[1] if 2 <= len(parts) <= 3 else parts[0]

    if not hashid:
        return

    lottery_char = hashid[0]
    hashid = hashid[1:]

    hash_parts = _split(hashid, separators)
    for part in hash_parts:
        alphabet_salt = (lottery_char + salt + alphabet)[:len(alphabet)]
        alphabet = _reorder(alphabet, alphabet_salt)
        yield _unhash(part, alphabet)

def _encode(values, salt, min_length, alphabet, separators, guards):
    """Helper function that does the hash building without argument checks."""

    len_alphabet = len(alphabet)
    len_separators = len(separators)
    values_hash = sum(x % (i + 100) for i, x in enumerate(values))
    encoded = lottery = alphabet[values_hash % len(alphabet)]

    for i, value in enumerate(values):
        if value < 0:
            value = -value
        alphabet_salt = (lottery + salt + alphabet)[:len_alphabet]
        alphabet = _reorder(alphabet, alphabet_salt)
        last = _hash(value, alphabet)
        encoded += last
        value %= ord(last[0]) + i
        encoded += separators[value % len_separators]

    encoded = encoded[:-1]  # cut off last separator

    return (encoded if len(encoded) >= min_length else
            _ensure_length(encoded, min_length, alphabet, guards, values_hash))



def _deprecated(func):
    """A decorator that warns about deprecation when the passed-in function is
    invoked."""
    @wraps(func)
    def with_warning(*args, **kwargs):
        warnings.warn(
            ('The %s method is deprecated and will be removed in v2.*.*' %
             func.__name__),
            DeprecationWarning
        )
        return func(*args, **kwargs)
    return with_warning


class Hashids(object):
    """Hashes and restores values using the "hashids" algorithm."""
    ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    def __init__(self, salt='', min_length=0, alphabet=ALPHABET):
        """
        Initializes a Hashids object with salt, minimum length, and alphabet.
        :param salt: A string influencing the generated hash ids.
        :param min_length: The minimum length for generated hashes
        :param alphabet: The characters to use for the generated hash ids.
        """
        self._min_length = max(int(min_length), 0)
        self._salt = salt

        separators = ''.join(x for x in 'cfhistuCFHISTU' if x in alphabet)
        alphabet = ''.join(x for i, x in enumerate(alphabet)
                           if alphabet.index(x) == i and x not in separators)

        len_alphabet, len_separators = len(alphabet), len(separators)
        if len_alphabet + len_separators < 16:
            raise ValueError('Alphabet must contain at least 16 '
                             'unique characters.')

        separators = _reorder(separators, salt)

        min_separators = _index_from_ratio(len_alphabet, RATIO_SEPARATORS)

        number_of_missing_separators = min_separators - len_separators
        if number_of_missing_separators > 0:
            separators += alphabet[:number_of_missing_separators]
            alphabet = alphabet[number_of_missing_separators:]
            len_alphabet = len(alphabet)

        alphabet = _reorder(alphabet, salt)
        num_guards = _index_from_ratio(len_alphabet, RATIO_GUARDS)
        if len_alphabet < 3:
            guards = separators[:num_guards]
            separators = separators[num_guards:]
        else:
            guards = alphabet[:num_guards]
            alphabet = alphabet[num_guards:]

        self._alphabet = alphabet
        self._guards = guards
        self._separators = separators

        # Support old API
        self.decrypt = _deprecated(self.decode)
        self.encrypt = _deprecated(self.encode)

    def encode(self, *values):
        """Builds a hash from the passed `values`.
        :param values The values to transform into a hashid
        >>> hashids = Hashids('arbitrary salt', 16, 'abcdefghijkl0123456')
        >>> hashids.encode(1, 23, 456)
        '1d6216i30h53elk3'
        """
        if not values:
            return ''

        # negative = False
            # negative = True
        if "." in str(values[0]):
            str_parts = str(values[0]).split(".")
            int_parts = [(int(str_parts[0]),), (int("1" + str_parts[1]),)]

            finalstr = _encode(int_parts[0], self._salt, self._min_length, self._alphabet,
                       self._separators, self._guards) + "." + _encode(int_parts[1], self._salt, self._min_length, self._alphabet,
                       self._separators, self._guards)
            if values[0] < 0:
                return "-" + finalstr
            else:
                return finalstr
        else:
            finalstr = _encode(values, self._salt, self._min_length, self._alphabet,
                       self._separators, self._guards)
            if values[0] < 0:
                return "-" + finalstr
            else:
                return finalstr

        return _encode(values, self._salt, self._min_length, self._alphabet,
                       self._separators, self._guards)

    def check(self, value, hashid):
        if self.encode(value) == hashid:
            print("Correct!")
        else:
            print("We believe this is not the right answer")
            raise ValueError

    def check_matrix(self, matrix, correct_matrix):
        if matrix.shape != correct_matrix.shape:
            print("We believe this is not the right answer")
            raise ValueError
        for (x,y),value in np.ndenumerate(matrix):
            if self.encode(value) != correct_matrix[x][y]:
                print("We believe this is not the right answer")
                raise ValueError
        print("Correct!")
        return True

    def encode_matrix(self, matrix):
        final_matrix = np.empty(matrix.shape, dtype="U30")
        for (x,y),value in np.ndenumerate(matrix):
            final_matrix[x][y] = self.encode(value)
        return final_matrix

    def decode(self, hashid):
        """Restore a tuple of numbers from the passed `hashid`.
        :param hashid The hashid to decode
        >>> hashids = Hashids('arbitrary salt', 16, 'abcdefghijkl0123456')
        >>> hashids.decode('1d6216i30h53elk3')
        (1, 23, 456)
        """
        if not hashid or not _is_str(hashid):
            return ()
        negative = False

        try:
            if "-" in hashid:
                negative = True
                hashid = hashid[1:]
            if "." in hashid:
                str_parts = hashid.split(".")
                integer_part = str_parts[0]
                decimal_part = str_parts[1]
                number = str(tuple(_decode(integer_part, self._salt, self._alphabet,
                                        self._separators, self._guards))[0]) + "." + str(tuple(_decode(decimal_part, self._salt, self._alphabet,
                                        self._separators, self._guards))[0])[1:]
                number = float(number)
            else:
                number = tuple(_decode(hashid, self._salt, self._alphabet,
                                        self._separators, self._guards))[0]
            if negative:
                return -number
            else:
                return number
            numbers = tuple(_decode(hashid, self._salt, self._alphabet,
                                    self._separators, self._guards))

            return numbers if hashid == self.encode(*numbers) else ()
        except ValueError:
            return ()

    def encode_hex(self, hex_str):
        """Converts a hexadecimal string (e.g. a MongoDB id) to a hashid.
        :param hex_str The hexadecimal string to encodes
        >>> Hashids.encode_hex('507f1f77bcf86cd799439011')
        'y42LW46J9luq3Xq9XMly'
        """
        numbers = (int('1' + hex_str[i:i+12], 16)
                   for i in range(0, len(hex_str), 12))
        try:
            return self.encode(*numbers)
        except ValueError:
            return ''

    def decode_hex(self, hashid):
        """Restores a hexadecimal string (e.g. a MongoDB id) from a hashid.
        :param hashid The hashid to decode
        >>> Hashids.decode_hex('y42LW46J9luq3Xq9XMly')
        '507f1f77bcf86cd799439011'
        """
        return ''.join(('%x' % x)[1:] for x in self.decode(hashid))



def test_function():
    print("test")

# hashids = Hashids(salt="mth314", min_length=10)
# a = hashids.encode(-6345)
# print(a)
# print(hashids.decode(a))

# b = np.matrix([[4.4,3.2,2.5],[5.8,3,2],[6,4,2]])
# encoded_b = hashids.encode_matrix(b)
# print(encoded_b)

# c = np.matrix([[4,3,2],[-5,3,2],[6,4,2]])
# hashids.check_matrix(c,encoded_b)

# d = np.matrix([[4.4,3.2,2.5],[5.8,3,2],[6,4,2]])
# hashids.check_matrix(d,encoded_b)

# dec_test = hashids.encode(-5.6)
# print(dec_test)
# print(hashids.decode(dec_test))
# hashids.check(-5.6,"-B1Ok4pk5jQ.Gl4MQ62Lna")

# zero_test = hashids.encode(5.6)
# print(hashids.decode(zero_test))
# zero_test = hashids.encode(5.04353032432406)
# print(zero_test)
# print(hashids.decode(zero_test))
# zero_test = hashids.encode(5.006)
# print(hashids.decode(zero_test))