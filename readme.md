# [Task 1.1 - Шифр Віженера, рівень 1](task1_1.py)
### Лістинг:
```python
def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return ''.join(key)

def encrypt(text, key):
    cipher_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i].upper()) + ord(key[i])) % 26
            x += ord('A')
            cipher_text.append(chr(x))
        else:
            cipher_text.append(text[i])
    return ''.join(cipher_text)

def decrypt(cipher_text, key):
    original_text = []
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
            x += ord('A')
            original_text.append(chr(x))
        else:
            original_text.append(cipher_text[i])
    return ''.join(original_text)
text = input("Введіть текст для шифрування: ")
key = "CRYPTOGRAPHY"
generated_key = generate_key(text, key)
cipher_text = encrypt(text, generated_key)
print(f"Зашифрований текст: {cipher_text}")
decrypted_text = decrypt(cipher_text, generated_key)
print(f"Розшифрований текст: {decrypted_text}")
```

### Пояснення до лістингу:
1. **Функція `generate_key`**: генерує ключ, який повторюється або обрізається відповідно до довжини тексту.
2. **Функція `encrypt`**: шифрує текст за допомогою шифру Віженера, перетворюючи літери на основі ключа.
3. **Функція `decrypt`**: відновлює оригінальний текст із зашифрованого, використовуючи той самий ключ.

**Примітка:** Текст може містити пробіли або інші неалфавітні символи, і вони залишаються незмінними під час шифрування та дешифрування.

# [Task 1.2 - Шифр Віженера, рівень 2](task1_2.py)
### Основні кроки:
1. **Метод Касікі**: Знаходження повторюваних послідовностей літер у шифротексті та визначення довжини ключа на основі відстаней між цими повтореннями.
2. **Метод Фрідмана**: Оцінка довжини ключа на основі індексу відповідності (IC).
3. **Частотний аналіз**: Визначення символів ключа за допомогою хі-квадрат статистики.
4. **Дешифрування**: Розшифровування тексту за знайденим ключем, зберігаючи пробіли та розділові знаки.

### Лістинг:

