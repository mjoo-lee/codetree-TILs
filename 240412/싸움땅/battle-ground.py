n,m,k = map(int, input().split())
board = [[-1 for _ in range(n+1)]] + [[-1] + list(map(int, input().split())) for _ in range(n)]
guns = [[[] for _ in range(n+1)] for _ in range(n+1)]
for i in range(1,n+1):
    for j in range(1,n+1):
        if board[i][j] > 0:
            guns[i][j].append(board[i][j])
            
hp = [0 for _ in range(m+1)]
location = [(-1,-1) for _ in range(m+1)]
direction = [0 for _ in range(m+1)]
player_gun = [0 for _ in range(m+1)] #각 참가자가 가진 총 정보	
points = [0 for _ in range(m+1)]

for i in range(1,m+1):
    x,y,d,s = map(int, input().split())
    location[i] = (x,y)
    direction[i] = d
    hp[i] = s

dir_ = {0:(-1,0),1:(0,1),2:(1,0),3:(0,-1)}


def pickndrop(i):
    curR, curC = location[i]
    curr_gun = player_gun[i]
    guns[curR][curC].sort(reverse=True)
    # print("기존 board", board)
    # print("현 위치", (curR, curC), "기존 총", guns[curR][curC])
    
    if curr_gun < guns[curR][curC][0]:
        drop = curr_gun
        player_gun[i] = guns[curR][curC][0]
        del guns[curR][curC][0]
        
        guns[curR][curC].append(drop)
        
        guns[curR][curC].sort(reverse=True)
        board[curR][curC] = guns[curR][curC][0]
        
    # print("현 위치", (curR, curC), "남겨진 총", guns[curR][curC])
    # print("이후 board", board)
def fight(i):
    (curR, curC) = location[i]
    
    for j in range(1,len(location)):
        if i!=j and (curR, curC) == location[j]:
            other_player = j
            break
    
    gun1, hp1 = player_gun[i], hp[i]
    gun2, hp2 = player_gun[j], hp[j]

    if (hp1+gun1, hp1, i) < (hp2+gun2, hp2, j):
        winner = j
        loser = i
    else:
        winner = i
        loser = j
    
    # print("승자",winner,"패자",loser, "/ 포인트", abs((hp1+gun1) - (hp2+gun2)))
    #이긴 사람 포인트 획득
    points[winner] += abs((hp1+gun1) - (hp2+gun2))
    
    #진 사람 
    #1. 총내려 놓기
    guns[curR][curC].append(player_gun[loser])
    player_gun[loser] = 0
    
    #2. 원래 방향으로 이동 -> 다른 플레이어 or 범위 밖이면 오른쪽으로 90도 회전
    dr, dc = dir_[direction[loser]]
    newR, newC = curR+dr, curC+dc
    
    while ((newR, newC) in location) or (newR< 1 or newC< 1 or newR> n or newC> n): #사람있거나 범위 밖이면
        direction[loser] = (direction[loser]+1)%4
        #print("패자 방향", dir_[direction[loser]])
        dr, dc = dir_[direction[loser]] #90도 회전
        newR, newC = curR + dr, curC + dc
    
    # print("패자 이동", newR, newC)
    location[loser] = (newR, newC) #이동
    if board[newR][newC] > 0:
        pickndrop(loser)
    
    #이긴사람 총 뽑기
    pickndrop(winner)
            
    
        
def move_player(i):
    curR, curC = location[i]
    dr, dc = dir_[direction[i]]
    
    # 1. 본인이 향하는 방향 1칸 이동
    newR, newC = curR + dr, curC + dc
    if newR < 1 or newC < 1 or newR > n or newC > n:
        newR, newC = curR - dr, curC - dc
        for k,v in dir_.items():
            if v == (-dr, -dc):
                direction[i] = k #향하는 방향 업데이트
    
    # print(i,"이동 to", newR, newC)
    location[i] = (newR, newC)
    
    # 1-1. 다른 플레이어 있는지 확인 -> 없으면 총 줍기
    other = False
    for idx, elem in enumerate(location):
        if i != idx and elem == (newR, newC):
            other = True
    
    if not other:
        if board[newR][newC] > 0:
            pickndrop(i)
                
    # 1-2. 다른 플레이어 있으면 대결
    else:
        fight(i)
        

for K in range(k):
    # print(K+1, "------번째------")
    for i in range(1,m+1):
        move_player(i)
        # print("@위치", location)
        # print("@@총",player_gun)
        
for i in range(1,m+1):
    print(points[i], end=" ")