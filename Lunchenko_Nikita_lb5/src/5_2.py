class AhoCorasick:
    def __init__(self):
        self.next = [{}]
        self.fail = [0]
        self.term = [-1]
        self.out = [[]]
        self.vertices = 1

    def add_pattern(self, pattern, pattern_id):
        print(f"\nДобавление подобразца '{pattern}' (ID={pattern_id + 1})")

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
        print(f"  Подобразец {pattern_id + 1} заканчивается в вершине {v}")

    def build_automaton(self):
        print(f"\nПОСТРОЕНИЕ АВТОМАТА")
        print(f"Начальный бор: {self.next}")
        print(f"Количество вершин в боре: {self.vertices}")

        queue = []

        print(f"\nИнициализация суффиксных ссылок для детей корня:")
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

        print(f"\nПОСТРОЕННЫЙ АВТОМАТ:")
        for i in range(self.vertices):
            print(f"Вершина {i}:")
            print(f"  Переходы: {self.next[i]}")
            print(f"  Суффиксная ссылка: {self.fail[i]}")
            print(f"  Терминальная ссылка: {self.term[i]}")
            print(f"  Выходные подобразцы: {[p + 1 for p in self.out[i]]}")

    def get_next(self, v, ch):
        if ch not in self.next[v]:
            if v == 0:
                self.next[v][ch] = 0
            else:
                self.next[v][ch] = self.get_next(self.fail[v], ch)
        return self.next[v][ch]

    def search(self, text, subpatterns):
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
                        pattern_len = len(subpatterns[pattern_id])
                        pos = i - pattern_len + 1
                        print(f"    Найден подобразец {pattern_id + 1} на позиции {pos}")
                        results.append((pos, pattern_id))
                print(f"    Переход по term[{u}] = {self.term[u]}")
                u = self.term[u]

        return results


def solve_with_wildcard(text, pattern, wildcard):
    print(f"\nПОИСК С ДЖОКЕРОМ")
    print(f"Текст: '{text}'")
    print(f"Образец: '{pattern}'")
    print(f"Символ джокера: '{wildcard}'")

    if pattern.count(wildcard) == len(pattern):
        print("Ошибка: образец состоит только из джокеров")
        return

    subpatterns = []
    positions = []

    current = ""
    start_pos = None

    print(f"\nРАЗБИЕНИЕ ОБРАЗЦА НА ПОДОБРАЗЦЫ:")
    for i, ch in enumerate(pattern):
        if ch != wildcard:
            if current == "":
                start_pos = i
            current += ch
        else:
            if current != "":
                subpatterns.append(current)
                positions.append(start_pos)
                print(f"   Подобразец '{current}' на позиции {start_pos} в образце")
                current = ""

    if current != "":
        subpatterns.append(current)
        positions.append(start_pos)
        print(f"   Подобразец '{current}' на позиции {start_pos} в образце")

    print(f"\nВсего подобразцов: {len(subpatterns)}")
    print(f"Подобразцы: {subpatterns}")
    print(f"Их позиции в образце: {positions}")

    if len(subpatterns) == 0:
        print("Ошибка: нет подобразцов без джокеров")
        return

    ac = AhoCorasick()
    for i, sp in enumerate(subpatterns):
        ac.add_pattern(sp, i)
    ac.build_automaton()

    occurrences = ac.search(text, subpatterns)

    pattern_len = len(pattern)
    text_len = len(text)
    counter = [0] * (text_len + 1)

    print(f"\nПРОВЕРКА СОВПАДЕНИЙ ОБРАЗЦА С ДЖОКЕРАМИ")
    print(f"Длина образца: {pattern_len}")
    print(f"Необходимо найти все {len(subpatterns)} подобразцов на правильных позициях")

    results = []

    for pos, pat_id in occurrences:
        start = pos - positions[pat_id]
        print(f"\nПодобразец {pat_id + 1} найден на позиции {pos}")
        print(f"  Позиция в образце: {positions[pat_id]}")
        print(f"  Предполагаемое начало образца: {start}")

        if start >= 0 and start + pattern_len <= text_len:
            counter[start] += 1
            print(f"  Счетчик совпадений для позиции {start + 1}: {counter[start]}/{len(subpatterns)}")

            if counter[start] == len(subpatterns):
                print(f"  НАЙДЕНО ПОЛНОЕ СОВПАДЕНИЕ на позиции {start + 1}")
                results.append(start + 1)
        else:
            print(f"  Выход за границы текста")

    print(f"\nИТОГОВЫЕ ПОЗИЦИИ ВХОЖДЕНИЙ:")
    if results:
        for pos in results:
            print(pos)
    else:
        print("Вхождения не найдены")


if __name__ == "__main__":
    text = input().strip()
    pattern = input().strip()
    wildcard = input().strip()

    solve_with_wildcard(text, pattern, wildcard)