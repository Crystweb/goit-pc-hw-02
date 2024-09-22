import math

# Функція для створення порядку стовпців на основі ключової фрази
def get_permutation_order(key):
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    return [x[0] for x in order]

# Функція для шифрування за допомогою простої перестановки
def encrypt_transposition(text, key):
    text = ''.join([char for char in text if char.isalpha()])  # Очищаємо текст від пробілів і неалфавітних символів
    key_len = len(key)
    permutation_order = get_permutation_order(key)
    
    # Розрахунок кількості рядків
    num_rows = math.ceil(len(text) / key_len)
    
    # Додаємо заповнювачі, щоб текст був кратний довжині ключа
    padded_text = text.ljust(num_rows * key_len)
    
    # Створюємо таблицю з рядків
    table = [padded_text[i:i + key_len] for i in range(0, len(padded_text), key_len)]
    
    # Шифруємо, переставляючи стовпці за порядком
    cipher_text = ''
    for index in permutation_order:
        for row in table:
            cipher_text += row[index]
    
    return cipher_text

# Функція для дешифрування за допомогою простої перестановки
def decrypt_transposition(cipher_text, key):
    key_len = len(key)
    num_rows = math.ceil(len(cipher_text) / key_len)
    
    permutation_order = get_permutation_order(key)
    
    # Створюємо таблицю для дешифрування
    num_full_columns = len(cipher_text) % key_len
    num_chars_in_column = num_rows if num_full_columns == 0 else num_rows - 1
    
    # Ініціалізуємо порожню таблицю
    table = [''] * key_len
    start = 0
    
    for index in permutation_order:
        column_length = num_rows if index < num_full_columns else num_chars_in_column
        table[index] = cipher_text[start:start + column_length]
        start += column_length
    
    # Зчитуємо текст по рядках з таблиці
    original_text = ''
    for i in range(num_rows):
        for col in table:
            if i < len(col):
                original_text += col[i]
    
    return original_text

# Функція для шифрування методом подвійної перестановки
def double_transposition_encrypt(text, key1, key2):
    # Перше шифрування (перестановка за першим ключем)
    first_encryption = encrypt_transposition(text, key1)
    # Друге шифрування (перестановка за другим ключем)
    second_encryption = encrypt_transposition(first_encryption, key2)
    return second_encryption

# Функція для дешифрування методом подвійної перестановки
def double_transposition_decrypt(cipher_text, key1, key2):
    # Перше дешифрування (перестановка за другим ключем)
    first_decryption = decrypt_transposition(cipher_text, key2)
    # Друге дешифрування (перестановка за першим ключем)
    second_decryption = decrypt_transposition(first_decryption, key1)
    return second_decryption

# Основна програма
key1 = "SECRET"
key2 = "CRYPTO"
text = input("Введіть текст для шифрування: ").upper()

# Шифрування
cipher_text = double_transposition_encrypt(text, key1, key2)
print(f"Зашифрований текст: {cipher_text}")

# Дешифрування
decrypted_text = double_transposition_decrypt(cipher_text, key1, key2)
print(f"Розшифрований текст: {decrypted_text}")
