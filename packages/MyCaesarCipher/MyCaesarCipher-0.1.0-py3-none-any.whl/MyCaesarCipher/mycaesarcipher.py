import itertools


class CaesarCipher:
    """Class containing cryptographic encryption/decryption methods using the Caesar-Cipher algorithm.

    - Substitutes each letter of a message with new "matching" letter shifted down alphabetically by a given amount.
    - Not for real-world cryptographic applications, as the Caesar Cipher is notoriously easy to crack.
    - More information on this cipher:
        - https://en.wikipedia.org/wiki/Caesar_cipher
    """

    def __init__(self):
        pass

    def encrypt(self, msg: str, key: int, consoleOutput: bool = True) -> str:
        """Simple Caesar Cypher cryptography tool.

        - Generates encrypted form of `msg: str` using the Caesar Cipher algorithm.

        Parameters:
            :param msg: msg to be encoded.
            :type msg: str
            :param key: key to use when encoding the given message.
            :type key: int
            :param printInfo: whether to print information to the console/stdout, defaults to True
            :type printInfo: bool, optional
            :return: encrypted form of entered msg.
            :rtype: str
        """

        result: str = ''

        #@ Iterate through msg char by char.

        for character in msg:
            #@ Encrypt uppercase characters in msg
            if (character.isupper()):
                result += chr((ord(character) + key - 65) % 26 + 65)
            #@ Encrypt lowercase characters in msg
            elif (character.islower()):
                result += chr((ord(character) + key - 97) % 26 + 97)
            #@ Encrypt numbers in msg
            elif (character.isdigit()):
                result += str((int(character) + key) % 10)
            #@ Leave all non-alphanumeric characters unchanged.
            else:
                result += character
        info: str = f'> Original Msg : {msg}\n> Shift-key : {key}\n> Encrypted Result: {result}\n'

        if consoleOutput:
            print(info)

        return result

    def decrypt(self, msg: str, consoleOutput: bool = True):
        """Simple Caesar Cipher brute-force decryption tool.

        - Decrypt plaintext `msg: str` encoded using the Caesar-Cipher algorithm.

        :param msg: msg to decode.
        :type msg: str
        :param consoleOutput: if true enable printing output to stdout, defaults to True.
        :type consoleOutput: bool
        :return: all possible pairs of shift-keys and their decrypted results.
        :rtype: str
        """

        #@ Outputs all possible shift-keys using the english alphabet.
        for key in range(26):
            translated = ''
            for character in msg:
                if (character.isupper()):
                    translated += chr((ord(character) - key - 65) % 26 + 65)
                #@ Decrypt lowercase characters in msg
                elif (character.islower()):
                    translated += chr((ord(character) - key - 97) % 26 + 97)
                #@ Decrypt numbers in msg
                elif (character.isdigit()):
                    translated += str((int(character) - key) % 10)
                #@ Leave all non-alphanumeric characters unchanged.
                else:
                    translated += character

            if consoleOutput:
                print(f'> Decrypted Shift-Key {key} : {translated}\n')
        return translated