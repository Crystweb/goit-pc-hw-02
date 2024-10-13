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
    # Створюємо список букв з їхніми індексами
    key_letters = list(key)
    indexed_key = list(enumerate(key_letters))
    # Сортуємо за буквою, а при рівності — за індексом
    sorted_key = sorted(indexed_key, key=lambda x: (x[1], x[0]))
    # Визначаємо порядок
    order = [idx for idx, char in sorted_key]
    return order

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

def double_transposition_encrypt(plaintext, key1, key2):
    """
    Виконує подвійне шифрування тексту за допомогою двох табличних шифрів.
    
    Args:
        plaintext (str): Оригінальний текст.
        key1 (str): Перший ключ (для першої транспозиції).
        key2 (str): Другий ключ (для другої транспозиції).
    
    Returns:
        str: Подвійно зашифрований текст.
    """
    first_encryption = encrypt_columnar_transposition(plaintext, key1)
    second_encryption = encrypt_columnar_transposition(first_encryption, key2)
    return second_encryption

def double_transposition_decrypt(ciphertext, key1, key2):
    """
    Виконує подвійне дешифрування тексту за допомогою двох табличних шифрів.
    
    Args:
        ciphertext (str): Подвійно зашифрований текст.
        key1 (str): Перший ключ (для першої транспозиції).
        key2 (str): Другий ключ (для другої транспозиції).
    
    Returns:
        str: Розшифрований текст.
    """
    first_decryption = decrypt_columnar_transposition(ciphertext, key2)
    second_decryption = decrypt_columnar_transposition(first_decryption, key1)
    return second_decryption

def main_level2():
    print("=== Рівень 2: Подвійний табличний шифр зі стовпчиковою транспозицією ===\n")
    
    # Ключі
    key1 = "SECRET"
    key2 = "CRYPTO"
    print(f"Перший ключ (для першої транспозиції): {key1}")
    print(f"Другий ключ (для другої транспозиції): {key2}\n")
    
    # Введення тексту
    plaintext = input("Введіть текст для шифрування: ")
    
    # Шифрування
    ciphertext = double_transposition_encrypt(plaintext, key1, key2)
    print(f"\nЗашифрований текст після подвійної транспозиції: {ciphertext}\n")
    
    # Дешифрування
    decrypted_text = double_transposition_decrypt(ciphertext, key1, key2)
    print(f"Розшифрований текст: {decrypted_text}\n")

def main():
    print("Виберіть рівень:")
    print("1. Табличний шифр зі стовпчиковою транспозицією (Ключ: SECRET)")
    print("2. Подвійний табличний шифр зі стовпчиковою транспозицією (Ключі: SECRET та CRYPTO)")
    choice = input("Введіть 1 або 2: ")
    
    if choice == '1':
        print("\n=== Рівень 1: Табличний шифр зі стовпчиковою транспозицією ===\n")
        key = "SECRET"
        print(f"Ключ: {key}\n")
        
        plaintext = input("Введіть текст для шифрування: ")
        
        # Шифрування
        ciphertext = encrypt_columnar_transposition(plaintext, key)
        print(f"\nЗашифрований текст: {ciphertext}\n")
        
        # Дешифрування
        decrypted_text = decrypt_columnar_transposition(ciphertext, key)
        print(f"Розшифрований текст: {decrypted_text}\n")
    
    elif choice == '2':
        main_level2()
    else:
        print("Невірний вибір. Завершення програми.")

if __name__ == "__main__":
    main()
