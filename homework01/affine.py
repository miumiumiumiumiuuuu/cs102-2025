def encrypt_affine(plaintext: str, a: int, b: int) -> str:
    ciphertext = ""
    m = 26

    for char in plaintext:
        if char.isupper():
            x = ord(char) - ord('A')
            encrypted_x = (a * x + b) % m
            encrypted_char = chr(encrypted_x + ord('A'))
            ciphertext += encrypted_char
        elif char.islower():
            x = ord(char) - ord('a')
            encrypted_x = (a * x + b) % m
            encrypted_char = chr(encrypted_x + ord('a'))
            ciphertext += encrypted_char
        else:
            ciphertext += char

    return ciphertext


def decrypt_affine(ciphertext: str, a: int, b: int) -> str:
    plaintext = ""
    m = 26
    def mod_inverse(a: int, m: int) -> int:
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return 1

    a_inv = mod_inverse(a, m)

    for char in ciphertext:
        if char.isupper():
            y = ord(char) - ord('A')
            decrypted_x = (a_inv * (y - b)) % m
            decrypted_char = chr(decrypted_x + ord('A'))
            plaintext += decrypted_char
        elif char.islower():
            y = ord(char) - ord('a')
            decrypted_x = (a_inv * (y - b)) % m
            decrypted_char = chr(decrypted_x + ord('a'))
            plaintext += decrypted_char
        else:
            plaintext += char

    return plaintext