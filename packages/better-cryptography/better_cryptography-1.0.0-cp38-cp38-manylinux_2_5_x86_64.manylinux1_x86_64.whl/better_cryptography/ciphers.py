"Python script containing functions and classes for general cryptographic use.\nDeveloped on linux, but should work on windows."

# importing libraries
from curses import keyname
import os # various file operations and directory walking.
import rsa # used in Ciphers class for RSA
from Crypto.Cipher import AES # used for string encryption/decryption
from Crypto.Cipher import Blowfish # used for string encryption/decryption
from Crypto.Protocol.KDF import PBKDF2 # used for generating secure keys
from cryptography.fernet import Fernet # used in Ciphers class for string/file encryption/decryption
from platform import system as get_platform # used to find OS
from Crypto.Cipher import Salsa20, ChaCha20, ChaCha20_Poly1305, DES, DES3, ARC2, ARC4, CAST # various ciphers for Cipher_Constructor method
from .file_encryption import AES_encrypt_file, AES_decrypt_file, BLO_encrypt_file, BLO_decrypt_file, BLO_encrypt_str, BLO_decrypt_str, one_time_pad_file_encrypt, one_time_pad_file_decrypt, AES_encrypt_string, AES_decrypt_string, Blowfish_encrypt_string, Blowfish_decrypt_string, FerNet_encrypt_file, FerNet_decrypt_file, FerNet_encrypt_string, FerNet_decrypt_string, true_one_time_pad_encrypt, true_one_time_pad_decrypt # cython functions


class NoKeyError(Exception):
    """
    Raised when no key was provided to a cipher object.
    """
    pass


class InvalidCipherArgument(Exception):
    """
    Raised when a parameter for a cipher is not provided.
    """
    pass


class UnknownError(Exception):
    """
    Raised when a an unknown error occurrs during encryption/decryption.
    """
    pass


