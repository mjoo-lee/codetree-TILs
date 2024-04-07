from collections import deque 


N,M,K = map(int, input().split())
board = [[-1 for _ in range(N+1)]] + [[-1] + list(map(int, input().split())) for _ in range(N)]

def selectWeakest(board):
    port, time, power = [float('inf'),float('inf')], float('-inf'), float('inf')
    for n in range(1,N+1):
        for m in range(1,M+1):
            if (power, -time, -(port[0]+port[1]), -port[1]) > (board[n][m], -recent[n][m], -(n+m), -m) and board[n][m] > 0:
                power, port, time = board[n][m], [n,m], recent[n][m] #업데이트
        
    return port        

def attack(board, n, m, k):
    #weakest
    weakest = [n,m]
    
    #제일 공격력 높은 포탑 선정
    port, time, power = [float('-inf'),float('-inf')], float('inf'), float('-inf')
    for n in range(1,N+1):
        for m in range(1,M+1):
            if [n,m] != weakest and (power, -time, -(port[0]+port[1]), -port[1]) < (board[n][m], -recent[n][m], -(n+m), -m,) and board[n][m] > 0:
                power, port, time = board[n][m], [n,m], recent[n][m] #업데이트
                #print("쎈거 고르는중:",port)
    
    #공격
    startR, startC = weakest[0], weakest[1]
    Power = board[startR][startC]
    halfPower = Power // 2
    #print("weakest:",startR, startC)
    #print("strongest:",port[0],port[1])
    #이동방향 설정
    if abs(port[0]-startR) < abs(startR-port[0]): 
        dr = startR-port[0]
    else:
        dr = port[0]-startR
    if abs(port[1]-startC) < abs(startC-port[1]): 
        dc = startC-port[1]
    else:
        dc = port[1]-startC
        
    
    laser = True
    path = deque()
    #1.레이저 공격 -> 우/하/좌/상
    while startR != port[0] or startC != port[1]:
        if board[startR][startC] == 0:
            laser = False
            break
        path.append((startR, startC))
        if dc > 0 and startC != port[1]: #우
            startC = (startC + 1) % (M+1)
        elif dr > 0 and startR != port[0]: #하
            startR = (startR + 1) % (N+1)
        elif dc < 0 and startC != port[1]: #좌
            startC = (startC - 1) % (M+1)
        elif dr < 0 and startR != port[0]: #상
            startR = (startR - 1) % (N+1)
        if startC == 0:
            startC = 1
        if startR == 0:
            startR = 1
    
        
    if laser:
        #print("레이저")
        #print("laser 경로:",path)
        del path[0]
        targetR, targetC = port[0], port[1] 
        
        #중간 경로 공격
        while path:
            attackR, attackC = path.popleft()
            board[attackR][attackC] -= halfPower

        #최종 목표 공격
        board[targetR][targetC] -= Power

    #2.포탄 공격
    if not laser:
        #print("포탄")
        targetR, targetC = port[0], port[1]
        #print(targetR, targetC)
        d = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        neighbor = deque()
        for dr, dc in d:
            neighR = (targetR + dr) % (N+1)
            neighC = (targetC + dc) % (M+1)
            if neighR == 0:
                neighR = 1
            elif neighR < 0:
                neighR += (N+1) 
            if neighC == 0:
                neighC = 1
            elif neighC < 0:
                neighC += (C+1)
            
            if [neighR, neighC] != port and board[neighR][neighC] != 0 and [neighR, neighC] not in neighbor: 
                neighbor.append([neighR, neighC])
    
        #주변 공격
        #print("neighbor:",neighbor)
        while neighbor:
            attackR, attackC = neighbor.popleft()
            board[attackR][attackC] -= halfPower

        #최종 목표 공격
        board[targetR][targetC] -= Power
        
    #포탑 부서짐
    for n in range(1,N+1):
        for m in range(1,M+1):
            if board[n][m] < 0:
                board[n][m] = 0

    return board, targetR, targetC

def countport(board):
    cnt = 0
    for n in range(1,N+1):
        for m in range(1,M+1):
            if board[n][m] > 0 :
                cnt += 1
    
    return cnt


recent = [[0 for _ in range(M+1)] for _ in range(N+1)]

for k in range(1,K+1):
    #print("처음 시작:", board)
    if countport(board) == 1:
        break
    
    #1. 공격자 선정 -> 공격력 증가
    weakest = selectWeakest(board)
    board[weakest[0]][weakest[1]] += (N+M)
    #print("공격자 공격력 증가:", board)
    
    #2. 공격자의 공격 & 3. 포탑 부서짐 -> 판 업데이트 
    board, targetR, targetC = attack(board, weakest[0], weakest[1], k)
    #print("공격:", board)
    
    recent[weakest[0]][weakest[1]] = k
    #4. 포탑 정비 (부서지지 않은 포탑 중 공격과 무관한 탑 공격력 + 1)
    for n in range(1,N+1):
        for m in range(1,M+1):
            if recent[n][m] < k and board[n][m] > 0 and [n,m] != [targetR, targetC]:
                board[n][m] += 1
    #print("recent:",recent)
    #print(k,"번째 턴 이후:",board)
    
#가장 강한 포탑 공격력 출력
strongest = 0
for n in range(1,N+1):
    for m in range(1,M+1):
        if strongest < board[n][m]:
            strongest = board[n][m]
print(strongest)