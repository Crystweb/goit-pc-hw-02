import math

def generate_order(key):
    """
    Генерує порядок стовпчиків на основі ключа.
    Порядок визначається алфавітним порядком букв ключа.
    У випадку повторюваних букв, порядок визначається їхнім порядком появи.
    
    Args:
        key (str): Ключове слово.
    
    Returns:
        list: Список індексів стовпчиків у порядку їх читання.
    """
    key = key.upper()
    # Сортуємо букви ключа з урахуванням їхніх індексів для повторюваних букв
    sorted_key = sorted([(char, idx) for idx, char in enumerate(key)], key=lambda x: (x[0], x[1]))
    order = {}
    current_order = 1
    for char, idx in sorted_key:
        order[idx] = current_order
        current_order += 1
    # Створюємо список стовпчиків у порядку їх читання
    ordered_columns = sorted(order, key=lambda x: order[x])
    return ordered_columns

def encrypt_columnar_transposition(plaintext, key):
    """
    Шифрує текст за допомогою стовпчикової транспозиції.
    Зберігає пробіли та розділові знаки.
    
    Args:
        plaintext (str): Текст для шифрування.
        key (str): Ключове слово.
    
    Returns:
        str: Зашифрований текст.
    """
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    ciphertext = [''] * key_length
    
    # Заповнюємо таблицю по рядках
    for idx, char in enumerate(plaintext):
        column = idx % key_length
        ciphertext[column] += char
    
    # Зчитуємо стовпчики у визначеному порядку
    encrypted_text = ''.join([ciphertext[idx] for idx in order])
    
    return encrypted_text

def decrypt_columnar_transposition(ciphertext, key):
    """
    Дешифрує текст за допомогою стовпчикової транспозиції.
    Зберігає пробіли та розділові знаки.
    
    Args:
        ciphertext (str): Зашифрований текст.
        key (str): Ключове слово.
    
    Returns:
        str: Розшифрований текст.
    """
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    num_of_rows = math.ceil(len(ciphertext) / key_length)
    num_full_columns = len(ciphertext) % key_length
    
    # Визначаємо кількість символів у кожному стовпчику
    column_lengths = {}
    for idx in order:
        if num_full_columns == 0 or idx < num_full_columns:
            column_lengths[idx] = num_of_rows
        else:
            column_lengths[idx] = num_of_rows - 1
    
    # Розподіляємо зашифрований текст по стовпчиках
    columns = {}
    pointer = 0
    for idx in order:
        length = column_lengths[idx]
        columns[idx] = ciphertext[pointer:pointer+length]
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
    
    key = "SECRET"
    print(f"Ключ: {key}\n")
    
    plaintext = input("Введіть текст для шифрування: ")
    
    # Шифрування
    ciphertext = encrypt_columnar_transposition(plaintext, key)
    print(f"\nЗашифрований текст: {ciphertext}\n")
    
    # Дешифрування
    decrypted_text = decrypt_columnar_transposition(ciphertext, key)
    print(f"Розшифрований текст: {decrypted_text}\n")

if __name__ == "__main__":
    main_level1()
