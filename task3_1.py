import string

# Створення матриці для шифру на основі фрази-ключа
def create_matrix(key):
    key = ''.join(sorted(set(key), key=key.index))  # Унікальні символи з ключа, зберігаючи порядок
    alphabet = string.ascii_uppercase.replace('J', '')  # Використовуємо алфавіт без 'J'
    
    # Створюємо повний список символів для матриці
    matrix_elements = key + ''.join([char for char in alphabet if char not in key])
    
    # Створюємо матрицю 5x5
    matrix = [list(matrix_elements[i:i+5]) for i in range(0, 25, 5)]
    
    return matrix

# Функція для знаходження координат літери в матриці
def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

# Функція для шифрування тексту
def encrypt_table_cipher(plaintext, matrix):
    plaintext = plaintext.upper().replace("J", "I")  # Замінюємо 'J' на 'I'
    plaintext = ''.join([char for char in plaintext if char.isalpha()])  # Видаляємо пробіли та неалфавітні символи

    # Розбиваємо текст на пари літер
    pairs = []
    i = 0
    while i < len(plaintext):
        first_letter = plaintext[i]
        second_letter = plaintext[i + 1] if i + 1 < len(plaintext) else 'X'
        
        # Якщо пари складаються з однакових літер, додаємо 'X' між ними
        if first_letter == second_letter:
            pairs.append((first_letter, 'X'))
            i += 1
        else:
            pairs.append((first_letter, second_letter))
            i += 2
    
    # Шифруємо кожну пару
    cipher_text = ''
    for (a, b) in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:
            # Літери в одному рядку - зміщуємо вправо
            cipher_text += matrix[row1][(col1 + 1) % 5]
            cipher_text += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            # Літери в одному стовпці - зміщуємо вниз
            cipher_text += matrix[(row1 + 1) % 5][col1]
            cipher_text += matrix[(row2 + 1) % 5][col2]
        else:
            # Літери в різних рядках і стовпцях - беремо на перетині
            cipher_text += matrix[row1][col2]
            cipher_text += matrix[row2][col1]
    
    return cipher_text

# Функція для дешифрування тексту
def decrypt_table_cipher(cipher_text, matrix):
    cipher_text = cipher_text.upper().replace("J", "I")
    
    # Дешифруємо кожну пару
    plaintext = ''
    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        
        if row1 == row2:
            # Літери в одному рядку - зміщуємо вліво
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            # Літери в одному стовпці - зміщуємо вгору
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            # Літери в різних рядках і стовпцях - беремо на перетині
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    
    return plaintext

# Основна програма
key = "MATRIX"
text = input("Введіть текст для шифрування: ").upper()

# Створюємо матрицю шифрування
matrix = create_matrix(key)
print("Матриця шифрування:")
for row in matrix:
    print(' '.join(row))

# Шифрування
cipher_text = encrypt_table_cipher(text, matrix)
print(f"Зашифрований текст: {cipher_text}")

# Дешифрування
decrypted_text = decrypt_table_cipher(cipher_text, matrix)
print(f"Розшифрований текст: {decrypted_text}")
