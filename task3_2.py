import math

from task3_1 import main_level1


def get_order(key):
    """
    Генерує порядок стовпчиків на основі ключа.
    Порядок визначається алфавітним порядком букв ключа.
    У випадку повторюваних букв, порядок визначається їхнім порядком появи.
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
    order = get_order(key)
    key_length = len(key)
    num_of_rows = math.ceil(len(plaintext) / key_length)
    
    # Заповнюємо таблицю рядками
    grid = [''] * key_length
    for idx, char in enumerate(plaintext):
        column = idx % key_length
        grid[column] += char
    
    # Якщо останній стовпчик не повністю заповнений, доповнюємо його символом 'X'
    for i in range(key_length):
        if len(grid[i]) < num_of_rows:
            grid[i] += 'X' * (num_of_rows - len(grid[i]))
    
    # Створюємо список стовпчиків у порядку шифрування
    sorted_columns = sorted(order.items(), key=lambda x: x[1])
    encrypted_text = ''.join([grid[idx] for idx, _ in sorted_columns])
    
    return encrypted_text

def decrypt_columnar_transposition(ciphertext, key):
    """
    Дешифрує текст за допомогою стовпчикової транспозиції.
    Зберігає пробіли та розділові знаки.
    """
    key = key.upper()
    order = get_order(key)
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
    
    # Видаляємо заповнювачі 'X' якщо вони були додані
    plaintext = plaintext.rstrip('X')
    
    return plaintext

def vigenere_encrypt(plaintext, key):
    """Шифрує текст за допомогою шифру Віженера."""
    encrypted = []
    key_length = len(key)
    key_int = [ord(k.upper()) - 65 for k in key]
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = key_int[key_index % key_length]
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char.upper()) - 65 + shift) % 26 + 65)
            encrypted.append(encrypted_char if char.isupper() else encrypted_char.lower())
            key_index += 1
        else:
            encrypted.append(char)  # Зберігаємо пробіли та розділові знаки
    return ''.join(encrypted)

def vigenere_decrypt(ciphertext, key):
    """Дешифрує текст за допомогою шифру Віженера."""
    decrypted = []
    key_length = len(key)
    key_int = [ord(k.upper()) - 65 for k in key]
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = key_int[key_index % key_length]
            decrypted_char = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
            decrypted.append(decrypted_char if char.isupper() else decrypted_char.lower())
            key_index += 1
        else:
            decrypted.append(char)  # Зберігаємо пробіли та розділові знаки
    return ''.join(decrypted)

def main_level2():
    print("=== Рівень 2: Подвійне шифрування (Віженер, потім Табличний шифр) ===\n")
    
    # Вхідний текст
    plaintext = input("Введіть текст для шифрування: ")
    
    # Ключі
    vigenere_key = "CRYPTO"
    table_key = "CRYPTO"
    
    # Шифрування за допомогою шифру Віженера
    vigenere_encrypted = vigenere_encrypt(plaintext, vigenere_key)
    print(f"\nТекст після шифру Віженера: {vigenere_encrypted}\n")
    
    # Шифрування за допомогою табличного шифру (стовпчикова транспозиція)
    table_ciphertext = encrypt_columnar_transposition(vigenere_encrypted, table_key)
    print(f"Зашифрований текст після табличного шифру: {table_ciphertext}\n")
    
    # Дешифрування табличного шифру
    table_decrypted = decrypt_columnar_transposition(table_ciphertext, table_key)
    print(f"Текст після дешифрування табличного шифру: {table_decrypted}\n")
    
    # Дешифрування шифру Віженера
    final_decrypted = vigenere_decrypt(table_decrypted, vigenere_key)
    print(f"Розшифрований текст: {final_decrypted}\n")


def main():
    print("Виберіть рівень:")
    print("1. Табличний шифр зі стовпчиковою транспозицією")
    print("2. Подвійне шифрування (Віженер, потім Табличний шифр)")
    choice = input("Введіть 1 або 2: ")

    if choice == '1':
        main_level1()
    elif choice == '2':
        main_level2()
    else:
        print("Невірний вибір. Завершення програми.")


if __name__ == "__main__":
    main()