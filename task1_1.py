# Функція для генерації ключа, що збігається за довжиною з текстом
def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return ''.join(key)

# Функція для шифрування тексту
def encrypt(text, key):
    cipher_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            # Перетворення символів у верхній регістр
            x = (ord(text[i].upper()) + ord(key[i])) % 26
            x += ord('A')
            cipher_text.append(chr(x))
        else:
            cipher_text.append(text[i])  # Залишаємо неалфавітні символи
    return ''.join(cipher_text)

# Функція для дешифрування тексту
def decrypt(cipher_text, key):
    original_text = []
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
            x += ord('A')
            original_text.append(chr(x))
        else:
            original_text.append(cipher_text[i])  # Залишаємо неалфавітні символи
    return ''.join(original_text)

# Основна програма
text = input("Введіть текст для шифрування: ")
key = "CRYPTOGRAPHY"

# Генерація ключа на основі введеного тексту
generated_key = generate_key(text, key)

# Шифрування тексту
cipher_text = encrypt(text, generated_key)
print(f"Зашифрований текст: {cipher_text}")

# Дешифрування тексту
decrypted_text = decrypt(cipher_text, generated_key)
print(f"Розшифрований текст: {decrypted_text}")