```python
import string
from collections import Counter
from math import gcd
from functools import reduce

ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def find_repeated_sequences_spacings(ciphertext, sequence_length=3):
    spacings = []
    seq_positions = {}
    for i in range(len(ciphertext) - sequence_length +1):
        seq = ciphertext[i:i+sequence_length]
        if seq in seq_positions:
            for pos in seq_positions[seq]:
                spacing = i - pos
                spacings.append(spacing)
            seq_positions[seq].append(i)
        else:
            seq_positions[seq] = [i]
    return spacings

def kasiski_examination(ciphertext, sequence_length=3):
    spacings = find_repeated_sequences_spacings(ciphertext, sequence_length)
    if not spacings:
        return None
    gcd_all = reduce(gcd, spacings)
    return gcd_all

def friedman_test(ciphertext):
    filtered_text = [c.upper() for c in ciphertext if c.isalpha()]
    N = len(filtered_text)
    if N <= 1:
        return 0

    freq = Counter(filtered_text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

def estimate_key_length_friedman(ciphertext):
    ic = friedman_test(ciphertext)
    N = len([c for c in ciphertext if c.isalpha()])
    if ic == 0:
        return 1
    # Формула Фрідмана: K ≈ (0.0265 * N) / [(IC * (N - 1)) - (0.0385 * N) + 0.065]
    numerator = 0.0265 * N
    denominator = (ic * (N - 1)) - (0.0385 * N) + 0.065
    if denominator <=0:
        return 1
    key_length_estimate = numerator / denominator
    return max(1, round(key_length_estimate))

def get_possible_key_lengths(ciphertext):
    key_length_kasiski = kasiski_examination(ciphertext)
    key_length_friedman = estimate_key_length_friedman(ciphertext)
    possible_lengths = []
    if key_length_kasiski and 1 < key_length_kasiski <= 20:
        possible_lengths.append(key_length_kasiski)
    possible_lengths.append(key_length_friedman)
    for length in range(1,4):
        if 1 <= (key_length_friedman - length) <= 20:
            possible_lengths.append(key_length_friedman - length)
        if 1 <= (key_length_friedman + length) <= 20:
            possible_lengths.append(key_length_friedman + length)
    possible_lengths = [k for k in possible_lengths if 1 <= k <= 20]
    possible_lengths = sorted(set(possible_lengths))
    return possible_lengths

def split_into_groups(ciphertext, key_length):
    groups = ['' for _ in range(key_length)]
    index = 0
    for char in ciphertext:
        if char.isalpha():
            groups[index % key_length] += char.upper()
            index += 1
    return groups

def chi_squared_statistic(counter, total):
    chi2 = 0.0
    for letter in string.ascii_uppercase:
        observed = counter.get(letter, 0)
        expected = ENGLISH_FREQ.get(letter, 0) * total
        chi2 += ((observed - expected) ** 2) / expected if expected > 0 else 0
    return chi2

def find_key_for_group(group):
    total = len(group)
    if total == 0:
        return 'A'
    counter = Counter(group)
    min_chi2 = float('inf')
    best_shift = 0
    for shift in range(26):
        decrypted = ''.join([chr((ord(c) - 65 - shift) % 26 + 65) for c in group])
        decrypted_counter = Counter(decrypted)
        chi2 = chi_squared_statistic(decrypted_counter, total)
        if chi2 < min_chi2:
            min_chi2 = chi2
            best_shift = shift
    return chr(best_shift + 65)

def find_key(groups):
    key = ''
    for group in groups:
        key += find_key_for_group(group)
    return key

def decrypt_vigenere(ciphertext, key):
    decrypted = []
    key_length = len(key)
    key_int = [ord(k) - 65 for k in key.upper()]
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = key_int[key_index % key_length]
            decrypted_char = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
            decrypted.append(decrypted_char if char.isupper() else decrypted_char.lower())
            key_index += 1
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def vigenere_encrypt(plaintext, key):
    encrypted = []
    key_length = len(key)
    key_int = [ord(k.upper()) - 65 for k in key]
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = key_int[key_index % key_length]
            encrypted_char = chr((ord(char.upper()) - 65 + shift) % 26 + 65)
            encrypted.append(encrypted_char if char.isupper() else encrypted_char.lower())
            key_index += 1
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def main():
    plaintext = input("Введіть текст для шифрування: ")

    vigenere_key = "CRYPTOGRAPHY"

    ciphertext = vigenere_encrypt(plaintext, vigenere_key)
    print(f"\nЗашифрований текст: {ciphertext}\n")

    # Якщо ви хочете дешифрувати власний текст, закоментуйте рядок шифрування та розкоментуйте нижче:
    # ciphertext = input("Введіть зашифрований текст: ")
    possible_key_lengths = get_possible_key_lengths(ciphertext)
    print(f"Можливі довжини ключа: {possible_key_lengths}")

    best_key = None
    best_chi2 = float('inf')
    best_decrypted = ''

    for key_length in possible_key_lengths:
        groups = split_into_groups(ciphertext, key_length)
        found_key = find_key(groups)
        decrypted_text = decrypt_vigenere(ciphertext, found_key)
        groups_decrypted = split_into_groups(decrypted_text, key_length)
        total_chi2 = 0.0
        for group in groups_decrypted:
            total = len(group)
            if total == 0:
                continue
            counter = Counter([c.upper() for c in group if c.isalpha()])
            chi2 = chi_squared_statistic(counter, total)
            total_chi2 += chi2
        average_chi2 = total_chi2 / key_length if key_length > 0 else float('inf')
        if average_chi2 < best_chi2:
            best_chi2 = average_chi2
            best_key = found_key
            best_decrypted = decrypted_text

    print(f"Оцінена довжина ключа: {len(best_key)}")
    print(f"Знайдений ключ: {best_key}")
    print(f"\nРозшифрований текст:\n{best_decrypted}")

if __name__ == "__main__":
    main()
```

### Пояснення до лістингу:

