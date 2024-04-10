import sys
import copy
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

originalK = copy.deepcopy(k)

def moveKnight(index, dir):
    queue = deque()
    queue.append(index)
    visited[index] = True

    ny = copy.deepcopy(r)
    nx = copy.deepcopy(c)
    nk = copy.deepcopy(k)

    while queue:
        x = queue.popleft()

        visited[x] = True

        ny[x] += dy[dir]
        nx[x] += dx[dir]

        for i in range(ny[x], ny[x] + h[x]):
            for j in range(nx[x], nx[x] + w[x]):
                if 0 > i or 0 > j or i >= L or j >= L: return False, ny, nx, nk  # 체스판 밖 -> 벽

                if graph[i][j] == 2: return False, ny, nx, nk  # 벽
                elif graph[i][j] == 1 and x != index: nk[x] -= 1  # 함정
        for i in range(N):
            if visited[i] == True or nk[i] <= 0: continue
            if ny[x] + h[x] < r[i] or r[i] + h[i] < ny[x]: continue  # 겹치는지 확인
            if nx[x] + w[x] < c[i] or c[i] + w[i] < nx[x]: continue  # 겹치는지 확인

            visited[i] = True
            queue.append(i)
    return True, ny, nx, nk

for _ in range(Q):
    visited = [False for _ in range(N)]
    index, dir = map(int, sys.stdin.readline().split())
    isTrue, ny, nx, nk = moveKnight(index - 1, dir)
    # print(isTrue, ny, nx, nk)

    if isTrue:
        r = ny
        c = nx
        k = nk

answer = 0
for i in range(N):
    if k[i] > 0:
        answer += (originalK[i] - k[i])
print(answer)