class Ciphers: # tested
    """
    A class for ciphering/deciphering operations.

    Developed in Linux, but should work with the windows filesystem as well.

    Parameters:
        Password: The password of the user.
    """


    def __init__(self, password=str) -> None:
        self.password = password
        self.marker  = b"E1m%nj2i$bhilj"


    # misc methods


    def generate_symmetric_key(self, salt=None): # tested
        "Method for generating keys. Will return tuple (key, salt) if salt is not provided."
        if salt is None:
            salt_ = os.urandom(32)
            key = PBKDF2(self.password, salt_, dkLen=32)
            return key, salt_
        else:
            key = PBKDF2(self.password, salt, dkLen=32)
            return key


    def generate_FerNet_key(self): # tested
        """
        A method for generating a FerNet key. Takes no arguements and returns a key in bytes format.
        """
        key = Fernet.generate_key()
        return key


    def check_path_validity(self, path=str, decrypting=bool, type_=str) -> int: # tested
        """
        A guard clause for file operations.

        Return codes:
            0: File path is suitable.
            1: File path is invalid.
        """
        try:
            assert path is not None
            assert "/." not in path
            assert get_platform() == "linux" and "/home/" in path
            assert os.path.isfile(path) is True or os.path.isdir(path) is True
            try:
                with open (path, "rb") as file:
                    file_type = file.read(3)
                    file_marker = file.read(len(self.marker))
            except PermissionError:
                return 1
            except FileNotFoundError:
                return 1
            except IsADirectoryError:
                return 0
            assert file_type == type_
            if decrypting:
                assert file_marker == self.marker
            else:
                assert file_marker != self.marker
        except AssertionError:
            return 1
        return 0
    

    def change_encrypting_password(self, old_password:str, new_password:str):  # tested
        """
        A method for changing the classes' `password` attribute.

        Parameters:
        `old_password`: The original password of the cipher; required for verification
        `new_password`: The password to replace the old one.

        Returns: 1, if the `old_password` parameter does not match the class `password` attribute.
        
        Returns 0 if the password change was successful.
        """
        if self.password == old_password:
            self.password = new_password
            return 0
        else:
            return 1


    def change_file_marker(self, new_file_marker:bytes):
        """
        Method for changing the file marker used to identify encrypted files.

        ## THIS MAY PREVENT DECRYPTION OF FILES THAT WERE ENCRYPTED WITH ANOTHER FILE MARKER.
        """
        self.marker = new_file_marker
        return 0



    # RSA methods 


    def generate_RSA_keys(self): # tested
        "method to generate a public/private key pair for RSA encryption."
        public_key, private_key = rsa.newkeys(4096)
        return (public_key, private_key)


    def RSA_encrypt_str(self, public_key, str_=str): # tested
        "method to encrypt a string with a RSA public key."
        encrypted_string = rsa.encrypt(str_.encode(), public_key)
        return encrypted_string


    def RSA_decrypt_str(self, private_key, encrypted_str:bytes): # tested
        "Method to decrypt a string with a RSA private key."
        decrypted_string = rsa.decrypt(encrypted_str, private_key).decode()
        return decrypted_string


    # AES methods


    def encrypt_file_AES(self, path:str) -> int: # tested
        """
        A method for encrypting a file/folder object with AES.

        Parameters:
            `path`: The path of the file/folder to be encrypted.

        Return codes:
            0: File encryption successful.
            1: Path is invalid.
        """
        # checking if the file path is ok
        return_code = self.check_path_validity(path, decrypting=False, type_="AES")
        if return_code != 0:
            return return_code
        try:
            AES_encrypt_file(self.password, path, self.marker)
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0


    def decrypt_file_AES(self, path:str) -> int:  # tested
        """
        A method for decrypting an encrypted file that was encrypted with AES.

        Takes only a file path as an argument.

        return codes:
            0: File decrypt successful.
            1: Path is invalid.
        """
        # checking if file is suitable
        return_code = self.check_path_validity(path, decrypting=True, type_="AES")
        if return_code != 0:
            return return_code
        # passing path onto compiled Cython code
        try:
            AES_decrypt_file(self.password, path, len(self.marker))
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0


    def encrypt_string_AES(self, string_to_encrypt:bytes, key=None):  # tested
        """
        Method for encrypting strings using the AES encryption alogrithm in CFB mode.

        Parameters:
            `string_to_encrypt`: the string being encrypted, in bytes
            `key`: the key to encrypt the string with. If not provided, will generate a new key using the `Ciphers` class `password` attribute.
        returns a tuple of `(ciphered_string, iv, key)` if key is not provided; otherwise returns a tuple of `(ciphered_string, iv)`.
        """
        if key is None:
            salt = os.urandom(32)
            key = self.generate_symmetric_key(salt)
            key_was_none = True
        else:
            key_was_none = False
        try:
            assert isinstance(string_to_encrypt, bytes)
        except AssertionError:
            string_to_encrypt = string_to_encrypt.encode()
        encrypted_string, iv = AES_encrypt_string(key, string_to_encrypt)
        if key_was_none:
            return encrypted_string, iv, key
        else:
            return encrypted_string, iv


    def decrypt_string_AES(self, encrypted_string:bytes, key:bytes, iv:bytes):  # tested
        """
        Method for decrypting strings using the AES encryption alogrithm in CFB mode.

        Parameters:
            `encrypted_string`: The string to be decrypted, in bytes.
            `key`: The key used to encrypt the string.
            `iv`: The Intialization vector used for encryption.
        returns the decrypted string in bytes format.
        """
        try:
            assert key is not None and iv is not None
        except AssertionError:
            raise InvalidCipherArgument("Key and IV must be provided.")
        decrypted_string = AES_decrypt_string(key, encrypted_string, iv)
        return decrypted_string


    # Blowfish methods


    def encrypt_file_blowfish(self, path:str):  # tested
        """
        A method for encrypting a file/folder object with Blowfish in CFB mode.

        Parameters:
            `path`: The path of the file/folder to be encrypted.

        Return codes:
            0: File encrypt successful.
            1: Path is invalid.
        """
        # checking if file is suitable
        return_code = self.check_path_validity(path, decrypting=False, type_="BLO")
        if return_code != 0:
            return return_code
        # passing onto cython code
        try:
            BLO_encrypt_file(self.password, path, self.marker)
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0


    def decrypt_file_blowfish(self, path=str):  # tested
        """
        A method for decrypting an encrypted file or folder that was encrypted using Blowfish.

        Parameters:
            `path`: The path of the file as a string.

        return codes:
            0: File decrypt successful.
            1: Path is invalid
        """
        # checking if file is suitable
        return_code = self.check_path_validity(path, decrypting=True, type_="BLO")
        if return_code != 0:
            return return_code
        # passing onto cython code
        try:
            BLO_decrypt_file(self.password, path, len(self.marker))
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0


    def encrypt_string_blowfish(self, string_to_encrypt:bytes, key=None):  # tested
        """
        Method for encrypting strings using the Blowfish encryption alogrithm in CFB mode.

        Parameters:
            `string_to_encrypt`: the string being encrypted, in bytes
            `key`: the key to encrypt the string with. If not provided, will generate a new key using the `Ciphers` class `password` attribute.
        returns a tuple of `(ciphered_string, iv, key)`
        """
        if key is None:
            salt = os.urandom(32)
            key = self.generate_symmetric_key(salt)
            key_was_none = True
        else:
            key_was_none = False
        try:
            assert isinstance(string_to_encrypt, bytes)
        except AssertionError:
            string_to_encrypt = string_to_encrypt.encode()
        encrypted_string, iv = Blowfish_encrypt_string(key, string_to_encrypt)
        if key_was_none:
            return encrypted_string, iv, key
        else:
            return encrypted_string, iv


    def decrypt_string_blowfish(self, encrypted_string:bytes, key:bytes, iv:bytes):  # tested
        """
        Method for decrypting strings using the Blowfish encryption alogrithm in CFB mode.

        Parameters:
            `encrypted_string`: The string to be decrypted, in bytes.
            `key`: The key used to encrypt the string.
            `iv`: The Intialization vector used for encryption.
        returns the decrypted string in bytes format.
        """
        try:
            assert key is not None and iv is not None
        except AssertionError:
            raise InvalidCipherArgument("Key and IV must be provided.")
        decrypted_string = Blowfish_decrypt_string(key, encrypted_string, iv)
        return decrypted_string


    # FerNet methods


    def encrypt_file_fernet(self, path:str, key:bytes):  # tested
        """
        A method for encrypting a file or folder using Fernet.

        parameters:

            path: The path to the file in string format.

            key: The key to be used for encryption.

        returns:
            0: File encrypt successful.
            1: Path is invalid.
        """
        return_code = self.check_path_validity(path, decrypting=False, type_="FER")
        if return_code != 0:
            return return_code
        # passing onto cython code
        try:
            assert isinstance(key, bytes)
        except AssertionError:
            raise InvalidCipherArgument("Key must be provided in bytes format.")
        try:
            FerNet_encrypt_file(path, key, self.marker)
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0
    

    def decrypt_file_fernet(self, path:str, key:bytes):  # tested
        """
        A method for decrypting an encrypted file or folder that was encrypted using FerNet.

        Parameters:
            `path`: The path of the file as a string.

            `key`: The key to encrypt the file with. Will raise a `NoKeyError` if not provided.

        return codes:
            0: File decrypt successful.
            1: Path is Invalid.
        """
        return_code = self.check_path_validity(path, decrypting=True, type_="FER")
        if return_code != 0:
            return return_code
        # passing onto cython code
        try:
            assert isinstance(key, bytes)
        except AssertionError:
            raise InvalidCipherArgument("Key must be provided in bytes format.")
        try:
            FerNet_decrypt_file(path, key, len(self.marker))
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0
    

    def encrypt_string_fernet(self, bstring:bytes, key=None):  # tested
        """
        Method for encrypting a string with the `cryptography` module's `Fernet` class.

        will return a tuple of `(encrypted_text, key)` if key is not provided.
        
         will return `encrypted_text` as a `bytes` object if the key is provided.
        """
        if key is None:
            key = self.generate_FerNet_key()
            key_was_none = True
        else:
            key_was_none = False
        try:
            assert isinstance(bstring, bytes)
        except AssertionError:
            bstring = bstring.encode()
        encrypted_string = FerNet_encrypt_string(key, bstring)
        if key_was_none:
            return encrypted_string, key
        else:
            return encrypted_string


    def decrypt_string_fernet(self, encrypted_string:bytes, key:bytes):  # tested
        """
        Method for decrypting a string with the `cryptography` module's `Fernet` class.

        Will raise a `NoKeyError` if a key for the cipher was not provided.

        Will return the decrypted text as a `bytes` object.
        """
        try:
            assert key is not None
        except AssertionError:
            raise NoKeyError("No key was provided for decryption.")
        decrypted_string = FerNet_decrypt_string(key, encrypted_string)
        return decrypted_string


    # One time pad methods


    def encrypt_file_one_time_pad(self, path:str, key_phrase:str, salt:bytes):  # tested
        """
        A method for encrypting a file or folder using a one time pad, with a key derived from a password and a salt.
        """
        return_code = self.check_path_validity(path, decrypting=False, type_="OTP")
        if return_code != 0:
            return return_code
        # passing onto cython code
        try:
            assert isinstance(key_phrase, str)
            assert isinstance(salt, bytes)
        except AssertionError:
            raise InvalidCipherArgument("Key phrase and salt must be provided.")
        try:
            one_time_pad_file_encrypt(path, key_phrase, salt, self.marker)
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0
    

    def decrypt_file_one_time_pad(self, path:str, key_phrase:str, salt:bytes):  # tested
        """
        A method for decrypting a file or folder that was encrypted using a one time pad, with a key derived from a password and a salt.
        """
        return_code = self.check_path_validity(path, decrypting=True, type_="OTP")
        if return_code != 0:
            return return_code
        # passing onto cython code
        try:
            assert isinstance(key_phrase, str)
            assert isinstance(salt, bytes)
        except AssertionError:
            raise InvalidCipherArgument("Key phrase and salt must be provided.")
        try:
            one_time_pad_file_decrypt(path, key_phrase, salt, self.marker)
        except Exception as error:
            raise UnknownError("Unknown error occurred: {}".format(error))
        return 0


    def true_OTP_encrypt_string(self, bstring:bytes):
        """
        A method for encrypting a string with a true one time pad.
        """
        # getting key
        # passing onto cython code
        try:
            assert isinstance(bstring, bytes)
        except AssertionError:
            bstring = bstring.encode()
        encrypted_string, key = true_one_time_pad_encrypt(bstring)
        return encrypted_string, key

    
    def true_OTP_decrypt_string(self, encrypted_string:bytes, key:bytes):
        """
        A method for decrypting a string with a true one time pad.
        """
        # passing onto cython code
        try:
            assert isinstance(encrypted_string, bytes)
            assert isinstance(key, bytes)
        except AssertionError:
            raise InvalidCipherArgument("Encrypted string and key must be provided in bytes.")
        decrypted_string = true_one_time_pad_decrypt(key, encrypted_string)
        return decrypted_string