1. **Частотні дані (`ENGLISH_FREQ`)**:
   - Використовуються для обчислення хі-квадрат статистики, щоб визначити, наскільки розшифрований текст відповідає типовим частотам англійських букв.

2. **Метод Касікі**:
   - Функція `find_repeated_sequences_spacings` шукає повторювані послідовності символів довжиною 3 та обчислює відстані між їх повтореннями.
   - Функція `kasiski_examination` обчислює найбільший спільний дільник (GCD) усіх відстаней, щоб оцінити довжину ключа.

3. **Метод Фрідмана**:
   - Функція `friedman_test` обчислює індекс відповідності (IC) для всього тексту.
   - Функція `estimate_key_length_friedman` використовує метод Фрідмана для оцінки довжини ключа за формулою:
     \[
     K \approx \frac{0.0265 \times N}{(IC \times (N - 1)) - (0.0385 \times N) + 0.065}
     \]
     де \( N \) — загальна кількість літер у тексті.

4. **Частотний аналіз**:
   - Функція `chi_squared_statistic` обчислює хі-квадрат статистику для порівняння частот букв у групі з очікуваними частотами англійської мови.
   - Функція `find_key_for_group` визначає символ ключа для кожної групи шляхом зсуву, який мінімізує хі-квадрат статистику.
   - Функція `find_key` агрегує символи ключа з усіх груп.

5. **Дешифрування**:
   - Функція `decrypt_vigenere` розшифровує текст за допомогою знайденого ключа, зберігаючи пробіли та розділові знаки без змін.

6. **Шифрування (для демонстрації)**:
   - Функція `vigenere_encrypt` використовується для шифрування тексту за допомогою шифру Віженера з відомим ключем "CRYPTOGRAPHY" для перевірки правильності роботи програми.

7. **Основна функція (`main`)**:
   - Вводить текст для шифрування.
   - Шифрує текст за допомогою шифру Віженера.
   - Виконує методи Касікі та Фрідмана для оцінки довжини ключа.
   - Визначає ключ за допомогою частотного аналізу.
   - Розшифровує текст за знайденим ключем.

# [Task 2.1 - Шифр перестановки, рівень 1](task2_1.py)
## Опис Табличного Шифру зі Стовпчиковою Транспозицією

**Табличний шифр зі стовпчиковою транспозицією** (Columnar Transposition Cipher) — це метод шифрування, який використовує ключове слово для перестановки символів тексту. Ключ визначає порядок, в якому стовпчики таблиці будуть читатися під час шифрування та дешифрування.

### Кроки Шифрування:
1. **Визначення порядку стовпчиків**:
   - Сортуємо букви ключа в алфавітному порядку.
   - Призначаємо кожній букві номер, який визначає порядок читання стовпчиків.
   - У випадку повторюваних букв, порядок визначається їхнім порядком появи у ключі.

2. **Запис тексту в таблицю**:
   - Записуємо текст по рядках у таблицю з кількістю стовпчиків, що дорівнює довжині ключа.
   - Зберігаємо пробіли та розділові знаки як звичайні символи.

3. **Читання стовпчиків у визначеному порядку**:
   - Зчитуємо текст стовпчиками відповідно до порядку, визначеного ключем, щоб сформувати зашифрований текст.

### Кроки Дешифрування:
1. **Визначення порядку стовпчиків**:
   - Використовуємо той самий порядок стовпчиків, що й при шифруванні.

2. **Розподіл зашифрованого тексту по стовпчиках**:
   - Розбиваємо зашифрований текст на стовпчики відповідно до порядку та довжини ключа.

3. **Відновлення оригінального тексту**:
   - Зчитуємо текст по рядках з таблиці, відновлюючи оригінальний текст.

## Лістинг

