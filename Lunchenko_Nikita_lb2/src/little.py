import math
import numpy as np


class Node:
    def __init__(self, matrix, d, edges_included, edges_excluded,
                 parent, str_num, col_num):
        self.matrix = matrix.copy()
        self.str_num = str_num.copy()
        self.col_num = col_num.copy()
        self.d = d
        self.edges_included = edges_included.copy()
        self.edges_excluded = edges_excluded.copy()
        self.N = len(matrix)
        self.parent = parent
        self.left = None
        self.right = None

    def find_d(self, i, j):
        original = self.matrix[i][j]
        self.matrix[i][j] = math.inf
        d = np.min(self.matrix[i]) + np.min(self.matrix[:, j])
        self.matrix[i][j] = original
        return d

    def find_heavy(self):
        d = -math.inf
        I, J = 0, 0
        for i in range(self.N):
            for j in range(self.N):
                if self.matrix[i][j] == 0:
                    regret = self.find_d(i, j)
                    if d < regret:
                        d = regret
                        I, J = i, j
        return I, J

    def privod(self):
        d = 0
        for i in range(self.N):
            m = np.min(self.matrix[i])
            if not math.isinf(m):
                d += m
                self.matrix[i] -= m
        for j in range(self.N):
            m = np.min(self.matrix[:, j])
            if not math.isinf(m) and m > 0:
                d += m
                self.matrix[:, j] -= m
        return d

    def find_chain_end(self, start_city):
        current = start_city
        while True:
            found = False
            for edge in self.edges_included:
                if edge[0] == current:
                    current = edge[1]
                    found = True
                    break
            if not found:
                break
        return current

    def find_chain_start(self, end_city):
        current = end_city
        while True:
            found = False
            for edge in self.edges_included:
                if edge[1] == current:
                    current = edge[0]
                    found = True
                    break
            if not found:
                break
        return current

    def left_tree(self, i, j):
        new_matrix = self.matrix.copy()

        from_city = self.str_num[i]
        to_city = self.col_num[j]
        chain_end = self.find_chain_end(to_city)
        chain_start = self.find_chain_start(from_city)

        if chain_end in self.str_num and chain_start in self.col_num:
            r = self.str_num.index(chain_end)
            c = self.col_num.index(chain_start)
            new_matrix[r][c] = math.inf

        new_matrix = np.delete(new_matrix, j, axis=1)
        new_matrix = np.delete(new_matrix, i, axis=0)

        new_str_num = self.str_num.copy()
        new_col_num = self.col_num.copy()

        new_str_num.pop(i)
        new_col_num.pop(j)

        new_node = Node(new_matrix, self.d,
                        self.edges_included.copy(), self.edges_excluded.copy(),
                        self, new_str_num, new_col_num)

        new_node.edges_included.append([from_city, to_city])
        if chain_end != chain_start:
            new_node.edges_excluded.append([chain_end, chain_start])
        else:
            new_node.edges_excluded.append([to_city, from_city])
        new_node.d += new_node.privod()
        self.left = new_node

    def right_tree(self, i, j):
        new_matrix = self.matrix.copy()
        new_matrix[i][j] = math.inf
        new_node = Node(new_matrix, self.d,
                        self.edges_included.copy(), self.edges_excluded.copy(),
                        self, self.str_num, self.col_num)
        new_node.edges_excluded.append([self.str_num[i], self.col_num[j]])
        new_node.d += new_node.privod()
        self.right = new_node

    def proverka(self):
        if self.N == 1:
            return 1
        for i in range(self.N):
            if np.min(self.matrix[i]) == math.inf:
                return 0
        for j in range(self.N):
            if np.min(self.matrix[:, j]) == math.inf:
                return 0
        return 1


def tree(node, N, best_path, best):
    if node is None:
        return best_path, best

    if len(node.edges_included) == N:
        if node.d < best:
            return node.edges_included.copy(), node.d
        return best_path, best

    if node.d >= best:
        return best_path, best

    if node.proverka() == 0:
        return best_path, best

    i, j = node.find_heavy()
    node.left_tree(i, j)
    node.right_tree(i, j)

    if node.left and node.right:
        if node.left.d <= node.right.d:
            best_path, best = tree(node.left, N, best_path, best)
            if node.right.d < best:
                best_path, best = tree(node.right, N, best_path, best)
        else:
            best_path, best = tree(node.right, N, best_path, best)
            if node.left.d < best:
                best_path, best = tree(node.left, N, best_path, best)
    elif node.left:
        best_path, best = tree(node.left, N, best_path, best)
    elif node.right:
        best_path, best = tree(node.right, N, best_path, best)

    return best_path, best


def build_route(edges):
    if not edges:
        return []
    nxt = {edge[0]: edge[1] for edge in edges}
    from_cities = set(nxt.keys())
    to_cities = set(nxt.values())
    start_candidates = from_cities - to_cities
    start = start_candidates.pop() if start_candidates else edges[0][0]

    route = [start]
    current = start
    while len(route) <= len(edges):
        current = nxt[current]
        route.append(current)
        if current == start:
            break
    return route


def normalize_route(route):
    route_zero = [x - 1 for x in route]
    if 0 in route_zero:
        idx = route_zero.index(0)
        route_zero = route_zero[idx:] + route_zero[1:idx + 1]
    return route_zero


def main():
    N = int(input())
    m = []
    for _ in range(N):
        row = list(map(float, input().split()))
        m.append(row)
    m = np.array(m)
    m = np.where(m == 0, math.inf, m)

    str_num = [i + 1 for i in range(N)]
    col_num = [i + 1 for i in range(N)]
    root = Node(m, 0, [], [], None, str_num, col_num)
    root.d = root.privod()

    best_path, best = tree(root, N, [], math.inf)

    if math.isinf(best):
        print("no path")
    else:
        print(int(best))
        path = normalize_route(build_route(best_path))
        print(' '.join(str(city) for city in path))


if __name__ == "__main__":
    main()