import string
from collections import Counter
from math import gcd
from functools import reduce

# Частотні дані для англійської мови
ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def find_repeated_sequences_spacings(ciphertext, sequence_length=3):
    """
    Знаходить повторювані послідовності символів та їх відстані у шифротексті.
    """
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
    """
    Виконує метод Касікі для оцінки довжини ключа.
    """
    spacings = find_repeated_sequences_spacings(ciphertext, sequence_length)
    if not spacings:
        return None
    # Обчислюємо GCD усіх відстаней
    gcd_all = reduce(gcd, spacings)
    return gcd_all

def friedman_test(ciphertext):
    """Обчислює індекс відповідності (IC) для всього тексту."""
    filtered_text = [c.upper() for c in ciphertext if c.isalpha()]
    N = len(filtered_text)
    if N <= 1:
        return 0

    freq = Counter(filtered_text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

def estimate_key_length_friedman(ciphertext):
    """Визначає ймовірну довжину ключа за методом Фрідмана."""
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
    """Отримує можливі довжини ключа за методами Касікі та Фрідмана."""
    key_length_kasiski = kasiski_examination(ciphertext)
    key_length_friedman = estimate_key_length_friedman(ciphertext)
    possible_lengths = []
    if key_length_kasiski and 1 < key_length_kasiski <= 20:
        possible_lengths.append(key_length_kasiski)
    possible_lengths.append(key_length_friedman)
    # Додамо також найбільш ймовірні ключові довжини біля оцінених значень
    for length in range(1,4):
        if 1 <= (key_length_friedman - length) <= 20:
            possible_lengths.append(key_length_friedman - length)
        if 1 <= (key_length_friedman + length) <= 20:
            possible_lengths.append(key_length_friedman + length)
    # Фільтруємо довжини ключа, щоб вони були в межах 1 і 20
    possible_lengths = [k for k in possible_lengths if 1 <= k <= 20]
    # Видаляємо дублікати
    possible_lengths = sorted(set(possible_lengths))
    return possible_lengths

def split_into_groups(ciphertext, key_length):
    """Розбиває текст на групи відповідно до довжини ключа."""
    groups = ['' for _ in range(key_length)]
    index = 0
    for char in ciphertext:
        if char.isalpha():
            groups[index % key_length] += char.upper()
            index += 1
    return groups

def chi_squared_statistic(counter, total):
    """Обчислює статистику хі-квадрат для заданого підрахунку частот."""
    chi2 = 0.0
    for letter in string.ascii_uppercase:
        observed = counter.get(letter, 0)
        expected = ENGLISH_FREQ.get(letter, 0) * total
        chi2 += ((observed - expected) ** 2) / expected if expected > 0 else 0
    return chi2

def find_key_for_group(group):
    """Визначає символ ключа для окремої групи за допомогою хі-квадрат статистики."""
    total = len(group)
    if total == 0:
        return 'A'  # Припускаємо зсув 0, якщо група порожня
    counter = Counter(group)
    min_chi2 = float('inf')
    best_shift = 0
    for shift in range(26):
        # Зсуваємо всі літери в групі на 'shift' назад
        decrypted = ''.join([chr((ord(c) - 65 - shift) % 26 + 65) for c in group])
        decrypted_counter = Counter(decrypted)
        chi2 = chi_squared_statistic(decrypted_counter, total)
        if chi2 < min_chi2:
            min_chi2 = chi2
            best_shift = shift
    return chr(best_shift + 65)

def find_key(groups):
    """Визначає ключ за допомогою частотного аналізу з використанням хі-квадрат статистики."""
    key = ''
    for group in groups:
        key += find_key_for_group(group)
    return key

def decrypt_vigenere(ciphertext, key):
    """Дешифрує текст за допомогою шифру Віженера, зберігаючи пробіли та розділові знаки."""
    decrypted = []
    key_length = len(key)
    key_int = [ord(k) - 65 for k in key.upper()]
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = key_int[key_index % key_length]
            decrypted_char = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
            # Збереження оригінального регістру
            decrypted.append(decrypted_char if char.isupper() else decrypted_char.lower())
            key_index += 1
        else:
            decrypted.append(char)  # Зберігаємо пробіли та розділові знаки
    return ''.join(decrypted)

def vigenere_encrypt(plaintext, key):
    """Шифрує текст за допомогою шифру Віженера."""
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
            encrypted.append(char)  # Зберігаємо пробіли та розділові знаки
    return ''.join(encrypted)

def main():
    # Введення тексту для шифрування
    plaintext = input("Введіть текст для шифрування: ")

    # Ключ для шифрування
    vigenere_key = "CRYPTOGRAPHY"

    # Шифрування тексту за допомогою шифру Віженера
    ciphertext = vigenere_encrypt(plaintext, vigenere_key)
    print(f"\nЗашифрований текст: {ciphertext}\n")

    # Введення зашифрованого тексту для дешифрування
    # Якщо ви хочете дешифрувати власний текст, закоментуйте рядок шифрування та розкоментуйте нижче:
    # ciphertext = input("Введіть зашифрований текст: ")

    # Крок 1: Оцінка довжини ключа за методами Касікі та Фрідмана
    possible_key_lengths = get_possible_key_lengths(ciphertext)
    print(f"Можливі довжини ключа: {possible_key_lengths}")

    # Крок 2: Оцінка ключа для кожної можливої довжини та вибір найкращого
    best_key = None
    best_chi2 = float('inf')
    best_decrypted = ''

    for key_length in possible_key_lengths:
        groups = split_into_groups(ciphertext, key_length)
        found_key = find_key(groups)
        decrypted_text = decrypt_vigenere(ciphertext, found_key)
        # Compute average chi-squared for the key
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
        # Keep the key with the lowest average chi2
        if average_chi2 < best_chi2:
            best_chi2 = average_chi2
            best_key = found_key
            best_decrypted = decrypted_text

    print(f"Оцінена довжина ключа: {len(best_key)}")
    print(f"Знайдений ключ: {best_key}")
    print(f"\nРозшифрований текст:\n{best_decrypted}")

if __name__ == "__main__":
    main()