```python
import math

def generate_order(key):
    key = key.upper()
    sorted_key = sorted([(char, idx) for idx, char in enumerate(key)], key=lambda x: (x[0], x[1]))
    order = {}
    current_order = 1
    for char, idx in sorted_key:
        order[idx] = current_order
        current_order += 1
    ordered_columns = sorted(order, key=lambda x: order[x])
    return ordered_columns

def encrypt_columnar_transposition(plaintext, key):
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    ciphertext = [''] * key_length
    
    for idx, char in enumerate(plaintext):
        column = idx % key_length
        ciphertext[column] += char
    
    encrypted_text = ''.join([ciphertext[idx] for idx in order])
    
    return encrypted_text

def decrypt_columnar_transposition(ciphertext, key):
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    num_of_rows = math.ceil(len(ciphertext) / key_length)
    num_full_columns = len(ciphertext) % key_length
    
    column_lengths = {}
    for idx in order:
        if num_full_columns == 0 or idx < num_full_columns:
            column_lengths[idx] = num_of_rows
        else:
            column_lengths[idx] = num_of_rows - 1
    
    columns = {}
    pointer = 0
    for idx in order:
        length = column_lengths[idx]
        columns[idx] = ciphertext[pointer:pointer+length]
        pointer += length
    
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
    
    ciphertext = encrypt_columnar_transposition(plaintext, key)
    print(f"\nЗашифрований текст: {ciphertext}\n")
    
    decrypted_text = decrypt_columnar_transposition(ciphertext, key)
    print(f"Розшифрований текст: {decrypted_text}\n")

if __name__ == "__main__":
    main_level1()
```

## Пояснення до лістингу

1. **Функція `generate_order(key)`**:
    - Приймає ключове слово та перетворює його у верхній регістр.
    - Сортує букви ключа в алфавітному порядку, враховуючи їхні початкові індекси для повторюваних букв.
    - Призначає кожній букві порядковий номер відповідно до сортування.
    - Повертає список індексів стовпчиків у порядку їх читання.

2. **Функція `encrypt_columnar_transposition(plaintext, key)`**:
    - Перетворює ключ на верхній регістр та визначає порядок стовпчиків.
    - Створює список стовпчиків, де кожен стовпчик представляє собою рядок тексту.
    - Заповнює стовпчики символами тексту по рядках.
    - Зчитує стовпчики у визначеному порядку для формування зашифрованого тексту.
    - Зберігає пробіли та розділові знаки як звичайні символи.

3. **Функція `decrypt_columnar_transposition(ciphertext, key)`**:
    - Перетворює ключ на верхній регістр та визначає порядок стовпчиків.
    - Обчислює кількість рядків у таблиці та визначає, які стовпчики будуть мати на один символ більше (у випадку неповних рядків).
    - Розподіляє зашифрований текст по стовпчиках відповідно до порядку та довжини стовпчиків.
    - Відновлює оригінальний текст, зчитуючи символи по рядках з таблиці.
    - Зберігає пробіли та розділові знаки як звичайні символи.

4. **Функція `main_level1()`**:
    - Виводить заголовок рівня 1.
    - Приймає текст для шифрування від користувача.
    - Шифрує текст за допомогою табличного шифру зі стовпчиковою транспозицією з ключем "SECRET".
    - Виводить зашифрований текст.
    - Дешифрує зашифрований текст для перевірки правильності роботи алгоритму.
    - Виводить розшифрований текст.

## Детальніше про Порядок Стовпчиків

Для ключа "SECRET" порядок стовпчиків визначається наступним чином:

1. **Сортування Букв Ключа**:
   - Ключ: S, E, C, R, E, T
   - Сортування за алфавітом: C, E, E, R, S, T

2. **Призначення Порядкових Номерів**:
   - C (індекс 2) — 1
   - E (індекс 1) — 2
   - E (індекс 4) — 3
   - R (індекс 3) — 4
   - S (індекс 0) — 5
   - T (індекс 5) — 6

3. **Порядок Читання Стовпчиків**:
   - Перший стовпчик — C (індекс 2)
   - Другий стовпчик — E (індекс 1)
   - Третій стовпчик — E (індекс 4)
   - Четвертий стовпчик — R (індекс 3)
   - П'ятий стовпчик — S (індекс 0)
   - Шостий стовпчик — T (індекс 5)

Отже, порядок стовпчиків для шифрування: [2, 1, 4, 3, 0, 5]

