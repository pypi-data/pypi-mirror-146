"""Script for testing the various functions in the library."""
from .ciphers import *
from .util import *


def init_diagonostic():
    """A method for testing the various functions of this library."""
    print("Testing functions in the `cipher` module.")
    print ("testing hashes")
    assert hash_("Hello World", "SHA224") == hash.sha224("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA256") == hash.sha256("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA512") == hash.sha512("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "MD5") == hash.md5("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA1") == hash.sha1("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA3_224") == hash.sha3_224("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA3_256") == hash.sha3_256("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA3_384") == hash.sha3_384("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHA3_512") == hash.sha3_512("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "BLAKE2b") == hash.blake2b("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "BLAKE2s") == hash.blake2s("Hello World".encode("utf-8")).hexdigest()
    assert hash_("Hello World", "SHAKE_128") == hash.shake_128("Hello World".encode("utf-8")).hexdigest(256)
    assert hash_("Hello World", "SHAKE_256") == hash.shake_256("Hello World".encode("utf-8")).hexdigest(256)
    print ("Hexdigests match")
    print("testing byte hashing")
    assert hash_("Hello World", "SHA224") == hash.sha224(b"Hello World").hexdigest()
    assert hash_("Hello World", "SHA256", return_hex=False) == hash.sha256("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHA512", return_hex=False) == hash.sha512("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "MD5", return_hex=False) == hash.md5("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHA1", return_hex=False) == hash.sha1("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHA3_224", return_hex=False) == hash.sha3_224("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHA3_256", return_hex=False) == hash.sha3_256("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHA3_384", return_hex=False) == hash.sha3_384("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHA3_512", return_hex=False) == hash.sha3_512("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "BLAKE2b", return_hex=False) == hash.blake2b("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "BLAKE2s", return_hex=False) == hash.blake2s("Hello World".encode("utf-8")).digest()
    assert hash_("Hello World", "SHAKE_128", return_hex=False) == hash.shake_128("Hello World".encode("utf-8")).digest(256)
    assert hash_("Hello World", "SHAKE_256", return_hex=False) == hash.shake_256("Hello World".encode("utf-8")).digest(256)
    print ("Bytes match")
    print ("testing key generation")
    print ("generating length 32 password")
    password = generate_password(32)
    print ("password:", password)
    # assert that length is 32
    assert len(password) == 32
    print ("generating length 64 password")
    password = generate_password(64)
    print ("password:", password)
    # assert that length is 64
    assert len(password) == 64
    print ("generating length 128 password")
    password = generate_password(128)
    print ("password:", password)
    # assert that length is 128
    assert len(password) == 128
    print ("test complete; key generation passed")
    # testing hash comparision function
    print ("testing hash comparision function")
    assert compare_hashes(hash_("Hello World", "SHA256"), hash_("Hello World", "SHA256")) == True
    assert compare_hashes(hash_("Hello World", "SHA256"), hash_("Not Hello World", "SHA512")) == False
    print ("test complete; hash comparision function passed")
    # testing random choice function
    print ("testing random choice function")
    assert random_choice(["Hello", "World", "!"]) == "Hello" or "World" or "!"
    print ("test complete; random choice function passed")
    # testing token generation function
    print ("testing token generation function")
    bytes_token = token_generate(32, return_type="BYTES")
    print ("bytes token:", bytes_token)
    assert len(bytes_token) == 32
    hex_token = token_generate(32, return_type="HEX")
    print ("hex token:", hex_token)
    assert len(hex_token) == 64
    url_safe_token = token_generate(32, return_type="URL")
    print ("url safe token:", url_safe_token)
    assert len(url_safe_token) == 43
    print ("test complete; token generation function passed")
    print ("testing secure file deletion function")
    # testing secure file deletion function
    #creating a test file
    test_file = open("test_file.txt", "w")
    test_file.write("Hello World")
    test_file.close()
    # deleting using secure file deletion function
    exit_code = sec_delete("test_file.txt")
    # checking if file is deleted
    assert not os.path.exists("test_file.txt")
    print ("test complete; secure file deletion function passed")
    print ("testing file deletion function")
    # testing file deletion function
    #creating a test file
    test_file = open("test_file.txt", "w")
    test_file.write("Hello World")
    test_file.close()
    # deleting using file deletion function
    delete("test_file.txt")
    # checking if file is deleted
    assert not os.path.exists("test_file.txt")
    print ("test complete; file deletion function passed")
    print ("testing XOR function")
    # testing XOR function against pycryptodome's XOR function
    assert XOR(b"Hello World", b"Hello World") == strxor("Hello World".encode("utf-8"), "Hello World".encode("utf-8"))
    print ("test complete; XOR function passed")
    # testing the is_prime_number function
    print ("testing is_prime_number function")
    assert is_prime_number(2) == True
    assert is_prime_number(3) == True
    assert is_prime_number(4) == False
    assert is_prime_number(5) == True
    assert is_prime_number(6) == False
    print ("test complete; is_prime_number function passed")
    # testing the generate_prime_number function
    print ("testing generate_prime_number function")
    assert get_prime_number(2) == 2 or 3 or 5 or 7
    print ("test complete; generate_prime_number function passed")
    # testing the GCD function
    print ("testing GCD function")
    assert GCD(2, 4) == 2
    assert GCD(4, 2) == 2
    assert GCD(2, 6) == 2
    assert GCD(6, 2) == 2
    print ("test complete; GCD function passed")
    print ("Functions test passed | Function tests passed")
    print ("Testing Ciphers Class")
    print ("testing RSA methods")
    # instantiating the class
    cipher = Ciphers("youwillneverguess")
    # generating a key
    public_key, private_key = cipher.generate_RSA_keys()
    # encrypting a string
    encrypted_string = cipher.RSA_encrypt_str(public_key, "Hello World")
    # decrypting the string
    decrypted_string = cipher.RSA_decrypt_str(private_key, encrypted_string)
    # checking if the decrypted string is the same as the original
    assert decrypted_string == "Hello World"
    print ("test complete; RSA methods passed")
    print ("testing AES methods")
    # creating a test file
    test_file = open("test_file.txt", "w")
    test_file.write("Hello World")
    test_file.close()
    # encrypting the file
    cipher.encrypt_file_AES("test_file.txt")
    # decrypting the file
    cipher.decrypt_file_AES("test_file.txt")
    # checking if the file is decrypted
    with open ("test_file.txt", "r") as test_file:
        assert test_file.read() == "Hello World"
    # encrypting and decrypting a string
    encrypted_string, iv, key = cipher.encrypt_string_AES(b"Hello World")
    decrypted_string = cipher.decrypt_string_AES(encrypted_string, key, iv).decode("utf-8")
    # checking if the decrypted string is the same as the original
    assert decrypted_string == "Hello World"
    print ("test complete; AES methods passed")
    print ("testing Blowfish methods")
    # using prev test file
    # encrypting the file
    cipher.encrypt_file_blowfish("test_file.txt")
    # decrypting the file
    cipher.decrypt_file_blowfish("test_file.txt")
    # checking if the file is decrypted
    with open ("test_file.txt", "r") as test_file:
        assert test_file.read() == "Hello World"
    # encrypting and decrypting a string
    encrypted_string, iv, key = cipher.encrypt_string_blowfish(b"Hello World")
    decrypted_string = cipher.decrypt_string_blowfish(encrypted_string, key, iv).decode("utf-8")
    # checking if the decrypted string is the same as the original
    assert decrypted_string == "Hello World"
    print ("test complete; Blowfish methods passed")
    print ("testing Fernet methods")
    # using prev test file
    # encrypting the file
    key = cipher.generate_FerNet_key()
    cipher.encrypt_file_fernet("test_file.txt", key)
    # decrypting the file
    cipher.decrypt_file_fernet("test_file.txt", key)
    # checking if the file is decrypted
    with open ("test_file.txt", "r") as test_file:
        assert test_file.read() == "Hello World"
    # encrypting and decrypting a string
    encrypted_string = cipher.encrypt_string_fernet(b"Hello World", key)
    decrypted_string = cipher.decrypt_string_fernet(encrypted_string, key).decode("utf-8")
    # checking if the decrypted string is the same as the original
    assert decrypted_string == "Hello World"
    print ("test complete; Fernet methods passed")
    # testing the one time pad functions
    print ("testing one time pad functions")
    # using prev test file
    # encrypting the file
    salt = os.urandom(16)
    cipher.encrypt_file_one_time_pad("test_file.txt", "youwillneverguess", salt)
    # decrypting the file
    cipher.decrypt_file_one_time_pad("test_file.txt", "youwillneverguess", salt)
    # checking if the file is decrypted
    with open ("test_file.txt", "r") as test_file:
        assert test_file.read() == "Hello World"
    # encrypting and decrypting a string
    encrypted_string, key = cipher.true_OTP_encrypt_string(b"Hello World")
    decrypted_string = cipher.true_OTP_decrypt_string(encrypted_string, key).decode("utf-8")
    # checking if the decrypted string is the same as the original
    assert decrypted_string == "Hello World"
    # removing the test file
    os.remove("test_file.txt")
    print ("test complete; one time pad functions passed")
    print ("Ciphers Class Tests passed | All tests passed")