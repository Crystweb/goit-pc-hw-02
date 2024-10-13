import math
from collections import defaultdict

def generate_order(key):
    """
    Генерує порядок стовпчиків на основі ключа.
    Порядок визначається алфавітним порядком букв ключа.
    У випадку повторюваних букв, порядок визначається їхнім появленням.
    """
    key = key.upper()
    sorted_key = sorted([(char, idx) for idx, char in enumerate(key)])
    order = {}
    current_order = 1
    for char, idx in sorted_key:
        order[idx] = current_order
        current_order += 1
    return order

def encrypt_columnar_transposition(plaintext, key):
    """
    Шифрує текст за допомогою стовпчикової транспозиції.
    Зберігає пробіли та розділові знаки.
    """
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    ciphertext = [''] * key_length
    
    # Заповнюємо таблицю по рядках
    for idx, char in enumerate(plaintext):
        column = idx % key_length
        ciphertext[column] += char
    
    # Створюємо список стовпчиків у порядку шифрування
    sorted_columns = sorted(order.items(), key=lambda x: x[1])
    encrypted_text = ''.join([ciphertext[idx] for idx, _ in sorted_columns])
    
    return encrypted_text

def decrypt_columnar_transposition(ciphertext, key):
    """
    Дешифрує текст за допомогою стовпчикової транспозиції.
    Зберігає пробіли та розділові знаки.
    """
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    num_of_rows = math.ceil(len(ciphertext) / key_length)
    sorted_columns = sorted(order.items(), key=lambda x: x[1])
    
    # Визначаємо кількість символів у кожному стовпчику
    num_full_columns = len(ciphertext) % key_length
    if num_full_columns == 0:
        num_full_columns = key_length
    
    column_lengths = {}
    for idx, (col_idx, _) in enumerate(sorted_columns):
        if idx < num_full_columns:
            column_lengths[col_idx] = num_of_rows
        else:
            column_lengths[col_idx] = num_of_rows - 1
    
    # Розподіляємо зашифрований текст по стовпчиках
    columns = {}
    pointer = 0
    for col_idx, _ in sorted_columns:
        length = column_lengths[col_idx]
        columns[col_idx] = ciphertext[pointer:pointer+length]
        pointer += length
    
    # Відновлюємо оригінальний текст
    plaintext = ''
    for i in range(num_of_rows):
        for j in range(key_length):
            if i < len(columns[j]):
                plaintext += columns[j][i]
    
    return plaintext

def main_level1():
    print("=== Рівень 1: Табличний шифр зі стовпчиковою транспозицією ===\n")
    
    key = "MATRIX"
    print(f"Ключ: {key}")
    
    plaintext = input("Введіть текст для шифрування: ")
    ciphertext = encrypt_columnar_transposition(plaintext, key)
    print(f"\nЗашифрований текст: {ciphertext}\n")
    
    decrypted_text = decrypt_columnar_transposition(ciphertext, key)
    print(f"Розшифрований текст: {decrypted_text}\n")

if __name__ == "__main__":
    main_level1()