## Висновок

Ця програма дозволяє ефективно шифрувати та дешифрувати текст за допомогою табличного шифру зі стовпчиковою транспозицією з ключем "SECRET", зберігаючи пробіли та розділові знаки.

# [Task 2.2 - Шифр перестановки, рівень 2](task2_2.py)
## Опис Подвійного Табличного Шифру зі Стовпчиковою Транспозицією

**Подвійний табличний шифр зі стовпчиковою транспозицією** — це метод шифрування, який використовує дві різні ключові фрази для двох послідовних перестановок тексту. Спочатку текст зашифровується першим ключем, а потім результат шифрується другим ключем.

### Кроки Шифрування:
1. **Перший Шифр (Ключ "SECRET")**:
   - Використовуємо табличний шифр зі стовпчиковою транспозицією з ключем "SECRET" для першої перестановки тексту.
2. **Другий Шифр (Ключ "CRYPTO")**:
   - Отриманий результат першого шифруємо ще раз за допомогою табличного шифру зі стовпчиковою транспозицією з ключем "CRYPTO".

### Кроки Дешифрування:
1. **Перший Дешифр (Ключ "CRYPTO")**:
   - Спочатку дешифруємо текст за допомогою табличного шифру зі стовпчиковою транспозицією з ключем "CRYPTO".
2. **Другий Дешифр (Ключ "SECRET")**:
   - Потім отриманий результат дешифруємо за допомогою табличного шифру зі стовпчиковою транспозицією з ключем "SECRET".

## Реалізація на Python

Нижче наведено повний Python код для **Рівня 2**, який реалізує подвійний табличний шифр зі стовпчиковою транспозицією з ключами "SECRET" та "CRYPTO".

### Основні Функції:

1. **`generate_order(key)`**: Визначає порядок стовпчиків на основі ключа.
2. **`encrypt_columnar_transposition(plaintext, key)`**: Шифрує текст за допомогою стовпчикової транспозиції.
3. **`decrypt_columnar_transposition(ciphertext, key)`**: Дешифрує текст за допомогою стовпчикової транспозиції.
4. **`double_transposition_encrypt(plaintext, key1, key2)`**: Виконує подвійне шифрування.
5. **`double_transposition_decrypt(ciphertext, key1, key2)`**: Виконує подвійне дешифрування.

### Лістинг:

```python
import math

def generate_order(key):
    key = key.upper()

    key_letters = list(key)
    indexed_key = list(enumerate(key_letters))
    sorted_key = sorted(indexed_key, key=lambda x: (x[1], x[0]))
    order = [idx for idx, char in sorted_key]
    return order

def encrypt_columnar_transposition(plaintext, key):
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    ciphertext = [''] * key_length
    
    for idx, char in enumerate(plaintext):
        column = idx % key_length
        ciphertext[column] += char
    
    encrypted_text = ''.join([ciphertext[idx] for idx in order])
    
    return encrypted_text

def decrypt_columnar_transposition(ciphertext, key):
    key = key.upper()
    order = generate_order(key)
    key_length = len(key)
    num_of_rows = math.ceil(len(ciphertext) / key_length)
    num_full_columns = len(ciphertext) % key_length
    
    column_lengths = {}
    for idx in order:
        if num_full_columns == 0 or idx < num_full_columns:
            column_lengths[idx] = num_of_rows
        else:
            column_lengths[idx] = num_of_rows - 1
    
    columns = {}
    pointer = 0
    for idx in order:
        length = column_lengths[idx]
        columns[idx] = ciphertext[pointer:pointer+length]
        pointer += length
    
    plaintext = ''
    for i in range(num_of_rows):
        for j in range(key_length):
            if i < len(columns[j]):
                plaintext += columns[j][i]
    
    return plaintext

def double_transposition_encrypt(plaintext, key1, key2):

    first_encryption = encrypt_columnar_transposition(plaintext, key1)
    second_encryption = encrypt_columnar_transposition(first_encryption, key2)
    return second_encryption

def double_transposition_decrypt(ciphertext, key1, key2):
    first_decryption = decrypt_columnar_transposition(ciphertext, key2)
    second_decryption = decrypt_columnar_transposition(first_decryption, key1)
    return second_decryption

def main_level2():
    print("=== Рівень 2: Подвійний табличний шифр зі стовпчиковою транспозицією ===\n")
    
    key1 = "SECRET"
    key2 = "CRYPTO"
    print(f"Перший ключ (для першої транспозиції): {key1}")
    print(f"Другий ключ (для другої транспозиції): {key2}\n")
    
    plaintext = input("Введіть текст для шифрування: ")
    
    ciphertext = double_transposition_encrypt(plaintext, key1, key2)
    print(f"\nЗашифрований текст після подвійної транспозиції: {ciphertext}\n")
    
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
        
        ciphertext = encrypt_columnar_transposition(plaintext, key)
        print(f"\nЗашифрований текст: {ciphertext}\n")
        
        decrypted_text = decrypt_columnar_transposition(ciphertext, key)
        print(f"Розшифрований текст: {decrypted_text}\n")
    
    elif choice == '2':
        main_level2()
    else:
        print("Невірний вибір. Завершення програми.")

if __name__ == "__main__":
    main()
```

