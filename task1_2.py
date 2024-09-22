from collections import Counter

# Функція для тесту Фрідмана
def friedman_test(cipher_text):
    cipher_text = ''.join([c for c in cipher_text if c.isalpha()])  # Видаляємо пробіли та неалфавітні символи
    N = len(cipher_text)
    freq = Counter(cipher_text)
    
    # Обчислюємо індекс відповідності
    ic = sum([f * (f - 1) for f in freq.values()]) / (N * (N - 1))
    
    # Очікуваний індекс для випадкового тексту
    ic_random = 1 / 26
    # Очікуваний індекс для англійської мови
    ic_english = 0.068
    
    # Оцінка довжини ключа
    key_length_estimate = (ic_english - ic_random) / (ic - ic_random)
    
    return round(key_length_estimate)

# Функція для розбиття тексту на групи за довжиною ключа
def group_text_by_key_length(cipher_text, key_length):
    groups = [''] * key_length
    for i, char in enumerate(cipher_text):
        if char.isalpha():
            groups[i % key_length] += char
    return groups

# Функція для знаходження найімовірніших літер ключа за допомогою частотного аналізу
def find_key_by_frequency(groups):
    # Найчастіша літера в англійській мові - 'E', зрушення на основі цього
    most_frequent_letter = 'E'
    key = ''
    
    for group in groups:
        freq = Counter(group)
        most_common = freq.most_common(1)[0][0]  # Найчастіша літера в групі
        # Визначаємо зсув для кожної групи
        shift = (ord(most_common.upper()) - ord(most_frequent_letter)) % 26
        key += chr(shift + ord('A'))
    
    return key

# Функція для дешифрування тексту
def decrypt_vigenere(cipher_text, key):
    original_text = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    cipher_text_as_int = [ord(i) for i in cipher_text]
    
    for i in range(len(cipher_text_as_int)):
        if cipher_text[i].isalpha():
            value = (cipher_text_as_int[i] - key_as_int[i % key_length]) % 26
            original_text.append(chr(value + ord('A')))
        else:
            original_text.append(cipher_text[i])  # Неалфавітні символи залишаємо незмінними
    
    return ''.join(original_text)

# Основна програма
cipher_text = input("Введіть зашифрований текст: ").upper()
cipher_text = ''.join([c for c in cipher_text if c.isalpha() or c == ' '])  # Очищаємо текст

# Крок 1: Оцінюємо довжину ключа
estimated_key_length = friedman_test(cipher_text)
print(f"Оцінена довжина ключа: {estimated_key_length}")

# Крок 2: Розбиваємо текст на групи за довжиною ключа
groups = group_text_by_key_length(cipher_text, estimated_key_length)

# Крок 3: Знаходимо ключ за допомогою частотного аналізу
found_key = find_key_by_frequency(groups)
print(f"Знайдений ключ: {found_key}")

# Крок 4: Дешифруємо текст з використанням знайденого ключа
decrypted_text = decrypt_vigenere(cipher_text, found_key)
print(f"Розшифрований текст: {decrypted_text}")
