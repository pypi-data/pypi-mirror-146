# MyCaesarCipher

> Simple cryptographic substitution-based cipher for encoding plaintext.

---

## About

- The [Caesar Cipher](https://en.wikipedia.org/wiki/Caesar_cipher) is one of the most simple and well known encryption techniques.

  - Each letter in the plaintext entry is replaced by a letter some fixed number of positions down the alphabet.

- This project was created as an exercise while I was taking the ["Cracking Codes with Python"](https://inventwithpython.com/cracking/) course - which I _highly_ recommend for both beginners and experienced python programmers interested in cryptography!

---

## Installation

### Using pip _(Recommended)_

> _Easiest_ method. _**Highly recommended**_ over manual installation.

- Run the following to install _**`MyCaesarCipher`**_ using `pip`:

```python
pip install MyCaesarCipher
```

- You should now be able to import/run _**`MyCaesarCipher`**_ within your python environment by entering the following:

```python
>>> from MyCaesarCipher import CaesarCipher
...
```

- Done!

---

### Manual Installation

> **_Not recommended._**

1. Before use, navigate to intended installation location, and create a new directory.
2. Install all dependencies for this package within said directory using:

   ```python
   pip install -r requirements.txt
   ```

3. Clone repository with the git client of your preference.
   - (Optional) move installation directory to **`"path/to/Python/Libs/site_packages/"`** to be able to import this package to a Python program like any other importable package.

- Done!

---

## Usage

- Within a Python environment or **`.py`** project, simply import the _**`MyCaesarCipher`**_ module to start encryption/decryption of ciphers.

### Message Encryption

- For encrypting text, use the **`CaesarCipher.encrypt`** class method:

```python
>>> from MyCaesarCipher import CaesarCipher

>>> encoder = CaesarCipher() # Create new class instance.
>>> code = 'Test Cipher'
>>> encoder.encrypt(text=code, key=200, consoleOutput=True)

> Original Msg : Test Cipher
> Shift-Key : 200
> Encrypted Result: LwklfUahzwj
```

- Therefore the final encrypted result using a shift-key of 200 is:
  - "**`LwklfUahzwj`**".

---

### Message Decryption

- For decrypting text, use the **`CaesarCipher.decrypt`** class method:

```python
>>> from MyCaesarCipher import CaesarCipher

>>> decoder = CaesarCipher() # Create new class instance.
>>> code = 'OznoiXdkczm'
>>> decoder.decrypt(text=code, consoleOutput=True)

> Decrypted Shift-Key 0 : OZNOIXDKCZM
> Decrypted Shift-Key 1 : NYMNHWCJBYL
> Decrypted Shift-Key 2 : MXLMGVBIAXK
> Decrypted Shift-Key 3 : LWKLFUAHZWJ
> Decrypted Shift-Key 4 : KVJKETZGYVI
> Decrypted Shift-Key 5 : JUIJDSYFXUH
> Decrypted Shift-Key 6 : ITHICRXEWTG
> Decrypted Shift-Key 7 : HSGHBQWDVSF
> Decrypted Shift-Key 8 : GRFGAPVCURE
> Decrypted Shift-Key 9 : FQEFZOUBTQD
> Decrypted Shift-Key 10 : EPDEYNTASPC
> Decrypted Shift-Key 11 : DOCDXMSZROB
> Decrypted Shift-Key 12 : CNBCWLRYQNA
> Decrypted Shift-Key 13 : BMABVKQXPMZ
> Decrypted Shift-Key 14 : ALZAUJPWOLY
> Decrypted Shift-Key 15 : ZKYZTIOVNKX
> Decrypted Shift-Key 16 : YJXYSHNUMJW
> Decrypted Shift-Key 17 : XIWXRGMTLIV
> Decrypted Shift-Key 18 : WHVWQFLSKHU
> Decrypted Shift-Key 19 : VGUVPEKRJGT
> Decrypted Shift-Key 20 : UFTUODJQIFS
> Decrypted Shift-Key 21 : TESTNCIPHER # <- Correct Result
> Decrypted Shift-Key 22 : SDRSMBHOGDQ
> Decrypted Shift-Key 23 : RCQRLAGNFCP
> Decrypted Shift-Key 24 : QBPQKZFMEBO
> Decrypted Shift-Key 25 : PAOPJYELDAN
```

- The **`CaesarCipher.decrypt`** method will return all possible shifted-key variations of the given encrypted message.

- _Generally_, the most legible key output will be the correct decrypted message, assuming the encrypted message was legible to begin with.

- Regardless, the correct output MUST be one of the output values due to the limitations of the algorithm being tied to the length of the alphabet [26] and amount of possible numbers [0-9].

---

## Contact

- If you have any questions, comments, or concerns that cannot be alleviated through the [project's GitHub repository](https://github.com/schlopp96/MyCaesarCipher), please feel free to contact me through my email address:

  - `schloppdaddy@gmail.com`
