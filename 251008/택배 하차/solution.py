import sys
import heapq

def can_put(s, N, k, w, h, c, center_r, center_c):
    result = True
    rr = -1
    # N ~ 1까지 검사
    if s == "d": # 떨어지는거라면, 현재 r 위치부터 떨어짐
        start = center_r 
        rr = center_r + h - 1
        while start+h - 1 <= N:
            possible = True
            for i in range(start, start+h, 1):
                for j in range(c, c + w):
                    if graph[i][j] != 0 and graph[i][j] != k:
                        result = False
                        possible = False
                        break
            if possible == True:
                result = True
                rr = start + h - 1
            else:
                result = False # 가장 가까운 밑으로 지나가지 못한다면 break
                break 
            start += 1

    elif s == "l":
        # print(center_r, center_c)
        for i in range(center_r, center_r - h, -1): # r: 가장 아래쪽, c: 가장 왼쪽
            for j in range(center_c, 0, -1):
                if graph[i][j] != 0 and graph[i][j] != k: # Debug: 자기자신일 때 제외
                    result = False
                    break
        
    
    elif s == "r":
        for i in range(center_r, center_r - h, -1):  # r: 가장 아래쪽, c: 가장 오른쪽
            for j in range(center_c, N + 1):
                if graph[i][j] != 0 and graph[i][j] != k:
                    result = False
                    break   

    # 있던자리부터 ~ N까지 검사
    elif s == "down": # 떨어지는거라면, 현재 r 위치부터 떨어짐
        start = center_r + 1
        rr = center_r
        while start <= N:
            possible = True
            for i in range(start, start-h, -1):
                for j in range(c, c + w):
                    if graph[i][j] != 0 and graph[i][j] != k:
                        result = False
                        possible = False
                        break
            if possible == True:
                result = True
                rr = start
            else:
                result = False # 가장 가까운 밑으로 지나가지 못한다면 break
                break 
            start += 1

    return result, rr
        

def put(N, k, w, h, c, center_r):
    for i in range(center_r, center_r-h, -1):
        for j in range(c, c + w):
            # if graph[i][j] == 0:
            graph[i][j] = k

def new_put(N, k, w, h, c, old, new):
    for i in range(old, old-h, -1):
        for j in range(c, c + w):
            graph[i][j] = 0
    for i in range(new, new-h, -1):
        for j in range(c, c + w):
            graph[i][j] = k

def remove(N, k, w, h, c, center_r):
    for i in range(center_r, center_r-h, -1):
        for j in range(c, c + w):
            graph[i][j] = 0



N, T = map(int, sys.stdin.readline().split())
heap = []
graph = [[0] * (N+1) for _ in range(N + 1)]
end = [False] * (N + 1)
end[0] = True
dic = {}

for _ in range(T):
    k, h, w, c = map(int, sys.stdin.readline().split())
    possible, rr = can_put("d", N, k, w, h, c, 1, -1)
    put(N, k, w, h, c, rr) # 1. 입력값으로 택배 쌓기
    dic[k] = [rr, h, w, c]
    heapq.heappush(heap, k)


cnt = 0
dirc = "l"
tmp = []
answer = []
while heap: # 모두 True가 될 때까지 반복
    k = heapq.heappop(heap)

    rr, h, w, c = dic[k]
    if can_put(dirc, N, k, w, h, c, rr, c)[0] == True: # Debug: 함수에서 리턴하는 첫번째 인자가 True라면
        answer.append(k)
        remove(N, k, w, h, c, rr)
        del dic[k]

        sorted_dict = dict(sorted(dic.items(), key=lambda x:x[1][0], reverse = True))

        #아래로 빼기
        for k_val, (rr_val, h_val, w_val, c_val) in sorted_dict.items():
            if rr - h >= rr_val:
                possible, new_rr = can_put("down", N, k_val, w_val, h_val, c_val, rr_val, -1)
                # if possible and new_rr != rr_val: # 더 내려갈 수 있다면 
                if new_rr != rr_val: # 더 내려갈 수 있다면 
                    new_put(N, k_val, w_val, h_val, c_val, rr_val, new_rr)
                    dic[k_val][0] = new_rr

        # 왼쪽/오른쪽으로 한번이라도 빼고 수행
        if tmp:
            for idx in tmp:
                heapq.heappush(heap, idx)
        tmp = []
        
        dirc = "r" if dirc == "l" else "l"

    else:
        tmp.append(k)


for ii in answer:
    print(ii)
