## Рівень 1: Табличний шифр зі стовпчиковою транспозицією з ключем "MATRIX"

### Опис стовпчикової транспозиції

**Стовпчикова транспозиція** (Columnar Transposition Cipher) — це метод шифрування, де текст записується в таблицю за стовпчиками відповідно до ключового слова, а потім читається стовпчиками у порядку, визначеному ключем.

**Кроки шифрування:**
1. **Визначення порядку стовпчиків:** Сортуємо букви ключа в алфавітному порядку, призначаючи кожній букві номер, який визначає порядок читання стовпчиків.
2. **Запис тексту в таблицю:** Записуємо текст по рядках у таблицю з кількістю стовпчиків, що дорівнює довжині ключа.
3. **Читання стовпчиків у визначеному порядку:** Зчитуємо текст стовпчиками відповідно до порядку, визначеного ключем, отримуючи зашифрований текст.

**Кроки дешифрування:**
1. **Визначення порядку стовпчиків:** Використовуємо той самий порядок стовпчиків, що й при шифруванні.
2. **Розподіл зашифрованого тексту по стовпчиках:** Розбиваємо зашифрований текст на стовпчики відповідно до порядку та довжини ключа.
3. **Відновлення оригінального тексту:** Зчитуємо текст по рядках з таблиці.

### Реалізація на Python

#### Основні функції:

1. **`generate_order(key)`**: Визначає порядок стовпчиків на основі ключа.
2. **`encrypt_columnar_transposition(plaintext, key)`**: Шифрує текст за допомогою стовпчикової транспозиції.
3. **`decrypt_columnar_transposition(ciphertext, key)`**: Дешифрує текст за допомогою стовпчикової транспозиції.

#### Повний код для Рівня 1:

```python
import math
from collections import defaultdict

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
```

#### Пояснення коду:

1. **Функція `generate_order(key)`**:
   - Перетворює ключ на верхній регістр.
   - Сортує букви ключа в алфавітному порядку, зберігаючи їхні індекси.
   - Призначає кожному стовпчику номер порядку на основі сортування.

2. **Функція `encrypt_columnar_transposition(plaintext, key)`**:
   - Записує текст по рядках у таблицю з кількістю стовпчиків, що дорівнює довжині ключа.
   - Зчитує стовпчики у порядку, визначеному ключем, щоб сформувати зашифрований текст.

3. **Функція `decrypt_columnar_transposition(ciphertext, key)`**:
   - Визначає кількість рядків у таблиці.
   - Визначає кількість символів у кожному стовпчику, враховуючи неповні стовпчики.
   - Розподіляє зашифрований текст по стовпчиках у визначеному порядку.
   - Зчитує текст по рядках, відновлюючи оригінальний текст.

4. **Функція `main_level1()`**:
   - Запитує у користувача текст для шифрування.
   - Шифрує текст за допомогою стовпчикової транспозиції з ключем "MATRIX".
   - Дешифрує отриманий зашифрований текст для перевірки правильності.


**Примітка:** У цьому прикладі пробіли та розділові знаки зберігаються у зашифрованому тексті, оскільки вони обробляються як звичайні символи.
