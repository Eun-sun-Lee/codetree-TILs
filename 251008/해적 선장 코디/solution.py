import heapq

class Monster:
    def __init__(self, id, attack, recovery):
        self.id = id
        self.attack = attack
        self.recovery = recovery
        self.last_attack = -float('inf') # 초기에는 언제든 공격 가능하도록 매우 작은 값으로 설정


class Game:
    def __init__(self):
        self.monsters = {} # monster class 담을 dictionary
        self.heap = []
        self.patchAttack = {}
    
    def add_monster(self, _id, _attack, _recovery):
        monster = Monster(_id, _attack, _recovery)
        self.monsters[_id] = monster 
        heapq.heappush(self.heap, (-_attack, _id))
    
    def change_attack(self, _id, _new_attack):
        self.monsters[_id].attack = _new_attack
        self.patchAttack[_id] = _new_attack 
        heapq.heappush(self.heap, (-_new_attack, _id))
    
    def battle(self, current_time):
        answer = [] # id
        tmpMonster = []
        total_attack = 0

        while self.heap and len(answer) < 5:
            mAttack, mId = heapq.heappop(self.heap)
            mAttack *= -1

            if mId in self.patchAttack:
                if mAttack != self.patchAttack[mId]:
                    continue # 수정된 몬스터 공격력 
                else:
                    del self.patchAttack[mId]
            
            if self.monsters[mId].last_attack + self.monsters[mId].recovery <= current_time:
                self.monsters[mId].last_attack = current_time
                answer.append(mId)
                total_attack += mAttack
        
            # else:
                # tmpMonster.append((-mAttack, mId))
            tmpMonster.append((-mAttack, mId))
        
        for mAttack, mId in tmpMonster: # 아직 회복 안된 몬스터나 이번 공격에 들어간 몬스터 다시 heap에 추가
            heapq.heappush(self.heap, (mAttack, mId))

        print(total_attack, end = ' ')
        print(len(answer), end = ' ')
        print(*answer)
            

# 메인 실행 부분
game = Game()

T = int(input()) # 명령의 수 입력

# 각 명령은 1시간 단위로 실행되므로, t를 현재 시간으로 사용
for t in range(1, T + 1):
    line = input().split()
    cmd = line[0]

    if cmd == '100':  # 공격 준비
        N = int(line[1])
        for _i in range(2, N * 3 + 2, 3):
            _id, power, rest = int(line[_i]), int(line[_i + 1]), int(line[_i + 2])
            game.add_monster(_id, power, rest)

    elif cmd == '200':  # 지원 요청
        _id, power, rest = int(line[1]), int(line[2]), int(line[3])
        game.add_monster(_id, power, rest)

    elif cmd == '300':  # 함포 교체
        _id, new_power = int(line[1]), int(line[2])
        game.change_attack(_id, new_power)

    elif cmd == '400':  # 공격 명령
        game.battle(t)
