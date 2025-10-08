import sys
import heapq

'''
초기에 택배 쌓을 때: d
왼쪽/오른쪽으로 택배 뺀 후 택배 떨어뜨릴 때: down
왼쪽으로 택배 뺄 때: l
오른쪽으로 택배 뺄 때: r

택배 쌓거나 뺄 수 있는지의 여부를 확인하고, 최대로 떨어뜨릴 수 있는 index와 가능 여부 반환
'''
def can_put(s, N, k, w, h, c, center_r, center_c):
    result = True
    rr = -1


    '''
    이전: N~1까지 검사 -> 택배가 떨어지는 순서과 관계없이 아래쪽부터 쌓일 우려가 있으므로 안됨.
    현재: 1~N까지 검사
    '''
    if s == "d": # 떨어지는거라면, 현재 r 위치부터 떨어짐
        start = center_r 
        rr = center_r + h - 1 # 가장 아래쪽(r이 큰) 값으로 세팅

        while start + h - 1 <= N:
            possible = True
            for i in range(start, start + h, 1):
                for j in range(c, c + w):
                    if graph[i][j] != 0 and graph[i][j] != k:
                        result = False
                        possible = False
                        break
            if possible == True: # graph[i][j] = 0이라면 rr값을 기록하고, 더 탐색
                result = True
                rr = start + h - 1
            else:
                result = False # 더이상 아래로 쌓을 수 없다면 break
                break 
            start += 1


    # 있던자리~N까지 검사
    elif s == "down": # 떨어지는거라면, 현재 r 위치부터 떨어짐
        start = center_r + 1 # 현재 위치 + 1 -> 즉, 다음 행부터 검사
        rr = center_r # 최대로 떨어진 후의 행의 초깃값: 현재 r(가장 아래쪽 행)

        while start <= N:
            possible = True
            for i in range(start, start-h, -1):
                for j in range(c, c + w):
                    if graph[i][j] != 0 and graph[i][j] != k:
                        result = False
                        possible = False
                        break
            if possible == True: # 현재 행이 가능하다면, 더 떨어질 수 있는지 탐색
                result = True
                rr = start
            else:
                result = False # 가장 가까운 밑으로 지나가지 못한다면 break
                break 
            start += 1

    elif s == "l":
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

    return result, rr
        

def put(N, k, w, h, c, center_r):
    for i in range(center_r, center_r-h, -1):
        for j in range(c, c + w):
            graph[i][j] = k

'''
택배를 떨어뜨리는 함수
1. 기존 영역의 graph 값을 0으로 설정
2. 새로 떨어질 영역의 graph 값을 고유의 번호값으로 설정
'''
def new_put(N, k, w, h, c, old, new):
    for i in range(old, old-h, -1):
        for j in range(c, c + w):
            graph[i][j] = 0
    for i in range(new, new-h, -1):
        for j in range(c, c + w):
            graph[i][j] = k

'''
택배를 왼쪽/오른쪽으로 빼내는 함수
-> 기존 영역의 graph 값을 0으로 설정
'''
def remove(N, k, w, h, c, center_r):
    for i in range(center_r, center_r-h, -1):
        for j in range(c, c + w):
            graph[i][j] = 0

'''
메인 함수
'''
N, T = map(int, sys.stdin.readline().split())
heap = []
graph = [[0] * (N+1) for _ in range(N + 1)]
dic = {}

for _ in range(T):
    k, h, w, c = map(int, sys.stdin.readline().split())
    possible, rr = can_put("d", N, k, w, h, c, 1, -1)
    put(N, k, w, h, c, rr) # 1. 입력값으로 택배 쌓기
    dic[k] = [rr, h, w, c]
    heapq.heappush(heap, k)


dirc = "l"
tmp = []
answer = []
while heap: # heap에 남아있을때까지 반복 
    k = heapq.heappop(heap) # heap에는 번호만 저장

    rr, h, w, c = dic[k] # 나머지 정보는 dictionary에서 꺼내서 사용 (rr 정보: 현재 번호의 택배가 위치한 가장 아래쪽(r이 큰) 행)
    '''
    1. heap에서 가장 작은 순서대로 꺼낸 번호를 현재 방향으로 뺄 수 있다면
    '''
    if can_put(dirc, N, k, w, h, c, rr, c)[0] == True: # Debug: 함수에서 리턴하는 첫번째 인자가 True라면
        answer.append(k)
        remove(N, k, w, h, c, rr) # 택배 제거
        del dic[k] # 택배를 빼냈으므로 dictionary에서 정보 제거

        sorted_dict = dict(sorted(dic.items(), key=lambda x:x[1][0], reverse = True))

        '''
        2. 현재 가장 아래쪽에 위치한 택배들부터 아래로 떨어뜨릴 수 있는지 검사
        '''
        for k_val, (rr_val, h_val, w_val, c_val) in sorted_dict.items():
            if rr - h >= rr_val: # 빼낸 택배보다 위쪽에 있는 택배들만 검사
                possible, new_rr = can_put("down", N, k_val, w_val, h_val, c_val, rr_val, -1)

                # if possible and new_rr != rr_val: # 더 내려갈 수 있다면 
                if new_rr != rr_val: # 만약 택배를 떨어뜨릴 수 있다면
                    new_put(N, k_val, w_val, h_val, c_val, rr_val, new_rr)
                    dic[k_val][0] = new_rr # 현재 택배가 위치한 가장 아래쪽 행 정보를 업데이트

        '''
        3. 왼쪽/오른쪽으로 물건 빼고 아래쪽으로 떨어뜨린 후, 다음 방향으로 물건을 또 빼기 위해 heap에서 뺐던 번호들 다시 삽입
        단, 이미 빼낸 택배는 제외
        '''
        # 왼쪽/오른쪽으로 한번이라도 빼고 수행
        if tmp:
            for idx in tmp:
                heapq.heappush(heap, idx)
        tmp = []
        
        dirc = "r" if dirc == "l" else "l" # 방향 전환
    '''
    4. 현재 번호를 현재 방향으로 빼낼 수 없다면 tmp 리스트에 삽입 (추후 다시 heap에 넣기 위함)
    '''
    else:
        tmp.append(k)


for ii in answer:
    print(ii)
