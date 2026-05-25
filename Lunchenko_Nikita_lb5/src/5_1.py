class AhoCorasick:
    def __init__(self):
        self.next = [{}]
        self.fail = [0]
        self.term = [-1]
        self.out = [[]]
        self.vertices = 1

    def add_pattern(self, pattern, pattern_id):
        print(f"\nДобавление образца '{pattern}' (ID={pattern_id + 1})")

        v = 0
        for i, ch in enumerate(pattern):
            print(f"  Текущая вершина: {v}, символ: '{ch}'")
            if ch not in self.next[v]:
                new_vertex = self.vertices
                self.next[v][ch] = new_vertex
                self.next.append({})
                self.fail.append(0)
                self.term.append(-1)
                self.out.append([])
                self.vertices += 1
                print(f"    Создана новая вершина {new_vertex}")
            else:
                print(f"    Переход по существующему ребру в вершину {self.next[v][ch]}")
            v = self.next[v][ch]

        self.out[v].append(pattern_id)
        print(f"  Образец {pattern_id + 1} заканчивается в вершине {v}")
        print(f"  Текущий бор: {self.next}")

    def build_automaton(self):
        print(f"\nПОСТРОЕНИЕ АВТОМАТА")
        print(f"Начальный бор: {self.next}")
        print(f"Количество вершин в боре: {self.vertices}")

        queue = []

        print(f"\n1. Инициализация суффиксных ссылок для детей корня:")
        for ch, nxt in self.next[0].items():
            self.fail[nxt] = 0
            queue.append(nxt)
            print(f"   Вершина {nxt}: fail = 0 (корень)")

        head = 0
        print(f"\nBFS построение суффиксных и конечных ссылок:")
        while head < len(queue):
            v = queue[head]
            head += 1
            print(f"\n   Обработка вершины {v}:")
            print(f"     Исходящие ребра: {self.next[v]}")

            for ch, nxt in self.next[v].items():
                print(f"     Символ '{ch}' -> вершина {nxt}:")

                f = self.fail[v]
                print(f"       Поиск суффиксной ссылки, начиная с fail[{v}] = {f}")

                while f > 0 and ch not in self.next[f]:
                    print(f"         Переход по fail[{f}] = {self.fail[f]}")
                    f = self.fail[f]

                if ch in self.next[f]:
                    self.fail[nxt] = self.next[f][ch]
                    print(f"       Найдено: fail[{nxt}] = {self.fail[nxt]}")
                else:
                    self.fail[nxt] = 0
                    print(f"       Не найдено: fail[{nxt}] = 0 (корень)")

                if self.out[self.fail[nxt]]:
                    self.term[nxt] = self.fail[nxt]
                    print(f"       Терминальная ссылка: term[{nxt}] = {self.term[nxt]} (выход в fail)")
                else:
                    self.term[nxt] = self.term[self.fail[nxt]]
                    print(f"       Терминальная ссылка: term[{nxt}] = {self.term[nxt]} (наследована)")

                queue.append(nxt)

        print(f"\n3. ПОСТРОЕННЫЙ АВТОМАТ:")
        for i in range(self.vertices):
            print(f"Вершина {i}:")
            print(f"  Переходы: {self.next[i]}")
            print(f"  Суффиксная ссылка: {self.fail[i]}")
            print(f"  Терминальная ссылка: {self.term[i]}")
            print(f"  Выходные образцы: {[p + 1 for p in self.out[i]]}")

    def get_next(self, v, ch):
        if ch not in self.next[v]:
            if v == 0:
                self.next[v][ch] = 0
            else:
                self.next[v][ch] = self.get_next(self.fail[v], ch)
        return self.next[v][ch]

    def search(self, text, patterns):
        print(f"\nПРОЦЕСС ПОИСКА В ТЕКСТЕ: '{text}'")

        results = []
        v = 0
        print(f"Начальное состояние: вершина {v}")

        for i, ch in enumerate(text):
            print(f"\nПозиция {i + 1}, символ '{ch}':")
            v = self.get_next(v, ch)
            print(f"  Переход в вершину: {v}")
            u = v

            if u > 0:
                print(f"  Проверка терминальных вершин:")

            while u > 0:
                if self.out[u]:
                    for pattern_id in self.out[u]:
                        pattern_len = len(patterns[pattern_id])
                        pos = i - pattern_len + 1
                        end_pos = i
                        print(f"    Найден образец {pattern_id + 1} на позиции {pos + 1}-{end_pos + 1}")
                        results.append((pos + 1, pattern_id + 1, pos, end_pos))
                print(f"    Переход по term[{u}] = {self.term[u]}")
                u = self.term[u]

        return results


def find_overlapping(results):
    print(f"\nАНАЛИЗ ПЕРЕСЕЧЕНИЙ:")
    overlapping = set()

    for i in range(len(results)):
        pos1, pat_id1, start1, end1 = results[i]
        for j in range(i + 1, len(results)):
            pos2, pat_id2, start2, end2 = results[j]

            if pat_id1 == pat_id2:
                continue

            if not (end1 < start2 or end2 < start1):
                print(
                    f"  Пересечение: образец {pat_id1} (поз.{pos1}-{end1 + 1}) и образец {pat_id2} (поз.{pos2}-{end2 + 1})")
                overlapping.add((pos1, pat_id1))
                overlapping.add((pos2, pat_id2))

    return sorted(overlapping)


if __name__ == "__main__":
    text = input().strip()
    n = int(input())
    patterns = []

    ac = AhoCorasick()

    for i in range(n):
        pattern = input().strip()
        patterns.append(pattern)
        ac.add_pattern(pattern, i)

    ac.build_automaton()

    print(f"Количество вершин в автомате: {ac.vertices}")

    results = ac.search(text, patterns)

    results.sort(key=lambda x: (x[0], x[1]))

    print(f"\nВСЕ НАЙДЕННЫЕ ВХОЖДЕНИЯ:")
    for pos, pat_id, _, _ in results:
        print(f"Позиция {pos}, образец {pat_id}: {patterns[pat_id - 1]}")

    overlapping = find_overlapping(results)

    print(f"\nОБРАЗЦЫ, ИМЕЮЩИЕ ПЕРЕСЕЧЕНИЯ:")
    if overlapping:
        for pos, pat_id in overlapping:
            print(f"Позиция {pos}, образец {pat_id}: {patterns[pat_id - 1]}")
    else:
        print("Пересекающиеся образцы не найдены")