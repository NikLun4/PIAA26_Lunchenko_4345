import matplotlib.pyplot as plt
import time
import numpy as np


class Square:
    def __init__(self, x=0, y=0, side=0):
        self.x = x
        self.y = y
        self.side = side

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Field:
    def __init__(self, side):
        self.count = 0
        self.best_count = float('inf')
        self.side = side
        self.bin_field = [0] * side
        self.line_mask = (1 << side) - 1
        self.squares = []
        self.best_squares = []
        self.current_solution = []
        self.best_solution = []

def can_place(field, square_side, pos):
    if not (pos.x + square_side <= field.side  and pos.y + square_side <= field.side):
        return False
    line_mask = ((1 << square_side) - 1) << pos.x
    for i in range(square_side):
        if field.bin_field[pos.y + i] & line_mask:
            return False
    return True

def place(field, line_mask, square_side, y_coord):
    for i in range(square_side):
        field.bin_field[y_coord + i] |= line_mask

def remove(field, line_mask, square_side, y_coord):
    for i in range(square_side):
        field.bin_field[y_coord + i] &= ~line_mask

def get_first_free_position(field):
    for y in range(field.side):
        free = ~field.bin_field[y] & field.line_mask
        if free:
            x = (free & -free).bit_length() - 1
            return Position(x, y)
    return Position(0, 0)

def is_grid_full(field):
    for i in range(field.side):
        if (field.bin_field[i] & field.line_mask) != field.line_mask:
            return False
    return True

def get_max_square_at_position(field, pos):
    dx = field.side - pos.x
    dy = field.side - pos.y
    max_possible = min(dx, dy)
    if max_possible > field.side - 1:
        max_possible = field.side - 1

    for side in range(max_possible, 0, -1):
        if can_place(field, side, pos):
            return side
    return 0

def find_minimal_parts_recursive(field):
    if field.count >= field.best_count:
        print("Возращаемся на предыдущий шаг")
        return

    if is_grid_full(field):
        field.best_solution = field.current_solution.copy()
        field.best_count = field.count
        print(f"Лучший способ - {field.best_count} квадратов")
        return
    pos = get_first_free_position(field)
    print(f"Найдена свободная клекта - ({pos.x}, {pos.y})")
    max_side = get_max_square_at_position(field, pos)
    print(f"Максимальная сторона квадрата в данной клетке - {max_side}")
    for side in range(max_side, 0, -1):
        line_mask = ((1 << side) - 1) << pos.x

        print(f"ставим квадрат длинной {side} на позицию ({pos.x}, {pos.y})")
        place(field, line_mask, side, pos.y)
        field.current_solution.append(Square(pos.x + 1, pos.y + 1, side))
        field.count += 1

        find_minimal_parts_recursive(field)

        print(f"удаляем квадрат длинной {side} на позиции ({pos.x}, {pos.y})")
        remove(field, line_mask, side, pos.y)
        field.current_solution.pop()
        field.count -= 1

def is_prime(N):
    if N < 2:
        return 0
    for i in range(2,int(N**0.5)+1):
        if N%i==0:
            return 0
    return 1

