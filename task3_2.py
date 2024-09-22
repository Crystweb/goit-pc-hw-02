import string

# Шифр Віженера
def vigenere_encrypt(plaintext, key):
    alphabet = string.ascii_uppercase
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper()
    cipher_text = ''
    
    for i, letter in enumerate(plaintext):
        letter_index = alphabet.index(letter)
        key_index = alphabet.index(key[i % len(key)])
        cipher_letter = alphabet[(letter_index + key_index) % 26]
        cipher_text += cipher_letter
    
    return cipher_text

def vigenere_decrypt(cipher_text, key):
    alphabet = string.ascii_uppercase
    key = key.upper()
    plaintext = ''
    
    for i, letter in enumerate(cipher_text):
        letter_index = alphabet.index(letter)
        key_index = alphabet.index(key[i % len(key)])
        plain_letter = alphabet[(letter_index - key_index) % 26]
        plaintext += plain_letter
    
    return plaintext

# Табличний шифр
def create_matrix(key):
    key = ''.join(sorted(set(key), key=key.index))  # Унікальні символи з ключа, зберігаючи порядок
    alphabet = string.ascii_uppercase.replace('J', '')  # Використовуємо алфавіт без 'J'
    
    # Створюємо повний список символів для матриці
    matrix_elements = key + ''.join([char for char in alphabet if char not in key])
    
    # Створюємо матрицю 5x5
    matrix = [list(matrix_elements[i:i+5]) for i in range(0, 25, 5)]
    
    return matrix

def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

def encrypt_table_cipher(plaintext, matrix):
    plaintext = plaintext.upper().replace("J", "I")
    plaintext = ''.join([char for char in plaintext if char.isalpha()])
    
    pairs = []
    i = 0
    while i < len(plaintext):
        first_letter = plaintext[i]
        second_letter = plaintext[i + 1] if i + 1 < len(plaintext) else 'X'
        if first_letter == second_letter:
            pairs.append((first_letter, 'X'))
            i += 1
        else:
            pairs.append((first_letter, second_letter))
            i += 2
    
    cipher_text = ''
    for (a, b) in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:
            cipher_text += matrix[row1][(col1 + 1) % 5]
            cipher_text += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher_text += matrix[(row1 + 1) % 5][col1]
            cipher_text += matrix[(row2 + 1) % 5][col2]
        else:
            cipher_text += matrix[row1][col2]
            cipher_text += matrix[row2][col1]
    
    return cipher_text

def decrypt_table_cipher(cipher_text, matrix):
    plaintext = ''
    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    
    return plaintext

# Основна програма
text = input("Введіть текст для шифрування: ").upper()
vigenere_key = "KEY"
table_key = "CRYPTO"

# Етап 1: Шифрування шифром Віженера
vigenere_encrypted = vigenere_encrypt(text, vigenere_key)
print(f"Зашифрований текст (Віженер): {vigenere_encrypted}")

# Етап 2: Шифрування табличним шифром
matrix = create_matrix(table_key)
table_encrypted = encrypt_table_cipher(vigenere_encrypted, matrix)
print(f"Зашифрований текст (табличний): {table_encrypted}")

# Етап 3: Дешифрування табличним шифром
table_decrypted = decrypt_table_cipher(table_encrypted, matrix)
print(f"Розшифрований текст (табличний): {table_decrypted}")

# Етап 4: Дешифрування шифром Віженера
vigenere_decrypted = vigenere_decrypt(table_decrypted, vigenere_key)
print(f"Розшифрований текст (Віженер): {vigenere_decrypted}")
