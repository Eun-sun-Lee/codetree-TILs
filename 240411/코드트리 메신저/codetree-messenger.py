import sys
import math
N, Q = map(int, sys.stdin.readline().split())

powerOff = []

#100
def init():
    parent = l[0:8]
    parent.insert(0, 0)
    authority = l[8:]
    authority.insert(0, 0)
    return parent, authority

#200
def power(idx):
    if idx in powerOff:
        powerOff.remove(idx)
        return
    powerOff.append(idx)

#300
def changeAuthority(idx, power):
    authority[idx] = power

#400
def changeParent(idx1, idx2):
    parent[idx1], parent[idx2] = parent[idx2], parent[idx1]
    # tmp = parent[idx1]
    
    # parent[idx1] = parent[idx2]
    # parent[idx2] = tmp

#500
def receiveAlram(idx, height):
    count = 0
    # height += 1
    # print("height: ", height)
    for i in range(idx + 1, len(parent)):
        if parent[i] == idx and i not in powerOff and height <= authority[i]:
            # print(i, authority[i], height)
            count += receiveAlram(i, height + 1) + 1
    return count

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