class Cipher_Constructor:
    """
    A class for simplifying cipher object generation.
    """


    def __init__(self) -> None:
        pass


    def intialize_AES_cipher(mode:str, key:bytes, iv=None, nonce=None) -> object:
        """
        method for simplifed generation of AES ciphers.
        Mode: The 3 letter mode for the cipher.
        Modes are:
            CFB

            CBC
            
            CTR
            
            ECB
            
            OFB
            
            OPENPGP
            
            CCM
            
            EAX
            
            GCM
            
            OCB

        key: The key to be used in the cipher.

        IV/Nonce: the nonce or IV to be used in the cipher, depending on the mode.
        """
        # this template will be used for all the modes
        if mode == "CFB":
            # guard clauses
            if iv is None:
                raise InvalidCipherArgument("Intialization vector was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            # generating cipher and returning
            cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
            return cipher
        elif mode == "CBC":
            if iv is None:
                raise InvalidCipherArgument("Intialization vector was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
            return cipher
        elif mode == "CTR":
            if nonce is None:
                raise InvalidCipherArgument("Nonce was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_CTR, nonce=nonce)
            return cipher
        elif mode == "ECB":
            if key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_ECB)
            return cipher
        elif mode == "OFB":
            if iv is None:
                raise InvalidCipherArgument("Intialization vector was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_OFB, iv=iv)
            return cipher
        elif mode == "OPENPGP":
            if iv is None:
                raise InvalidCipherArgument("Intialization vector was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_OPENPGP, iv=iv)
            return cipher
        elif mode == "CCM":
            if nonce is None:
                raise InvalidCipherArgument("Nonce was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_CCM, nonce=nonce)
            return cipher
        elif mode == "EAX":
            if nonce is None:
                raise InvalidCipherArgument("Nonce was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce)
            return cipher
        elif mode == "GCM":
            if nonce is None:
                raise InvalidCipherArgument("Nonce was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_GCM, nonce=nonce)
            return cipher
        elif mode == "OCB":
            if nonce is None:
                raise InvalidCipherArgument("Nonce was not provided.")
            elif key is None:
                raise NoKeyError("Key was not provided.")
            cipher = AES.new(key=key, mode=AES.MODE_OCB, nonce=nonce)
            return cipher


    def intialize_Blowfish_cipher(mode:str, key:bytes, iv=None, nonce=None) -> object:
        """
        A simplifed method for generating Blowfish cipher objects.

        Parameters:

        `Mode`: The string indicating which mode to set the cipher in.

            Modes are:

            `ECB` - 

            `CBC` - 

            `CFB`

            `OFB` - 

            `CTR` - 

            `OPENPGP` - 

            `EAX` - 
        
        `key`: the key to use in the cipher.

        `iv`/`nonce`: The Intialization vector or nonce to be used in the cipher (dependent on the mode)

        """
        # all things with "O" or o in them
        if "O" in mode or "o" in mode:
            # checking if mode is OPENPGP
            if "OPEN" in mode or "open" in mode:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_OPENPGP, iv=iv)
                return cipher
            else:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_OFB, iv=iv)
                return cipher
        elif "E" in mode:
            if "X" in mode:
                if nonce is None:
                    raise InvalidCipherArgument("nonce not provided.")
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_EAX, nonce=nonce)
                return cipher
            else:
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_ECB)
                return cipher
        elif "B" in mode:
            if "BC" in mode:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_CBC, iv=iv)
                return cipher
            elif "T" in mode:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided.")
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_CTR, nonce=nonce)
                return cipher
            else:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = Blowfish.new(key=key, mode=Blowfish.MODE_CFB, iv=iv)

    
    def Intialize_Salsa20(key:bytes, nonce:bytes) -> object:
        """
        A method for generating a `Salsa20` cipher object.

        Parameters:
        
        `key`: The byte key to be used in creating the cipher object.

        `nonce`: The nonce to be used in creating the cipher. Must be either 16 or 32 bytes in length.

        Returns: a `Salsa20` cipher object.
        """
        if len(nonce) != 16 and len(nonce) != 32:
            raise InvalidCipherArgument("Nonce length was not 16 or 32 bytes.")
        cipher = Salsa20.new(key=key, nonce=nonce)
        return cipher
    

    def intialize_ChaCha20(key:bytes, nonce:bytes) -> object:
        """
        A method for generating a `ChaCha20` cipher object.

        Parameters:
        
        `key`: The byte key to be used in creating the cipher object.

        `nonce`: The nonce to be used in creating the cipher. Must be either 8 or 12 bytes in length.

        Returns: a `ChaCha20` cipher object.
        """
        if len(nonce) != 8 and len(nonce) != 12:
            raise InvalidCipherArgument("Nonce length was not 8 or 12 bytes.")
        cipher = ChaCha20.new(key=key, nonce=nonce)
        return cipher


    def intialize_ChaCha20P1305(key:bytes, nonce:bytes) -> object:
        """
        A method for generating a `ChaCha20_Poly1305` cipher object.

        Parameters:
        
        `key`: The byte key to be used in creating the cipher object.

        `nonce`: The nonce to be used in creating the cipher. Must be either 8 or 12 bytes in length.

        Returns: a `ChaCha20` cipher object.
        """
        if len(nonce) != 8 and len(nonce) != 12:
            raise InvalidCipherArgument("Nonce length was not 8 or 12 bytes.")
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        return cipher
        pass


    def intialize_DES(mode:str, key:bytes, iv=None, nonce=None) -> object:
        """
        A method for generating a `DES` cipher object.

        Parameters:
        `mode`: an uppercase string indicating which mode the cipher should be set to.

        Valid modes are:
            `ECB`

            `CBC` - 
            
            `CFB` -
            
            `OFB` - 
            
            `CTR` - 
            
            `OPENPGP` - 
            
            `EAX`
        

        `key`: The key to set the cipher with.

        `iv`/`nonce`: The intialization vector or nonce to set the cipher with. Dependent on the `mode` used.
        Will raise an `InvalidCipherArgument` error if the required parameter is not provided.
        """
        mode_ = mode.upper()
        if "O" in mode_:
            if "OPEN" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = DES.new(key=key, mode=DES.MODE_OPENPGP, iv=iv)
                return cipher
            else:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = DES.new(key=key, mode=DES.MODE_OFB, iv=iv)
                return cipher
        elif "C" in mode_:
            if "CBC" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = DES.new(key=key, mode=DES.MODE_CBC, iv=iv)
                return cipher
            elif "R" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided.")
                cipher = DES.new(key=key, mode=DES.MODE_CTR, nonce=nonce)
                return cipher
        else:
            if "X" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided")
                cipher = DES.new(key=key, mode=DES.MODE_EAX, nonce=nonce)
                return cipher
            elif "EC" in mode_:
                cipher = DES.new(key=key, mode=DES.MODE_ECB)
                return cipher
            else:
                raise InvalidCipherArgument("Unsupported mode given.")


    def intalize_DES3(mode:str, key:bytes, iv=None, nonce=None) -> object:
        """
        A method for generating a `DES3` cipher object.

        Parameters:
        `mode`: an uppercase string indicating which mode the cipher should be set to.

        Valid modes are:
            `ECB`

            `CBC`
            
            `CFB`
            
            `OFB`
            
            `CTR`
            
            `OPENPGP`
            
            `EAX`
        

        `key`: The key to set the cipher with.

        `iv`/`nonce`: The intialization vector or nonce to set the cipher with. Dependent on the `mode` used.
        Will raise an `InvalidCipherArgument` error if the required parameter is not provided.
        """
        mode_ = mode.upper()
        if "O" in mode_:
            if "OPEN" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = DES3.new(key=key, mode=DES3.MODE_OPENPGP, iv=iv)
                return cipher
            else:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = DES3.new(key=key, mode=DES3.MODE_OFB, iv=iv)
                return cipher
        elif "C" in mode_:
            if "CBC" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = DES3.new(key=key, mode=DES3.MODE_CBC, iv=iv)
                return cipher
            elif "R" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided.")
                cipher = DES3.new(key=key, mode=DES3.MODE_CTR, nonce=nonce)
                return cipher
        else:
            if "X" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided")
                cipher = DES3.new(key=key, mode=DES3.MODE_EAX, nonce=nonce)
                return cipher
            elif "EC" in mode_:
                cipher = DES3.new(key=key, mode=DES3.MODE_ECB)
                return cipher
            else:
                raise InvalidCipherArgument("Unsupported mode given.")


    def intialize_ARC2(mode:str, key:bytes, iv=None, nonce=None) -> object:
        """
        A method for generating an `ARC2` cipher object.

        Parameters:
        `mode`: an uppercase string indicating which mode the cipher should be set to.

        Valid modes are:
            `ECB`

            `CBC`
            
            `CFB`
            
            `OFB`
            
            `CTR`
            
            `OPENPGP`
            
            `EAX`
        

        `key`: The key to set the cipher with.

        `iv`/`nonce`: The intialization vector or nonce to set the cipher with. Dependent on the `mode` used.
        Will raise an `InvalidCipherArgument` error if the required parameter is not provided.
        """
        mode_ = mode.upper()
        if "O" in mode_:
            if "OPEN" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = ARC2.new(key=key, mode=ARC2.MODE_OPENPGP, iv=iv)
                return cipher
            else:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = ARC2.new(key=key, mode=ARC2.MODE_OFB, iv=iv)
                return cipher
        elif "C" in mode_:
            if "CBC" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = ARC2.new(key=key, mode=ARC2.MODE_CBC, iv=iv)
                return cipher
            elif "R" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided.")
                cipher = ARC2.new(key=key, mode=ARC2.MODE_CTR, nonce=nonce)
                return cipher
        else:
            if "X" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided")
                cipher = ARC2.new(key=key, mode=ARC2.MODE_EAX, nonce=nonce)
                return cipher
            elif "EC" in mode_:
                cipher = ARC2.new(key=key, mode=ARC2.MODE_ECB)
                return cipher
            else:
                raise InvalidCipherArgument("Unsupported mode given.")


    def intalize_ARC4(key:bytes, drop=0) -> object:
        """
        A method for generating an `ARC4` cipher OBJECT.

        Parameters:

        `key`: the key to use in the cipher; must be between 5 and 256 bytes.

        `drop`: The amount of bytes to drop from the intial keystream.

        returns: an `ARC4` cipher object.
        """
        cipher = ARC4.new(key=key, drop=drop)
        return cipher


    def intialize_CAST(mode:str, key:str, iv=None, nonce=None):
        """
        A method for generating a `CAST` cipher object.

        Parameters:
        `mode`: an uppercase string indicating which mode the cipher should be set to.

        Valid modes are:
            `ECB`

            `CBC`
            
            `CFB`
            
            `OFB`
            
            `CTR` 
            
            `OPENPGP` 
            
            `EAX`
        

        `key`: The key to set the cipher with.

        `iv`/`nonce`: The intialization vector or nonce to set the cipher with. Dependent on the `mode` used.
        Will raise an `InvalidCipherArgument` error if the required parameter is not provided.
        """
        mode_ = mode.upper()
        if "O" in mode_:
            if "OPEN" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = CAST.new(key=key, mode=CAST.MODE_OPENPGP, iv=iv)
                return cipher
            else:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = CAST.new(key=key, mode=CAST.MODE_OFB, iv=iv)
                return cipher
        elif "C" in mode_:
            if "CBC" in mode_:
                if iv is None:
                    raise InvalidCipherArgument("Intialization vector not provided.")
                cipher = CAST.new(key=key, mode=CAST.MODE_CBC, iv=iv)
                return cipher
            elif "R" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided.")
                cipher = CAST.new(key=key, mode=CAST.MODE_CTR, nonce=nonce)
                return cipher
        else:
            if "X" in mode_:
                if nonce is None:
                    raise InvalidCipherArgument("Nonce not provided")
                cipher = CAST.new(key=key, mode=CAST.MODE_EAX, nonce=nonce)
                return cipher
            elif "EC" in mode_:
                cipher = CAST.new(key=key, mode=CAST.MODE_ECB)
                return cipher
            else:
                raise InvalidCipherArgument("Unsupported mode given.")


    def intialize_FerNet_cipher(key:bytes) -> object:
        """
        Returns a `Fernet` cipher object given the key.
        """
        if key is None:
            raise NoKeyError("Key was not provided.")
        fernet_cipher = Fernet(key=key)
        return fernet_cipher
