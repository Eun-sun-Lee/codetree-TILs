import sys
import math
N, Q = map(int, sys.stdin.readline().split())

powerOff = []
memo = [-1 for _ in range(N + 1)]

#100
def init():
    parent = l[0:N]
    parent.insert(0, 0)
    authority = l[N:]
    authority.insert(0, 0)
    return parent, authority

#200
def power(idx):
    if idx in powerOff:
        powerOff.remove(idx)
        memo[0] = -1
        return
    powerOff.append(idx)
    memo[0] = -1

#300
def changeAuthority(idx, power):
    authority[idx] = power
    memo[0] = -1

#400
def changeParent(idx1, idx2):
    parent[idx1], parent[idx2] = parent[idx2], parent[idx1]
    memo[0] = -1
    # authority[idx1], authority[idx2] = authority[idx2], authority[idx1]

#500
def receiveAlram(idx, height):
    
    # if N == 10 and Q == 10:
    #     print(parent, authority)
    if memo[0] != -1 and memo[idx] != -1: return memo[idx]
    else : memo[idx] = -1

    for i in range(1, len(parent)):
        # if N == 10 and Q == 10:
        #         print(i, authority[i], height)
        if parent[i] == idx and i not in powerOff:
            if height <= authority[i]:
                memo[idx] += receiveAlram(i, height + 1) + 1
            else:
                memo[idx] += receiveAlram(i, height + 1) 
    memo[0] = 0
    return memo[idx] + 1

def pathCompression(i):
    while pt[i] != i:
        pt[i] = pt[pt[i]]
        i = pt[i]
    return i

for _ in range(Q):
    l = list(map(int, sys.stdin.readline().split()))
    comm = l.pop(0)

    if comm == 100: 
        parent, authority = init()
    elif comm == 200:
        power(l[0])
    elif comm == 300:
        changeAuthority(l[0], l[1])
    elif comm == 400:
        changeParent(l[0], l[1])
    elif comm == 500:
        height = 1
        alarm = receiveAlram(l[0], height)
        print(alarm)