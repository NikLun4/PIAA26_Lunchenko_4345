def build_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m

    j = 0
    print("Выполнение префикс-функции для pattern =", pattern)
    for i in range(1, m):
        print(f"Итерация i = {i} (символ '{pattern[i]}')")
        while j > 0 and pattern[i] != pattern[j]:
            print(f"  {i}-й элемент - '{pattern[i]}' не равен {j}-му элементу - '{pattern[j]}'")
            j = pi[j - 1]
            print(f"  Откат j = {j}")
        if pattern[i] == pattern[j]:
            print(f"  {i}-й элемент - '{pattern[i]}' равен {j}-му элементу - '{pattern[j]}'")
            j += 1
        pi[i] = j
    print(f"Префикс-функция: {pi}\n")
    return pi

def kmp_search(pattern, text):
    if not pattern or not text:
        return []

    pi = build_prefix_function(pattern)
    print(pi)
    result = []
    j = 0

    print(f"Поиск вхождений {pattern} в {text}:")
    for i in range(len(text)):
        print(f"Итерация i = {i} (символ текста '{text[i]}')\n j = {j}")

        while j > 0 and text[i] != pattern[j]:
            print(f"  Несовпадение: text[{i}]='{text[i]}' != pattern[{j}]='{pattern[j]}'")
            j = pi[j - 1]

        if text[i] == pattern[j]:
            print(f"  Совпадение: text[{i}]='{text[i]}' == pattern[{j}]='{pattern[j]}'")
            j += 1

        if j == len(pattern):
            print(f"Вхождение на позиции: {i - len(pattern) + 1}")
            result.append(i - len(pattern) + 1)
            j = pi[j - 1]

    return result

def find_cyclic_shift(A, B):
    if len(A) != len(B):
        return -1

    n = len(A)

    if n == 0:
        return 0
    double_B = B + B
    occurrences = kmp_search(A, double_B)

    for pos in occurrences:
        if pos < n:
            return pos

    return -1

A = input()
B = input()

result = find_cyclic_shift(A, B)
print(result)