def find_max_b(N):
    for i in range(N//2, 2, -1):
        if N%i == 0:
            return N//i


def prefill_primary(field,N):
    print("Выполяется предзаполнение")
    a = N // 2 + 1
    b = N // 2
    place(field, ((1 << a) - 1) << 0, a, 0)
    field.current_solution.append(Square(1, 1, a))
    field.count += 1
    print(f"ставим квадрат длинной {a} на позицию (1, 1)")

    place(field, ((1 << b) - 1) << 0, b, a)
    field.current_solution.append(Square(1, a + 1, b))
    field.count += 1
    print(f"ставим квадрат длинной {b} на позицию (1, {a+1})")

    place(field, ((1 << b) - 1) << a, b, 0)
    field.current_solution.append(Square(a + 1, 1, b))
    field.count += 1
    print(f"ставим квадрат длинной {b} на позицию ({a+1}, 1)")

    if (a%2):
        place(field, ((1 << 1) - 1) << b, 1, a)
        field.current_solution.append(Square(b + 1, a+1,1))
        field.count += 1
        print(f"ставим квадрат длинной 1 на позицию ({b+1}, {a+1})")

        place(field, ((1 <<2) - 1) << a, b, 2)
        field.current_solution.append(Square(a+1, b + 1,2))
        field.count += 1
        print(f"ставим квадрат длинной 2 на позицию ({a+1}, {b+1})")

    print("Выполнено предзаполнение для простых чисел")

def prefill_even(field,N):
    print("Выполяется предзаполнение")
    place(field, ((1 << N//2) - 1) << 0, N//2, 0)
    field.current_solution.append(Square(1 , 1, N//2))
    field.count += 1
    print(f"ставим квадрат длинной {N//2} на позицию (1, 1)")

    place(field, ((1 << N//2) - 1) << N//2, N//2, 0)
    field.current_solution.append(Square(1+N//2 , 1, N//2))
    field.count += 1
    print(f"ставим квадрат длинной {N//2} на позицию ({1+N//2}, 1)")

    place(field, ((1 << N//2) - 1) << 0, N//2, N//2)
    field.current_solution.append(Square(1 , 1+N//2, N//2))
    field.count += 1
    print(f"ставим квадрат длинной {N//2} на позицию (1, {1+N//2})")

    place(field, ((1 << N // 2) - 1) << N//2, N//2, N // 2)
    field.current_solution.append(Square(1 + N//2, 1 + N // 2, N // 2))
    field.count += 1
    print(f"ставим квадрат длинной {N//2} на позицию ({1+N//2}, {1+N//2})")

    print("Выполнено предзаполнение для числе кратных 2")


def prefill_three(field,N):
    print("Выполяется предзаполнение")
    b = find_max_b(N)
    a = N//b

    place(field, ((1 <<  a*(b-1)) - 1) << 0, a*(b-1), 0)
    field.current_solution.append(Square(1, 1, a*(b-1)))
    field.count += 1
    print(f"ставим квадрат длинной {a*(b-1)} на позицию (1, 1)")

    for i in range (0,b):
        place(field, ((1 << a) - 1) << N-a, a, i*a)
        field.current_solution.append(Square(N-a+1, 1+i*a, a))
        field.count += 1
        print(f"ставим квадрат длинной {a} на позицию ({N-a+1}, {1+i*a})")

    for i in range (0,b-1):
        place(field, ((1 << a) - 1) << i*a, a, N-a)
        field.current_solution.append(Square(1+i*a, N-a+1, a))
        field.count += 1
        print(f"ставим квадрат длинной {a} на позицию ({1+i*a}, {N-a+1})")

    print("Выполнено предзаполнение для числе кратных 3")

def prefill_known_patterns(field):
    N = field.side
    if is_prime(N): prefill_primary(field, N)
    elif N%2==0: prefill_even(field, N)
    elif N%3==0: prefill_three(field, N)


def reduce_to_prime_base(N):
    for p in range(3, int(N**0.5) + 1):
        if N % p == 0 and is_prime(p):
            return p, N // p

    return N, 1

def print_solution(field, scale):
    print(field.best_count)

    for sq in field.best_solution:
        x = sq.x
        y = sq.y
        s = sq.side

        if scale > 1:
            if x != 1:
                x = (x - 1) * scale + 1
            if y != 1:
                y = (y - 1) * scale + 1
            s *= scale

        print(f"{x} {y} {s}")


def find_minimum_partition():
    try:
        N = int(input())
        if N < 2 or N > 63:
            return 1
    except:
        return 1

    field = Field(N)
    scale = 1
    if (field.count == 0 and N%2):
        p, q = reduce_to_prime_base(N)

        if q > 1:
            scale = q
            N = p
            field = Field(N)
    print(f"Масштабирование - {scale}\nРассматриваем N = {N}")
    prefill_known_patterns(field)

    if not is_grid_full(field):
        find_minimal_parts_recursive(field)
    else:
        print("Поле полностью заполнено")
        field.best_solution = field.current_solution.copy()
        field.best_count = field.count
    print_solution(field, scale)


def create_graphics():
    Times = []
    Times_complex = []
    Times_primary = []
    Primary_values = []
    N_values = list(range(3, 40))
    Complex_values = []

    for N in N_values:
        field = Field(N)
        scale = 1
        start = time.perf_counter() * 1e3
        if (field.count == 0 and N % 2 and N%3):
            p, q = reduce_to_prime_base(N)

            if q > 1:
                scale = q
                N = p
                field = Field(N)
        prefill_known_patterns(field)

        if not is_grid_full(field):
            find_minimal_parts_recursive(field)
        else:
            field.best_solution = field.current_solution.copy()
            field.best_count = field.count
        end = time.perf_counter() * 1e3
        Times.append(end - start)
        if is_prime(N*scale):
            Primary_values.append(N*scale)
            Times_primary.append(end - start)
        elif scale != 1:
            Complex_values.append(N*scale)
            Times_complex.append(end - start)

    plt.figure(figsize=(6, 10))
    plt.plot(N_values, Times, 'ro-', markersize=6, linewidth=1.5, label='Все N')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Время операции (мс)', fontsize=12)
    plt.legend()
    plt.savefig('Plot.png')
    plt.show()

    plt.figure(figsize=(6, 10))
    plt.plot([N_values[i] for i in range(1, len(Times), 2)], [Times[i] for i in range(1,len(N_values), 2)], 'ro-', markersize=6, linewidth=1.5, label='N кратные 2')
    plt.plot([N_values[i] for i in range(6, len(N_values), 6)], [Times[i] for i in range(6, len(N_values), 6)], 'bo-', markersize=6, linewidth=1.5, label='N кратные 3')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Время операции (мс)', fontsize=12)
    plt.legend()
    plt.savefig('Plot_full.png')
    plt.show()

    plt.figure(figsize=(6, 10))
    plt.plot(Complex_values, Times_complex, 'ro-', markersize=6, linewidth=1.5, label='Составные N')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Время операции (мс)', fontsize=12)
    plt.legend()
    plt.savefig('Plot_complex.png')
    plt.show()

    plt.figure(figsize=(6, 10))
    plt.plot(Primary_values, Times_primary, 'ro-', markersize=6, linewidth=1.5, label='простые N')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlabel('N', fontsize=12)
    plt.ylabel('Время операции (мс)', fontsize=12)
    plt.legend()
    z = np.polyfit(Primary_values, np.log(Times_primary), 1)
    trend = np.exp(z[1]) * np.exp(z[0] * np.array(Primary_values))
    plt.plot(Primary_values, trend, 'b--', linewidth=2,
             label='Экспонента')
    plt.ylim(0, 4000)
    plt.savefig('Plot_primary.png')
    plt.show()
    print(Times)

if __name__ == "__main__":
    print("1 - Алгоритм для задаваемого N\n2 - Построение графиков")
    if (input() == "1"):
        find_minimum_partition()
    else:
        create_graphics()