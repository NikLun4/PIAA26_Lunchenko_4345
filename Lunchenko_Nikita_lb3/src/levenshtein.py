def levenshtein_distance(s1, s2):
    n, m = len(s1), len(s2)

    dp = [[0] * (m + 1) for i in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = i
        print(f"Для ячейки {i}, 0, лучший результат ячейка {i-1}, 0 + удаление")
    for j in range(1, m + 1):
        dp[0][j] = j
        print(f"Для ячейки 0, {j}, лучший результат ячейка {0}, {j-1} + вставка")
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            delete_cost = dp[i - 1][j] + 1
            insert_cost = dp[i][j - 1] + 1
            replace_cost = dp[i - 1][j - 1] + cost

            dp[i][j] = min(delete_cost, insert_cost, replace_cost)
            if delete_cost == dp[i][j]:
                print(f"Для ячейки {i}, {j}, лучший результат ячейка {i-1}, {j} + удаление")
            elif insert_cost == dp[i][j]:
                print(f"Для ячейки {i}, {j}, лучший результат ячейка {i}, {j-1} + вставка")
            elif cost == 0:
                print(f"{s1[i-1]} = {s2[j-1]}, ячейка {i}, {j} = {i-1}, {j-1} ")
            else:
                print(f"Для ячейки {i}, {j}, лучший результат ячейка {i-1}, {j-1} + замена")

    for i in dp:
        print(i)
    return dp

def v_11():
    A = input().strip()
    B = input().strip()

    n, m = len(A), len(B)
    dp = levenshtein_distance(A, B)

    min_prefix_dist = float('inf')
    best_prefixes = []

    for i in range(n + 1):
        dist = dp[i][m]
        prefix = A[:i]

        if dist < min_prefix_dist:
            min_prefix_dist = dist
            best_prefixes = [prefix]
        elif dist == min_prefix_dist:
            best_prefixes.append(prefix)

    print(f"Минимальное расстояние: {min_prefix_dist}")
    print(f"Префиксы с минимальным расстоянием:")
    for p in best_prefixes:
        print(f"  '{p}'" if p else "  (пустая строка)")

    A_rev = A[::-1]
    B_rev = B[::-1]

    dp_rev = levenshtein_distance(A_rev, B_rev)

    min_suffix_dist = float('inf')
    best_suffixes = []

    for length in range(n + 1):
        dist = dp_rev[length][m]
        suffix = A[n - length:] if length > 0 else ""

        if dist < min_suffix_dist:
            min_suffix_dist = dist
            best_suffixes = [suffix]
        elif dist == min_suffix_dist:
            best_suffixes.append(suffix)

    print(f"Минимальное расстояние: {min_suffix_dist}")
    print(f"Суффиксы с минимальным расстоянием:")
    for s in best_suffixes:
        print(f"  '{s}'" if s else "  (пустая строка)")

if __name__ == "__main__":
    v_11()
