def solve():
    first = input().strip()
    if not first:
        return
    start = int(first)

    rows = []
    for i in range(100):
        line = input().strip()
        if not line:
            break
        rows.append(list(map(float, line.split())))

    n = len(rows)
    matrix = rows

    INF = float('inf')
    in_mst = [False] * n
    min_edge = [INF] * n
    parent = [-1] * n
    min_edge[start] = 0

    for i in range(n):
        u = -1
        best = INF
        for v in range(n):
            if not in_mst[v] and min_edge[v] < best:
                best = min_edge[v]
                u = v
        if u == -1:
            break
        in_mst[u] = True
        for v in range(n):
            w = matrix[u][v]
            if w != -1 and not in_mst[v] and w < min_edge[v]:
                min_edge[v] = w
                parent[v] = u

    mst_adj = [[] for i in range(n)]
    for v in range(n):
        if parent[v] != -1:
            p = parent[v]
            w = matrix[p][v]
            mst_adj[p].append((v, w))
            mst_adj[v].append((p, w))

    visited = [False] * n
    euler_tour = []

    def dfs(u):
        visited[u] = True
        euler_tour.append(u)
        for v, w in sorted(mst_adj[u], key=lambda x: x[1]):
            if not visited[v]:
                dfs(v)
                euler_tour.append(u)

    dfs(start)

    order = []
    seen = [False] * n
    for v in euler_tour:
        if not seen[v]:
            seen[v] = True
            order.append(v)
    order.append(start)

    path_length = 0.0
    for i in range(len(order) - 1):
        u = order[i]
        v = order[i + 1]
        path_length += matrix[u][v]

    print(f"{path_length:.2f}")
    print(" ".join(str(x) for x in order))


if __name__ == "__main__":
    solve()