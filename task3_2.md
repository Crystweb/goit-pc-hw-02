## Рівень 2: Подвійне шифрування (Віженер, потім Табличний шифр)

### Опис завдання

Зашифруємо текст спочатку за допомогою **шифру Віженера** з ключем "CRYPTO", а потім отриманий результат зашифруємо за допомогою **стовпчикової транспозиції** з ключем "CRYPTO".

### Реалізація на Python

#### Основні функції:

1. **`vigenere_encrypt(plaintext, key)`**: Шифрує текст за допомогою шифру Віженера.
2. **`vigenere_decrypt(ciphertext, key)`**: Дешифрує текст за допомогою шифру Віженера.
3. **`encrypt_columnar_transposition(plaintext, key)`**: Шифрує текст за допомогою стовпчикової транспозиції.
4. **`decrypt_columnar_transposition(ciphertext, key)`**: Дешифрує текст за допомогою стовпчикової транспозиції.

#### Повний код для Рівня 2:

```python
import math

def generate_order(key):
    key = key.upper()
    sorted_key = sorted([(char, idx) for idx, char in enumerate(key)])
    order = {}
    current_order = 1
    for char, idx in sorted_key:
        order[idx] = current_order
        current_order += 1
    return order

def encrypt_columnar_transposition(plaintext, key):

    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    ciphertext = [''] * key_length
    
    for idx, char in enumerate(plaintext):
        column = idx % key_length
        ciphertext[column] += char
    
    sorted_columns = sorted(order.items(), key=lambda x: x[1])
    encrypted_text = ''.join([ciphertext[idx] for idx, _ in sorted_columns])
    
    return encrypted_text

def decrypt_columnar_transposition(ciphertext, key):
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    num_of_rows = math.ceil(len(ciphertext) / key_length)
    sorted_columns = sorted(order.items(), key=lambda x: x[1])
    
    num_full_columns = len(ciphertext) % key_length
    if num_full_columns == 0:
        num_full_columns = key_length
    
    column_lengths = {}
    for idx, (col_idx, _) in enumerate(sorted_columns):
        if idx < num_full_columns:
            column_lengths[col_idx] = num_of_rows
        else:
            column_lengths[col_idx] = num_of_rows - 1
    
    columns = {}
    pointer = 0
    for col_idx, _ in sorted_columns:
        length = column_lengths[col_idx]
        columns[col_idx] = ciphertext[pointer:pointer+length]
        pointer += length
    
    plaintext = ''
    for i in range(num_of_rows):
        for j in range(key_length):
            if i < len(columns[j]):
                plaintext += columns[j][i]
    
    return plaintext

def vigenere_encrypt(plaintext, key):
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
            encrypted.append(char)
    return ''.join(encrypted)

def vigenere_decrypt(ciphertext, key):
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
    
    plaintext = input("Введіть текст для шифрування: ")
    
    vigenere_key = "CRYPTO"
    table_key = "CRYPTO"
    
    vigenere_encrypted = vigenere_encrypt(plaintext, vigenere_key)
    print(f"\nТекст після шифру Віженера: {vigenere_encrypted}\n")
    
    table_ciphertext = encrypt_columnar_transposition(vigenere_encrypted, table_key)
    print(f"Зашифрований текст після табличного шифру: {table_ciphertext}\n")
    
    table_decrypted = decrypt_columnar_transposition(table_ciphertext, table_key)
    print(f"Текст після дешифрування табличного шифру: {table_decrypted}\n")
    
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
```

#### Пояснення коду:

1. **Функція `generate_order(key)`**:
   - Сортує букви ключа в алфавітному порядку.
   - Призначає кожній букві порядковий номер, визначаючи порядок стовпчиків для шифрування та дешифрування.
   - У випадку повторюваних букв, порядок визначається їхнім порядком появи у ключі.

2. **Функція `encrypt_columnar_transposition(plaintext, key)`**:
   - Записує текст по рядках у таблицю зі стовпчиками, кількість яких дорівнює довжині ключа.
   - Зчитує стовпчики у визначеному порядку, формуючи зашифрований текст.
   - Зберігає пробіли та розділові знаки як звичайні символи.

3. **Функція `decrypt_columnar_transposition(ciphertext, key)`**:
   - Визначає кількість рядків у таблиці на основі довжини зашифрованого тексту та ключа.
   - Визначає кількість символів у кожному стовпчику, враховуючи неповні стовпчики.
   - Розподіляє зашифрований текст по стовпчиках відповідно до порядку.
   - Відновлює оригінальний текст, зчитуючи по рядках.

4. **Функції `vigenere_encrypt` та `vigenere_decrypt`**:
   - Реалізують шифр Віженера, зберігаючи пробіли та розділові знаки як звичайні символи.
   - Кожна літера тексту зсувається на величину, визначену відповідною літерою ключа.
   - Дешифрування виконується шляхом зворотного зсуву.

5. **Функція `main_level1()`**:
   - Виконує шифрування та дешифрування тексту за допомогою стовпчикової транспозиції з ключем "MATRIX".

6. **Функція `main_level2()`**:
   - Виконує подвійне шифрування: спочатку шифрує текст за допомогою шифру Віженера з ключем "CRYPTO", потім отриманий результат шифрує за допомогою табличного шифру зі стовпчиковою транспозицією з ключем "CRYPTO".
   - Дешифрує текст у зворотному порядку: спочатку дешифрує табличний шифр, потім шифр Віженера.

7. **Функція `main()`**:
   - Запитує у користувача вибір рівня та виконує відповідні функції.


### Додаткові пояснення:

1. **Збереження пробілів та розділових знаків:**
   - У даній реалізації пробіли та розділові знаки розглядаються як звичайні символи і включаються у шифр та дешифрований текст.

2. **Коректність шифрування та дешифрування:**
   - Для перевірки коректності роботи програми можна зашифрувати текст та дешифрувати його, переконавшись, що оригінальний текст відновлюється без втрат.

3. **Гнучкість ключів:**
   - Ви можете змінювати ключі "MATRIX" та "CRYPTO" на будь-які інші ключові фрази за потребою, враховуючи, що ключ має бути без пробілів та розділових знаків.

4. **Обробка великих текстів:**
   - Чим більший обсяг тексту, тим точніше шифрування та дешифрування, особливо при використанні стовпчикової транспозиції.

5. **Розширення функціоналу:**
   - Можна додати можливість вибору різних методів шифрування та дешифрування, або автоматичного визначення ключа.