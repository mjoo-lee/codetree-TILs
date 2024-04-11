from collections import deque

n,m = map(int, input().split())
board = [[-1 for _ in range(n+1)]] + [[-1] + list(map(int, input().split())) for _ in range(n)]
convi = [[-1,-1]] + [list(map(int, input().split())) for _ in range(m)] #사람마다 가야할 편의점


basecamp = []
for i in range(1,n+1):
    for j in range(1,n+1):
        if board[i][j] == 1:
            basecamp.append([i,j]) #basecamp 정보

canMove = [True for _ in range(m+1)]
people = [[-1,-1] for _ in range(m+1)] #사람 위치 정보 
            
from collections import deque

def closest(targetR, targetC, t):
    d = [(-1,0),(0,-1),(0,1),(1,0)] #상좌우하
    
    
    minDist = float('inf')
    minR, minC = float('inf'), float('inf')
    for b in basecamp:
        bR, bC = b
        if (bR, bC) in prohibited:
            continue
            
        q = deque()
        q.append((bR, bC, 0))
        visited = set((bR, bC))
        
        while q:
            curR, curC, cnt = q.popleft()
            if curR == targetR and curC == targetC and (cnt, bR, bC) < (minDist, minR, minC):
                minDist = cnt
                minR, minC = bR, bC
                    
            for dr, dc in d:
                newR, newC = curR + dr, curC + dc
                if 1<=newR<=n and 1<=newC<=n and (newR, newC) not in prohibited and (newR, newC) not in visited:
                    q.append((newR, newC, cnt+1))
                    visited.add((newR, newC))

    return minR, minC


def shortestPath(startR, startC, idx):
    
    d = [(-1,0),(0,-1),(0,1),(1,0)] #상좌우하
    
    targetR, targetC = convi[idx]
    #print("target", targetR, targetC)
    visited = set()
    q = deque()
    q.append(([startR, startC], []))
    visited.add((startR, startC))
    path = []
    while q:
        [curR, curC], temp = q.popleft()
        #print("cur", curR, curC)
        if curR == targetR and curC == targetC:
            if path:
                if len(temp) < len(path):
                    path = temp
            else:
                path = temp
   
        for dr, dc in d:
            newR, newC = curR + dr, curC + dc
            #print("new", newR, newC)
            if 1<=newR<=n and 1<=newC<=n and (newR, newC) not in prohibited and (newR, newC) not in visited:
                q.append(([newR, newC], temp+[[newR, newC]]))
                visited.add((newR, newC))
    
    return path
            
            
def allout(convi, people):
    for i in range(1,m+1):
        if convi[i] != people[i]:
            return False
    
    return True
        

def move(board, t):
    global convi, info, prohibited
    

    if not canMove[t]:
        return

    startR, startC = people[t]
    targetR, targetC = convi[t] #t번째 사람이 가야할 편의점
    moved = False
    # 1. 베이스캠프로 이동
    if t <= m and not toBase[t]:
        baseR, baseC = closest(targetR, targetC, t)
        #print(baseR, baseC)
        if (baseR, baseC) not in prohibited:
            people[t] = [baseR, baseC] #베이스캠프로 이동
            toBase[t] = True
            moved = True
            if (baseR, baseC) not in prohibited:
                prohibited.add((baseR, baseC)) 
            #print("베이스캠프 이동",people)

    # 2. 편의점 향해 1칸 이동
    if not moved:
        shortest = shortestPath(people[t][0], people[t][1], t)
        #print("shortest",shortest)
        nextR, nextC = shortest.pop(0)
        people[t] = [nextR, nextC]
        #print("편의점 향해 1칸", people)

    # 3. 편의점 도착
    if people[t] == convi[t]:
        canMove[t] = False
        prohibited.add((convi[t][0], convi[t][1]))
        #print(t, "편의점 도착", people)
        return

cnt = 0
prohibited = set()
toBase = [False for _ in range(1+m)]

while not allout(convi,people):
    cnt += 1
#     print(cnt)
#     print("prohibited",prohibited)
    if cnt <= m:
        for t in range(1,cnt+1):
#             print("t",t)
#             print("처음",people)
            move(board, t)
    else:
        if not allout(convi,people):
            for t in range(1,m+1):
                move(board,t)
    
    
    
#     print("convi",convi)
#     print("people",people)
#     print("================")

print(cnt)