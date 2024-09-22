import math

# Функція для створення порядку стовпців на основі ключової фрази
def get_permutation_order(key):
    # Створюємо список пар (індекс, літера) для сортування
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    # Повертаємо індекси перестановки
    return [x[0] for x in order]

# Функція для шифрування методом простої перестановки
def encrypt_transposition(text, key):
    # Очищаємо текст, прибираємо пробіли та неалфавітні символи
    text = ''.join([char for char in text if char.isalpha()])
    
    key_len = len(key)
    # Порядок стовпців на основі ключа
    permutation_order = get_permutation_order(key)
    
    # Додаємо заповнювачі для вирівнювання матриці
    num_rows = math.ceil(len(text) / key_len)
    padded_text = text.ljust(num_rows * key_len)
    
    # Заповнюємо таблицю за рядками
    table = [padded_text[i:i + key_len] for i in range(0, len(padded_text), key_len)]
    
    # Шифруємо текст, переставляючи стовпці за порядком перестановки
    cipher_text = ''
    for index in permutation_order:
        for row in table:
            cipher_text += row[index]
    
    return cipher_text

# Функція для дешифрування методом простої перестановки
def decrypt_transposition(cipher_text, key):
    key_len = len(key)
    num_rows = math.ceil(len(cipher_text) / key_len)
    
    # Порядок стовпців на основі ключа
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

# Основна програма
key = "SECRET"
text = input("Введіть текст для шифрування: ").upper()

# Шифрування
cipher_text = encrypt_transposition(text, key)
print(f"Зашифрований текст: {cipher_text}")

# Дешифрування
decrypted_text = decrypt_transposition(cipher_text, key)
print(f"Розшифрований текст: {decrypted_text}")
