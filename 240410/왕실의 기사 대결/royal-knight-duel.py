import sys
from collections import deque

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

L, N, Q = map(int, sys.stdin.readline().split())

r = [0 for _ in range(N)]
c = [0 for _ in range(N)]
h = [0 for _ in range(N)]
w = [0 for _ in range(N)]
k = [0 for _ in range(N)]
visited = [False for _ in range(N)]

graph = []
for _ in range(L):
    l = list(map(int, sys.stdin.readline().split()))
    graph.append(l)

for i in range(N):
    r[i], c[i], h[i], w[i], k[i] = map(int, sys.stdin.readline().split())
    r[i] -= 1
    c[i] -= 1

originalK = k[:]  # 깊은 복사가 아닌 얕은 복사를 사용합니다.

def moveKnight(index, dir):
    queue = deque()
    queue.append(index)
    visited[index] = True

    while queue:
        x = queue.popleft()

        visited[x] = True

        ny = r[x] + dy[dir]
        nx = c[x] + dx[dir]

        for i in range(ny, ny + h[x]):
            for j in range(nx, nx + w[x]):
                if 0 > i or 0 > j or i >= L or j >= L: return False, [], [], []  # 체스판 밖 -> 벽

                if graph[i][j] == 2: return False, [], [], []  # 벽
                elif graph[i][j] == 1 and x != index: k[x] -= 1  # 함정

        for i in range(N):
            if visited[i] == True or k[i] <= 0: continue
            if ny + h[x] <= r[i] or r[i] + h[i] <= ny: continue  # 겹치는지 확인
            if nx + w[x] <= c[i] or c[i] + w[i] <= nx: continue  # 겹치는지 확인

            visited[i] = True
            queue.append(i)

    return True, r[:], c[:], k[:]

for _ in range(Q):
    visited = [False for _ in range(N)]
    index, dir = map(int, sys.stdin.readline().split())
    isTrue, nr, nc, nk = moveKnight(index - 1, dir)

    if isTrue:
        r = nr
        c = nc
        k = nk

answer = 0