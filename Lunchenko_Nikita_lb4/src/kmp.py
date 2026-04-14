def kmp_search(pattern, text):
    if not pattern:
        return []

    m = len(pattern)
    pi = [0] * m
    j = 0

    print("Выполнение префикс функции")
    for i in range(1, m):
        print(f"Итерация i = {i} (символ '{pattern[i]}')")
        while j > 0 and pattern[i] != pattern[j]:
            print(f"{i}-й элемент - {pattern[i]} не равен {j}-му  элементу - {pattern[j]}")
            j = pi[j-1]
            print(f"Откат j с {j} на pi[{j-1}] = {pi[j-1]}")
        if pattern[i] == pattern[j]:
            print(f"{i}-й элемент - {pattern[i]} равен {j}-му  элементу - {pattern[j]}")
            j += 1
        pi[i] = j
    print(f"Префикс функци - {pi}")
    result = []
    j = 0
    print("Поиск вхождений")
    for i in range(len(text)):
        print(f"Итерация i = {i} (символ текста '{text[i]}')\nj = {j}")

        while j > 0 and text[i] != pattern[j]:
            print(f"Несовпадение: text[{i}]='{text[i]}' != pattern[{j}]='{pattern[j]}'")
            j = pi[j - 1]

        if text[i] == pattern[j]:
            print(f"Совпадение: text[{i}]='{text[i]}' == pattern[{j}]='{pattern[j]}'")
            j += 1

        if j == m:
            print(f"Вхождение на позиции: {i - m + 1}")
            result.append(i - m + 1)
            j = pi[j - 1]

    return result

pattern = input()
text = input()

occurrences = kmp_search(pattern, text)

if occurrences:
    print(','.join(map(str, occurrences)))
else:
    print(-1)