## Пояснення до лістингу:

1. **Функція `generate_order(key)`**:
   - Приймає ключове слово та перетворює його в верхній регістр.
   - Створює список букв з їхніми індексами.
   - Сортує букви ключа в алфавітному порядку, враховуючи їхні початкові індекси для повторюваних букв.
   - Призначає кожній букві порядковий номер відповідно до сортування.
   - Повертає список індексів стовпчиків у порядку їх читання.

2. **Функція `encrypt_columnar_transposition(plaintext, key)`**:
   - Перетворює ключ на верхній регістр та визначає порядок стовпчиків.
   - Створює список стовпчиків, де кожен стовпчик представляє собою рядок тексту.
   - Заповнює стовпчики символами тексту по рядках.
   - Зчитує стовпчики у визначеному порядку для формування зашифрованого тексту.
   - Зберігає пробіли та розділові знаки як звичайні символи.

3. **Функція `decrypt_columnar_transposition(ciphertext, key)`**:
   - Перетворює ключ на верхній регістр та визначає порядок стовпчиків.
   - Обчислює кількість рядків у таблиці та визначає, які стовпчики будуть мати на один символ більше (у випадку неповних рядків).
   - Розподіляє зашифрований текст по стовпчиках відповідно до порядку та довжини стовпчиків.
   - Відновлює оригінальний текст, зчитуючи символи по рядках з таблиці.
   - Зберігає пробіли та розділові знаки як звичайні символи.

4. **Функція `double_transposition_encrypt(plaintext, key1, key2)`**:
   - Виконує шифрування тексту двома послідовними транспозиціями: спочатку з ключем `key1`, потім з ключем `key2`.

5. **Функція `double_transposition_decrypt(ciphertext, key1, key2)`**:
   - Виконує дешифрування тексту двома послідовними транспозиціями: спочатку з ключем `key2`, потім з ключем `key1`.

6. **Функція `main_level2()`**:
   - Виводить заголовок рівня 2.
   - Приймає текст для шифрування від користувача.
   - Виконує подвійне шифрування за допомогою ключів "SECRET" та "CRYPTO".
   - Виводить зашифрований текст після подвійної транспозиції.
   - Виконує дешифрування зашифрованого тексту, відновлюючи оригінальний текст.
   - Виводить розшифрований текст.

7. **Функція `main()`**:
   - Запитує у користувача вибір рівня (1 або 2).
   - Викликає відповідну функцію для обробки вибору.


## Детальніше про Порядок Стовпчиків

#### Ключ "SECRET"

1. **Сортування Букв Ключа**:
   - Ключ: S, E, C, R, E, T
   - Сортування за алфавітом: C, E, E, R, S, T

2. **Призначення Порядкових Номерів**:
   - C (індекс 2) — 1
   - E (індекс 1) — 2
   - E (індекс 4) — 3
   - R (індекс 3) — 4
   - S (індекс 0) — 5
   - T (індекс 5) — 6

