"""Miscellenious functions in the `better_cryptography` library."""

import os
import gc
import string
import secrets
import hashlib as hash
from random import shuffle
from Crypto.Util.strxor import strxor
from platform import system as get_platform
from Crypto.Util.number import isPrime, getPrime, GCD
from Crypto.Util.RFC1751 import english_to_key, key_to_english


class InvalidKeyArgument(Exception):
    """
    Raised when a key generation function recieves an incorrect parameter, or when a given parameter does not meet the requirements of the underlying key generation function.
    """
    pass


def hash_(ToHash, hash_code:str, return_hex=True, return_length = 256): # tested
    """
    Miscellenious function for implementing hash algorithms.

    Parameters:
    `ToHash`: The bytes to be hashed; if not bytes, it will be converted to bytes.
    `hash_code`: A string indicating which hashing algorithm to use.
    currently supported hashes are:
    
    `'SHA256'`: SHA256 hashing algorithm.
    `'SHA_384'`: SHA384 hashing algorithm.
    `'SHA512'`: SHA512 hashing algorithm.
    `'MD5'`: MD5 hashing algorithm.
    `'SHA1'`: SHA1 hashing algorithm.
    `'SHA3_224'`: SHA3_224 hashing algorithm.
    `'SHA3_256'`: SHA3-256 hashing algorithm.
    `'SHA3_384'`: SHA3-384 hashing algorithm.
    `'SHA3_512'`: SHA3-512 hashing algorithm.
    `'BLAKE2b'`: BLAKE2b hashing algorithm.
    `'BLAKE2s'`: BLAKE2s hashing algorithm.
    `'SHAKE_128'`: SHAKE_128 hashing algorithm.
    `'SHAKE_256'`: SHAKE_256 hashing algorithm.


    `return_hex`: A boolean indicating whether the output should be in hexadecimal or not.

    `return_length`: An optional parameter specifying the amount of bytes to return. Used only in shake algorithms.

    Returns: a hash of the specific algorithm and data representation.
    """
    if ToHash is not bytes and isinstance(ToHash, str):
        ToHash = bytes(ToHash, 'utf-8')
    hash_code = hash_code.upper()
    if hash_code == "SHA224":
        hash_obj = hash.sha224(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA256":
        hash_obj = hash.sha256(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA512":
        hash_obj = hash.sha512(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "MD5":
        hash_obj = hash.md5(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA384":
        hash_obj = hash.sha384(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA1":
        hash_obj = hash.sha1(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "BLAKE2B":
        hash_obj = hash.blake2b(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "BLAKE2S":
        hash_obj = hash.blake2s(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA3_224":
        hash_obj = hash.sha3_224(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA3_256":
        hash_obj = hash.sha3_256(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA3_384":
        hash_obj = hash.sha3_384(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHA3_512":
        hash_obj = hash.sha3_512(ToHash)
        if return_hex is False:
            return hash_obj.digest()
        else:
            return hash_obj.hexdigest()
    elif hash_code == "SHAKE_128":
        hash_obj = hash.shake_128(ToHash)
        if return_hex is False:
            return hash_obj.digest(return_length)
        else:
            return hash_obj.hexdigest(return_length)
    elif hash_code == "SHAKE_256":
        hash_obj = hash.shake_256(ToHash)
        if return_hex is False:
            return hash_obj.digest(return_length)
        else:
            return hash_obj.hexdigest(return_length)
    else:
        raise ValueError("Unknown hash algorithm.")


def random_choice(given_list:list): # tested
    """
    A function to randomly choose an item from a given list.

    Parameters:
    `given_list`: The list to choose from.

    Returns: the chosen item in the list.
    """
    chosen = secrets.choice(given_list)
    return chosen


def compare_hashes(hash_1=str, hash_2=str) -> bool: # tested
    """
    hash comparision function. 

    Takes 2 strings and compares them to see if they are the same.
    returns a boolean value in such a way to reduce timing attack efficacy.

    Parameters:
    `hash_1`: The string to compare the second hash to.
    `hash_2`: The string to be compared.
    """
    result = secrets.compare_digest(hash_1, hash_2)
    return result


def token_generate(size:int, return_type="HEX"): # tested
    """
    Simplifed method for interfacing with the secrets module.

    Parameters:
    `return_type`: What is being returned. modes are `'URL'`, `'HEX'`, and `'BYTES'`.
    
    `size`: the number of bytes in the token to be generated.

    returns: a token of the specific type, or 1 to indicate that the return type was not valid.
    """
    if return_type.upper() == "HEX":
        token = secrets.token_hex(size)
        return token
    if return_type.upper() == "BYTES":
        token = secrets.token_bytes(size)
        return token
    if return_type.upper() == "URL":
        token = secrets.token_urlsafe(size)
        return token
    else:
        return 1


def generate_password(length:int) -> str: # tested
    """
    Generates and returns a random password of n `length`.
    """
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    shuffle(characters)
    password = []
    for i in range(length):
        password.append(secrets.choice(characters))
    shuffle(password)
    final_password = "".join(password)
    # deleting uneeded variables
    del characters
    return final_password


def sec_delete(file_path:str, random_fill = True, null_fill = True, passes = 35) -> int: # tested
    """
    Secure file deletion function with overwriting and null filling.

    It is best practice to combine this with another secure file deletion protocol.
    return codes:
    1: Attempting to access root folder or hidden file.
    2: Attempt to pass a dangerous command to command line.
    0: File successfully deleted.
    """
    file_path = os.path.abspath(file_path)
    if "/home/" not in file_path or "/." in file_path:
        return 1
    elif "sudo rm -rf /" in file_path:
        return 2
    # testing if platform is Linux
    if get_platform() != "Linux":
        return 3
    else:
        with open (file_path, "rb") as file:
            data = file.read()
        length = len(data)
        if random_fill is True:
            for _ in range(passes):
                with open(file_path, "wb") as file:
                    file.write(os.urandom(length))
        if null_fill is True:
            for _ in range(passes):
                with open (file_path, "wb") as file:
                    file.write(b"\x00" * length)
        os.system("rm {}".format(file_path))
        # deleting uneeded variables
        del data, length, file_path, random_fill, null_fill, passes
        return 0


def delete(path:str) -> int: # tested
    """
    File deletion function.

    Parameters:
    `path`: The path to the file, in string format.

    Returns: An integer value indicating if the function successfully executed.
    """
    path = os.path.abspath(path)
    if '/home/' not in path or "/." in path:
        return 1
    elif "sudo rm -rf /" in path:
        return 2
    # checking if the platform is Linux
    elif get_platform() == "Linux":
        os.system("rm {}".format(path))
        return 0
    else:
        return 3


def XOR(bytes1:bytes, bytes2:bytes, write_to=None):
    """
    A function for preforming XOR operations on bytestrings.
    Returns: None if `write_to` is `None`, otherwise returns the XOR'ed string.
    """
    bytes_string = strxor(bytes1, bytes2, output = write_to)
    return bytes_string


def is_prime_number(number:int) -> bool:
    """
    A function for testing if a number is prime. Returns a boolean value.
    """
    number_is_prime = isPrime(number)
    return number_is_prime


def get_prime_number(length_in_bits:int) -> int:
    """
    A function for generating a prime number of bit length `length_in_bits`.
    """
    prime_number = getPrime(length_in_bits)
    return prime_number


def get_GCD(number1:int, number2:int) -> int:
    """
    A function to find the greatest common denominator between `number1` and `number2`.
    Returns the greatest common denominator.
    """
    greatest_CD = GCD(number1, number2)
    return greatest_CD


def englishToKey(words:str) -> bytes:
    """
    A function for generating a key using english words.

    Parameters:
    `words`: The words to be used in generating the key, seperated by whitespace. The length must be a multiple of 6.
    """
    split_words = words.split(" ")
    amount_of_words = len(split_words)
    if amount_of_words % 6 != 0:
        raise InvalidKeyArgument("Given amount of words are not a multiple of 6.")
    key = english_to_key(s=words)
    # deleting uneeded variables
    del amount_of_words, split_words
    return key


def keyToEnglish(key:bytes):
    """
    A function for  converting a bytestring to a string of english words.

    Parameters:
    'key': The bytestring to convert to english words. Its length must be a multiple of 8.
    """
    length_of_key = len(key)
    if length_of_key % 8 != 0:
        raise InvalidKeyArgument("Key length is not a multiple of 8.")
    words = key_to_english(key=key)
    return words


def collect():
    gc.collect()
    return 0