3. **Порядок Читання Стовпчиків**:
   - Перший стовпчик — C (індекс 2)
   - Другий стовпчик — E (індекс 1)
   - Третій стовпчик — E (індекс 4)
   - Четвертий стовпчик — R (індекс 3)
   - П'ятий стовпчик — S (індекс 0)
   - Шостий стовпчик — T (індекс 5)

#### Ключ "CRYPTO"

1. **Сортування Букв Ключа**:
   - Ключ: C, R, Y, P, T, O
   - Сортування за алфавітом: C, O, P, R, T, Y

2. **Призначення Порядкових Номерів**:
   - C (індекс 0) — 1
   - O (індекс 5) — 2
   - P (індекс 3) — 3
   - R (індекс 1) — 4
   - T (індекс 4) — 5
   - Y (індекс 2) — 6

3. **Порядок Читання Стовпчиків**:
   - Перший стовпчик — C (індекс 0)
   - Другий стовпчик — O (індекс 5)
   - Третій стовпчик — P (індекс 3)
   - Четвертий стовпчик — R (індекс 1)
   - П'ятий стовпчик — T (індекс 4)
   - Шостий стовпчик — Y (індекс 2)

### Важливі Моменти для Коректної Роботи:

1. **Збереження Пробілів та Розділових Знаків**:
   - У цій реалізації пробіли та розділові знаки розглядаються як звичайні символи та включаються у шифр та дешифрований текст.

2. **Коректність Сортування Ключа**:
   - Сортування ключа враховує як алфавітний порядок букв, так і їхні початкові індекси для обробки повторюваних букв.

3. **Обробка Неповних Рядків**:
   - При дешифруванні враховується, що деякі стовпчики можуть мати на один символ менше, ніж інші, якщо довжина тексту не кратна довжині ключа.

4. **Гнучкість Ключів**:
   - Ви можете змінювати ключі "SECRET" та "CRYPTO" на будь-які інші ключові фрази, враховуючи, що ключ має бути без пробілів та розділових знаків.


## Висновок

Ця програма дозволяє ефективно шифрувати та дешифрувати текст за допомогою подвійного табличного шифру зі стовпчиковою транспозицією, використовуючи ключі "SECRET" та "CRYPTO". Програма зберігає пробіли та розділові знаки, а також правильно обробляє повторювані букви у ключах.

# [Task 3.1 - Табличний шифр, рівень 1](task3_1.py)
## Табличний шифр зі стовпчиковою транспозицією з ключем "MATRIX"
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


### Основні функції:

1. **`generate_order(key)`**: Визначає порядок стовпчиків на основі ключа.
2. **`encrypt_columnar_transposition(plaintext, key)`**: Шифрує текст за допомогою стовпчикової транспозиції.
3. **`decrypt_columnar_transposition(ciphertext, key)`**: Дешифрує текст за допомогою стовпчикової транспозиції.

### Лістинг:

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

### Пояснення до лістингу:

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


# [Task 3.2 - Табличний шифр, рівень 2](task3_2.py)
## Рівень 2: Подвійне шифрування (Віженер, потім Табличний шифр)

### Опис завдання

Зашифруємо текст спочатку за допомогою **шифру Віженера** з ключем "CRYPTO", а потім отриманий результат зашифруємо за допомогою **стовпчикової транспозиції** з ключем "CRYPTO".

### Основні функції:

1. **`vigenere_encrypt(plaintext, key)`**: Шифрує текст за допомогою шифру Віженера.
2. **`vigenere_decrypt(ciphertext, key)`**: Дешифрує текст за допомогою шифру Віженера.
3. **`encrypt_columnar_transposition(plaintext, key)`**: Шифрує текст за допомогою стовпчикової транспозиції.
4. **`decrypt_columnar_transposition(ciphertext, key)`**: Дешифрує текст за допомогою стовпчикової транспозиції.

### Лістинг:

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

### Пояснення до лістингу:

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